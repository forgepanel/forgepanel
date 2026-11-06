// Additional cgroup-v2 visible-mount-root hints; strictly read-only and
// explicitly NOT a process-effective or tenant-allocatable resource budget.
package probe

import (
	"strconv"
	"strings"
)

const (
	visibleCPUQuotaPath = "/sys/fs/cgroup/cpu.max"
	visibleMemoryMaxPath = "/sys/fs/cgroup/memory.max"
	visibleMemoryCurrentPath = "/sys/fs/cgroup/memory.current"
	visiblePidsMaxPath = "/sys/fs/cgroup/pids.max"
	maxCgroupTokenBytes int64 = 128
)

type VisibleCgroupRootHints struct {
	ObservationScope string `json:"observation_scope"`
	CPUQuotaState string `json:"cpu_quota_state"`
	CPUQuotaMicrosecondsHint uint64 `json:"cpu_quota_microseconds_hint"`
	CPUPeriodMicrosecondsHint uint64 `json:"cpu_period_microseconds_hint"`
	MemoryMaxState string `json:"memory_max_state"`
	MemoryLimitBytesHint uint64 `json:"memory_limit_bytes_hint"`
	MemoryCurrentState string `json:"memory_current_state"`
	MemoryUsageBytesHint uint64 `json:"memory_usage_bytes_hint"`
	PIDsMaxState string `json:"pids_max_state"`
	PIDsLimitHint uint64 `json:"pids_limit_hint"`
}

func newVisibleHints() VisibleCgroupRootHints {
	return VisibleCgroupRootHints{
		ObservationScope:"VISIBLE_MOUNT_ROOT_ONLY_UNVERIFIED",
		CPUQuotaState:"NOT_OBSERVED", MemoryMaxState:"NOT_OBSERVED",
		MemoryCurrentState:"NOT_OBSERVED", PIDsMaxState:"NOT_OBSERVED",
	}
}

func digitsOnly(raw string) bool {
	if raw == "" {
		return false
	}
	for _, digit := range raw {
		if digit < '0' || digit > '9' {
			return false
		}
	}
	return true
}

func parseLimitToken(data []byte, allowZero bool) (string, uint64) {
	fields := strings.Fields(string(data))
	if len(fields) != 1 {
		return "INVALID_TOKEN", 0
	}
	if fields[0] == "max" && !allowZero {
		return "MAX_TOKEN_UNVERIFIED", 0
	}
	if !digitsOnly(fields[0]) {
		return "INVALID_TOKEN", 0
	}
	v, err := strconv.ParseUint(fields[0], 10, 64)
	if err != nil || (!allowZero && v == 0) {
		return "INVALID_TOKEN", 0
	}
	return "NUMERIC_TOKEN_UNVERIFIED", v
}

func parseCPUQuota(data []byte) (string, uint64, uint64) {
	fields := strings.Fields(string(data))
	if len(fields) != 2 {
		return "INVALID_TOKEN", 0, 0
	}
	if !digitsOnly(fields[1]) {
		return "INVALID_TOKEN", 0, 0
	}
	period, err := strconv.ParseUint(fields[1], 10, 64)
	if err != nil || period == 0 {
		return "INVALID_TOKEN", 0, 0
	}
	if fields[0] == "max" {
		return "MAX_TOKEN_UNVERIFIED", 0, period
	}
	if !digitsOnly(fields[0]) {
		return "INVALID_TOKEN", 0, 0
	}
	quota, err := strconv.ParseUint(fields[0], 10, 64)
	if err != nil || quota == 0 {
		return "INVALID_TOKEN", 0, 0
	}
	return "NUMERIC_TOKEN_UNVERIFIED", quota, period
}

// observeVisibleCgroupRootHints deliberately reads fixed paths only; on
// cgroup mounts/namespaces these may not represent the process's effective
// restrictions or any hosting tenant. Never use them for admission.
func observeVisibleCgroupRootHints(source Source, warnings *[]string) VisibleCgroupRootHints {
	r := newVisibleHints()
	paths := []struct{
		path string
		state *string
		warning string
	}{
		{visibleCPUQuotaPath, &r.CPUQuotaState, "cgroup_cpu_max_unavailable"},
		{visibleMemoryMaxPath, &r.MemoryMaxState, "cgroup_memory_max_unavailable"},
		{visibleMemoryCurrentPath, &r.MemoryCurrentState, "cgroup_memory_current_unavailable"},
		{visiblePidsMaxPath, &r.PIDsMaxState, "cgroup_pids_max_unavailable"},
	}
	for _, p := range paths {
		data, err := source.ReadLimited(p.path, maxCgroupTokenBytes)
		if err != nil {
			*warnings = append(*warnings, p.warning)
			continue
		}
		switch p.path {
		case visibleCPUQuotaPath:
			r.CPUQuotaState, r.CPUQuotaMicrosecondsHint, r.CPUPeriodMicrosecondsHint = parseCPUQuota(data)
		case visibleMemoryMaxPath:
			r.MemoryMaxState, r.MemoryLimitBytesHint = parseLimitToken(data, false)
		case visibleMemoryCurrentPath:
			r.MemoryCurrentState, r.MemoryUsageBytesHint = parseLimitToken(data, true)
		case visiblePidsMaxPath:
			r.PIDsMaxState, r.PIDsLimitHint = parseLimitToken(data, false)
		}
		if *p.state == "INVALID_TOKEN" {
			*warnings = append(*warnings, "cgroup_root_token_invalid")
		}
	}
	return r
}
