<!-- forgepanel-doc id=FP-00-DOC-READINESS revision=4 status=documented -->
# Documentation gap register and completion gates — ForgePanel

[Français](../../fr/00-project-control/documentation-readiness.md) · [Project control](README.md) · [Traceability](requirements-traceability.md) · [Coverage](coverage.md)

**Targeted audit of both `develop` repositories**: paired language indexes do not mean complete implementation contracts or real integration tests. The [version 1 data register](../../evidence/documentation-readiness-v1.json) preserves stable identifiers and dependencies. Core snapshot `a6a924370ef2c4b922b38d148594ed50d08f3b6e`; Hub snapshot `243d1ebb99649372ccc931deb603d172b2e17e18`. Recheck after future changes. **Q1–Q170 preserved; Q171+ not approved.**

## How to interpret this register

`BLOCKED` = genuinely missing prerequisite bytes; `OPEN` = missing detailed specification, contract or test evidence. `P0` = editorial priority for first functional release or legal distribution; `P1` = later gate/dependency. **Priorities are documentation work sequencing, not new owner product decisions.** Never mark `DOCUMENTED`/`VERIFIED` without linked evidence; green Markdown CI is not an application test.

## Gaps and owners

| ID | Phase / priority | Authority | Rules | Missing deliverable | Issue / state |
|---|---|---|---|---|---|
| DOC-GAP-001 | R1 / P0 | Project Control / Engineering | Q120 | Original Foundation v0.7 archive and provenance-preserving application import; optional-MFA patch inspected | [#2](https://github.com/yyogas/forgepanel/issues/2) · **BLOCKED** |
| DOC-GAP-002 | R2 / P0 | Core / Security | Q124, Q130 | Permanent administrator identity and optional MFA enable/skip/resume/recovery boundaries | [#6](https://github.com/yyogas/forgepanel/issues/6) · **OPEN** |
| DOC-GAP-003 | R2 / P0 | Engineering / Core | Q119, Q120 | Bootable locked Symfony runtime and real HTTPS/session/CSRF/browser contracts | [#3](https://github.com/yyogas/forgepanel/issues/3) · **OPEN** |
| DOC-GAP-004 | R2 / P0 | Database / Core | Q126 | PostgreSQL persistent hosting model, migrations, tenant ownership, concurrency, backup/restore transaction semantics | [#3](https://github.com/yyogas/forgepanel/issues/3) · **OPEN** |
| DOC-GAP-005 | R3 / P0 | DevOps / Security | Q61, Q62, Q119 | Signed one-command installer, trusted package origin, OS compatibility and interruption/reinstall path | [#15](https://github.com/yyogas/forgepanel/issues/15) · **OPEN** |
| DOC-GAP-006 | R3 / P0 | API/IPC / Security | Q47, Q120 | Typed least-privilege Symfony-to-Go operations, durable jobs/errors/audit/locks without arbitrary shell | [#9](https://github.com/yyogas/forgepanel/issues/9) · **OPEN** |
| DOC-GAP-007 | R4 / P0 | Modules / Hosting | Q83, Q91, Q119 | First isolated PHP-FPM website, per-site WebStack selector, configuration plan and health | [#22](https://github.com/yyogas/forgepanel/issues/22) · **OPEN** |
| DOC-GAP-008 | R4 / P0 | Services / Security | Q123, Q164 | External DNS A/AAAA published-family checks, bounded independent probe, port 80 HTTP-01 and HTTPS | [#29](https://github.com/yyogas/forgepanel/issues/29) · **OPEN** |
| DOC-GAP-009 | R4 / P0 | Security / Modules | Q136, Q167 | Scoped website-manager permissions, restricted SFTP public keys, revocation, expiring grants and cross-tenant denial | [#22](https://github.com/yyogas/forgepanel/issues/22) · **OPEN** |
| DOC-GAP-010 | R4 / P0 | Recovery / Database | Q126, Q145, Q166 | Encrypted recoverable panel/site backups with key access and full isolated restore per backup | [#23](https://github.com/yyogas/forgepanel/issues/23) · **OPEN** |
| DOC-GAP-011 | R3 / P0 | DevOps / QA | Q132, Q151, Q152, Q161, Q162 | Real ephemeral KVM runner, immutable launched bytes, actual quotas, snapshots, fault drills and signed private evidence | [#42](https://github.com/yyogas/forgepanel/issues/42) · **OPEN** |
| DOC-GAP-012 | R4 / P0 | DevOps / Operations | Q125, Q155, Q165 | Allowlisted per-server OS packages/service maintenance, bounded repair and local compensation | [#15](https://github.com/yyogas/forgepanel/issues/15) · **OPEN** |
| DOC-GAP-013 | R5 / P1 | Architecture / API | Q120 | Neutral signed detached-extension ABI, lifecycle, compatibility, explicit privileges and fail-open Core autonomy | [#7](https://github.com/yyogas/forgepanel/issues/7) · **OPEN** |
| DOC-GAP-014 | R6 / P1 | Hub / API | Q168, Q169, Q170 | Detached Symfony publisher runtime, signed Core handshake and separate publisher identity/database | [#2](https://github.com/yyogas/forgepanel-hub/issues/2) · **OPEN** |
| DOC-GAP-015 | R6 / P1 | Hub / Commerce | Q56, Q60, Q169, Q170 | Published catalog, sandbox billing, idempotent entitlement, risk transfer and signed FR/EN advisory flow | [#3](https://github.com/yyogas/forgepanel-hub/issues/3) · **OPEN** |
| DOC-GAP-016 | PRE-PUBLIC / P0 | Legal / Governance | Q111, Q112, Q118 | Operative AGPL-only/or-later choice, commercial terms, contributor CLA/rights and verified private security routes | [#11](https://github.com/yyogas/forgepanel/issues/11) · **OPEN** |
| DOC-GAP-017 | DESIGN / P0 | Design System / Product | Q55, Q70, Q80 | Review and adopt or reject V3 visual candidate; version tokens/components, role layouts and accessibility tests | [#18](https://github.com/yyogas/forgepanel/issues/18) · **OPEN** |
| DOC-GAP-018 | POST-MVP / P1 | Modules / Plugins | Q51, Q80, Q81 | Complete module/plugin/app/recipe cards and signed manifest policy without arbitrary plugin execution | [#7](https://github.com/yyogas/forgepanel/issues/7) · **OPEN** |
| DOC-GAP-019 | POST-MVP / P1 | Observability / Performance | Q67, Q68, Q142 | Versioned SLO, structured logs/retention, health, capacity and per-application performance budgets | [#17](https://github.com/yyogas/forgepanel/issues/17) · **OPEN** |
| DOC-GAP-020 | POST-MVP / P1 | Recovery / Architecture | Q90, Q100 | Authorized cross-server website migration and selective restore with staging and compatibility/rollback plan | [#26](https://github.com/yyogas/forgepanel/issues/26) · **OPEN** |
| DOC-GAP-021 | RELEASE / P0 | QA / Release | Q119, Q127, Q132 | Actual clean VM-to-PHP-site-HTTPS MVP proof, signed builds, private beta readiness and incident stop conditions | [#29](https://github.com/yyogas/forgepanel/issues/29) · **OPEN** |
| DOC-GAP-022 | GUIDES / P1 | Documentation / Support | Q119, Q124 | Validated operator/client guides, rollback runbooks, troubleshooting, FR/EN UI terminology and accessibility | [#29](https://github.com/yyogas/forgepanel/issues/29) · **OPEN** |

## Required closure gates

**Mandatory closure evidence:** complete module/user story, positive and negative scenarios, dependencies, typed API/errors, roles/permissions, data and migration impact, security, audit/observability, failure/recovery, traceable tests, versions and paired FR/EN. Mark truly inapplicable elements N/A with justification; never invent undecided business values.

## Evidence limits

**Material blockers:** original SRC-03 missing; no operational Symfony/PostgreSQL Core, installer or verified PHP HTTPS site; no working neutral extension ABI; Hub candidate only. R1 ZIP safety and R3 KVM observation/admission/staging tools do exist on `develop` (PR #37–#43), but synthetic tests do not certify any OS. [Status](status.md) · [Roadmap](implementation-roadmap.md) · [QA](../13-tests-quality/README.md).

## Targeted documentary progress for DOC-GAP-005 and DOC-GAP-006

[Candidate R3 IPC contract](../08-api-contracts/symfony-go-ipc-r3.md), [installer state machine](../14-devops-releases/installer-lifecycle-r3.md), [closed operations registry](../../evidence/typed-agent-operations-v1.json) and [24 planned tests](../13-tests-quality/r3-ipc-installer-gates.md) improve traceability. **Both states remain OPEN / OPEN**: no actual Symfony↔Go IPC, installer, SQL job model or real VM test has been approved or executed. No gap is closed and no retry/timeout/quota values are invented.

## Candidate R3 detail for DOC-GAP-004 and DOC-GAP-006

The [12 durable job requirements](../09-database/durable-jobs-r3.md), [12 peer trust requirements](../08-api-contracts/local-peer-trust-r3.md), [24 planned QA cases](../13-tests-quality/r3-jobs-peer-gates.md) and [candidate schemas](../../evidence/candidate-job-record-v1.schema.json) make the gaps more concrete. **Both remain OPEN** because actual PostgreSQL tables/migrations, authenticated Go IPC/daemon and concurrency/OS tests are not reviewed/verified. Timings, retries, protocol, service users and quotas remain open technical choices. Q1–Q170 preserved, Q171+ unanswered.

## Further candidates for DOC-GAP-004/005/006 — no gap closure

[Physical DB proposal](../09-database/physical-jobs-model-r3.md), [service identities](../14-devops-releases/linux-service-identities-r3.md) and [typed execution](../08-api-contracts/typed-execution-recovery-r3.md) add implementation-specific choices and [36 candidate tests](../13-tests-quality/r3-physical-execution-gates.md). Machine-readable JSON is **not approved**; **DOC-GAP-004, DOC-GAP-005 and DOC-GAP-006 remain OPEN** pending actual PostgreSQL, Linux and VM evidence. The original total of 22 readiness gaps is unchanged.
