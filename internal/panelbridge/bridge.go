//go:build linux

// Package panelbridge invokes a fixed, installed Symfony console as an
// unprivileged account. It never executes PHP application code as root.
package panelbridge

import (
	"context"
	"errors"
	"fmt"
	"io"
	"os"
	"os/exec"
	"os/user"
	"path/filepath"
	"strconv"
	"syscall"
	"time"
)

const ConsolePath = "/usr/share/forgepanel/panel/bin/console"

// CheckTrustedPath rejects writable or non-root-owned code and parent directories.
// A trusted administrator changing these paths concurrently is outside this boundary.
func CheckTrustedPath(path string) error {
	if !filepath.IsAbs(path) || filepath.Clean(path) != path {
		return errors.New("absolute canonical path required")
	}
	current := path
	for {
		st, e := os.Lstat(current)
		if e != nil {
			return e
		}
		owner, ok := st.Sys().(*syscall.Stat_t)
		if !ok || owner.Uid != 0 || st.Mode().Perm()&0022 != 0 || st.Mode()&os.ModeSymlink != 0 {
			return errors.New("untrusted code path ownership or permissions")
		}
		if current == path && !st.Mode().IsRegular() {
			return errors.New("executable/script is not a regular file")
		}
		if current != path && !st.IsDir() {
			return errors.New("parent is not a directory")
		}
		if current == "/" {
			break
		}
		current = filepath.Dir(current)
	}
	return nil
}
func Allowed(action string) bool {
	return action == "status" || action == "token" || action == "resume"
}
func Run(action string, out, errOut io.Writer) error {
	if !Allowed(action) {
		return errors.New("unsupported console bridge action")
	}
	if os.Geteuid() != 0 {
		return errors.New("local sudo/root access is required")
	}
	if err := CheckTrustedPath(ConsolePath); err != nil {
		return fmt.Errorf("installed panel is unavailable or untrusted: %w", err)
	}
	php, e := filepath.EvalSymlinks("/usr/bin/php")
	if e != nil {
		return e
	}
	if e = CheckTrustedPath(php); e != nil {
		return e
	}
	account, e := user.Lookup("forgepanel")
	if e != nil {
		return errors.New("dedicated forgepanel OS account does not exist; installer is not deployed")
	}
	uid, e := strconv.ParseUint(account.Uid, 10, 32)
	if e != nil {
		return e
	}
	gid, e := strconv.ParseUint(account.Gid, 10, 32)
	if e != nil {
		return e
	}
	if uid == 0 {
		return errors.New("refusing to run panel PHP as root")
	}
	ctx, cancel := context.WithTimeout(context.Background(), 30*time.Second)
	defer cancel()
	cmd := exec.CommandContext(ctx, php, ConsolePath, "forgepanel:setup:"+action, "--env=prod", "--no-debug", "--no-interaction")
	cmd.Dir = "/usr/share/forgepanel/panel"
	cmd.Env = []string{"PATH=/usr/bin:/bin", "LANG=C.UTF-8", "APP_ENV=prod", "APP_DEBUG=0", "FORGEPANEL_LOCAL_BOOTSTRAP=1"}
	cmd.SysProcAttr = &syscall.SysProcAttr{Credential: &syscall.Credential{Uid: uint32(uid), Gid: uint32(gid), Groups: []uint32{}}, Pdeathsig: syscall.SIGKILL}
	cmd.Stdout = out
	cmd.Stderr = errOut
	if e = cmd.Run(); e != nil {
		return fmt.Errorf("panel console failed (database and PHP must be healthy): %w", e)
	}
	return nil
}
