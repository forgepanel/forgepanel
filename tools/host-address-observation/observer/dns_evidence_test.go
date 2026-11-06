package observer

import (
	"context"
	"errors"
	"net"
	"strings"
	"testing"
)

type fakeResolver struct {
	answers []net.IPAddr
	err error
	calls int
	seen string
}
func (f *fakeResolver) LookupIPAddr(_ context.Context, host string) ([]net.IPAddr, error) {
	f.calls++
	f.seen = host
	return f.answers, f.err
}
func ipRecord(s string) net.IPAddr { return net.IPAddr{IP: net.ParseIP(s)} }
func inventory(host string, assigned ...string) Report {
	r := newReport()
	r.FQDNCandidate = host
	r.FQDNStatus = "CANDIDATE_UNVERIFIED"
	for _, ip := range assigned { r.Addresses = append(r.Addresses, Address{IP: ip}) }
	return r
}
func TestDNSNoFQDNNeverLooksUp(t *testing.T) {
	r := &fakeResolver{answers: []net.IPAddr{ipRecord("192.0.2.10")}}
	out := InspectResolver(context.Background(), newReport(), r)
	if r.calls != 0 || out.ResolverStatus != "NO_FQDN" || len(out.VerifiedAccessURLs) != 0 { t.Fatalf("bad no-domain: %+v", out) }
}
func TestDNSRejectInjectedHostnameWithoutLookup(t *testing.T) {
	for _, name := range []string{"host.example.com\nevil", "bad/host.example.com", "localhost", "1.2.3.4"} {
		r := &fakeResolver{}
		out := InspectResolver(context.Background(), inventory(name), r)
		if r.calls != 0 || out.ResolverStatus != "NO_FQDN" { t.Fatalf("unsafe lookup (%q): %+v", name, out) }
	}
}
func TestDNSMatchedLocalStillUnverified(t *testing.T) {
	r := &fakeResolver{answers: []net.IPAddr{ipRecord("2001:db8::3"), ipRecord("192.0.2.12"), ipRecord("192.0.2.12")}}
	out := InspectResolver(context.Background(), inventory("node.example.org", "2001:db8::3", "192.0.2.12"), r)
	if r.calls != 1 || r.seen != "node.example.org" || out.ResolverStatus != "MATCHED_LOCAL_OS_RESOLVER_ONLY" || len(out.ResolvedAddresses) != 2 || len(out.NonlocalAddresses) != 0 { t.Fatalf("bad match: %+v", out) }
	if out.DNSAuthorityVerified || len(out.VerifiedAccessURLs) != 0 || out.TLSVerification != "NOT_EXECUTED" || out.PublicReachability != "NOT_EXECUTED" { t.Fatal("local lookup promoted to public proof") }
}
func TestDNSNATOrUnmappedEvidence(t *testing.T) {
	out := InspectResolver(context.Background(), inventory("node.example.org", "10.0.0.2"), &fakeResolver{answers: []net.IPAddr{ipRecord("198.51.100.2")}})
	if out.ResolverStatus != "NAT_OR_REMOTE_ROUTING_UNVERIFIED" || len(out.NonlocalAddresses) != 1 { t.Fatalf("NAT gap hidden: %+v", out) }
}
func TestDNSRejectLoopbackEvenIfAssigned(t *testing.T) {
	out := InspectResolver(context.Background(), inventory("node.example.org", "127.0.0.1", "192.0.2.2"), &fakeResolver{answers: []net.IPAddr{ipRecord("127.0.0.1"), ipRecord("192.0.2.2")}})
	if out.ResolverStatus != "REJECTED_RESOLVER_ANSWERS_UNVERIFIED" || out.RejectedAnswerCount != 1 || len(out.LocallyAssignedAddresses) != 1 { t.Fatalf("unusable address promoted: %+v", out) }
}
func TestDNSErrorOnlySafeWarnings(t *testing.T) {
	secret := "sensitive private-resolver error details"
	out := InspectResolver(context.Background(), inventory("node.example.org"), &fakeResolver{err: errors.New(secret)})
	if out.ResolverStatus != "RESOLVER_ERROR_UNVERIFIED" || strings.Contains(strings.Join(out.Warnings, ","), secret) { t.Fatalf("unredacted failure: %+v", out) }
}
func TestDNSAnswerLimitFailsClosed(t *testing.T) {
	answers := make([]net.IPAddr, 33)
	for i := range answers { answers[i] = ipRecord("192.0.2.2") }
	out := InspectResolver(context.Background(), inventory("node.example.org", "192.0.2.2"), &fakeResolver{answers: answers})
	if out.ResolverStatus != "TOO_MANY_ANSWERS_UNVERIFIED" || len(out.ResolvedAddresses) != 0 { t.Fatalf("limit: %+v", out) }
}
func TestDNSNilResolverFailsClosed(t *testing.T) {
	out := InspectResolver(context.Background(), inventory("node.example.org"), nil)
	if out.ResolverStatus != "RESOLVER_UNAVAILABLE" || len(out.VerifiedAccessURLs) != 0 { t.Fatalf("nil resolver: %+v", out) }
}
func TestDNSMappedIPv4Normalized(t *testing.T) {
	out := InspectResolver(context.Background(), inventory("node.example.org", "192.0.2.2"), &fakeResolver{answers: []net.IPAddr{ipRecord("::ffff:192.0.2.2")}})
	if out.ResolverStatus != "MATCHED_LOCAL_OS_RESOLVER_ONLY" || len(out.ResolvedAddresses) != 1 || out.ResolvedAddresses[0] != "192.0.2.2" { t.Fatalf("mapped: %+v", out) }
}
func TestDNSEmptyAnswerNoFalseSuccess(t *testing.T) {
	out := InspectResolver(context.Background(), inventory("node.example.org", "192.0.2.2"), &fakeResolver{})
	if out.ResolverStatus != "NO_ADDRESS_ANSWERS_UNVERIFIED" || len(out.VerifiedAccessURLs) != 0 { t.Fatalf("empty response: %+v", out) }
}
