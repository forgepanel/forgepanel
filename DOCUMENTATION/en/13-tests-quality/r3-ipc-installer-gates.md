<!-- forgepanel-doc id=FP-13-R3-IPC-INSTALL-QA revision=1 status=specified -->
# R3 — Typed IPC and secure installer test matrix

[Français](../../fr/13-tests-quality/r3-ipc-installer-gates.md) · [Quality](README.md) · [IPC contract](../08-api-contracts/symfony-go-ipc-r3.md) · [Installer](../14-devops-releases/installer-lifecycle-r3.md)

**All 24 cases are `PLANNED`; no real functional PASS.** Static Python tests only validate IDs and candidate JSON artifacts; **they open no IPC socket, change no Linux configuration and start no VM**. Privileged actions remain `BLOCKED_UNTIL_QUALIFIED`. Real execution requires genuine SRC-03 Foundation source, tested Symfony/PostgreSQL, reviewed secure agent and authorized disposable VM.

## A. Symfony ↔ Go IPC — 12 positive/negative scenarios

| Test ID | Area | Positive path | Denial/failure path | Status |
|---|---|---|---|---|
| `R3-IPC-TEST-001` | Peer authentication | Validated IPC peer identity | Deny spoofed/missing peer or forged actor claim | **PLANNED** |
| `R3-IPC-TEST-002` | RBAC and tenant | Operation allowed for proven actor/resource | Deny cross-tenant, missing permission and Hub-as-root | **PLANNED** |
| `R3-IPC-TEST-003` | Closed operation set | Named ACT-FP action with typed payload | Reject shell.exec, command, argv and unknown fields | **PLANNED** |
| `R3-IPC-TEST-004` | Contract compatibility | Supported and negotiated contract version | Incompatible version/old payload is denied | **PLANNED** |
| `R3-IPC-TEST-005` | Idempotency | Same key and digest returns previous job | Same key with different payload = IDEMPOTENCY_CONFLICT | **PLANNED** |
| `R3-IPC-TEST-006` | Lost ACK | Read durable job after committed intent | No second activation after lost reply | **PLANNED** |
| `R3-IPC-TEST-007` | Revisions and lock | Current revision and owned resource lock | Deny stale revision, concurrent writer, expired lease | **PLANNED** |
| `R3-IPC-TEST-008` | Timeout and retry | Transient failure retried within approved policy | Never blind-replay irreversible timed-out action | **PLANNED** |
| `R3-IPC-TEST-009` | Agent crash | Recover desired/observed state after restart | No SUCCESS without observed VERIFY evidence | **PLANNED** |
| `R3-IPC-TEST-010` | Redaction | Correlated timestamped audit without secrets | Deny cookies/tokens/DB credential disclosure | **PLANNED** |
| `R3-IPC-TEST-011` | Authorized signed plans | Plan and permissions rechecked at effect time | Deny changed plan or expired approval | **PLANNED** |
| `R3-IPC-TEST-012` | Hub outage | Core continues without Hub | Deny Hub privileged endpoint and required Hub availability | **PLANNED** |

## B. Trusted installation — 12 positive/negative scenarios

| Test ID | Area | Positive path | Denial/failure path | Status |
|---|---|---|---|---|
| `R3-INSTALL-TEST-001` | Signature trust | Signed release metadata and exact artifact bytes | Deny unknown root, tampered bytes and revoked key | **PLANNED** |
| `R3-INSTALL-TEST-002` | Freshness/replay | Current authorized anti-rollback metadata | Deny stale channel, replay and expiry | **PLANNED** |
| `R3-INSTALL-TEST-003` | OS compatibility | OS/version/arch preflight on authorized VM | Deny unqualified OS without auto-selection | **PLANNED** |
| `R3-INSTALL-TEST-004` | Existing services | Inventory plus approved adoption plan | Never overwrite unmanaged file, listener or account | **PLANNED** |
| `R3-INSTALL-TEST-005` | Snapshot and backup | Checkpoint and recovery key accessible | Deny APPLY without verified required backup | **PLANNED** |
| `R3-INSTALL-TEST-006` | APPLY authorization | Typed action on current approved plan | Deny generic root shell, expired plan, foreign tenant | **PLANNED** |
| `R3-INSTALL-TEST-007` | Packages and interruption | Staging and idempotent recovery | Network/disk failure never yields fake success | **PLANNED** |
| `R3-INSTALL-TEST-008` | Health and HTTPS | Panel, DB, agent, TLS and admin path verified | Service active but portal unavailable = FAIL | **PLANNED** |
| `R3-INSTALL-TEST-009` | Port and firewall | Admin remains reachable after networking change | Lost last admin path is a critical veto | **PLANNED** |
| `R3-INSTALL-TEST-010` | Safe compensation | Restore only known reversible steps | Irreversible SQL DDL is never falsely rolled back | **PLANNED** |
| `R3-INSTALL-TEST-011` | Upgrades/recovery | Reinstall/upgrade and restart covered | Crash after apply requires RECOVER or observed proof | **PLANNED** |
| `R3-INSTALL-TEST-012` | Release evidence | Exact signed VM evidence before promotion | SKIP, fixtures and docs-only checks never equal PASS | **PLANNED** |

## Evidence required for any future executed campaign

Each executed test must record: ID, tested commit SHA, source/signed digest evidence, OS/architecture/version, WebStack profile when relevant, PHP/Go/Symfony/PostgreSQL versions, policy/revision/idempotency, pseudonymized authenticated peer/actor/tenant, installer step/plan, redacted logs, **observed Linux effects**, positive and negative actual/expected results, recovery/cleanup, reviewer and `PASS/FAIL/BLOCKED/SKIP`.

**Separate these layers:** parser unit tests, actual peer-authenticated Unix socket integration, transactional PostgreSQL concurrency, agent failure and restart, disposable OS VM with systemd/fs/AppArmor or SELinux, real HTTPS/rollback, and regression tests. Container and document checks cannot replace full OS VMs. Do not invent commercial CPU/RAM/TTL limits; actual test policy must be explicitly approved.

## Dependency and owner gates

**R1:** genuine verified/licensed source (issue #2). **R2:** real Symfony/PG with optional MFA (issues #3 and #6). **R3:** ratified authenticated IPC, durable job model, minimal Linux accounts, signed packages and installer, comparative VM tests and Q132 hard security vetoes. **R4:** real first PHP/HTTPS site, scoped SFTP and isolated restoration; later gates remain open. Private Hub can never initiate an arbitrary root action.

**Documentation-only progress:** [candidate IPC contracts](../08-api-contracts/symfony-go-ipc-r3.md), [installer state machine](../14-devops-releases/installer-lifecycle-r3.md) and [typed action register](../../evidence/typed-agent-operations-v1.json) now share IDs. Do not close `DOC-GAP-005` or `DOC-GAP-006` without ratification, source implementation and real test evidence. Q1–Q170 unchanged; Q171+ unanswered.
