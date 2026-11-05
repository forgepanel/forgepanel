<!-- forgepanel-doc id=FP-08-R3-IPC revision=1 status=specified -->
# R3 — Candidate Symfony ↔ Go agent IPC, authorization and typed operations

[Français](../../fr/08-api-contracts/symfony-go-ipc-r3.md) · [API](README.md) · [R3 installer](../14-devops-releases/installer-lifecycle-r3.md) · [R3 QA](../13-tests-quality/r3-ipc-installer-gates.md)

**Status: SPECIFIED / CANDIDATE — no executable route, socket, daemon, privileged request or migration.** Owner: API / IPC / Contracts, subject to Security, Core, Database, DevOps and QA reviews. Requirement IDs `IPC-FP-0001`–`IPC-FP-0012` map to Q47/Q61/Q62/Q66/Q120, [DOC-GAP-005/006](../00-project-control/documentation-readiness.md), and [issues #9](https://github.com/yyogas/forgepanel/issues/9) / [#15](https://github.com/yyogas/forgepanel/issues/15). **Q1–Q170 unchanged; Q171+ unanswered.** Transport, Linux users, PostgreSQL schema, exact limits and final wire versions await ratification after the genuine SRC-03 source import (issue #2).

## Trust boundaries and ownership

```text
Untrusted browser ─HTTPS─> Symfony (sessions, CSRF, RBAC, policy/quotas)
                           ├── PostgreSQL: durable intent, job and audit (TBD)
                           └── private authenticated IPC (candidate)
                               └── nonroot Go: independently validate policy
                                   └── named bounded system operations/adapters
                                       └── Linux: least privilege and auditing
Private Hub ─ optional limited outward client ─> future Core public contracts
```

**IPC-FP-0001 — Privilege separation.** The Symfony Super Administrator is neither Linux root nor an independently privileged IPC peer. Hub, extension and webhook identities are never privileged actors by default. No browser-to-root path.

**IPC-FP-0002 — Peer authentication.** Candidate local transport is a **private Unix domain socket with independently verified peer process identity**, protected filesystem/socket access and distinct service accounts; remote agents would require mutually authenticated identity and a separately reviewed protocol. Exact Unix credentials/rotation/reconnect and remote mTLS are **open choices**. A claimed `actor_id` in Symfony's payload cannot itself prove the transport peer.

**IPC-FP-0003 — Two-level authorization.** Symfony validates actor, role, tenant/org, plan, consent/approval and resource ownership before submitting intent. Go **independently revalidates** operation, resource scope, target, policy and actual server capability. Commercial entitlements never grant Linux privileges.

**IPC-FP-0004 — Closed operation registry.** Operations exist only when present in the [candidate registry](../../evidence/typed-agent-operations-v1.json) with strict schema, permissions and negative tests. **Strictly forbidden**: `shell.exec`, `exec arbitrary command`, `run arbitrary command`, user-provided shell/scripts or raw QEMU arguments, arbitrary PHP/JS executed as root. An operation identifier can never be interpreted as an OS command.

## Candidate envelopes — require ratification

**IPC-FP-0005 — Request.** A candidate request carries `contract_version`, registry-bound `operation_id`, `request_id`, `correlation_id`, `idempotency_key`, independently checkable actor/tenant/target, `expected_revision`, `policy_revision`, `deadline`, and **per-operation typed payload**. No raw password or secret data; protected reference identifiers only. Field names and types are **candidates**, not available endpoints.

**IPC-FP-0006 — Response/errors.** Admission returns a typed `ACCEPTED`, `DENIED` or `REJECTED`; separate durable job states are `QUEUED`, `RUNNING`, `VERIFYING`, `SUCCEEDED`, `FAILED`, `COMPENSATION_REQUIRED`, `BLOCKED`. `ACCEPTED` never means that Linux changed or VERIFY passed. Candidate error taxonomy: `UNAUTHENTICATED`, `FORBIDDEN`, `SCOPE_DENIED`, `INVALID_INPUT`, `STALE_REVISION`, `IDEMPOTENCY_CONFLICT`, `RESOURCE_LOCKED`, `CAPABILITY_UNAVAILABLE`, `TRUST_FAILURE`, `TIMEOUT`, `DEPENDENCY_UNAVAILABLE`, `PARTIAL_FAILURE`, `RECOVERY_REQUIRED`. Never emit a stack trace, SQL credentials or secret to a client.

**IPC-FP-0007 — Idempotency/bounds.** Persist `(operation_id, scope, idempotency_key, payload_digest)` and policy decision before acknowledging asynchronous work. The same tuple can fetch the previous result; **same key/different payload = conflict**, not reexecution. Message sizes, deadlines, worker limits, retention, retries and lock leases are **approval-dependent parameters**. Retry only explicitly classified transient failures under strict bounds; no exactly-once guarantee across PostgreSQL and Linux.

**IPC-FP-0008 — Durable jobs and crashes.** Record each transition with request/actor, authority, contract and policy revision, target, timestamps, plan hash, step/attempt, redacted failure reason and observed effect. Restarting must reconcile incomplete jobs, not blindly replay irreversible changes. An acknowledgement lost after commit is recovered by querying the same job.

**IPC-FP-0009 — Locking/concurrency.** Operations on listeners, packages, Linux accounts, sites or services acquire scoped bounded locks and compare the resource's observed revision/ownership. Lease expiry is not permission for a new apply; reconcile desired/observed state first.

**IPC-FP-0010 — Input/output security.** Strict decoders reject unknown fields, noncanonical/symlink/TOCTOU paths, command injection, unapproved URLs/SSRF and out-of-bounds values. Unmanaged service configuration cannot be adopted/overwritten without explicit plan and consent. Redact all tokens, cookies, signing material, MFA secrets and tenant content in JSON logs.

**IPC-FP-0011 — Q47 lifecycle.** Sensitive mutations follow `DRAFT → PLAN → PREFLIGHT → SNAPSHOT → APPLY → VERIFY → COMMIT`, else `RECOVER`; an optional staging step is separate. A PostgreSQL transaction **cannot make Linux updates atomic**. A bounded agent only performs authorized actions tied to a versioned, expiring plan hash; irreversible stages require scoped approval and recovery disclosure.

**IPC-FP-0012 — Versioning/readiness.** Negotiate schema versions explicitly; incompatible versions fail closed and deprecation is announced. Liveness is not readiness: database, agent, trust keys and emergency admin access are distinct checks. Hub outages never disable free Core. Documentation does not activate any public IPC endpoint.

## Candidate typed operation cards — no privileged apply authorized

| ID | Logical operation | Class | Main prerequisite | Status |
|---|---|---|---|---|
| ACT-FP-0001 | `host.capabilities.observe` | Read only | authenticated local peer, fixed readable paths | CANDIDATE |
| ACT-FP-0002 | `artifact.signature.verify` | Read only | independent trust anchor, signed digest | CANDIDATE |
| ACT-FP-0003 | `installer.plan.compile` | Read only | validated schema/policy/OS compatibility | CANDIDATE |
| ACT-FP-0004 | `installer.stage_verified_packages` | Bounded staging | verified manifest, private directory and limits | CANDIDATE |
| ACT-FP-0005 | `installer.activate_signed_generation` | Bounded privileged, future | approved signed plan, checkpoint, lock, qualifying VM evidence | **NOT AUTHORIZED** |
| ACT-FP-0006 | `installer.health.check` | Read only | explicitly scoped service/plan identity, no tenant data | CANDIDATE |
| ACT-FP-0007 | `installer.compensate_generation` | Bounded privileged, future | safe checkpoint, independent approval for risk, audit and no irreversible action | **NOT AUTHORIZED** |

Registry entries describe *typed business actions*, **not** an implemented Go API, migration, CLI or executor. The two privileged actions are conceptual and blocked pending architecture/security approval, dedicated code and genuine VM qualification. No generic `command`, `argv`, `script_path` or `shell` wire field is allowed.

## Cross-owner handoffs and evidence

- **Database:** concrete job, lease, idempotency and audit tables, migrations, retention and concurrency **not finalized**; invent no columns.
- **Security:** transport peer authentication, RBAC/tenant constraints, secret protection, privilege separation and threat model need review; no generic root shell.
- **DevOps:** package identity, allowlisted changes, rollback and trusted release lifecycle in the [R3 installer contract](../14-devops-releases/installer-lifecycle-r3.md).
- **QA:** [`R3-IPC-TEST-001..012`](../13-tests-quality/r3-ipc-installer-gates.md) **PLANNED**: cross-tenant denial, replay, crashes, concurrent updates, lost replies, version mismatch and security.

**DOC-GAP-006 remains OPEN.** Ratify real wire schemas and scopes, implement PHP/Go only after R1/R2 gates and verify denials on an authorized VM. This is a candidate specification, not an independent security review.
