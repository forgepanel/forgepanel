<!-- forgepanel-doc id=FP-19-R3-JOB-INTEGRITY-AUDIT revision=1 status=specified -->
# R3 targeted review — Job idempotency, restore and tenant isolation

[Français](../../fr/19-audits-risks/r3-job-integrity-audit.md) · [Risks](README.md) · [Physical model](../09-database/physical-jobs-model-r3.md) · [Durable jobs](../09-database/durable-jobs-r3.md) · [R3 QA](../13-tests-quality/r3-physical-execution-gates.md)

**Internal targeted technical review of R3 candidate documents, not an independent security audit.** Reviewed baseline: Core `develop` commit `0af257ce362e01f5ef590d05b01a376d9e36cee8`, PR #48, `candidate-r3-physical-data-model-v1.json`, `candidate-job-transitions-v1.json`. No Linux, Go socket, PostgreSQL or historical Foundation application was executed. **Verdict: four OPEN findings; model not approved for migrations or privileged effects.** Q1–Q170 preserved, optional administrator MFA, Core standalone without Hub, R1 still blocked by missing SRC-03.

## AUDIT-FP-0033 / RISK-033 — Denied admission audit without fabricated job

**Severity: HIGH. Status: OPEN.** Scope: Database / API / Observability. **Finding:** admission denials `DENIED/REJECTED` must be audited **without** creating an accepted job, but candidate `fp_job_audit_events` previously only listed a `job_id uuid FK`, with no explicit representation of denied-admission events. An implementation could silently drop denials, invent a fake `ACCEPTED` job or use an invalid FK.

**Evidence:** [physical data model](../09-database/physical-jobs-model-r3.md) `DBPH-FP-0004/0011`, [admission contract](../08-api-contracts/symfony-go-ipc-r3.md) and [committed accepted-job schema](../../evidence/candidate-job-record-v1.schema.json).

**Recommendation / required change:** audit subject must be expressible independently of job existence. The **candidate revision** adds `request_ref`, `subject_kind`, `decision_code` and **conditionally nullable `job_id` for denied/rejected admissions only**; accepted job events require a valid job reference. Require approved conditional DB constraints, redacted correlated errors, duplicate safety and retention. **No approved DDL.**

**Owner: Database / API / Observability / Security. Required tests: `R3-AUDIT-TEST-001/002`.**

## AUDIT-FP-0034 / RISK-034 — Fencing reset after deletion or SQL restore

**Severity: CRITICAL for privileged activation, HIGH for unexecuted documentation. Status: OPEN.** Scope: Database / Security / DevOps. **Finding:** `fencing_generation bigint` in a current lease row alone is insufficient: if the lease row is deleted/recreated or PostgreSQL restored to an older snapshot, a previously issued generation may be reused. A paused old worker could resume and mutate Linux with what appears to be a current capability.

**Evidence:** `fp_resource_leases` and `DBPH-FP-0006/0012`, [typed effect contract](../08-api-contracts/typed-execution-recovery-r3.md) `EXEC-FP-0005`, [RISK-028](README.md).

**Recommendation / required change:** require a durable **monotonic high-water mark** per resource never reset by row recreation. Design an **independent post-restore recovery epoch** that revokes all pre-restore capabilities, verified **at the effect boundary**, not only in restored PostgreSQL. Candidate `fencing_epoch_ref` is an **unapproved placeholder**, **not** a secure implemented mechanism. Until restore epoch coordination and crash handling are demonstrated, **deny ACT-FP-0005/0007** and any resumed APPLY.

**Owner: Database / Security / DevOps / API. Required tests: `R3-AUDIT-TEST-003/004`.**

## AUDIT-FP-0035 / RISK-035 — Inbox dedup mistaken for Linux effect

**Severity: HIGH. Status: OPEN.** Scope: Database / IPC / Engineering / SRE. **Finding:** `fp_agent_inbox` receipt proves at most delivery. Recorded **before** a side effect, a crash could cause the consumer to skip an effect never applied. Recorded **after** an effect, an ACK loss could cause duplicate application. `UNIQUE(consumer_ref,message_id)` alone does not guarantee exactly-once external Linux mutation.

**Evidence:** `fp_agent_outbox/inbox`, `DBPH-FP-0007`, [candidate transition model](../../evidence/candidate-job-transitions-v1.json).

**Recommendation / required change:** explicitly distinguish proposed `RECEIVED`, `IN_PROGRESS`, `EFFECT_UNCERTAIN`, `EFFECT_VERIFIED`, `PROVEN_NO_EFFECT` and an **independently observed** effect verdict reference. Under uncertainty, reread Linux state and check current authorization/fence **before** any new effect. These names and fields are **candidates**, not an implemented durable state machine.

**Owner: Database / API-IPC / SRE / Security. Required tests: `R3-AUDIT-TEST-005/006`.**

## AUDIT-FP-0036 / RISK-036 — Scope authority and SQL tenant context spoofing

**Severity: HIGH. Status: OPEN.** Scope: Database / Security / Core. **Finding:** physical proposal contains future `scope_kind`/UUID `scope_ref` without actual owning entities/FKs. A NULL/wildcard scope, forged JSON tenant or SQL session GUC controlled by shared runtime identity could merge unrelated tenant jobs. RLS alone is not actor authentication.

**Evidence:** `DBPH-FP-0002/0003/0010`, [physical model](../09-database/physical-jobs-model-r3.md), [peer trust](../08-api-contracts/local-peer-trust-r3.md), [RISK-030](README.md).

**Recommendation / required change:** approve a scope catalogue and FKs with hosting data-model owner; require nonnull authorized scope and composite tenant/resource constraints tied to a **trusted, server-authenticated Core actor context**. Server-scoped mutations need separately proven server authority, not missing tenant scope. Test RLS/connection-context spoofing as defense-in-depth.

**Owner: Database / Security / Core. Required tests: `R3-AUDIT-TEST-007/008`.**

## Eight mandatory negative test plans

| ID | Required negative reproduction | State |
|---|---|---|
| `R3-AUDIT-TEST-001` | Denied admission audited without fabricated accepted job; durable request correlation | **PLANNED** |
| `R3-AUDIT-TEST-002` | Accepted-job audit without real FK, missing request ref or secret data denied | **PLANNED** |
| `R3-AUDIT-TEST-003` | Delete/recreate resource lease: old fence generation must never regain authority | **PLANNED** |
| `R3-AUDIT-TEST-004` | Restore earlier DB snapshot, wake old worker: no privileged APPLY | **PLANNED** |
| `R3-AUDIT-TEST-005` | Crash between inbox receipt and effect: never claim verified effect | **PLANNED** |
| `R3-AUDIT-TEST-006` | Crash between effect and ACK: dedup/reconciliation, no second APPLY | **PLANNED** |
| `R3-AUDIT-TEST-007` | NULL scope or forged tenant in request/SQL context fails cross-tenant | **PLANNED** |
| `R3-AUDIT-TEST-008` | Tenant attempts server scope or spoofs RLS context: deny | **PLANNED** |

The eight cases above are **future integration tests**, separate from static Python JSON/document consistency checks. **Zero functional tests were executed.** Future PASS evidence must name commit, migration, OS/PG, authenticated actor/scope, request, SQL and Linux before/after state, attempts, fence/epoch, typed errors, redacted audit and compensation. Use `SKIP/BLOCKED` when no real authorized environment exists.

## Review decision and handoffs

- **Verdict: REVIEW REQUIRED / OPEN.** These are proposed **specification** corrections. This does not certify security, authorize `CREATE TABLE` or close any finding.
- **Database:** denied-admission audit subject, scope FKs, nonresettable fencing, inbox/outbox and real migration design.
- **Security:** actor trust, replay and post-restore effect-boundary fencing, RLS and privileges.
- **API/IPC:** ACK distinct from Linux outcome, idempotency, restart/recovery states and typed errors.
- **DevOps/QA:** real crash/restore/stale-worker scenarios on authorized disposable OS/PG and absence of privileged effects.
- **MASTER:** resolve conflicts, no automatic adoption of the physical schema. `DOC-GAP-004/005/006` stay OPEN and [genuine source #2](https://github.com/yyogas/forgepanel/issues/2) remains the application gate.
