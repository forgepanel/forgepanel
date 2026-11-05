// Package staging prepares a private, SHA-256-pinned copy of a local QCOW2
// image for manual review. It never starts QEMU or grants execution rights.
package staging

import (
	"crypto/sha256"
	"encoding/hex"
	"encoding/json"
	"io"
	"os"
	"path/filepath"
	"runtime"
	"strings"
	"syscall"

	"github.com/yyogas/forgepanel/tools/kvm-host-probe/admission"
)

const (
	SchemaVersion = "1"
	ImageName     = "image.qcow2"
	ReceiptName   = "stage-receipt.json"
)

type Result struct {
	SchemaVersion            string   `json:"schema_version"`
	Tool                     string   `json:"tool"`
	Status                   string   `json:"status"`
	Qualification            string   `json:"qualification"`
	RunID                    string   `json:"run_id,omitempty"`
	PolicyID                 string   `json:"policy_id,omitempty"`
	PolicyRevision           string   `json:"policy_revision,omitempty"`
	PolicySHA256             string   `json:"policy_sha256,omitempty"`
	RequestSHA256            string   `json:"request_sha256,omitempty"`
	RequestedVCPUs           int      `json:"requested_vcpus,omitempty"`
	RequestedMemoryMiB       int      `json:"requested_memory_mib,omitempty"`
	RequestedDurationSeconds int      `json:"requested_duration_seconds,omitempty"`
	StagedImageSHA256        string   `json:"staged_image_sha256,omitempty"`
	StagedBytes              int64    `json:"staged_bytes,omitempty"`
	StagedFilename           string   `json:"staged_filename,omitempty"`
	StagedBytesVerified      bool     `json:"staged_bytes_verified"`
	ManualReviewRequired     bool     `json:"manual_review_required"`
	ExecutionAuthorized      bool     `json:"execution_authorized"`
	ImmutableStorageVerified bool     `json:"immutable_storage_verified"`
	ResourceQuotasEnforced   bool     `json:"resource_quotas_enforced"`
	VMExecuted               bool     `json:"vm_executed"`
	ReportSigned             bool     `json:"report_signed"`
	Blockers                 []string `json:"blockers"`
}

func initial() Result {
	return Result{SchemaVersion: SchemaVersion, Tool: "forgepanel-kvm-image-stage",
		Status: "BLOCKED", Qualification: "NOT_EXECUTED", ManualReviewRequired: true,
		Blockers: []string{}}
}
func block(r Result, code string) Result {
	r.Blockers = append(r.Blockers, code)
	return r
}

// ownedPrivateDir opens a canonical, private directory using a descriptor.
// Symlinked directory names, different owners, and shared modes are denied.
func ownedPrivateDir(path string) (int, string) {
	if !filepath.IsAbs(path) || filepath.Clean(path) != path {
		return -1, "directory_not_absolute_or_clean"
	}
	canonical, err := filepath.EvalSymlinks(path)
	if err != nil || canonical != path {
		return -1, "directory_not_canonical"
	}
	fd, err := syscall.Open(path, syscall.O_RDONLY|syscall.O_DIRECTORY|syscall.O_NOFOLLOW|syscall.O_CLOEXEC, 0)
	if err != nil {
		return -1, "private_directory_unavailable"
	}
	var info syscall.Stat_t
	if syscall.Fstat(fd, &info) != nil || uint32(info.Mode)&syscall.S_IFMT != syscall.S_IFDIR || int(info.Uid) != os.Geteuid() || info.Mode&0o077 != 0 || info.Mode&06000 != 0 {
		syscall.Close(fd)
		return -1, "directory_not_private_or_owned"
	}
	return fd, ""
}

func sourceFile(dirFD int, name string, maxBytes int64) (*os.File, syscall.Stat_t, string) {
	var zero syscall.Stat_t
	fd, err := syscall.Openat(dirFD, name, syscall.O_RDONLY|syscall.O_NOFOLLOW|syscall.O_NONBLOCK|syscall.O_CLOEXEC, 0)
	if err != nil {
		return nil, zero, "image_unavailable_or_unsafe"
	}
	var info syscall.Stat_t
	if syscall.Fstat(fd, &info) != nil || uint32(info.Mode)&syscall.S_IFMT != syscall.S_IFREG || info.Nlink != 1 || int(info.Uid) != os.Geteuid() || info.Mode&0o177 != 0 || info.Mode&06000 != 0 || info.Size < 8 || info.Size > maxBytes {
		syscall.Close(fd)
		return nil, zero, "image_not_private_regular_or_bounded"
	}
	return os.NewFile(uintptr(fd), "pinned-source-image"), info, ""
}

func within(root, path string) bool {
	rel, err := filepath.Rel(root, path)
	return err == nil && rel != ".." && !strings.HasPrefix(rel, "../")
}

func sameNamedDirectory(parentFD int, name string, expected syscall.Stat_t) bool {
	fd, err := syscall.Openat(parentFD, name, syscall.O_RDONLY|syscall.O_DIRECTORY|syscall.O_NOFOLLOW|syscall.O_CLOEXEC, 0)
	if err != nil {
		return false
	}
	defer syscall.Close(fd)
	var actual syscall.Stat_t
	if syscall.Fstat(fd, &actual) != nil {
		return false
	}
	return actual.Dev == expected.Dev && actual.Ino == expected.Ino
}

// Stage uses admission's full SHA-256 review gate, then reads the source image
// again through a protected FD and re-hashes bytes while writing a private
// copy. It never overwrites a destination or uses an arbitrary command API.
func Stage(policy admission.Policy, request admission.Request, stagingParent string) Result {
	return stageWithCopy(policy, request, stagingParent, io.CopyN)
}

// stageWithCopy uses dependency injection only for deterministic failure tests;
// production always passes io.CopyN and cannot receive runtime commands.
func stageWithCopy(policy admission.Policy, request admission.Request, stagingParent string, copyN func(io.Writer, io.Reader, int64) (int64, error)) Result {
	r := initial()
	if runtime.GOOS != "linux" || runtime.GOARCH != "amd64" {
		return block(r, "linux_amd64_lab_required")
	}
	if os.Geteuid() == 0 {
		return block(r, "root_execution_forbidden")
	}
	admit := admission.Admit(policy, request)
	if admit.Status != "REVIEW_REQUIRED" {
		return block(r, "image_admission_failed")
	}
	sourceDir, code := ownedPrivateDir(policy.ImageDirectory)
	if code != "" {
		return block(r, "source_"+code)
	}
	defer syscall.Close(sourceDir)
	parentDir, code := ownedPrivateDir(stagingParent)
	if code != "" {
		return block(r, "staging_"+code)
	}
	defer syscall.Close(parentDir)
	// Source and staging roots must not contain one another.
	if within(policy.ImageDirectory, stagingParent) || within(stagingParent, policy.ImageDirectory) {
		return block(r, "staging_parent_not_independent")
	}

	source, before, code := sourceFile(sourceDir, request.ImageFilename, policy.MaxImageBytes)
	if code != "" {
		return block(r, code)
	}
	defer source.Close()

	if err := syscall.Mkdirat(parentDir, request.RunID, 0o700); err != nil {
		return block(r, "run_directory_already_exists_or_unavailable")
	}
	r.Status = "PARTIAL_STAGE_REQUIRES_MANUAL_CLEANUP"
	stageFD, err := syscall.Openat(parentDir, request.RunID, syscall.O_RDONLY|syscall.O_DIRECTORY|syscall.O_NOFOLLOW|syscall.O_CLOEXEC, 0)
	if err != nil {
		return block(r, "run_directory_not_accessible")
	}
	defer syscall.Close(stageFD)
	var created syscall.Stat_t
	if syscall.Fstat(stageFD, &created) != nil || int(created.Uid) != os.Geteuid() || created.Mode&0o077 != 0 {
		return block(r, "run_directory_not_private_or_owned")
	}

	targetFD, err := syscall.Openat(stageFD, ImageName, syscall.O_WRONLY|syscall.O_CREAT|syscall.O_EXCL|syscall.O_NOFOLLOW|syscall.O_CLOEXEC, 0o600)
	if err != nil {
		return block(r, "unable_to_create_staged_image")
	}
	target := os.NewFile(uintptr(targetFD), "staged-image")
	digest := sha256.New()
	copied, copyErr := copyN(io.MultiWriter(target, digest), source, before.Size)
	var extra [1]byte
	nExtra, extraErr := source.Read(extra[:])
	syncErr := target.Sync()
	chmodErr := target.Chmod(0o400)
	closeErr := target.Close()
	if copyErr != nil || copied != before.Size || nExtra != 0 || extraErr != io.EOF || syncErr != nil || chmodErr != nil || closeErr != nil {
		return block(r, "image_copy_incomplete_or_changed")
	}
	var after syscall.Stat_t
	if syscall.Fstat(int(source.Fd()), &after) != nil || before.Dev != after.Dev || before.Ino != after.Ino || before.Size != after.Size || before.Mtim != after.Mtim || before.Ctim != after.Ctim || before.Mode != after.Mode || before.Nlink != after.Nlink || before.Uid != after.Uid {
		return block(r, "source_image_changed_during_copy")
	}
	if hex.EncodeToString(digest.Sum(nil)) != request.ImageSHA256 {
		return block(r, "staged_image_digest_mismatch")
	}

	// Verify destination bytes through a new FD. Even this is not an immutable
	// guarantee against a future write by the same UID.
	outFD, err := syscall.Openat(stageFD, ImageName, syscall.O_RDONLY|syscall.O_NOFOLLOW|syscall.O_NONBLOCK|syscall.O_CLOEXEC, 0)
	if err != nil {
		return block(r, "staged_image_reopen_failed")
	}
	out := os.NewFile(uintptr(outFD), "staged-image-verify")
	var dst syscall.Stat_t
	dstErr := syscall.Fstat(outFD, &dst)
	check := sha256.New()
	verified, hashErr := io.Copy(check, io.LimitReader(out, policy.MaxImageBytes+1))
	var dstAfter syscall.Stat_t
	afterErr := syscall.Fstat(outFD, &dstAfter)
	outCloseErr := out.Close()
	if dstErr != nil || hashErr != nil || afterErr != nil || outCloseErr != nil || dst.Size != before.Size || verified != before.Size || int(dst.Uid) != os.Geteuid() || dst.Nlink != 1 || uint32(dst.Mode)&syscall.S_IFMT != syscall.S_IFREG || dst.Mode&0o377 != 0 || dst.Mode&06000 != 0 || dst.Dev != dstAfter.Dev || dst.Ino != dstAfter.Ino || dst.Size != dstAfter.Size || dst.Mtim != dstAfter.Mtim || dst.Ctim != dstAfter.Ctim || hex.EncodeToString(check.Sum(nil)) != request.ImageSHA256 {
		return block(r, "staged_image_integrity_failed")
	}

	if !sameNamedDirectory(parentDir, request.RunID, created) {
		return block(r, "run_directory_identity_changed")
	}
	policyJSON, _ := json.Marshal(policy)
	requestJSON, _ := json.Marshal(request)
	policyDigest := sha256.Sum256(policyJSON)
	requestDigest := sha256.Sum256(requestJSON)
	receipt := Result{SchemaVersion: SchemaVersion, Tool: "forgepanel-kvm-image-stage", Status: "STAGED_FOR_MANUAL_REVIEW", Qualification: "NOT_EXECUTED",
		RunID: request.RunID, PolicyID: policy.PolicyID, PolicyRevision: policy.Revision, PolicySHA256: hex.EncodeToString(policyDigest[:]), RequestSHA256: hex.EncodeToString(requestDigest[:]),
		RequestedVCPUs: request.VCPUs, RequestedMemoryMiB: request.MemoryMiB, RequestedDurationSeconds: request.DurationSeconds, StagedImageSHA256: request.ImageSHA256, StagedBytes: before.Size, StagedFilename: ImageName,
		StagedBytesVerified: true, ManualReviewRequired: true, Blockers: []string{}}
	receiptFD, err := syscall.Openat(stageFD, ReceiptName, syscall.O_WRONLY|syscall.O_CREAT|syscall.O_EXCL|syscall.O_NOFOLLOW|syscall.O_CLOEXEC, 0o600)
	if err != nil {
		return block(r, "unable_to_create_receipt")
	}
	receiptFile := os.NewFile(uintptr(receiptFD), "stage-receipt")
	encoder := json.NewEncoder(receiptFile)
	encoder.SetIndent("", "  ")
	writeErr := encoder.Encode(receipt)
	rsyncErr := receiptFile.Sync()
	rchmodErr := receiptFile.Chmod(0o400)
	rcloseErr := receiptFile.Close()
	if writeErr != nil || rsyncErr != nil || rchmodErr != nil || rcloseErr != nil {
		return block(r, "receipt_write_failed")
	}
	if syscall.Fsync(stageFD) != nil || syscall.Fsync(parentDir) != nil {
		return block(r, "staging_directory_sync_failed")
	}
	if !sameNamedDirectory(parentDir, request.RunID, created) {
		return block(r, "run_directory_identity_changed")
	}
	return receipt
}
