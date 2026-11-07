package releases

import (
	"crypto/ed25519"
	"crypto/sha256"
	"encoding/hex"
	"encoding/json"
	"errors"
	"io"
	"regexp"
	"strings"
	"time"
)

// Verification does not establish trust in a key downloaded alongside a release.
// The caller must provision the public key independently and persist anti-rollback state.
type Manifest struct {
	Schema    int        `json:"schema"`
	Version   string     `json:"version"`
	Sequence  uint64     `json:"sequence"`
	ExpiresAt time.Time  `json:"expires_at"`
	Artifacts []Artifact `json:"artifacts"`
}
type Artifact struct {
	Name   string `json:"name"`
	SHA256 string `json:"sha256"`
	Size   int64  `json:"size"`
}

var filename = regexp.MustCompile(`^[a-zA-Z0-9][a-zA-Z0-9._-]{0,127}$`)

func Verify(raw, signature []byte, key ed25519.PublicKey, now time.Time, minSequence uint64) (Manifest, error) {
	var m Manifest
	if len(raw) > 1<<20 || len(key) != ed25519.PublicKeySize || len(signature) != ed25519.SignatureSize || !ed25519.Verify(key, raw, signature) {
		return m, errors.New("invalid release signature")
	}
	d := json.NewDecoder(strings.NewReader(string(raw)))
	d.DisallowUnknownFields()
	if e := d.Decode(&m); e != nil {
		return m, e
	}
	var x any
	if d.Decode(&x) != io.EOF {
		return m, errors.New("trailing manifest content")
	}
	if m.Schema != 1 || m.Sequence < minSequence || m.Sequence == 0 || m.Version == "" || !now.Before(m.ExpiresAt) || len(m.Artifacts) == 0 {
		return m, errors.New("expired, rolled back or unsupported manifest")
	}
	seen := map[string]bool{}
	for _, a := range m.Artifacts {
		sum, e := hex.DecodeString(a.SHA256)
		if !filename.MatchString(a.Name) || a.Size < 1 || a.Size > 2<<30 || e != nil || len(sum) != 32 || seen[a.Name] {
			return m, errors.New("invalid artifact metadata")
		}
		seen[a.Name] = true
	}
	return m, nil
}
func CheckArtifact(r io.Reader, a Artifact) error {
	if a.Size < 1 || a.Size > 2<<30 {
		return errors.New("invalid size")
	}
	h := sha256.New()
	n, e := io.Copy(h, io.LimitReader(r, a.Size+1))
	if e != nil {
		return e
	}
	if n != a.Size || hex.EncodeToString(h.Sum(nil)) != strings.ToLower(a.SHA256) {
		return errors.New("artifact size/digest mismatch")
	}
	return nil
}
