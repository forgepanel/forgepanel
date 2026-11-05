// Command forgepanel-kvm-image-admit only validates pinned artifacts and policy.
// It cannot launch a VM or grant system authorization.
package main

import (
	"encoding/json"
	"errors"
	"fmt"
	"io"
	"os"
	"path/filepath"
	"syscall"

	"github.com/yyogas/forgepanel/tools/kvm-host-probe/admission"
)

func openPrivateJSON(path string) (io.ReadCloser, error) {
	if !filepath.IsAbs(path) || filepath.Clean(path) != path {
		return nil, errors.New("invalid_config_path")
	}
	canonical, err := filepath.EvalSymlinks(path)
	if err != nil || canonical != path {
		return nil, errors.New("noncanonical_config_path")
	}
	fd, err := syscall.Open(path, syscall.O_RDONLY|syscall.O_NOFOLLOW|syscall.O_NONBLOCK|syscall.O_CLOEXEC, 0)
	if err != nil {
		return nil, errors.New("config_unavailable")
	}
	f := os.NewFile(uintptr(fd), "private-configuration")
	info, err := f.Stat()
	if err != nil || !info.Mode().IsRegular() || info.Size() > admission.MaxJSONBytes || info.Mode().Perm()&0o077 != 0 {
		f.Close()
		return nil, errors.New("config_not_private_regular_or_bounded")
	}
	stat, ok := info.Sys().(*syscall.Stat_t)
	if !ok || int(stat.Uid) != os.Geteuid() || stat.Nlink != 1 {
		f.Close()
		return nil, errors.New("config_not_owned_or_hardlinked")
	}
	return f, nil
}
func run(args []string) (int, admission.Result) {
	fail := admission.Result{SchemaVersion: "1", Tool: "forgepanel-kvm-image-admission", Status: "BLOCKED",
		Qualification: "NOT_EXECUTED", Blockers: []string{"usage_requires_private_policy_and_manifest"}}
	if len(args) != 2 || args[0] == args[1] {
		return 2, fail
	}
	if os.Geteuid() == 0 {
		fail.Blockers[0] = "root_execution_forbidden"
		return 2, fail
	}
	pf, err := openPrivateJSON(args[0])
	if err != nil {
		fail.Blockers[0] = "policy_file_not_private_or_accessible"
		return 2, fail
	}
	defer pf.Close()
	policy, err := admission.DecodeJSON[admission.Policy](pf)
	if err != nil {
		fail.Blockers[0] = "invalid_explicit_policy"
		return 2, fail
	}
	rf, err := openPrivateJSON(args[1])
	if err != nil {
		fail.Blockers[0] = "manifest_file_not_private_or_accessible"
		return 2, fail
	}
	defer rf.Close()
	request, err := admission.DecodeJSON[admission.Request](rf)
	if err != nil {
		fail.Blockers[0] = "invalid_run_manifest"
		return 2, fail
	}
	report := admission.Admit(policy, request)
	if report.Status != "REVIEW_REQUIRED" {
		return 2, report
	}
	return 0, report
}
func main() {
	code, report := run(os.Args[1:])
	encoder := json.NewEncoder(os.Stdout)
	encoder.SetIndent("", "  ")
	if err := encoder.Encode(report); err != nil {
		fmt.Fprintln(os.Stderr, "unable to write read-only admission report")
		os.Exit(1)
	}
	os.Exit(code)
}
