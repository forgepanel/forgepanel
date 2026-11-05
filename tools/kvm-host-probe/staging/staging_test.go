package staging

import (
	"bytes"
	"crypto/sha256"
	"encoding/hex"
	"encoding/json"
	"errors"
	"io"
	"os"
	"path/filepath"
	"runtime"
	"testing"

	"github.com/yyogas/forgepanel/tools/kvm-host-probe/admission"
)

func lab(t *testing.T) (admission.Policy, admission.Request, string, string) {
	t.Helper()
	if runtime.GOOS != "linux" || runtime.GOARCH != "amd64" || os.Geteuid() == 0 {
		t.Skip("nonroot Linux/amd64 lab required")
	}
	// Each source/staging root is independently owned and mode 0700.
	root := t.TempDir()
	images := filepath.Join(root, "images")
	stagingRoot := filepath.Join(root, "staged")
	for _, dir := range []string{images, stagingRoot} {
		if err := os.Mkdir(dir, 0700); err != nil {
			t.Fatal(err)
		}
	}
	image := filepath.Join(images, "base.qcow2")
	imageData := append([]byte{'Q', 'F', 'I', 0xfb, 0, 0, 0, 3}, bytes.Repeat([]byte{0x7a}, 4096)...)
	if err := os.WriteFile(image, imageData, 0600); err != nil {
		t.Fatal(err)
	}
	digest := sha256.Sum256(imageData)
	p := admission.Policy{SchemaVersion: "1", PolicyID: "local-lab", Revision: "rev-1", ImageDirectory: images, MaxVCPUs: 4, MaxMemoryMiB: 1024, MaxDurationSeconds: 120, MaxImageBytes: 1024 * 1024}
	r := admission.Request{SchemaVersion: "1", RunID: "sample-001", ImageFilename: "base.qcow2", ImageSHA256: hex.EncodeToString(digest[:]), ImageFormat: "qcow2", VCPUs: 1, MemoryMiB: 256, DurationSeconds: 30}
	return p, r, stagingRoot, image
}

func expectBlocked(t *testing.T, got Result, code string) {
	t.Helper()
	if got.Status != "BLOCKED" || len(got.Blockers) != 1 || got.Blockers[0] != code || got.VMExecuted || got.ExecutionAuthorized || got.ImmutableStorageVerified || got.ReportSigned {
		t.Fatalf("expected deny %s; got %+v", code, got)
	}
}

func TestStagedCopyMatchesPinnedBytesAndReceipt(t *testing.T) {
	p, r, root, source := lab(t)
	result := Stage(p, r, root)
	if result.Status != "STAGED_FOR_MANUAL_REVIEW" || !result.StagedBytesVerified {
		t.Fatalf("unexpected: %+v", result)
	}
	if result.Qualification != "NOT_EXECUTED" || result.VMExecuted || result.ExecutionAuthorized || result.ResourceQuotasEnforced || result.ImmutableStorageVerified || result.ReportSigned || !result.ManualReviewRequired {
		t.Fatalf("false safety claims: %+v", result)
	}
	dir := filepath.Join(root, r.RunID)
	if mode := mustStat(t, dir).Mode().Perm(); mode != 0700 {
		t.Fatalf("directory mode %o", mode)
	}
	copied := filepath.Join(dir, ImageName)
	if mode := mustStat(t, copied).Mode().Perm(); mode != 0400 {
		t.Fatalf("copied mode %o", mode)
	}
	if mode := mustStat(t, filepath.Join(dir, ReceiptName)).Mode().Perm(); mode != 0400 {
		t.Fatalf("receipt mode %o", mode)
	}
	sourceData, err := os.ReadFile(source)
	if err != nil {
		t.Fatal(err)
	}
	stagedData, err := os.ReadFile(copied)
	if err != nil {
		t.Fatal(err)
	}
	if !bytes.Equal(sourceData, stagedData) {
		t.Fatal("staged content differs")
	}
	receiptData, err := os.ReadFile(filepath.Join(dir, ReceiptName))
	if err != nil {
		t.Fatal(err)
	}
	var receipt Result
	if err := json.Unmarshal(receiptData, &receipt); err != nil {
		t.Fatal(err)
	}
	if receipt.Status != result.Status || receipt.StagedImageSHA256 != r.ImageSHA256 || receipt.StagedBytes != int64(len(stagedData)) || len(receipt.Blockers) != 0 {
		t.Fatalf("receipt: %+v", receipt)
	}
	if bytes.Contains(receiptData, []byte(p.ImageDirectory)) || bytes.Contains(receiptData, []byte(root)) {
		t.Fatal("private paths leaked")
	}
}

func mustStat(t *testing.T, path string) os.FileInfo {
	t.Helper()
	s, err := os.Lstat(path)
	if err != nil {
		t.Fatal(err)
	}
	return s
}

func TestRefuseOverwriteExistingRun(t *testing.T) {
	p, r, root, _ := lab(t)
	first := Stage(p, r, root)
	if first.Status != "STAGED_FOR_MANUAL_REVIEW" {
		t.Fatalf("initial: %+v", first)
	}
	before, _ := os.ReadFile(filepath.Join(root, r.RunID, ReceiptName))
	expectBlocked(t, Stage(p, r, root), "run_directory_already_exists_or_unavailable")
	after, _ := os.ReadFile(filepath.Join(root, r.RunID, ReceiptName))
	if !bytes.Equal(before, after) {
		t.Fatal("existing receipt changed")
	}
}
func TestRejectAlteredSourceBeforeWriting(t *testing.T) {
	p, r, root, image := lab(t)
	if err := os.WriteFile(image, bytes.Repeat([]byte{'x'}, 4096), 0600); err != nil {
		t.Fatal(err)
	}
	expectBlocked(t, Stage(p, r, root), "image_admission_failed")
	if _, err := os.Stat(filepath.Join(root, r.RunID)); !os.IsNotExist(err) {
		t.Fatalf("unexpected destination: %v", err)
	}
}
func TestRejectUnapprovedNetwork(t *testing.T) {
	p, r, root, _ := lab(t)
	r.NetworkEnabled = true
	expectBlocked(t, Stage(p, r, root), "image_admission_failed")
	if _, err := os.Stat(filepath.Join(root, r.RunID)); !os.IsNotExist(err) {
		t.Fatal("run directory created")
	}
}
func TestRejectInvalidRunID(t *testing.T) {
	p, r, root, _ := lab(t)
	r.RunID = "../danger"
	expectBlocked(t, Stage(p, r, root), "image_admission_failed")
}
func TestRejectSharedParent(t *testing.T) {
	p, r, root, _ := lab(t)
	if err := os.Chmod(root, 0750); err != nil {
		t.Fatal(err)
	}
	expectBlocked(t, Stage(p, r, root), "staging_directory_not_private_or_owned")
}
func TestRejectSymlinkedParent(t *testing.T) {
	p, r, root, _ := lab(t)
	alias := filepath.Join(t.TempDir(), "alias")
	if err := os.Symlink(root, alias); err != nil {
		t.Fatal(err)
	}
	expectBlocked(t, Stage(p, r, alias), "staging_directory_not_canonical")
}
func TestRejectNestedStagingRoot(t *testing.T) {
	p, r, _, _ := lab(t)
	nested := filepath.Join(p.ImageDirectory, "staging")
	if err := os.Mkdir(nested, 0700); err != nil {
		t.Fatal(err)
	}
	expectBlocked(t, Stage(p, r, nested), "staging_parent_not_independent")
}
func TestRejectSourceNestedUnderStagingRoot(t *testing.T) {
	p, r, _, _ := lab(t)
	root := filepath.Dir(p.ImageDirectory)
	if err := os.Chmod(root, 0700); err != nil {
		t.Fatal(err)
	}
	if !within(root, p.ImageDirectory) {
		t.Fatal("test must have source nested under candidate parent")
	}
	expectBlocked(t, Stage(p, r, root), "staging_parent_not_independent")
}
func TestRejectSourceSymlink(t *testing.T) {
	p, r, root, source := lab(t)
	if err := os.Rename(source, source+".real"); err != nil {
		t.Fatal(err)
	}
	if err := os.Symlink(source+".real", source); err != nil {
		t.Fatal(err)
	}
	expectBlocked(t, Stage(p, r, root), "image_admission_failed")
}
func TestPartialCopyFailClosedWithoutReceipt(t *testing.T) {
	p, r, root, _ := lab(t)
	injected := func(w io.Writer, src io.Reader, n int64) (int64, error) {
		count, err := io.CopyN(w, src, 32)
		if err != nil {
			return count, err
		}
		return count, errors.New("interrupted")
	}
	result := stageWithCopy(p, r, root, injected)
	if result.Status != "PARTIAL_STAGE_REQUIRES_MANUAL_CLEANUP" || result.StagedBytesVerified || !result.ManualReviewRequired {
		t.Fatalf("unexpected: %+v", result)
	}
	if _, err := os.Stat(filepath.Join(root, r.RunID, ReceiptName)); !os.IsNotExist(err) {
		t.Fatalf("partial stage has receipt: %v", err)
	}
	if mode := mustStat(t, filepath.Join(root, r.RunID)).Mode().Perm(); mode != 0700 {
		t.Fatalf("partial directory mode %o", mode)
	}
}
func TestMutationDuringCopyRefusedWithPartialMarker(t *testing.T) {
	p, r, root, source := lab(t)
	injected := func(w io.Writer, src io.Reader, n int64) (int64, error) {
		// A same-UID mutation while the source FD is live must fail.
		if err := os.WriteFile(source, bytes.Repeat([]byte{'y'}, 64), 0600); err != nil {
			t.Fatal(err)
		}
		return io.CopyN(w, src, n)
	}
	result := stageWithCopy(p, r, root, injected)
	if result.Status != "PARTIAL_STAGE_REQUIRES_MANUAL_CLEANUP" || result.StagedBytesVerified {
		t.Fatalf("unexpected: %+v", result)
	}
	if _, err := os.Stat(filepath.Join(root, r.RunID, ReceiptName)); !os.IsNotExist(err) {
		t.Fatalf("receipt incorrectly created: %v", err)
	}
}
func TestNeverReportSystemExecution(t *testing.T) {
	p, r, root, _ := lab(t)
	report := Stage(p, r, root)
	if report.Qualification != "NOT_EXECUTED" || report.VMExecuted || report.ExecutionAuthorized || report.ImmutableStorageVerified || report.ReportSigned || report.ResourceQuotasEnforced {
		t.Fatalf("false VM claim: %+v", report)
	}
}
