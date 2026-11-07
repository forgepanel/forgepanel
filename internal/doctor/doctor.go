//go:build linux

package doctor

import (
	"bufio"
	"encoding/json"
	"fmt"
	"forgepanel.dev/core/internal/installer"
	"os"
	"os/exec"
	"runtime"
	"strings"
	"time"
)

type Result string

const (
	Pass Result = "PASS"
	Warn Result = "WARN"
	Fail Result = "FAIL"
)

type Check struct {
	ID      string `json:"id"`
	Result  Result `json:"result"`
	Message string `json:"message"`
}

type Summary struct {
	Passed   int `json:"passed"`
	Warnings int `json:"warnings"`
	Failures int `json:"failures"`
}

type Report struct {
	SchemaVersion int       `json:"schema_version"`
	GeneratedAt   time.Time `json:"generated_at"`
	Checks        []Check   `json:"checks"`
	Summary       Summary   `json:"summary"`
}

func (r *Report) add(id string, result Result, message string) {
	r.Checks = append(r.Checks, Check{ID: id, Result: result, Message: message})
	switch result {
	case Pass:
		r.Summary.Passed++
	case Warn:
		r.Summary.Warnings++
	case Fail:
		r.Summary.Failures++
	}
}

func ParseOSRelease(contents string) map[string]string {
	m := make(map[string]string)
	sc := bufio.NewScanner(strings.NewReader(contents))
	for sc.Scan() {
		line := strings.TrimSpace(sc.Text())
		if line == "" || strings.HasPrefix(line, "#") {
			continue
		}
		k, v, ok := strings.Cut(line, "=")
		if !ok {
			continue
		}
		k, v = strings.TrimSpace(k), strings.TrimSpace(v)
		if strings.HasPrefix(v, `"`) && strings.HasSuffix(v, `"`) && len(v) >= 2 {
			v = v[1 : len(v)-1]
		}
		m[k] = v
	}
	return m
}

func SupportedOS(id, version string) bool {
	return installer.Targeted(installer.Facts{ID: id, Version: version, Architecture: "amd64"})
}

func Run() Report {
	r := Report{SchemaVersion: 1, GeneratedAt: time.Now().UTC(), Checks: make([]Check, 0, 8)}
	contents, err := os.ReadFile("/etc/os-release")
	osid, version := "", ""
	if err != nil {
		r.add("os.detect", Fail, "Cannot read /etc/os-release")
	} else {
		facts := ParseOSRelease(string(contents))
		osid, version = facts["ID"], facts["VERSION_ID"]
		if SupportedOS(osid, version) {
			r.add("os.support", Pass, fmt.Sprintf("Targeted OS: %s %s (not yet certified)", osid, version))
		} else {
			r.add("os.support", Fail, fmt.Sprintf("Unsupported/unknown OS: %s %s", osid, version))
		}
	}
	if runtime.GOARCH == "amd64" {
		r.add("arch", Pass, "linux/amd64 target")
	} else {
		r.add("arch", Warn, "Architecture "+runtime.GOARCH+" needs validation")
	}
	if _, err := os.Stat("/run/systemd/system"); err == nil {
		r.add("systemd", Pass, "systemd runtime directory detected")
	} else {
		r.add("systemd", Warn, "systemd does not appear to be PID 1 (possibly a container)")
	}
	binary := "apt-get"
	if osid == "almalinux" {
		binary = "dnf"
	}
	if _, err := exec.LookPath(binary); err == nil {
		r.add("packages", Pass, binary+" available")
	} else {
		r.add("packages", Warn, binary+" not found")
	}
	if _, err := os.Stat("/sys/fs/cgroup/cgroup.controllers"); err == nil {
		r.add("cgroups_v2", Pass, "cgroups v2 detected")
	} else {
		r.add("cgroups_v2", Warn, "cgroups v2 unavailable or not mounted")
	}
	if osid == "almalinux" {
		enforce, err := os.ReadFile("/sys/fs/selinux/enforce")
		if err != nil {
			r.add("selinux", Warn, "SELinux status unavailable; enforcing required for certification")
		} else if strings.TrimSpace(string(enforce)) == "1" {
			r.add("selinux", Pass, "SELinux enforcing")
		} else {
			r.add("selinux", Warn, "SELinux is not enforcing")
		}
	} else if osid == "ubuntu" {
		enabled, err := os.ReadFile("/sys/module/apparmor/parameters/enabled")
		if err == nil && strings.HasPrefix(strings.TrimSpace(string(enabled)), "Y") {
			r.add("apparmor", Pass, "AppArmor enabled")
		} else {
			r.add("apparmor", Warn, "AppArmor is not detected as enabled")
		}
	}
	return r
}

func (r Report) JSON() ([]byte, error) { return json.MarshalIndent(r, "", "  ") }
