<!-- forgepanel-doc id=FP-13-R2-GATES revision=1 status=specified -->
# R2 — Symfony, identity and PostgreSQL integration test matrix

[Français](../../fr/13-tests-quality/r2-integration-gates.md) · [Quality](README.md) · [Identity](../03-core/bootstrap-identity-r2.md) · [Transactions](../09-database/setup-transaction-r2.md)

**Status: all 20 cases `PLANNED`; 0 real HTTP/SQL integration tests verified in this lot.** The historical in-memory prototype tests and green documentation CI cannot demonstrate a booted Symfony stack, connected PostgreSQL or real recovery. Original SRC-03 Foundation archive remains unavailable. This is a **candidate test plan**, not an implementation verdict. Q1–Q170 preserved and admin MFA optional.

## Campaign A — Authentication and HTTP security

| Test ID | Contract | Positive scenario | Negative/denial scenario | State |
|---|---|---|---|---|
| `R2-AUTH-001` | Initial account and skipped MFA | Wizard completes without TOTP; permanent login after commit | Reject TOTP-required field when skipped | **PLANNED** |
| `R2-AUTH-002` | Enabled MFA enrollment | TOTP proof and protected recovery | Invalid/replayed TOTP cannot advance | **PLANNED** |
| `R2-AUTH-003` | Expired/replayed bootstrap token | Valid token exchanged once | Nonenumerating bounded denial for expired/consumed | **PLANNED** |
| `R2-AUTH-004` | CSRF/Host/Origin/proxy | Trusted origin and valid CSRF | Deny spoofed Host, untrusted proxy, absent CSRF | **PLANNED** |
| `R2-AUTH-005` | Concurrent first-admin creation | Exactly one durable initial account | Concurrent attempts cannot create duplicate initial admins | **PLANNED** |
| `R2-AUTH-006` | Lost response after commit | Read committed outcome and resume without duplication | Retry must not extend grant indefinitely | **PLANNED** |
| `R2-AUTH-007` | Resume and grant revocation | New authorized grant with old revoked | Old grant/revision denied | **PLANNED** |
| `R2-AUTH-008` | Permanent session lifecycle | Rotation on login/logout and server expiration | Reject fixation, non-Secure cookie and bootstrap-session reuse | **PLANNED** |
| `R2-AUTH-009` | Org/site scope authorization | Authorized website manager only for owned sites | Deny cross-tenant/API out-of-role/generic shell | **PLANNED** |
| `R2-AUTH-010` | Lost admin access and Hub outage | Authorized audited local recovery without Hub | Deny weak proof, public root endpoint, admin deletion | **PLANNED** |

**Campaign A preconditions:** genuine Foundation source imported and reviewed; Composer lock audited with Symfony actually booted, test hosts/secrets, local HTTPS test origin, browser cookies/CSRF and dedicated PostgreSQL. A case is PASS only when both positive **and** negative paths are observed with redacted logs.

## Campaign B — PostgreSQL transactions and recovery

| Test ID | Contract | Positive scenario | Negative/denial scenario | State |
|---|---|---|---|---|
| `R2-DB-TEST-001` | Fresh installation | Apply migration in dedicated test PostgreSQL | Deny modified or invalid migration | **PLANNED** |
| `R2-DB-TEST-002` | Concurrent migrations | One migration holds lock | Deny duplicate DDL/partial table | **PLANNED** |
| `R2-DB-TEST-003` | Setup singleton | Single setup row with valid revision | Reject second singleton and stale revision | **PLANNED** |
| `R2-DB-TEST-004` | Initial administrator uniqueness | One initial admin after concurrent transactions | DB rejects second `initial_admin=true` | **PLANNED** |
| `R2-DB-TEST-005` | Proof/state/audit rollback | Atomic success + audit commit | Forced exception leaves no grant or fake success audit | **PLANNED** |
| `R2-DB-TEST-006` | Persistent invalid attempts | Attempt counter and limits persist | Rollback must not reset deliberate lockout | **PLANNED** |
| `R2-DB-TEST-007` | Lost response/idempotency | Retry recognizes committed transition | No duplicated admin/grant | **PLANNED** |
| `R2-DB-TEST-008` | Crash/restart/concurrency | Durable state recovered correctly | Deadlock/interruption/missing DB produce safe error | **PLANNED** |
| `R2-DB-TEST-009` | Skipped MFA/secret persistence | No TOTP secret on skip; encrypted if enabled | No secret leak in DB logs/exports/HTTP | **PLANNED** |
| `R2-DB-TEST-010` | Restore and recovery-key loss | Consistent SQL/identity restore when key available | Without key, recoverability fails explicitly | **PLANNED** |

**Campaign B preconditions:** separate migrator and application DB identities, authorized disposable PostgreSQL test database, versioned/checksummed migrations, known transaction isolation and controlled restoration points. Corruption/interruption scenarios run **only on authorized disposable environments**, not customer or production hosts.

## Mandatory evidence for each case

An actual test report must include **commit SHA, OS/PHP/Symfony/PostgreSQL versions, migration ID/checksum, test ID, actor/tenant, prerequisites, command/HTTP, observed/expected result, error code, transactional state, correlation, redacted logs, cleanup and `PASS/FAIL/BLOCKED/SKIP`**. With no actual database, use `SKIP`, never `PASS`. Performance thresholds and commercial settings are still open; never invent values.

## Review and dependency gates

1. **R1 blocked:** recover genuine SRC-03 archive (issue #2), provenance and optional-MFA fix of historical mandatory path.
2. **R2 candidates:** ratify schemas/contracts, then boot Symfony + PostgreSQL with local identity and optional MFA.
3. **Execute all 20 cases**, including rollback, concurrency and uncertain commit, and attach exact commit/OS evidence.
4. Database, Security and API/IPC own schema/recovery/endpoint changes.
5. Free Core remains autonomous without Hub; no generic `shell.exec`, privileged install or `stable/main/production` promotion without further qualification.

[Identity issue #6](https://github.com/yyogas/forgepanel/issues/6) · [Symfony/PG issue #3](https://github.com/yyogas/forgepanel/issues/3) · [`DOC-GAP-002`–`DOC-GAP-004`](../00-project-control/documentation-readiness.md). Completion needs evidence and review; this plan closes no issue.
