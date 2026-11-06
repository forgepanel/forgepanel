<!-- forgepanel-doc id=FP-14-R3-LINUX-IDENTITY revision=1 status=specified -->
# R3 — Candidate Linux accounts, services and privilege separation

[Français](../../fr/14-devops-releases/linux-service-identities-r3.md) · [DevOps](README.md) · [Peer trust](../08-api-contracts/local-peer-trust-r3.md) · [Typed execution](../08-api-contracts/typed-execution-recovery-r3.md) · [QA](../13-tests-quality/r3-physical-execution-gates.md)

**Authority: DevOps / Build / Release and Security / Hardening, with API/IPC and Database. SPECIFIED / CANDIDATE.** No Linux account/group, systemd unit, socket or privilege is created. Account names, filesystem paths, LSM profiles and Linux distributions require **approval after authorized VM testing** and R1 genuine source/R2 Symfony/PG. Requirements `LINUX-FP-0001..0012` describe security boundaries, not deployed configuration. Q1–Q170 and autonomous public Core without Hub remain binding.

## Twelve service identity guarantees

**LINUX-FP-0001 — Separate actors.** Distinguish Linux system admin, PostgreSQL migrator/DDL, Symfony runtime, isolated IPC bridge, nonroot Go agent, **future disabled** minimal privileged handler, read-only observation identity and tenant website Unix users. Application Super Administrator is **not** Linux root. Publisher Hub licensing never grants Linux privileges.

**LINUX-FP-0002 — Symfony/browser separation.** Symfony validates HTTPS/session/CSRF and RBAC, org and resource ownership before intent. Hosted PHP workers, tenant scripts, plugins and webhooks **must not access privileged server-control IPC**. Actual panel versus tenant process isolation needs real verification.

**LINUX-FP-0003 — Isolated IPC bridge.** A distinct process **outside tenant PHP-FPM pools and third-party apps** may exclusively own private Go transport access. Its UID/GID/filesystem rights must be minimal; bridge credentials alone do not authenticate the end-user actor. Direct IPC access from a broad shared web runtime is **a risk to review**, not granted by default.

**LINUX-FP-0004 — Nonroot Go agent.** The agent validates fixed typed schemas, policy/plan digests, peer identities, real resource scopes and observations without generic shell, arbitrary sudo or CAP_SYS_ADMIN. Do not give shared groups access to customer content. Future high-risk effects require dedicated handlers, not hidden elevation inside generic Go code.

**LINUX-FP-0005 — Privileged handler disabled.** A narrow privileged handler **may** be separately designed only after threat modelling and architecture/security approval; it is absent today. It would accept only an explicitly approved `ACT-FP` operation with versioned plan/actor/resource and validated effect boundary. `ACT-FP-0005` and `ACT-FP-0007` remain `BLOCKED_UNTIL_QUALIFIED`. No arbitrary scripts, downloaded executables, free shell args or raw QEMU options.

**LINUX-FP-0006 — Separate PostgreSQL identities.** Candidate DDL migrator, Symfony runtime DB identity, dispatcher/worker and audit reader roles have separate limited grants. Runtime cannot own tables, execute DDL or create roles. DB roles are never confused with Unix UIDs or user-facing admin sessions.

**LINUX-FP-0007 — Socket/filesystem boundary.** Candidate private filesystem Unix domain socket inside a **dedicated systemd-managed runtime directory**, with owner/type/mode and group membership reviewed. Canonical paths and symlink/replacement checks precede any reuse. Group-writable sockets require verified member identities. Example `/run/forgepanel/agent.sock` is **illustrative only**, not a selected installation path.

**LINUX-FP-0008 — Kernel peer identity.** Verify **kernel-reported** Linux credentials (`SO_PEERCRED` candidate) and process instance, not a JSON UID/PID. After restart/PID reuse/FD transfer/credential rotation require fresh trust. Valid process UID does not prove an end-user actor mandate; that remains separately scoped and validated.

**LINUX-FP-0009 — systemd/LSM sandboxing.** Review and VM-test candidates `NoNewPrivileges`, `PrivateTmp`, `ProtectSystem`, `ProtectHome`, `RestrictAddressFamilies`, `CapabilityBoundingSet`, CPU/memory/task controls and OS-qualified AppArmor/SELinux. Never blindly apply a profile that breaks IPC, required network access or recovery. `DynamicUser` is **not selected** by this doc, since stable peer UID/ownership may matter.

**LINUX-FP-0010 — Fencing at effect boundary.** After a worker loses its lease, its old fencing generation must fail an independent Linux-side resource/plan/revision check **at the point of mutation**. A monotonic database field alone is not enough. If the effect boundary cannot enforce this under concurrent operation, **deny mutation**, even if another worker owns a SQL lease.

**LINUX-FP-0011 — Secrets/logs/recovery.** Per-service secret scope, protected storage, rotation/revocation and correlated redacted events; never ship publisher private signing keys in public Core. A separately auditable local emergency admin route must survive agent, DB or Hub outage, with risk-aware restrictions and no user-provided root shell.

**LINUX-FP-0012 — Install/update/revoke.** Add accounts/services/permissions only via verified signed package and explicit Q47 plan, preserving backups, ownership and rollback when safe. Uninstall/reinstall cannot arbitrarily remove tenant UIDs or reuse unknown service identities. No OS support claim until actual Debian/Ubuntu/AlmaLinux VM isolation/recovery tests.

## Candidate identity matrix — no accounts are created today

| Logical label (final Unix name not chosen) | Duty | Must not own |
|---|---|---|
| `panel_http` | Symfony HTTP/user sessions and RBAC | Linux root, DDL, generic shell, out-of-scope tenant content |
| `panel_ipc_bridge` | Private transport, peer process instance and bounded requests | Hosted tenant rights, publisher signing key, package manager |
| `panel_agent` | Nonroot typed Go validation, safe observations/readiness | Global root, arbitrary exec, tenant hosting secrets |
| `panel_privileged_handler` | **FUTURE DISABLED**: approved allowlisted Linux effects | Generic shell, Hub control, unapproved operations |
| `panel_migrator` | Dedicated checksummed SQL DDL during maintenance | Web session and permanent runtime rights |
| `panel_db_runtime` | Tenant-scoped application DB writes only | DDL/ownership/DB superuser or unrelated tables |
| `hosted_site_user` | Hosted customer PHP/files/SFTP under owned scope | Go socket, panel configuration or other tenants |
| `panel_observer` | Authorized redacted metrics/health/audit reads | Secrets, mutation or installation grant |

All names above are **logical labels**, not reserved Unix users. `panel_privileged_handler` cannot be enabled by this documentation. Grants/groups need real isolation tests, especially PHP-FPM and restricted SFTP.

## Candidate provisioning and revocation

1. Read-only inventory of users/GIDs, services, sockets/ports, unmanaged files and permission ownership.
2. Validate the exact OS/packages, verified signed plan, account/group collision prevention, backup and emergency access.
3. Only after approval, process proposed account/service changes via a typed durable Q47 plan: `PLAN → PREFLIGHT → SNAPSHOT → STAGE → APPLY → VERIFY/RECOVER`. Privileged handlers remain disabled.
4. Test malicious hosted site and compromised bridge separately: neither may access private socket/system data or escalate via a forged actor mandate.
5. Rotation must reject stale sessions and clean only product-owned files; retain backups under approved retention.
6. Losing the last admin route, tenant isolation or recoverability is a Q132 hard veto.

## Evidence and handoffs

All [12 `R3-LINUX-TEST-001..012`](../13-tests-quality/r3-physical-execution-gates.md) remain **PLANNED**. Container permission tests/Markdown cannot establish real SELinux/AppArmor/tenant isolation. Security reviews identities/LSM, DevOps packages/systemd/OS, API/IPC kernel peer, Database DDL/runtime grants and QA true OS VMs. **No root action is implemented here.**
