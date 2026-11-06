// Package probe observes fixed Linux host hints without network calls,
// subprocesses, Docker sockets, privileges, or filesystem mutation.
// These observations never authorize tenant execution or a host driver.
package probe

import (
	"fmt"
	"io"
	"io/fs"
	"os"
	"runtime"
	"sort"
	"strconv"
	"strings"
)

const (
	meminfoPath                 = "/proc/meminfo"
	cgroupControllersPath       = "/sys/fs/cgroup/cgroup.controllers"
	maxMeminfoBytes       int64 = 64 << 10
	maxCgroupBytes        int64 = 4 << 10
)

var dockerPaths = [...]string{"/usr/bin/docker", "/usr/local/bin/docker"}
var podmanPaths = [...]string{"/usr/bin/podman", "/usr/local/bin/podman"}

// Source is read-only and injectable. Only fixed allowlisted paths are read.
type Source interface {
	ReadLimited(path string, maxBytes int64) ([]byte, error)
	Lstat(path string) (fs.FileInfo, error)
}

type OSSource struct{}

func (OSSource) ReadLimited(path string, maxBytes int64) ([]byte, error) {
	f, err := os.Open(path)
	if err != nil {
		return nil, err
	}
	defer f.Close()
	data, err := io.ReadAll(io.LimitReader(f, maxBytes+1))
	if err != nil {
		return nil, err
	}
	if int64(len(data)) > maxBytes {
		return nil, fmt.Errorf("bounded read exceeded")
	}
	return data, nil
}
func (OSSource) Lstat(path string) (fs.FileInfo, error) { return os.Lstat(path) }

type Report struct {
	SchemaVersion              int      `json:"schema_version"`
	ProbeName                  string   `json:"probe_name"`
	RuntimeOS                  string   `json:"runtime_os"`
	RuntimeArch                string   `json:"runtime_arch"`
	LogicalCPUCountHint        int      `json:"logical_cpu_count_hint"`
	MemoryTotalBytesHint       uint64   `json:"memory_total_bytes_hint"`
	MemoryAvailableBytesHint   uint64   `json:"memory_available_bytes_hint"`
	MemoryObservation          string   `json:"memory_observation"`
	CgroupV2Controllers        []string `json:"cgroup_v2_controllers"`
	CgroupObservation          string   `json:"cgroup_observation"`
	VisibleCgroupRoot          VisibleCgroupRootHints `json:"visible_cgroup_root"`
	DockerBinaryCandidate      string   `json:"docker_binary_candidate"`
	PodmanBinaryCandidate      string   `json:"podman_binary_candidate"`
	ObservationStatus          string   `json:"observation_status"`
	Warnings                   []string `json:"warnings"`
	DriverQualification        string   `json:"driver_qualification"`
	QualifiedContainerDrivers  []string `json:"qualified_container_drivers"`
	HostIdentityVerified       bool     `json:"host_identity_verified"`
	ActorAuthorizationVerified bool     `json:"actor_authorization_verified"`
	HostCapacityBudgetVerified bool     `json:"host_capacity_budget_verified"`
	CgroupLimitsEnforced       bool     `json:"cgroup_limits_enforced"`
	ContainerRuntimeTested     bool     `json:"container_runtime_tested"`
	ReportSigned               bool     `json:"report_signed"`
	LinuxExecutionAuthorized   bool     `json:"linux_execution_authorized"`
	InstallApplyAvailable      bool     `json:"install_apply_available"`
}

// parseMeminfo accepts exact MemTotal/MemAvailable kB lines, rejecting
// duplicate, malformed, overflowing and contradictory values.
func parseMeminfo(data []byte) (total, available uint64, ok bool) {
	values := make(map[string]uint64, 2)
	for _, line := range strings.Split(string(data), "\n") {
		fields := strings.Fields(line)
		if len(fields) == 0 {
			continue
		}
		key := fields[0]
		if key != "MemTotal:" && key != "MemAvailable:" {
			continue
		}
		if len(fields) != 3 || fields[2] != "kB" {
			return 0, 0, false
		}
		if _, exists := values[key]; exists {
			return 0, 0, false
		}
		value, err := strconv.ParseUint(fields[1], 10, 64)
		if err != nil || value == 0 || value > ^uint64(0)/1024 {
			return 0, 0, false
		}
		values[key] = value * 1024
	}
	total, hasTotal := values["MemTotal:"]
	available, hasAvailable := values["MemAvailable:"]
	if !hasTotal || !hasAvailable || available > total {
		return 0, 0, false
	}
	return total, available, true
}

// A cgroup controller file is a hint, not proof of tenant confinement.
func parseControllers(data []byte) ([]string, bool) {
	fields := strings.Fields(string(data))
	if len(fields) == 0 || len(fields) > 32 {
		return []string{}, false
	}
	seen := make(map[string]bool, len(fields))
	for _, value := range fields {
		if len(value) > 32 {
			return []string{}, false
		}
		for _, c := range value {
			if !((c >= 'a' && c <= 'z') || (c >= '0' && c <= '9') || c == '_') {
				return []string{}, false
			}
		}
		seen[value] = true
	}
	result := make([]string, 0, len(seen))
	for v := range seen {
		result = append(result, v)
	}
	sort.Strings(result)
	return result, true
}

// inspectExecutable only lstat's fixed paths. A binary or symlink cannot
// establish Docker/Podman runtime compatibility, availability or safety.
func inspectExecutable(source Source, paths []string) (string, bool) {
	unknown := false
	for _, p := range paths {
		info, err := source.Lstat(p)
		if err != nil {
			if !os.IsNotExist(err) {
				unknown = true
			}
			continue
		}
		if info.Mode()&os.ModeSymlink != 0 {
			return "SYMLINK_UNVERIFIED", false
		}
		if info.Mode().IsRegular() && info.Mode()&0o111 != 0 {
			return "EXECUTABLE_FILE_UNVERIFIED", false
		}
		return "UNEXPECTED_FILE_TYPE_UNVERIFIED", false
	}
	if unknown {
		return "INSPECTION_FAILED", true
	}
	return "NOT_OBSERVED", false
}

// Inspect returns only untrusted OS hints; never verified free capacity.
func Inspect(source Source, goos, goarch string, logicalCPUs int) Report {
	r := Report{
		SchemaVersion: 1, ProbeName: "forgepanel-app-center-host-observe",
		RuntimeOS: goos, RuntimeArch: goarch, MemoryObservation: "NOT_OBSERVED",
		CgroupObservation: "NOT_OBSERVED", CgroupV2Controllers: []string{},
		DockerBinaryCandidate: "NOT_OBSERVED", PodmanBinaryCandidate: "NOT_OBSERVED",
		ObservationStatus: "INCONCLUSIVE", Warnings: []string{},
		DriverQualification: "NOT_EXECUTED", QualifiedContainerDrivers: []string{},
	}
	if goos != "linux" {
		r.VisibleCgroupRoot = newVisibleHints()
		r.ObservationStatus = "NOT_APPLICABLE"
		r.Warnings = append(r.Warnings, "linux_required")
		return r
	}
	if logicalCPUs >= 1 && logicalCPUs <= 65536 {
		r.LogicalCPUCountHint = logicalCPUs
	} else {
		r.Warnings = append(r.Warnings, "cpu_count_unavailable")
	}
	if data, err := source.ReadLimited(meminfoPath, maxMeminfoBytes); err == nil {
		if total, available, ok := parseMeminfo(data); ok {
			r.MemoryTotalBytesHint = total
			r.MemoryAvailableBytesHint = available
			r.MemoryObservation = "OS_MEMORY_HINT_UNVERIFIED"
		} else {
			r.Warnings = append(r.Warnings, "meminfo_invalid")
		}
	} else {
		r.Warnings = append(r.Warnings, "meminfo_unavailable")
	}
	if data, err := source.ReadLimited(cgroupControllersPath, maxCgroupBytes); err == nil {
		if controllers, ok := parseControllers(data); ok {
			r.CgroupV2Controllers = controllers
			r.CgroupObservation = "CGROUP_V2_FILE_OBSERVED_UNVERIFIED"
		} else {
			r.Warnings = append(r.Warnings, "cgroup_controllers_invalid")
		}
	} else {
		r.Warnings = append(r.Warnings, "cgroup_v2_unavailable")
	}
	r.VisibleCgroupRoot = observeVisibleCgroupRootHints(source, &r.Warnings)
	var failed bool
	r.DockerBinaryCandidate, failed = inspectExecutable(source, dockerPaths[:])
	if failed {
		r.Warnings = append(r.Warnings, "docker_binary_inspection_failed")
	}
	r.PodmanBinaryCandidate, failed = inspectExecutable(source, podmanPaths[:])
	if failed {
		r.Warnings = append(r.Warnings, "podman_binary_inspection_failed")
	}
	if r.LogicalCPUCountHint > 0 && r.MemoryObservation == "OS_MEMORY_HINT_UNVERIFIED" {
		r.ObservationStatus = "OS_HINTS_UNVERIFIED"
	}
	return r
}
func InspectHost() Report { return Inspect(OSSource{}, runtime.GOOS, runtime.GOARCH, runtime.NumCPU()) }
