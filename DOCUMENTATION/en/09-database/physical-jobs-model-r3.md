<!-- forgepanel-doc id=FP-09-R3-PHYSICAL-JOBS revision=2 status=specified -->
# R3 — Candidate physical PostgreSQL model for Core jobs

[Français](../../fr/09-database/physical-jobs-model-r3.md) · [Database](README.md) · [Logical jobs](durable-jobs-r3.md) · [Typed execution](../08-api-contracts/typed-execution-recovery-r3.md) · [QA](../13-tests-quality/r3-physical-execution-gates.md)

**Authority: Database / Data Model. SPECIFIED / CANDIDATE — no approved DDL or executed migration.** This is a concrete proposal derived from DB-FP-0001..0012 and IPC-FP-0001..0012, not a replacement. `fp_*` names, fields, types, indexes and isolation policies **are suggestions, not an approved schema**. Historical SRC-03 Foundation v0.7 still missing (issue #2); no running Symfony/PG R2 (issue #3). **DOC-GAP-004 and DOC-GAP-006 remain OPEN.** Q1–Q170 preserved, no Q171+ or numeric choices approved.

## Twelve candidate physical invariants

**DBPH-FP-0001 — Preserve provenance.** Historical `fp_setup`, `fp_admins`, and `fp_setup_audit` are **observed in SRC-03 evidence**, not applied Core tables. Do not alter them or add new structures before genuine source comparison, ADR and Database/Security approval. Internal panel PostgreSQL is distinct from hosted customer databases.

**DBPH-FP-0002 — Immutable scope.** Each intent binds a verified `scope_kind` (server/org/account/site—catalogue **to review**), `scope_ref`, `resource_kind`, `resource_ref` and closed-registry `operation_id`. Never interpret a missing tenant as wildcard. Server-scoped work requires separately verified server authority. Real org/site foreign keys require the future hosting data model owner’s approval.

**DBPH-FP-0003 — Atomic scoped idempotency.** Candidate uniqueness `(scope_kind, scope_ref, resource_kind, resource_ref, operation_id, idempotency_fingerprint)` plus immutable `payload_sha256`, `contract_version` and `policy_revision`. Under transaction, verify actor/ownership/revision and insert or lock the existing intent. Same key/digest retrieves the **same job**; same key/different payload returns `IDEMPOTENCY_CONFLICT`. Never start a second APPLY as a side effect of ON CONFLICT.

**DBPH-FP-0004 — Commit before ACK.** Atomically insert admitted intent, initial `QUEUED` state, decision audit and an outbox record **before** acknowledging asynchronous `ACCEPTED`. If commit fails, do not report an accepted job. `DENIED/REJECTED` are response/audit outcomes, **not** fabricated accepted-job rows.

**DBPH-FP-0005 — Executions and transitions.** One execution references an intent. State is `QUEUED/RUNNING/VERIFYING/SUCCEEDED/FAILED/COMPENSATION_REQUIRED/BLOCKED`. `SUCCEEDED` needs an observed effect and passed health checks. Neither an IPC ACK, zero process exit, nor systemd `active` alone is such evidence.

**DBPH-FP-0006 — Monotonic lease fencing.** Only a current generation owns a mutation lease for a resource; `fencing_generation` increases on ownership transfer. An effect-boundary Linux validator must reject stale generations even if a former worker wakes up. SQL lease expiry **does not prove** the old worker stopped changing Linux. `QUEUED` has no lease; `RUNNING` requires one.

**DBPH-FP-0007 — Outbox/inbox duplicate safety.** `At-least-once` transport is acceptable only when dispatcher/consumer deduplicate against durable message IDs and independently check effects. Transport ACK is separate from domain job success. **No exactly-once distributed PostgreSQL/Linux transaction** is promised.

**DBPH-FP-0008 — Steps and compensation.** Every stage records identity, ordered sequence, plan digest, approval, start, observation, checkpoint and compensation class (reversible, uncertain, irreversible). Rolling back a DB transaction is not undoing an already applied Linux effect; checkpoint use requires readable/verifiable content and recovery keys.

**DBPH-FP-0009 — Short transactions/concurrency.** Lock job/intent/leases in deterministic order and handle conflicts/deadlocks with a still-unapproved isolation/retry policy. Never hold a SQL transaction open across a long external Linux mutation; instead perform short state transitions, outbox delivery, effect observation and recovery.

**DBPH-FP-0010 — Separated DB roles.** Migration/DDL, Symfony runtime, read-only observer and worker/dispatcher need independent identities and smallest grants. Runtime must not own tables or execute DDL. RLS/`FORCE ROW LEVEL SECURITY` may be additional safeguards but **cannot replace** actual actor/tenant proof, RBAC or authenticated connection context.

**DBPH-FP-0011 — Redacted audit/retention.** Timestamped append-only logical audit never stores raw idempotency tokens when sensitive, credentials, cookies, private signing material or tenant content. Prevent unauthorized alteration; protect collection/retention and deletion according to policy **not yet ratified**, maintaining anti-replay commitments.

**DBPH-FP-0012 — Migration and restore.** Checksum migrations, forward recovery for irreversible DDL, verified backups, concurrent migration tests and key recovery are required. Restoring older PostgreSQL state may resurrect jobs/leases: invalidate stale grants and **reconcile actual Linux state before reexecuting anything**.

## Proposed physical tables and constraints — NOT an executable SQL migration

| Proposed `fp_*` object | Candidate types/columns | Candidate constraints |
|---|---|---|
| `fp_operation_intents` | `intent_id uuid PK`, `scope_kind text`, `scope_ref uuid`, `resource_kind text`, `resource_ref uuid`, `operation_id text`, `actor_ref uuid`, `idempotency_fingerprint bytea`, `payload_sha256 bytea`, `contract_version text`, `policy_revision text`, `expected_revision text`, `created_at timestamptz` | UNIQUE(scope/resource/operation/key), not-null verified scope; operation registry is never a dynamic command |
| `fp_job_executions` | `job_id uuid PK`, `intent_id uuid FK`, `state text`, `state_revision bigint`, `attempt_count integer`, `observed_effect text`, `updated_at timestamptz` | UNIQUE(intent_id); allowed states and attempt CHECK; versioned transitions |
| `fp_resource_leases` | `scope_kind text`, `scope_ref uuid`, `resource_kind text`, `resource_ref uuid`, `owner_job_id uuid FK`, `fencing_generation bigint`, `expires_at timestamptz`, `resource_revision text` | UNIQUE(scope_kind,scope_ref,resource_kind,resource_ref), monotonic fencing, compare-and-swap |
| `fp_job_step_events` | `event_id bigint PK`, `job_id uuid FK`, `step_seq bigint`, `step_ref text`, `transition text`, `effect_verdict text`, `plan_sha256 bytea`, `audit_ref text`, `created_at timestamptz` | UNIQUE(job_id,step_seq), append-only logical event journal |
| `fp_agent_outbox` | `message_id uuid PK`, `job_id uuid FK`, `channel text`, `payload_digest bytea`, `delivery_status text`, `attempts integer`, `next_attempt_at timestamptz` | retry/sweep indexes, delivery separated from Linux result |
| `fp_agent_inbox` | `consumer_ref text`, `message_id uuid`, `observed_job_id uuid FK`, `receipt_at timestamptz` | UNIQUE(consumer_ref,message_id), durable consumer dedup |
| `fp_recovery_checkpoints` | `checkpoint_id uuid PK`, `job_id uuid FK`, `artifact_digest bytea`, `recovery_class text`, `storage_ref text`, `verified_at timestamptz` | never store plaintext recovery secrets; keys must be available |
| `fp_job_audit_events` | `audit_id bigint PK`, `job_id uuid FK`, `actor_ref uuid`, `correlation_ref text`, `outcome text`, `created_at timestamptz` | append-only, redacted, narrowly readable |

**No listed table, column, FK, type or index is approved.** This creates **no** `CREATE TABLE`, `ALTER TABLE`, seed, migration, database grant or API. Candidate UUID types presume future consistency with hosting resource identity and cannot be wired to unapproved entities.

## Candidate atomic admission — illustrative, NOT ready-to-run SQL

~~~text
BEGIN;
  authorize actor/tenant/resource using trusted server-side Core context;
  validate policy, operation registry, target and expected revision;
  insert-or-find intent by scope/resource/operation/idempotency fingerprint;
  lock selected intent, compare immutable payload/contract/policy digests;
  changed payload on same key -> rollback / IDEMPOTENCY_CONFLICT;
  existing matching intent -> return original durable job, without new effect;
  new intent -> commit QUEUED job, audit and outbox record together;
COMMIT;
only acknowledge ACCEPTED(job_ref) after successful commit;
dispatcher and Go consumer later validate fencing, plan and observed effects.
~~~

This is a **pseudo-algorithm**, not validated SQL. Exact UPSERT, transaction isolation, resource lock ordering, outbox and idempotency SQL constraints require Database-owned tests.

## Negative evidence and handoffs

Real disposable PostgreSQL tests must cover parallel same-key requests, different payload conflict, forced rollback, lost postcommit ACK, stale worker, duplicate outbox messages, failed agent, DB restore and lost keys. All [`R3-PHYS-TEST-001..012`](../13-tests-quality/r3-physical-execution-gates.md) are **PLANNED**. Security reviews tenant/RLS and fencing at Linux effect; API owns IPC ACK; DevOps owns actual cleanup and failures; Database owns any future DDL and migrations **in a separate PR after SRC-03 import and R2 integration**. PostgreSQL structure alone cannot certify Linux security.
