package main

import (
	"bytes"
	"crypto/sha256"
	"encoding/hex"
	"encoding/json"
	"os"
	"path/filepath"
	"runtime"
	"testing"

	"github.com/yyogas/forgepanel/tools/kvm-host-probe/admission"
)

func prepare(t *testing.T) (string, string, string) {
	t.Helper()
	if runtime.GOOS != "linux" || runtime.GOARCH != "amd64" || os.Geteuid() == 0 {
		t.Skip("nonroot Linux/amd64 required")
	}
	root := t.TempDir()
	imgRoot := filepath.Join(root, "img")
	staging := filepath.Join(root, "out")
	if err := os.Mkdir(imgRoot, 0700); err != nil {
		t.Fatal(err)
	}
	if err := os.Mkdir(staging, 0700); err != nil {
		t.Fatal(err)
	}
	content := append([]byte{'Q', 'F', 'I', 0xfb, 0, 0, 0, 3}, bytes.Repeat([]byte{0x20}, 96)...)
	if err := os.WriteFile(filepath.Join(imgRoot, "test.qcow2"), content, 0600); err != nil {
		t.Fatal(err)
	}
	hash := sha256.Sum256(content)
	policy := admission.Policy{SchemaVersion: "1", PolicyID: "local", Revision: "r1", ImageDirectory: imgRoot, MaxVCPUs: 2, MaxMemoryMiB: 1024, MaxDurationSeconds: 60, MaxImageBytes: 2048}
	request := admission.Request{SchemaVersion: "1", RunID: "run-001", ImageFilename: "test.qcow2", ImageSHA256: hex.EncodeToString(hash[:]), ImageFormat: "qcow2", VCPUs: 1, MemoryMiB: 256, DurationSeconds: 30}
	policyPath := filepath.Join(root, "policy.json")
	requestPath := filepath.Join(root, "request.json")
	p, _ := json.Marshal(policy)
	r, _ := json.Marshal(request)
	if err := os.WriteFile(policyPath, p, 0600); err != nil {
		t.Fatal(err)
	}
	if err := os.WriteFile(requestPath, r, 0600); err != nil {
		t.Fatal(err)
	}
	return policyPath, requestPath, staging
}
func TestNoArgumentsDenies(t *testing.T) {
	code, r := run(nil)
	if code != 2 || r.Status != "BLOCKED" || r.Qualification != "NOT_EXECUTED" {
		t.Fatalf("unexpected %+v", r)
	}
}
func TestValidCLIStagesWithoutExecution(t *testing.T) {
	p, r, out := prepare(t)
	code, report := run([]string{p, r, out})
	if code != 0 || report.Status != "STAGED_FOR_MANUAL_REVIEW" || !report.StagedBytesVerified || report.VMExecuted || report.ExecutionAuthorized || report.ImmutableStorageVerified {
		t.Fatalf("unsafe result %+v code=%d", report, code)
	}
}
func TestSharedPolicyDenied(t *testing.T) {
	p, r, out := prepare(t)
	if err := os.Chmod(p, 0644); err != nil {
		t.Fatal(err)
	}
	code, report := run([]string{p, r, out})
	if code != 2 || report.Blockers[0] != "policy_not_private_or_accessible" {
		t.Fatalf("unexpected %+v", report)
	}
}
func TestSymlinkRequestDenied(t *testing.T) {
	p, r, out := prepare(t)
	alias := filepath.Join(filepath.Dir(r), "request-link.json")
	if err := os.Symlink(r, alias); err != nil {
		t.Fatal(err)
	}
	code, report := run([]string{p, alias, out})
	if code != 2 || report.Blockers[0] != "request_not_private_or_accessible" {
		t.Fatalf("unexpected %+v", report)
	}
}
func TestTrailingJSONDenied(t *testing.T) {
	p, r, out := prepare(t)
	f, err := os.OpenFile(r, os.O_APPEND|os.O_WRONLY, 0)
	if err != nil {
		t.Fatal(err)
	}
	if _, err := f.WriteString(" {} "); err != nil {
		t.Fatal(err)
	}
	f.Close()
	code, report := run([]string{p, r, out})
	if code != 2 || report.Blockers[0] != "invalid_request_json" {
		t.Fatalf("unexpected %+v", report)
	}
}
func TestRelativePathDenied(t *testing.T) {
	_, r, out := prepare(t)
	code, report := run([]string{"policy.json", r, out})
	if code != 2 || report.Blockers[0] != "policy_not_private_or_accessible" {
		t.Fatalf("unexpected %+v", report)
	}
}
