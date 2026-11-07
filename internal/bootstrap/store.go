//go:build linux

// Package bootstrap implements the LOCAL, first-run authorization secret store.
// It does not create an administrator or serve an HTTP endpoint.
// Production integration must atomically establish the first administrator
// in the Symfony database and mark this bootstrap as completed.
package bootstrap

import (
	"crypto/rand"
	"crypto/sha256"
	"crypto/subtle"
	"encoding/base64"
	"encoding/hex"
	"encoding/json"
	"errors"
	"fmt"
	"io"
	"os"
	"path/filepath"
	"syscall"
	"time"
)

const (
	lifetime    = 15 * time.Minute
	maxAttempts = 5
	stateName   = "bootstrap.json"
	lockName    = ".bootstrap.lock"
)

var (
	ErrPending     = errors.New("consumed bootstrap requires explicit recovery, not token regeneration")
	ErrNotIssued   = errors.New("bootstrap token has not been issued")
	ErrActivated   = errors.New("initial setup has already been completed")
	ErrNotConsumed = errors.New("bootstrap token must be consumed before setup completion")
	ErrUnsafeDir   = errors.New("bootstrap state directory is not private and owned by this process")
	ErrUnsafeFile  = errors.New("bootstrap state file has unsafe permissions or type")
)

type State string

const (
	StateNotIssued State = "NOT_ISSUED"
	StateIssued    State = "TOKEN_ISSUED"
	StateExpired   State = "TOKEN_EXPIRED"
	StateLocked    State = "TOKEN_LOCKED"
	StateConsumed  State = "TOKEN_CONSUMED"
	StateActivated State = "ACTIVATED"
)

type Status struct {
	State          State      `json:"state"`
	IssuedAt       *time.Time `json:"issued_at,omitempty"`
	ExpiresAt      *time.Time `json:"expires_at,omitempty"`
	ConsumedAt     *time.Time `json:"consumed_at,omitempty"`
	ActivatedAt    *time.Time `json:"activated_at,omitempty"`
	FailedAttempts int        `json:"failed_attempts"`
}

type record struct {
	Version        int        `json:"version"`
	TokenHash      string     `json:"token_sha256"`
	IssuedAt       time.Time  `json:"issued_at"`
	ExpiresAt      time.Time  `json:"expires_at"`
	ConsumedAt     *time.Time `json:"consumed_at,omitempty"`
	ActivatedAt    *time.Time `json:"activated_at,omitempty"`
	FailedAttempts int        `json:"failed_attempts"`
}

type Store struct {
	Dir string
	Now func() time.Time
}

func NewStore(dir string) *Store {
	return &Store{Dir: dir, Now: time.Now}
}

func (s *Store) Regenerate() (string, error) {
	var token string
	err := s.locked(true, func() error {
		old, err := s.read()
		if err != nil {
			return err
		}
		if old != nil && old.ActivatedAt != nil {
			return ErrActivated
		}
		if old != nil && old.ConsumedAt != nil {
			return ErrPending
		}
		buf := make([]byte, 32)
		if _, err := io.ReadFull(rand.Reader, buf); err != nil {
			return fmt.Errorf("generate secure token: %w", err)
		}
		token = base64.RawURLEncoding.EncodeToString(buf)
		digest := sha256.Sum256([]byte(token))
		now := s.Now().UTC()
		return s.write(&record{
			Version:   1,
			TokenHash: hex.EncodeToString(digest[:]),
			IssuedAt:  now,
			ExpiresAt: now.Add(lifetime),
		})
	})
	return token, err
}

func (s *Store) Status() (Status, error) {
	result := Status{State: StateNotIssued}
	err := s.locked(false, func() error {
		r, err := s.read()
		if err != nil || r == nil {
			return err
		}
		result.IssuedAt = &r.IssuedAt
		result.ExpiresAt = &r.ExpiresAt
		result.ConsumedAt = r.ConsumedAt
		result.ActivatedAt = r.ActivatedAt
		result.FailedAttempts = r.FailedAttempts
		switch {
		case r.ActivatedAt != nil:
			result.State = StateActivated
		case r.ConsumedAt != nil:
			result.State = StateConsumed
		case !s.Now().Before(r.ExpiresAt):
			result.State = StateExpired
		case r.FailedAttempts >= maxAttempts:
			result.State = StateLocked
		default:
			result.State = StateIssued
		}
		return nil
	})
	return result, err
}

// Consume verifies a one-time token and burns it on success.
// Called only by a future authenticated setup endpoint owned by the Go agent.
// It must NOT be wired to a public generic "verify token" API.
func (s *Store) Consume(token string) (bool, error) {
	accepted := false
	err := s.locked(false, func() error {
		r, err := s.read()
		if err != nil {
			return err
		}
		if r == nil {
			return ErrNotIssued
		}
		if r.ActivatedAt != nil {
			return ErrActivated
		}
		if r.ConsumedAt != nil || !s.Now().Before(r.ExpiresAt) || r.FailedAttempts >= maxAttempts {
			return nil
		}
		digest := sha256.Sum256([]byte(token))
		expected, err := hex.DecodeString(r.TokenHash)
		if err != nil || len(expected) != sha256.Size {
			return errors.New("corrupt bootstrap token digest")
		}
		if subtle.ConstantTimeCompare(digest[:], expected) != 1 || len(token) != 43 {
			r.FailedAttempts++
			return s.write(r)
		}
		now := s.Now().UTC()
		r.ConsumedAt = &now
		if err := s.write(r); err != nil {
			return err
		}
		accepted = true
		return nil
	})
	return accepted, err
}

// MarkActivated is a privileged, local internal primitive ONLY. Integration
// must call it AFTER creation of the first admin has been committed by Symfony.
// This PoC has no HTTP registration workflow and does not call this method.
func (s *Store) MarkActivated() error {
	return s.locked(false, func() error {
		r, err := s.read()
		if err != nil {
			return err
		}
		if r == nil {
			return ErrNotIssued
		}
		if r.ActivatedAt != nil {
			return ErrActivated
		}
		if r.ConsumedAt == nil {
			return ErrNotConsumed
		}
		now := s.Now().UTC()
		r.ActivatedAt = &now
		return s.write(r)
	})
}

func (s *Store) locked(create bool, fn func() error) error {
	if s.Dir == "" || !filepath.IsAbs(s.Dir) {
		return ErrUnsafeDir
	}
	if create {
		if err := os.MkdirAll(s.Dir, 0700); err != nil {
			return err
		}
	} else {
		if _, err := os.Lstat(s.Dir); errors.Is(err, os.ErrNotExist) {
			return fn()
		} else if err != nil {
			return err
		}
	}
	if err := s.checkDir(); err != nil {
		return err
	}
	f, err := os.OpenFile(filepath.Join(s.Dir, lockName), os.O_CREATE|os.O_RDWR|syscall.O_NOFOLLOW|syscall.O_CLOEXEC, 0600)
	if err != nil {
		return err
	}
	defer f.Close()
	info, err := f.Stat()
	if err != nil {
		return err
	}
	if !info.Mode().IsRegular() || info.Mode().Perm()&0077 != 0 {
		return ErrUnsafeFile
	}
	owner, ok := info.Sys().(*syscall.Stat_t)
	if !ok || int(owner.Uid) != os.Geteuid() || owner.Nlink != 1 {
		return ErrUnsafeFile
	}
	if err := syscall.Flock(int(f.Fd()), syscall.LOCK_EX); err != nil {
		return err
	}
	defer syscall.Flock(int(f.Fd()), syscall.LOCK_UN)
	return fn()
}

func (s *Store) checkDir() error {
	info, err := os.Lstat(s.Dir)
	if err != nil {
		return err
	}
	if !info.IsDir() || info.Mode().Perm()&0077 != 0 {
		return ErrUnsafeDir
	}
	owner, ok := info.Sys().(*syscall.Stat_t)
	if !ok || int(owner.Uid) != os.Geteuid() {
		return ErrUnsafeDir
	}
	return nil
}

func (s *Store) read() (*record, error) {
	filename := filepath.Join(s.Dir, stateName)
	// Open with O_NOFOLLOW so an unexpected symlink is never followed.
	fd, err := syscall.Open(filename, syscall.O_RDONLY|syscall.O_NOFOLLOW|syscall.O_CLOEXEC, 0)
	if errors.Is(err, syscall.ENOENT) {
		return nil, nil
	}
	if err != nil {
		return nil, err
	}
	f := os.NewFile(uintptr(fd), filename)
	defer f.Close()
	info, err := f.Stat()
	if err != nil {
		return nil, err
	}
	if !info.Mode().IsRegular() || info.Mode().Perm()&0077 != 0 {
		return nil, ErrUnsafeFile
	}
	owner, ok := info.Sys().(*syscall.Stat_t)
	if !ok || int(owner.Uid) != os.Geteuid() {
		return nil, ErrUnsafeFile
	}
	var r record
	dec := json.NewDecoder(io.LimitReader(f, 8192))
	dec.DisallowUnknownFields()
	if err := dec.Decode(&r); err != nil {
		return nil, err
	}
	if r.Version != 1 {
		return nil, errors.New("unsupported bootstrap state schema")
	}
	return &r, nil
}

func (s *Store) write(r *record) error {
	f, err := os.CreateTemp(s.Dir, ".state-*")
	if err != nil {
		return err
	}
	name := f.Name()
	defer os.Remove(name)
	if err := f.Chmod(0600); err != nil {
		f.Close()
		return err
	}
	if err := json.NewEncoder(f).Encode(r); err != nil {
		f.Close()
		return err
	}
	if err := f.Sync(); err != nil {
		f.Close()
		return err
	}
	if err := f.Close(); err != nil {
		return err
	}
	if err := os.Rename(name, filepath.Join(s.Dir, stateName)); err != nil {
		return err
	}
	dir, err := os.Open(s.Dir)
	if err != nil {
		return err
	}
	defer dir.Close()
	return dir.Sync()
}
