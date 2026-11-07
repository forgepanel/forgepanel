//go:build linux

package doctor

import "testing"

func TestOSSupport(t *testing.T) {
	cases := []struct {
		id, ver string
		want    bool
	}{
		{"debian", "12", true}, {"debian", "13", true}, {"ubuntu", "24.04", true},
		{"ubuntu", "26.04", true}, {"almalinux", "9.6", true}, {"almalinux", "10", true},
		{"debian", "11", false}, {"ubuntu", "25.04", false}, {"almalinux", "8.10", false},
	}
	for _, tt := range cases {
		if got := SupportedOS(tt.id, tt.ver); got != tt.want {
			t.Errorf("%s %s: got %t want %t", tt.id, tt.ver, got, tt.want)
		}
	}
}

func TestParseOSRelease(t *testing.T) {
	m := ParseOSRelease("# comment\nID=ubuntu\nVERSION_ID=\"24.04\"\nNAME=\"Ubuntu Linux\"\n")
	if m["ID"] != "ubuntu" || m["VERSION_ID"] != "24.04" || m["NAME"] != "Ubuntu Linux" {
		t.Fatalf("unexpected: %+v", m)
	}
}
