<!-- forgepanel-doc id=FP-07-PORTALS revision=3 status=specified -->
# FORGE / PANEL access — fixed ports, autodetected IP and domain

[Français](../../fr/07-interfaces-roles/portal-access-routing.md) · [Roles](README.md) · [Tests](../13-tests-quality/portal-access-gates.md)

> **SPECIFIED / not implemented.** Owner correction on 6 November 2026: **no customizable domain input**. ForgePanel must discover the machine's IP address automatically and also detect a usable existing domain name, if any. Approved paths and ports remain unchanged. SRC-03 does not yet ship these two portals.

## Expected access without a domain-entry field

| Surface | Autodetected machine IP | If machine FQDN is discovered and verified | Prefix and port |
|---|---|---|---|
| FORGE, server administration | `https://<detected-IP>:8447/forge` | `https://<verified-FQDN>:8447/forge` | `/forge`, 8447 |
| PANEL, customer hosting | `https://<detected-IP>:8446/panel` | `https://<verified-FQDN>:8446/panel` | `/panel`, 8446 |

IPv6 literals require brackets, e.g. `https://[2001:db8::10]:8447/forge` (documentation-only illustrative address). **The same existing FQDN may serve both surfaces: the port and path define the portal.** Never assume `forge.domain`, `panel.domain` or automatically generated subdomains.

**Port 443 is not an automatically provisioned access path**: a pre-existing HTTPS reverse proxy/virtual host may be considered separately only after explicit qualification. The installer does not create domains, DNS entries or aliases for either portal. Root `/` redirects remain undecided.

## Automatic discovery and checks without false confidence

1. Inspect OS network interfaces and routing tables read-only to list assigned IPv4 and IPv6 addresses. Reject loopback and unusable/interface-incompatible candidates. A private IP may be reachable on a LAN but must not be described as public.
2. Determine which detected addresses can actually serve the respective 8447/8446 listener. NAT, proxies, external IPs and firewalls mean an interface IP does not necessarily equal the public address. Never invent a public IP or contact an external discovery service without an approved policy.
3. Obtain system hostname/FQDN as a **candidate**, not proof from `/etc/hosts`, reverse DNS alone or request `Host`. Check DNS A/AAAA records, actually published address families and verified network routing to this server (including separately verified NAT where applicable).
4. Check TLS certificates, relevant SNI, listeners and reachability. A direct HTTPS-by-IP URL cannot be advertised as **trusted and working** without a valid certificate covering that IP. Never instruct users to bypass TLS warnings.
5. Present results as `VERIFIED`, `UNVERIFIED` or `UNAVAILABLE` with provenance and failure reasons. If no domain is found, show **no domain-based link**. Preserve and verify a secure local administrative fallback.

Certificate provider, NAT discovery and actual bind addresses are open technical choices, **not assumed defaults**.

## Routing and security requirements

| ID | Requirement | Expected verification |
|---|---|---|
| PORTAL-FP-0001 | FORGE retains `/forge` and HTTPS **8447**. | Admin listener/authorization, no automatic Linux root privilege. |
| PORTAL-FP-0002 | PANEL retains `/panel` and HTTPS **8446**. | Customer listener and cross-tenant RBAC isolation. |
| PORTAL-FP-0003 | OS-detected IP; existing FQDN discovered and **verified**, never freely configured. | No customizable-domain field or automatic subdomain generation. |
| PORTAL-FP-0004 | Authorization applies across HTTP, API, services and Go agent. | PANEL account cannot execute FORGE admin actions. |
| PORTAL-FP-0005 | Independent admin/customer sessions and cookies; MFA stays optional. | Separate login, CSRF, rotation and logout. |
| PORTAL-FP-0006 | Different ports on one IP do not isolate cookies. | Distinct cookie names, independent session contexts and server guards. |
| PORTAL-FP-0007 | Historical `/setup` reserved for FORGE bootstrap after reviewed migration. | No setup path reachable from PANEL. |
| PORTAL-FP-0008 | Reject untrusted hosts and proxy headers. | Prevent Host spoofing, forged `Forwarded` and open redirects. |
| PORTAL-FP-0009 | Per-portal Twig/UX/JS/CSS bundles and themes. | No asset collision or widget privilege bypass. |
| PORTAL-FP-0010 | Changes to listeners, DNS/TLS, firewall or fallback follow Q47. | Plan, backup, health, audit and recovery. |
| PORTAL-FP-0011 | The private Hub is neither a dependency nor a route of standard Core. | No publisher secrets or privileges in either portal. |
| PORTAL-FP-0012 | Generated URLs use only **verified discovered** access origins. | No invented URLs or origins derived from unchecked `Host`. |

## Target implementation and limits

- **Symfony**: `/forge/**` and `/panel/**` routes, distinct firewalls, sessions and authorization. Go agent independently validates typed Linux operations; no generic `shell.exec` API.
- **Discovery**: read-only inventory of host IP/FQDN with status/provenance; no automatic DNS changes. Failed verification yields diagnosis, not a fabricated working link.
- **Installer**: discover access, select bind interfaces only after technical qualification, check TLS/firewall; **no customizable domain input**. Preserve fallback admin access throughout changes.
- **UI**: isolated headers/sidebars, branding and CSS per portal; permissions never depend on theme.
- **Migration**: prototype `/setup` and `__Host-FORGE_ADMIN` must be reviewed, not claimed active at `/forge`.

[API/ingress contract](../08-api-contracts/portal-route-boundary.md) · [Candidate registry](../../../evidence/portal-access-registry-v1.json) · [Planned QA](../13-tests-quality/portal-access-gates.md).

**Status:** JSON/documentation validation is static only; no real IP discovery, DNS/TLS probe, Symfony login, VM or installation has been qualified here.
