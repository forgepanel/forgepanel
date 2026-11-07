//go:build linux

package installer

import (
	"encoding/json"
	"reflect"
	"strings"
	"testing"
)

func TestTargetMatrix(t *testing.T) {
	for _, f := range []Facts{{"debian", "12", "amd64"}, {"debian", "13", "amd64"}, {"ubuntu", "24.04", "amd64"}, {"ubuntu", "26.04", "amd64"}, {"almalinux", "9.6", "amd64"}, {"almalinux", "10.0", "amd64"}} {
		for _, profile := range Profiles {
			t.Run(f.ID+f.Version+"/"+profile, func(t *testing.T) {
				c := DefaultConfig()
				c.WebStack = profile
				p, e := Build(f, c)
				if e != nil || p.Executable || len(p.Blockers) == 0 || len(p.Steps) != 10 {
					t.Fatalf("unsafe/invalid plan: %+v %v", p, e)
				}
				p2, _ := Build(f, c)
				if !reflect.DeepEqual(p, p2) {
					t.Fatal("plan is not deterministic")
				}
			})
		}
	}
}
func TestRejectUnsupported(t *testing.T) {
	for _, f := range []Facts{{"debian", "11", "amd64"}, {"ubuntu", "22.04", "amd64"}, {"almalinux", "9.bad", "amd64"}, {"almalinux", "90", "amd64"}, {"rocky", "9", "amd64"}, {"debian", "13", "arm64"}} {
		if _, e := Build(f, DefaultConfig()); e == nil {
			t.Fatalf("accepted %+v", f)
		}
	}
}
func TestRejectInvalidConfig(t *testing.T) {
	for _, mutate := range []func(*Config){func(c *Config) { c.AdminPort = 443 }, func(c *Config) { c.UserPort = 8447 }, func(c *Config) { c.AdminHost = "https://panel.example.com" }, func(c *Config) { c.AdminHost = "panel.example.com"; c.UserHost = c.AdminHost }, func(c *Config) { c.WebStack = "nginx;id" }, func(c *Config) { c.Modules = []string{"shell"} }, func(c *Config) { c.Modules = []string{"dns", "dns"} }, func(c *Config) { c.UserHost = "client.example.com" }} {
		c := DefaultConfig()
		mutate(&c)
		if c.Validate() == nil {
			t.Fatalf("accepted %+v", c)
		}
	}
}
func TestStrictJSON(t *testing.T) {
	b, _ := json.Marshal(DefaultConfig())
	if _, e := DecodeConfig(strings.NewReader(string(b))); e != nil {
		t.Fatal(e)
	}
	for _, s := range []string{string(b) + " {}", `{"schema_version":1,"command":"rm"}`, string(b[:len(b)-1]) + `,"unrecognized":true}`} {
		if _, e := DecodeConfig(strings.NewReader(s)); e == nil {
			t.Fatal("accepted ambiguous JSON")
		}
	}
}
func TestSeparateHosts(t *testing.T) {
	c := DefaultConfig()
	c.AdminHost = "forge.example.com"
	c.UserHost = "panel.example.com"
	if e := c.Validate(); e != nil {
		t.Fatal(e)
	}
}

func TestRejectOversizedAndDuplicateJSON(t *testing.T) {
	b, _ := json.Marshal(DefaultConfig())
	for _, s := range []string{string(b) + strings.Repeat(" ", 65536), string(b[:len(b)-1]) + `,"admin_port":8447}`, `{"schema_version":1}`} {
		if _, e := DecodeConfig(strings.NewReader(s)); e == nil {
			t.Fatal("invalid JSON input accepted")
		}
	}
}

func TestRejectNullHostname(t *testing.T) {
	b, _ := json.Marshal(DefaultConfig())
	raw := strings.Replace(string(b), `"admin_host":""`, `"admin_host":null`, 1)
	if _, e := DecodeConfig(strings.NewReader(raw)); e == nil {
		t.Fatal("null hostname accepted")
	}
}
