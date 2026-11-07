package releases

import (
	"crypto/ed25519"
	"crypto/rand"
	"crypto/sha256"
	"encoding/hex"
	"encoding/json"
	"strings"
	"testing"
	"time"
)

func TestVerify(t *testing.T) {
	pub, priv, _ := ed25519.GenerateKey(rand.Reader)
	now := time.Now()
	h := sha256.Sum256([]byte("payload"))
	m := Manifest{1, "0.7.0-dev", 2, now.Add(time.Hour), []Artifact{{"panel.tar.gz", hex.EncodeToString(h[:]), 7}}}
	raw, _ := json.Marshal(m)
	sig := ed25519.Sign(priv, raw)
	if _, e := Verify(raw, sig, pub, now, 2); e != nil {
		t.Fatal(e)
	}
	if e := CheckArtifact(strings.NewReader("payload"), m.Artifacts[0]); e != nil {
		t.Fatal(e)
	}
	for _, bad := range []string{"payloae", "payload!", "payloa"} {
		if CheckArtifact(strings.NewReader(bad), m.Artifacts[0]) == nil {
			t.Fatal("tamper accepted")
		}
	}
	for _, tc := range []struct {
		name  string
		bytes []byte
		sig   []byte
		key   ed25519.PublicKey
		at    time.Time
		seq   uint64
	}{{"tamper", append(append([]byte{}, raw...), 32), sig, pub, now, 2}, {"expiry", raw, sig, pub, now.Add(time.Hour), 2}, {"rollback", raw, sig, pub, now, 3}, {"badkey", raw, sig, nil, now, 2}} {
		t.Run(tc.name, func(t *testing.T) {
			if _, e := Verify(tc.bytes, tc.sig, tc.key, tc.at, tc.seq); e == nil {
				t.Fatal("verification bypass")
			}
		})
	}
}
func TestRejectArtifactTraversal(t *testing.T) {
	pub, priv, _ := ed25519.GenerateKey(rand.Reader)
	for _, name := range []string{"../root", "/etc/passwd", "a/b", "-option"} {
		m := Manifest{1, "dev", 1, time.Now().Add(time.Hour), []Artifact{{name, strings.Repeat("a", 64), 1}}}
		r, _ := json.Marshal(m)
		if _, e := Verify(r, ed25519.Sign(priv, r), pub, time.Now(), 0); e == nil {
			t.Fatal("invalid name accepted")
		}
	}
}
