// Package probe performs a non-privileged, read-only KVM host inspection.
// The result is not a VM certification and must not be used to authorize
// privileged panel actions.
package probe

import (
	"fmt"
	"io"
	"io/fs"
	"os"
	"runtime"
	"strings"
	"unicode"
)

const (
	cpuInfoPath         = "/proc/cpuinfo"
	osReleasePath       = "/etc/os-release"
	kvmDevicePath       = "/dev/kvm"
	kvmModulePath       = "/sys/module/kvm"
	maxCPUBytes   int64 = 2 << 20
	maxOSBytes    int64 = 16 << 10
)

// Source restricts host access to reads and lstat; no shell or device open.
// This interface makes filesystem fault and hostile-value testing possible.
type Source interface {
	ReadLimited(path string, maxBytes int64) ([]byte, error)
	Lstat(path string) (fs.FileInfo, error)
}

type HostSource struct{}

func (HostSource) ReadLimited(path string, maxBytes int64) ([]byte, error) {
	f, err := os.Open(path)
	if err != nil {
		return nil, err
	}
	defer f.Close()
	b, err := io.ReadAll(io.LimitReader(f, maxBytes+1))
	if err != nil {
		return nil, err
	}
	if int64(len(b)) > maxBytes {
		return nil, fmt.Errorf("read limit exceeded")
	}
	return b, nil
}

func (HostSource) Lstat(path string) (fs.FileInfo, error) { return os.Lstat(path) }

type Report struct {
	SchemaVersion          string   `json:"schema_version"`
	ProbeName              string   `json:"probe_name"`
	RuntimeOS              string   `json:"runtime_os"`
	RuntimeArch            string   `json:"runtime_arch"`
	OSID                   string   `json:"os_id"`
	OSVersion              string   `json:"os_version"`
	KVMDevice              string   `json:"kvm_device"`
	CPUVirtualization      string   `json:"cpu_virtualization"`
	KVMKernelModule        string   `json:"kvm_kernel_module"`
	HostAssessment         string   `json:"host_assessment"`
	Qualification          string   `json:"qualification"`
	VMExecuted             bool     `json:"vm_executed"`
	VMImagePinned          bool     `json:"vm_image_pinned"`
	ResourceQuotasVerified bool     `json:"resource_quotas_verified"`
	SnapshotTested         bool     `json:"snapshot_tested"`
	FailureRecoveryTested  bool     `json:"failure_recovery_tested"`
	ReportSigned           bool     `json:"report_signed"`
	Warnings               []string `json:"warnings"`
}

func cleanOSValue(raw string) string {
	raw = strings.TrimSpace(raw)
	if len(raw) >= 2 && raw[0] == '"' && raw[len(raw)-1] == '"' {
		raw = raw[1 : len(raw)-1]
	}
	if len(raw) == 0 || len(raw) > 64 {
		return "unknown"
	}
	for _, ch := range raw {
		if !(unicode.IsLetter(ch) || unicode.IsDigit(ch) || ch == '.' || ch == '-' || ch == '_' || ch == '+') {
			return "unknown"
		}
	}
	return raw
}

func releaseFields(data []byte) (string, string) {
	osID, version := "unknown", "unknown"
	for _, line := range strings.Split(string(data), "\n") {
		if strings.HasPrefix(line, "ID=") {
			osID = cleanOSValue(strings.TrimPrefix(line, "ID="))
		}
		if strings.HasPrefix(line, "VERSION_ID=") {
			version = cleanOSValue(strings.TrimPrefix(line, "VERSION_ID="))
		}
	}
	return osID, version
}

func cpuVirtualization(data []byte, arch string) string {
	if arch != "amd64" && arch != "386" {
		return "UNKNOWN_FOR_ARCH"
	}
	foundFlags := false
	for _, line := range strings.Split(string(data), "\n") {
		key, values, found := strings.Cut(line, ":")
		if !found || strings.TrimSpace(key) != "flags" {
			continue
		}
		foundFlags = true
		for _, flag := range strings.Fields(values) {
			if flag == "vmx" || flag == "svm" {
				return "FLAG_PRESENT"
			}
		}
	}
	if foundFlags {
		return "FLAG_ABSENT"
	}
	return "UNAVAILABLE"
}

func readState(source Source, path string, maxBytes int64, warnings *[]string, code string) []byte {
	data, err := source.ReadLimited(path, maxBytes)
	if err != nil {
		*warnings = append(*warnings, code)
		return nil
	}
	return data
}

// Inspect captures only static read-only evidence and refuses to infer the
// results of VM snapshots, recovery, resource quotas, signature or runtime.
func Inspect(source Source, goos string, arch string) Report {
	r := Report{
		SchemaVersion: "1", ProbeName: "forgepanel-kvm-host-probe",
		RuntimeOS: goos, RuntimeArch: arch, OSID: "unknown", OSVersion: "unknown",
		KVMDevice: "NOT_CHECKED", CPUVirtualization: "NOT_CHECKED",
		KVMKernelModule: "NOT_CHECKED", HostAssessment: "INCONCLUSIVE",
		Qualification: "NOT_EXECUTED", Warnings: []string{},
	}
	if goos != "linux" {
		r.HostAssessment = "NOT_APPLICABLE"
		r.Warnings = append(r.Warnings, "linux_host_required")
		return r
	}
	osData := readState(source, osReleasePath, maxOSBytes, &r.Warnings, "os_release_unavailable")
	if osData != nil {
		r.OSID, r.OSVersion = releaseFields(osData)
	}
	info, err := source.Lstat(kvmDevicePath)
	if err != nil {
		if os.IsNotExist(err) {
			r.KVMDevice = "ABSENT"
		} else {
			r.KVMDevice = "UNKNOWN"
			r.Warnings = append(r.Warnings, "kvm_device_stat_failed")
		}
	} else if info.Mode()&os.ModeSymlink != 0 {
		r.KVMDevice = "UNTRUSTED_SYMLINK"
	} else if info.Mode()&os.ModeCharDevice != 0 && info.Mode()&os.ModeDevice != 0 {
		r.KVMDevice = "CHAR_DEVICE_PRESENT"
	} else {
		r.KVMDevice = "NOT_CHAR_DEVICE"
	}
	cpuData := readState(source, cpuInfoPath, maxCPUBytes, &r.Warnings, "cpuinfo_unavailable")
	if cpuData == nil {
		r.CPUVirtualization = "UNAVAILABLE"
	} else {
		r.CPUVirtualization = cpuVirtualization(cpuData, arch)
	}
	mod, err := source.Lstat(kvmModulePath)
	if err != nil {
		if os.IsNotExist(err) {
			r.KVMKernelModule = "ABSENT"
		} else {
			r.KVMKernelModule = "UNKNOWN"
			r.Warnings = append(r.Warnings, "kvm_module_stat_failed")
		}
	} else if mod.IsDir() {
		r.KVMKernelModule = "PRESENT"
	} else {
		r.KVMKernelModule = "UNEXPECTED_TYPE"
	}
	if r.KVMDevice == "CHAR_DEVICE_PRESENT" {
		if r.CPUVirtualization == "FLAG_PRESENT" {
			r.HostAssessment = "CANDIDATE_FOR_ISOLATED_VM_TESTS"
		} else {
			r.HostAssessment = "INCONCLUSIVE"
		}
		r.Warnings = append(r.Warnings, "device_permissions_not_verified", "no_vm_boot_or_snapshot_test_performed")
	} else if r.KVMDevice == "ABSENT" || r.KVMDevice == "NOT_CHAR_DEVICE" || r.KVMDevice == "UNTRUSTED_SYMLINK" {
		r.HostAssessment = "NO_TRUSTED_KVM_DEVICE"
	}
	return r
}

// InspectHost only makes bounded reads, lstat calls, and no changes to Linux.
func InspectHost() Report { return Inspect(HostSource{}, runtime.GOOS, runtime.GOARCH) }
