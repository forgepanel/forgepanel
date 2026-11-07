//go:build linux

package bootstrap

import (
	"errors"
	"os"
	"path/filepath"
	"sync"
	"testing"
	"time"
)

func TestTokenLifecycle(t *testing.T) {
	s := NewStore(filepath.Join(t.TempDir(), "state"))
	clock := time.Date(2026, 11, 5, 12, 0, 0, 0, time.UTC)
	s.Now = func() time.Time { return clock }
	status, err := s.Status()
	if err != nil || status.State != StateNotIssued {
		t.Fatalf("initial status: %v %v", status, err)
	}
	token, err := s.Regenerate()
	if err != nil || len(token) != 43 {
		t.Fatalf("generation failed: %v", err)
	}
	if _, err := os.Stat(filepath.Join(s.Dir, stateName)); err != nil {
		t.Fatal(err)
	}
	info, err := os.Stat(filepath.Join(s.Dir, stateName))
	if err != nil || info.Mode().Perm() != 0600 {
		t.Fatalf("state mode: %v %v", info, err)
	}
	info, err = os.Stat(s.Dir)
	if err != nil || info.Mode().Perm() != 0700 {
		t.Fatalf("dir mode: %v %v", info, err)
	}
	raw, err := os.ReadFile(filepath.Join(s.Dir, stateName))
	if err != nil {
		t.Fatal(err)
	}
	// The raw token must never be present in the persistence record.
	if contains(string(raw), token) {
		t.Fatal("plaintext secret persisted")
	}
	ok, err := s.Consume("not-the-token")
	if err != nil || ok {
		t.Fatalf("bad token accepted: %v %v", ok, err)
	}
	ok, err = s.Consume(token)
	if err != nil || !ok {
		t.Fatalf("valid token rejected: %v %v", ok, err)
	}
	ok, err = s.Consume(token)
	if err != nil || ok {
		t.Fatalf("replay accepted: %v %v", ok, err)
	}
	if err := s.MarkActivated(); err != nil {
		t.Fatal(err)
	}
	status, err = s.Status()
	if err != nil || status.State != StateActivated {
		t.Fatalf("activated status: %v %v", status, err)
	}
	_, err = s.Regenerate()
	if !errors.Is(err, ErrActivated) {
		t.Fatalf("regenerated activated token: %v", err)
	}
}

func TestExpiryAndLockout(t *testing.T) {
	s := NewStore(filepath.Join(t.TempDir(), "state"))
	now := time.Now()
	s.Now = func() time.Time { return now }
	token, err := s.Regenerate()
	if err != nil {
		t.Fatal(err)
	}
	for i := 0; i < 5; i++ {
		ok, err := s.Consume("wrong")
		if err != nil || ok {
			t.Fatalf("bad attempt #%d: %v", i, err)
		}
	}
	st, err := s.Status()
	if err != nil || st.State != StateLocked {
		t.Fatalf("expected locked: %+v %v", st, err)
	}
	ok, err := s.Consume(token)
	if err != nil || ok {
		t.Fatalf("locked token accepted: %v %v", ok, err)
	}
	token, err = s.Regenerate()
	if err != nil {
		t.Fatal(err)
	}
	now = now.Add(16 * time.Minute)
	st, err = s.Status()
	if err != nil || st.State != StateExpired {
		t.Fatalf("expected expired: %+v %v", st, err)
	}
	ok, err = s.Consume(token)
	if err != nil || ok {
		t.Fatalf("expired token accepted: %v %v", ok, err)
	}
}

func TestConcurrentSingleUse(t *testing.T) {
	s := NewStore(filepath.Join(t.TempDir(), "state"))
	token, err := s.Regenerate()
	if err != nil {
		t.Fatal(err)
	}
	var wg sync.WaitGroup
	successes := make(chan bool, 24)
	for i := 0; i < 24; i++ {
		wg.Add(1)
		go func() {
			defer wg.Done()
			ok, err := s.Consume(token)
			if err != nil {
				t.Errorf("consume: %v", err)
			}
			successes <- ok
		}()
	}
	wg.Wait()
	close(successes)
	count := 0
	for ok := range successes {
		if ok {
			count++
		}
	}
	if count != 1 {
		t.Fatalf("got %d successes, want one", count)
	}
}

func TestRejectSymlinkState(t *testing.T) {
	dir := filepath.Join(t.TempDir(), "state")
	if err := os.Mkdir(dir, 0700); err != nil {
		t.Fatal(err)
	}
	external := filepath.Join(t.TempDir(), "external")
	if err := os.WriteFile(external, []byte("private"), 0600); err != nil {
		t.Fatal(err)
	}
	if err := os.Symlink(external, filepath.Join(dir, stateName)); err != nil {
		t.Fatal(err)
	}
	s := NewStore(dir)
	if _, err := s.Status(); err == nil {
		t.Fatal("symlinked state was accepted")
	}
}

func contains(s, sub string) bool {
	for i := 0; i+len(sub) <= len(s); i++ {
		if s[i:i+len(sub)] == sub {
			return true
		}
	}
	return false
}

func TestRejectLockSymlink(t *testing.T) {
	dir := filepath.Join(t.TempDir(), "state")
	os.Mkdir(dir, 0700)
	external := filepath.Join(t.TempDir(), "external")
	os.WriteFile(external, []byte("private"), 0600)
	os.Symlink(external, filepath.Join(dir, lockName))
	if _, err := NewStore(dir).Regenerate(); err == nil {
		t.Fatal("symlink lock accepted")
	}
}
func TestNoRegenerationAfterConsumption(t *testing.T) {
	s := NewStore(filepath.Join(t.TempDir(), "state"))
	token, _ := s.Regenerate()
	s.Consume(token)
	if _, err := s.Regenerate(); !errors.Is(err, ErrPending) {
		t.Fatal("pending registration reopened")
	}
}
