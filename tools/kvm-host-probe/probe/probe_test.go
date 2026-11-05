package probe

import (
	"errors"
	"io/fs"
	"os"
	"reflect"
	"strings"
	"testing"
	"time"
)

type fileInfo struct{ mode fs.FileMode }

func (f fileInfo) Name() string       { return "fake" }
func (f fileInfo) Size() int64        { return 0 }
func (f fileInfo) Mode() fs.FileMode  { return f.mode }
func (f fileInfo) ModTime() time.Time { return time.Time{} }
func (f fileInfo) IsDir() bool        { return f.mode.IsDir() }
func (f fileInfo) Sys() any           { return nil }

type fakeReader struct {
	files  map[string][]byte
	stats  map[string]fs.FileInfo
	failed map[string]error
	reads  []string
}

func (f *fakeReader) ReadLimited(path string, max int64) ([]byte, error) {
	f.reads = append(f.reads, path)
	if err := f.failed[path]; err != nil {
		return nil, err
	}
	b, ok := f.files[path]
	if !ok {
		return nil, fs.ErrNotExist
	}
	if int64(len(b)) > max {
		return nil, errors.New("too large")
	}
	return b, nil
}
func (f *fakeReader) Lstat(path string) (fs.FileInfo, error) {
	f.reads = append(f.reads, path)
	if err := f.failed[path]; err != nil {
		return nil, err
	}
	i, ok := f.stats[path]
	if !ok {
		return nil, fs.ErrNotExist
	}
	return i, nil
}
func ready() *fakeReader {
	return &fakeReader{
		files:  map[string][]byte{osReleasePath: []byte("ID=debian\nVERSION_ID=\"12\"\n"), cpuInfoPath: []byte("processor : 0\nflags : fpu vmx avx\n")},
		stats:  map[string]fs.FileInfo{kvmDevicePath: fileInfo{os.ModeDevice | os.ModeCharDevice}, kvmModulePath: fileInfo{os.ModeDir}},
		failed: map[string]error{},
	}
}
func TestReadOnlyKVMHostCandidate(t *testing.T) {
	source := ready()
	r := Inspect(source, "linux", "amd64")
	if r.HostAssessment != "CANDIDATE_FOR_ISOLATED_VM_TESTS" {
		t.Fatalf("unexpected status: %+v", r)
	}
	if r.OSID != "debian" || r.OSVersion != "12" {
		t.Fatalf("OS fields: %+v", r)
	}
	if r.Qualification != "NOT_EXECUTED" || r.VMExecuted || r.SnapshotTested || r.ReportSigned || r.ResourceQuotasVerified {
		t.Fatalf("false claims: %+v", r)
	}
	allowed := []string{osReleasePath, kvmDevicePath, cpuInfoPath, kvmModulePath}
	if !reflect.DeepEqual(source.reads, allowed) {
		t.Fatalf("unexpected paths: %v", source.reads)
	}
}
func TestNoTrustedKVMWhenMissing(t *testing.T) {
	source := ready()
	delete(source.stats, kvmDevicePath)
	r := Inspect(source, "linux", "amd64")
	if r.HostAssessment != "NO_TRUSTED_KVM_DEVICE" || r.KVMDevice != "ABSENT" {
		t.Fatalf("unexpected: %+v", r)
	}
}
func TestSymlinkDeviceRejected(t *testing.T) {
	source := ready()
	source.stats[kvmDevicePath] = fileInfo{os.ModeSymlink}
	r := Inspect(source, "linux", "amd64")
	if r.KVMDevice != "UNTRUSTED_SYMLINK" || r.HostAssessment != "NO_TRUSTED_KVM_DEVICE" {
		t.Fatalf("unexpected: %+v", r)
	}
}
func TestRegularFileCannotImpersonateKVM(t *testing.T) {
	source := ready()
	source.stats[kvmDevicePath] = fileInfo{0o644}
	r := Inspect(source, "linux", "amd64")
	if r.KVMDevice != "NOT_CHAR_DEVICE" {
		t.Fatalf("unexpected: %+v", r)
	}
}
func TestFlagsMissingPreventsCandidate(t *testing.T) {
	source := ready()
	source.files[cpuInfoPath] = []byte("flags : fpu avx avx2\n")
	r := Inspect(source, "linux", "amd64")
	if r.HostAssessment != "INCONCLUSIVE" || r.CPUVirtualization != "FLAG_ABSENT" {
		t.Fatalf("unexpected: %+v", r)
	}
}
func TestFlagSubstringDoesNotSuffice(t *testing.T) {
	if got := cpuVirtualization([]byte("flags : fakevmx hypervisor"), "amd64"); got != "FLAG_ABSENT" {
		t.Fatal(got)
	}
}
func TestSVMFlag(t *testing.T) {
	if got := cpuVirtualization([]byte("flags : svm avx2"), "amd64"); got != "FLAG_PRESENT" {
		t.Fatal(got)
	}
}
func TestOtherArchNeverAssumesCPUFlag(t *testing.T) {
	source := ready()
	r := Inspect(source, "linux", "arm64")
	if r.CPUVirtualization != "UNKNOWN_FOR_ARCH" || r.HostAssessment != "INCONCLUSIVE" {
		t.Fatalf("unexpected: %+v", r)
	}
}
func TestNonLinuxSkipsHostFiles(t *testing.T) {
	src := ready()
	r := Inspect(src, "windows", "amd64")
	if r.HostAssessment != "NOT_APPLICABLE" || len(src.reads) != 0 {
		t.Fatalf("unexpected: %+v reads=%v", r, src.reads)
	}
}
func TestCPUInfoFailureUncertainty(t *testing.T) {
	src := ready()
	src.failed[cpuInfoPath] = os.ErrPermission
	r := Inspect(src, "linux", "amd64")
	if r.CPUVirtualization != "UNAVAILABLE" || r.HostAssessment != "INCONCLUSIVE" {
		t.Fatalf("unexpected: %+v", r)
	}
}
func TestDeviceStatErrorNotMisclassifiedAsAbsent(t *testing.T) {
	src := ready()
	src.failed[kvmDevicePath] = os.ErrPermission
	r := Inspect(src, "linux", "amd64")
	if r.KVMDevice != "UNKNOWN" || r.HostAssessment != "INCONCLUSIVE" {
		t.Fatalf("unexpected: %+v", r)
	}
}
func TestBadOSReleaseDoesNotLeakArbitraryString(t *testing.T) {
	src := ready()
	src.files[osReleasePath] = []byte("ID=debian\nVERSION_ID=\"12 ; SECRET=x\"\n")
	r := Inspect(src, "linux", "amd64")
	if r.OSVersion != "unknown" {
		t.Fatalf("unsafe version: %q", r.OSVersion)
	}
}
func TestOSReleaseUnavailable(t *testing.T) {
	src := ready()
	delete(src.files, osReleasePath)
	r := Inspect(src, "linux", "amd64")
	if r.OSID != "unknown" || !strings.Contains(strings.Join(r.Warnings, ","), "os_release_unavailable") {
		t.Fatalf("unexpected: %+v", r)
	}
}
func TestNoHiddenHostIdentity(t *testing.T) {
	r := Inspect(ready(), "linux", "amd64")
	if _, ok := reflect.TypeOf(r).FieldByName("Hostname"); ok {
		t.Fatal("host identity must not be collected")
	}
	if _, ok := reflect.TypeOf(r).FieldByName("IP"); ok {
		t.Fatal("IP identity must not be collected")
	}
}
