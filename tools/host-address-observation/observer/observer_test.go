package observer

import (
    "errors"
    "net"
    "strings"
    "testing"
)

type fakeSource struct {
    interfaces []net.Interface
    addresses map[string][]net.Addr
    hostname string
    ifErr error
    hostErr error
    addrErr map[string]error
}
func (f fakeSource) Interfaces() ([]net.Interface, error) { return f.interfaces, f.ifErr }
func (f fakeSource) Addrs(iface net.Interface) ([]net.Addr, error) { return f.addresses[iface.Name], f.addrErr[iface.Name] }
func (f fakeSource) Hostname() (string, error) { return f.hostname, f.hostErr }

func network(raw string) net.Addr {
    ip := net.ParseIP(raw)
    if ip == nil { panic("invalid fixture IP: "+raw) }
    bits := 128
    if ip.To4()!=nil { bits=32 }
    return &net.IPNet{IP: ip, Mask: net.CIDRMask(bits,bits)}
}
func up(name string) net.Interface { return net.Interface{Name:name,Flags:net.FlagUp} }

func TestPortalConventionAndNoNetworkClaims(t *testing.T) {
    r:=Inspect(fakeSource{hostname:"host.example.org"})
    if len(r.Portals)!=2 ||
        r.Portals[0]!=(Portal{Name:"FORGE",Path:"/forge",HTTPSPort:8447}) ||
        r.Portals[1]!=(Portal{Name:"PANEL",Path:"/panel",HTTPSPort:8446}) {
        t.Fatalf("unexpected portals: %+v",r.Portals)
    }
    if len(r.VerifiedAccessURLs)!=0 || r.DNSVerification!="NOT_EXECUTED" ||
        r.TLSVerification!="NOT_EXECUTED" || r.ListenerVerification!="NOT_EXECUTED" ||
        r.PublicReachability!="NOT_EXECUTED" {
        t.Fatalf("no TLS/DNS/reachability claims allowed: %+v",r)
    }
}

func TestIPv4IPv6FilteringAndScope(t *testing.T) {
    f:=fakeSource{
        hostname:"node.example.org",
        interfaces:[]net.Interface{up("eth0"),{Name:"lo",Flags:net.FlagUp|net.FlagLoopback},{Name:"down"}},
        addresses:map[string][]net.Addr{
            "eth0":{network("10.10.1.5"),network("2001:db8::10"),network("fd00::1"),network("169.254.1.1"),network("fe80::1"),network("224.0.0.1"),network("0.0.0.0"),network("::1")},
            "lo":{network("127.0.0.1")},
            "down":{network("192.0.2.40")},
        },
    }
    r:=Inspect(f)
    if len(r.Addresses)!=3 { t.Fatalf("bad IP filter: %+v",r.Addresses) }
    expected:=map[string]string{"10.10.1.5":"PRIVATE_UNVERIFIED","2001:db8::10":"NON_PRIVATE_UNVERIFIED","fd00::1":"PRIVATE_UNVERIFIED"}
    for _,a:=range r.Addresses {
        if expected[a.IP]!=a.Scope || a.Status!="UNVERIFIED" { t.Errorf("bad address: %+v",a) }
    }
    if r.ObservationStatus!="OBSERVED_UNVERIFIED" || r.FQDNStatus!="CANDIDATE_UNVERIFIED" {
        t.Fatalf("inaccurate status: %+v",r)
    }
}

func TestStableSortingDedupAndMappedIPv4(t *testing.T) {
    f:=fakeSource{
        interfaces:[]net.Interface{up("z0"),up("a0")},
        addresses:map[string][]net.Addr{
            "z0":{network("203.0.113.7"),network("10.0.0.5")},
            "a0":{network("10.0.0.5"),network("::ffff:192.0.2.7")},
        },
    }
    r:=Inspect(f)
    if len(r.Addresses)!=3 || r.Addresses[0].IP!="10.0.0.5" || r.Addresses[0].Interface!="a0" ||
        r.Addresses[1].IP!="192.0.2.7" || r.Addresses[2].IP!="203.0.113.7" {
        t.Fatalf("sorting/dedup mismatch: %+v",r.Addresses)
    }
}

func TestFQDNCandidateCaseAndTrailingDot(t *testing.T) {
    r:=Inspect(fakeSource{hostname:"Node.Example.org."})
    if r.FQDNCandidate!="node.example.org" || r.FQDNStatus!="CANDIDATE_UNVERIFIED" {
        t.Fatalf("invalid FQDN candidate: %+v",r)
    }
}

func TestNoDomainOrGeneratedSubdomain(t *testing.T) {
    values:=[]string{"","localhost","node","127.0.0.1","node_bad.example.org",
        "evil.example.com/redirect","-bad.example.org","node..example.org",
        strings.Repeat("a",64)+".example.com","node.123","node.example.org"+string(rune(10))+"Injected: yes"}
    for _,raw:=range values {
        t.Run(raw,func(t *testing.T){
            r:=Inspect(fakeSource{hostname:raw})
            if r.FQDNStatus!="NONE" || r.FQDNCandidate!="" || len(r.VerifiedAccessURLs)!=0 {
                t.Fatalf("unsafe hostname in report: %+v",r)
            }
        })
    }
}

func TestInterfaceAndHostnameErrorsDoNotBecomeSuccess(t *testing.T) {
    r:=Inspect(fakeSource{ifErr:errors.New("unavailable"),hostErr:errors.New("unavailable")})
    if r.ObservationStatus!="UNAVAILABLE" || r.FQDNStatus!="UNAVAILABLE" ||
        len(r.Warnings)!=2 || len(r.Addresses)!=0 {
        t.Fatalf("unavailable source reported success: %+v",r)
    }
}

func TestPartialInterfaceFailureKeepsOtherEvidence(t *testing.T) {
    f:=fakeSource{
        interfaces:[]net.Interface{up("eth0"),up("eth1")},
        addresses:map[string][]net.Addr{"eth1":{network("192.168.4.2")}},
        addrErr:map[string]error{"eth0":errors.New("read blocked")},
    }
    r:=Inspect(f)
    if r.ObservationStatus!="PARTIAL_UNVERIFIED" || len(r.Addresses)!=1 ||
        len(r.Warnings)!=1 || r.Warnings[0]!="interface_addresses_unavailable" {
        t.Fatalf("partial error was hidden: %+v",r)
    }
}

func TestInterfaceNameIsSanitized(t *testing.T) {
    bad:="bad"+string(rune(10))+"secret"
    f:=fakeSource{
        interfaces:[]net.Interface{up(bad)},
        addresses:map[string][]net.Addr{bad:{network("192.168.10.1")}},
    }
    r:=Inspect(f)
    if len(r.Addresses)!=1 || r.Addresses[0].Interface!="unknown" {
        t.Fatalf("bad label allowed: %+v",r.Addresses)
    }
}

func TestLimitPreventsUnboundedListing(t *testing.T) {
    f:=fakeSource{interfaces:make([]net.Interface,maxInterfaces+1),addresses:map[string][]net.Addr{}}
    for i:=range f.interfaces { f.interfaces[i]=up(string(rune('a'+i%26))+string(rune('a'+(i/26)%26))) }
    r:=Inspect(f)
    if r.ObservationStatus!="PARTIAL_UNVERIFIED" || len(r.Warnings)==0 || r.Warnings[0]!="interfaces_truncated" {
        t.Fatalf("limit not reported: %+v",r)
    }
}

func TestHostnameCandidateDoesNotVerifyInternetEndpoint(t *testing.T) {
    f:=fakeSource{hostname:"node.example.org",interfaces:[]net.Interface{up("eth0")},
        addresses:map[string][]net.Addr{"eth0":{network("192.0.2.6")}}}
    r:=Inspect(f)
    if r.FQDNStatus=="VERIFIED" || len(r.VerifiedAccessURLs)!=0 {
        t.Fatal("hostname and IP facts promoted to verified endpoint")
    }
}
