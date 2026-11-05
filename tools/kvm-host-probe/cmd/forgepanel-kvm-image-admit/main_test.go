package main

import (
	"crypto/sha256"
	"encoding/hex"
	"encoding/json"
	"os"
	"path/filepath"
	"testing"

	"github.com/yyogas/forgepanel/tools/kvm-host-probe/admission"
)

func configs(t *testing.T) (string, string) {
	t.Helper()
	dir := t.TempDir()
	imageRoot := filepath.Join(dir, "images")
	if err := os.Mkdir(imageRoot, 0o700); err != nil {
		t.Fatal(err)
	}
	image := []byte{'Q', 'F', 'I', 0xfb, 0, 0, 0, 3, 1, 2, 3, 4}
	if err := os.WriteFile(filepath.Join(imageRoot, "image.qcow2"), image, 0o600); err != nil {
		t.Fatal(err)
	}
	sum := sha256.Sum256(image)
	policy := admission.Policy{SchemaVersion: "1", PolicyID: "local-lab", Revision: "r1", ImageDirectory: imageRoot,
		MaxVCPUs: 2, MaxMemoryMiB: 512, MaxDurationSeconds: 90, MaxImageBytes: 2048}
	req := admission.Request{SchemaVersion: "1", RunID: "job-001", ImageFilename: "image.qcow2",
		ImageSHA256: hex.EncodeToString(sum[:]), ImageFormat: "qcow2", VCPUs: 1, MemoryMiB: 256, DurationSeconds: 60}
	p := filepath.Join(dir, "policy.json")
	m := filepath.Join(dir, "manifest.json")
	data, _ := json.Marshal(policy)
	if err := os.WriteFile(p, data, 0o600); err != nil {
		t.Fatal(err)
	}
	data, _ = json.Marshal(req)
	if err := os.WriteFile(m, data, 0o600); err != nil {
		t.Fatal(err)
	}
	return p, m
}
func TestCLIReportsReviewRequiredNotQualification(t *testing.T) {
	if os.Geteuid() == 0 {
		t.Skip("requires nonroot testing")
	}
	p, m := configs(t)
	code, result := run([]string{p, m})
	if code != 0 || result.Status != "REVIEW_REQUIRED" || result.Qualification != "NOT_EXECUTED" ||
		result.VMExecuted || result.RunnerIsolated || result.ReportSigned {
		t.Fatalf("unsafe: %d %+v", code, result)
	}
}
func TestCLIRequiresBothDocuments(t *testing.T) {
	code, res := run([]string{})
	if code != 2 || res.Status != "BLOCKED" {
		t.Fatalf("unexpected: %+v", res)
	}
}
func TestCLIDeniesSharedPolicy(t *testing.T) {
	if os.Geteuid() == 0 {
		t.Skip("requires nonroot testing")
	}
	p, m := configs(t)
	if err := os.Chmod(p, 0o644); err != nil {
		t.Fatal(err)
	}
	code, res := run([]string{p, m})
	if code != 2 || res.Blockers[0] != "policy_file_not_private_or_accessible" {
		t.Fatalf("unexpected: %+v", res)
	}
}
func TestCLIDeniesSymlinkedManifest(t *testing.T) {
	if os.Geteuid() == 0 {
		t.Skip("requires nonroot testing")
	}
	p, m := configs(t)
	alias := filepath.Join(filepath.Dir(m), "alias.json")
	if err := os.Symlink(m, alias); err != nil {
		t.Fatal(err)
	}
	code, res := run([]string{p, alias})
	if code != 2 || res.Blockers[0] != "manifest_file_not_private_or_accessible" {
		t.Fatalf("unexpected: %+v", res)
	}
}
func TestCLIDeniesRelativePaths(t *testing.T) {
	if os.Geteuid() == 0 {
		t.Skip("requires nonroot testing")
	}
	_, m := configs(t)
	code, res := run([]string{"policy.json", m})
	if code != 2 || res.Status != "BLOCKED" {
		t.Fatalf("unexpected: %+v", res)
	}
}
