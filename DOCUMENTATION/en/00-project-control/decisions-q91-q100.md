<!-- forgepanel-doc id=FP-00-Q91-100 revision=1 status=specified -->
# Q91–Q100 decisions — Version support, isolation, deployments and migration

[Français](../../fr/00-project-control/decisions-q91-q100.md) · [Decision register](decisions.md) · [Q81–Q90](decisions-q81-q90.md) · [Website lifecycle](../02-architecture/website-lifecycle.md)

## Explicit owner choices (5 November 2026)

Choices **Q91 C, Q92 D, Q93 C, Q94 D, Q95 C, Q96 D, Q97 C, Q98 C, Q99 D, Q100 D** extend Q1–Q90. State **SPECIFIED**, neither IMPLEMENTED nor VERIFIED. ForgePanel remains a complete free AGPL Core with optional private Hub, one brand per organization (Q55) and optional administrator MFA.

| Ref | Confirmed choice | Requirements and boundaries |
|---|---|---|
| Q91 C | **Maintained PHP versions with EOL alerts and planned migrations** | Separate panel and tenant PHP, track package provenance, support schedule, extension compatibility and per-site migration plans. No additional PHP version is certified. |
| Q92 D | **Per-site PHP-FPM pool, quotas and stronger Linux isolation as supported** | Separate identities/processes/sockets, safe filesystem boundaries, CPU/RAM/process caps and qualified SELinux/AppArmor/cgroups policies. An FPM pool alone is not full tenant isolation. |
| Q93 C | **Manual or webhook-driven Git Deploy with validation and per-site policy** | Repository identity/ref, authenticated anti-replay webhooks, signatures/commits per policy, scoped credentials, staging and health checks. A webhook never grants a generic root command. |
| Q94 D | **Per-site staging policy with privacy, distinct secrets, retention and audit** | Files-only or limited-data clone by consent, masking/anonymization, blocked production mail/webhooks, non-indexable domains, retention and controlled purges. |
| Q95 C | **Multiple ACME authorities, DNS-01 adapters, alerts and controlled renewal** | Issuer compatibility, domain ownership, wildcard via eligible challenge, protected DNS credentials, failures and scheduled renewal windows. |
| Q96 D | **Multiple DB engines per account with separate quotas and grants** | Isolated MariaDB/MySQL and PostgreSQL, optional Redis/Valkey for cache/queues; per-resource roles/secrets/quotas. Panel PostgreSQL stays separate. |
| Q97 C | **Key-based restricted SSH with plan rules, revocation, expiry and audit** | Authorized accounts only, OS identity and scoped boundaries; no unrestricted root or implicit web terminal (Q87 B). Validate actual SSH confinement/auth methods. |
| Q98 C | **Swappable Webmail chosen per server/provider with domain policies** | Choose among compatible engines/provider UI, preserve mailbox isolation, DNS/TLS, antispam/quarantine (Q88), and org's single brand. |
| Q99 D | **Soft/hard quotas, alerts, grace and authorized extra allocation** | Inherited plan/account/resource limits with real measurements and notices; temporary extension is bounded/audited by authorized admin, never disables host security or actual disk constraints. |
| Q100 D | **Cross-server migration/restore with compatibility, isolated staging, rotated secrets and audited recovery** | Preflight OS/WebStack/PHP/DB/mail/ports, authenticated encrypted transfer, source/target snapshots, authorized data copying, DNS/TLS cutover and recovery. Do not promise universal restores across incompatible systems. |

## Administration and ownership

Settings remain **scoped and inheritable**: global admin → server → organization → plan → account → site. Lower scopes cannot exceed parent restrictions or access other tenants. UI only offers capabilities verified on the real OS/driver. Sensitive operations follow Q47's `PLAN → VALIDATE → SNAPSHOT → STAGE → APPLY → VERIFY → COMMIT/RECOVER` with idempotency, locks, observed state and disclosed partial compensation.

**Core** owns PHP versions, Linux isolation, Git jobs, DNS-01, data engines, SSH, quotas, Webmail, staging and cross-server migrations. **Hub** may publish version/recipe compatibility and premium entitlements but **never collects private SSH/TLS keys, hosted DB/mail copies or unrestricted shells**. Core essential operations do not require subscription.

## Required verification

- PHP EOL advisory, extension/API preflight, planned change window, application health and recoverability; no automatic destructive end-of-support action.
- Per-site FPM OS isolation for UID/GID, sockets, symlinks, processes and Linux access controls across actually qualified OSes.
- Manual and webhook Git triggers, signatures, replay, invalid refs, altered commits, build failure and secret redaction.
- Staging consent, anonymization, key rotation, outbound suppression, expiry cleanup and tenant separation.
- ACME multiple issuers, DNS credentials/challenges, wildcard, rate limits and failed renewal.
- Multi-DB/cache: role isolation, quotas, network authorization, backups, failure/retry and no public exposure.
- SSH expiry/revocation, hosting-plan limits, logging and constrained commands/paths.
- Webmail/provider compatibility and mailbox/domain quarantine permissions.
- Soft/hard quota crossing, grace exhaustion, authorized allocation, concurrency and real disk capacity.
- Migration across OS/version/profile, capacity failures, interrupted transfer, consistency, DNS/TLS, credentials and verified compensation.

## Open implementation details

Exact supported PHP versions/exception policy, preferred isolation drivers, Git providers/identities, webhook approval rules, staging masking defaults, ACME CAs/DNS adapters, certified SQL/cache engines, SSH identity authority, Webmail providers, grace/quota numbers, migration bandwidth/window and DNS authority. No specific vendor or numeric default is inferred.

**State: owner-approved design documentation. HTTP, SQL, Go agent, Linux and VM implementations/testing remain outstanding.**
