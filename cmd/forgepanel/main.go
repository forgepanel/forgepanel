//go:build linux

// ForgePanel development CLI: diagnostics, install planning and a fixed
// privilege-dropping bridge to the installed Symfony setup commands.
package main

import (
	"crypto/ed25519"
	"encoding/base64"
	"encoding/json"
	"flag"
	"fmt"
	"io"
	"os"
	"path/filepath"
	"runtime"
	"strings"
	"time"

	"forgepanel.dev/core/internal/doctor"
	"forgepanel.dev/core/internal/installer"
	"forgepanel.dev/core/internal/panelbridge"
	"forgepanel.dev/core/internal/releases"
)

const (
	version        = "0.7.0-dev"
	exitUsage      = 64
	exitInternal   = 70
	exitPermission = 77
	exitPreflight  = 2
)

func main() { os.Exit(run(os.Args[1:])) }

func run(args []string) int {
	if len(args) == 0 {
		usage()
		return exitUsage
	}
	switch args[0] {
	case "help", "--help", "-h":
		usage()
		return 0
	case "version", "--version":
		fmt.Println("ForgePanel CLI", version)
		return 0
	case "doctor":
		return runDoctor(args[1:])
	case "install":
		return runInstall(args[1:])
	case "release":
		return runRelease(args[1:])
	case "setup":
		return runSetup(args[1:])
	case "status":
		fmt.Fprintln(os.Stderr, "Full platform status is not implemented in this prototype. Use 'forgepanel doctor' or 'forgepanel setup status'.")
		return exitInternal
	case "repair", "services", "webstack", "admin", "update", "backup":
		fmt.Fprintln(os.Stderr, "Not implemented in the v0.7 CLI prototype; no system changes were made.")
		return exitInternal
	default:
		fmt.Fprintln(os.Stderr, "Unknown command:", args[0])
		usage()
		return exitUsage
	}
}

func runDoctor(args []string) int {
	f := flag.NewFlagSet("doctor", flag.ContinueOnError)
	f.SetOutput(os.Stderr)
	useJSON := f.Bool("json", false, "Output JSON for automation")
	if err := f.Parse(args); err != nil || f.NArg() != 0 {
		return exitUsage
	}
	report := doctor.Run()
	if *useJSON {
		data, err := report.JSON()
		if err != nil {
			fmt.Fprintln(os.Stderr, err)
			return exitInternal
		}
		fmt.Println(string(data))
	} else {
		fmt.Println("ForgePanel Doctor — READ-ONLY preflight")
		for _, check := range report.Checks {
			fmt.Printf("[%-4s] %-16s %s\n", check.Result, check.ID, check.Message)
		}
		fmt.Printf("Summary: %d passed, %d warnings, %d failures\n", report.Summary.Passed, report.Summary.Warnings, report.Summary.Failures)
	}
	if report.Summary.Failures > 0 {
		return exitPreflight
	}
	return 0
}

func runSetup(args []string) int {
	if len(args) == 0 {
		return exitUsage
	}
	action := args[0]
	if (action == "status" && len(args) != 1) || ((action == "token" || action == "resume") && (len(args) != 2 || args[1] != "--regenerate")) || !panelbridge.Allowed(action) {
		fmt.Fprintln(os.Stderr, "Usage: sudo forgepanel setup status | setup token --regenerate | setup resume --regenerate")
		return exitUsage
	}
	var out io.Writer = os.Stdout
	if action != "status" {
		tty, e := os.OpenFile("/dev/tty", os.O_WRONLY, 0)
		if e != nil {
			fmt.Fprintln(os.Stderr, "An interactive controlling terminal is required; no secret issued.")
			return exitPermission
		}
		defer tty.Close()
		out = tty
	}
	if e := panelbridge.Run(action, out, os.Stderr); e != nil {
		fmt.Fprintln(os.Stderr, e)
		return exitInternal
	}
	return 0
}

func runInstall(args []string) int {
	if len(args) == 0 || args[0] != "plan" {
		fmt.Fprintln(os.Stderr, "Only 'install plan' is implemented. Production apply is blocked; no system changes were made.")
		return exitUsage
	}
	f := flag.NewFlagSet("install plan", flag.ContinueOnError)
	config := f.String("config", "", "JSON configuration file")
	osRelease := f.String("os-release", "/etc/os-release", "OS release file; fixtures simulate a target only")
	useJSON := f.Bool("json", false, "JSON output")
	arch := f.String("arch", runtime.GOARCH, "Target architecture (planning only)")
	if f.Parse(args[1:]) != nil || f.NArg() != 0 {
		return exitUsage
	}
	c := installer.DefaultConfig()
	if *config != "" {
		file, e := os.Open(*config)
		if e != nil {
			fmt.Fprintln(os.Stderr, e)
			return exitInternal
		}
		defer file.Close()
		c, e = installer.DecodeConfig(file)
		if e != nil {
			fmt.Fprintln(os.Stderr, e)
			return exitUsage
		}
	}
	contents, e := os.ReadFile(*osRelease)
	if e != nil {
		fmt.Fprintln(os.Stderr, e)
		return exitInternal
	}
	facts := doctor.ParseOSRelease(string(contents))
	p, e := installer.Build(installer.Facts{ID: facts["ID"], Version: facts["VERSION_ID"], Architecture: *arch}, c)
	if e != nil {
		fmt.Fprintln(os.Stderr, e)
		return exitPreflight
	}
	if *useJSON {
		b, _ := json.MarshalIndent(p, "", "  ")
		fmt.Println(string(b))
	} else {
		fmt.Printf("ForgePanel installer — PLAN ONLY\nTarget: %s %s / %s\nRequested webstack: %s\n", p.Facts.ID, p.Facts.Version, p.Facts.Architecture, p.Config.WebStack)
		for _, s := range p.Steps {
			fmt.Printf("%-22s %s\n", s.ID, s.Description)
		}
		fmt.Println("Executable: false. No packages, ports, users or firewall rules were modified.")
		for _, b := range p.Blockers {
			fmt.Println("BLOCKER:", b)
		}
	}
	return 0
}
func runRelease(args []string) int {
	if len(args) == 0 || args[0] != "verify" {
		return exitUsage
	}
	f := flag.NewFlagSet("release verify", flag.ContinueOnError)
	manifest := f.String("manifest", "", "Signed JSON manifest")
	signature := f.String("signature", "", "Detached base64 Ed25519 signature")
	key := f.String("public-key", "", "Independently provisioned base64 Ed25519 public key")
	minimum := f.Uint64("min-sequence", 1, "Trusted minimum sequence; no persistence is implemented")
	if f.Parse(args[1:]) != nil || f.NArg() != 0 || *manifest == "" || *signature == "" || *key == "" {
		return exitUsage
	}
	read := func(p string, limit int64) ([]byte, error) {
		h, e := os.Open(filepath.Clean(p))
		if e != nil {
			return nil, e
		}
		defer h.Close()
		b, e := io.ReadAll(io.LimitReader(h, limit+1))
		if e == nil && int64(len(b)) > limit {
			return nil, fmt.Errorf("oversized file")
		}
		return b, e
	}
	raw, e := read(*manifest, 1<<20)
	if e != nil {
		fmt.Fprintln(os.Stderr, e)
		return exitInternal
	}
	sig, e := read(*signature, 1024)
	if e != nil {
		return exitInternal
	}
	pk, e := read(*key, 1024)
	if e != nil {
		return exitInternal
	}
	sb, e := base64.StdEncoding.DecodeString(strings.TrimSpace(string(sig)))
	if e != nil {
		return exitUsage
	}
	kb, e := base64.StdEncoding.DecodeString(strings.TrimSpace(string(pk)))
	if e != nil {
		return exitUsage
	}
	m, e := releases.Verify(raw, sb, ed25519.PublicKey(kb), time.Now(), *minimum)
	if e != nil {
		fmt.Fprintln(os.Stderr, e)
		return exitPreflight
	}
	fmt.Printf("Manifest signature verified: %s (sequence %d). Artifact bytes were NOT verified by this command. Trust depends on the supplied key.\n", m.Version, m.Sequence)
	return 0
}

func usage() {
	fmt.Print(`ForgePanel CLI 0.7.0-dev — development source, not a production installer

Read-only commands:
  forgepanel version
  forgepanel doctor [--json]
  forgepanel install plan [--config examples/install.json] [--json]
  forgepanel release verify --manifest FILE --signature FILE --public-key FILE

Installed panel bridge (requires PHP, PostgreSQL, migrations and local sudo):
  sudo forgepanel setup status
  sudo forgepanel setup token --regenerate
  sudo forgepanel setup resume --regenerate

Not implemented: install apply, repair, services, webstack, admin, update, backup.
No automatic package installation or firewall modification in this release.
`)
}
