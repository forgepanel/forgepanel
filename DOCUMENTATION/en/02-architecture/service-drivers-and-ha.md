<!-- forgepanel-doc id=FP-02-SERVICES revision=1 status=specified -->
# Local/external service drivers, backups and multi-server orchestration

[Français](../../fr/02-architecture/service-drivers-and-ha.md) · [Architecture](README.md) · [Q61–Q70 decisions](../00-project-control/infrastructure-decisions.md)

## DNS and mail adapters (Q63 C, Q64 C)

Every service exposes **capabilities** before configuration is offered. DNS adapters declare provider, managed zones, RRset operations, TTL, validation, propagation, DNSSEC if supported and safe remove semantics. A zone has one logical owner at a time; the controller rejects competing provider updates. Moving local/external authority is an explicit migration with records and delegation verification.

Mail drivers declare mailboxes, aliases, domains, quotas, transport, TLS policies, antispam/antivirus where supported and DNS prerequisites (SPF, DKIM, DMARC, MX). Distinguish local hosting, outgoing relay and external service provider capabilities. A provider is not silently selected; ports, certificates, secrets, sender reputation and open-relay risks are checked during PLAN. No single PowerDNS/Postfix/Dovecot backend has been imposed.

## Backup and DR (Q65 D)

Coverage must distinguish:
- ForgePanel configuration and application PostgreSQL, encryption keys, hosted accounts/sites, databases, mail and volumes;
- local/remote destination, replication, encryption, versions, retention/immutability, capacity and cost;
- provenance and restore: versioned manifests, isolated recovery drills, key availability and data integrity;
- incidents: node recovery plans, authorized manual/automatic steps and **measured** RPO/RTO.

Immutability alone neither replaces multiple locations nor proves recoverability. Never claim deletion-resistant features unsupported by the destination provider.

## Multi-server and HA (Q67 D)

The central Core stores **desired state**, each Go agent reports **observed state**. Operations need unique IDs, idempotency, scopes, durable locks and results. Server groups, policy assignment, workload moves, failover and replication require explicit contracts; hosted services must not depend on controller reachability.

HA requires quorum boundaries, split-brain detection, fencing/leases, consistent backups and recovery procedures. A distributed PostgreSQL database, replicated DNS or shared storage do **not** become available merely by installing ForgePanel. Clustering is a later phase under Q54, enabled only for certified setups.

## WebStacks and listeners (Q69 D)

Planning IDs `nginx_apache_fpm`, `nginx_fpm`, `apache_fpm`, `caddy_fpm`, `caddy_frankenphp` denote possible compositions, not installed profiles. Frontends coexist **on distinct IP/listeners** or behind a clearly configured ingress router. Each IP:port/protocol tuple has one owner. Per-site profile choice is possible only if the network topology actually delivers requests correctly. Apache `.htaccess` is bypassed when Nginx serves static content directly; protect at first ingress or route required requests through Apache in strict mode.

For each versioned configuration: plan, service config tests, TLS/listener validation, stage, activate, reload, health-check, compensate when needed. A customer frontend outage must not remove panel administration.

## Monitoring (Q68 C)

Collect local metrics, configure alert rules, email/webhooks and third-party exporters under permissions and consent. Deduplicate, suppress notification storms, support silencing, escalation and acknowledgment. Never automatically export sensitive tenant data, secrets or identifiers to external monitoring systems.

**State: design only.** Adapters, HA and recovery still need real OS/VM tests before VERIFIED status.
