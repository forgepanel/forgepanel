//go:build linux

package main

import (
	"os"
	"path/filepath"
	"testing"
)

func TestReadOnlyCommands(t *testing.T) {
	if run([]string{"version"}) != 0 {
		t.Fatal("version")
	}
	dir := t.TempDir()
	p := filepath.Join(dir, "os-release")
	os.WriteFile(p, []byte("ID=debian\nVERSION_ID=13\n"), 0600)
	if run([]string{"install", "plan", "--os-release", p, "--json"}) != 0 {
		t.Fatal("plan")
	}
	if run([]string{"install", "apply"}) != exitUsage {
		t.Fatal("apply was not blocked")
	}
	if run([]string{"setup", "token"}) != exitUsage {
		t.Fatal("invalid setup")
	}
	if run([]string{"arbitrary"}) != exitUsage {
		t.Fatal("unknown command")
	}
}
