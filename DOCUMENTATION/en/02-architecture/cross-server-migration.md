<!-- forgepanel-doc id=FP-02-XSERVER revision=2 status=specified -->
# Cross-server website migration — planning, compatibility and recovery

[Français](../../fr/02-architecture/cross-server-migration.md) · [Website lifecycle](website-lifecycle.md) · [Q91–Q100 decisions](../00-project-control/decisions-q91-q100.md)

## Q100 D goal

An authorized operator may plan **migration or restoration of a website between two ForgePanel servers**, optionally through isolated staging. The source/destination are independently authenticated, tenant ownership is checked, and transfer is approved **at both scopes**. No generic root shell is exposed. Production data, mail, backups and personal information must not be routed through commercial Hub.

## Discovery, preflight and capabilities

Build a versioned compatibility matrix: OS/architecture, storage/quota, Unix account, DNS/ACME, IP/port/listeners, WebStack and `.htaccess`, PHP/versions/extensions/FPM isolation, MariaDB/MySQL/PostgreSQL, optional Redis/Valkey, persistent storage, cron/jobs, SSH/SFTP, mailboxes and certificates. Show **blocking mismatches**, repairable differences and missing dependencies; never create accounts on targets lacking actual isolation support.

## Migration pipeline

1. **DISCOVER/AUTHORIZE**: authenticate source/destination agents, owners and permissions; scope data/consent and time window.
2. **PLAN/PREVIEW**: compatibility, risk, maintenance window, estimated size/cost, potential overwrite, DNS/TLS strategy and policy revisions.
3. **SNAPSHOT**: consistent source/target backups, known SQL snapshot point, protected secrets and audit; require tested last-known-good recovery where feasible.
4. **TRANSFER**: authenticated encrypted channel, digests/integrity and resumable idempotent chunks with quotas/rate limits, never via Hub billing.
5. **STAGING/ADAPT**: isolated OS/app identity, rotated necessary credentials, compatible PHP/DB/WebStack, test URLs, disabled outbound jobs and site privacy/retention.
6. **VERIFY**: HTTP/TLS/.htaccess, PHP/SQL, application, mail, quotas, restore readiness, network leak prevention and site health.
7. **CUTOVER**: authorized DNS/proxy/frontend switch, with warnings for TTL, propagation, sessions, queued mail and concurrent writes. Require maintenance or deny if consistency cannot be ensured.
8. **COMMIT/RECOVER**: persist resource ownership, revisions and durable job status; keep source backup and remove it by policy; on failure offer explicit restore and report irreversible effects.

High-risk changes follow Q47. SQL schema migrations and third-party email cannot be undone by simple configuration rollback. Q100 does **not** choose active bidirectional data replication for application workloads.

## Q110 D — presynchronization and conditional advanced failover

The Q100 pipeline remains; Q110 adds **pre-sync** of files/data with digests and resumable transfer, **staging verification** and final synchronization followed by controlled **DNS/proxy cutover**. **Advanced replication/failover** is optional and only where application, SQL, storage, network, leader selection, session and transaction compatibility is tested for the OS/versions involved. Concurrent writes need proven consistency or a defined freeze/maintenance window. If uncertified, offer a traditional announced-interruption migration, **never guaranteed zero downtime**. Measure actual RPO/RTO, protect credentials, back up source/target, and document failback and irreversible effects.

[Q101–Q110 policy](runtime-exceptions-and-data-continuity.md).

## Security boundaries

- Protect **source secrets**; regenerate necessary credentials/tokens for target, never export SSH/TLS private keys by default.
- Check destructive target-overwrite risk, file/symlink permissions and DB user mapping before applying.
- Staging must not send production email, process real payments, call real webhooks or become indexed without explicit permission.
- Keep Core PostgreSQL isolated from hosted DB services.
- Durable backups follow Q65/Q75 (encrypted/offsite/immutable, 3-2-1 and restoration drills).
- Air-gapped or uncertified host migrations require a reviewed secure-import workflow, **not** presumed universal support.

## Acceptance tests (not run)

Two authorized VMs with different OS/WebStacks, interrupted transfer after snapshot, wrong-tenant denial, unsupported PHP, insufficient storage, concurrent DB writes, delayed DNS, key rotation/recovery, outbound staging suppression, duplicate jobs and unclear cutover state. Verify both restored data and lack of impact on neighboring sites.

**State: specified only. No working cross-server migrator, two-phase commit, cluster or production restore engine exists.**
