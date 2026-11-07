//go:build linux

package panelbridge

import (
	"os"
	"path/filepath"
	"testing"
)

func TestActionsAreClosed(t *testing.T) {
	for _, s := range []string{"status", "token", "resume"} {
		if !Allowed(s) {
			t.Fatal(s)
		}
	}
	for _, s := range []string{"exec", "token;id", "../console", ""} {
		if Allowed(s) {
			t.Fatal("arbitrary action accepted")
		}
	}
}
func TestRejectUntrustedPath(t *testing.T) {
	d := t.TempDir()
	p := filepath.Join(d, "console")
	os.WriteFile(p, []byte("php"), 0666)
	os.Chmod(p, 0666)
	if CheckTrustedPath(p) == nil {
		t.Fatal("writable code accepted")
	}
	if CheckTrustedPath("relative") == nil {
		t.Fatal("relative accepted")
	}
	os.Remove(p)
	os.Symlink("/etc/passwd", p)
	if CheckTrustedPath(p) == nil {
		t.Fatal("symlink accepted")
	}
}
