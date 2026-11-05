<!-- forgepanel-doc id=FP-02-PHP-STAGING revision=2 status=specified -->
# Per-site PHP, Git staging, ACME, access and quota policy

[Français](../../fr/02-architecture/php-staging-and-access-policy.md) · [Website lifecycle](website-lifecycle.md) · [Q91–Q100](../00-project-control/decisions-q91-q100.md)

## Maintained PHP and qualified confinement (Q91 C, Q92 D)

The controller discovers **actually available and maintained** customer PHP versions on each OS/signed channel: version, upstream/vendor EOL, package source, extensions and WebStack compatibility. The panel's **Symfony PHP runtime is never tenant-selectable**. Alerts and planned site migration windows are configurable; an incompatible EOL transition must not silently run or delete site data.

Sites can use a **dedicated PHP-FPM pool**, distinct Unix identity/socket, CPU/memory/process quotas and hardened profiles where actual kernel/OS capabilities are certified (cgroups, SELinux/AppArmor, systemd sandbox, namespaces or other qualified mechanisms). Tenant-private paths/secrets remain inaccessible despite symlinks/socket confusion. An allowed PHP directive cannot override server security ceilings. Proposed `standard`/`hardened` profile names are **candidates**, not verified protection claims.

## Manual/webhook Git Deploy (Q93 C) and private staging (Q94 D)

Select manual, authenticated webhook or both for each site. A Git notification must verify signature/secret, audience, freshness, allowed ref, idempotency, quota and authorization; staging may follow another branch than production. Immutable build inputs, redacted logs, revision tracking and health checks make jobs retryable without arbitrary root scripts.

Production-to-staging copies follow **site-specific policies**: files only or limited DB, consent/approval, redaction/anonymization of sensitive information, rotated secrets, independent URLs/identities, nonindexing and blocked/neutralized **SMTP sends, payment callbacks, outgoing webhooks and destructive jobs** by default. Define retention, expiry, exports and deletion under legal constraints and audit accesses. A read-only database is not the same as anonymized data.

## Multiple ACME CAs and DNS-01 (Q95 C)

Manage ACME accounts, allowed issuers, HTTP-01/DNS-01 by domain ownership/capability, versioned DNS-01 drivers and protected API tokens. Wildcard issuance needs an eligible challenge, typically DNS-01. Renewals have bounded retry/alert policy and certificate/key/hostname checks plus previous config generations; never discard the known-good certificate before new validation.

## Data, SSH and Webmail (Q96 D, Q97 C, Q98 C)

A tenant may allocate multiple MariaDB/MySQL and PostgreSQL engines with **separate identities, quotas, grants and secrets**; Redis/Valkey remain optional cache/queue drivers where supported, with no default public network exposure. Panel PostgreSQL remains distinct from customer databases.

SSH requires authorized keys scoped to plan/account, limited identities/paths/commands, expiry and revocation. Q97 does not add a web terminal or customer root shell; SSH confinement requires Linux certification.

Webmail selection follows capabilities of server and mail provider, with domain/mailbox rights, private messages, filtering, quarantine and TLS. Drivers must be qualified; UI cannot claim unavailable provider features.

## Quota grace without relaxing hard limits (Q99 D)

**Hard** limits respect actual host capacity (disk/inodes/CPU/RAM/processes, mail/DB provider constraints). **Soft** ceilings and warning thresholds may allow a bounded grace or an extra allocation granted by a separately authorized administrator, with expiry/audit. No extension may exceed real capacity, security boundaries or other tenant grants. Show plan/account/site inheritance and measured usage. Commercial entitlements are separate from system authorization.

## Required Q101–Q109 refinements

- **EOL PHP (Q101 C)**: exception scoped to site, owner, reason, expiration and planned migration; disclose risk and record review, never silently renew.
- **Confinement (Q102 C)**: plan/site-selected profiles limited to **OS-certified** Linux capabilities; FPM pools do not replace host enforcement.
- **Deployments (Q103 C)**: distinguish `production` and `staging` manual/webhook, test and approval policies; webhook never elevates privileges.
- **Sensitive staging (Q104 D)**: files/schema/anonymized data profiles; extra approval for sensitive copies, distinct secrets, retention and audit.
- **ACME (Q105 C)**: preapproved alternate CAs, bounded retries, alerts, recovery and retained last-known-good certificate.
- **Databases (Q106 D)**: shared/dedicated by plan, optional clusters/replication **only after driver certification**; tenant scoping remains mandatory.
- **SSH (Q107 C)**: keys, restrictions, allowed IPs, temporary grants and SSH certs only with qualified trust infrastructure, revocation/audit.
- **Webmail (Q108 D)**: recommend an engine only after security/compatibility/maintenance tests; no unqualified default.
- **Quotas (Q109 C)**: grace **per plan and resource kind** with time/cap bounds, never over physical/security limits.

[Q101–Q110 contracts and tests](runtime-exceptions-and-data-continuity.md) · [Decisions](../00-project-control/decisions-q101-q110.md). **None are implemented**.

## Proposed contracts and failures

Candidate `PHPVersionCatalog`, `SiteIsolationPolicy`, `GitDeployTrigger`, `StagingPrivacyPolicy`, `AcmeIssuerAdapter`, `TenantDataService`, `SSHAccessPolicy`, `WebmailDriver`, `QuotaGraceGrant`, each versioned, scoped, capability- and audit-aware. Reject unsupported EOL versions absent an approved exception, replayed webhook, unauthorized Git ref, unconsented staging copies, unavailable DNS adapter, expired SSH access, incompatible Webmail driver and capacity-overriding quota extensions.

**State: contract design only. No PHP/SSH/mail/ACME/Git hosting runtime is VM-certified.**
