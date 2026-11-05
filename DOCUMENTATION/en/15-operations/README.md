<!-- forgepanel-doc id=FP-15 revision=4 status=documented -->
# Operations, diagnosis and recovery

[Français](../../fr/15-operations/README.md) · [Index](../README.md)

## Current operational limit

There is no deployed ForgePanel instance in this repository. SRC-03's CLI provides read-only `doctor`, plan generation and conditional setup console bridging. `status`, `repair`, `services`, `webstack`, `admin`, `update` and `backup` are not complete operational commands; unsupported operations refuse without changing the system. Do not tell an operator to repair production with them.

## Prototype setup recovery

On a future correctly installed prototype, `sudo forgepanel setup status` queries setup; token/resume generation requires an interactive terminal and the fixed trusted Symfony console. PHP and PostgreSQL must be healthy. The Go binary remaining executable does not make database-dependent account recovery work during a database outage. Token regeneration is allowed before the initial account; after creation, use the defined local resume flow rather than reopening initial registration.

## Target incident procedure

Record symptoms, revision and affected resource; run non-mutating diagnostics; preserve redacted logs and last known configuration; restrict exposure if necessary; prepare a bounded repair plan; confirm destructive impact; apply under resource locks; verify health and recovery; record outcome and remaining risk. Never erase logs, disable mandatory access controls or overwrite unrelated service configuration as an automatic fix.

Observe service health, operation IDs, duration, failure categories, resource saturation and certificate/backup status. Metrics must not contain tenant secrets or high-cardinality credentials. Alert routing and retention are not implemented yet and need explicit configuration.

## Category-based retention (Q59)

Privileged audit records, system logs, jobs, metrics, diagnostics, sessions, backups, tickets and Hub commercial records require distinct policies. Retention, anonymization, archives and purges are configurable within legal/security limits; no default duration is invented and required incident/recovery evidence cannot be erased. [Q56–Q60](../00-project-control/commerce-identity-release-policy.md).

## Advanced operation and monitoring (Q65, Q67, Q68)

Encrypted multi-destination backups with replication/immutability, local monitoring and email/webhook/external alert integrations, and a phased multi-server/HA/DR target. All adapters expose quotas, consent, retention and recovery; real availability needs restore/failure tests. Clustering follows the foundation milestone. [Architecture](../02-architecture/service-drivers-and-ha.md).

## 3-2-1, observability and recovery (Q75, Q77, Q78)

The target backup profile is **3-2-1**, with scheduled restore tests, replication and an offsite copy according to actual capabilities and budgets; Q65 immutability still requires a supporting destination. Q78 monitoring uses configurable Prometheus/OpenTelemetry adapters with permissioned exports. Q77 phases remote agents before optional HA/external orchestrator modules: redundancy, quorum and recovery require tests rather than a UI checkbox. [Reference](../00-project-control/decisions-q71-q80.md).

## Backup and restoration requirements

Define consistent coverage for configuration, metadata, customer files, databases and encryption keys. Test restore in an isolated environment and record recovery time/data loss; do not promise RPO/RTO numbers before measurements. Key loss can make encrypted MFA data unrecoverable. A future repair engine must separate diagnosis, dry-run and application, keep previous access until a new endpoint is checked, and require a fallback for interrupted changes.

[Security](../10-security/README.md) · [Quality](../13-tests-quality/README.md)
