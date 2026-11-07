<!-- forgepanel-doc id=FP-13-R2-GATES revision=3 status=specified -->
# R2 — Symfony, identity and PostgreSQL integration test matrix

[Français](../../fr/13-tests-quality/r2-integration-gates.md) · [Quality](README.md) · [Identity](../03-core/bootstrap-identity-r2.md) · [Transactions](../09-database/setup-transaction-r2.md)

**Status: PARTIAL R2 EVIDENCE — 20 full acceptance cases remain `PLANNED`.** Real disposable PostgreSQL tests and a Symfony HttpKernel smoke suite have now passed on draft feature branches; neither covers every positive/negative scenario in the 20-case matrix. The genuine SRC-03 archive was recovered, but its source import (#59) and the optional-admin-MFA patch (#60) remain unmerged and under review. This matrix retains its full acceptance requirements rather than silently upgrading incomplete cases to PASS. Q1–Q220 owner directions, optional admin MFA and Hub independence remain in force.

**Additional verified partial R2 identity subset (not full case acceptance):** [draft PR #63](https://github.com/yyogas/forgepanel/pull/63), code commit `97cfbf73100b237b8781e9c34bb0038ce7ccc1e4`, [CI #42389514939](https://github.com/yyogas/forgepanel/actions/runs/42389514939): **29 real PostgreSQL assertions**, **31 real Symfony HttpKernel/SQL assertions**, two green runs. Covers password verification, optional MFA, replay/recovery, CSRF, session rotation/expiry, forbidden read-only mutations and logout. **Does not establish a permanent production login, full Symfony Security role system, browser cookies, HTTPS gateway or the entire R2 test matrix.** [Detailed FR/EN evidence](r2-admin-readonly-qa.md).

## Verified partial evidence from draft branches — 2026-11-07

| Subset | Named Git commit and successful CI | What passed | What is *not* established |
|---|---|---|---|
| PostgreSQL / PDO | [`66447a0ef88e`](https://github.com/yyogas/forgepanel/commit/66447a0ef88e323411ad14edfa9b80cd550c955f), [CI #42383929498](https://github.com/yyogas/forgepanel/actions/runs/42383929498), [draft PR #61](https://github.com/yyogas/forgepanel/pull/61) | PostgreSQL **16.15**, PHP **8.3.6**, migrations `001_setup.sql` + `002_optional_admin_mfa.sql` in an ephemeral `*_test` database; **23 live assertions**, row-lock timeout, single-admin constraint, rollback, MFA skip and state/replay checks | Full concurrent competing HTTP registrations, separate DB roles, crash/restart and restore tests |
| Symfony HttpKernel | [`d34dba52405c`](https://github.com/yyogas/forgepanel/commit/d34dba52405c7cb7b450da989c3e8977ae8e0332), [CI #42385350165](https://github.com/yyogas/forgepanel/actions/runs/42385350165), [draft PR #62](https://github.com/yyogas/forgepanel/pull/62) | Symfony **7.4** kernel/container/routes, locked **47-package** Composer dependency install, `composer audit --locked` (no advisories reported), **12 HTTP-kernel assertions** checking HTTPS origin, Host/port, methods, Origin, request size, absent CSRF, security headers | Real HTTPS gateway, full browser sessions, positive authenticated CSRF workflow, permanent login, recovery or deployable installation |

**Evidence boundaries:** these successful subsets are **VERIFIED on the named draft commits**, not `R2 COMPLETE`, not release/production or a certification of supported OS/WebStack combinations. The absent-CSRF check observed a denial (HTTP 401 or 403) pending permanent-authentication semantics. A passing static check, CI upload or Composer audit is not an independent security review. Both PRs are stacked behind source PR #59 and optional-MFA PR #60. [R2 PostgreSQL details](r2-postgres-execution.md) · [Symfony HTTP details](r2-symfony-http-smoke.md).



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

1. **R1 source import remains unmerged:** the genuine SRC-03 archive has been recovered and source is in [draft PR #59](https://github.com/yyogas/forgepanel/pull/59), with the optional-admin-MFA patch in [draft PR #60](https://github.com/yyogas/forgepanel/pull/60). Independent security/licensing review is still required.
2. **R2 candidates:** ratify schemas/contracts, then boot Symfony + PostgreSQL with local identity and optional MFA.
3. **Execute all 20 cases**, including rollback, concurrency and uncertain commit, and attach exact commit/OS evidence.
4. Database, Security and API/IPC own schema/recovery/endpoint changes.
5. Free Core remains autonomous without Hub; no generic `shell.exec`, privileged install or `stable/main/production` promotion without further qualification.

[Identity issue #6](https://github.com/yyogas/forgepanel/issues/6) · [Symfony/PG issue #3](https://github.com/yyogas/forgepanel/issues/3) · [`DOC-GAP-002`–`DOC-GAP-004`](../00-project-control/documentation-readiness.md). Completion needs evidence and review; this plan closes no issue.
