<!-- forgepanel-doc id=FP-13-R2-POSTGRES revision=1 status=specified -->
# R2 — Disposable real-PostgreSQL integration candidate

[Français](../../fr/13-tests-quality/r2-postgres-execution.md) · [R2 master plan](r2-integration-gates.md) · [R1 source import](../12-development/foundation-v07-source-import.md)

## Goal and source prerequisites

Exercise the **actual PostgreSQL transaction authority** from Foundation v0.7 with the separately proposed **optional-admin-MFA v0.7.1 patch**, without running on an operator/customer database. This is a stacked draft implementation on top of the R1 v0.7 source PR and the v0.7.1 patch PR. Source import, migration/legal/security review and the complete R2 gate are **not approved by this change**.

The CI workflow `.github/workflows/r2-postgres-disposable.yml` provisions a disposable PostgreSQL 16 **test-only** service on GitHub's ephemeral `ubuntu-24.04` runner, installs PHP `pdo_pgsql` and runs two independent PHP test scripts. No SSH/root shell, installed daemon or customer services are invoked. The original 001/002 SQL migrations and the already-imported PDO/SetupService are used without modification. Docker is used by the **CI runner only** and does **not** create a Docker dependency for ForgePanel Core.

## Real SQL test cases

| Reference | Actual assertion | Evidence required |
|---|---|---|
| R2-DB-TEST-001 (partial) | Apply `001_setup.sql` then `002_optional_admin_mfa.sql` in isolated random test schema | Actual DB, migration files and cleanup |
| R2-DB-TEST-003 (partial) | Exactly one setup singleton, durable state across two connections | Committed SQL state |
| R2-DB-TEST-004 (partial) | DB-enforced unique initial administrator | Reject a second `initial_admin=true` insert |
| R2-DB-TEST-005 (partial) | Existing smoke test injects audit failure and checks rolled-back admin and token | Real PostgreSQL trigger/transaction |
| R2-DB-TEST-006 (partial) | Failed proof attempt persists and can be observed from another connection | Durable attempts |
| R2-DB-TEST-007 (partial) | Reuse of committed one-time bootstrap token and stale revision denied | No second admin |
| R2-DB-TEST-008 (partial) | Row lock conflict returns bounded `55P03`, rollback leaves token usable | Two real SQL sessions |
| R2-DB-TEST-009 (partial) | Explicit MFA skip removes pending secret and recovery hashes, audit retained | Nullable column, state and audit |

The original `tests/postgres.php` also checks **TOTP enabled**, successful configuration and a simulated transaction failure. The new script explicitly checks the **MFA skip** path introduced in v0.7.1. A PASS establishes only the listed observed SQL assertions, not complete R2 compliance. A skipped test (exit 77) is never a PASS. No actual PR/CI result is asserted by this candidate document until the job succeeds.

## Hard safety gates

- Refuse if no `pdo_pgsql`, no `FORGE_TEST_ALLOW_SCHEMA_CREATE=1`, no explicit `FORGE_TEST_PG_DSN` or target database name that does not end with `_test`.
- Create a random, isolated schema; clean up in `finally` after rolling back open transactions. No production database credentials, live data, secret stores, privileged local Linux changes or developer-machine default credentials.
- Distinguish a bounded row-lock timeout from two simultaneously successful registrations. Full independent worker races, crash during commit, restored PG, migration ledger, genuine least-privilege migrator/runtime roles and encrypted-backup recovery remain **NOT RUN** and require Database/Security/QA review.
- Production `install apply` remains unavailable. Core works without Hub; optional admin MFA remains the product direction.
- GitHub's public repository and workflow logs must not contain real connection passwords or client data: the CI credential is a conspicuous test-only placeholder scoped to an ephemeral local PostgreSQL service.

## Next independent gates

Resolve and pin Composer/Symfony dependencies with auditable `composer.lock`; boot real Symfony HTTP with allowed origin/Host/CSRF, access controls, fresh bootstrap session and the permanent login contract. Execute the remaining R2 database/concurrency/restart/restore test matrix in independent approved environments. Do not mark the complete 20-case R2 matrix PASS based on this limited subset.