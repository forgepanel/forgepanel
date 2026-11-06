<!-- forgepanel-doc id=FP-13-R3-PHYSICAL-QA revision=1 status=specified -->
# R3 — PostgreSQL physical model, Linux identities and typed execution QA gates

[Français](../../fr/13-tests-quality/r3-physical-execution-gates.md) · [QA](README.md) · [DB model](../09-database/physical-jobs-model-r3.md) · [Linux identities](../14-devops-releases/linux-service-identities-r3.md) · [Typed execution](../08-api-contracts/typed-execution-recovery-r3.md)

**All 36 scenarios are `PLANNED`. No actual SQL, IPC, Linux mutation or VM test ran in this lot.** GitHub CI Python checks only candidate text/JSON consistency, not PostgreSQL concurrency or independent system security. Owner Q1–Q170 preserved, Q171+ unanswered.

## A. Proposed PostgreSQL physical jobs — 12 tests

| Test | Area | Positive path | Denial/failure | Status |
|---|---|---|---|---|
| `R3-PHYS-TEST-001` | Concurrent admission | One intent/job after concurrent matching requests | Duplicate inserts never create second APPLY | **PLANNED** |
| `R3-PHYS-TEST-002` | Key/digest collision | Same key/digest returns original job | Same key changed payload -> IDEMPOTENCY_CONFLICT | **PLANNED** |
| `R3-PHYS-TEST-003` | Tenant scope | Explicit server and tenant scopes | Null/wildcard and cross-tenant rejected | **PLANNED** |
| `R3-PHYS-TEST-004` | Commit-before-ACK | Atomic intent/job/audit/outbox | Failed commit cannot emit ACCEPTED | **PLANNED** |
| `R3-PHYS-TEST-005` | Resource lease uniqueness | One scoped resource lease generation | Two writers cannot own same resource lease | **PLANNED** |
| `R3-PHYS-TEST-006` | Stale fencing | Current worker validated at effect boundary | Stale worker rejected despite SQL lease expiry | **PLANNED** |
| `R3-PHYS-TEST-007` | Success transition | VERIFYING and observed effect precede SUCCEEDED | Unobserved QUEUED/RUNNING success denied | **PLANNED** |
| `R3-PHYS-TEST-008` | Duplicate outbox | Consumer deduplicates delivery retry | Lost ACK causes no new Linux effect | **PLANNED** |
| `R3-PHYS-TEST-009` | Deadlock and outage | Short transaction and bounded conflict handling | Mixed DDL/runtime and long SQL lock rejected | **PLANNED** |
| `R3-PHYS-TEST-010` | Redacted audit | Correlated append-only step journal | No credentials/cookies/tokens logged | **PLANNED** |
| `R3-PHYS-TEST-011` | Irreversible rollback | Restore only proven reversible step | Irreversible SQL DDL never falsely rolled back | **PLANNED** |
| `R3-PHYS-TEST-012` | Restored job state | Reconcile jobs/leases after PostgreSQL restore | Old credentials/replays invalidated before APPLY | **PLANNED** |

## B. Linux users and system services — 12 tests

| Test | Area | Positive path | Denial/failure | Status |
|---|---|---|---|---|
| `R3-LINUX-TEST-001` | Nondestructive inventory | Detect existing UID/GID/service without mutation | Account/group collision refused | **PLANNED** |
| `R3-LINUX-TEST-002` | Tenant versus panel | Tenant PHP-FPM isolated from Core service | Tenant cannot read socket or panel secrets | **PLANNED** |
| `R3-LINUX-TEST-003` | Isolated IPC bridge | Dedicated bridge identity with scoped access | Compromised web/plugin cannot impersonate bridge | **PLANNED** |
| `R3-LINUX-TEST-004` | Nonroot Go agent | Go validates peer and operation as nonroot | CAP_SYS_ADMIN, sudo and generic shell denied | **PLANNED** |
| `R3-LINUX-TEST-005` | Disabled privileged handler | Handler absent/disabled by default | ACT-FP-0005/0007 never enabled automatically | **PLANNED** |
| `R3-LINUX-TEST-006` | DDL versus runtime | Migrator role separate from runtime SQL | Runtime cannot own tables or execute DDL | **PLANNED** |
| `R3-LINUX-TEST-007` | Protected socket | Private runtime dir owner/type/mode checked | Symlink/replaced inode/shared group denied | **PLANNED** |
| `R3-LINUX-TEST-008` | Peer UID and mandate | Kernel UID AND actor mandate/scope rechecked | Valid UID alone grants no business authorization | **PLANNED** |
| `R3-LINUX-TEST-009` | systemd/LSM profile | OS-tested hardening preserves safe access | Profile breaking socket/recovery denied | **PLANNED** |
| `R3-LINUX-TEST-010` | Handler-side fencing | Handler rechecks fence/revision at effect | Stale worker/plan cannot mutate Linux | **PLANNED** |
| `R3-LINUX-TEST-011` | Rotation and restart | Reconnect only on fresh approved identity | Old FD/session/certificate denied | **PLANNED** |
| `R3-LINUX-TEST-012` | Uninstall safety | Remove only product-owned accounts/services | Removing tenant UID/last admin route is veto | **PLANNED** |

## C. Per-operation execution and recovery — 12 tests

| Test | Area | Positive path | Denial/failure | Status |
|---|---|---|---|---|
| `R3-EXEC-TEST-001` | Closed operation registry | Approved ACT-FP and dedicated handler | shell.exec/argv/script_path impossible | **PLANNED** |
| `R3-EXEC-TEST-002` | Peer, actor, scope | Validate peer/mandate/resource before effect | Hub license/UI admin/foreign tenant denied | **PLANNED** |
| `R3-EXEC-TEST-003` | Current plan digest | Digest/signature/revision checked at effect time | Changed/expired plan rejected | **PLANNED** |
| `R3-EXEC-TEST-004` | Privileged action gate | Privileged handlers remain blocked | ACT-FP-0005/0007 never pass without qualification | **PLANNED** |
| `R3-EXEC-TEST-005` | Effect fencing | Handler checks lock and generation at effect | Stale worker/race cannot perform second APPLY | **PLANNED** |
| `R3-EXEC-TEST-006` | Nondestructive planning | Plan and diff without Linux mutation | Unmanaged port/unknown package denies | **PLANNED** |
| `R3-EXEC-TEST-007` | Backup and authorization | Verify backup/approval/digest before APPLY | Missing backup/unavailable key blocks | **PLANNED** |
| `R3-EXEC-TEST-008` | Actual verification | Functional health and observed effect before success | Zero exit/active service cannot imply success | **PLANNED** |
| `R3-EXEC-TEST-009` | Lost ACK/crash | Recover by reconciling PG and Linux state | Uncertain APPLY never blind-replayed | **PLANNED** |
| `R3-EXEC-TEST-010` | Safe compensation | Verified reversible checkpoint only | SQL DDL/lost key not a full rollback | **PLANNED** |
| `R3-EXEC-TEST-011` | Redacted observability | Actor/plan/effect audit without secrets | Export token or private evidence denied | **PLANNED** |
| `R3-EXEC-TEST-012` | Hub independence and qualification | Core works without Hub on tested target | Unqualified OS, Hub root and unknown version denied | **PLANNED** |

## Actual campaign prerequisites and evidence

**Required dependency order:** verify/import genuine SRC-03 source (R1) → prove Symfony/PG identity with optional administrator MFA (R2) → approve Database/API/Security contracts → verified signed packages, dedicated accounts/sockets and constrained handlers → actual authorized disposable OS VMs with system observation and recovery.

**Each executed test must record:** test ID, SHA, OS/architecture/tool versions, VM image, policy/digest, pseudonymized actor/tenant, verified peer credentials (no secrets), current role/permission, request/outbox/inbox, before/after SQL state, fencing generation, observed Linux effect, redacted logs, positive/negative result, injected failure, cleanup/recovery/rollback and `PASS/FAIL/BLOCKED/SKIP`. A written test or `SKIP` is **never PASS**.

**Q132 hard vetoes:** cross-tenant exposure, port collision, loss of last admin route, generic root execution, promised-but-impossible recovery and false success after crash. Never invent numerical TTL, timeout or quota thresholds. Public Core remains functional without Hub and `ACT-FP-0005/0007` privileged operations remain **blocked**. `DOC-GAP-004/005/006` remain **OPEN** pending specialized reviews and real test evidence.
