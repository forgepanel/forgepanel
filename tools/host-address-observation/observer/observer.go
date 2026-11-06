// Package observer reports OS-assigned addresses and a possible host FQDN.
// It never verifies public reachability, DNS, TLS, or a running ForgePanel.
package observer

import (
    "net"
    "net/netip"
    "os"
    "sort"
    "strings"
    "unicode"
)

const (
    maxInterfaces = 128
    maxIPs = 256
)

// Source makes all network-interface reads injectable for offline tests.
type Source interface {
    Interfaces() ([]net.Interface, error)
    Addrs(net.Interface) ([]net.Addr, error)
    Hostname() (string, error)
}

type OSSource struct{}
func (OSSource) Interfaces() ([]net.Interface, error) { return net.Interfaces() }
func (OSSource) Addrs(i net.Interface) ([]net.Addr, error) { return i.Addrs() }
func (OSSource) Hostname() (string, error) { return os.Hostname() }

type Portal struct {
    Name string `json:"name"`
    Path string `json:"path"`
    HTTPSPort int `json:"https_port"`
}

type Address struct {
    Interface string `json:"interface"`
    IP string `json:"ip"`
    Family string `json:"family"`
    Scope string `json:"scope"`
    Status string `json:"status"`
}

type Report struct {
    SchemaVersion int `json:"schema_version"`
    ToolName string `json:"tool_name"`
    ObservationStatus string `json:"observation_status"`
    Addresses []Address `json:"addresses"`
    FQDNCandidate string `json:"fqdn_candidate,omitempty"`
    FQDNStatus string `json:"fqdn_status"`
    Portals []Portal `json:"portals"`
    DNSVerification string `json:"dns_verification"`
    TLSVerification string `json:"tls_verification"`
    ListenerVerification string `json:"listener_verification"`
    PublicReachability string `json:"public_reachability"`
    VerifiedAccessURLs []string `json:"verified_access_urls"`
    Warnings []string `json:"warnings"`
}

func newReport() Report {
    return Report{
        SchemaVersion: 1, ToolName: "forgepanel-host-address-observation",
        ObservationStatus: "UNAVAILABLE", Addresses: []Address{},
        FQDNStatus: "UNAVAILABLE",
        Portals: []Portal{
            {Name: "FORGE", Path: "/forge", HTTPSPort: 8447},
            {Name: "PANEL", Path: "/panel", HTTPSPort: 8446},
        },
        DNSVerification: "NOT_EXECUTED", TLSVerification: "NOT_EXECUTED",
        ListenerVerification: "NOT_EXECUTED", PublicReachability: "NOT_EXECUTED",
        VerifiedAccessURLs: []string{}, Warnings: []string{},
    }
}

func validFQDN(s string) bool {
    if len(s) < 3 || len(s) > 253 || net.ParseIP(s) != nil { return false }
    labels := strings.Split(s, ".")
    if len(labels) < 2 { return false }
    for _, label := range labels {
        if len(label) < 1 || len(label) > 63 || label[0] == '-' || label[len(label)-1] == '-' { return false }
        for _, c := range label {
            if !((c >= 'a' && c <= 'z') || (c >= '0' && c <= '9') || c == '-') { return false }
        }
    }
    numericTLD := true
    for _, c := range labels[len(labels)-1] {
        if c < '0' || c > '9' { numericTLD = false; break }
    }
    return !numericTLD
}

func cleanInterfaceName(name string) string {
    if name == "" || len(name) > 32 { return "unknown" }
    for _, c := range name {
        if unicode.IsControl(c) || c > 127 { return "unknown" }
    }
    return name
}

func ipOf(addr net.Addr) net.IP {
    switch v := addr.(type) {
    case *net.IPNet: return v.IP
    case *net.IPAddr: return v.IP
    default: return nil
    }
}

// Inspect reads OS facts only. No DNS query, external call, socket bind,
// network configuration, TLS dial, shell or privileged action is permitted.
func Inspect(source Source) Report {
    r := newReport()
    partial := false
    interfaces, err := source.Interfaces()
    if err != nil {
        r.Warnings = append(r.Warnings, "interfaces_unavailable")
    } else {
        r.ObservationStatus = "OBSERVED_UNVERIFIED"
        sort.Slice(interfaces, func(i, j int) bool { return interfaces[i].Name < interfaces[j].Name })
        if len(interfaces) > maxInterfaces {
            interfaces = interfaces[:maxInterfaces]
            partial = true
            r.Warnings = append(r.Warnings, "interfaces_truncated")
        }
        seen := make(map[string]bool)
        for _, iface := range interfaces {
            if iface.Flags&net.FlagUp == 0 || iface.Flags&net.FlagLoopback != 0 { continue }
            addrs, addrErr := source.Addrs(iface)
            if addrErr != nil {
                partial = true
                r.Warnings = append(r.Warnings, "interface_addresses_unavailable")
                continue
            }
            for _, addr := range addrs {
                candidate, valid := netip.AddrFromSlice(ipOf(addr))
                if !valid { continue }
                candidate = candidate.Unmap()
                if !candidate.IsGlobalUnicast() || candidate.IsLoopback() || candidate.IsLinkLocalUnicast() || candidate.IsUnspecified() { continue }
                key := candidate.String()
                if seen[key] { continue }
                if len(r.Addresses) >= maxIPs {
                    partial = true
                    r.Warnings = append(r.Warnings, "addresses_truncated")
                    break
                }
                seen[key] = true
                family := "IPv6"
                if candidate.Is4() { family = "IPv4" }
                scope := "NON_PRIVATE_UNVERIFIED"
                if candidate.IsPrivate() { scope = "PRIVATE_UNVERIFIED" }
                r.Addresses = append(r.Addresses, Address{
                    Interface: cleanInterfaceName(iface.Name), IP: key,
                    Family: family, Scope: scope, Status: "UNVERIFIED",
                })
            }
            if len(r.Addresses) >= maxIPs {
                partial = true
                r.Warnings = append(r.Warnings, "addresses_capacity_reached")
                break
            }
        }
        sort.Slice(r.Addresses, func(i, j int) bool {
            if r.Addresses[i].Family != r.Addresses[j].Family {
                return r.Addresses[i].Family < r.Addresses[j].Family
            }
            return r.Addresses[i].IP < r.Addresses[j].IP
        })
    }

    hostname, hostErr := source.Hostname()
    if hostErr != nil {
        r.FQDNStatus = "UNAVAILABLE"
        r.Warnings = append(r.Warnings, "hostname_unavailable")
    } else {
        hostname = strings.ToLower(strings.TrimSuffix(hostname, "."))
        if validFQDN(hostname) {
            r.FQDNCandidate = hostname
            r.FQDNStatus = "CANDIDATE_UNVERIFIED"
        } else {
            r.FQDNStatus = "NONE"
        }
    }
    if partial { r.ObservationStatus = "PARTIAL_UNVERIFIED" }
    return r
}

// InspectHost is an unprivileged read-only observation of this OS.
func InspectHost() Report { return Inspect(OSSource{}) }
