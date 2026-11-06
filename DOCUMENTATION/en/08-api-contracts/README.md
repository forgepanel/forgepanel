<!-- forgepanel-doc id=FP-08 revision=12 status=documented -->
# APIs and contracts

[Français](../../fr/08-api-contracts/README.md) · [Index](../README.md)

## Candidate FORGE / PANEL contract

The [routing, host and session boundary](portal-route-boundary.md) specifies **FORGE `/forge` on 8447** and **PANEL `/panel` on 8446**, with OS-detected IP addresses and a verified existing FQDN if present, without domain customization or automatic port-443 virtual hosts. The [non-runtime registry](../../../evidence/portal-access-registry-v1.json), its [offline validator](../../../scripts/validate_portal_access_registry.py) and [contract tests](../../../tests/documentation/test_portal_access_contract.py) do not replace real Symfony/HTTPS tests. No active API or route is implied.

## Contracts observed in SRC-03

The archive contains `contracts/install-config.schema.json` (JSON Schema 2020-12, schema_version 1), Go/PHP validators and setup routes. There is no implemented public hosting REST API, OpenAPI document, agent socket protocol, webhook dispatcher or distributed job broker.

| Field | Existing contract |
|---|---|
| `schema_version` | Exactly 1 |
| `admin_port`, `user_port` | Integers 1024–65535; must differ |
| `admin_host`, `user_host` | Strings up to 253 characters; ASCII host validation in code; a nonempty user host requires a distinct nonempty admin host |
| `webstack` | One of `nginx_apache_fpm`, `nginx_fpm`, `apache_fpm`, `caddy_fpm`, `caddy_frankenphp` |
| `modules` | Unique values from `dns`, `mail`, `database`, `sftp`, `backup` |

All fields are required; extra fields are rejected. Cross-field checks are in code, not fully expressed by the schema. Valid intent is not available infrastructure. Do not silently change a field's meaning when adding execution.

Routes: `/setup`, `/setup/resume`, `/setup/mfa`, `/setup/recovery`, `/setup/configuration` accept their declared GET/POST methods; `/setup/review` and `/setup/configuration.json` are GET views/exports. POST operations use CSRF checks and setup grants. These source routes are not deployed endpoints.

CLI exit codes in source: 0 success, 2 preflight failure, 64 invalid/unsupported usage, 70 internal/unimplemented operation, 77 permission/TTY refusal. `install apply` is refused; `release verify` validates the manifest signature, not downloaded artifact bytes.

## Proposed Q61–Q70 contracts

Signed artifact registry and anti-rollback metadata (Q61), capability-based DNS/mail/backup/monitoring adapters (Q63–Q65/Q68), idempotent scoped multi-server operations with observed state (Q67), listener ownership and WebStack generations (Q69), versioned navigation/widgets (Q70). Typed scoped operations only; agent API never accepts an arbitrary shell command. [Specification](../00-project-control/infrastructure-decisions.md). **Candidate contracts only**, no new working endpoints.

## Per-site WebStack advisor contract (Q79)

Candidate `webstack.recommend(site_draft,server_facts,policy_revision)` returns eligible profiles, reasons, dependencies and warnings; `webstack.planSwitch(site_id,target,revision)` plans an existing site's transition with idempotency, authorization, listener ownership, `.htaccess` security and backup. Switching must not merely edit a database field or the server's global stack. [Specification](../02-architecture/site-webstack-advisor.md). No such working API exists.

## Candidate Q81–Q90 hosting contracts

`site.webstack.recommend`, `site.webstack.planSwitch`, `site.php.planConfig`, `site.tls.issueOrImport`, `site.deploy.planGit`, `site.staging.clone`, `tenant.database.allocate`, `tenant.cache.provision`, `tenant.files.list/write`, `tenant.ssh.configure`, `mail.domain.rules`, `hosting.plan.effectiveQuotas`, `site.restore.plan`. All require identity, tenant/org, hosting plan, real capabilities, revision, idempotency and audit, no generic root shell. None is operational. [Website lifecycle](../02-architecture/website-lifecycle.md).

## Proposed Q91–Q100 contracts

`php.catalog.supportedVersions`, `site.php.planMigration`, `site.isolation.capabilities`, `site.git.deployManual`, `site.git.acceptWebhook`, `site.staging.privacyPolicy`, `site.tls.listIssuers`, `site.tls.dns01Driver`, `tenant.data.engineQuota`, `tenant.ssh.rotateOrRevoke`, `mail.webmail.capabilities`, `hosting.quota.graceGrant` and `site.migration.planTransfer`. Require identity, tenant, resource, policy, revision, idempotency and audit; Git notifications and remote operations never mean generic shell commands. These are **candidate interfaces only**. [Q91–Q100](../00-project-control/decisions-q91-q100.md).

## Candidate Q101–Q110 contracts

`php.exception.request/approve/expire`, `site.isolation.listCertifiedProfiles`, `site.deploy.environmentPolicy`, `staging.sensitiveData.approve`, `acme.issuer.retryOrRecover`, `database.topology.plan`, `ssh.access.tempGrant/revoke`, `webmail.driver.recommend`, `quota.grace.planGrant`, `migration.preSync.planFailover` are **candidate non-operational** actions. Each needs actor, tenant/account/site/environment, OS-qualified capability, typed input, approvals, expiry, revision, idempotency, redacted audit and recovery status. Approval never makes a webhook a root shell, and failed failover must preserve recovery. [Q101–Q110](../00-project-control/decisions-q101-q110.md).

## Future protocol requirements

Specify an operation envelope with version, operation ID, actor/scope, target resource, correlation/idempotency key and typed parameters. Authenticate local peers or remote agent identities; never accept shell commands. Persist admission before acknowledging asynchronous work. Define retries, cancellation, lease expiry, duplicate delivery and partial-failure semantics. An event is a recorded fact, not proof that all consumers succeeded.

Version compatibility and migration tests precede any new public API. Proposed endpoints from earlier conversations are examples, not published contracts.

[Core](../03-core/README.md) · [Database](../09-database/README.md)

## R3 — Candidate typed Symfony ↔ Go IPC contract

[R3 IPC contract](symfony-go-ipc-r3.md) defines `IPC-FP-0001..0012`: peer authentication, independent RBAC/tenant enforcement, allowlisted actions, typed request/response, errors, idempotency, durable jobs, locks, Q47 lifecycle and recovery. The [seven candidate operations](../../evidence/typed-agent-operations-v1.json), [request](../../evidence/candidate-ipc-request-v1.schema.json) and [response](../../evidence/candidate-ipc-response-v1.schema.json) JSON Schemas are **documentation only, not active**. Two privileged operations remain **`BLOCKED_UNTIL_QUALIFIED`**; no `shell.exec` or new public endpoint. [R3 tests](../13-tests-quality/r3-ipc-installer-gates.md).

## R3 — Local peer trust boundary

[Candidate peer trust](local-peer-trust-r3.md) adds PEER-FP-0001..0012 for a **proposed** private Unix socket, kernel-observed peer identity, separated service users, Go-side reauthorization, anti-replay and fail-closed reconnection. The [candidate peer-binding schema](../../evidence/candidate-peer-binding-v1.schema.json) is **neither a signed attestation nor a running API**. JSON actor_claim, supplied UID/PID or socket file permissions alone cannot grant Linux operations. [Durable jobs](../09-database/durable-jobs-r3.md) and [R3 QA](../13-tests-quality/r3-jobs-peer-gates.md).

## R3 — Typed Linux effect and compensation contracts

[12 `EXEC-FP-0001..0012` requirements](typed-execution-recovery-r3.md) specify per-operation actor/plan/revision authority, effect-boundary fencing, observed health and safe recovery, without creating a privileged process. [Guard registry](../../evidence/candidate-typed-execution-guards-v1.json) matches the **7 ACT-FP operations**; `ACT-FP-0005/0007` remain **`BLOCKED_UNTIL_QUALIFIED`**. Arbitrary payload commands/shell.exec are prohibited, and schema-valid JSON authenticates no peer or actor. [12 R3 negative tests](../13-tests-quality/r3-physical-execution-gates.md).

## R3 — Critical review of admission, dedup and observed effects

[Targeted review](../19-audits-risks/r3-job-integrity-audit.md) requires denied-admission audit without fake jobs, warns that inbox ACK is not Linux effect proof and that stale fencing capabilities must remain invalid **after PostgreSQL restore**. A caller-provided actor_claim or scope_ref does not prove tenant identity. **RISK-033..036 OPEN**, two privileged operations blocked, [eight tests PLANNED](../19-audits-risks/r3-job-integrity-audit.md).
