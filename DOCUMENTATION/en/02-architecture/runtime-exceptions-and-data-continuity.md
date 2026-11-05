<!-- forgepanel-doc id=FP-02-Q101-110 revision=1 status=specified -->
# Runtime exceptions, staging, access and continuity policies (Q101–Q110)

[Français](../../fr/02-architecture/runtime-exceptions-and-data-continuity.md) · [Decisions](../00-project-control/decisions-q101-q110.md) · [PHP and staging](php-staging-and-access-policy.md) · [Cross-server migration](cross-server-migration.md)

## 1. Temporary unsupported PHP and qualified confinement

Proposed `PHPVersionException` includes `site_id`, EOL version, package origin, reason, granting administrator, expiry, evidence, risks and `migration_plan_id`. Scope exception to the **approved site and time window**. Show warnings, refuse policy-forbidden new deployments and require a new decision before expiry. Do not automatically delete hosting data or shut down a site without a separately authorized action.

A candidate `SiteIsolationProfile` declares FPM identities/sockets, mounts, quotas, cgroup capabilities, SELinux/AppArmor/systemd policy and **certified OS matrix**. Operators may select only profiles authorized by both their hosting plan and actual host capabilities; reject incomplete/falsely claimed profiles. PHP EOL exceptions cannot disable other isolation protections.

## 2. Per-environment Git approval

Each website environment (`production`, `staging` or another approved environment) has its own `DeployPolicy`: `manual`/`webhook` triggers, allowed refs, authenticated secrets, protected branch, tests, deploy window, initiating grants and configurable approvals. Q76 approval is **per action/environment**; double approval is not silently mandatory for all staging deploys. Verify webhook signature, timestamp and replay before queueing jobs; never treat event payloads as generic root shell commands.

## 3. Sensitive data in staging

`StagingCopyPolicy` may declare `files_only`, `schema_only` or `anonymized_data` (proposed categories), with data classifications. Sensitive content needs a **separate extra approval** recording actor, approver, scope, purpose and lifetime. Protect against reidentification, copied secrets/tokens, real payment callbacks and outgoing email/webhooks, indexing and forbidden access. Enforce bounded retention, controlled purge, deletion tests and explicitly documented legal/audit holds.

## 4. Resilient ACME renewal

An `AcmeIssuerAdapter` declares CA, eligible challenges, accounts, DNS-01, rate limits and fallback terms. Alternative issuers must be **approved in advance**. On failure: bounded backoff retries, alert/escalation, preserve last valid cert until safely replaced; if no safe alternative, create incident/manual recovery. Never skip domain verification or log private keys.

## 5. Shared/dedicated databases and optional certified clusters

Hosting plan declares `database_topology`: **shared** (tenant-isolated roles/DBs) or **dedicated**, permitted engines and limits. Replication/clusters are **optional certified drivers**, not automatic from SQL engine selection. Specify replication guarantees, leader role, failover, backup and restore per engine. Optional Redis/Valkey does not receive public ports or access to other tenants' DBs. Panel PostgreSQL remains separate.

## 6. Temporary SSH, recommended Webmail and quota grace

`SSHAccessGrant` includes Unix user, key or trusted SSH CA certificate, allowed IPs, path/command restrictions, expiry, revocation and audit. Never promise SSH certificates when no qualified CA/driver is available. No generic root or web terminal is implied.

Recommend a Webmail driver only after **security, maintenance and compatibility testing** for the actual server/provider/domain, documenting criteria and migration limitations. Do not silently default to Roundcube or SnappyMail.

`QuotaGracePolicy` is scoped by **plan and resource kind**: soft threshold, hard ceiling, alerts, time-limited grace, Q99 admin-approved allocation and expiry. Grace is not unlimited capacity; reject any extension violating host capacity or security constraints.

## 7. Conditional pre-sync and advanced failover

Migration may follow `snapshot → presync → isolated staging → consistency/final sync → DNS/proxy cutover → verify`, with durable locks, logs, recovery and **measured** RPO/RTO. Active replication/failover is allowed **only when DB, application, storage, network topology and consistency tests support it**. If concurrent writes cannot be reconciled, require a maintenance window or reject the move. Repeated synchronization does not provide distributed transactions or guaranteed zero downtime. [Pipeline details](cross-server-migration.md).

## Exit gates

Disposable OS environments and isolated accounts, real policy engine tests, interruption/recovery cases, secret protection and reviewed emergency operations. All API/types described are **proposals, not working Core code**.
