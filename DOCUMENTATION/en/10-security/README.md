<!-- forgepanel-doc id=FP-10 revision=4 status=documented -->
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

## Minimum release gates

Never request the Linux root password through the panel. Keep the customer portal closed until authorization/session isolation is tested. Do not disable SELinux/AppArmor or firewall rules to make tests pass. Avoid secret-bearing URLs, logs and artifacts. Require read-only diagnosis before a proposed repair and explicit authorization for destructive changes. Restore tests must cover encryption keys, not just SQL/files.

Five-attempt bootstrap lockout can itself be abused for denial of service; network restrictions and recovery tests remain needed. TOTP code vectors do not equal a cryptographic audit. A port number is not an authorization boundary.

## Reporting and review

No supported production release, private reporting email or response SLA has been established. Use GitHub private reporting only when available; otherwise request a private channel without posting exploit details or secrets publicly. Establish that channel before public distribution. Review sensitive code separately from implementation; no independent reviewer was available in this documentation audit. See [risk register](../19-audits-risks/README.md).
