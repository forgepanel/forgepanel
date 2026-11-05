<!-- forgepanel-doc id=FP-02-WEBSITE revision=1 status=specified -->
# Website architecture — WebStack, PHP, TLS, deployment, data and recovery

[Français](../../fr/02-architecture/website-lifecycle.md) · [WebStack advisor](site-webstack-advisor.md) · [Q81–Q90 decisions](../00-project-control/decisions-q81-q90.md)

## Site boundaries

Each site belongs to an identified tenant/account/server and has versioned desired state: domains, isolated Unix owner, document root, WebStack, PHP/PHP-FPM runtime/version/extensions, CPU/memory/process/disk limits, certificates, databases, files and permitted SFTP/SSH, deployment references, backups, staging and observed state. The **Symfony panel runtime** stays separate from customer runtimes.

Hosting plans define **higher-level policies** that sites cannot bypass. Site settings may override inherited account/plan values only with capability and permission. Authorization must be enforced by services, APIs and agents, not just by hiding UI controls.

## Per-site WebStack recommendation and switching (Q81 C, Q82 D and Q79)

On each new website the advisor produces an explainable recommendation based on application/version, `.htaccess`, PHP/extensions, qualified OS/services, isolation/security, resources and listener availability. Eligible profiles among `nginx_apache_fpm`, `nginx_fpm`, `apache_fpm`, `caddy_fpm`, `caddy_frankenphp` are displayed; incompatible profiles cannot be selected. Each IP/port listener has one owner. No customer setting changes the panel's own ingress.

For an existing site, `webstack.planSwitch(site,target,expected_revision)` inventories routes/impact, allows a maintenance window/notifications, snapshots the existing config and uses an **isolated temporary test route** only when supported. **Progressive cutover** is available only when routing can split traffic safely without breaking sessions, writes or access controls. Otherwise warn of a potentially interrupted controlled cutover. Validate service config, TLS, PHP, `.htaccess`, health and recovery/compensation before finalize. Never promise zero downtime or universal SQL rollback.

## Per-site PHP (Q83 C)

Each site chooses a **supported, qualified PHP version** within server/plan policy. Configurable extensions and PHP-FPM directives are typed **allowlisted keys** (e.g. memory, execution time, request/worker limits, uploads) bounded by tenant resources, permissions and OS capabilities. Distinct OS identity for pools/sockets; no unrestricted templating/shell/paths. Policy rejects attempts to weaken host security or reuse the panel's runtime.

## DNS, certificates and renewal (Q84 C)

ACME HTTP-01 and/or DNS-01 depending on actual capability. Wildcard issuance requires an eligible challenge, notably **DNS-01**, plus domain proof and provider support. Imported certificates require key/cert match, lifetime, hostname and access checks. Private keys are never logged or sent to Hub. Renewal uses bounded retries, expiry alerts, drift detection, previous generation retention, reload and health checks. No unauthorized domains.

## Git deployment and staging (Q85 C)

Files/SFTP remain available alongside Git Deploy. Source repository, ref/tag/commit, digest and deployment revision are tracked; deploy keys are protected outside logs. Stage in an isolated directory, validate runtime/dependencies, preview in staging, back up relevant state and activate after health checks. SQL migrations, user uploads and persistent data need separate recovery: **deploying an old commit does not revert them**.

Staging is an **independent resource** with URL/certificate, config, data and secrets. Outbound email/webhooks/public indexing should be disabled or explicitly authorized. Q85 does not select full blue-green/canary CI/CD pipelines; **Q82's WebStack progressive switching** is conditional on real routing capability and separate from application deployment.

## Databases, cache and file access (Q86 D, Q87 B)

Use MariaDB/MySQL and PostgreSQL adapters for tenant DBs. Redis/Valkey are optional cache/queue drivers and must not be exposed publicly without suitable controls. Tenant databases/roles and network/socket access are scoped. ForgePanel Core's PostgreSQL stays **separate from hosted DBs**. Secrets, quotas, backup and access policy require secure configuration.

File manager and SFTP honor Unix ownership, canonical paths, symlink rules and quotas. **Restricted optional SSH** is offered only to authorized accounts, without generic root shells or an implicit web terminal. Suspended accounts and forbidden sessions/paths must be denied.

## Mail and hosting plans (Q88 C, Q89 C)

Where the native/external mail driver actually supports it, offer SPF/DKIM/DMARC, TLS, antispam/antivirus, webmail, quarantine, filters and reports **per domain**, with per-mailbox access and protected secrets. An external provider may expose fewer capabilities; UI must not claim absent features.

Hosting plans define storage, domains, DBs, mailboxes, CPU/memory/processes, PHP versions/extensions and related resources. Show effective inherited values, hard/soft caps, alerts and measured usage. Enforce quotas via qualified OS/system controls (cgroups/quotas), not by GUI counters alone.

## Cloning, restore and data safeguards (Q90 D)

Sites allow **full or selective** (files, DB, config) restore and **staging clones**. Source/destination selection requires authorization and tenant scope, disk check, target snapshot before overwrite, data redaction where appropriate, rotated secrets/URLs and health checks. Cross-environment restore never grants access to data the actor cannot already access. Test real recovery and partial failure; immutable copies and retention follow Q65/Q75.

## State, tests and non-implementation

All stages are durable, audited and idempotent: `PLAN → VALIDATE → SNAPSHOT → STAGE → APPLY/SWITCH → VERIFY → COMMIT/RECOVER`. Test interruption/retry and cross-tenant cases, ACME/DNS/Git outages, incompatible PHP extensions, isolated FPM pools, irreversible SQL changes, accidental public test routes, cloned credentials and partial restore. Hub has neither hosting data nor Linux privileges on customer installations.

**Specification only: no live site engine, Git Deploy, webmail, backup engine or staging UI is currently available.**
