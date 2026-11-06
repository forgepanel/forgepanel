<!-- forgepanel-doc id=FP-09-R3-DURABLE-JOBS revision=2 status=specified -->
# R3 — Durable jobs, concurrency, idempotency and leases: candidate contract

[Français](../../fr/09-database/durable-jobs-r3.md) · [Database](README.md) · [Typed IPC](../08-api-contracts/symfony-go-ipc-r3.md) · [Peer trust](../08-api-contracts/local-peer-trust-r3.md) · [R3 tests](../13-tests-quality/r3-jobs-peer-gates.md)

**Owner: Database / Data Model.** Mandatory API/IPC, Core, Security, DevOps and QA reviews. **State SPECIFIED / CANDIDATE, not ratified.** Evidence files are **design-time JSON schemas**, not PostgreSQL migrations. No historical SRC-03 source, new table or application worker was implemented. Dependencies [R1 #2](https://github.com/yyogas/forgepanel/issues/2), [R2 #3](https://github.com/yyogas/forgepanel/issues/3) and [Configuration Engine #9](https://github.com/yyogas/forgepanel/issues/9); `DOC-GAP-004` and `DOC-GAP-006` remain **OPEN**. Q1–Q170 preserved; no Q171+ thresholds are invented.

## Persistence invariants

**DB-FP-0001 — Intent identity.** Persist independently authorized tenant/resource scope, closed `operation_id`, actor, policy/contract versions, expected revision, canonical payload digest, `idempotency_key`, `request_id` and `correlation_id`. Tenant identity must derive from **server-side trusted scope**, never only a user-supplied claim.

**DB-FP-0002 — Atomic admission.** Revalidate authority, revision, conflicts and limits before durably committing intent + policy decision + audit and a transactional outbox record if needed. Acknowledge asynchronous `ACCEPTED` **only after PostgreSQL commit**. ACK never proves Linux effects.

**DB-FP-0003 — Scoped idempotency.** Candidate uniqueness spans `tenant_scope + resource_scope + operation_id + idempotency_key`; preserve the immutable digest of version, policy and payload. Same key/same digest retrieves **the same committed job**; same key/different digest yields `IDEMPOTENCY_CONFLICT` without executing anything. A retry must never cross an organization or resource boundary.

**DB-FP-0004 — Resource leases and fencing.** Mutating jobs acquire resource-scoped owner/generation (`fencing_token` candidate), expiry and observed revision. **Lease expiry never permits blind APPLY**: reconcile desired/observed state and earlier effects. The Linux consumer must reject an old generation even if a former worker resumes.

**DB-FP-0005 — Step journal.** Record ordered step identity, signed/hashed plan, start/end, attempt, resource, observed result, redacted reason, checkpoint and compensation verdict. Only `QUEUED → RUNNING → VERIFYING → SUCCEEDED` on actual verified effect; `FAILED`, `COMPENSATION_REQUIRED` and `BLOCKED` must retain uncertainty accurately.

**DB-FP-0006 — Crash reconciliation.** On worker restart, inspect job, outbox/inbox and resource state **before** any new effect. If an external effect may have occurred but cannot be proven, require `COMPENSATION_REQUIRED` and review, **never** silent replay. Irreversible operations require controlled/manual verification.

**DB-FP-0007 — Inbox/outbox.** Commit the intention to publish in the same transaction as the business state transition; `at-least-once` delivery needs consumer deduplication, with delivery ACK separate from domain success. Crash between commit, dispatch and acknowledgement must not lose jobs or reapply them.

**DB-FP-0008 — Concurrency/order.** Permit harmless concurrent observations but serialize or explicitly constrain mutations affecting tenants, sites, listeners, Linux users, services, packages and policies. Deny stale revision, lost lease, unresolved deadlocks and overlapping mutations. DDL migrations use a separate authority.

**DB-FP-0009 — Transactional redacted audit.** Log timestamped correlation, actor/authority/scope, plan/step IDs, versions and expected/observed results. Never log full tokens, cookies, signing/private keys, DB credentials, hosting customer content or raw backups. Never surface SQL internal failures directly to clients.

**DB-FP-0010 — Cancellation/deadline.** A cancellation is a **request to stop**, not a transactionally guaranteed reversal of Linux effects. During APPLY, identify an actual safe stop/compensation boundary. Timeout, retry, backoff, lease and retention limits remain **unapproved configuration values**. Expired deadline never means `SUCCEEDED`.

**DB-FP-0011 — Migration/availability.** Plan checksummed migrations, separate DDL/runtime DB roles, unique constraints and tenant FK controls, backup/restore and compatible rolling upgrades. Migration failure must not expose an unprotected public admin endpoint or enable uncontrolled `install apply`.

**DB-FP-0012 — Retention/deletion.** Set per-category retention/erasure rules consistent with legal and audit constraints, while retaining sufficient anti-replay state for a documented grace window; do not invent any duration. Purge sensitive payloads and personal data without erasing required security audit evidence prematurely.

## Candidate logical entities — no schema approved

| Conceptual entity | Candidate information | Ownership and constraints |
|---|---|---|
| `OperationIntent` | tenant, actor, operation, resource, digest, idem key, revisions, state | Scope/op/key uniqueness; Database + Security |
| `JobExecution` | intent ref, state, attempt, target, observation, timestamps | Versioned transitions, no unobserved success |
| `ResourceLease` | resource, owner, generation, expiry, observed revision | Monotonic fencing checked by agent |
| `JobStepEvent` | step, evidence, state, observed effect, error, correlation | Redacted append-only journal |
| `DispatchOutbox/Inbox` | canonical message, destination, delivery ACK, dedup | At-least-once transport, idempotent effect |
| `RecoveryCheckpoint` | plan, digest, reversible action, state, retention | No false cross-SQL/Linux atomic rollback |

**None of these names is approved as actual `fp_*` tables.** [Candidate job record schema](../../evidence/candidate-job-record-v1.schema.json) describes **an already committed admitted job**, not rejected admission requests (which require separate IPC response/audit and no job), and [candidate transition registry](../../evidence/candidate-job-transitions-v1.json) describes allowed steps; neither runs in production. Actual FKs, indexes, physical tables and migrations require SRC-03 review and Database ratification.

## Mandatory failure/race scenarios

- Two simultaneous same-key/digest requests must map to one intent/job; same key/changed payload → `IDEMPOTENCY_CONFLICT`.
- PostgreSQL commits but HTTP/IPC reply is lost: retry must read durable status without a second `APPLY`.
- Worker A loses lease, B acquires it, A resumes: fencing must reject A before any system effect; B reconciles observed state.
- Crash after a **bounded** Linux mutation but before `VERIFYING`: remain uncertain and never automatically replay.
- Outbox deliveries duplicated, delayed or reordered: no privilege escalation or unobserved `SUCCEEDED`.
- Panel PostgreSQL restore or lost decryption key: stale grant invalidation, explicit recovery failure; no sensitive audit export.

## Ownership and open implementation decisions

**Database** must propose/approve table topology, constraints, isolation level, SQL/outbox mechanics, FK, TTL/retries and retention. **API/IPC** owns wire and acknowledgement semantics; **Security** owns peer/tenant/secret/lease trust; **DevOps** owns observable effects and compensations. All [12 `R3-JOB-TEST-001..012`](../13-tests-quality/r3-jobs-peer-gates.md) are **PLANNED**. No real DB, agent or installer executed in this lot. Free Core jobs must continue without Hub.

## Schema invariant: queued jobs have no lease

The persistent job record models **only actually committed admissions** (`admission=ACCEPTED`, `admitted_after_commit=true`): a denied request must not invent a `job_ref`. `QUEUED` has **no lease** (`lease=null`) and no effect evidence, while `RUNNING` requires a **structured fencing lease** before any external effect. These are candidate schema constraints, not a deployed PostgreSQL migration or actual distributed lock. Documentation revision only.
