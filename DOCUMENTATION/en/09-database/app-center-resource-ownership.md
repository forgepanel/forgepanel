<!-- forgepanel-doc id=FP-09-APP-OWNERSHIP revision=1 status=specified -->
# App Center — candidate data ownership and resource reservations

[Français](../../fr/09-database/app-center-resource-ownership.md) · [Database](README.md) · [Recipe contract](../08-api-contracts/app-center-recipe-contracts.md)

**DRAFT / PROPOSED ONLY.** This is a conceptual data model, **not a PostgreSQL DDL migration, approved table layout, running code or a new product decision**. Final ownership, constraints, migrations, retention, row-level authorization and recovery require Database/Security/API specialist review. Existing Q1–Q170 decisions remain authoritative; Q171+ remain open.

## Separate identities and immutable variant types

| Candidate concept | Purpose | Required boundary |
|---|---|---|
| `AppDefinition` | Common name, app family, publisher and localized description | Does **not** represent an executable installation |
| `AppRecipeVariant` | Owner-reviewed immutable version + `recipe_kind`, digest/license/compatibility | `native_script` and `container_stack` **cannot share** a variant key or installation recipe identity |
| `AppInstallation` | Actual host/tenant/account/site context, recipe version, desired/observed state | Must record precisely one engine; no engine conversion by UPDATE |
| `AppNativeResources` | Owned website, document-root files, scoped SQL grants, PHP/site quotas | Cannot reference OCI image store/network as its install resource |
| `AppContainerResources` | Qualified engine, image digest, container/volume/network/port ownership and cgroup limits | Cannot take over native site files/SQL or reserved FORGE/PANEL ports |
| `AppOperation` | Durable, tenant-scoped request, state transition, actor, revision, idempotency/correlation | Independent native/container operation namespace and authorization |
| `AppBackupReference` | Backup target kind, tenant/engine identity, restore coverage and retention policy | Native site+SQL versus container volumes/config/SQL require different consistency checks |
| `AppResourceReservation` | Proposed locks/leases for disk, database grants, port and host capacity | No double allocation; receipt is not an applied Linux effect |

These are **names of candidate logical entities**, not pre-approved schemas or table names. The Core's PostgreSQL control plane must not be confused with tenant MySQL/MariaDB/PostgreSQL data. The private Hub may publish reviewed metadata, never own tenant installation records, files, database passwords or persistent volume data.

## Constraints to review before DDL

- An installation selects **exactly one** immutable recipe kind and version/digest. Changing native to container requires a new, reviewed migration process and a different installation identity.
- A `native_script` plan can allocate only resources of its authorized tenant website. A `container_stack` plan uses approved Docker/Podman capabilities and separate quotas, security and networking.
- Proposed idempotency uniqueness must include tenant, engine kind, target resource, operation and client token; retries cannot change actor/scope, package digest or destination silently.
- Port ownership and Linux resources are verified in the **observed system** (not only a row in PostgreSQL). Reserve 8447 FORGE and 8446 PANEL against container host-port collisions.
- Storage and backups are not garbage-collected by recipe removal alone; data/retention approval and verifiable restoration must be explicit.
- Missing host capabilities, unsigned packages, unverified publisher and capacity faults are **fail-closed**, without granting commercial or system privileges.
- Model partial success and unrecoverable migrations explicitly; an SQL transaction does not roll back filesystem/container effects automatically.
- Hub catalog unavailability does not disable the free native catalog in the local Core.

## Audit and lifecycle

`DRAFT → PREFLIGHT → APPROVAL_REQUIRED? → STAGED → APPLYING → VERIFYING → SUCCEEDED / FAILED / RECOVERY_REQUIRED` is a **candidate job workflow**, not an adopted enum. Include state history and source authorization, redacted diagnostics, operation correlation and transaction/recovery proof. Restore operations must be isolated to their owning engine and tenant, with no cross-engine implicit conversion.

## Gate and evidence

[Candidate fixtures and validator](../08-api-contracts/app-center-recipe-contracts.md) have **metadata-only tests**; [32 functional/VM scenarios](../13-tests-quality/app-center-engine-gates.md) remain PLANNED. Exact DDL, migrations, indexes, locking strategy, transactional boundaries, backup storage and retention are **not** defined or approved in this document.
