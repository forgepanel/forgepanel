<!-- forgepanel-doc id=FP-04 revision=1 status=documented -->
# Native module catalog

[Français](../../fr/04-modules/README.md) · [Index](../README.md)

## Meaning of native

A native module belongs to the reviewed product and uses core contracts. It may be optional to activate, but essential hosting does not require third-party marketplace code. A service is the Linux software managed by a module; an interface is its user-facing entry point. These are not interchangeable concepts.

| Module | Dependencies and scope | Current evidence |
|---|---|---|
| Identity / Authorization | Core state, sessions, permissions, account scope | Initial enrollment prototype only; full RBAC absent |
| Infrastructure / WebStack | OS adapters, listeners, service drivers | Planning identifiers only |
| Hosting / Websites / Domains | Identity, quotas, WebStack, TLS | Planned; no site provisioning |
| DNS / Mail / Database | Domains, service adapters, secrets, backups | `dns`, `mail`, `database` selection tokens only |
| Files / SFTP | Tenant identity, safe paths, storage quotas | `sftp` token; no file manager source supplied |
| Backup / Restore | Storage, secrets, resource consistency | `backup` token; no backup engine |
| Monitoring / Jobs / Updates | Observability, durable execution, trust roots | Read-only doctor and signature-verification prototype only |

## Lifecycle contract

A module declares ID, version, supported core contract, dependencies, capability requirements, permissions, data/migrations, health checks and removal policy. Installation, activation, deactivation, upgrade and removal are separate operations. Deactivation must not silently delete customer data. Removal requires an inventory, retention decision and restoration plan.

Failure must identify the owning resource and pending compensation; other modules cannot assume success from a queued request. Configuration should be generated and validated through the core, not by arbitrary shell hooks. Tests include denied cross-tenant operations, missing dependencies, upgrade failure and recovery.

The detailed [component records](components.md) cover existing prototype units and the required record format. No runtime module manifest/parser or registry is implemented in the inspected archive. A future module is accepted only with its contracts, migrations, tests, monitoring and uninstall behavior documented in both languages.
