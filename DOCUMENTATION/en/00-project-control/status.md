<!-- forgepanel-doc id=FP-00-STATUS revision=24 status=documented -->
# Status and dependency-ordered roadmap

[Français](../../fr/00-project-control/status.md) · [Project control](README.md)

## Evidence levels

`PROPOSED`: option requiring assessment. `SPECIFIED`: requirements/contracts written. `IMPLEMENTED`: source exists, with its location named. `VERIFIED`: a named check ran against a named input/environment. `PUBLISHED`: identifiable release and artifacts. `DEPLOYED`: identified environment and deployed revision. `MERGED` describes Git integration only. Documentation status is separate from feature status.

## Baseline on 2026-11-05

| Scope | Real state |
|---|---|
| GitHub before this task | Private, empty; no branches, commits, issues, PRs or releases returned |
| Repository after this documentation change | Documentation, governance and documentation validation tooling; no application import |
| Foundation v0.6/v0.7 | Supplied development archives; provenance recorded in the audit |
| v0.7 native tests | Re-executed successfully in the local container; not VM certification |
| Symfony HTTP and PostgreSQL integration | Sources/test supplied; not executed in this audit |
| Installer, full agent, WebStacks, full RBAC, plugins | Not available as a working product |
| Release and production | None evidenced; license unresolved |

All six OS targets and five profiles are planning inputs. Thirty fixture combinations are not thirty installations. The `production` branch initially points to a README-only bootstrap commit and deploys nothing.

## Roadmap — Q120 D order, Q119 B MVP

**Approved dependency chain: source import → real Symfony/PostgreSQL and optional MFA/identity tests → safe installer → first PHP site/domain/HTTPS and basic VPS administration → neutral extension ABI → private Hub.** The [detailed roadmap](implementation-roadmap.md) defines R1–R6 and evidence gates. **Q119 B first functional version ends with a verified HTTPS PHP site**: native DNS, mail, HA, marketplace and all six OSes are not day-one certified prerequisites. Core source is still unimported; no stage is declared delivered.

## Roadmap

| Priority | Deliverable | Dependency and exit evidence |
|---|---|---|
| P0 | Documentation baseline and reviewed PR | Link/parity checks; facts and risks recorded |
| P1 | Provenance-preserving source import | Reviewed v0.7 inventory; no secrets/generated binaries; license status explicit; tests repeated on imported commit |
| P2 | Symfony + PostgreSQL integration | Dependency resolution/lock/audit; real HTTP, transaction rollback/concurrency and browser tests |
| P3 | Permanent identity and recovery | Login/logout, optional MFA (enroll/disable/recovery), scoped authorization, session isolation tests; fix v0.7 setup gate |
| P4 | Six-OS packaging and service foundation | Trusted package sources, runtime policy, systemd and mandatory access controls verified in VMs |
| P5 | Plan execution and one-command installation | Durable steps, safe retries, TLS, rollback/compensation, signed distribution and reinstall/update tests |
| P6 | Hosting modules and additional stacks | Proven isolation, resource controls, backups/restores and per-profile VM evidence |
| P7 | Third-party ecosystem | Trust model, contracts, isolation and maintenance policy accepted before execution |

Additional 2026-11-05 choices Q48–Q55: **AGPL-3.0 + commercial license**, contributor **CLA**, premium plugins/cloud/managed/partners/support, **Docker and Podman**, after 60 offline days deny new premium operations while preserving existing data, **manually reviewed partner applications**, hosting + VPS first, **one brand per organization**. [Licensing](license-commerce.md) · [Container drivers](../02-architecture/container-drivers.md). None is an implemented feature.

New owner product decisions Q1–Q8 and Q47 on 2026-11-05: **dual licensing (exact texts open)**, full free Core with optional premium/support, all audiences phased, customer PHP/Node.js/Python/containers, organization white-label, separately consented Hub exchange, **60-day** commercial offline grace, official/verified partners, safe sensitive changes. [Full policy](product-policy.md). These are not implemented features.

Confirmed Q56–Q60: **independent payment provider adapters**, **Stable/Beta/Dev with staged rollout/recovery**, **local accounts plus optional SSO/OIDC**, **category-based retention**, **perpetual/subscription purchases with trials/coupons/bundles/add-ons**. These remain **specified, not implemented**. Q61–Q70 are decided, not implemented. See [Q56–Q60](commerce-identity-release-policy.md).

Q61–Q70 are **confirmed (2026-11-05)**: signed CI/CD with anti-rollback and approvals; universal installer plus signed DEB/RPM; local/external DNS and mail; encrypted, replicated and immutable backups with recovery; sensitive reauthentication/approval; multi-server/HA; monitoring integrations; per-site/IP/port WebStacks; visual widgets/navigation within one brand. [Q61–Q70 specification](infrastructure-decisions.md). **Specified only; no certified runtime or cluster.**

The owner has confirmed **Q71–Q80**: protected key rotation, controlled service adoption, DNS chosen after tests, Postfix/Dovecot with relays, 3-2-1 and restore drills, per-action approvals, phased HA/orchestration, Prometheus/OpenTelemetry, **per-site WebStack recommendations with later switching**, and declarative widgets. [Product reference](decisions-q71-q80.md) · [Per-site WebStack](../02-architecture/site-webstack-advisor.md). These are specifications, not a new release or certification.

**Q81–Q90 confirmed (2026-11-05)**: per-site application/security/resource-aware WebStack recommendations and temporary/progressive transitions when feasible; per-site PHP/FPM/extensions; ACME/wildcard/DNS-01; Git Deploy with staging; MariaDB/MySQL/PostgreSQL with optional Redis/Valkey; file manager/SFTP with restricted SSH; webmail/antispam/quarantine; inherited quotas; selective restore and staging clones. [Q81–Q90 specification](decisions-q81-q90.md). **Specified, not shipped**.

**Q91–Q100** are confirmed: maintained PHP and planned migrations, confined per-site PHP-FPM, validated manual/webhook Git Deploy, site-scoped staging privacy/retention, multiple ACME and DNS-01, multiple tenant DB/cache engines, plan-scoped restricted SSH, configurable Webmail, quotas with bounded grace and authorized increments, secure cross-server migration/restore. [Q91–Q100 register](decisions-q91-q100.md). All remain **specified, not implemented or certified**.

**Q101–Q110 confirmed (2026-11-05)**: time-limited PHP EOL exceptions/planned migration, OS-certified plan/site isolation, manual/webhook Git with per-environment approvals, sensitive staging requiring extra permission, multi-CA ACME with recovery, shared/dedicated SQL and optional certified clusters, temporary/certified SSH access, test-qualified Webmail advice, quota grace by resource and conditional pre-sync/replication/failover. [Q101–Q110 decisions](decisions-q101-q110.md). **Specified only; no new runtime or OS certification.**

**Q121–Q130 confirmed (2026-11-05)**: first OS/WebStack **after comparative VM/security testing** (neither selected), external DNS with ACME **HTTP-01**, local administrator and site-manager roles, VPS observation plus controlled OS package upgrades, actual panel-config/PHP-file backup/restore, internal tests then **authorized private beta** after prerequisites, premium self-service transfers with manual lost-server recovery, contractual partner maintenance/alerts/withdrawal and security lead+deputy/triage. [Q121–Q130 decisions](decisions-q121-q130.md) · [MVP qualification](mvp-qualification.md). **Specified only; no running VM/product delivered.**

**Q131–Q140 confirmed (2026-11-05)**: local/CI VM qualification with snapshots, failures and per-OS reports; WebStack load, maintenance, recovery and disqualifying criteria; A/AAAA/80/HTTP-01/HTTPS checks; planned OS upgrades with impact/backup/health/recovery; encrypted local MVP backup with optional remote; site-manager scoped PHP/domains/TLS/files/SFTP/backup; private beta by waves/suspension/recovery; high-risk premium transfer dual approval; automated partner alerts/escalation/withdrawal; coordinated security notices. [Decisions](decisions-q131-q140.md) · [MVP qualification](mvp-qualification.md). **Everything remains to be implemented and tested.**

**Q141–Q150 confirmed (2026-11-05)**: **local/cloud** full VM drivers, compatible CI and common reports; **per-app-class** performance budgets and version regression tests; wizard suggesting external DNS records then rechecking A/AAAA/80/HTTP-01/HTTPS (**no auto-edit**); per-server OS update policy with later multi-server coordination; vault/off-failure backup recovery with optional external KMS/multiple custodians; shell-disabled, expiring/revocable/quota-audited SFTP; private beta health-based pause/recovery; later Hub cryptographic possession/org proof, severity/contract-driven partner action and signed coordinated risk-based security advisories. [Q141–Q150](decisions-q141-q150.md). **No shipped runtime or OS certification.**

**Q151–Q160 confirmed (2026-11-05)**: **local QEMU/KVM first**, cloud adapters later; signed historical internal VM reports; severity-based performance regression blocking with audited exceptions **never bypassing safety vetoes**; A/AAAA checks **only where published** for HTTP-01; approved **per-server** OS reboot/backup/recovery policies; encrypted archives deemed recoverable **only after isolated restore** and key checks; site-scoped public SFTP key expiry/audit; beta cohorts with local health and **separately consented** diagnostics; later Hub transfer risk triggers (lost host, repetition, identity) and signed **human FR/EN + structured machine** advisories. [Decisions](decisions-q151-q160.md) · [MVP qualification](mvp-qualification.md). **No runtime/VM certified.**

No date or version commitment is implied by these priorities. Product-owner decisions still needed: software/contribution license and authorized private security contact. Package/runtime choices require an evidence-based technical proposal, not a new architecture by assumption.

## Q161–Q170 adopted — no implemented feature claim

**Q161 C, Q162 B, Q163 C, Q164 B, Q165 C, Q166 C, Q167 C, Q168 C, Q169 C, Q170 B** are SPECIFIED, preserving Q1–Q160. R3 requires ephemeral KVM/private immutable proofs; R4 external DNS probe, bounded OS recovery, each-backup isolated restore and public SFTP keys; beta privacy cohorts; Hub R6 after R5 ABI for versioned risk-based transfers and signed JSON FR/EN advisories. [Decisions](decisions-q161-q170.md) · [Tests](../13-tests-quality/mvp-gates-q161-q170.md). No Core runtime was imported or verified by this documentation.

## R1 — Verifiable progress while application source remains absent

A read-only SRC-03 provenance preflight is **implemented** and tested on 16 synthetic ZIPs; see [R1 preflight](../12-development/source-archive-intake.md). It rejects changed archives, unsafe paths, links, collisions, excessive expansion and selected secret patterns, with **no import or system side effects**. The original v0.7 source required by [issue #2](https://github.com/yyogas/forgepanel/issues/2) is still unavailable here: **R1 source import = BLOCKED**, R2 Symfony/PG and the real R3 VM runner, R4–R6 remain unimplemented (R3 preparatory tools do exist). V3 HTML UI is a separate visual proposal, not an adopted Core baseline.

## R1 tooling status: provenance quarantine

Core now contains standalone `verify_source_archive.py` and `stage_source_archive.py`, which can verify and **prepare nonprivileged off-repository** source copies. **33 synthetic local unit tests passed**; exact-commit PR CI must be checked separately. Quarantine receipt `STAGED_FOR_MANUAL_REVIEW` is not an import; **no Symfony/Go application or installer has been imported or deployed**. Foundation v0.7 original ZIP remains missing and issue #2 stays open. [Procedure](../12-development/source-staging.md).

## Current verified baseline — R1 / R2 / R3 (after PR #43)

**Observed `develop` snapshot:** `a6a924370ef2c4b922b38d148594ed50d08f3b6e`. PRs #37, #38, #39, #40, #41 and #43 are **merged**. These are Git facts and preparatory tools; they do not make Q161–Q170 operational.

| Work | Code state | Exact evidence and limits |
|---|---|---|
| R1 ZIP preflight / private staging / integrity audit | **MERGED / synthetic PASS** | [PR #37](https://github.com/yyogas/forgepanel/pull/37), [#38](https://github.com/yyogas/forgepanel/pull/38), [#39](https://github.com/yyogas/forgepanel/pull/39), [post-merge CI](https://github.com/yyogas/forgepanel/actions/runs/42109154403); 60 synthetic tests, no actual SRC-03 imported |
| R1 genuine Foundation v0.7 source | **BLOCKED** | [Issue #2](https://github.com/yyogas/forgepanel/issues/2) remains open, pinned checksum in [evidence](../../evidence/sources.json); no original Symfony/Go application source imported |
| R2 real Symfony + PostgreSQL | **NOT IMPLEMENTED/NOT VERIFIED** | [Issue #3](https://github.com/yyogas/forgepanel/issues/3); no integrated HTTP/SQL application runtime in this repository |
| R3 KVM host observation, QCOW2 admission and private copying | **MERGED / synthetic PASS** | [PR #40](https://github.com/yyogas/forgepanel/pull/40), [#41](https://github.com/yyogas/forgepanel/pull/41), [#43](https://github.com/yyogas/forgepanel/pull/43), [post-merge Go CI](https://github.com/yyogas/forgepanel/actions/runs/42120185132), [docs CI](https://github.com/yyogas/forgepanel/actions/runs/42120185238); 62 synthetic Go test functions |
| R3 real KVM runner, VM, quotas, signed evidence | **NOT IMPLEMENTED/NOT QUALIFIED** | [Issue #42](https://github.com/yyogas/forgepanel/issues/42) open; tools always report `NOT_EXECUTED`, staged files are not guaranteed immutable |
| R4 PHP/ACME/restore; R5 ABI; R6 Hub | **NOT INTEGRATED** | [MVP #29](https://github.com/yyogas/forgepanel/issues/29), [ABI #7](https://github.com/yyogas/forgepanel/issues/7), [Hub](https://github.com/yyogas/forgepanel-hub); no complete hosting installation |

**Document reconciliation:** previous “feature branch candidate / merge to be checked” sentences are historical, not current state. PRs remain in the changelog and specialist docs; this table is the **reconciled observed Git snapshot**. For genuine completeness, track the [22 open gaps](documentation-readiness.md), [traceability matrix](requirements-traceability.md), [open issues](https://github.com/yyogas/forgepanel/issues) and qualification requirements. **No stable/main/production promotion.**

## R3 — Candidate typed IPC and installer contracts, not executable

[12 Symfony↔Go IPC requirements](../08-api-contracts/symfony-go-ipc-r3.md) and [12 installer requirements](../14-devops-releases/installer-lifecycle-r3.md) now have a [closed seven-action candidate registry](../../evidence/typed-agent-operations-v1.json) with **two explicitly blocked privileged actions** and [24 planned QA cases](../13-tests-quality/r3-ipc-installer-gates.md). **SPECIFIED only**: no working authenticated IPC socket, privileged Go agent, final wire protocol, SQL job model, package, installer or running VM. `DOC-GAP-005/006` stay OPEN. This does not unblock R1/R2 or couple Core to Hub.
