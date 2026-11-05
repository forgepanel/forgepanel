<!-- forgepanel-doc id=FP-00-EXECUTION revision=1 status=specified -->
# Technical implementation roadmap — Q120 D and Q119 B MVP

[Français](../../fr/00-project-control/implementation-roadmap.md) · [Project status](status.md) · [Q111–Q120 decisions](decisions-q111-q120.md)

## Owner-approved dependency order

**Import source → verify Symfony/PostgreSQL → implement and test installer → deliver first PHP site/VPS → prove generic extension API → build/integrate private ForgePanel-Hub.**

This order **rules out commercial Hub or marketplace being a prerequisite for a usable Core**, without replacing Q1–Q110. Preparatory tasks may overlap, but a phase is not accepted without named evidence for its dependencies. **No application implementation is claimed by this roadmap.**

| Gate | Work | Verifiable exit criteria |
|---|---|---|
| **R1 — Source import** | Import verified Foundation v0.7 archive and review the separate optional-MFA v0.7.1 patch, provenance, file inventory, hashes and pending license | Scoped `features/* → develop` PR, no committed generated binaries/secrets, rerun Go/PHP checks and native `make check`; still refuse unsafe `install apply`. Preserve FR/EN docs and single changelog. [Issue #2](https://github.com/yyogas/forgepanel/issues/2), [MFA #6](https://github.com/yyogas/forgepanel/issues/6). |
| **R2 — Symfony/PostgreSQL** | Lock Composer dependencies, boot real Symfony app and dedicated PDO/PG, initial setup/permanent identity, optional MFA choice, HTTP security | Real HTTP/browser, HTTPS/CSRF/session/origin/permission tests; optional-MFA enable/skip/resume and PostgreSQL rollback, concurrency, restart and lost-response testing on named revision. [Issue #3](https://github.com/yyogas/forgepanel/issues/3). |
| **R3 — Verified installer** | Go build, trusted signed artifacts, one-command install, preflight, idempotent apply, systemd identities/TLS, durable logging and recovery | Install/reinstall/upgrade and simulated failures on **at least one explicitly qualified OS**, followed by each claimed OS via disposable VM matrix. No six-OS certification assumed. [Issue #15](https://github.com/yyogas/forgepanel/issues/15). |
| **R4 — First PHP site and basic VPS** | Minimal agent, local identity/RBAC, safe config, one actually qualified WebStack, domain routing, isolated PHP-FPM and valid HTTPS cert, basic VPS diagnostics | From clean VM: install → wizard → admin login → **create/manage PHP site + domain + HTTPS** → successful HTTPS request → deny unauthorized actions → verify config backup/recovery. Real OS/HTTP/TLS/PHP/permission tests. [Site #20](https://github.com/yyogas/forgepanel/issues/20), [hosting #22](https://github.com/yyogas/forgepanel/issues/22). |
| **R5 — Generic detached-extension API** | Versioned neutral service ABI, scopes, signature checks, verify/stage/activate/disable/remove; use **non-Hub test extension** | Test extension works on standard Core, rejected when unsigned/incompatible; Core and hosted sites still function after removal or crash. [Issue #7](https://github.com/yyogas/forgepanel/issues/7). |
| **R6 — Hub after R5** | Isolated Symfony/PG Hub, organizations/offers, sandbox payments, license pools, catalog/verified partners, signed distributions | Real Core-Hub integration tests for offline Core, idempotent signed callbacks, license transfer/revocation reasons, privacy; Core login/recovery never requires Hub. [Hub repository](https://github.com/yyogas/forgepanel-hub). |

**R4 defines the Q119 B first usable MVP**. R5/R6 follow this first milestone. Q54 continues to favor shared hosting and VPS administration. Multi-server HA, full mail, native authoritative DNS, every WebStack and all six target OSes are **not** automatically required for first acceptance. Select the first OS/WebStack/domain through test evidence, not an implicit default.

## Cross-cutting release gates

Named OS/version, commit, toolchain and test results, permanent identities/sessions, real HTTP/PG/VM and recovery are required to assert the installer/site works. Documentation CI and standalone domain checks are **not** sufficient.

Before **public distribution**, complete legal review of AGPL/commercial variant and contributor CLA (Q111/Q112), inventory third-party rights and trademark terms, and **configure/test** private GitHub vulnerability reporting plus a dedicated verified security email with triage (Q118). No invented address or prematurely published license.

For every change: scoped `features/*` PR into `develop`, explicit acceptance and negative tests, bilingual docs and changelog, evidence review when available; only later authorized promotion to `stable`, `main`, `production`. A docs merge is never a product release.

## Current evidence

Core source remains **unimported** from the separate v0.7 archive; optional-MFA v0.7.1 is also separate. Symfony/PG integration, live installer and hosting tests are not demonstrated by current repository documentation CI. This plan contains **no release date or actual deployment**.
