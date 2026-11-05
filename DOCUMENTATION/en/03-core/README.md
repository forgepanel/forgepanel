<!-- forgepanel-doc id=FP-03 revision=1 status=documented -->
# Core and bootstrap

[Français](../../fr/03-core/README.md) · [Index](../README.md)

## Current core evidence

SRC-03 contains `cmd/forgepanel` and `internal/{doctor,installer,panelbridge,releases,bootstrap}`. These are prototype packages, not a complete long-running kernel or native module registry. The historical `internal/bootstrap` file store remains tested but is not connected to web activation.

Web setup uses `SetupService`, `SetupRepository` and `SetupTransaction`. PostgreSQL owns the token verifier, initial administrator and setup state in one transaction. `NEW → TOKEN_ISSUED → MFA_PENDING → CONFIGURING → REVIEWED` describes the actual phase names. `REVIEWED` means a stored draft; it never means installed or production-ready.

## Security and failure semantics

The source generates 32-byte random bootstrap secrets, stores SHA-256 verifiers, expires tokens after 900 seconds and locks token attempts after five failures. Setup grants last 1800 seconds. The external v0.7 prototype creates a pending-MFA administrator and requires TOTP before configuration. **This requirement is now superseded**: the wizard must offer both “enable MFA” and “continue without MFA”, then enter CONFIGURING either way. The external v0.7 source is not yet imported or fixed. Local resume revokes the old grant and issues a new one-use code; it is not a permanent administrator login.

The SQL implementation locks `fp_setup` and writes account/state/audit together. Invalid attempts must persist; infrastructure errors roll back. The in-memory tests do not prove PostgreSQL concurrency or lost-response recovery. Client retries after an uncertain commit need explicit integration tests before exposure.

## Target kernel contracts

Startup must validate configuration and dependencies, recover durable operations, register capabilities, then become ready. Shutdown stops admission, checkpoints safe operations and releases leases only after durable state. Readiness must distinguish panel, database and agent health. No plugin may be required to initialize authorization or recovery.

Future jobs require correlation and idempotency keys, resource locks, bounded retries, failure classification and compensating actions. Reconciliation compares desired and observed state without overwriting administrator-owned files. Module registration must reject dependency cycles and incompatible contract versions. These mechanisms are specified requirements, not archive functionality.

[Component records](../04-modules/components.md) · [Database](../09-database/README.md) · [Operations](../15-operations/README.md)
