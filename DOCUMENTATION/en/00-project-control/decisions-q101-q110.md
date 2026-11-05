<!-- forgepanel-doc id=FP-00-Q101-110 revision=1 status=specified -->
# Q101–Q110 decisions — Exceptions, policies and continuity

[Français](../../fr/00-project-control/decisions-q101-q110.md) · [Decision register](decisions.md) · [Q91–Q100](decisions-q91-q100.md) · [Operating policies](../02-architecture/runtime-exceptions-and-data-continuity.md)

## Explicit owner decisions — 5 November 2026

Choices **Q101 C, Q102 C, Q103 C, Q104 D, Q105 C, Q106 D, Q107 C, Q108 D, Q109 C, Q110 D** extend **Q1–Q100** without superseding them. Status **SPECIFIED**: documentation does not implement, deploy or certify these services. Free AGPL Core remains Hub-independent, administrator MFA **optional**, **one brand per organization**, Q47 and effective RBAC retained.

| Ref | Confirmed choice | Scope and safety |
|---|---|---|
| Q101 C | **Administrator-authorized temporary EOL PHP exceptions with planned migration** | Explicit scoped exception, owner, rationale, expiry, visibility and audit; no silent renewal or permanent bypass. Unsupported versions remain identified as risky. |
| Q102 C | **Isolation profiles selectable by plan/site based on certified Linux capabilities** | Parent policy and permissions, typed allowlisted profiles; Unix identities/FPM pools, cgroups/SELinux/AppArmor only after OS validation. UI selection is not proof of confinement. |
| Q103 C | **Manual/webhook Git Deploy policy by site AND environment, configurable approval** | Separate staging/production rules for branches/ref, actors, signed events and tests; webhooks never execute generic root shells. |
| Q104 D | **Per-site staging copy profiles with special approval for sensitive data, retention and audit** | Files-only, schema or anonymized data by policy; enhanced approval for sensitive information, isolated secrets and disabled production communications, safe redaction and expiry. |
| Q105 C | **Multiple ACME issuers, bounded retries, alerts and recovery procedure** | Allowlisted CAs/DNS-01, provider limits, credentials, challenges/hostnames; keep the last valid certificate until a safe replacement is active. |
| Q106 D | **Shared or dedicated DB services by plan, optional clusters/replication through certified drivers** | MariaDB/MySQL and PostgreSQL, optional Redis/Valkey; separate identities/quotas/scopes and tested replication/leader/quorum semantics. |
| Q107 C | **SSH keys, restrictions and allowed IPs, temporary access and SSH certificates when compatible** | Plan policy, expiry/revocation, audit, permitted paths/commands and protected keys; certificates require a trusted CA and verified lifecycle. |
| Q108 D | **Webmail recommended after security, compatibility and maintenance testing** | No unqualified default engine; later choice by server/provider/domain (Q98), mailbox/TLS/antispam/quarantine compatibility and permissions. |
| Q109 C | **Quota grace duration and cap configurable per plan AND resource type** | Soft/hard limits, warnings, bounded allowance; separately authorized admin extension (Q99), never above physical capacity or isolation. |
| Q110 D | **Pre-sync, staging, DNS/proxy switch and advanced replication/failover when compatible** | Source/target checks, DB consistency and concurrent writes, secret safety, maintenance windows, health tests and recovery; replication does not imply zero downtime or atomicity. |

## Settings and trust boundaries

`global → server → organization → plan → account → site → environment` determines effective settings and permitted overrides **within parent constraints**. EOL exceptions are audited and time-limited, not general security shutdown switches. Operation approvals, backup, revisions, capability evidence and retention are enforced by service/agent. High-impact work uses **PLAN → VALIDATE → SNAPSHOT → STAGE → APPLY → VERIFY → COMMIT/RECOVER**, including progressive migration and data transfer.

**Core** owns PHP, isolation, Git, staging, ACME, DB/storage, SSH, Webmail, quotas and destination servers. **Private Hub** publishes package prerequisites/versions and optional premium entitlements, but **does not perform migration, issue customer SSH certificates, or collect hosted databases, files or messages**. Paid rights never substitute for Linux authorization.

## Future verification (not performed)

- Expired PHP exceptions, migration and recovery; owner notification; no automatic unreviewed renewal.
- Unavailable isolation profile, child override, symlink/socket/FPM escape, cgroups and SELinux/AppArmor OS checks.
- Production webhook without approval, replay, site/environment confusion, failed builds and secrets in logs.
- Sensitive staging without extra approval, ineffective masking, real mail/callbacks, cleanup and audit evidence.
- ACME rate limits, DNS provider outage, unauthorized fallback CA, renewal failure and retained valid certificate.
- Shared/dedicated/cluster database tenancy, failover/lag/split-brain, consistent restore and denied uncertified engines.
- Temporary/certified SSH expiry/revocation, forbidden IP, compromised CA and unauthorized commands.
- Webmail outdated/incompatible driver, mailbox/domain isolation and migration safety.
- Distinct disk/CPU/mail grace periods, actual host exhaustion, authorized extension and concurrency.
- Pre-sync, concurrent writes, TTL/proxy switch, incompatible app, failed failover and audited compensation.

## Open parameters

Max PHP exception window, OS-qualified isolation profiles, default production approvers, sensitive-data classification/masking rules, ACME issuer order, default DB/cache topology, SSH CA/access lifetimes, Webmail recommendation criteria, numeric quota grace/caps, and failover RPO/RTO thresholds. **No vendor or numeric default is silently selected.**
