package admission

import (
	"bytes"
	"crypto/sha256"
	"encoding/hex"
	"encoding/json"
	"os"
	"path/filepath"
	"runtime"
	"strings"
	"testing"
)

func imageFixture(t *testing.T) (Policy, Request, string) {
	t.Helper()
	root := filepath.Join(t.TempDir(), "images")
	if err := os.Mkdir(root, 0o700); err != nil {
		t.Fatal(err)
	}
	image := filepath.Join(root, "baseline.qcow2")
	data := append([]byte{'Q', 'F', 'I', 0xfb, 0, 0, 0, 3}, bytes.Repeat([]byte{0x21}, 128)...)
	if err := os.WriteFile(image, data, 0o600); err != nil {
		t.Fatal(err)
	}
	sum := sha256.Sum256(data)
	policy := Policy{SchemaVersion: "1", PolicyID: "local-kvm-lab", Revision: "r1", ImageDirectory: root,
		MaxVCPUs: 4, MaxMemoryMiB: 2048, MaxDurationSeconds: 180, MaxImageBytes: 1024 * 1024}
	req := Request{SchemaVersion: "1", RunID: "case-001", ImageFilename: "baseline.qcow2", ImageFormat: "qcow2",
		ImageSHA256: hex.EncodeToString(sum[:]), VCPUs: 2, MemoryMiB: 512, DurationSeconds: 60}
	return policy, req, image
}

func expectBlocked(t *testing.T, report Result, reason string) {
	t.Helper()
	if report.Status != "BLOCKED" || len(report.Blockers) != 1 || report.Blockers[0] != reason {
		t.Fatalf("expected BLOCKED/%s, got %+v", reason, report)
	}
	if report.VMExecuted || report.ReportSigned || report.Q132SecurityGatesPassed || report.ArtifactVerified {
		t.Fatalf("blocked report falsely claims actual evidence: %+v", report)
	}
}

func TestAdmissionOnlyRequiresManualReview(t *testing.T) {
	if runtime.GOOS != "linux" || runtime.GOARCH != "amd64" || os.Geteuid() == 0 {
		t.Skip("nonroot linux/amd64 lab required")
	}
	policy, req, _ := imageFixture(t)
	report := Admit(policy, req)
	if report.Status != "REVIEW_REQUIRED" || report.Qualification != "NOT_EXECUTED" || !report.ArtifactVerified {
		t.Fatalf("unexpected: %+v", report)
	}
	if report.VMExecuted || report.ReportSigned || report.RunnerIsolated || report.ResourceQuotasEnforced || report.Q132SecurityGatesPassed || report.ImageFormatFullyValidated {
		t.Fatalf("false qualification claim: %+v", report)
	}
	if report.ImageSHA256 != req.ImageSHA256 || report.ImageBytes <= 8 {
		t.Fatal("image identity missing")
	}
	serialized, _ := json.Marshal(report)
	if bytes.Contains(serialized, []byte(policy.ImageDirectory)) {
		t.Fatal("private image directory leaked")
	}
}

func TestMisconfiguredPolicyDenied(t *testing.T) {
	p, r, _ := imageFixture(t)
	p.MaxVCPUs = 0
	expectBlocked(t, Admit(p, r), "invalid_explicit_policy")
	p, r, _ = imageFixture(t)
	p.ImageDirectory = "relative"
	expectBlocked(t, Admit(p, r), "invalid_explicit_policy")
	p, r, _ = imageFixture(t)
	p.Revision = ""
	expectBlocked(t, Admit(p, r), "invalid_explicit_policy")
}
func TestResourceRequestsMustBeWithinExplicitPolicy(t *testing.T) {
	for _, kind := range []string{"cpu", "memory", "duration", "zero"} {
		t.Run(kind, func(t *testing.T) {
			p, r, _ := imageFixture(t)
			switch kind {
			case "cpu":
				r.VCPUs = p.MaxVCPUs + 1
			case "memory":
				r.MemoryMiB = p.MaxMemoryMiB + 1
			case "duration":
				r.DurationSeconds = p.MaxDurationSeconds + 1
			case "zero":
				r.VCPUs = 0
			}
			expectBlocked(t, Admit(p, r), "resource_request_exceeds_explicit_policy")
		})
	}
}
func TestUnsafeGuestCapabilitiesDenied(t *testing.T) {
	for _, kind := range []string{"network", "shares", "privileged"} {
		t.Run(kind, func(t *testing.T) {
			p, r, _ := imageFixture(t)
			switch kind {
			case "network":
				r.NetworkEnabled = true
			case "shares":
				r.HostSharesEnabled = true
			case "privileged":
				r.Privileged = true
			}
			expectBlocked(t, Admit(p, r), "unsafe_guest_capability_requested")
		})
	}
}
func TestUnpinnedAndUnrecognizedImagesDenied(t *testing.T) {
	for _, kind := range []string{"wrong-format", "wrong-sha", "wrong-image-name", "dotdot", "slash", "bad-run"} {
		t.Run(kind, func(t *testing.T) {
			p, r, _ := imageFixture(t)
			expected := "invalid_pinned_image"
			switch kind {
			case "wrong-format":
				r.ImageFormat = "raw"
			case "wrong-sha":
				r.ImageSHA256 = "ABC"
			case "wrong-image-name":
				r.ImageFilename = "../disk.qcow2"
				expected = "invalid_image_filename"
			case "dotdot":
				r.ImageFilename = "bad..image.qcow2"
				expected = "invalid_image_filename"
			case "slash":
				r.ImageFilename = "other/disk.qcow2"
				expected = "invalid_image_filename"
			case "bad-run":
				r.RunID = "RUN_ABC"
				expected = "invalid_run_identity"
			}
			expectBlocked(t, Admit(p, r), expected)
		})
	}
}
func TestDigestMismatchDenied(t *testing.T) {
	p, r, _ := imageFixture(t)
	r.ImageSHA256 = strings.Repeat("a", 64)
	expectBlocked(t, Admit(p, r), "image_sha256_mismatch")
}
func TestSymlinkImageDenied(t *testing.T) {
	p, r, image := imageFixture(t)
	if err := os.Rename(image, image+".real"); err != nil {
		t.Fatal(err)
	}
	if err := os.Symlink(image+".real", image); err != nil {
		t.Fatal(err)
	}
	expectBlocked(t, Admit(p, r), "image_unavailable_or_unsafe")
}
func TestHardlinkedImageDenied(t *testing.T) {
	p, r, image := imageFixture(t)
	if err := os.Link(image, image+".alias"); err != nil {
		t.Fatal(err)
	}
	expectBlocked(t, Admit(p, r), "image_not_private_regular_or_within_limit")
}
func TestExecutableImageDenied(t *testing.T) {
	p, r, image := imageFixture(t)
	if err := os.Chmod(image, 0o700); err != nil {
		t.Fatal(err)
	}
	expectBlocked(t, Admit(p, r), "image_not_private_regular_or_within_limit")
}
func TestSharedImageDirectoryDenied(t *testing.T) {
	p, r, _ := imageFixture(t)
	if err := os.Chmod(p.ImageDirectory, 0o750); err != nil {
		t.Fatal(err)
	}
	expectBlocked(t, Admit(p, r), "image_directory_not_private_or_owned")
}
func TestSymlinkedImageDirectoryDenied(t *testing.T) {
	p, r, _ := imageFixture(t)
	alias := filepath.Join(t.TempDir(), "alias")
	if err := os.Symlink(p.ImageDirectory, alias); err != nil {
		t.Fatal(err)
	}
	p.ImageDirectory = alias
	expectBlocked(t, Admit(p, r), "image_directory_not_canonical")
}
func TestNoMagicDenied(t *testing.T) {
	p, r, image := imageFixture(t)
	b, _ := os.ReadFile(image)
	copy(b[:4], []byte("NOPE"))
	if err := os.WriteFile(image, b, 0o600); err != nil {
		t.Fatal(err)
	}
	expectBlocked(t, Admit(p, r), "image_qcow2_header_unrecognized")
}
func TestUnsupportedQCOWVersionDenied(t *testing.T) {
	p, r, image := imageFixture(t)
	b, _ := os.ReadFile(image)
	b[7] = 1
	if err := os.WriteFile(image, b, 0o600); err != nil {
		t.Fatal(err)
	}
	expectBlocked(t, Admit(p, r), "image_qcow2_header_unrecognized")
}
func TestImageSizeBoundDenied(t *testing.T) {
	p, r, _ := imageFixture(t)
	p.MaxImageBytes = 64
	expectBlocked(t, Admit(p, r), "image_not_private_regular_or_within_limit")
}
func TestMissingImageDenied(t *testing.T) {
	p, r, image := imageFixture(t)
	if err := os.Remove(image); err != nil {
		t.Fatal(err)
	}
	expectBlocked(t, Admit(p, r), "image_unavailable_or_unsafe")
}
func TestDecodeJSONRejectsUnknownFields(t *testing.T) {
	_, err := DecodeJSON[Policy](strings.NewReader(`{"schema_version":"1","unapproved":true}`))
	if err == nil {
		t.Fatal("unknown fields accepted")
	}
}
func TestDecodeJSONRejectsTrailingPayload(t *testing.T) {
	_, err := DecodeJSON[Request](strings.NewReader(`{} {"backdoor":true}`))
	if err == nil {
		t.Fatal("trailing payload accepted")
	}
}
func TestDecodeJSONRejectsMalformed(t *testing.T) {
	_, err := DecodeJSON[Policy](strings.NewReader(`{"schema_version":`))
	if err == nil {
		t.Fatal("bad JSON accepted")
	}
}
func TestDecodeJSONRejectsOversize(t *testing.T) {
	s := `{"schema_version":"1","extra":"` + strings.Repeat("A", int(MaxJSONBytes)) + `"}`
	_, err := DecodeJSON[Policy](strings.NewReader(s))
	if err == nil {
		t.Fatal("oversized JSON accepted")
	}
}
func TestDecodeJSONRejectsTrailingWhitespaceBeyondLimit(t *testing.T) {
	input := `{}` + strings.Repeat(" ", int(MaxJSONBytes)+1)
	_, err := DecodeJSON[Policy](strings.NewReader(input))
	if err == nil {
		t.Fatal("oversized trailing whitespace accepted")
	}
}
