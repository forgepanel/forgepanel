<!-- forgepanel-doc id=FP-02-CONFIG revision=8 status=specified -->
# Configuration Engine — administrable settings specification

[Français](../../fr/02-architecture/configuration-engine.md) · [Architecture](README.md) · [Product policy](../00-project-control/product-policy.md)

## Goal and scopes

Every setting must declare a stable `key`, schema/type/units, default, documentation, group, scope, revision, source, effective value, required OS/WebStack capability, dependencies, permissions, secret classification, impact class, validation and recovery policy.

**Intended precedence**: product defaults → global server administrator policy → server → organization/reseller → hosting plan → account → website/application → explicitly permitted per-user override. A narrower scope may override only delegated keys within parent constraints. Security minima and upper-tier limits always apply; Expert mode affects presentation, never real authorization.

Secrets must be referenced through protected storage, not exposed as plaintext values in API responses, logs, exports, views, unprotected backups or manifests.

## Configurable setting families

| Family | Exposed options | Authority and limits |
|---|---|---|
| General UI | Locale, timezone, density, dark/light themes, widgets, announcements | User/organization preference; no rights change |
| Branding / white-label | Logo, palettes, favicon, name, domain, email templates, reseller identity | Authorized organization; DNS/TLS validation; distinct cookie origins |
| Identity and RBAC | Roles, permissions, sessions, API access, **optional** MFA, login policy | Server/super-admin authority; safeguards and recent authentication |
| Ports/network | IP/IPv6, portal ports, listeners, hostnames, proxies | System administrator; retain last known good access until new one confirmed |
| WebStack and PHP | Nginx/Apache/Caddy profiles, PHP-FPM/FrankenPHP versions, limits and compatible rules | Server policy, real capability, tenant isolation |
| Application runtimes | PHP, Node.js, Python, versions, extensions, container deployment | Authorized tenants/servers; cgroups, signed images, restrictions |
| DB, DNS and mail | Providers, quotas, zones, mailboxes, storage, backups | Native service/tenant boundaries; no privilege escalation |
| System security | Firewall, SELinux/AppArmor, SSH, SFTP, lockouts, audit | Administrator; **no implicit disablement of controls** |
| Backups | Destinations, retention, encryption, schedules, restore tests | Server/tenant rights and anti-deletion policy |
| Jobs and updates | Time windows, stable/beta channels, retries, locks, alerts | Dedicated permissions and signature validation |
| Modules/extensions | Activation, versions, settings, package sources, contracts, grants | Signed trust; Core works without any extension |
| Hub communication | Opt-in registration, premium entitlement queries, update discovery, minimal metrics, diagnostics and marketing **separate** | Distinct permissions/consents; free Core independent |
| Commercial licenses | Entitlement state, expiry, last proof, 60-day offline policy and alerts | **Displayed** status; entitlement issuance controlled by publisher, client may not self-extend |

Performance options cannot become unrestricted shell execution or disable tenant isolation.

## Q47 safe-change lifecycle

1. `DRAFT`: local change, read-only diff, actor/scope.
2. `PLAN`: compile platform-specific steps, permissions, dependencies, listener conflicts and compatibility.
3. `PREFLIGHT`: verify resources, syntax, certificates, existing backups and preconditions.
4. `SNAPSHOT`: preserve relevant configuration/data before modification, encrypted where appropriate; define restore scope.
5. `APPLY`: lock affected resources, prepare versioned generation, apply idempotent steps and durable audit.
6. `VERIFY`: systemd service status, panel health, local and functional service checks.
7. `COMMIT`: persist applied revision, audit and notification state.
8. `RECOVER`: restore reversible pieces and explicitly compensate/flag irreversible results.

Presentation-only changes may apply immediately. Changes to ports, firewall, WebStack, RBAC or storage require at least PLAN/PREFLIGHT/SNAPSHOT/APPLY/VERIFY. Maintain emergency admin access for network changes; do not promise universal rollback for database deletion or package installation.

## New Q56–Q60 settings

Core will expose **Stable/Beta/Dev** channels with authorization and compatibility checks (Q57), local accounts plus optional SSO/OIDC while admin MFA remains optional (Q58), and per-category retention within legal/security constraints (Q59). Independent payment providers and perpetual/subscription/trial/coupon/bundle/add-on offers belong to **Hub**, not Core (Q56/Q60). None is implemented. [Specification](../00-project-control/commerce-identity-release-policy.md).

## New Q61–Q70 configuration families

Release signature/channel/approvals (Q61); verified DEB/RPM setup (Q62); capability-based DNS/mail providers (Q63–Q64); backup destinations, encryption, retention, replication/immutability (Q65); reauthentication and extra approval (Q66); server groups/HA policy (Q67); alert rules and recipients (Q68); IP/port listener ownership and per-site profile (Q69); versioned visual editing (Q70). Sensitive mutations follow PLAN/VALIDATE/SNAPSHOT/APPLY/VERIFY/RECOVER. [Details](../00-project-control/infrastructure-decisions.md).

## Q71–Q80 policy and site-specific choices

The settings registry must expose key custody/rotation, eligible existing-service adoption, tested DNS/mail adapters, 3-2-1 backups and restore drills, approval/recovery policies, server groups, Prometheus/OpenTelemetry exports and approved declarative widgets. **Q79** adds `recommended_webstack` **per site** and a separate `webstack.planSwitch(site_id,target_profile,revision)` operation, subject to PLAN/VALIDATE/SNAPSHOT/STAGE/VERIFY/RECOVER without touching unrelated vhosts. [Details](site-webstack-advisor.md).

## Q81–Q90 website settings

Candidate typed allowlisted keys: `site.webstack.profile`, `site.webstack.recommendation_revision`, `site.php.version`, `site.php.extensions`, `site.php.fpm_limits`, `site.tls.mode`, `site.tls.acme_challenge`, `site.deploy.git_ref`, `site.staging.policy`, `account.database.drivers`, `account.cache.drivers`, `account.ssh.access`, `mail.domain.filters`, `plan.quota.*`, `site.restore.scope`. Child settings cannot bypass plan/server ceilings. These are proposed contract examples, not working API keys.

Q82 switching requires `PLAN → PREFLIGHT → SNAPSHOT → STAGE → TEMP_ROUTE_TEST (when supported) → CUTOVER (progressive only if safe) → VERIFY → FINALIZE/RECOVER`. Show maintenance, notifications, potential downtime and recovery limits. Q90 restores/staging clones require the same controls. [Website lifecycle](website-lifecycle.md) and [Q81–Q90](../00-project-control/decisions-q81-q90.md).

## Q91–Q100 settings and sensitive operations

Candidate keys: `site.php.support_policy` (maintained versions/EOL/migration window), `site.php.isolation_profile` (qualified Linux capability), `site.deploy.trigger_policy` (manual/signed webhook/allowed refs), `site.staging.data_policy` (masking, SMTP/webhooks, secrets and retention), `site.tls.issuer` and `site.tls.dns01_provider`, `account.data_services` (per-engine grants/quotas), `account.ssh.policy` (keys/revocation/expiry), `mail.domain.webmail_driver`, `plan.quota.grace_policy` (threshold and authorized extension), `site.migration.plan` (source/target compatibility). Sensitive values are references to protected secrets. Child scopes cannot relax server security.

Cross-server migration and staging creation require durable idempotency, locks, plan/backup/test/commit or compensation. **Q99 cannot bypass physical hard limits**. [Q91–Q100](../00-project-control/decisions-q91-q100.md) · [Website lifecycle](website-lifecycle.md).

## Configurable Q101–Q110 policies

Candidate versioned keys: `site.php.eol_exception` (grant/expiry/migration), `site.isolation.profile` (plan/site with OS certification), `site.environment.deploy_policy` (manual/webhook and approvals), `site.staging.copy_policy` (classification/extra approval/retention/audit), `site.tls.acme_fallback` (allowed CAs/retries/alerts/recovery), `account.database.topology` (shared/dedicated, optional certified clustering), `account.ssh.temporary_grants` (IP/expiry/qualified CA), `mail.webmail.recommendation` (security/maintenance evidence), `plan.quota.grace_by_resource` (duration/cap) and `site.migration.advanced_cutover` (pre-sync, consistency and failover).

All settings remain constrained by effective RBAC, parent policies and **verified** OS capabilities. Exceptions/approvals/temporary grants need revision, expiry and audit. Configuration Engine never promises hard quota overrides or zero-downtime migrations. [Q101–Q110](../00-project-control/decisions-q101-q110.md) · [Technical rules](runtime-exceptions-and-data-continuity.md). **Not implemented**.

## Proposed API and acceptance

Candidate operations: `config.readEffective(scope)`, `config.plan(changes,expected_revision)`, `config.apply(plan_id,idempotency_key)`, `config.history(resource)`, `config.recover(generation_id)`. Use schema revisions and errors `PERMISSION_DENIED`, `POLICY_LOCKED`, `CAPABILITY_UNAVAILABLE`, `CONFLICT`, `PLAN_STALE`, `PARTIAL_RECOVERY`.

Tests: prevent tenant scope escalation; deny unauthorized CLI/API; reject stale revision; invalid configuration never activated; detect port collision; prove new admin endpoint before dropping old; failure after snapshot; explicit partial compensation; detect drift without overwriting foreign-owned files; show effective values and permission reasoning without exposing secrets.

**Status: specified only. There is no functioning Configuration Engine in the current repository.**

## Q47 → R3: future agent operation boundary

[Candidate Symfony ↔ Go IPC](../08-api-contracts/symfony-go-ipc-r3.md) describes plan/revision/idempotency/audit envelopes, while the [installer lifecycle](../14-devops-releases/installer-lifecycle-r3.md) maps Q47 phases to separated observation, staging and privileged steps. The [ACT-FP registry](../../evidence/typed-agent-operations-v1.json) is **documentary**: no setting key becomes a system command, no UI expert mode bypasses isolation, and two privileged actions remain blocked. Database job records, actual Linux checks, timeouts and retries require owner reviews before implementation.
