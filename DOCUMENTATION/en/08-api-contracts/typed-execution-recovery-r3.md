<!-- forgepanel-doc id=FP-08-R3-TYPED-EXECUTION revision=1 status=specified -->
# R3 — Typed execution, observed effects and safe recovery contract

[Français](../../fr/08-api-contracts/typed-execution-recovery-r3.md) · [API/IPC](README.md) · [Action registry](../../evidence/typed-agent-operations-v1.json) · [PostgreSQL jobs](../09-database/physical-jobs-model-r3.md) · [Linux identities](../14-devops-releases/linux-service-identities-r3.md) · [QA](../13-tests-quality/r3-physical-execution-gates.md)

**Authority: API / IPC / Contracts with Security, Database, DevOps and QA. SPECIFIED / CANDIDATE.** No executable handler, Unix socket, HTTP route, privileged binary, Linux command or system change is introduced. Contracts are **validation models, not root authorization**. `EXEC-FP-0001..0012` extend IPC-FP-0001..0012 and INST-FP-0001..0012 without changing Q1–Q170. `DOC-GAP-005/006` remain **OPEN**, with missing R1 source and R2 runtime.

## Twelve candidate execution requirements

**EXEC-FP-0001 — Closed registry and strict types.** Evaluate only an explicitly approved `operation_id` from [ACT-FP-0001..0007](../../evidence/typed-agent-operations-v1.json). A schema-valid payload is **necessary but not sufficient**. Forbid `command`, `argv`, `script_path`, `shell`, `raw_args`, runtime-provided interpreters or downloaded executables; handlers are dedicated, not dynamically resolved OS commands.

**EXEC-FP-0002 — Actor/permission at effect time.** The bridge carries authenticated actor authority narrowly scoped to operation/tenant/resource/plan/revision. Go **independently** verifies Linux peer, ownership and effective permission at the effect boundary. Expert UI, application Super Admin or private Hub license cannot bypass this review.

**EXEC-FP-0003 — Immutable plan digest/contract.** A versioned canonical `plan_digest` binds exact artifacts, target, policy, approvals and input fields, checked at admission **and the effect boundary**. Modified/expired plans or stale target revisions are denied, never silently re-used.

**EXEC-FP-0004 — Minimal system privilege.** Future privileged handlers must be narrowly scoped to named packages/services/verified generations and independent approval, never generic root execution. Until confinement and real VM testing are approved, `ACT-FP-0005` and `ACT-FP-0007` remain **`BLOCKED_UNTIL_QUALIFIED`**.

**EXEC-FP-0005 — Effect-boundary fencing.** Every mutation independently verifies resource identity/ownership, observed revision, lease owner and monotonic fencing token **at the time of the effect**. A stale worker can never apply after lease transfer. If Linux/handler cannot enforce this against concurrent operations, **BLOCK the mutation** rather than claiming safety.

**EXEC-FP-0006 — Nondestructive PLAN/PREFLIGHT.** Expose impact, dependencies, permissions, unmanaged files, port/listener conflicts and trusted artifact provenance. Read-only checks do not authorize APPLY. STAGE may only create bounded private verified copies, not activate services or install unsigned scripts.

**EXEC-FP-0007 — Guarded APPLY with evidence.** Before sensitive APPLY require fresh actor approval, Q47 PLAN/PREFLIGHT/SNAPSHOT, verified required backup, signed provenance, current plan/revisions, local tenant authority and a current resource lock. Handler records intended/observed effects and a durable step ID. IPC ACK or zero exit code alone **does not** establish successful Linux change.

**EXEC-FP-0008 — Functional VERIFY before success.** Verify actual domain effect and dependent service health (vhost, HTTP/TLS, panel login, DB connectivity, per-operation expected state), including tenant denial and emergency administrator route. No `SUCCEEDED` before `VERIFYING` and authenticated observed-effect evidence.

**EXEC-FP-0009 — Crash, lost ACK and unknown effects.** If Linux may have changed before timeout/restart/response loss, **never replay blindly**. Read durable PostgreSQL state and independently inspect Linux, distinguishing proven absent, applied, partial and unknown effects. Unknown state requires `COMPENSATION_REQUIRED` or controlled blocked recovery; numerical deadline/retry values remain unapproved.

**EXEC-FP-0010 — Safe compensation and irreversibility.** Compensate **only** provably reversible steps with accessible, verified checkpoints. Irreversible SQL DDL, lost keys or unmanaged packages/services cannot be undone by binary rollback. Disclose irreversibility before approval; require independent human recovery when necessary.

**EXEC-FP-0011 — Redacted audit and secrets.** Audit plan/version/commit, pseudonymized actor/tenant/resource, authenticated peer, decision, checkpoint, fencing and health observations with correlation, not raw tokens, customer content, private keys or credentials. Evidence read/export permissions differ from execution authority; Q152 signing/Q162 immutable storage remain **unimplemented**.

**EXEC-FP-0012 — Compatibility and delegation.** A handler activates only on an exactly qualified OS/WebStack/contract version/capability combination. Mismatch or Hub outage grants no privileges; public Core works locally, or specifically blocks operations whose **own Core prerequisites** are missing. Schema upgrades must retain idempotency/recovery and Q132 critical vetoes.

## Operation-specific candidate guards — no handler is executable

| ID | Candidate logical function | Effect and necessary evidence | Current authority |
|---|---|---|---|
| `ACT-FP-0001` | `host.capabilities.observe` | Bounded observation, not OS certification | CANDIDATE, not registered |
| `ACT-FP-0002` | `artifact.signature.verify` | Independent publisher trust root, signature **and actual artifact bytes**; failure = `TRUST_FAILURE` | CANDIDATE, no trusted publisher service |
| `ACT-FP-0003` | `installer.plan.compile` | Nondestructive diff, ownership and revisions | CANDIDATE, no APPLY |
| `ACT-FP-0004` | `installer.stage_verified_packages` | Verified bounded private copy, no active service changes | CANDIDATE, no working installer |
| `ACT-FP-0005` | `installer.activate_signed_generation` | **FUTURE privileged** signed plan/checkpoint/current fencing/operator approval/qualified VM | **BLOCKED_UNTIL_QUALIFIED** |
| `ACT-FP-0006` | `installer.health.check` | Scoped panel/PG/service health, not just `active` | CANDIDATE, no endpoint |
| `ACT-FP-0007` | `installer.compensate_generation` | **FUTURE privileged** bounded compensation, checkpoint, fresh authorization/audit | **BLOCKED_UNTIL_QUALIFIED** |

[Candidate execution guards](../../evidence/candidate-typed-execution-guards-v1.json) define effect class and negative gates by ID. **They are not a deployable permission table or a signed root policy.** This lot does not add executable handlers or public actions.

## Separate job and effect state

~~~text
INTENT durably committed in PostgreSQL (ACCEPTED != Linux applied)
      → QUEUED (no resource lease)
      → RUNNING (valid owned lease, rechecked fencing at effect boundary)
      → VERIFYING (observed effect + functional health checks)
      → SUCCEEDED (only after proof and durable audit)
               or FAILED (proven no external effect)
               or COMPENSATION_REQUIRED (partial/uncertain effect)
               or BLOCKED (trust/authorization/revision veto)
~~~

Every transition retains redacted, durable request/job/step/correlation IDs, policy revision and plan digest. Unknown effects must **never** become `SUCCEEDED`. Expired leases never restore execution authority.

## Error classification and ownership

| Failure | Candidate response | Recovery |
|---|---|---|
| Unauthenticated peer, foreign tenant, unknown operation | `UNAUTHENTICATED/FORBIDDEN/SCOPE_DENIED/INVALID_INPUT` | No mutating job/effect |
| Changed/expired plan or invalid signature | `TRUST_FAILURE/STALE_REVISION` | Refuse before APPLY |
| Same idempotency key, changed digest | `IDEMPOTENCY_CONFLICT` | Read existing job, never reapply |
| Stale fence, owned lock busy, unmanaged resource | `RESOURCE_LOCKED` / `BLOCKED` | Reconcile and require new plan |
| Timeout/crash after possible external effect | `PARTIAL_FAILURE/RECOVERY_REQUIRED` | Inspect PG and Linux, separate compensation |
| Health fails despite service `active` | `RECOVERY_REQUIRED` | Restore only proven reversible changes |
| Irreversible DDL or unavailable backup key | `RECOVERY_REQUIRED` | Controlled manual recovery, no fake rollback |

All [12 `R3-EXEC-TEST-001..012`](../13-tests-quality/r3-physical-execution-gates.md) remain **PLANNED**. API/IPC owns protocol/error ratification; Database owns durable jobs; Security owns trust/fencing/privilege; DevOps owns handlers/OS, QA owns authorized-VM effects. R1/R2 remain prerequisites; this documentation executes no system command.
