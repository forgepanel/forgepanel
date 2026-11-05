<!-- forgepanel-doc id=FP-02 revision=7 status=documented -->
# System architecture

[Français](../../fr/02-architecture/README.md) · [Index](../README.md)

## Design baseline versus implementation

The target is a modular Symfony monolith and a separate Go system agent, not a fleet of premature microservices. Hosting, VPS, developer and reseller audiences will be served in phases (Q3); Core stays independent of Hub and premium subscriptions. Symfony owns identity, scoped authorization, UI, API and business workflows. Go owns typed Linux operations and OS/service adapters. PostgreSQL holds application state. A narrow privileged executor is a target boundary, not an existing archive daemon.

```text
Admin / Customer portal (separate hosts and authorization)
                      |
          Symfony control plane -- PostgreSQL
                      |
      private versioned IPC / remote mTLS (planned)
                      |
            Go agent and operation journal
                      |
        bounded privileged operations + OS adapters
                      |
     Linux services / isolated hosting accounts
```

SRC-03 actually contains a CLI, a plan builder, a fixed local console bridge, setup PHP code and SQL. It does not implement the agent IPC above. The bridge executes selected Symfony console actions after dropping root privileges; it is not the future system executor.

## Dependency rules

Domain/application code depends on contracts, not on Debian package names, Nginx paths or a particular UI. OS adapters resolve package/service/security differences. Web profiles compose ingress, routing and runtime drivers. A listener has one owner; mixed stacks require explicit routing or distinct listeners/IPs.

Retain SELinux/AppArmor and detect firewall ownership. Package selection and PHP panel runtime versions remain unqualified for the six targets. The panel runtime/gateway must remain separate from customer stacks so a broken customer configuration does not remove administration.

## Web profiles

`nginx_apache_fpm`, `nginx_fpm`, `apache_fpm`, `caddy_fpm`, `caddy_frankenphp` are the archive's profile identifiers. They validate intent only. For strict `.htaccess` compatibility, route relevant requests through Apache; a Nginx static bypass must not bypass access rules. FrankenPHP worker mode requires application compatibility and per-tenant isolation evidence before enablement.

Configuration changes follow plan, stage, validate, activate, reload, health-check and finalize/compensate. This is a target protocol, not a globally atomic Linux transaction. Destructive data changes need explicit recovery semantics.

The future [Configuration Engine](configuration-engine.md) governs inherited settings and safe plan/validate/backup/recover lifecycle (Q47). Customer runtimes PHP, Node.js, Python and containers (Q4) will be independent from the panel runtime. Not implemented.

Q51 targets [independent Docker and Podman adapters](container-drivers.md) without requiring both on each host. This is a design goal, not a delivered feature.

The Q63–Q69 design is in [services and HA](service-drivers-and-ha.md): local/external DNS/mail, replicated/immutable backups, multi-server orchestration, monitoring and IP/port ingresses. Signing and package distribution appear in [Q61–Q70](../00-project-control/infrastructure-decisions.md). These drivers remain unimplemented.

Under Q79 a [per-site WebStack advisor](site-webstack-advisor.md) will recommend compatible profiles at creation and later support controlled switching with migration plans, `.htaccess`/listener checks and recovery. Q72 allows safe adoption of existing services without overwriting foreign configuration; Q77 phases multi-server management before HA. [Q71–Q80 decisions](../00-project-control/decisions-q71-q80.md).

The new [website lifecycle](website-lifecycle.md) covers Q81–Q90: WebStack advice considering isolation/resources/listeners; maintenance and test-route/progressive transition **where feasible**; PHP-FPM/extensions, ACME TLS, Git staging, SQL/cache engines, file/SSH, webmail, quotas and clone/restore. This is specified, not operational.

Q91–Q100 add [PHP, staging, ACME, access and quota policies](php-staging-and-access-policy.md), plus [cross-server migration with preflight and recovery](cross-server-migration.md). These extend the [website lifecycle](website-lifecycle.md) without delivering running services. Operators will be able to select tenant PHP and per-site Git modes within verified security and capability constraints.

New [Q101–Q110 continuity contracts](runtime-exceptions-and-data-continuity.md) define bounded PHP exceptions, qualified Linux confinement, per-environment Git policies, sensitive staging, multi-CA ACME, shared/dedicated DB with optional replication, temporary SSH, recommended Webmail, quota grace and conditional pre-sync/failover. They are **specified only**; real OS/profile availability needs evidence. [Register](../00-project-control/decisions-q101-q110.md).

Q141–Q147 are detailed in [VM drivers, performance budgets, backup recovery security and SFTP](certification-backup-security.md). Container-only tests do not qualify an OS/WebStack. The external DNS assistant suggests/rechecks without automatic writes. MVP OS update policy is **per server**, backup KMS is optional and beta pause health gates are configurable. [Q141–Q150](../00-project-control/decisions-q141-q150.md). These are specifications, not live services.

[Decisions](../00-project-control/decisions.md) · [Contracts](../08-api-contracts/README.md) · [Security](../10-security/README.md)
