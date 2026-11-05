<!-- forgepanel-doc id=FP-09-TRANSACTION-R2 revision=1 status=specified -->
# R2 — Candidate PostgreSQL contract: bootstrap, concurrency and recovery

[Français](../../fr/09-database/setup-transaction-r2.md) · [Database](README.md) · [R2 identity](../03-core/bootstrap-identity-r2.md) · [R2 tests](../13-tests-quality/r2-integration-gates.md)

**Owner:** Database / Data Model with Core, Security and API/IPC. **SPECIFIED — CANDIDATE**: no schema, migration or table is added by this document. Foundation v0.7 SRC-03 is absent from `develop` (issue #2), so these observations derive from the existing inventory, **not an executed PostgreSQL database**. IDs `R2-DB-001` through `R2-DB-012`.

## Observed inventory, no invented structures

Historical `apps/panel/migrations/001_setup.sql` defines **exactly three tables**: `fp_setup` (singleton, JSONB state/revision/token), `fp_admins` (UUID, unique email, hash, role, MFA and activation), and `fp_setup_audit` (timestamped events). A partial `initial_admin=true` index enforces a single initial administrator; prototype PDO repository locks `fp_setup` with `SELECT … FOR UPDATE`. **This is not an applied Core migration in the repository today.** The hosting multi-tenant data model is neither implemented nor finally specified down to constraints.

## Required transactional guarantees

| ID | Candidate rule | Evidence and negative case |
|---|---|---|
| R2-DB-001 | **Versioned ordered migrations** with checksum, author/status/dependencies, distinct DDL vs runtime account | Fresh install, resumability, tampering, concurrent migrators |
| R2-DB-002 | Exactly one `fp_setup` row, cryptographic verifier and monotonic revision | Parallel creation, corrupt JSONB, stale version |
| R2-DB-003 | DB-enforced unique initial administrator, normalized unique email and durable accounts | Concurrent requests, duplicate email, role collision |
| R2-DB-004 | Token/attempt/grant/state updates in **one locked SQL transaction** | Replay, lost counter, rollback |
| R2-DB-005 | Atomic audit event and domain result when semantically part of same DB transaction | Crash after business update, false success audit |
| R2-DB-006 | Version/revision and row lock for setup mutations, out-of-order denial | Lost update, stale page, duplicate POST |
| R2-DB-007 | Safe retry after uncertain commit, never duplicate admin or grant forever | Same operation repeated, delayed response |
| R2-DB-008 | SQL exceptions mapped to safe domain errors, no DB credentials/secrets in logs | DB down, deadlock, timeout, malformed data |
| R2-DB-009 | Migration forward/recovery plan, never claim automatic SQL downgrade after irreversible DDL | Partial migrations, missing file, irreversibility |
| R2-DB-010 | Durable separation of bootstrap grant and permanent login session, expiry/revocation, no Hub dependency | Restart, old cookie, clock skew |
| R2-DB-011 | Encrypt MFA secret **only if MFA enabled**, recovery key outside common failure domain | Skipped MFA, key loss on restore, stale secret |
| R2-DB-012 | Do not invent tenant/hosting tables before approved FK/RBAC/retention data model | Cross-tenant reads, unsafe cascading deletes, orphans |

## Atomic scenarios and race handling

**Initial activation.** Begin transaction; lock singleton; verify proof and revision; check activation state; insert account with unique initial-admin constraint and Argon2id hash; record state transition and audit; commit; then respond. **No privileged Linux side effects inside this SQL transaction.** On failure roll back together and log only redacted technical context. MFA is a **choice**: DB constraints must not require TOTP data when owner chooses `skip`.

**Response lost after commit.** Client receives no response despite committed data. Retry must discover durable outcome without a second initial account or endlessly extended grant; specific idempotency key schema/retention remain a **contract to ratify**, not a chosen new column.

**Concurrency/double POST.** Two sessions race to create the first admin. Exactly one succeeds and the other gets a safe conflict. Test with actual PostgreSQL transaction isolation, never only the in-memory repository.

**Unavailability/crash/restore.** A backed-up bootstrap grant must not be replayable without authorization after restore. Restoring account/permissions requires accessible protected recovery keys. Never mark encrypted archives recoverable after losing the only key; full Q166 each-backup isolated restore remains a separate R4 gate.

## Unratified implementation parameters

- **Actual DDL, migrations and extensions:** review original SRC-03 and obtain Database approval before changes.
- **Concurrency:** choose isolation level, deadlock/retry policy, possible advisory locks, grant TTL/attempt thresholds, retention and idempotency schema using actual tests. No numeric defaults introduced here.
- **Hosting:** organization/tenant/site/account/quota/revision data model requires separate contract and migrations; do not invent columns.
- **Maintenance:** DDL/migration and backup identities distinct from Symfony runtime, never from HTTP, generic privileged shell or Hub.

## Evidence matrix

See [`R2-DB-TEST-001` through `R2-DB-TEST-010`](../13-tests-quality/r2-integration-gates.md). All are **PLANNED**. Historical PHP in-memory tests and PostgreSQL `SKIP` cannot validate real concurrency, rollback or recovery. Gate: obtain original ZIP → review/adapt contracts → boot Symfony + authorized PG test DB → actual concurrent/integration SQL tests on named SHA → API/Security review and FR/EN update.

[Issue #3](https://github.com/yyogas/forgepanel/issues/3) · [Gap register](../00-project-control/documentation-readiness.md). Closing `DOC-GAP-004` requires approved data model and SQL evidence; this document is insufficient.
