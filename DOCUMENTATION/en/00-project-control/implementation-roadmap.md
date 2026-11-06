<!-- forgepanel-doc id=FP-00-EXECUTION revision=15 status=specified -->
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

## Q141–Q150 — evidence and responsibility refinements

- **R3, Q141 D:** **local/cloud full VM** adapters, qualified CI runners, snapshots/fault injection and shared OS/stack/commit reports; fixtures and `SKIP` never establish certification. **Q142 D:** application-class configurable performance budgets and cross-version regressions, with Q132 security disqualifiers ahead of speed.
- **R4, Q143 C:** suggest **external DNS records** and recheck A/AAAA/80/HTTP-01/443/TLS **without automatic DNS edits**. **Q144 D:** **per-server** planned/backup/health/recovery OS update policy; later multi-server orchestration. **Q145 D:** encrypted local backups with usable off-host recovery keys, vault/protected copy, **optional** external KMS and multi-authority custodians. **Q146 C:** real shell-disabled SFTP with expiry/revocation, quotas, audit and cross-tenant/path-traversal denials.
- **After R4, Q147 C:** private beta Q137 cohorts with **configurable health/stop gates**, pause new waves on critical issues, notification and recovery; never mandatory Core telemetry or destructive access suspension.
- **Hub R6 after R5, Q148 C:** installation identity keys, signed fresh challenge, key rotation/anti-replay, organization binding and manual lost-host route, preserving **risk-based extra approval Q138**. **Q149 C:** partner severity/contract deadlines, alert/escalation/withdrawal. **Q150 D:** signed historical advisories, configurable notices, partner-coordinated **risk-based disclosure windows**, no invented SLA/timing.

**First OS/WebStack awaits Q121/Q122 evidence; none of these services is operational.** [Q141–Q150 decisions](decisions-q141-q150.md) · [MVP matrix](mvp-qualification.md).

## Q151–Q160 — driver order and verifiable gates

**R3 (qualification):** start with **local QEMU/KVM (Q151 A)** and keep common cloud driver ABI for later. Every qualification needs an **internal matrix**, **signed historical** report with provenance, snapshots and scenario **PASS/FAIL/SKIP (Q152 C)**. App-type performance budgets block by severity; **approved audited** exceptions may waive certain performance regressions but **never Q132 security/recovery disqualifiers** (Q153 C).

**R4 (initial site):** external DNS **only published A/AAAA families**, each advertised route compatible with HTTP-01/HTTPS (Q154 C), Q143 advisor proposes then **rechecks without DNS edits**. **Per-server** approved OS update/reboot after impact/backup/health/recovery (Q155 C). Encrypted local backup is **not recoverable by claim** until its protected recovery-key accessibility is checked periodically and a **real isolated restoration** succeeds (Q156 C); optional Q145 KMS/multiple custodians. SFTP **without shell**, site-policy-scoped **public-key management**, expiry/revocation, quotas/audit and sensitive action validation (Q157 C).

**After R4 (private beta):** **local health**, manual reports and minimized **separately opted-in** diagnostics per cohort (Q158 C). Q147 halt/recovery rules work without mandatory telemetry. **Hub R6 after neutral R5 ABI:** Q159 C fraud flags from lost/repeated transfer, inconsistent organization or compromise retain Q138 risk-based second approval; Q160 C includes signed **human FR/EN plus machine-structured** advisories with configurable notice and Q150 coordinated disclosure.

Q120 D stays **source → Symfony/PG → installer → initial site/VPS → neutral ABI → Hub**, with no date or implementation implied. [Q151–Q160 decisions](decisions-q151-q160.md).

## Cross-cutting release gates

Named OS/version, commit, toolchain and test results, permanent identities/sessions, real HTTP/PG/VM and recovery are required to assert the installer/site works. Documentation CI and standalone domain checks are **not** sufficient.

Before **public distribution**, complete legal review of AGPL/commercial variant and contributor CLA (Q111/Q112), inventory third-party rights and trademark terms, and **configure/test** private GitHub vulnerability reporting plus a dedicated verified security email with triage (Q118). No invented address or prematurely published license.

For every change: scoped `features/*` PR into `develop`, explicit acceptance and negative tests, bilingual docs and changelog, evidence review when available; only later authorized promotion to `stable`, `main`, `production`. A docs merge is never a product release.

## Current evidence

Core source remains **unimported** from the separate v0.7 archive; optional-MFA v0.7.1 is also separate. Symfony/PG integration, live installer and hosting tests are not demonstrated by current repository documentation CI. This plan contains **no release date or actual deployment**.

## Additional Q151–Q160 exit-test evidence

[Per-gate R3/R4/R5/R6 MVP matrix](../13-tests-quality/mvp-gates-q151-q160.md) requires both positive **and negative** cases. KVM/signed internal report/performance-only Q153 gates at R3; published-IP DNS, per-server reboot, **accessible keys and actual isolated restoration**, site-scoped public-key SFTP at R4; consented cohort beta afterwards; Hub fraud review and signed human+machine advisory after R5 neutral ABI. **PLANNED: document checks do not execute VM or backups.**

## Q161–Q170 roadmap additions — real exit evidence

**R3**: ephemeral local KVM runner with pinned images/quotas/cleanup (Q161 C); private immutable **internal signed** evidence (Q162 B); **performance-only** severity-based, independently approved, expiring audited waivers without weakening Q132 vetoes (Q163 C). **R4**: DNS/HTTP-01 checked locally **and** via one independent external probe for each advertised A/AAAA (Q164 B); bounded nondestructive OS recovery with human risk approvals (Q165 C); isolated restore of each backup before recoverable status plus periodic deep checks/host-key disaster drills (Q166 C); scoped **public** SFTP keys with allowed algorithm/rotation/approvals (Q167 C). **Post-R4 beta**: separate consents and reidentification-safe cohorts (Q168 C). **Hub R6 after R5 ABI**: versioned premium fraud policy (Q169 C), signed JSON Schema synchronized FR/EN advisories (Q170 B). [Test matrix](../13-tests-quality/mvp-gates-q161-q170.md). No real VM/recovery execution is claimed.

## R1 gate — verified private staging without source import

R1 tooling now includes `verify_source_archive.py` (read-only preflight) and `stage_source_archive.py` (**preview by default**, then explicit non-root copy to a fresh private directory with per-file digest validation). This executes no historical PHP/Go, adds no Core application files to Git and validates neither licensing nor installation. It precedes independent source review and import PR. Genuine SRC-03 remains unavailable: **R1 source import blocked, R2–R6 unchanged**. [Quarantine contract](../12-development/source-staging.md).

## Additional R1 entry gate: independently audit staged files

Issue #2 (genuine Foundation source import) now explicitly requires: original SRC-03 archive → [preflight](../12-development/source-archive-intake.md) → [private staging](../12-development/source-staging.md) → [ZIP/receipt/disk comparison](../12-development/source-staging-audit.md) → license/security review → separate import PR with **byte re-hashing during import** → real PHP/Go tests. Preflight/audit tools are **not** the hosting Core implementation, and the actual ZIP remains unavailable here.

## Parallel R3 preparation — KVM observation is not a VM runner

Without changing the approved **R1 → R2 → R3 → R4 → R5 → R6** order, standalone [`tools/kvm-host-probe`](../14-devops-releases/kvm-host-probe.md) prepares **only a nonprivileged local host observation** (Q151 A/Q161 C). It is not the QEMU/KVM runner, selects no OS, produces no pinned images/quotas/snapshots or signed evidence, and cannot replace real installer/recovery test results. Its unit tests are independent of the still-blocked R1 original Foundation source import.

## Parallel R3 preparation — image admission is not VM execution

After the host probe, [QCOW2 admission](../14-devops-releases/kvm-image-admission.md) checks a manifest, image bytes and **explicitly supplied** ceilings without defaults, privileged system actions or QEMU execution. Remaining steps: signed image provenance/authorization → immutable launch-time pinned bytes → ephemeral isolated KVM runner with real quotas → snapshots/failure/recovery → signed Q152 reports and private immutable Q162 storage → R3 qualification with Q132 vetoes. **R1 → R2 → R3 → R4 → R5 → R6 unchanged**; original Foundation sources still missing.

## R3 preparation — provisional pinned image bytes

[Verified private copying](../14-devops-releases/kvm-image-staging.md) complements R3 observation/admission without changing **R1 → R2 → R3 → R4 → R5 → R6**. It creates `image.qcow2` plus an unsigned provenance receipt in a private lab directory; a future runner must **revalidate exact bytes at launch**, prove isolation, enforce real quotas and clean up guest resources before any Q152/Q162 evidence. R1 Foundation v0.7 remains blocked by the missing historical ZIP.

## R3 documentation lot — IPC and installer prerequisites before implementation

[Typed R3 IPC](../08-api-contracts/symfony-go-ipc-r3.md), [installer recovery lifecycle](../14-devops-releases/installer-lifecycle-r3.md) and [planned QA](../13-tests-quality/r3-ipc-installer-gates.md) clarify approval dependencies without skipping R1 → R2. After genuine SRC-03 import and tested Symfony/PostgreSQL: ratify typed IPC/permissions, durable job model/migrations, daemon and Linux trust boundaries, artifact provenance/signatures; only then implement an installer and run disposable OS VMs. Transport, limits, providers and pilot OS remain open. **`DOC-GAP-005` and `DOC-GAP-006` remain OPEN**.

## R2/R3 documentary sequencing: durable state and peer identity

Before any Linux effect, Database must ratify [job/idempotency/fencing](../09-database/durable-jobs-r3.md) and Security/API must ratify [peer trust protocol](../08-api-contracts/local-peer-trust-r3.md). Imported R1 source and actual R2 Symfony/PG remain hard prerequisites for operational R3. Implement jobs/bridge **without generic privileged shell commands**, then separately test scope authorization, lost ACK, stale workers, failover and SQL/Linux outcomes in authorized VMs. [24 cases planned](../13-tests-quality/r3-jobs-peer-gates.md), none executed.
