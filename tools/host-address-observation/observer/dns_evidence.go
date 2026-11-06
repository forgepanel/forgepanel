// Package observer's optional DNS evidence uses the local OS resolver only.
// A match is not authoritative/public DNS, working HTTPS, or reachable access.
package observer

import (
	"context"
	"net"
	"net/netip"
	"sort"
	"time"
)

const (
	maxResolverAnswers = 32
	resolverTimeout = 4 * time.Second
)

// Resolver is injectable; unit tests never make network queries.
type Resolver interface {
	LookupIPAddr(ctx context.Context, host string) ([]net.IPAddr, error)
}

type OSResolver struct{}

func (OSResolver) LookupIPAddr(ctx context.Context, host string) ([]net.IPAddr, error) {
	return net.DefaultResolver.LookupIPAddr(ctx, host)
}

type DNSReport struct {
	SchemaVersion int `json:"schema_version"`
	ToolName string `json:"tool_name"`
	CandidateHostname string `json:"candidate_hostname,omitempty"`
	ResolverStatus string `json:"resolver_status"`
	ResolvedAddresses []string `json:"resolved_addresses"`
	LocallyAssignedAddresses []string `json:"locally_assigned_addresses"`
	NonlocalAddresses []string `json:"nonlocal_addresses"`
	RejectedAnswerCount int `json:"rejected_answer_count"`
	DNSAuthorityVerified bool `json:"dns_authority_verified"`
	PublicReachability string `json:"public_reachability"`
	TLSVerification string `json:"tls_verification"`
	ListenerVerification string `json:"listener_verification"`
	VerifiedAccessURLs []string `json:"verified_access_urls"`
	Warnings []string `json:"warnings"`
}

func newDNSReport() DNSReport {
	return DNSReport{
		SchemaVersion: 1, ToolName: "forgepanel-os-resolver-observation",
		ResolverStatus: "NOT_EXECUTED",
		ResolvedAddresses: []string{}, LocallyAssignedAddresses: []string{},
		NonlocalAddresses: []string{}, VerifiedAccessURLs: []string{},
		PublicReachability: "NOT_EXECUTED", TLSVerification: "NOT_EXECUTED",
		ListenerVerification: "NOT_EXECUTED", Warnings: []string{},
	}
}

// InspectResolver performs at most one bounded, opt-in lookup of the local
// machine's FQDN candidate. /etc/hosts or split DNS may affect the answer.
func InspectResolver(ctx context.Context, host Report, resolver Resolver) DNSReport {
	out := newDNSReport()
	if host.FQDNStatus != "CANDIDATE_UNVERIFIED" || !validFQDN(host.FQDNCandidate) {
		out.ResolverStatus = "NO_FQDN"
		return out
	}
	out.CandidateHostname = host.FQDNCandidate
	if resolver == nil {
		out.ResolverStatus = "RESOLVER_UNAVAILABLE"
		out.Warnings = append(out.Warnings, "resolver_unavailable")
		return out
	}
	timed, cancel := context.WithTimeout(ctx, resolverTimeout)
	defer cancel()
	answers, err := resolver.LookupIPAddr(timed, out.CandidateHostname)
	if err != nil {
		out.ResolverStatus = "RESOLVER_ERROR_UNVERIFIED"
		out.Warnings = append(out.Warnings, "os_resolver_error")
		return out
	}
	if timed.Err() != nil {
		out.ResolverStatus = "RESOLVER_ERROR_UNVERIFIED"
		out.Warnings = append(out.Warnings, "os_resolver_context_expired")
		return out
	}
	if len(answers) > maxResolverAnswers {
		out.ResolverStatus = "TOO_MANY_ANSWERS_UNVERIFIED"
		out.Warnings = append(out.Warnings, "resolver_answer_limit")
		return out
	}
	local := make(map[string]bool, len(host.Addresses))
	for _, address := range host.Addresses {
		parsed, err := netip.ParseAddr(address.IP)
		if err != nil { continue }
		local[parsed.Unmap().String()] = true
	}
	seen := make(map[string]bool, len(answers))
	for _, answer := range answers {
		ip, ok := netip.AddrFromSlice(answer.IP)
		if !ok { out.RejectedAnswerCount++; continue }
		ip = ip.Unmap()
		if !ip.IsGlobalUnicast() || ip.IsLoopback() || ip.IsLinkLocalUnicast() || ip.IsUnspecified() {
			out.RejectedAnswerCount++
			continue
		}
		s := ip.String()
		if seen[s] { continue }
		seen[s] = true
		out.ResolvedAddresses = append(out.ResolvedAddresses, s)
		if local[s] {
			out.LocallyAssignedAddresses = append(out.LocallyAssignedAddresses, s)
		} else {
			out.NonlocalAddresses = append(out.NonlocalAddresses, s)
		}
	}
	sort.Strings(out.ResolvedAddresses)
	sort.Strings(out.LocallyAssignedAddresses)
	sort.Strings(out.NonlocalAddresses)
	switch {
	case out.RejectedAnswerCount > 0:
		out.ResolverStatus = "REJECTED_RESOLVER_ANSWERS_UNVERIFIED"
		out.Warnings = append(out.Warnings, "unusable_resolver_address")
	case len(out.ResolvedAddresses) == 0:
		out.ResolverStatus = "NO_ADDRESS_ANSWERS_UNVERIFIED"
	case len(out.NonlocalAddresses) > 0:
		out.ResolverStatus = "NAT_OR_REMOTE_ROUTING_UNVERIFIED"
	default:
		out.ResolverStatus = "MATCHED_LOCAL_OS_RESOLVER_ONLY"
	}
	return out
}
