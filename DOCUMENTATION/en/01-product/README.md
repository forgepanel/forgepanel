<!-- forgepanel-doc id=FP-01 revision=1 status=documented -->
# Product scope and journeys

[Français](../../fr/01-product/README.md) · [Index](../README.md)

## Users and boundaries

ForgePanel targets server owners, hosting operators, agencies, resellers and hosting customers. These personas are product targets; only initial administrator enrollment is prototyped in SRC-03. The product owner communicates in natural language and is not responsible for technical implementation or review.

## Required journeys

| ID | Journey | Acceptance criterion |
|---|---|---|
| REQ-001 | Install from one command | On a supported clean VM, verify origin/signatures, preflight, install isolated panel services, report verified HTTPS access; interruption and rerun must not corrupt state |
| REQ-002 | Claim the installation | Local privileged proof issues a short-lived one-use token; create an independent panel account, require MFA, close initial registration |
| REQ-003 | Configure through a resumable wizard | Explain service dependencies and system changes; save progress; validate the plan before applying it; no ambiguous success after partial failure |
| REQ-004 | Host a site without marketplace plugins | Native account, domain, PHP runtime, TLS, database/files and backup capabilities work under explicit resource permissions |
| REQ-005 | Diagnose and recover locally | Read-only diagnosis works without the web UI; repairs are previewed, bounded, audited and preserve unrelated data |
| REQ-006 | Offer multiple OS/web profiles | Publish support only for individually tested combinations; unavailable profiles are not selectable as working capabilities |

The archive reaches a reviewed configuration draft, not installation completion. DNS, certificates, mail, file management, reseller operations and service provisioning remain outside its implementation.

## Scope discipline

Core foundations are mandatory; native service modules may be selected without depending on third-party plugins. Plugins extend capabilities rather than provide basic authorization or safety. Recipes install customer applications; they are neither core modules nor privileged extensions.

No pricing, trial period, license server, marketplace business model or WCP360 commercial rule is adopted by this baseline. Such choices require separate product decisions. Success is verified operation and recovery, not a large number of dashboard screens.

[Module catalog](../04-modules/README.md) · [Priorities](../00-project-control/status.md)
