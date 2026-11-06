package probe

import (
	"encoding/json"
	"errors"
	"io/fs"
	"os"
	"reflect"
	"strings"
	"testing"
	"time"
)

type fakeInfo struct{ mode fs.FileMode }

func (f fakeInfo) Name() string       { return "fixture" }
func (f fakeInfo) Size() int64        { return 0 }
func (f fakeInfo) Mode() fs.FileMode  { return f.mode }
func (f fakeInfo) ModTime() time.Time { return time.Time{} }
func (f fakeInfo) IsDir() bool        { return f.mode.IsDir() }
func (f fakeInfo) Sys() any           { return nil }

type fakeSource struct {
	files  map[string][]byte
	stats  map[string]fs.FileInfo
	errors map[string]error
	reads  []string
	bounds map[string]int64
}

func (f *fakeSource) ReadLimited(path string, max int64) ([]byte, error) {
	f.reads = append(f.reads, path)
	f.bounds[path] = max
	if err := f.errors[path]; err != nil {
		return nil, err
	}
	b, ok := f.files[path]
	if !ok {
		return nil, os.ErrNotExist
	}
	if int64(len(b)) > max {
		return nil, errors.New("too long")
	}
	return b, nil
}
func (f *fakeSource) Lstat(path string) (fs.FileInfo, error) {
	f.reads = append(f.reads, path)
	if err := f.errors[path]; err != nil {
		return nil, err
	}
	v, ok := f.stats[path]
	if !ok {
		return nil, os.ErrNotExist
	}
	return v, nil
}
func ready() *fakeSource {
	return &fakeSource{
		files: map[string][]byte{
			meminfoPath:           []byte("MemTotal: 8388608 kB\nMemFree: 123 kB\nMemAvailable: 4194304 kB\n"),
			cgroupControllersPath: []byte("memory io cpu pids cpu"),
		},
		stats: map[string]fs.FileInfo{
			dockerPaths[0]: fakeInfo{mode: 0755},
			podmanPaths[0]: fakeInfo{mode: os.ModeSymlink | 0777},
		},
		errors: map[string]error{}, bounds: map[string]int64{},
	}
}
func TestReadOnlyRealisticObservation(t *testing.T) {
	src := ready()
	r := Inspect(src, "linux", "amd64", 4)
	if r.ObservationStatus != "OS_HINTS_UNVERIFIED" || r.LogicalCPUCountHint != 4 {
		t.Fatalf("status %+v", r)
	}
	if r.MemoryTotalBytesHint != 8*1024*1024*1024 || r.MemoryAvailableBytesHint != 4*1024*1024*1024 {
		t.Fatalf("mem %+v", r)
	}
	if r.MemoryObservation != "OS_MEMORY_HINT_UNVERIFIED" || r.CgroupObservation != "CGROUP_V2_FILE_OBSERVED_UNVERIFIED" {
		t.Fatal(r)
	}
	if !reflect.DeepEqual(r.CgroupV2Controllers, []string{"cpu", "io", "memory", "pids"}) {
		t.Fatal(r.CgroupV2Controllers)
	}
	if r.DockerBinaryCandidate != "EXECUTABLE_FILE_UNVERIFIED" || r.PodmanBinaryCandidate != "SYMLINK_UNVERIFIED" {
		t.Fatal(r)
	}
	want := []string{meminfoPath, cgroupControllersPath, dockerPaths[0], podmanPaths[0]}
	if !reflect.DeepEqual(src.reads, want) {
		t.Fatalf("unapproved reads %v", src.reads)
	}
	if src.bounds[meminfoPath] != maxMeminfoBytes || src.bounds[cgroupControllersPath] != maxCgroupBytes {
		t.Fatal(src.bounds)
	}
	assertNoClaims(t, r)
}
func assertNoClaims(t *testing.T, r Report) {
	t.Helper()
	if r.DriverQualification != "NOT_EXECUTED" || len(r.QualifiedContainerDrivers) != 0 ||
		r.HostIdentityVerified || r.ActorAuthorizationVerified || r.HostCapacityBudgetVerified ||
		r.CgroupLimitsEnforced || r.ContainerRuntimeTested || r.ReportSigned ||
		r.LinuxExecutionAuthorized || r.InstallApplyAvailable {
		t.Fatalf("unverified facts promoted to authority %+v", r)
	}
}
func TestJSONNoClaim(t *testing.T) {
	r := Inspect(ready(), "linux", "amd64", 4)
	b, e := json.Marshal(r)
	if e != nil {
		t.Fatal(e)
	}
	var m map[string]any
	if e := json.Unmarshal(b, &m); e != nil {
		t.Fatal(e)
	}
	for _, k := range []string{"host_identity_verified", "actor_authorization_verified", "host_capacity_budget_verified", "cgroup_limits_enforced", "container_runtime_tested", "report_signed", "linux_execution_authorized", "install_apply_available"} {
		if m[k] != false {
			t.Fatalf("%s not false", k)
		}
	}
}
func TestNonLinuxNeverTouchesFiles(t *testing.T) {
	src := ready()
	r := Inspect(src, "darwin", "arm64", 8)
	if r.ObservationStatus != "NOT_APPLICABLE" || len(src.reads) != 0 || r.LogicalCPUCountHint != 0 {
		t.Fatal(r)
	}
	assertNoClaims(t, r)
}
func TestMissingMeminfoNeverPromotesAvailableBudget(t *testing.T) {
	src := ready()
	delete(src.files, meminfoPath)
	r := Inspect(src, "linux", "amd64", 8)
	if r.MemoryObservation != "NOT_OBSERVED" || r.MemoryAvailableBytesHint != 0 || r.ObservationStatus != "INCONCLUSIVE" {
		t.Fatal(r)
	}
	assertNoClaims(t, r)
}
func TestBoundedHostReadFailsClosed(t *testing.T) {
	src := ready()
	src.files[meminfoPath] = []byte(strings.Repeat("X", int(maxMeminfoBytes)+1))
	r := Inspect(src, "linux", "amd64", 4)
	if r.MemoryObservation != "NOT_OBSERVED" || r.MemoryAvailableBytesHint != 0 || len(r.Warnings) == 0 {
		t.Fatal(r)
	}
}
func TestDuplicateMemTotalRejected(t *testing.T) {
	for _, s := range []string{"MemTotal: 10 kB\nMemTotal: 10 kB\nMemAvailable: 4 kB", "MemTotal: 10 kB\nMemAvailable: 4 kB\nMemAvailable: 2 kB"} {
		_, _, ok := parseMeminfo([]byte(s))
		if ok {
			t.Fatalf("accepted %q", s)
		}
	}
}
func TestMalformedMeminfoRejected(t *testing.T) {
	for _, s := range []string{"MemTotal: -1 kB\nMemAvailable: 1 kB", "MemTotal: 100 B\nMemAvailable: 1 kB", "MemTotal: 100 kB\nMemAvailable: 0 kB", "MemTotal: 100 kB\nMemAvailable: 101 kB", "MemTotal: 18446744073709551615 kB\nMemAvailable: 1 kB", "MemTotal: 100 kB\nMemAvailable: 10kB", "MemTotal: 100 kB\nMemAvailable: nonsense kB", "MemTotal: 100 kB\nMemAvailable: 10 kB ignored"} {
		_, _, ok := parseMeminfo([]byte(s))
		if ok {
			t.Fatalf("accepted %q", s)
		}
	}
}
func TestMeminfoIgnoresIrrelevantLines(t *testing.T) {
	total, free, ok := parseMeminfo([]byte("Bad: whatever\nMemTotal: 1024 kB\nUnevaluated: no\nMemAvailable: 512 kB\n"))
	if !ok || total != 1024*1024 || free != 512*1024 {
		t.Fatal(total, free, ok)
	}
}
func TestEmptyControllersRejected(t *testing.T) {
	for _, s := range []string{"", "  \n", "cpu pids ../etc/passwd", "cpu CMD;evil", strings.Repeat("a", 33), strings.Repeat("cpu ", 33)} {
		_, ok := parseControllers([]byte(s))
		if ok {
			t.Fatalf("accepted %q", s)
		}
	}
}
func TestControllersDedupSorted(t *testing.T) {
	c, ok := parseControllers([]byte("pids memory cpu cpu io"))
	if !ok || !reflect.DeepEqual(c, []string{"cpu", "io", "memory", "pids"}) {
		t.Fatal(c, ok)
	}
}
func TestMissingCgroupDoesNotPretendDisabled(t *testing.T) {
	src := ready()
	delete(src.files, cgroupControllersPath)
	r := Inspect(src, "linux", "amd64", 4)
	if r.CgroupObservation != "NOT_OBSERVED" || len(r.CgroupV2Controllers) != 0 {
		t.Fatal(r)
	}
	assertNoClaims(t, r)
}
func TestBinarySymlinkNotVerified(t *testing.T) {
	src := ready()
	src.stats[dockerPaths[0]] = fakeInfo{mode: os.ModeSymlink | 0777}
	r := Inspect(src, "linux", "amd64", 4)
	if r.DockerBinaryCandidate != "SYMLINK_UNVERIFIED" {
		t.Fatal(r)
	}
	assertNoClaims(t, r)
}
func TestBinaryNonExecutableNotQualified(t *testing.T) {
	src := ready()
	src.stats[dockerPaths[0]] = fakeInfo{mode: 0644}
	r := Inspect(src, "linux", "amd64", 4)
	if r.DockerBinaryCandidate != "UNEXPECTED_FILE_TYPE_UNVERIFIED" {
		t.Fatal(r)
	}
}
func TestBinaryProbeUnknownErrorNotLeaked(t *testing.T) {
	src := ready()
	delete(src.stats, dockerPaths[0])
	src.errors[dockerPaths[0]] = errors.New("private secret in stat error")
	r := Inspect(src, "linux", "amd64", 4)
	if r.DockerBinaryCandidate != "INSPECTION_FAILED" || !strings.Contains(strings.Join(r.Warnings, ","), "docker_binary_inspection_failed") {
		t.Fatal(r)
	}
	if strings.Contains(strings.Join(r.Warnings, ","), "private secret") {
		t.Fatal("error leakage")
	}
}
func TestBothMissingBinaryMeansNoQualification(t *testing.T) {
	src := ready()
	src.stats = map[string]fs.FileInfo{}
	r := Inspect(src, "linux", "amd64", 4)
	if r.DockerBinaryCandidate != "NOT_OBSERVED" || r.PodmanBinaryCandidate != "NOT_OBSERVED" {
		t.Fatal(r)
	}
	assertNoClaims(t, r)
}
func TestMalformedCPUCountNeverGrantsCapacity(t *testing.T) {
	for _, n := range []int{-1, 0, 65537} {
		r := Inspect(ready(), "linux", "amd64", n)
		if r.LogicalCPUCountHint != 0 || r.ObservationStatus != "INCONCLUSIVE" {
			t.Fatal(n, r)
		}
		assertNoClaims(t, r)
	}
}
func TestErrorCodesDoNotContainRawPathsOrSecrets(t *testing.T) {
	src := ready()
	src.errors[meminfoPath] = errors.New("db admin secret")
	src.errors[cgroupControllersPath] = errors.New("password is secret")
	r := Inspect(src, "linux", "amd64", 4)
	raw := strings.Join(r.Warnings, " ")
	if strings.Contains(raw, "secret") || strings.Contains(raw, "password") {
		t.Fatal(raw)
	}
	assertNoClaims(t, r)
}
func TestFixedPathsAndNoDockerSocket(t *testing.T) {
	src := ready()
	_ = Inspect(src, "linux", "amd64", 2)
	for _, name := range src.reads {
		if strings.Contains(name, "sock") || name == "/" || strings.Contains(name, "/etc/shadow") {
			t.Fatal(name)
		}
	}
}
func TestCandidateBinaryLocalFallback(t *testing.T) {
	src := ready()
	delete(src.stats, dockerPaths[0])
	src.stats[dockerPaths[1]] = fakeInfo{mode: 0755}
	r := Inspect(src, "linux", "amd64", 4)
	if r.DockerBinaryCandidate != "EXECUTABLE_FILE_UNVERIFIED" {
		t.Fatal(r)
	}
}
