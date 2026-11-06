<!-- forgepanel-doc id=FP-08-PORTAL-ROUTING revision=2 status=specified -->
# Candidate contract — access discovery and FORGE / PANEL surface resolution

[Français](../../fr/08-api-contracts/portal-route-boundary.md) · [API index](README.md) · [Access convention](../07-interfaces-roles/portal-access-routing.md)

**SPECIFIED, not implemented.** Owner correction: **no customizable domain input**, automatic discovery of the host's IPs and an existing, verified domain if present. The `/forge`, `/panel` route prefixes and `8447`, `8446` ports remain fixed. This document does not implement any live URL or network action.

## Discover IP and FQDN independently of client requests

1. **Read-only host inventory**: inspect network interfaces, routes, assigned IPv4/IPv6 addresses and bind targets; keep interface, address family, scope and verification status. Exclude loopback/unusable addresses. A private IP may be valid on a LAN but does not imply public reachability.
2. **Existing FQDN**: ask the OS hostname/resolver for a candidate and verify published A/AAAA and actual authorized reachable routing. Reverse DNS alone, `/etc/hosts` alone or request `Host` are not proof. If NAT is involved, verify the reachable path using an expressly approved method; otherwise mark `UNVERIFIED`.
3. **TLS**: the certificate must cover the chosen access address (IP-SAN for an IP URL, DNS name for an FQDN URL). Never bypass certificate validation. Listener, certificate and network probe evidence are needed before reporting `VERIFIED`.
4. **Display**: only present working links for verified address/port/prefix combinations. With no FQDN, show **no domain link** and do not request manual domain entry. Certificate/NAT details and a secure local fallback remain subject to qualification.
5. **443**: do not generate a virtual host, DNS record or redirect automatically. Support for an already deployed 443 HTTPS gateway is a separate qualified integration, not the standard access mode.

## Surface resolution matrix (illustrative origins)

| Request | Surface decision |
|---|---|
| `https://<detected-IP>:8447/forge` | FORGE if listener, certificate and authorization are valid |
| `https://<detected-IP>:8446/panel` | PANEL if listener, certificate and authorization are valid |
| `https://<detected-IP>:8447/panel` | DENY |
| `https://<detected-IP>:8446/forge` | DENY |
| `https://<verified-FQDN>:8447/forge` | FORGE if DNS, routing, TLS and authorization are verified |
| `https://<verified-FQDN>:8446/panel` | PANEL if DNS, routing, TLS and authorization are verified |
| `https://<verified-FQDN>:8447/panel` and `...:8446/forge` | DENY |
| FQDN missing, unresolvable or inconsistent with reachable route | No domain link advertised |
| IP found only on a private LAN | LAN candidate, never claimed publicly reachable |
| Forged Host/proxy headers or unknown domain | DENY; no authorization/redirect from untrusted values |
| `https://<host>:443/forge` or `/panel` | Not automatically provided; separate qualified integration |
| Historical `/setup` | NOT MIGRATED; review required |

IPv6 literals must be enclosed in `[brackets]` in URLs. The same IP or FQDN may serve both interfaces: ports and prefixes combined with authorization select the surface. Browsers share cookies across ports on one host; **never** assume that changing ports isolates sessions.

## Security boundaries and failures

- **Ingress**: listener + canonical path + trusted Host (when applicable) + valid TLS. A discovered FQDN candidate does not grant route permissions; ignore browser-supplied surface identity.
- **Symfony**: two route spaces, distinct host-only `Secure`, `HttpOnly`, `SameSite` cookies, independent server sessions/CSRF/rotation, resource-level RBAC in APIs and services. MFA optional; sensitive reauthentication/approvals follow Q66/Q76.
- **Go**: no Linux privilege from a path, port or UI role alone. Revalidate identity, resource scope and allowlisted typed operation; no arbitrary `shell.exec`.
- **Proxies**: only explicitly trusted proxies may supply authoritative `Forwarded`/`X-Forwarded-*`. Generate callback URLs from approved verified origins, never raw Host.
- **UI/Hub**: independent FORGE/PANEL bundles and themes; private Hub detached, no publisher routes, secrets or privilege in public Core.
- **Installer**: no custom hostname entry form. Preserve admin fallback and never overwrite third-party network config during discovery.

## Gates and evidence

The [static candidate registry](../../../evidence/portal-access-registry-v1.json) and [contract tests](../../../tests/documentation/test_portal_access_contract.py) check consistency only, without probing real interfaces or certifying URLs. The [22 planned HTTP/VM tests](../13-tests-quality/portal-access-gates.md) must run after genuine source import R1, Symfony/PostgreSQL R2, and TLS gateway/installer R3. **This document certifies no IP, domain, certificate, listener or running route.**
