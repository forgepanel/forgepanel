<!-- forgepanel-doc id=FP-06 revision=2 status=documented -->
# Applications and installation recipes

[Français](../../fr/06-apps-recipes/README.md) · [Index](../README.md)

No application catalog, recipe executor or automated CMS installation exists in the supplied prototype. References to WordPress, Symfony or Laravel in the conversation describe intended use cases, not tested compatibility or bundled software.

## Required recipe record

Each recipe must identify the application, artifact source and integrity information, license, runtime/extensions, supported web profiles, storage/database requirements, secret inputs, lifecycle commands, health checks and supported update path. Record whether `.htaccess`, worker mode, background jobs or writable directories are required. Never infer compatibility from the application's name alone.

A recipe consumes a hosting account, approved runtime, database and storage allocation. It runs as the account/application identity, not root. The web document root and non-public files must be explicit. Arbitrary user input may not become a shell command or an unrestricted path. A database credential must not appear in command logs, build artifacts or the repository.

## Lifecycle

Plan prerequisites and quota impact; stage immutable input; validate configuration; back up data before migration; activate under resource locks; check health; record the installed artifact and version. A failed code deployment can be reverted separately from a database migration: never promise rollback when the schema/data change is irreversible. Removal must ask whether data, databases and backups are retained.

## Deployment and staging (Q83–Q85, Q90)

Recipes must describe PHP/extensions, WebStack/TLS, files/SFTP/Git deployment, staging, code rollback **distinct from DB migrations**, selective clone/restore. Tenant identity, credentials, data and staging URLs stay isolated. Q85 C selects Git Deploy, preview, backup and controlled recovery, not automatically blue-green/canary pipelines. [Website lifecycle](../02-architecture/website-lifecycle.md).

## Acceptance and observability

Test a clean installation, duplicate request, interrupted download, invalid signature/hash, invalid runtime, database migration failure, restoration and removal within an isolated tenant. Observe job/correlation IDs, artifact identity, duration and sanitized errors. Future catalog entries must link to those tests and name the qualifying OS/profile/runtime combination. No executable recipe may be advertised until these records exist.

Decision Q4 adds **PHP, Node.js, Python and containerized customer applications** as target runtimes, independently isolated, quota-bounded, versioned and configurable. **Docker and Podman are confirmed as separate adapters (Q51 C)**; signed images, networking and volumes still require specification and testing; this is not shipped.

[Modules](../04-modules/README.md) · [Contracts](../08-api-contracts/README.md) · [Operations](../15-operations/README.md)
