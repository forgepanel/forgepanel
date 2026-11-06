<!-- forgepanel-doc id=FP-09 revision=9 status=documented -->
# Database, transactions and migrations

[Français](../../fr/09-database/README.md) · [Index](../README.md)

## Actual prototype schema

SRC-03 `apps/panel/migrations/001_setup.sql` defines three tables, not the large hosting model previously proposed.

| Table | Data and constraints |
|---|---|
| `fp_setup` | Single row constrained to singleton=1; JSONB versioned setup payload including token/grant/resume verifiers, expiry, counters, phase and configuration revision |
| `fp_admins` | UUID, unique email, password hash, initial administrator flag, restricted super-admin role, encrypted MFA secret, activation state, TOTP counter and recovery-code hashes |
| `fp_setup_audit` | Generated bigint primary key, event, JSONB metadata and timestamp |

A partial unique index permits only one `initial_admin=true`. `PdoSetupRepository` locks the setup row with `FOR UPDATE`; account/state/audit writes use the same transaction. This is an inspected implementation, not a demonstrated concurrency guarantee in this environment.

## Customer data services Q86/Q90 — targets

**MariaDB/MySQL and PostgreSQL tenant DBs** will use separate drivers and scoped roles/quotas; **Redis/Valkey** are optional cache/queue services. These resources do not exist in the current setup-only schema. Staging clones/selective restores need consistent snapshots, protected credentials, tenant authorization and pre-overwrite checks. Panel PostgreSQL stays separate from customer databases. [Website lifecycle](../02-architecture/website-lifecycle.md).

## Customer engines and cross-server migration (Q96, Q100)

One hosting account may own **separate MariaDB/MySQL and PostgreSQL** services plus optional Redis/Valkey cache/queues under verified capabilities, with per-engine quota/grant/secret policy (Q96). Panel-internal PostgreSQL is **not** shared with customer DBs. Cross-server migration Q100 needs version/schema preflight, consistent snapshot, authenticated encrypted transfer, DB account mapping, rotated secrets and audited recovery. No customer DB driver or cross-server migrator exists in the current setup-only prototype. [Details](../02-architecture/cross-server-migration.md).

## SQL/cache topology and migration Q106/Q110

Beyond Q96 multiple tenant DB engines, **Q106 D** allows **shared or dedicated per-plan** services, plus **optional, actually certified** cluster/replication adapters. Each driver documents tenant schema/user isolation, quorum/leader/failover when supported, replication lag, consistent backup, secrets and restoration. Redis/Valkey are not automatically SQL or clustered storage. **Q110 D** permits pre-sync and advanced cutover only with tested application-write and transaction consistency; otherwise require maintenance/freeze and recovery. Panel PostgreSQL remains separate. [Migration](../02-architecture/cross-server-migration.md) · [Decisions](../00-project-control/decisions-q101-q110.md).

## Migration and ownership requirements

The SQL file is not applied per HTTP request. No complete migration runner or upgrade/rollback framework is provided. Future packages must separate a migration role from the non-DDL runtime role, track applied migration IDs/checksums and prevent concurrent migrators. Test fresh install and upgrade from each supported source revision. Destructive migrations require backups, retention decisions and a forward/recovery plan; a code downgrade is not an automatic data rollback.

Secrets require both database and encryption-key recovery. Do not store the encryption key in the same publicly readable backup as encrypted MFA data. Audit retention, deletion policy, customer schema and tenant-enforced query boundaries remain to be specified before hosting features are added.

## Required evidence

Run the supplied PostgreSQL test only against an explicitly authorized dedicated `_test` database. It covers a forced rollback and persistence, not every concurrency/failure mode. Add simultaneous activation, lost response after commit, database restart, stale configuration revision and restore/key-loss scenarios. No PDO PostgreSQL driver/server was available for this audit; in-memory tests are not SQL integration tests.

[Core](../03-core/README.md) · [Quality](../13-tests-quality/README.md)

## R2 — Candidate transaction contract, no migrations

[Candidate R2 PostgreSQL/transaction contract](setup-transaction-r2.md) traces `R2-DB-001`–`R2-DB-012`: setup singleton, initial admin uniqueness, locks/revisions, retries after lost response, rollback/audit and key recovery. **No new table, column, migration, isolation level or grant TTL is decided**. Database must review against imported SRC-03 before real PostgreSQL [R2 tests](../13-tests-quality/r2-integration-gates.md).

## R3 — Handoff: durable IPC jobs, idempotency and locks (unmodeled)

Future [Symfony ↔ Go IPC](../08-api-contracts/symfony-go-ipc-r3.md) needs durable intent/approval/job/audit, revisions, idempotency and scoped leases, while the [installer lifecycle](../14-devops-releases/installer-lifecycle-r3.md) must recover from crashes without replaying Linux changes. **This lot creates no PostgreSQL table/column/migration**. Database owns actual schemas, approved unique `(scope,operation,idempotency_key)` or equivalent, digest reconciliation, leases, audit/outbox, concurrency, recovery and retention tests, coordinated with Security and API/IPC. Names are examples, not authorized DDL.

## R3 — Candidate durable job and lease model

[R3 PostgreSQL job contract](durable-jobs-r3.md) documents 12 requirements DB-FP-0001..0012 for durable intent, scoped idempotency, leases/fencing, state transitions, outbox/inbox, lost ACK, concurrency, redacted audit and recovery. [Candidate transition registry](../../evidence/candidate-job-transitions-v1.json) and [job record schema](../../evidence/candidate-job-record-v1.schema.json) are **not DDL or installed tables**. No lease duration, SQL isolation, migration or retry setting is approved absent Database/API/Security review. [QA plan](../13-tests-quality/r3-jobs-peer-gates.md).

## R3 — Proposed physical PostgreSQL jobs, no DDL

[Candidate physical PostgreSQL model](physical-jobs-model-r3.md) details `DBPH-FP-0001..0012`, **8 proposed table objects**, uniqueness, relationships, tenant scope, idempotency, outbox/inbox, fenced leases and recovery. [Candidate table register](../../evidence/candidate-r3-physical-data-model-v1.json) is **not a migration** and does not modify any of the three historical SRC-03 tables. Types/FKs/indexes, DB roles and limits require Database/Security review after genuine source import. [36 R3 planned tests](../13-tests-quality/r3-physical-execution-gates.md).

## R3 — Review of denied admission, inbox and restored fences

[Targeted review](../19-audits-risks/r3-job-integrity-audit.md) raises **RISK-033/034/035/036** against the [candidate physical model](physical-jobs-model-r3.md): record denials without fake jobs, nonresettable fencing after lease deletion/restore, inbox receipt distinct from Linux effect, authenticated scope even with RLS. [Eight future tests](../19-audits-risks/r3-job-integrity-audit.md) remain `PLANNED`. **No real table/constraint/fencing mechanism is fixed or approved**; Database review and migrations remain OPEN.
