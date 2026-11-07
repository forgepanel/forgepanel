<!-- forgepanel-doc id=FP-04-PROGRESSIVE revision=2 status=proposed -->
# ForgePanel — Independent optional modules, visibility and availability

[Français](../../fr/04-modules/progressive-release-policy.md) · [Current catalog](README.md) · [Strategy](../00-project-control/modular-development-strategy.md) · [40-entry registry](../../evidence/forgepanel-modular-roadmap-proposed-v2.json)

**Updated candidate of the earlier progressive policy; not a runtime integration.** The registry preserves 15 proposed v1 Core capabilities and 25 optional modules/extensions. Each `target_release` is indicative only; none is represented as installed, executable or operating-system certified.

## Required classification

| Class | Example | Failure/absence consequence |
|---|---|---|
| **Mandatory Core** | Identity/RBAC, PHP/TLS, control SQL, files/SFTP, backup/restore, typed Linux operations | Blocks release of the **promised essential workflow** if absent/unverified |
| **Noncritical Core UI** | Read-only module catalog | Degrade that page, not serving sites, sessions or emergency recovery |
| **Public optional module** | ONE-CLICK INSTALL, Container Apps, mail, WAF | Never prevent the Core/previous sites from running when absent |
| **Private publisher extension** | ForgePanel-Hub | Core auth/hosting/backup/recovery continue when Hub is offline |

A firewall baseline, valid TLS, permissions, security audit or proved restoration are not deferrable merely by calling them “future plugins” if needed to protect an advertised workflow.

## Separate lifecycle controls

- **Documentation/development**: `PLANNED`, `SPECIFIED`, `DEVELOPING`, `IN_REVIEW`, `TESTING`, `RELEASE_READY`, `RELEASED`, `DEPRECATED`. `DEVELOPING` requires identifiable live commit/issue/PR evidence, not a document or prototype card.
- **Availability on the host**: an actually installed package with valid provenance/signature and verified Core/API/OS/resource compatibility and dependencies. A visible card proves none of this.
- **Activation**: locally scoped server/tenant/site authorization, plan/entitlement where applicable, safe migrations, backup/recovery and health and audit. Only an allowed Core operation can activate anything.
- **Visibility**: `HIDDEN`, `ADMIN_PREVIEW`, `CUSTOMER_INFO`, `CUSTOMER_AVAILABLE`. Editing visibility never elevates permissions.

**UI contract:** “Developing” / “Planned” opens a read-only page with category, value, dependencies, tentative release, evidenced status, limitations and next milestone. No fake install/activate action, no empty routes or broken side-menu links. Use **Module Manager → Coming soon** and filters by stage/category/release. “Available” is shown only with verified package, compatibility, permissions and working route. UI supports FR/EN and accessibility.

## Module manifest contract — required before execution, not implemented yet

Every future module must declare: `id`, `owner`, `type`, `status`, `business_value`, `target_release`, `core_version_range`, `api_contract_version`, `dependencies`, `conflicts`, `permissions`, `data_migrations`, `feature_flag`, `default_enabled`, `installable`, `public_visibility`, `distribution_channel`, `rollback_strategy`, `tests`, `documentation`, `support_level`, and any `license_entitlement`. The candidate registry records these expected keys as **requirements**, not as functioning signed install manifests.

Future checks **must run server-side**: unique IDs, strict versions and acyclic dependency graph, no Core→optional hard dependency, migrations isolated from mandatory bootstrap, proven OS capability, RBAC/tenant checks at the effect boundary, idempotency/policy revision, quotas, provenance/signatures/anti-rollback, redacted audit, retries/recovery and data retention. Premium licenses cannot confer Linux privileges. No generic privileged `shell.exec` equivalent.

### Unavailable/failed conditions

- **Absent**: no optional route, worker, job, service or SQL object loaded; an informational card may remain.
- **Disabled**: no new effects, data retained, active jobs drained/recovered under contract, never silently deleted.
- **Incompatible**: activation denied with a precise explanation and potential reviewed migration path; Core continues.
- **Failed**: scoped/correlated failure and audit, without cascading into Core availability.
- **Private Hub offline**: new premium actions have explicit denied/unknown behavior under approved policy; free Core features and existing hosted data remain accessible.

## Free ONE-CLICK INSTALL versus CONTAINER APPS

**ONE-CLICK INSTALL** is a **free native** classic script/app installation engine with **no Docker/Podman or premium Hub dependency**; third-party app licenses remain separate. **CONTAINER APPS** is a different stack engine, with separately qualified **Docker** and **Podman** drivers, pinned/signed images, network/ports/volumes, CPU/RAM/PIDs/I/O budgets, verified isolation and backup/restore. Never apply a container recipe through the native executor. The same product may have **two independent recipe variants**; read-only common search is allowed, silent conversion is not. Preserve Q171/Q176/Q191–Q213, and Coraza detection-first remains a **candidate** under Q174, not an automatic operational WAF.

## Proposed milestones, without promised dates

| Release target | Example optional scope | Actual state |
|---|---|---|
| `1.0` | Informational catalog; no required optional app engines | R1–R4 Core **not certified** |
| `1.1.x` | ONE-CLICK, Git Deploy, neutral R5 ABI | Specified, not executable |
| `1.2.x` | Docker, staging, extended SQL/cache, R6 Hub after ABI | Specified, not executable |
| `1.3.x` | Podman, local DNS/mail, WAF, malware | Specified, not executable |
| `1.4.x+` | Webmail, reseller, visual studio, configuration, billing | Specified, not executable |
| `2.x` | Multi-server/HA/customer VM features | Dependent on measured capacity/risk; not executable |
| `3.x` | Ecosystem governance and scale | Exploratory, not a forced SemVer major |

A component ships only after a scoped PR, accepted API/DB/security contracts, end-to-end and regression tests, qualified OS/resources and changelog. Development can continue between releases without exposing unfinished code to customers.

## Governance and evidence

The documentary [v2 registry](../../evidence/forgepanel-modular-roadmap-proposed-v2.json) explicitly denies execution; it is **not an agent privilege registry**. The [35 planned QA cases](../13-tests-quality/modular-release-gates.md) require real execution before claiming qualification. R5 neutral SDK and R6 Hub follow the R4 MVP and are never required for Core 1.0. **Admin MFA remains optional; security and audit remain mandatory.**