<!-- forgepanel-doc id=FP-13-R3-JOBS-PEER-QA revision=1 status=specified -->
# R3 — Durable job and local IPC peer security QA matrix

[Français](../../fr/13-tests-quality/r3-jobs-peer-gates.md) · [QA](README.md) · [Durable jobs](../09-database/durable-jobs-r3.md) · [Peer identity](../08-api-contracts/local-peer-trust-r3.md)

**Status: 24 `PLANNED` cases and zero integrated `PASS` results.** These are positive/negative test plans, **not executed PHP/Go/PostgreSQL tests**. Candidate [state transition registry](../../evidence/candidate-job-transitions-v1.json), [job schema](../../evidence/candidate-job-record-v1.schema.json) and [peer observation schema](../../evidence/candidate-peer-binding-v1.schema.json) are documentation, never authentication proof.

## A. Transactions, idempotency, fencing and recovery — 12 cases

| Test ID | Area | Positive path | Denial / failure path | State |
|---|---|---|---|---|
| `R3-JOB-TEST-001` | Job identity | Same key/digest yields one durable job | Concurrent duplicate creates no second job | **PLANNED** |
| `R3-JOB-TEST-002` | Digest conflict | New key creates a distinct admitted intent | Same key/different payload yields IDEMPOTENCY_CONFLICT | **PLANNED** |
| `R3-JOB-TEST-003` | Tenant isolation | Server-side verified tenant scope | Foreign tenant cannot access job via reused key | **PLANNED** |
| `R3-JOB-TEST-004` | Commit before ACK | ACCEPTED only after durable commit | Failed commit cannot produce ACCEPTED or success | **PLANNED** |
| `R3-JOB-TEST-005` | Lost acknowledgement | Retry retrieves identical persisted job | No second APPLY after missing ACK | **PLANNED** |
| `R3-JOB-TEST-006` | Expired fencing lease | Current worker has correct fencing generation | Resumed stale worker refused before side effect | **PLANNED** |
| `R3-JOB-TEST-007` | Revision race | Mutation holds current lock and revision | Concurrent/stale APPLY must fail closed | **PLANNED** |
| `R3-JOB-TEST-008` | Uncertain external effect | Verified external effect passes VERIFYING | Crash after effect cannot replay or report SUCCEEDED | **PLANNED** |
| `R3-JOB-TEST-009` | Duplicate outbox delivery | Inbox deduplicates repeated message | Duplicate/reordered delivery causes no second effect | **PLANNED** |
| `R3-JOB-TEST-010` | Cancel/timeout | Cancellation before effect safely blocks | Timeout during APPLY cannot imply no effect | **PLANNED** |
| `R3-JOB-TEST-011` | Redacted durable audit | Transition and correlation without secrets | Logs/errors never leak DB credentials or tokens | **PLANNED** |
| `R3-JOB-TEST-012` | PostgreSQL restore/recovery | Reconcile jobs/revisions after restore | Stale grants/replay or lost keys cannot yield PASS | **PLANNED** |

## B. Private Symfony ↔ Go IPC peer identity — 12 cases

| Test ID | Area | Positive path | Denial / failure path | State |
|---|---|---|---|---|
| `R3-PEER-TEST-001` | Isolated IPC bridge | Dedicated bridge accesses authorized private channel | Tenant PHP cannot connect to privileged socket | **PLANNED** |
| `R3-PEER-TEST-002` | Service identity | UID/GID and process instance match policy | Shared UID alone insufficient; wrong binary denied | **PLANNED** |
| `R3-PEER-TEST-003` | Forged identity claim | Kernel-observed peer credentials validated | UID/PID provided in JSON never trusted | **PLANNED** |
| `R3-PEER-TEST-004` | Socket path safety | Private socket owner/type/inode valid | Symlink/replacement/overbroad group denied | **PLANNED** |
| `R3-PEER-TEST-005` | Actor auth | Actor mandate bound to verified Symfony session/request | Unsigned claim or unauthenticated actor denied | **PLANNED** |
| `R3-PEER-TEST-006` | Resource scope | Go independently validates tenant/resource rights | Foreign tenant site or wrong role denied | **PLANNED** |
| `R3-PEER-TEST-007` | Credential rotation/restart | Authorized reconnect with fresh identity | Old session/reused FD denied | **PLANNED** |
| `R3-PEER-TEST-008` | Replay and digest | Same request retrieves durable decision | Nonce alone, changed digest or replay denied | **PLANNED** |
| `R3-PEER-TEST-009` | Resource saturation | Approved limits and bounded queues | Too many connections/jobs cannot bypass privilege | **PLANNED** |
| `R3-PEER-TEST-010` | Broken transport | Durable state recoverable after restart | IPC timeout cannot blindly retry APPLY | **PLANNED** |
| `R3-PEER-TEST-011` | Closed operation register | Known operation with validated typed input | shell.exec/raw argv and ACT-FP-0005/0007 denied | **PLANNED** |
| `R3-PEER-TEST-012` | Versioning/Hub independence | Compatible local protocol, Core works without Hub | Unknown version, Hub root and remote endpoint denied | **PLANNED** |

## Preconditions for actual future execution

**R1:** obtain/review genuine SRC-03; **R2:** real Symfony/PG/identity with optional administrator MFA; **R3:** authenticated local socket, separated bridge identity, ratified versioned protocol, Go service, reviewed durable SQL jobs/migrations, independent authorization and an authorized VM before Linux mutations. Never a generic privileged shell API. Test layers must distinguish disposable PostgreSQL transaction tests, real Linux kernel peer identity tests, HTTP/Symfony flows and bounded real Linux effects inside isolated VMs.

**Evidence per case:** commit SHA, OS/architecture/PHP-Go-Symfony-PostgreSQL versions, policy/revision, pseudonymized tenant/resource IDs, authenticated peer identity, positive/negative scenario, typed request/error, redacted traces, PostgreSQL before/after state, fencing generation, actually observed Linux effect, recovery/cleanup, security decision and `PASS/FAIL/BLOCKED/SKIP`. Missing real environment = `SKIP`, **never PASS**.

## Hard denial gates

Unix file permissions do not independently prove end-user identity. Schema-valid JSON never authorizes `ACT-FP-0005/0007`. Lease expiry does not imply no previous effect; `SUCCEEDED` without `VERIFYING` and observed evidence is invalid. Q132 tenant leakage, port collision, lost admin access and unrecoverable failure vetoes remain, regardless of performance.

**Tracking:** `DOC-GAP-004` and `DOC-GAP-006` remain **OPEN**; [issues #3](https://github.com/yyogas/forgepanel/issues/3) and [#9](https://github.com/yyogas/forgepanel/issues/9) open. Static Python document checks validate IDs/schema parity, not production code. Q1–Q170 preserved, Q171+ undecided.
