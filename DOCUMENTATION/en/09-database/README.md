<!-- forgepanel-doc id=FP-09 revision=2 status=documented -->
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

## Migration and ownership requirements

The SQL file is not applied per HTTP request. No complete migration runner or upgrade/rollback framework is provided. Future packages must separate a migration role from the non-DDL runtime role, track applied migration IDs/checksums and prevent concurrent migrators. Test fresh install and upgrade from each supported source revision. Destructive migrations require backups, retention decisions and a forward/recovery plan; a code downgrade is not an automatic data rollback.

Secrets require both database and encryption-key recovery. Do not store the encryption key in the same publicly readable backup as encrypted MFA data. Audit retention, deletion policy, customer schema and tenant-enforced query boundaries remain to be specified before hosting features are added.

## Required evidence

Run the supplied PostgreSQL test only against an explicitly authorized dedicated `_test` database. It covers a forced rollback and persistence, not every concurrency/failure mode. Add simultaneous activation, lost response after commit, database restart, stale configuration revision and restore/key-loss scenarios. No PDO PostgreSQL driver/server was available for this audit; in-memory tests are not SQL integration tests.

[Core](../03-core/README.md) · [Quality](../13-tests-quality/README.md)
