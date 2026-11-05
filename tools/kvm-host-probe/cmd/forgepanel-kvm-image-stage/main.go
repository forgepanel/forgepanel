// Command forgepanel-kvm-image-stage prepares one non-executable private image
// copy from pinned source bytes. It does not invoke QEMU or elevate privileges.
package main

import (
	"encoding/json"
	"fmt"
	"io"
	"os"
	"path/filepath"
	"syscall"

	"github.com/yyogas/forgepanel/tools/kvm-host-probe/admission"
	"github.com/yyogas/forgepanel/tools/kvm-host-probe/staging"
)

func openPrivateInput(path string) (io.ReadCloser, bool) {
	if !filepath.IsAbs(path) || filepath.Clean(path) != path {
		return nil, false
	}
	canonical, err := filepath.EvalSymlinks(path)
	if err != nil || canonical != path {
		return nil, false
	}
	fd, err := syscall.Open(path, syscall.O_RDONLY|syscall.O_NOFOLLOW|syscall.O_NONBLOCK|syscall.O_CLOEXEC, 0)
	if err != nil {
		return nil, false
	}
	file := os.NewFile(uintptr(fd), "private-json-input")
	var meta syscall.Stat_t
	if syscall.Fstat(fd, &meta) != nil || uint32(meta.Mode)&syscall.S_IFMT != syscall.S_IFREG || meta.Nlink != 1 || int(meta.Uid) != os.Geteuid() || meta.Mode&0o177 != 0 || meta.Mode&06000 != 0 || meta.Size > admission.MaxJSONBytes || meta.Size <= 0 {
		file.Close()
		return nil, false
	}
	return file, true
}
func denied(code string) staging.Result {
	return staging.Result{SchemaVersion: staging.SchemaVersion, Tool: "forgepanel-kvm-image-stage", Status: "BLOCKED", Qualification: "NOT_EXECUTED", ManualReviewRequired: true, Blockers: []string{code}}
}
func run(args []string) (int, staging.Result) {
	if len(args) != 3 {
		return 2, denied("usage_requires_policy_request_and_private_staging_root")
	}
	if os.Geteuid() == 0 {
		return 2, denied("root_execution_forbidden")
	}
	policyFile, ok := openPrivateInput(args[0])
	if !ok {
		return 2, denied("policy_not_private_or_accessible")
	}
	defer policyFile.Close()
	policy, err := admission.DecodeJSON[admission.Policy](policyFile)
	if err != nil {
		return 2, denied("invalid_policy_json")
	}
	requestFile, ok := openPrivateInput(args[1])
	if !ok {
		return 2, denied("request_not_private_or_accessible")
	}
	defer requestFile.Close()
	request, err := admission.DecodeJSON[admission.Request](requestFile)
	if err != nil {
		return 2, denied("invalid_request_json")
	}
	report := staging.Stage(policy, request, args[2])
	if report.Status != "STAGED_FOR_MANUAL_REVIEW" {
		return 2, report
	}
	return 0, report
}
func main() {
	exitCode, report := run(os.Args[1:])
	enc := json.NewEncoder(os.Stdout)
	enc.SetIndent("", "  ")
	if err := enc.Encode(report); err != nil {
		fmt.Fprintln(os.Stderr, "cannot encode staging report")
		os.Exit(1)
	}
	os.Exit(exitCode)
}
