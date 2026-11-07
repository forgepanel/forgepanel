<!-- forgepanel-doc id=FP-13-MODULAR-GATES revision=1 status=proposed -->
# ForgePanel — Modular release gates and optional-failure qualification

[Français](../../fr/13-tests-quality/modular-release-gates.md) · [QA](README.md) · [Strategy](../00-project-control/modular-development-strategy.md) · [Test registry](../../evidence/forgepanel-modular-qa-proposed-v1.json)

**35 proposed scenarios, all `NOT_RUN` on any installed product.** Offline JSON/Python structural tests of this package cannot establish real HTTP, SQL, VM, security or backup/restore outcomes. Each future run must attach exact SHA, qualified OS/WebStack and VM image digest, timestamp, harness, logs/evidence and reviewer where required. `SKIP` is never PASS.

## 1. Essential scenarios to preserve

- Verified Core/PostgreSQL install and recovery, initial bootstrap/login, optional MFA, scoped RBAC, sessions and audit on a qualified OS.
- Real PHP website/domain/HTTPS, Linux and tenant isolation, files/SFTP, bounded VPS maintenance and tested isolated restore.
- Rejection of unsupported OS/WebStack claims; cross-tenant negative checks, redacted logs, CSRF and interrupted-operation recovery.

## 2. Test optional-module degradation

| IDs | Expected outcome | Failure means |
|---|---|---|
| MOD-QA-001..005 | Core/session/site and backup/restore run without Hub, One-Click, containers, distant catalog or broken optional service | Cascading dependency failure |
| MOD-QA-006..010 | Planned/absent ≠ executable: no live route/job/migration/command; flags/RBAC enforced server-side | Unauthorized code execution |
| MOD-QA-011..015 | Tenant isolation, data retention, incompatible upgrades, Hub outage and failures remain contained | Weak isolation/recovery |
| MOD-QA-016..021 | Native/container recipe separation, no fake buttons, evidenced labels, accessible FR/EN without XSS | Engine confusion or misleading UX |
| MOD-QA-022..028 | Actual OS support, optional MFA, genuine restore, P0/P1 RC/GA veto, signed artifact and patched security | Unqualified release |
| MOD-QA-029..035 | Hub no Linux grants, free Core independent, R2/VM/legal/Git readiness evidence | Commercial coupling/false verification |

Exact descriptions and **individual `NOT_RUN` statuses** are recorded in the [machine registry](../../evidence/forgepanel-modular-qa-proposed-v1.json). These are ranges of independent scenarios, never one bulk PASS. A missing/unverified **essential** capability blocks its promised release. An absent **properly isolated optional** capability does not block the Core milestone.

## 3. Module Manager acceptance

Verify with UI + server checks: an upcoming informational card has no `execute`, `install` or `activate` path; DEVELOPING links to a real commit/PR; absent routes do not break navigation; no permissions/tenant identity are inferred from UI controls; hiding a card does not change activation. Future installation uses a **separate qualified contract** for RBAC/signature/dependencies/migrations/backup/recovery/audit. Until a real API exists, catalog UI is a non-operational demonstrator.

## 4. Gate statuses and vetoes

Use `PASS`, `FAIL`, `BLOCKED`, `NOT_RUN`, each with exact evidence. GA is blocked by missing E2E for advertised functionality, open scope-specific P0/P1, failed critical restore, untrusted artifacts or optional modules contaminating Core startup. Security and tenant-isolation vetoes cannot be waived by performance exceptions. All 35 scenarios still require **real execution on installed artifacts**; this document is not certification.