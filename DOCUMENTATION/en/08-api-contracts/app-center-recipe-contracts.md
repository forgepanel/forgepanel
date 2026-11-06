<!-- forgepanel-doc id=FP-08-APP-RECIPE revision=2 status=specified -->
# App Center — discriminated recipe contracts and admission boundaries

[Français](../../fr/08-api-contracts/app-center-recipe-contracts.md) · [API index](README.md) · [Two-engine policy](../06-apps-recipes/app-center-engines.md)

**Status: DRAFT SPECIFICATION / CANDIDATE-ONLY.** No production manifest parser, installer, Docker/Podman handler, Symfony endpoint or catalog executor has been implemented. The owner's confirmed product choices are the **free native One-Click engine**, the **separate Docker/Podman Container Apps engine**, and no runtime mixing. The exact schemas and resource policies below remain technical candidates requiring specialist review. Q171+ remain open.

## Common envelope — candidate version 1

Each candidate is a JSON object with explicit `schema_version=1`, `contract_status=CANDIDATE_ONLY` and `execution_allowed=false`. It identifies `app_id`, `variant_id`, `app_version`, `publisher_id`, `recipe_kind`, `artifact` (HTTPS origin, SHA-256 and third-party license identifier), and exactly **one** execution-specific object:

- `recipe_kind=native_script`: only `native`, never `container`. `native` identifies the owned website/tenant scope, a **supported** native runtime, a compatible SQL engine if required and required runtime extensions. It is an abstract **install plan**, not an accepted shell script. The future installer may use only independently approved, typed and tenant-confined operations.
- `recipe_kind=container_stack`: only `container`, never `native`. `container` identifies an explicitly qualified driver **DOCKER** or **PODMAN**, a non-empty set of pinned OCI image digests, separately declared persistent volumes and bounded positive CPU/RAM/PID requests. Root privilege, Docker/Podman sockets, host-root bind mounts, untrusted Compose providers, host networking and uncontrolled ports are forbidden by default. A Docker Compose file is *not* the candidate execution format.

The `app_id` may be shared by both kinds, but `variant_id` and `recipe_kind` identify **different installation definitions**. Installed resource IDs, entitlement checks, upgrade histories and backups cannot be shared or silently migrated across engines.

## Two non-executable synthetic examples

The files [native fixture](../../../evidence/app-center-fixtures/native-cms.v1.json) and [container fixture](../../../evidence/app-center-fixtures/container-worker.v1.json) contain **invented fixture identities and non-resolving example.invalid origins**. Their digests are syntactic test values, not real checked downloads. **Never use them to install applications, grant permissions or publish packages.**

The [offline admission validator](../../../scripts/validate_app_center_recipe.py) checks only these candidate shapes and some essential fail-closed invariants. It does **not** execute commands, inspect Docker/Podman, access SQL, download anything, validate artifact signatures, evaluate real host capacities or authorize installation. It must never be used as the sole production security control.

**Fixture limitation, not a product restriction:** the current offline candidate validator recognizes only `PHP_FPM` for synthetic native examples. This does **not** remove Q4 targets for Node.js, Python or other qualified native runtimes. Each additional native runtime requires a separate reviewed handler, security model, compatible WebStack, quotas and dedicated VM tests before inclusion. The requested **free ONE-CLICK INSTALL engine** remains the product boundary; this particular fixture is not the complete application catalog.

## Planned request and lifecycle boundary

A future Core API shall distinguish `native.planInstall` from `container.planInstall` and route them to different typed executors. Both need authenticated tenant/host scope, effective resource ownership, host capabilities, manifest version/digest, operation revision, idempotency key, correlation ID and signed/approved provenance. The Core **re-authorizes locally** even if a Hub catalog entry is shown as approved. Hub absence must not disable the free native catalog.

An admitted *metadata document* is not an admission to perform Linux operations. No executable handler may accept an unknown manifest property, a shell command, a raw Compose blob, raw PHP snippets, unrestricted filesystem paths, client-provided privileged arguments or an unreviewed arbitrary script URL.

### Native-only security and resources

A native install requires owned-site identity, isolated PHP-FPM or other qualified site runtime, site storage/inode limits, DB permissions scoped to its database, safe archive extraction and canonical filesystem checks. Protect symlinks, path traversal, hidden nonpublic configuration, secrets, upload directories and background jobs. Backups must cover **files and consistent SQL**; an app-level update and SQL schema rollback are different problems. One-Click Installer access is **free even when Hub is offline**, without Docker/Podman.

### Container-only security and resources

A container stack requires a separately qualified Docker **or** Podman driver and its exact Compose/provider behavior (if any). Enforce namespaces, rootless/capability strategy, cgroup CPU/RAM/PID budgets, image storage, persistent volume quotas, network reachability, ports, logs and secret handling. A running container or successful image pull does **not** prove app health. Preserve volumes/data on uninstall unless explicitly authorized; reject privileged containers, host socket and sensitive mounts by default.

## Explicit cross-engine failure outcomes

- Unknown `recipe_kind`, both `native` and `container` supplied, or the wrong-specific field: **REJECT_TYPE_MISMATCH** before resource allocation.
- Unknown field such as `command`, `shell`, `compose_file`, `env_file`, `host_path`, `privileged` or unapproved `hooks`: **REJECT_UNREVIEWED_FIELD**.
- Unpinned image, non-HTTPS artifact origin, malformed checksum, missing tenant provenance or license: **REJECT_UNTRUSTED_ARTIFACT**.
- Runtime/driver unsupported or no resources available: **BLOCKED_CAPABILITY**, not automatic fallback to the other engine.
- Any candidate with `execution_allowed=true` or claimed production approval: **REJECT_UNAPPROVED_EXECUTION**.

Codes above are **proposed error taxonomy**, not implemented API enums. Safe failure must have no Linux side effect and must keep existing site/DB/volume data intact. Every real action later needs a durable job ledger, policy-versioned audit and recovery. An HTTP acknowledgment is not a successful installation.

## Ownership and remaining gates

- **API/IPC**: versioned typed contracts and explicit deny rules for each engine.
- **Database**: proposed shared application identity with distinct variant, installation, quota, job, resource and backup ownership; no tables/migrations approved.
- **Security**: no generic privileged shell, signature/provenance validation and tenant isolation; test malicious archives, Compose/path injections and resource exhaustion.
- **QA**: [32 integration scenarios](../13-tests-quality/app-center-engine-gates.md) are **PLANNED**, while offline contract-check tests may pass independently.
- **Operations**: first Core PHP/HTTPS R4 remains prior to either application installer. No release, service, OS validation or paid feature change is implied.

[Core native/container boundary](../06-apps-recipes/app-center-engines.md) · [R&D driver qualification](../02-architecture/container-drivers.md).
