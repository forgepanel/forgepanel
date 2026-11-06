<!-- forgepanel-doc id=FP-06-APP-CENTER-ENGINES revision=1 status=specified -->
# ForgePanel App Center — separate native and container installation engines

[Français](../../fr/06-apps-recipes/app-center-engines.md) · [Apps/Recipes index](README.md) · [Tests](../13-tests-quality/app-center-engine-gates.md)

**Status: SPECIFIED / TECHNICAL DRAFT.** On **6 November 2026** the owner confirmed **two independent App Center families** and an entirely free **ONE-CLICK INSTALL** engine. This direction complements Q2/Q50 (free Core), Q4 (customer runtimes), Q8/Q53 (official and reviewed partner catalog), Q47 (plan/validate/recover), Q51 (independent Docker and Podman drivers) and Q81–Q110 (PHP, databases, staging and quotas). It does **not** approve every technical candidate below or imply a working installer. Q171+ remain unanswered.

## Confirmed product rules

1. **App Center is a navigation umbrella, not a universal installation executor.** It contains two independent sections: **ONE-CLICK INSTALL** (native scripts, Softaculous-like) and **CONTAINER APPS** (containerized applications, 1Panel-like).
2. **ONE-CLICK INSTALL is always free to ForgePanel users** and never requires a premium entitlement, payment, subscription, publisher Hub license, Docker/Podman runtime or Hub connection. Third-party application license terms and server/resource costs are **separate**: a free installer does not make a commercial app free.
3. Every application/edition/version explicitly declares **one execution type**: \`native_script\` or \`container_stack\`. A container recipe cannot silently replace a native install or vice versa. The same app may publish **two separately qualified recipes**.
4. Container management uses Q51's independent Docker or Podman drivers **only after verifying host capabilities**. Do not install a container engine merely to host an ordinary PHP site. A Docker Compose recipe is **not automatically** qualified for Podman.
5. The local Core owns authorization and execution. The optional private Hub may publish **versioned catalog metadata** under narrow contracts, but never owns tenant files, database/volume secrets, Linux privilege or signing keys. Essential free native recipes must remain usable without Hub.

## Responsibility and resource comparison

| Area | ONE-CLICK INSTALL — native | CONTAINER APPS — Docker/Podman |
|---|---|---|
| Typical use | CMS, shops, forums and scripts running under traditional hosting | Services, developer tools, multi-service stacks and image-based apps |
| Prerequisites | Owned site/account, qualified WebStack/PHP or native runtime, supported SQL when required | Qualified Docker **or** Podman driver, images, networks, volumes, resource and exposure policy |
| Isolation unit | Tenant Linux identity, qualified PHP-FPM/site runtime, confined paths/ACL, quotas | Container identity/namespaces, seccomp/capabilities, cgroups, ports/network, volumes and host identities |
| Resources | Hosted files, PHP workers, I/O, SQL users/database quotas, tenant storage | Images/layers, persistent volumes, CPU/RAM/PIDs, virtual networks, host ports, secrets, service dependencies |
| Install | Verified upstream artifact → files/DB/config → checks → activation | Verified images → approved stack definition → volumes/networks/quotas → launch → health |
| Backup | Website files + SQL + restore-critical secrets | Persistent volumes + DB/services + stack definition + consistent secret recreation |
| Update | Code version, DB migrations, PHP/runtime compatibility and pre-change backup | Image digests, stack changes, volume/data migrations, controlled replacement |
| Remove | Explicit inventory and choice to retain site/DB/backups | Explicit inventory and choice to retain containers/network/volumes/backups |
| Permission | Site-manager limited to owned sites/hosting policy | Separate \`app.container.*\` scopes subject to server policy and real capabilities |
| Quota | Hosting/files/DB and runtime resource limits | CPU/RAM/PIDs/image storage/volume/ports/network quotas |
| ForgePanel engine price | **Free without a premium requirement** | Basic Core capability under Q2/Q50; no additional container-engine pricing decided |
| Initial roadmap | **Post-R4**, not a prerequisite for the first R4 PHP/HTTPS site | Later phase after Docker/Podman qualification and independent security review |

## WordPress demonstrates the critical difference

- **Native**: application files owned by the authorized site identity, compatible PHP-FPM, MariaDB/MySQL, secure WordPress configuration, confined ACLs and website/database restoration. **Docker is not required.**
- **Container**: verified WordPress image and a separately approved database dependency, persistent volumes, networks and ports managed by a container driver.
- A native website does **not** become a container merely by changing UI selection. Cross-engine conversion requires a separate migrator with data export/import, DNS, credentials, backups and recovery.

## Candidate implementation architecture (requires specialist review)

\`\`\`text
ForgePanel App Center (navigation only)
├── ONE-CLICK INSTALL [free]
│   └── NativeRecipeRegistry → NativeInstallPlanner → NativeInstallExecutor
│                                 └── site/PHP-FPM/SQL/files/ACL/quota
└── CONTAINER APPS
    └── ContainerRecipeRegistry → ContainerInstallPlanner
                                  ├── DockerDriver
                                  └── PodmanDriver
                                        → images/volumes/networks/cgroups

Shared read-only catalog search, artifact/version verification, job ledger,
tenant identity, auditing and status conventions are possible. Executors,
runtime drivers, resource namespaces and recovery remain separate.
\`\`\`

The Core must not interpret recipes as **arbitrary shell commands**. Distinct manifest kinds require \`recipe_kind\`, pinned artifact revision, host, organization/tenant/site, resource limits, requested permissions, configuration revision, idempotency and correlation IDs. Linux Go operations remain **typed, allowlisted, scoped and auditable**. No \`shell.exec\` or unreviewed package-supplied scripts.

### Native manifest — proposed fields

\`recipe_kind=native_script\`, ID/app/version/publisher/source/integrity, third-party license, OS/WebStack/PHP/extensions, SQL MySQL/MariaDB/PostgreSQL **only where app-compatible**, secret inputs, confined relative paths, owning account/site, validated settings, typed lifecycle operations, backup/restore, retention and health. Never interpolate user strings into \`chown\`, \`chmod\` or an unrestricted PHP CLI; use constrained allowlisted operations under tenant identity.

### Container manifest — proposed fields

\`recipe_kind=container_stack\`, ID/app/version, qualified driver (\`docker\`/\`podman\`), OS/architecture compatibility, pinned image digests with trust policy, service topology, listener/port ownership, ingress/network, CPU/RAM/PIDs/I/O, image storage and volumes, UID/GID mapping, secret handling, capabilities, prohibited dangerous mounts, dependency startup order, health checks, upgrade/recovery and data-retention policy. A 1Panel \`docker-compose.yml\` is **research input**, not an executable ForgePanel manifest. Arbitrary Compose with host-root bind mounts or Docker socket access is denied by default.

### Jobs and recovery

Each engine independently applies \`DRAFT → PREFLIGHT → APPROVAL_REQUIRED (when applicable) → STAGED → APPLYING → VERIFYING → SUCCEEDED/FAILED/RECOVERY_REQUIRED\`. A durable correlated job and observed state are needed: HTTP acknowledgement or running containers alone is not successful application health. SQL/volume migrations can be irreversible: disclose risks, preserve customer data and test recovery. **Uninstall app is not permission to delete retained data/backups.**

## Candidate access boundaries

Within \`/panel\`, an authorized website manager can install native recipes only for owned websites subject to quotas. Container actions require **separate tenant/server capabilities** even when the same person can install native apps. Within \`/forge\`, administrators manage policies, approved catalogs, host capabilities, network risks and driver availability. Exact child URLs, UI layout, reseller rights and default Container Apps activation are **not yet approved**. A common read-only overview may exist, but installation, backup and action controls must remain separated by engine.

## Verified references — study, not code copying

- [1Panel](https://github.com/1Panel-dev/1Panel) and [appstore dev](https://github.com/1Panel-dev/appstore/tree/dev) package versioned \`apps/<app>/<version>/data.yml + docker-compose.yml\` including image, volumes, networks, parameters and ports. Its [WordPress recipe](https://github.com/1Panel-dev/appstore/blob/dev/apps/wordpress/7.1.4/docker-compose.yml) **runs in Docker**, showing why ForgePanel needs a different native installer.
- [1Panel n8n Compose](https://github.com/1Panel-dev/appstore/blob/dev/apps/n8n/2.47.2/docker-compose.yml) demonstrates image/port/volume/network dependencies; **review security configuration independently** rather than importing upstream Compose settings blindly.
- [1Panel App Store Skills format](https://github.com/1Panel-dev/1Panel-appstore-skills/blob/main/references/appstore-format.md) describes app manifests and optional lifecycle scripts; those scripts do not grant ForgePanel execution authority.
- [Softaculous documentation](https://www.softaculous.net/docs/enduser/install-a-script/) illustrates traditional script installation involving hosting domain, path, database and application administrator, not a mandatory Docker runtime.
- The 1Panel App Store repository declares **GPL-3.0**; copying source, manifests or artwork into a dual-licensed ForgePanel product requires legal/provenance review. App publisher rights and trademarks are separate.

## Open technical choices — not silently approved

- Initial native recipe list, maintenance/security scanning, signature/upgrade cadence, exact qualified OS/runtime combinations.
- Tenant Linux confinement for native applications and tightly bounded application-specific helpers such as WP-CLI.
- Rootless Docker/Podman policy, Compose provider qualification, exceptions for rootful engines, tenant network segmentation and volume ownership.
- App/plan/reseller classification and detailed UI/UX, access policy and host capacity gates.
- Third-party commercial application licenses/support; **this study sets no fee for apps or container management**.
- Single common app-definition table vs two physical registries, schema/migrations, offline signed catalogs, QA evidence.

**Governance:** Architecture → Security → API/IPC → Database → QA/VM → MASTER → Source Code. The first R4 Core PHP/domain/HTTPS milestone does **not** depend on this catalog split. [QA test matrix](../13-tests-quality/app-center-engine-gates.md).
