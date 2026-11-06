<!-- forgepanel-doc id=FP-07 revision=8 status=documented -->
# Portals, identities and authorization

[Français](../../fr/07-interfaces-roles/README.md) · [Index](../README.md)

## Application roles are not Linux privileges

The target roles are Super Administrator, server administrator, reseller, hosting customer and scoped collaborator. Only `ROLE_SUPER_ADMIN` on the initial account exists in SRC-03's schema; this is not a complete RBAC implementation. Linux `root`, the `forgepanel` service identity and tenant OS accounts are separate security subjects. An application role must never expose an unrestricted root shell.

The target authorization decision combines permission, tenant/resource ownership, delegated scope, resource state and sensitive-action reauthentication. UI visibility is not enforcement. Check the service boundary, API and system operation independently; deny missing or ambiguous authority. Do not claim Symfony Voters are configured when the archive only has a setup firewall and capability checks.

## Portals and sessions

The confirmed portals are **FORGE** `/forge` on HTTPS **8447** and **PANEL** `/panel` on HTTPS **8446**. Installer **detects the host IPs** and any existing FQDN, then verifies DNS/routing/TLS; it **does not request a customizable domain** or create subdomains/443 virtual hosts automatically. IP and FQDN URLs retain the **same ports**. See the [detailed contract](portal-access-routing.md) and [22 planned QA scenarios](../13-tests-quality/portal-access-gates.md). The prototype accepts separate unprivileged ports; the customer portal remains disabled. A shared IP with separate ports **does not isolate cookies**: sessions, cookie names and server-side permission checks remain distinct.

The setup cookie is configured as `__Host-FORGE_ADMIN`, Secure, HttpOnly, SameSite Strict, path `/`. Real HTTP tests remain pending. `PUBLIC_ACCESS` on setup routes does not remove SetupService's token/grant checks; it also does not create a permanent authenticated administrator session.

## Approvals, visual modes and sessions (Q66, Q70)

Sensitive operations require recent authentication, with **configurable extra approval** when policy requires it (Q66 C). MFA remains optional; an audited controlled emergency path is required for single-admin scenarios. The visual editor (Q70 D) only exposes validated widgets/routes; menu visibility never changes access rights. [Design](../11-design-system/visual-editor.md) · [Decisions](../00-project-control/infrastructure-decisions.md).

## Website-manager role Q136 C

For sites owned or explicitly delegated, the **website manager** may view state and manage **PHP, domain, TLS, files**, use **SFTP** and request **backup/restore** within plan, quotas and Q47 permissions. It cannot upgrade OS packages, change global security/panel settings, access another organization's websites or elevate privileges. Sensitive TLS/restore operations require preview, audit and policy-specific approval; administrator MFA stays optional. [Q131–Q140](../00-project-control/decisions-q131-q140.md). **This role is not implemented.**

## Q146 C — restricted SFTP

Q136 website manager gets SFTP only for owned/permitted sites, with **confined Unix identity, secure canonical paths/symlinks, keys, enforced quotas and access audit**. SFTP grants **no shell by default**. Expired/revoked grant denies new sessions without deleting tenant files. Test owned-site success and denied other tenant, parent paths, symlinks and quotas; never provide a root terminal. [Q141–Q150 decisions](../00-project-control/decisions-q141-q150.md).

## Per-site SFTP public-key management (Q157 C)

Authorized website managers may **register/revoke public keys** for owned sites under account/plan policy, with path limits, expiry, quotas and access audit. Sensitive operations (e.g. powerful new key/identity changes) may require recent authentication/targeted approval Q66/Q76; **no private-key upload, root shell or access to other sites**. Expiry/revocation must not delete hosted files. Actual Unix/SFTP services enforce scope, not a UI toggle alone. [Contracts](../02-architecture/qualification-and-security-contracts.md).

## Required tests before expansion

Verify customer-to-admin denial, cross-account object access, reseller scope, direct API access without UI, stale/revoked authorization, session rotation, logout, CSRF, rate limits and recovery-code replay. Record actor and effective scope in audit without logging credentials. Reseller/user guides must remain marked future until these flows exist.

Q5 adds organization/reseller white-label themes, HTTPS domains, logos and email templates. Branding permissions never grant cross-tenant file or customer access. The [Configuration Engine](../02-architecture/configuration-engine.md) defines inheritance; no runtime exists yet.

Q58 C retains **local accounts** with **optional SSO/OIDC**. Identity-provider groups and claims cannot automatically grant administrator roles. Test token validation, account linking, organization scope and local recovery. Administrator MFA stays **optional**. See [Q56–Q60](../00-project-control/commerce-identity-release-policy.md).

[Security](../10-security/README.md) · [Setup core](../03-core/README.md) · [Design system](../11-design-system/README.md)
