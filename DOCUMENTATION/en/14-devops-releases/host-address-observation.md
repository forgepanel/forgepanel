<!-- forgepanel-doc id=FP-14-HOST-OBSERVE revision=1 status=specified -->
# Standalone read-only machine address observation — preparatory R3 tool

[Français](../../fr/14-devops-releases/host-address-observation.md) · [DevOps](README.md) · [Portal contract PR #50](https://github.com/yyogas/forgepanel/pull/50)

## Provenance and state

The Go utility in [tools/host-address-observation](../../../tools/host-address-observation/README.md) is a standalone **IMPLEMENTED PROTOTYPE**, not an import of historical Foundation v0.7 source or a live Core subsystem. It runs without root privileges, network calls, DNS resolution, shell, socket listening, file writes, or changes to the host. **R1 Foundation source import and R2 Symfony/PostgreSQL integration remain blocked/open independently.**

Owner-confirmed FORGE (/forge, HTTPS 8447) and PANEL (/panel, HTTPS 8446) paths and ports are reported as **static metadata**, not installed listeners. The operating system supplies IPv4/IPv6 addresses and an optional syntactically valid FQDN candidate; no customizable portal-domain setting, generated forge./panel. subdomain or automatically installed 443 host is introduced. Tenant website domains and Q5 branding remain separate features.

## What the report means

- OS interface facts: usable assigned unicast addresses from up/non-loopback interfaces, sorted and deduplicated, with scope labels PRIVATE_UNVERIFIED or NON_PRIVATE_UNVERIFIED. The latter is **not proof of a public/routable IP**, especially with CGNAT and reserved ranges.
- Hostname fact: a syntactically valid full OS hostname yields CANDIDATE_UNVERIFIED; a local/non-FQDN hostname yields NONE. No forward DNS proof is attempted, since /etc/hosts, local resolvers or split-horizon records can be misleading.
- Verification: DNS, TLS, listener and public-reachability fields are always NOT_EXECUTED, verified_access_urls is always empty. An IP HTTPS URL needs a certificate covering that IP; a FQDN URL requires actual verified DNS, routing and TLS before the UI may advertise it as working.
- Errors: unavailable data or bounded enumeration is surfaced through UNAVAILABLE or PARTIAL_UNVERIFIED and sanitized warning codes; no false success or fallback to guessed addresses.

## Acceptance and integration boundary

The dedicated CI runs Go unit tests on synthetic interfaces, race detector, vet and a no-working-URL output check. These checks establish only properties of the **standalone source**. Integration under [runtime issue #51](https://github.com/yyogas/forgepanel/issues/51) still requires actual Foundation import, authenticated Symfony routes, tested Go agent boundary, trusted DNS/HTTPS probes, NAT-aware routing and VM/HTTP qualification. No privileged shell executor or publisher Hub dependency is added.

**Status:** code for an unprivileged observer may be tested; integration, DNS verification, TLS certification, public address detection and published access URLs remain NOT IMPLEMENTED.
