<!-- forgepanel-doc id=FP-08-PORTAL-ROUTING revision=1 status=specified -->
# Candidate contract — FORGE / PANEL surface resolution

[Français](../../fr/08-api-contracts/portal-route-boundary.md) · [API index](README.md) · [Access convention](../07-interfaces-roles/portal-access-routing.md)

**Status: SPECIFIED / NOT IMPLEMENTED.** This record extends `PORTAL-FP-0001..0012`; it creates no public API, Symfony route, HTTPS listener or operating security certification. Foundation v0.7 source import and real Symfony/PostgreSQL R2 integration remain prerequisites.

## Surface resolution before authentication

A trusted ingress resolves a portal from the **combination** of local listener, allowed HTTPS hostname, applicable certificate and canonical path prefix. Surface is a security context, not a role grant or browser-supplied bearer token. `forge.ip-server.com` and `panel.up-server.com` are configurable examples, not hardcoded production defaults.

| Origin and path (examples) | Target resolution | Condition |
|---|---|---|
| `https://<IP>:8447/forge` | FORGE | Valid IP TLS, admin listener, authorized admin actor |
| `https://<IP>:8446/panel` | PANEL | Valid IP TLS, customer listener, authorized actor |
| `https://<IP>:8447/panel` | DENY | Never fall back to PANEL on admin listener |
| `https://<IP>:8446/forge` | DENY | Never fall back to FORGE on customer listener |
| `https://<configured-forge-host>:443/forge` | FORGE | Exact host, SNI/certificate, trusted proxy, admin authorization |
| `https://<configured-panel-host>:443/panel` | PANEL | Exact host, SNI/certificate, trusted proxy, customer authorization |
| `https://<configured-forge-host>:443/panel` | DENY | No cross-portal route |
| `https://<configured-panel-host>:443/forge` | DENY | No cross-portal route |
| `https://<unknown-host>:443/forge` | DENY | Exact allowed-host policy; no permissive default virtual host |
| `http://<host>:80/forge` | DENY/safe redirect only after policy | Never send admin session or secret over unencrypted HTTP |
| Historic SRC-03 `/setup` | NOT MIGRATED | Separate bootstrap review before exposure |

**Note:** an absent valid IP-address certificate does not justify bypassing TLS verification. Qualify an alternative secure local recovery path before opening access. Optional `/` redirect to `/forge` or `/panel` remains **proposed, not yet approved**.

## Symfony boundary and responsibility

- **Routes**: separate logical `FORGE` and `PANEL` route spaces; never trust client-supplied surface identity. Encoded paths, duplicate separators, aliases or normalization must not bypass guards.
- **Sessions**: independent login contexts and cookie names, independent server session storage, `Secure`, `HttpOnly`, `SameSite`, CSRF and rotation. A cookie scoped to a shared IP can reach **both ports 8446 and 8447**; ports do not separate cookies. The prototype's temporary `__Host-FORGE_ADMIN` cookie is not a final permanent-session decision.
- **Authentication**: local identity plus optional SSO under Q58; administrator MFA remains **optional**. Q66/Q76 sensitive operations may require reauthentication and approval. A PANEL role never becomes FORGE authority by changing a URL.
- **Authorization**: Core enforces role + organization + resource ownership + delegation + state + policy, and API/services/Go agent recheck scope before Linux effects. No generic `shell.exec` or user-provided command execution.
- **Proxy headers**: enumerate trusted proxy sources exactly; ignore/reject untrusted `Forwarded` and `X-Forwarded-*`. Build callback and absolute URLs from configured origins, not raw `Host`.
- **UI**: independent FORGE/PANEL entry bundles, CSS roots and themes; shared components only under verified contracts. JavaScript and widgets do not grant privilege. Private Hub stays detached, with no public publisher routes in Core.

## Implementation prerequisites

1. **R1**: obtain and import the genuine Foundation v0.7 archive with hashes/provenance, without fabricating missing source.
2. **R2**: boot real Symfony/PostgreSQL with routes, firewalls, sessions, permanent identity and optional-MFA bootstrap.
3. **R3**: qualify installer and HTTPS gateway; plan and verify port, IP, hosts, DNS/TLS and firewall as `validate → apply → health → recover`, preserving fallback access.
4. **R4**: test isolation with hosted sites/listeners before exposing customer portal.
5. **R5/R6**: neutral extension ABI and only then private publisher Hub; FORGE/PANEL must not depend on it.

## Static registry and tests

The [candidate JSON registry](../../../evidence/portal-access-registry-v1.json) is a **non-executable** description of paths/ports/invariants, checked by an [offline validator](../../../scripts/validate_portal_access_registry.py) and [contract unit tests](../../../tests/documentation/test_portal_access_contract.py). They detect contradictory documentation, **not** working Symfony routing or live server vulnerabilities. The [18 HTTP/VM tests](../13-tests-quality/portal-access-gates.md) remain `PLANNED`.

Unresolved choices: actual hostnames, IP certificates, trusted proxy policy, final cookie names and `/` redirects — **no unapproved value is invented**.
