<!-- forgepanel-doc id=FP-02 revision=1 status=documented -->
# System architecture

[Français](../../fr/02-architecture/README.md) · [Index](../README.md)

## Design baseline versus implementation

The target is a modular Symfony monolith and a separate Go system agent, not a fleet of premature microservices. Symfony owns identity, scoped authorization, UI, API and business workflows. Go owns typed Linux operations and OS/service adapters. PostgreSQL holds application state. A narrow privileged executor is a target boundary, not an existing archive daemon.

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

[Decisions](../00-project-control/decisions.md) · [Contracts](../08-api-contracts/README.md) · [Security](../10-security/README.md)
