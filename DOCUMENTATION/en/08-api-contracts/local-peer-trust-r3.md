<!-- forgepanel-doc id=FP-08-R3-PEER-TRUST revision=1 status=specified -->
# R3 — Local Symfony ↔ Go peer identity and scoped trust

[Français](../../fr/08-api-contracts/local-peer-trust-r3.md) · [API / IPC](README.md) · [Typed IPC](symfony-go-ipc-r3.md) · [Durable jobs](../09-database/durable-jobs-r3.md) · [QA matrix](../13-tests-quality/r3-jobs-peer-gates.md)

**Authority: API / IPC / Contracts and Security / Hardening (mandatory joint review).** **SPECIFIED / CANDIDATE**; **transport not selected**, no socket, daemon, certificate, token or Linux identity created. Final choices belong to Security, DevOps and Database review, not to this page. Requirements `PEER-FP-0001`–`PEER-FP-0012`; preserve Q47/Q66/Q120 and Q132 critical vetoes, Q1–Q170 unchanged. [Issue #9](https://github.com/yyogas/forgepanel/issues/9) and [DOC-GAP-006](../00-project-control/documentation-readiness.md) remain **OPEN**. Genuine SRC-03 source not imported.

## Why a private socket is insufficient

A socket filename, a PHP-FPM UID, a JSON `actor_id` field or the existence of a certificate **does not alone authorize a system operation**. Safety needs all of: (a) authenticated peer/process, (b) bounded authentic message, (c) independently validated actor/tenant/resource permissions, (d) approved plan and revision/hash, (e) closed typed Go operation registry, (f) observed effects and audit.

## Twelve local trust requirements

**PEER-FP-0001 — Exposure.** Candidate local transport is a **private filesystem Unix domain socket**, with no public TCP/HTTP listener, provisioned by an isolated service, and disabled until trust/configuration is valid. No abstract namespace or implicit FD passing without explicit review; exact socket characteristics remain open.

**PEER-FP-0002 — Process identities.** Distinct Symfony, dedicated IPC bridge, nonroot Go agent and **only if eventually approved** minimal privileged executor identities. Shared tenant, mail, webserver or Hub UIDs must never be sufficient. An untrusted PHP-FPM application, plugin or webhook must not have write access to a privileged IPC socket.

**PEER-FP-0003 — Actual peer identity.** On Linux, consider **kernel-reported peer credentials** (`SO_PEERCRED` or equivalent qualified mechanism), verify UID/GID and process instance, and assess `pidfd` or process start identity to mitigate PID reuse. **Never trust UID/PID asserted in a payload** or treat a shared UID as proof of expected executable. Exact method remains a technical decision.

**PEER-FP-0004 — Path protection.** Dedicated-owned private parent directory, strict socket mode, reject symlinks/hardlinks and TOCTOU, use `openat`/`O_NOFOLLOW` where applicable; verify ownership, type and device/inode before replacing any existing path. A socket shared with a Unix group requires independent membership audit.

**PEER-FP-0005 — Session lifecycle.** Bind the handshake to verified peer identity, negotiated protocol and effective configuration. Revoke old sessions after restart/rotation, reject reused file descriptors and unauthorized reconnect, and refuse operations before service `readiness`. A live transport connection is not proof that an end-user actor is authenticated.

**PEER-FP-0006 — Actor mandate.** Symfony authorizes user session and resource scope **server-side**; a narrow actor grant might bind operation, tenant, resource, revision, plan and request to Go. Go checks origin, scope and freshness. A JSON `actor_claim` alone is **not a signature or verified delegation**. Cryptographic protocol, TTL and trust key are open choices, not code artifacts here.

**PEER-FP-0007 — Independent authorization and closed registry.** Go revalidates real resource ownership/tenant/permissions against `ACT-FP-*` allowlist; reject `shell.exec`, unknown or disabled operations, raw command/argv/script/QEMU args. `ACT-FP-0005` and `ACT-FP-0007` remain **`BLOCKED_UNTIL_QUALIFIED`**, even when request JSON validates. Hub commercial entitlements cannot grant Linux authority.

**PEER-FP-0008 — Replay/idempotency.** Bind `request_id`, `idempotency_key`, canonical digest and durable decision to independently verified freshness. A supplied timestamp or nonce alone is not proof. Replay cache, window and rotation policy remain open, coordinated with [Database](../09-database/durable-jobs-r3.md).

**PEER-FP-0009 — Resource bounds.** Limit message size/depth, connected peers, admission/jobs per scope, queue growth and deadlines under reviewed policy. Strict parsing rejects unknown fields/versions, raw secrets, arbitrary URLs, unsafe paths and out-of-range values. No numerical defaults are approved here.

**PEER-FP-0010 — Failure/readiness.** Transport failure, saturation, permission changes or Go restart yields `DEPENDENCY_UNAVAILABLE`/`BLOCKED` **without assuming no Linux side effect**; retrieve durable job state through authorized path, never blind-retry `APPLY`. Liveness vs readiness of DB/agent/socket and emergency admin access are separate.

**PEER-FP-0011 — Logs, privacy and rotation.** Structured correlated audit of peer, actor, scope, operation, resource, contract version, denials and observed effects without tokens, cookies, signing keys, DB credentials or customer data. Support peer compromise/revocation and rotation without silently escalating. The Hub is never given a private Core monitoring or system-access backdoor.

**PEER-FP-0012 — Versioning and remote future.** Only **local/private IPC** is under consideration for R3. Multi-server operation needs a separately reviewed mutually authenticated protocol (possibly `mTLS`) with PKI/rotation, replay/partition handling and explicit local authorization. **No remote port, CA or protocol is approved** in this documentation.

## Candidate logical exchange — no implemented service

```text
Symfony (session/RBAC/resource scope) → durable PostgreSQL intent
        → strictly typed request (candidate-1 schema)
        → connect private filesystem Unix socket
        → Go observes kernel peer identity and validates channel session
        → Go independently rechecks actor grant, operation, tenant, policy, plan, revision
        → persist ACCEPTED/DENIED/REJECTED; job status separate from Linux effect
        → privileged Linux action only after future dedicated security approval
        → observed effect → VERIFY → SUCCEEDED, or failure/recovery status
```

**No current Go API performs this sequence.** Candidate [request](../../evidence/candidate-ipc-request-v1.schema.json) and [response](../../evidence/candidate-ipc-response-v1.schema.json) Schemas describe syntax only. The [peer binding JSON schema](../../evidence/candidate-peer-binding-v1.schema.json) is a **documentation model for kernel-observed attestation**: it neither retrieves `SO_PEERCRED` nor signs or authenticates anything on its own.

## Threat matrix and needed evidence

| Threat | Required refusal | Future QA |
|---|---|---|
| Tenant PHP/plugin compromise | No privileged socket access or service-user impersonation | `R3-PEER-TEST-001/002` |
| Spoofed JSON UID/PID | Ignore non-kernel peer identity | `R3-PEER-TEST-003` |
| Replaced socket/symlink/loose mode | Fail closed before exchange, audit | `R3-PEER-TEST-004` |
| Authorized peer, other tenant's actor claim | Independent tenant/role check, no disclosure | `R3-PEER-TEST-005/006` |
| Reconnect after rotation, replay | Fresh trust and verified digest/job state | `R3-PEER-TEST-007/008` |
| Saturation, crash, incompatible version | Bounded refusal and durable recovery | `R3-PEER-TEST-009/010` |
| Generic command or unsupported version | Deny before any privilege | `R3-PEER-TEST-011/012` |

**HANDOFF:** Security must ratify peer identity, Linux users, credentials and threat model; API/IPC owns schema/version/errors; Database owns grants/replays; DevOps owns socket/systemd/filesystem/restart; QA owns [12 `R3-PEER-TEST-001..012` cases](../13-tests-quality/r3-jobs-peer-gates.md), all **PLANNED**. No created secrets, privileged API, remote endpoint or Hub channel.
