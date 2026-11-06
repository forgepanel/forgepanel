<!-- forgepanel-doc id=FP-13-PORTAL-ACCESS revision=2 status=specified -->
# Test matrix — FORGE / PANEL access

[Français](../../fr/13-tests-quality/portal-access-gates.md) · [QA](README.md) · [Portal contract](../07-interfaces-roles/portal-access-routing.md)

**Status: PLANNED.** No case below has been run. The current repository contains neither an integrated Symfony runtime, a qualified HTTPS gateway nor a working customer Panel. IDs describe measurable test targets, not `PASS` results.

## Static-only contract verification

The [candidate JSON registry](../../../evidence/portal-access-registry-v1.json), [offline validator](../../../scripts/validate_portal_access_registry.py) and [negative mutation/traceability tests](../../../tests/documentation/test_portal_access_contract.py) run in documentation CI. **They do not execute any TEST-PORTAL-0001..0018 scenario**, which remains `PLANNED` pending a real application, TLS gateway and qualified VM.

## Required environment and evidence

Every record must name Core version/commit SHA, qualified OS/VM, listener configuration, certificates, DNS origins, authentication profile, test command/navigation, observed result, redacted logs and correlation ID. Start with real HTTP/SQL/HTTPS integration, then a full VM; a unit test does not prove Internet-facing safety.

| ID | Scenario | Expected result |
|---|---|---|
| TEST-PORTAL-0001 | `https://<server-ip>:8447/forge` with valid IP TLS. | FORGE only for authorized administrator; otherwise login/denial without privileged content. |
| TEST-PORTAL-0002 | `https://<server-ip>:8446/panel` with valid IP TLS. | PANEL for authorized customer roles only, no FORGE privileges. |
| TEST-PORTAL-0003 | Distinct hosts on 443 with correct SNI and certificates. | FORGE host → `/forge`; PANEL host → `/panel`; no portal swap. |
| TEST-PORTAL-0004 | Unknown host, forged Host, missing SNI or wrong certificate. | Safe rejection; no other portal or tenant data exposed. |
| TEST-PORTAL-0005 | Authenticated customer calls `/forge` directly, via API or modified request. | Denied across layers; no privileged job or system effect. |
| TEST-PORTAL-0006 | FORGE session reused via same IP but PANEL port (and vice versa). | No cross-authentication although a browser shares cookies across ports on the same host. |
| TEST-PORTAL-0007 | Admin/User cookies and sessions, logout, rotation, CSRF, SameSite. | Distinct contexts; no session token reuse. |
| TEST-PORTAL-0008 | `Forwarded`, `X-Forwarded-Host/Proto/Prefix` spoofed by untrusted source. | Values ignored/denied; URLs and redirects cannot be attacker-controlled. |
| TEST-PORTAL-0009 | Encoded paths, `//`, `..\`, capitalization and route aliases. | Safe canonicalization and identical permissions on resolved routes; no bypass. |
| TEST-PORTAL-0010 | Existing `/setup` and future `/forge` bootstrap after import. | FORGE bootstrap only, one-use token, no setup exposed through PANEL. |
| TEST-PORTAL-0011 | FORGE and PANEL assets/menus/widgets on desktop/mobile. | Isolated bundles/styles; hidden menu does not enable unauthorized API. |
| TEST-PORTAL-0012 | Admin changes DNS, Panel host, TLS, port or firewall. | Impact plan, authorization, tests, fallback access, audit and recovery on failure. |
| TEST-PORTAL-0013 | Tenant-site host or ambiguous frontend route. | Site and portals cannot impersonate each other; no listener collision. |
| TEST-PORTAL-0014 | Callback URLs, email links, absolute URLs, login redirects. | Approved configured origin and prefix; no arbitrary `Host` or cross-portal token. |
| TEST-PORTAL-0015 | Standard Core installation without Hub/publisher plugin. | No private publisher routes or Hub secrets; hosting and administration work offline. |
| TEST-PORTAL-0016 | Optional MFA enrolled/skipped; sensitive reauthentication. | Both flows valid under Q66/Q76; authorization and audit still mandatory. |
| TEST-PORTAL-0017 | Missing DNS/certificate for IP path and fallback access. | Explicit report, never advise bypassing TLS; qualified secure local alternative. |
| TEST-PORTAL-0018 | Root path redirect on dedicated domain, if approved. | Redirect only to the same portal's prefix; never to foreign/adjacent host. |

## Acceptance

Bilingual documentation, API contracts, identity model, proxy configuration and Design System must follow this same access convention. Changing a critical host/port/path requires regression tests. A mockup, static check or green PR does not qualify an active route; only real tests on the named revision can earn `VERIFIED`.

Dependencies: [R2 identity](../03-core/bootstrap-identity-r2.md) · [R3 installer](../14-devops-releases/installer-lifecycle-r3.md) · [Security](../10-security/README.md).
