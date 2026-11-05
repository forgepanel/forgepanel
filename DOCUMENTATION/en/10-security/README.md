<!-- forgepanel-doc id=FP-10 revision=1 status=documented -->
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

## Minimum release gates

Never request the Linux root password through the panel. Keep the customer portal closed until authorization/session isolation is tested. Do not disable SELinux/AppArmor or firewall rules to make tests pass. Avoid secret-bearing URLs, logs and artifacts. Require read-only diagnosis before a proposed repair and explicit authorization for destructive changes. Restore tests must cover encryption keys, not just SQL/files.

Five-attempt bootstrap lockout can itself be abused for denial of service; network restrictions and recovery tests remain needed. TOTP code vectors do not equal a cryptographic audit. A port number is not an authorization boundary.

## Reporting and review

No supported production release, private reporting email or response SLA has been established. Use GitHub private reporting only when available; otherwise request a private channel without posting exploit details or secrets publicly. Establish that channel before public distribution. Review sensitive code separately from implementation; no independent reviewer was available in this documentation audit. See [risk register](../19-audits-risks/README.md).
