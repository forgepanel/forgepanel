<!-- forgepanel-doc id=FP-04 revision=7 status=documented -->
# Native module catalog

[Français](../../fr/04-modules/README.md) · [Index](../README.md)

## App Center — independent application engines

The owner-confirmed App Center navigation contains **ONE-CLICK INSTALL** (free native scripts without containers) and **CONTAINER APPS** (separate Docker/Podman-powered deployment). Permissions, resources, quotas and restoration contracts remain distinct. Neither mode may require publisher Hub or generic root shell access. [Architecture and third-party reference audit](../06-apps-recipes/app-center-engines.md) · [Planned tests](../13-tests-quality/app-center-engine-gates.md). No app installer is currently implemented.

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

## Q63–Q68 native module responsibilities

The design includes local/external DNS (Q63), native/external mail (Q64), encrypted replicated/immutable backup and restore (Q65), integrations and alerting (Q68), and multi-server/HA agents (Q67). Modules expose capabilities, authorization and observed state; no optional service is implicitly installed. HA is a phased target, not necessarily part of the first hosting milestone. [Architecture](../02-architecture/service-drivers-and-ha.md).

## Module selection and adaptation (Q72–Q79)

The installer may detect/adopt existing services following inventory, permission and recovery planning (Q72), never silently take ownership of foreign files. DNS local engine is recommended after driver testing (Q73); Postfix/Dovecot first mail driver with external providers/relays (Q74); 3-2-1 backup and restore drills (Q75); Prometheus/OpenTelemetry adapters (Q78). For every website Core recommends a WebStack without imposing it and later allows a **controlled switch** (Q79). [Details](../00-project-control/decisions-q71-q80.md).

## New Q81–Q90 module capabilities

Hosting scope now includes per-site WebStack recommendation and safe switching, PHP-FPM versions/extensions/quotas **per site**, ACME/imported certificates, Git Deploy and staging, MariaDB/MySQL and PostgreSQL drivers, optional Redis/Valkey cache, file manager/SFTP/restricted SSH, per-domain webmail/quarantine, inherited plan/quotas, selective restore and staging clones. Features remain capability- and plan-dependent; paid Hub entitlements never gate essential security. These services are **not implemented**. [Architecture](../02-architecture/website-lifecycle.md).

## Q91–Q100 target modules

Website management now targets a **maintained PHP catalog with EOL notices/planned migration** (Q91), **per-site FPM pools and stronger Linux profiles** (Q92), **manual/authenticated-webhook Git Deploy** (Q93), privacy-controlled staging (Q94), **multi-CA ACME/DNS-01** (Q95), per-account multi-engine SQL/cache grants (Q96), plan-scoped restricted expiring SSH (Q97), provider-selectable Webmail (Q98), quota alerts/grace/approved allocation (Q99) and safeguarded cross-server migration (Q100). Core gains no implicit web terminal and Hub cannot store site data. [Decisions](../00-project-control/decisions-q91-q100.md).

## Q101–Q110 module policies

Future modules declare OS/plan/site capabilities for time-limited PHP EOL exemptions with migration (Q101), certified Linux isolation (Q102), manual/webhook Git with per-environment approvals (Q103), privacy-preserving staging with special sensitive-data approval (Q104), multi-CA ACME recovery (Q105), shared/dedicated DB with **optional certified** replication (Q106), temporary/qualified SSH certificates (Q107), test-recommended Webmail (Q108), per-resource quota grace (Q109) and conditional pre-sync/advanced failover (Q110). Core owns execution and tenant data. [Decisions](../00-project-control/decisions-q101-q110.md).

## Lifecycle contract

A module declares ID, version, supported core contract, dependencies, capability requirements, permissions, data/migrations, health checks and removal policy. Installation, activation, deactivation, upgrade and removal are separate operations. Deactivation must not silently delete customer data. Removal requires an inventory, retention decision and restoration plan.

Failure must identify the owning resource and pending compensation; other modules cannot assume success from a queued request. Configuration should be generated and validated through the core, not by arbitrary shell hooks. Tests include denied cross-tenant operations, missing dependencies, upgrade failure and recovery.

The detailed [component records](components.md) cover existing prototype units and the required record format. No runtime module manifest/parser or registry is implemented in the inspected archive. A future module is accepted only with its contracts, migrations, tests, monitoring and uninstall behavior documented in both languages.
