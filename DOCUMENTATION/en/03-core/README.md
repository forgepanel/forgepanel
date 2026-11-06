<!-- forgepanel-doc id=FP-03 revision=4 status=documented -->
# Core and bootstrap

[Français](../../fr/03-core/README.md) · [Index](../README.md)

## Current core evidence

SRC-03 contains `cmd/forgepanel` and `internal/{doctor,installer,panelbridge,releases,bootstrap}`. These are prototype packages, not a complete long-running kernel or native module registry. The historical `internal/bootstrap` file store remains tested but is not connected to web activation.

Web setup uses `SetupService`, `SetupRepository` and `SetupTransaction`. PostgreSQL owns the token verifier, initial administrator and setup state in one transaction. `NEW → TOKEN_ISSUED → MFA_PENDING → CONFIGURING → REVIEWED` describes the actual phase names. `REVIEWED` means a stored draft; it never means installed or production-ready.

## Security and failure semantics

The source generates 32-byte random bootstrap secrets, stores SHA-256 verifiers, expires tokens after 900 seconds and locks token attempts after five failures. Setup grants last 1800 seconds. The external v0.7 prototype creates a pending-MFA administrator and requires TOTP before configuration. **This requirement is now superseded**: the wizard must offer both “enable MFA” and “continue without MFA”, then enter CONFIGURING either way. The external v0.7 source is not yet imported or fixed. Local resume revokes the old grant and issues a new one-use code; it is not a permanent administrator login.

The SQL implementation locks `fp_setup` and writes account/state/audit together. Invalid attempts must persist; infrastructure errors roll back. The in-memory tests do not prove PostgreSQL concurrency or lost-response recovery. Client retries after an uncertain commit need explicit integration tests before exposure.

## First-release roles (Q124 B)

The verified initial flow must provide permanent local administrator login with recovery and a **website-manager** role restricted to its authorized resources. Linux root remains separate from application Super Administrator. Administrator MFA is **optional**; skipping TOTP enrollment cannot block the wizard. Sessions, CSRF, API/agent enforcement and cross-tenant denial need real Symfony/PG integration testing. [Qualification](../00-project-control/mvp-qualification.md). These remain release criteria, not operating features.

## Target kernel contracts

Startup must validate configuration and dependencies, recover durable operations, register capabilities, then become ready. Shutdown stops admission, checkpoints safe operations and releases leases only after durable state. Readiness must distinguish panel, database and agent health. No plugin may be required to initialize authorization or recovery.

Future jobs require correlation and idempotency keys, resource locks, bounded retries, failure classification and compensating actions. Reconciliation compares desired and observed state without overwriting administrator-owned files. Module registration must reject dependency cycles and incompatible contract versions. These mechanisms are specified requirements, not archive functionality.

[Component records](../04-modules/components.md) · [Database](../09-database/README.md) · [Operations](../15-operations/README.md)

## R2 — Detailed identity and bootstrap contract (candidate)

[Candidate R2 identity/session/optional-MFA contract](bootstrap-identity-r2.md) separates historical SRC-03 states, durable administrator, bootstrap grants, recovery and session scope. It defines `R2-ID-001`–`R2-ID-012`; endpoint schemas, durations and recovery policies still require Security/API/Database review and real tests. **No Symfony runtime or historical MFA patch is imported** by this document.

## Core — Durable intent and isolated IPC bridge (candidate)

Future Core mutations require a [PostgreSQL durable job ledger](../09-database/durable-jobs-r3.md) and an [authenticated Symfony ↔ Go peer channel](../08-api-contracts/local-peer-trust-r3.md). Symfony UI cannot grant root; the bridge must isolate tenant/plugin code while Go revalidates scope/permissions. HTTP/ACK success never proves Linux mutation and a stale worker must fail its fencing check. [PLANNED tests](../13-tests-quality/r3-jobs-peer-gates.md). No daemon, socket or final physical SQL model is shipped by these documents.
