<!-- forgepanel-doc id=FP-00-Q81-90 revision=1 status=specified -->
# Q81–Q90 decisions — Hosting, websites and recovery

[Français](../../fr/00-project-control/decisions-q81-q90.md) · [Register](decisions.md) · [Per-site WebStack](../02-architecture/site-webstack-advisor.md) · [Website lifecycle](../02-architecture/website-lifecycle.md)

## Owner decisions — 5 November 2026

All ten choices **Q81 C, Q82 D, Q83 C, Q84 C, Q85 C, Q86 D, Q87 B, Q88 C, Q89 C, Q90 D** are confirmed and extend Q1–Q80. They are **specified only**: no working hosting modules or real VM/browser integration have been demonstrated. Free AGPL Core remains independent of Hub and subscriptions. Optional admin MFA, one brand per organization, sensitive reauthentication and Q47 recovery planning remain in force.

| ID | Confirmed decision | Requirements and boundaries |
|---|---|---|
| Q81 C | **WebStack advisor based on application, .htaccess, PHP, OS, isolation, security, resources and listeners** | **Per-site** recommendation (Q79) with explainable evidence; incompatible profiles blocked; no unmeasured performance claims. |
| Q82 D | **WebStack switching with preview, backup, maintenance/notice, temporary-route testing or progressive cutover where feasible** | Authorized versioned plan, isolated test route, protected TLS/access policy, cutover/recovery without altering other sites. Progressive cutover is topology-dependent and zero downtime is not guaranteed. |
| Q83 C | **Per-site PHP versions, extensions, PHP-FPM settings and resource quotas** | Isolated Unix FPM pools, safe directives, permitted versions and plan/account/site inheritance. Panel PHP remains separate. A PHP setting never confers host privileges. |
| Q84 C | **Automatic ACME, custom certificates, DNS-01, wildcards, renewals and alerts** | Domain ownership, compatible DNS/ACME, protected keys and renewal policy; wildcard validation requires an eligible challenge, typically DNS-01. |
| Q85 C | **Files/SFTP, Git Deploy, staging/preview, backups and controlled recovery** | Permissioned versioned deployment with code/data/secrets distinguished. Advanced blue-green/canary pipelines are **not selected** by Q85. |
| Q86 D | **MariaDB/MySQL, PostgreSQL and optional Redis/Valkey adapters** | SQL drivers for DBs and cache/queue drivers for Redis/Valkey where available. Separate tenant scope/quota; Core's own PostgreSQL is not automatically a client DB. |
| Q87 B | **Web file manager, SFTP and restricted SSH for authorized accounts** | Per-tenant OS identity, safe paths, quotas and limited/audited SSH access. **Web terminal is not selected**. |
| Q88 C | **SPF/DKIM/DMARC/TLS, antispam/antivirus, webmail, quarantine, filters and per-domain reports** | Domain/mailbox owner-scoped UI, protected secrets and isolation, subject to actual mail engine capabilities. Advanced legal archiving not selected. |
| Q89 C | **Hosting plans/quotas (disk, domains, mail, DB, CPU/RAM/processes/PHP) with inheritance, alerts and usage** | Parent policy cannot be bypassed; show measured usage, soft/hard limits and enforce at service/agent boundary. |
| Q90 D | **Full/selective restore, recovery tests, staging clone and controlled cross-environment restore** | Resource owner consent, versioned plan, independent identities/secrets/target environment; no copying of production credentials by default; backup before overwrite. |

## Administrable model and dependencies

`organization → hosting plan → account → website/application` governs permitted PHP versions, extensions, quotas, WebStack, certificates, storage, databases, file access and recovery. Every setting declares effective value, provenance, permission and actual OS/service capability. Unavailable capability is disclosed, never simulated.

**Configuration Engine** applies high-impact changes through `PLAN → VALIDATE → SNAPSHOT → STAGE → APPLY → HEALTH CHECK → FINALIZE / RECOVER`. Linux changes are not globally atomic; SQL/data side effects may require manual recovery. Q54 still prioritizes **shared hosting + VPS**, with later advanced features in phases. Optional services need not be installed on every host.

## Security and Core/Hub separation

Tenant content (files, mail, DB, private TLS/SSH keys, SQL dumps and credentials) remains with **Core or the explicitly selected provider**. Private Hub may publish compatible recipes/plugin metadata but **cannot read or administer customer site data**. Paid entitlements confer neither Core RBAC nor Linux permissions. Quotas/deployments must not cross tenant boundaries.

## Required verification

- Per-site recommendation/routing, `.htaccess`, listeners, temporary/progressive cutover, cutover interruption and recovery.
- OS-qualified PHP versions, distinct FPM pools, forbidden directives, enforced isolation/quotas.
- ACME DNS-01/wildcard, failed challenge, key handling, renewals and imported certs.
- Git Deploy and staging; code rollback versus irreversible SQL migration, secret preservation.
- MariaDB/MySQL, PostgreSQL, Redis/Valkey scope, sockets, auth, backup/restore, cross-tenant denial.
- File manager/SFTP/SSH path traversal, symlinks, permission failures and suspended accounts.
- Open-relay prevention, SPF/DKIM/DMARC, private quarantine and mailbox/domain webmail authorization.
- Plan inheritance, child ceilings, concurrent accounting, overuse and alerts.
- Safe clone/restore with consistent DB, rotated credentials, no outbound staging mail by default, privacy and rollback.

## Still open

Actual DNS/ACME/storage/webmail providers; panel PHP version versus client PHP EOL policy; Git provider and deploy-key model; default database driver; certified isolation/quota implementation; storage/backup schedule; personally identifiable content handling during cloning. No implicit defaults or providers are chosen.
