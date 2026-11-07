//go:build linux

// Package installer builds declarative plans. It never installs packages.
package installer

import (
	"bytes"
	"crypto/sha256"
	"encoding/hex"
	"encoding/json"
	"errors"
	"fmt"
	"io"
	"regexp"
	"strings"
)

var idPattern = regexp.MustCompile(`^[a-z][a-z0-9_-]*$`)
var versionPattern = regexp.MustCompile(`^[0-9]+(?:\.[0-9]+)*$`)
var labelPattern = regexp.MustCompile(`^[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?$`)

var Profiles = []string{"nginx_apache_fpm", "nginx_fpm", "apache_fpm", "caddy_fpm", "caddy_frankenphp"}

type Facts struct {
	ID           string `json:"id"`
	Version      string `json:"version"`
	Architecture string `json:"architecture"`
}
type Config struct {
	SchemaVersion int      `json:"schema_version"`
	AdminPort     int      `json:"admin_port"`
	UserPort      int      `json:"user_port"`
	AdminHost     string   `json:"admin_host"`
	UserHost      string   `json:"user_host"`
	WebStack      string   `json:"webstack"`
	Modules       []string `json:"modules"`
}
type Step struct {
	ID          string `json:"id"`
	Kind        string `json:"kind"`
	Description string `json:"description"`
}
type Plan struct {
	SchemaVersion  int      `json:"schema_version"`
	Facts          Facts    `json:"target"`
	Config         Config   `json:"requested"`
	InputDigest    string   `json:"input_sha256"`
	PackageManager string   `json:"package_manager"`
	Components     []string `json:"component_requirements"`
	Steps          []Step   `json:"steps"`
	Executable     bool     `json:"executable"`
	Blockers       []string `json:"blockers"`
	Notes          []string `json:"notes"`
}

func DefaultConfig() Config { return Config{1, 8447, 8446, "", "", "nginx_apache_fpm", []string{}} }
func DecodeConfig(r io.Reader) (Config, error) {
	var c Config
	raw, err := io.ReadAll(io.LimitReader(r, 65537))
	if err != nil {
		return c, err
	}
	if len(raw) > 65536 {
		return c, errors.New("configuration exceeds 64 KiB")
	}
	// Reject duplicate top-level keys instead of silently choosing one value.
	scan := json.NewDecoder(bytes.NewReader(raw))
	token, err := scan.Token()
	if err != nil || token != json.Delim('{') {
		return c, errors.New("a JSON object is required")
	}
	seen := map[string]bool{}
	for scan.More() {
		key, err := scan.Token()
		if err != nil {
			return c, err
		}
		name, ok := key.(string)
		if !ok || seen[name] {
			return c, errors.New("duplicate or invalid configuration key")
		}
		seen[name] = true
		var value json.RawMessage
		if err = scan.Decode(&value); err != nil {
			return c, err
		}
		if bytes.Equal(bytes.TrimSpace(value), []byte("null")) {
			return c, errors.New("configuration values must not be null")
		}

	}
	if _, err = scan.Token(); err != nil {
		return c, err
	}
	for _, required := range []string{"schema_version", "admin_port", "user_port", "admin_host", "user_host", "webstack", "modules"} {
		if !seen[required] {
			return c, fmt.Errorf("missing configuration key: %s", required)
		}
	}
	d := json.NewDecoder(bytes.NewReader(raw))
	d.DisallowUnknownFields()
	if err = d.Decode(&c); err != nil {
		return c, err
	}
	var extra any
	if d.Decode(&extra) != io.EOF {
		return c, errors.New("one JSON object is required")
	}
	if c.Modules == nil {
		return c, errors.New("modules must be an array, not null")
	}
	return c, c.Validate()
}
func Targeted(f Facts) bool {
	if !idPattern.MatchString(f.ID) || !versionPattern.MatchString(f.Version) {
		return false
	}
	switch f.ID {
	case "debian":
		return f.Version == "12" || f.Version == "13"
	case "ubuntu":
		return f.Version == "24.04" || f.Version == "26.04"
	case "almalinux":
		major := strings.Split(f.Version, ".")[0]
		return major == "9" || major == "10"
	}
	return false
}
func hostname(h string) bool {
	if h == "" {
		return true
	}
	if len(h) > 253 || h != strings.ToLower(h) || !strings.Contains(h, ".") {
		return false
	}
	for _, l := range strings.Split(h, ".") {
		if !labelPattern.MatchString(l) {
			return false
		}
	}
	return true
}
func (c Config) Validate() error {
	if c.SchemaVersion != 1 {
		return errors.New("unsupported configuration schema")
	}
	if c.AdminPort < 1024 || c.AdminPort > 65535 || c.UserPort < 1024 || c.UserPort > 65535 || c.AdminPort == c.UserPort {
		return errors.New("distinct unprivileged ports 1024..65535 are required")
	}
	if !hostname(c.AdminHost) || !hostname(c.UserHost) {
		return errors.New("use lowercase ASCII DNS hostnames, without schemes, paths or ports")
	}
	if c.UserHost != "" && (c.AdminHost == "" || c.AdminHost == c.UserHost) {
		return errors.New("user portal requires a distinct admin hostname; ports do not isolate cookies")
	}
	valid := false
	for _, p := range Profiles {
		if p == c.WebStack {
			valid = true
		}
	}
	if !valid {
		return errors.New("unknown webstack profile")
	}
	allowed := map[string]bool{"dns": true, "mail": true, "database": true, "sftp": true, "backup": true}
	seen := map[string]bool{}
	for _, m := range c.Modules {
		if !allowed[m] || seen[m] {
			return fmt.Errorf("unknown or repeated native module: %q", m)
		}
		seen[m] = true
	}
	return nil
}
func Build(f Facts, c Config) (Plan, error) {
	if !Targeted(f) {
		return Plan{}, errors.New("distribution/version is not in the target matrix")
	}
	if f.Architecture != "amd64" {
		return Plan{}, errors.New("only amd64 is in this development matrix")
	}
	if err := c.Validate(); err != nil {
		return Plan{}, err
	}
	canonical, _ := json.Marshal(struct {
		F Facts
		C Config
	}{f, c})
	sum := sha256.Sum256(canonical)
	pm := "apt"
	if f.ID == "almalinux" {
		pm = "dnf"
	}
	p := Plan{SchemaVersion: 1, Facts: f, Config: c, InputDigest: hex.EncodeToString(sum[:]), PackageManager: pm,
		Components: []string{"panel.php>=8.2", "panel.symfony=7.4", "panel.postgresql", "panel.https-gateway", "agent.go"},
		Executable: false, Blockers: []string{"production_apply_not_implemented", "signed_release_channel_not_configured", "os_package_manifests_not_certified"},
		Notes: []string{"No packages, users, files, listeners or firewall rules are modified.", "Requirements are symbolic, not verified package names or availability.", "User portal remains disabled until hostname/TLS and authorization checks pass.", "Panel runtime and gateway must remain independent of customer webstacks.", "Preserve SELinux/AppArmor and existing services; never disable them to resolve a conflict.", "Bootstrap activation uses PostgreSQL in v0.7; v0.6 local tokens are not accepted by the web application."}}
	for _, v := range []Step{
		{"preflight", "inspect", "Detect privileges, systemd, capacity, repositories, existing services and port conflicts"},
		{"release.verify", "verify", "Verify release signature against independently provisioned trust root"},
		{"packages.resolve", "plan", "Resolve and verify OS-specific package versions and runtime compatibility"},
		{"core.install", "install", "Install panel, private PHP runtime, database and Go binaries"},
		{"security.apply", "configure", "Create least-privilege identities and mandatory access-control policies"},
		{"database.migrate", "migrate", "Create the singleton bootstrap guard and initial schema transactionally"},
		{"gateway.configure", "configure", "Prepare verified HTTPS access on the administrator endpoint only"},
		{"health.verify", "verify", "Check the panel, local agent and database before issuing a token"},
		{"bootstrap.issue", "authorize", "Issue one expiring token on the controlling terminal"},
		{"wizard.open", "handoff", "Display access URL; webstack and optional services are deferred to the wizard"},
	} {
		p.Steps = append(p.Steps, v)
	}
	return p, nil
}
