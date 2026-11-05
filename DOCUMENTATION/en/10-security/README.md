<!-- forgepanel-doc id=FP-10 revision=7 status=documented -->
# Security model and disclosure

[Français](../../fr/10-security/README.md) · [Index](../README.md)

## Assets, actors and boundaries

Protect Linux privileges, tenant data, database credentials, MFA/encryption keys, setup capabilities, signing authority and audit integrity. Consider unauthenticated network callers, hostile tenant code, compromised plugins, untrusted inputs and interrupted privileged work. A process already compromised as the application user can use that user's database privileges; the bootstrap environment flag is not a sandbox against that attacker.

| Boundary | Requirement |
|---|---|
| Browser → Symfony | Verified HTTPS, exact trusted host/origin, CSRF on mutations, secure session lifecycle, rate limits, resource authorization |
| Symfony → agent | Authenticated versioned private channel; typed allowlisted operations; no `exec(command)` API |
| Agent → Linux | Least privilege, bounded executor, safe path resolution, resource locks, system audit |
| Tenant → tenant | Separate identities/permissions and explicit resource controls; a PHP-FPM pool alone is not sufficient |
| Artifact → installation | Independent trust anchor, verified signatures/hashes, anti-rollback policy and safe key rotation |

SRC-03 implements setup-domain checks and source-level HTTP guards only. Systemd hardening, mandatory access controls, tenant isolation, production secret rotation, full login/RBAC and backup restoration are not demonstrated.

## Optional administrator MFA policy

Administrator MFA is **optional**, not a condition of initial account creation or wizard access. Offer TOTP and later WebAuthn, allow later enrollment, controlled disablement and recovery codes when enabled. Sensitive operations still require recent authentication and contextual permissions. The mandatory v0.7 source path needs a tested code fix.

## Hub communications and commercial entitlements

Under Q6, Hub enrollment is voluntary; premium checks, version discovery, diagnostics/support and marketing have separate permissions/consents or legal processing grounds. No automatic collection of hosting files, email, databases or secrets. Under Q7, the commercial offline grace is **60 days** for eligible previously verified premium rights, subject to contract dates; refusal/revocation must be explicit and non-destructive for essential hosting. See [product policy](../00-project-control/product-policy.md).

## Identity, payments and retention (Q56, Q58, Q59)

Hub payment providers use independent drivers with authenticated and deduplicated webhooks, never rights based only on browser redirects. SSO/OIDC is **optional**, with secure local recovery; administrator MFA stays optional. Per-category retention is limited by law, audit and backup requirements. These components are not operational.

## Trust chain and sensitive operations (Q61, Q65, Q66)

Signed packages/release metadata with protected trust roots, anti-rollback and approvals; encrypted replicated/immutable backup and real restore tests; recent authentication and configurable extra approval for sensitive operations. **Administrator MFA stays optional**, including setup. Signatures, backups and approval are not substitutes for independent permission enforcement. [Q61–Q70](../00-project-control/infrastructure-decisions.md).

## Keys, adoption and approvals (Q71, Q72, Q76)

Signed releases need protected key custody, rotation and anti-rollback (Q71); never distribute publisher private keys in code/packages. Adopting existing services (Q72) requires permissions, ownership inventory, snapshots and protection of unmanaged configurations. Sensitive actions (Q76) may require an independent approver; local emergency access remains audited. **Admin MFA remains optional** and approvals do not replace RBAC. [Decisions](../00-project-control/decisions-q71-q80.md).

## Website isolation, certificates and data — Q81–Q90

WebStack switching needs permission, safe listeners/`.htaccess`, HTTP/TLS and no disclosure via temporary test routes (Q81/Q82). Per-site PHP-FPM version/directives/extensions are allowlisted and quotas enforced (Q83). ACME/wildcard/imported TLS requires domain proof, DNS-01 and protected keys (Q84). Git Deploy/staging, clone and restore must never silently copy credentials/private data (Q85/Q90). Tenant-scoped MariaDB/MySQL/PostgreSQL/Redis/Valkey (Q86), restricted file manager/SFTP/SSH without root or implicit web terminal (Q87), private webmail/quarantine (Q88) and enforceable plan quotas (Q89). [Details](../02-architecture/website-lifecycle.md). **Not implemented.**

## Runtime and migration security (Q91–Q100)

Each website PHP pool/identity and actual Linux confinement require testing, with EOL notices and planned safe upgrade (Q91/Q92). Manual/webhook Git needs auth, anti-replay, allowed refs and secret-safe logs (Q93). Staging needs data masking, distinct secrets/URLs, blocked real outbound actions, retention/audit (Q94). ACME uses multiple issuers/DNS-01 with domain proof and protected tokens (Q95). Per-tenant DB/cache/SSH require quotas and expiry/revocation (Q96/Q97); Webmail and quarantine require authorized mailbox/domain access (Q98). Quota grace never bypasses host capacity or tenant separation (Q99). Cross-server migration requires both-side permissions, encryption, secret rotation and audited recovery (Q100). [Reference](../00-project-control/decisions-q91-q100.md). **Not implemented.**

## Q101–Q110 trust boundaries

EOL PHP exceptions are **temporary, site-scoped, authorized and audited**, with planned migration (Q101), never overriding isolation selected only from **OS-certified** Linux capabilities (Q102). Manual/webhook deployment policy applies by site and environment, with configurable approval and anti-replay (Q103); sensitive staging copies require **special approval** and isolated secrets (Q104). Multiple ACME CAs have bounded retries, alerts and last-good recovery (Q105). Shared/dedicated DB plus optional certified clusters enforce tenant scope (Q106). SSH keys/IPs and temporary/certified access include revocation (Q107). Webmail advice must show maintenance/security proof (Q108). Per-plan/resource quota grace never overrides host security or capacity (Q109). Advanced migration is allowed only with tested source/target consistency (Q110). [Specification](../00-project-control/decisions-q101-q110.md). **Tests not performed**.

## Minimum release gates

Never request the Linux root password through the panel. Keep the customer portal closed until authorization/session isolation is tested. Do not disable SELinux/AppArmor or firewall rules to make tests pass. Avoid secret-bearing URLs, logs and artifacts. Require read-only diagnosis before a proposed repair and explicit authorization for destructive changes. Restore tests must cover encryption keys, not just SQL/files.

Five-attempt bootstrap lockout can itself be abused for denial of service; network restrictions and recovery tests remain needed. TOTP code vectors do not equal a cryptographic audit. A port number is not an authorization boundary.

## Reporting and review

No supported production release, private reporting email or response SLA has been established. Use GitHub private reporting only when available; otherwise request a private channel without posting exploit details or secrets publicly. Establish that channel before public distribution. Review sensitive code separately from implementation; no independent reviewer was available in this documentation audit. See [risk register](../19-audits-risks/README.md).
