// Package admission checks explicitly pinned local QCOW2 test images and
// bounded VM requests. It cannot execute QEMU or certify an operating system.
package admission

import (
	"bytes"
	"crypto/sha256"
	"encoding/hex"
	"encoding/json"
	"errors"
	"io"
	"os"
	"path/filepath"
	"regexp"
	"runtime"
	"strings"
	"syscall"
)

const (
	MaxJSONBytes  int64 = 16 * 1024
	SchemaVersion       = "1"
)

var (
	runIDPattern     = regexp.MustCompile(`^[a-z0-9][a-z0-9-]{0,63}$`)
	imageNamePattern = regexp.MustCompile(`^[a-zA-Z0-9][a-zA-Z0-9._-]{0,127}\.qcow2$`)
	digestPattern    = regexp.MustCompile(`^[a-f0-9]{64}$`)
)

// The local test administrator must explicitly supply all policy bounds.
// These limits are NOT approved hosting-plan quotas or enforced VM limits.
type Policy struct {
	SchemaVersion      string `json:"schema_version"`
	PolicyID           string `json:"policy_id"`
	Revision           string `json:"revision"`
	ImageDirectory     string `json:"image_directory"`
	MaxVCPUs           int    `json:"max_vcpus"`
	MaxMemoryMiB       int    `json:"max_memory_mib"`
	MaxDurationSeconds int    `json:"max_duration_seconds"`
	MaxImageBytes      int64  `json:"max_image_bytes"`
}

type Request struct {
	SchemaVersion     string `json:"schema_version"`
	RunID             string `json:"run_id"`
	ImageFilename     string `json:"image_filename"`
	ImageSHA256       string `json:"image_sha256"`
	ImageFormat       string `json:"image_format"`
	VCPUs             int    `json:"vcpus"`
	MemoryMiB         int    `json:"memory_mib"`
	DurationSeconds   int    `json:"duration_seconds"`
	NetworkEnabled    bool   `json:"network_enabled"`
	HostSharesEnabled bool   `json:"host_shares_enabled"`
	Privileged        bool   `json:"privileged"`
}

// Even REVIEW_REQUIRED means no guest boot, isolation or signed report.
type Result struct {
	SchemaVersion             string   `json:"schema_version"`
	Tool                      string   `json:"tool"`
	Status                    string   `json:"status"`
	Qualification             string   `json:"qualification"`
	RunID                     string   `json:"run_id,omitempty"`
	PolicyID                  string   `json:"policy_id,omitempty"`
	PolicyRevision            string   `json:"policy_revision,omitempty"`
	ImageSHA256               string   `json:"image_sha256,omitempty"`
	ImageBytes                int64    `json:"image_bytes,omitempty"`
	ArtifactVerified          bool     `json:"artifact_verified"`
	VMExecuted                bool     `json:"vm_executed"`
	RunnerIsolated            bool     `json:"runner_isolated"`
	ResourceQuotasEnforced    bool     `json:"resource_quotas_enforced"`
	ImageFormatFullyValidated bool     `json:"image_format_fully_validated"`
	ReportSigned              bool     `json:"report_signed"`
	Q132SecurityGatesPassed   bool     `json:"q132_security_gates_passed"`
	Blockers                  []string `json:"blockers"`
}

func blocked(reason string) Result {
	return Result{SchemaVersion: SchemaVersion, Tool: "forgepanel-kvm-image-admission", Status: "BLOCKED",
		Qualification: "NOT_EXECUTED", Blockers: []string{reason}}
}

// DecodeJSON denies unknown fields, trailing objects and oversized content.
func DecodeJSON[T any](r io.Reader) (T, error) {
	var result T
	data, err := io.ReadAll(io.LimitReader(r, MaxJSONBytes+1))
	if err != nil || int64(len(data)) > MaxJSONBytes {
		return result, errors.New("manifest_or_policy_size_limit")
	}
	d := json.NewDecoder(bytes.NewReader(data))
	d.DisallowUnknownFields()
	if d.Decode(&result) != nil {
		return result, errors.New("invalid_manifest_or_policy")
	}
	var extra any
	if d.Decode(&extra) != io.EOF {
		return result, errors.New("invalid_trailing_data")
	}
	return result, nil
}

func validPolicy(p Policy) bool {
	return p.SchemaVersion == SchemaVersion &&
		runIDPattern.MatchString(p.PolicyID) && runIDPattern.MatchString(p.Revision) &&
		filepath.IsAbs(p.ImageDirectory) && filepath.Clean(p.ImageDirectory) == p.ImageDirectory &&
		p.MaxVCPUs > 0 && p.MaxMemoryMiB > 0 && p.MaxDurationSeconds > 0 && p.MaxImageBytes >= 8
}
func validRequest(r Request, p Policy) string {
	if r.SchemaVersion != SchemaVersion || !runIDPattern.MatchString(r.RunID) {
		return "invalid_run_identity"
	}
	if !imageNamePattern.MatchString(r.ImageFilename) || strings.HasPrefix(r.ImageFilename, ".") ||
		strings.Contains(r.ImageFilename, "..") {
		return "invalid_image_filename"
	}
	if r.ImageFormat != "qcow2" || !digestPattern.MatchString(r.ImageSHA256) {
		return "invalid_pinned_image"
	}
	if r.VCPUs < 1 || r.VCPUs > p.MaxVCPUs || r.MemoryMiB < 1 || r.MemoryMiB > p.MaxMemoryMiB ||
		r.DurationSeconds < 1 || r.DurationSeconds > p.MaxDurationSeconds {
		return "resource_request_exceeds_explicit_policy"
	}
	if r.NetworkEnabled || r.HostSharesEnabled || r.Privileged {
		return "unsafe_guest_capability_requested"
	}
	return ""
}

// Openat with O_NOFOLLOW and fstat on owned descriptors protects the final
// image path. The byte identity must still be rechecked by a future executor.
func admitImage(root, name, expected string, maxBytes int64) (int64, string) {
	canonical, err := filepath.EvalSymlinks(root)
	if err != nil || canonical != root {
		return 0, "image_directory_not_canonical"
	}
	rootFD, err := syscall.Open(root, syscall.O_RDONLY|syscall.O_DIRECTORY|syscall.O_NOFOLLOW|syscall.O_CLOEXEC, 0)
	if err != nil {
		return 0, "image_directory_unavailable"
	}
	defer syscall.Close(rootFD)
	var directory syscall.Stat_t
	if syscall.Fstat(rootFD, &directory) != nil || uint32(directory.Mode)&syscall.S_IFMT != syscall.S_IFDIR ||
		int(directory.Uid) != os.Geteuid() || directory.Mode&0o077 != 0 {
		return 0, "image_directory_not_private_or_owned"
	}
	fd, err := syscall.Openat(rootFD, name, syscall.O_RDONLY|syscall.O_NOFOLLOW|syscall.O_CLOEXEC|syscall.O_NONBLOCK, 0)
	if err != nil {
		return 0, "image_unavailable_or_unsafe"
	}
	f := os.NewFile(uintptr(fd), "verified-image")
	defer f.Close()
	var before syscall.Stat_t
	if syscall.Fstat(fd, &before) != nil || uint32(before.Mode)&syscall.S_IFMT != syscall.S_IFREG ||
		before.Nlink != 1 || int(before.Uid) != os.Geteuid() || before.Mode&0o177 != 0 ||
		before.Size < 8 || before.Size > maxBytes {
		return 0, "image_not_private_regular_or_within_limit"
	}
	header := make([]byte, 8)
	if _, err := io.ReadFull(f, header); err != nil {
		return 0, "image_header_unreadable"
	}
	if string(header[:4]) != "QFI\xfb" || !(header[4] == 0 && header[5] == 0 && header[6] == 0 && (header[7] == 2 || header[7] == 3)) {
		return 0, "image_qcow2_header_unrecognized"
	}
	h := sha256.New()
	_, _ = h.Write(header)
	n, err := io.Copy(h, io.LimitReader(f, maxBytes+1))
	if err != nil || n+8 != before.Size || n+8 > maxBytes {
		return 0, "image_changed_or_too_large_during_hash"
	}
	var after syscall.Stat_t
	if syscall.Fstat(fd, &after) != nil || before.Dev != after.Dev || before.Ino != after.Ino ||
		before.Size != after.Size || before.Mtim != after.Mtim || before.Ctim != after.Ctim {
		return 0, "image_changed_during_verification"
	}
	if hex.EncodeToString(h.Sum(nil)) != expected {
		return 0, "image_sha256_mismatch"
	}
	return before.Size, ""
}

// Admit DOES NOT start QEMU or open /dev/kvm. This is a review gate only.
func Admit(policy Policy, request Request) Result {
	if runtime.GOOS != "linux" || runtime.GOARCH != "amd64" {
		return blocked("linux_amd64_lab_required")
	}
	if os.Geteuid() == 0 {
		return blocked("root_execution_forbidden")
	}
	if !validPolicy(policy) {
		return blocked("invalid_explicit_policy")
	}
	if reason := validRequest(request, policy); reason != "" {
		return blocked(reason)
	}
	imageBytes, reason := admitImage(policy.ImageDirectory, request.ImageFilename, request.ImageSHA256, policy.MaxImageBytes)
	if reason != "" {
		return blocked(reason)
	}
	return Result{SchemaVersion: SchemaVersion, Tool: "forgepanel-kvm-image-admission", Status: "REVIEW_REQUIRED",
		Qualification: "NOT_EXECUTED", RunID: request.RunID, PolicyID: policy.PolicyID,
		PolicyRevision: policy.Revision, ImageSHA256: request.ImageSHA256, ImageBytes: imageBytes,
		ArtifactVerified: true, Blockers: []string{}}
}
