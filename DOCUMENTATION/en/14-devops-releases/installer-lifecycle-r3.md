<!-- forgepanel-doc id=FP-14-R3-INSTALLER revision=2 status=specified -->
# R3 — Candidate trusted installation, approval and recovery lifecycle

[Français](../../fr/14-devops-releases/installer-lifecycle-r3.md) · [DevOps](README.md) · [Typed IPC](../08-api-contracts/symfony-go-ipc-r3.md) · [R3 QA](../13-tests-quality/r3-ipc-installer-gates.md)

**Status: SPECIFIED / CANDIDATE.** There is no official installer, published install URL, ForgePanel DEB/RPM package, privileged executor, live service updater or operational Stable/Beta/Dev distribution channel. Dependencies: [genuine Foundation source #2](https://github.com/yyogas/forgepanel/issues/2), [Symfony/PG #3](https://github.com/yyogas/forgepanel/issues/3), [Configuration Engine #9](https://github.com/yyogas/forgepanel/issues/9), [release #15](https://github.com/yyogas/forgepanel/issues/15). Owner DevOps / Build / Release; handoffs to Security, API/IPC, Database and QA. Requirements `INST-FP-0001`–`INST-FP-0012`. **Preserves Q47, Q61 C, Q62 C, Q71/Q72 and Q119/Q120 without new Q171+ owner decisions.**

## Trust chain before any privileged step

**INST-FP-0001 — Provenance.** A one-command install is offered **only after** a verified bootstrap with an independent protected trust anchor can actually be distributed. No official URL, version or channel has been picked. Never execute unsigned downloaded scripts, HTTP redirects, webpage content, or a digest distributed alongside compromised bytes as trust. Verify **actual installed bytes**, not only a manifest's detached signature.

**INST-FP-0002 — Artifact signatures, channel and anti-rollback.** Verify publisher identity, protected trust roots, rotation/revocation, signed release metadata and individual artifacts, exact hash/size, authorized Stable/Beta/Dev channel, freshness/expiry and version downgrade policy. Signature failure, replay or revoked key = `BLOCKED`. Build, signing and release approval identities stay separate; **publisher private signing keys never ship with public Core**.

**INST-FP-0003 — OS qualification.** Documentary **target platforms** are Debian 12/13, Ubuntu LTS 24.04/26.04 and AlmaLinux 9/10. This claims no real support: separately test each OS/version/architecture for package provenance, dependencies, filesystem permissions, firewall, AppArmor/SELinux, systemd, PHP/PG, update and recovery. **First MVP OS/WebStack is not chosen** until comparative Q121/Q122 VM evidence and Q132 security vetoes. Signed APT/DNF repositories are future contracts, not live URLs.

**INST-FP-0004 — Nondestructive inventory.** Observe networks, bound IP/ports/listeners, installed services, packages, accounts, mounts, free space, OS and conflicts with no mutations. Distinguish clean install, reinstall and existing-service adoption. **Never overwrite unowned service files** without an explicit, authorized ownership/backup/adoption/recovery plan.

## Candidate installation state machine aligned with Q47

| Phase | Durable prerequisite/evidence | Success or denial |
|---|---|---|
| `DRAFT` | Version/OS and operator intention; no Linux effect | Draft request |
| `PLAN` | Diff, origin, resource scope, roles, dependencies, revision and plan digest | Refuse OS/port conflict or unregistered operation |
| `PREFLIGHT` | Packages/trust, capabilities, permissions, emergency admin route, config syntax | `BLOCKED` unless trust/access pass |
| `SNAPSHOT` | Recoverable checkpoint, DB/secret impact and previous observed state | `BLOCKED` when required recovery cannot be shown |
| `STAGE` | Verified artifacts in bounded isolated staging and rehashed bytes | No active service change |
| `APPLY` | Fresh explicit approval, locks, **launch-time** plan/signature/revision checks | Only registered typed Go actions |
| `VERIFY` | Health of service/UI/DB/TLS/admin access, independent observation | Service `active` alone is insufficient |
| `COMMIT` | Observed final state, version/digest, audit, reconciliation | Record outcome, not automatic release |
| `RECOVER` | Halt and inventory partial changes, restore reversible steps only | Disclose irreversible effects/manual recovery |
| `BLOCKED` | Evidence of failed prerequisites | Never blindly resume privileged apply |

**INST-FP-0005 — Authorized plan.** `APPLY` requires a fresh explicitly authorized plan bound to origin/version/revision/target/actor/permissions, with checked current preconditions, backup and approvals. Exact plan format, TTL and approval policy are **open for technical ratification**; an Expert UI mode never bypasses denials.

**INST-FP-0006 — Durability and idempotence.** Persist intent, approval, step and observed results before acknowledgement. A restarted controller reconciles desired and observed state rather than replaying an irreversible step. Retried/duplicated requests must not silently apply twice. **No atomic transaction exists across PostgreSQL and Linux.**

**INST-FP-0007 — Linux installation.** Dedicated OS adapters and named operations manage approved package/service transitions using minimal users, filesystem permissions, systemd units and preserved AppArmor/SELinux/firewall policy. **No `shell.exec`, generic root command, user-uploaded script or free-form command in a manifest.** Network changes retain a verified emergency admin path.

**INST-FP-0008 — Setup identity.** No root password in Symfony/browser setup. The wizard establishes a **permanent recoverable admin** with **optional MFA** and distinct bootstrap/login sessions ([R2 contract](../03-core/bootstrap-identity-r2.md)). A successful install plan alone does not mean that panel activation succeeded.

**INST-FP-0009 — Recovery.** Verify a checkpoint and recovery key access before risky mutations; define config rollback, bounded package recovery and compensation. An irreversible SQL DDL mutation **cannot be undone simply by rolling back application code**. Record `RECOVERY_REQUIRED` with controlled manual instructions when restoration is impossible. Q166 will eventually require full isolated per-backup restores before calling a backup recoverable.

**INST-FP-0010 — Health and continuity.** `VERIFY` checks agent/database/panel/admin sessions, listeners, redacted diagnostics, TLS and login routes; before/after network changes, prove a safe active admin path or refuse. Liveness is not readiness or complete functionality.

**INST-FP-0011 — Evidence/observability.** Record exact revision/commit, OS/arch, VM image, trust verdict and artifact hashes, actor/approval, plan hash, every step, correlation, roles/locks, health and compensation with secrets redacted. Per-environment reports distinguish `PASS/FAIL/BLOCKED/SKIP`; green documentation CI, fixtures and containers **never certify** real systemd, package-manager or VM isolation. Q152/Q162 later require signed private immutable evidence.

**INST-FP-0012 — Compatibility and lifecycle.** Fresh install, retry, upgrade, patch, rollback, uninstall and disaster recovery need explicit paths and negative tests. PostgreSQL migration/backup order follows reviewed policy, with no fictitious automatic SQL downgrade. Hub is optional and cannot be root controller or a prerequisite for standard Core recovery/installation. No `stable/main/production` promotion without required gates and reviews.

## Explicit failure handling

| Failure condition | Required handling |
|---|---|
| Invalid/revoked signature, unknown root, tampered manifest, stale version | `BLOCKED` before privileges, redacted audit |
| Unsupported OS/package/service or untrusted extension | Refuse; never infer another OS/WebStack works |
| Unmanaged file, bound port, unauthorized resource | Refuse or require reviewed adoption/recovery plan |
| Disk full, network outage, reboot, failed service after `APPLY` | Restore only verified reversible state; otherwise `RECOVERY_REQUIRED` |
| Irreversible SQL or unavailable backup key | Never claim complete rollback/recoverable state |
| Hub offline or diagnostics opt-out | Free Core continues without remote publisher commands |

## Ownership and exit evidence

- **API/IPC:** each privileged Go step must be described by the [candidate operation register](../../evidence/typed-agent-operations-v1.json) and later approved as a versioned typed contract without free-form commands.
- **Database:** migrations, jobs and backups require separately approved schemas; no tables/columns defined here.
- **Security:** operator proof, separation of approvals, signature/trust/secret storage, timeouts and local recovery require review; no independent audit has occurred.
- **QA / DevOps:** [`R3-INSTALL-TEST-001..012`](../13-tests-quality/r3-ipc-installer-gates.md) must run on authorized disposable VMs with exact OS/commit and failure/recovery evidence.

**DOC-GAP-005 remains OPEN.** This document enables no installation. Genuine Foundation Core source, functioning R2 Symfony/PostgreSQL and an authorized Linux executor are not integrated.

## Dependency on durable state and local channel trust

Future APPLY requires [durable intent/lock/job state](../09-database/durable-jobs-r3.md) and [independently verified peer trust](../08-api-contracts/local-peer-trust-r3.md). Worker lease expiry never permits a second blind apply; lost IPC ACK is not proof of no external effect. On uncertainty preserve COMPENSATION_REQUIRED and emergency admin access. **These contracts remain candidates**: no installer, actual SQL job tables, remote mTLS or running Unix socket. [QA](../13-tests-quality/r3-jobs-peer-gates.md).
