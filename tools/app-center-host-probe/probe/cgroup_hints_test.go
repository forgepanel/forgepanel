package probe

import (
	"errors"
	"reflect"
	"strings"
	"testing"
)

func TestCgroupRootCPUQuotaNumeric(t *testing.T) {
	status, quota, period := parseCPUQuota([]byte("250000 100000\n"))
	if status != "NUMERIC_TOKEN_UNVERIFIED" || quota != 250000 || period != 100000 {
		t.Fatal(status, quota, period)
	}
}

func TestCgroupRootCPUQuotaMaxToken(t *testing.T) {
	status, quota, period := parseCPUQuota([]byte("max 100000\n"))
	if status != "MAX_TOKEN_UNVERIFIED" || quota != 0 || period != 100000 {
		t.Fatal(status, quota, period)
	}
}

func TestCgroupRootCPUQuotaRejectsMalformed(t *testing.T) {
	for _, payload := range []string{
		"", "max", "100000", "max 0", "0 100000", "-1 100000",
		"100000 0", "100000 -1", "max no", "1 2 3",
		"18446744073709551616 100000", "100000 18446744073709551616",
		"1 2\nother", "max 100000;bad", "100\x00 10000",
	} {
		with, quota, period := parseCPUQuota([]byte(payload))
		if with != "INVALID_TOKEN" || quota != 0 || period != 0 {
			t.Fatalf("accepted unsafe cpu.max %q: %s/%d/%d", payload, with, quota, period)
		}
	}
}

func TestCgroupRootLimitAndMaxTokens(t *testing.T) {
	for _, record := range []struct {
		payload string
		status string
		value uint64
	}{
		{"max\n", "MAX_TOKEN_UNVERIFIED", 0},
		{"2048\n", "NUMERIC_TOKEN_UNVERIFIED", 2048},
		{"1", "NUMERIC_TOKEN_UNVERIFIED", 1},
	} {
		state, value := parseLimitToken([]byte(record.payload), false)
		if state != record.status || value != record.value {
			t.Fatal(record, state, value)
		}
	}
}

func TestCgroupRootMemoryCurrentZeroIsObservedHint(t *testing.T) {
	state, bytes := parseLimitToken([]byte("0\n"), true)
	if state != "NUMERIC_TOKEN_UNVERIFIED" || bytes != 0 {
		t.Fatal(state, bytes)
	}
}

func TestCgroupRootNumericLimitZeroRejected(t *testing.T) {
	state, value := parseLimitToken([]byte("0\n"), false)
	if state != "INVALID_TOKEN" || value != 0 {
		t.Fatal(state, value)
	}
}

func TestCgroupRootMemoryCurrentDoesNotAcceptMax(t *testing.T) {
	state, _ := parseLimitToken([]byte("max"), true)
	if state != "INVALID_TOKEN" {
		t.Fatal(state)
	}
}

func TestCgroupRootLimitMalformedAndOverflowRejected(t *testing.T) {
	for _, s := range []string{
		"", "-1", "+5", "max 1024", "1234 ignored", "1\n3", 
		"18446744073709551616", "5/7", "0.5", "CPU",
	} {
		state, value := parseLimitToken([]byte(s), false)
		if state != "INVALID_TOKEN" || value != 0 {
			t.Fatalf("accepted %q as %s %d", s, state, value)
		}
	}
}

func TestCgroupRootVisibleHintsAreNotTenantEntitlement(t *testing.T) {
	src := ready()
	obs := observeVisibleCgroupRootHints(src, &[]string{})
	if obs.ObservationScope != "VISIBLE_MOUNT_ROOT_ONLY_UNVERIFIED" ||
		obs.CPUQuotaState != "NUMERIC_TOKEN_UNVERIFIED" ||
		obs.MemoryMaxState != "NUMERIC_TOKEN_UNVERIFIED" ||
		obs.PIDsMaxState != "MAX_TOKEN_UNVERIFIED" {
		t.Fatal(obs)
	}
	rep := Inspect(src, "linux", "amd64", 4)
	assertNoClaims(t, rep)
}

func TestCgroupRootTokensMissingDoNotCreateFakeLimits(t *testing.T) {
	src := ready()
	delete(src.files, visibleCPUQuotaPath)
	delete(src.files, visibleMemoryMaxPath)
	delete(src.files, visibleMemoryCurrentPath)
	delete(src.files, visiblePidsMaxPath)
	var warnings []string
	r := observeVisibleCgroupRootHints(src, &warnings)
	if r.CPUQuotaState != "NOT_OBSERVED" ||
		r.MemoryMaxState != "NOT_OBSERVED" ||
		r.MemoryCurrentState != "NOT_OBSERVED" ||
		r.PIDsMaxState != "NOT_OBSERVED" ||
		r.CPUQuotaMicrosecondsHint != 0 || r.MemoryLimitBytesHint != 0 ||
		r.MemoryUsageBytesHint != 0 || r.PIDsLimitHint != 0 || len(warnings) != 4 {
		t.Fatal(r, warnings)
	}
}

func TestCgroupRootTokenParseErrorHidesRawInput(t *testing.T) {
	src := ready()
	src.files[visibleCPUQuotaPath] = []byte("rm -rf /\n")
	var warnings []string
	r := observeVisibleCgroupRootHints(src, &warnings)
	if r.CPUQuotaState != "INVALID_TOKEN" || strings.Contains(strings.Join(warnings, " "), "rm -rf") {
		t.Fatal(r, warnings)
	}
}

func TestCgroupRootReadErrorIsRedacted(t *testing.T) {
	src := ready()
	src.errors[visibleMemoryMaxPath] = errors.New("private API key")
	var warnings []string
	r := observeVisibleCgroupRootHints(src, &warnings)
	if r.MemoryMaxState != "NOT_OBSERVED" || !strings.Contains(strings.Join(warnings, " "), "cgroup_memory_max_unavailable") {
		t.Fatal(r, warnings)
	}
	if strings.Contains(strings.Join(warnings, " "), "private") {
		t.Fatal("leaked private error")
	}
}

func TestCgroupRootFixedPathsAndBoundedBytes(t *testing.T) {
	src := ready()
	_ = Inspect(src, "linux", "amd64", 2)
	want := []string{visibleCPUQuotaPath, visibleMemoryMaxPath, visibleMemoryCurrentPath, visiblePidsMaxPath}
	for _, path := range want {
		if src.bounds[path] != maxCgroupTokenBytes {
			t.Fatalf("unbounded read of %s: %d", path, src.bounds[path])
		}
	}
	if !reflect.DeepEqual(src.reads[2:6], want) {
		t.Fatalf("unexpected cgroup paths %v", src.reads)
	}
}

func TestCgroupRootOversizeReadFailsWithoutQuota(t *testing.T) {
	src := ready()
	src.files[visibleMemoryMaxPath] = []byte(strings.Repeat("1", int(maxCgroupTokenBytes)+1))
	var warnings []string
	r := observeVisibleCgroupRootHints(src, &warnings)
	if r.MemoryMaxState != "NOT_OBSERVED" || r.MemoryLimitBytesHint != 0 {
		t.Fatal(r)
	}
}

func TestNonLinuxCgroupRootRemainsUnobserved(t *testing.T) {
	src := ready()
	r := Inspect(src, "windows", "amd64", 4)
	if r.VisibleCgroupRoot.CPUQuotaState != "NOT_OBSERVED" ||
		r.VisibleCgroupRoot.MemoryMaxState != "NOT_OBSERVED" || len(src.reads) != 0 {
		t.Fatal(r, src.reads)
	}
}
