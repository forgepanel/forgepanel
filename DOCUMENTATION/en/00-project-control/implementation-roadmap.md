<!-- forgepanel-doc id=FP-00-EXECUTION revision=4 status=specified -->
# Technical implementation roadmap — Q120 D and Q119 B MVP

[Français](../../fr/00-project-control/implementation-roadmap.md) · [Project status](status.md) · [Q111–Q120 decisions](decisions-q111-q120.md)

## Owner-approved dependency order

**Import source → verify Symfony/PostgreSQL → implement and test installer → deliver first PHP site/VPS → prove generic extension API → build/integrate private ForgePanel-Hub.**

This order **rules out commercial Hub or marketplace being a prerequisite for a usable Core**, without replacing Q1–Q110. Preparatory tasks may overlap, but a phase is not accepted without named evidence for its dependencies. **No application implementation is claimed by this roadmap.**

| Gate | Work | Verifiable exit criteria |
|---|---|---|
| **R1 — Source import** | Import verified Foundation v0.7 archive and review the separate optional-MFA v0.7.1 patch, provenance, file inventory, hashes and pending license | Scoped `features/* → develop` PR, no committed generated binaries/secrets, rerun Go/PHP checks and native `make check`; still refuse unsafe `install apply`. Preserve FR/EN docs and single changelog. [Issue #2](https://github.com/yyogas/forgepanel/issues/2), [MFA #6](https://github.com/yyogas/forgepanel/issues/6). |
| **R2 — Symfony/PostgreSQL** | Lock Composer dependencies, boot real Symfony app and dedicated PDO/PG, initial setup/permanent identity, optional MFA choice, HTTP security | Real HTTP/browser, HTTPS/CSRF/session/origin/permission tests; optional-MFA enable/skip/resume and PostgreSQL rollback, concurrency, restart and lost-response testing on named revision. [Issue #3](https://github.com/yyogas/forgepanel/issues/3). |
| **R3 — Verified installer** | Signed Go builds, verified bootstrap, preflight, idempotent systemd/service changes, logs/recovery. **Compare VM evidence and dependencies before selecting the first OS (Q121 D).** | Real install/upgrade/failure/recovery comparison with OS/commit evidence; **no chosen OS** and no six-OS certification without separate testing. [Qualification](mvp-qualification.md) · [issue #15](https://github.com/yyogas/forgepanel/issues/15). |
| **R4 — First PHP site and basic VPS** | **Select first WebStack from actual compatibility/security tests (Q122 D)**; isolated PHP site with **externally managed DNS**, ACME **HTTP-01** and auto HTTPS (Q123 A); permanent identity and **admin + website-manager PHP/domain/TLS/files/SFTP and backup/restore limited by RBAC** (Q124 B/Q136 C); VPS resources/services/logs plus **controlled OS package updates** (Q125 B); **real panel-config + PHP-site-files backup and restore** (Q126 B). | Clean VM: installer/setup/login → PHP website/domain/external DNS → port-80 HTTP challenge → real HTTPS → own-site SFTP allowed and cross-tenant SFTP denied → role denial → audited planned package update → successful backup/restore. Recover panel PG state consistently where needed for admin/site functionality. No preselected stack or CA. [Qualification](mvp-qualification.md) · [site #20](https://github.com/yyogas/forgepanel/issues/20) · [MVP #29](https://github.com/yyogas/forgepanel/issues/29). |
| **R5 — Generic detached-extension API** | Versioned neutral service ABI, scopes, signature checks, verify/stage/activate/disable/remove; use **non-Hub test extension** | Test extension works on standard Core, rejected when unsigned/incompatible; Core and hosted sites still function after removal or crash. [Issue #7](https://github.com/yyogas/forgepanel/issues/7). |
| **R6 — Hub after R5** | Isolated Symfony/PG Hub, organizations/offers, sandbox payments, license pools, catalog/verified partners, signed distributions | Real Core-Hub integration tests for offline Core, idempotent signed callbacks, license transfer/revocation reasons, privacy; Core login/recovery never requires Hub. [Hub repository](https://github.com/yyogas/forgepanel-hub). |

**R4 defines the Q119 B first usable MVP**. R5/R6 follow this first milestone. Q54 continues to favor shared hosting and VPS administration. Multi-server HA, full mail, native authoritative DNS, every WebStack and all six target OSes are **not** automatically required for first acceptance. Select the first OS/WebStack/domain through test evidence, not an implicit default.

## Q121–Q130 additions: MVP evidence, beta and security roles

**Q121 D / Q122 D:** choose initial OS/WebStack **from comparative VM evidence**, not an invented owner default. **Q123 A:** initial site uses **external DNS** and ACME **HTTP-01**, not native authoritative DNS or a DNS-01 driver as an MVP prerequisite. **Q124 B / Q125 B / Q126 B:** local admin/site manager, observed VPS with safe package updates, restored panel configuration and PHP website files. See [qualification matrix](mvp-qualification.md).

**Q127 B:** isolated internal tests then an **authorized private beta** only after owner's release approval, working confidential security channel and review of distribution/license duties **for external beta recipients too**. Private beta is not public/stable and is no legal exemption. Q128 D self-service license transfers plus manual recovery of a lost server and Q129 C partner contractual maintenance/alerts/withdrawal remain **Hub-after-ABI**. **Q130 C** requires an **actually appointed** security lead and deputy with triage/coordination; never invent identities or a mailbox.

## Q131–Q140 — evidence gates and sequencing

- **R3, Q131 D**: compare **local/CI full VMs**, snapshots, simulated failures and OS/version reports with `PASS/FAIL/SKIP`; **no preselected OS**. **Q132 D** adds WebStack load, maintenance and recovery tests with **hard security rejection criteria** independent of performance.
- **R4, Q133 C**: diagnostics for **A/AAAA**, **port 80**, HTTP-01 challenge routing and **HTTPS** readiness with external DNS (Q123). **Q134 C**: impact-planned OS updates with backup, health and recovery. **Q135 B**: **encrypted local** backup, **optional remote**, and actual panel-config/PHP-file restore. **Q136 C**: website-manager permissions for PHP/domains/TLS/files/**SFTP/backup/restore** under scoped policies and quotas, no OS privilege.
- **After R4, Q137 D**: invitations/accepted beta terms, **staged waves**, private issue/version channel, **pause and recovery**; never open private beta before VM evidence, legal review for recipients and security triage.
- **After R5/Hub, Q138 D**: premium transfers with cryptographic proof, fraud controls and **configurable independent approval** for high-risk lost-host recovery. **Q139 C**: partner severity, alerts, escalation and withdrawal under Q129 contracts. **Q140 C**: Q130 lead/deputy coordinate fixes/security notices and customer communications; verify Q118 reporting.

Q131–Q140 do not preselect OS/stack, authorize beta launch or permit data deletion on beta access suspension. [Updated MVP matrix](mvp-qualification.md) · [Decisions](decisions-q131-q140.md). **Implementation and real testing remain pending.**

## Cross-cutting release gates

Named OS/version, commit, toolchain and test results, permanent identities/sessions, real HTTP/PG/VM and recovery are required to assert the installer/site works. Documentation CI and standalone domain checks are **not** sufficient.

Before **public distribution**, complete legal review of AGPL/commercial variant and contributor CLA (Q111/Q112), inventory third-party rights and trademark terms, and **configure/test** private GitHub vulnerability reporting plus a dedicated verified security email with triage (Q118). No invented address or prematurely published license.

For every change: scoped `features/*` PR into `develop`, explicit acceptance and negative tests, bilingual docs and changelog, evidence review when available; only later authorized promotion to `stable`, `main`, `production`. A docs merge is never a product release.

## Current evidence

Core source remains **unimported** from the separate v0.7 archive; optional-MFA v0.7.1 is also separate. Symfony/PG integration, live installer and hosting tests are not demonstrated by current repository documentation CI. This plan contains **no release date or actual deployment**.
