<!-- forgepanel-doc id=FP-07-PORTALS revision=1 status=specified -->
# FORGE / PANEL access contract — paths, domains and ports

[Français](../../fr/07-interfaces-roles/portal-access-routing.md) · [Portals and roles](README.md) · [Tests](../13-tests-quality/portal-access-gates.md)

> **SPECIFIED — not implemented or certified.** Product convention reiterated by the owner on 6 November 2026. The SRC-03 prototype does not provide two working portals. Hostnames below are configurable examples, not deployed domains.

## Confirmed access convention

| Surface | Direct HTTPS access by IP | Configured HTTPS host on 443 | Canonical path prefix | Audience |
|---|---|---|---|---|
| **FORGE** (server administration) | `https://<server-ip>:8447/forge` | `https://forge.ip-server.com/forge` | `/forge` | Super administrator / authorized server administrators |
| **PANEL** (customer hosting) | `https://<server-ip>:8446/panel` | `https://panel.up-server.com/panel` | `/panel` | Customers, website managers, resellers and scoped collaborators |

Example hosts are replaceable by administrators within an explicit allowed-host policy. `<server-ip>` is illustrative: IPv4/IPv6 reachability and a valid certificate covering the IP must be verified. Secure HTTPS access must never require disabling TLS verification. Both 443 virtual hosts require SNI/Host routing **and** explicit host allowlisting. Direct ports must remain separate from tenant website listeners.

**Proposed refinement, subject to qualification:** requests to `/` on the configured FORGE host may redirect to `/forge` and `/` on the configured PANEL host to `/panel`, only once installation and routing are validated. Do not create cross-portal redirects or claim `/` on a shared unrelated hostname.

## Routing and security requirements

| ID | Requirement | Expected verification |
|---|---|---|
| PORTAL-FP-0001 | `/forge` and port 8447 belong to the FORGE Admin surface. | Admin HTTPS route and service verified; no implicit Linux root privilege. |
| PORTAL-FP-0002 | `/panel` and port 8446 belong to the PANEL User surface. | User routes under server-side authorization; tenants isolated. |
| PORTAL-FP-0003 | Both HTTPS 443 virtual hosts are independently configurable and validated. | SNI, `Host`, reverse proxy and certificate checked; unauthorized hosts denied. |
| PORTAL-FP-0004 | Authorization is enforced across HTTP **and** API/services/Go agent. | Customer cannot reach admin operations through direct URL, API, alias, method or job. |
| PORTAL-FP-0005 | Admin/user sessions and cookies are distinct, host-side and server-side; MFA remains optional. | Host-only Secure/HttpOnly cookies, separate session contexts, rotation/CSRF and independent logout. |
| PORTAL-FP-0006 | IP:port separation does not isolate cookies. | Distinct cookie names and server checks: browsers share cookies across ports on the same host. |
| PORTAL-FP-0007 | Admin initial setup/recovery routes remain FORGE bootstrap-only. | Prototype `/setup` is explicitly migrated/wrapped after import and testing; never exposed in PANEL. |
| PORTAL-FP-0008 | `Forwarded`/`X-Forwarded-*` are trusted only from approved reverse proxies. | Deny Host spoofing, injected prefixes, forged scheme and open redirects. |
| PORTAL-FP-0009 | Twig/UX/Tailwind assets and styles are isolated by portal. | Separate bundles/CSS roots, shared components only by contract, no theme or privilege bleed. |
| PORTAL-FP-0010 | Changes to host, port, TLS or firewall are sensitive Q47 operations. | Preflight, impact preview, fallback admin access, validation, audit and recovery on failure. |
| PORTAL-FP-0011 | The publisher Hub remains a separate optional private extension/service. | No publisher route or Hub secrets in the standard Core. |
| PORTAL-FP-0012 | Links, emails and callback URLs use their surface's approved origin and prefix. | Never build absolute URLs from unchecked Host; no cross-portal token leakage. |

## Proposed implementation boundaries

- **Symfony**: distinct `/forge/**` and `/panel/**` route spaces, firewalls, sessions, RBAC and independent authorization services. The Core enforces each operation; menus are not a security boundary.
- **HTTPS gateway**: dedicated 8447/8446 listeners; configurable FORGE/PANEL hosts on 443 once DNS/TLS are ready. Reject unauthorized host/port/prefix combinations even through a reverse proxy. Keep the control plane reachable independently of customer WebStack configurations.
- **Frontend**: versioned independent FORGE/PANEL bundles, e.g. `forge-admin` and `forge-user` (candidate names, not shipped assets). Controlled shared branding, distinct CSS roots, independently customizable header/sidebar and RBAC-bound widgets.
- **Installer**: wizard presents host choices and verifies IP:port conflicts, firewall, certificates, SNI and fallback access; it must not silently take over third-party listeners. Idempotent recovery on failure.
- **Prototype migration**: SRC-03's existing `/setup` routes and `__Host-FORGE_ADMIN` bootstrap cookie need explicit compatibility review. Do not imply those routes already work under `/forge`. Permanent cookie names and alias/redirect policy still need qualification.

## Exit gates and evidence

The [QA scenarios](../13-tests-quality/portal-access-gates.md) must run against real Symfony + PostgreSQL and a VM with HTTPS. Static/documentation tests are not evidence of session isolation or active listeners. **R1/R2/R3/R4 remain gated by existing requirements; this record does not add running routes.**

Related: [Design system](../11-design-system/README.md) · [Installer](../14-devops-releases/README.md) · [API contracts](../08-api-contracts/README.md) · [Security](../10-security/README.md).
