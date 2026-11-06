<!-- forgepanel-doc id=FP-13-PORTAL-ACCESS revision=3 status=specified -->
# FORGE / PANEL tests — autodetected IP and FQDN

[Français](../../fr/13-tests-quality/portal-access-gates.md) · [QA](README.md) · [Access](../07-interfaces-roles/portal-access-routing.md)

**Status: PLANNED, not executed.** IP/domain discovery and Symfony routes are not operational. A static documentation check is neither real TLS testing nor hosting qualification.

## Existing static validation

The [candidate registry](../../../evidence/portal-access-registry-v1.json), [offline validator](../../../scripts/validate_portal_access_registry.py) and [documentation contract tests](../../../tests/documentation/test_portal_access_contract.py) detect, among other inconsistencies, a reintroduced custom-domain field or an automatic HTTPS 443 virtual host. They execute **none** of the following HTTP/VM scenarios.

## Integration and VM test matrix

Each test must name commit SHA, OS/VM, assigned IPs, OS hostname, DNS results, TLS certs, routing/NAT, port, method, actor, actual outcome, redacted logs and PASS/FAIL/SKIP. SKIP cannot imply PASS.

| ID | Scenario | Expected outcome |
|---|---|---|
| TEST-PORTAL-0001 | System-detected IP on HTTPS 8447 with `/forge` and valid IP certificate. | FORGE surface for authenticated administrators only. |
| TEST-PORTAL-0002 | System-detected IP on HTTPS 8446 with `/panel` and valid IP certificate. | Authorized PANEL surface, no admin privilege. |
| TEST-PORTAL-0003 | One existing verified FQDN for both direct ports. | `FQDN:8447/forge` and `FQDN:8446/panel`, no forced separate subdomains. |
| TEST-PORTAL-0004 | Unknown FQDN, spoofed Host, invalid SNI/certificate. | Safe rejection without leaking another surface. |
| TEST-PORTAL-0005 | PANEL customer invokes `/forge` via direct URL or API. | Denied in ingress and services/agent, no privileged job. |
| TEST-PORTAL-0006 | FORGE session on the same IP reused through the other port. | No cross-login; distinct cookies/server contexts, never by port alone. |
| TEST-PORTAL-0007 | Login, logout, CSRF, SameSite, session rotation for both portals. | Independently isolated and enforced. |
| TEST-PORTAL-0008 | Untrusted `Forwarded` and `X-Forwarded-*` values. | Cannot control redirects, origins or permission. |
| TEST-PORTAL-0009 | `//`, encoded paths, traversal, casing changes and aliases. | Safe canonicalization without authorization bypass. |
| TEST-PORTAL-0010 | Historic bootstrap `/setup` migrated to FORGE. | Never exposed via PANEL, one-use grant and setup restrictions. |
| TEST-PORTAL-0011 | FORGE/PANEL bundles and widgets. | No CSS/JS collision, RBAC independent of UI visibility. |
| TEST-PORTAL-0012 | Administrator changes listener, TLS or firewall. | Plan, verification, fallback access, audit/recovery; no custom-domain form. |
| TEST-PORTAL-0013 | Customer website hostname or listener collision. | No site/portal takeover. |
| TEST-PORTAL-0014 | Callbacks, email links, absolute URLs and login redirects. | Generated only from autodetected verified origins, never raw Host. |
| TEST-PORTAL-0015 | Standard Core without publisher Hub. | No Hub routes/secrets, Core remains autonomous. |
| TEST-PORTAL-0016 | Optional MFA enrolled/skipped and sensitive action. | Optional MFA, mandatory authorization/audit and policy-specific reauthentication. |
| TEST-PORTAL-0017 | IP URL without a valid IP-SAN certificate. | No claim that HTTPS link is trusted; diagnostics and secure fallback. |
| TEST-PORTAL-0018 | Root `/` request or unconfigured 443 gateway. | No implicit redirect or auto-provisioned 443 vhost. |
| TEST-PORTAL-0019 | No configured FQDN or valid DNS for host. | IP-only candidates, no domain link and no domain-entry field. |
| TEST-PORTAL-0020 | Multiple interfaces: private/public IP, loopback and NAT. | Provenance inventory, no assumed public IP; verified/unverified states. |
| TEST-PORTAL-0021 | IPv6-only or mixed IPv4/IPv6 configuration. | Use detected suitable IPs only; bracket IPv6 literals in URL. |
| TEST-PORTAL-0022 | FQDN resolves externally to A/AAAA without verified interface/routing/NAT match. | `UNVERIFIED`, no claim of accessible domain. |

## Exit gates

R1: genuine source; R2: running Symfony and PostgreSQL; R3: HTTPS gateway, TLS and network check; R4: tenant and customer journeys. These cases require real named environments, exact commits and security review. Python/documentation checks remain distinct.
