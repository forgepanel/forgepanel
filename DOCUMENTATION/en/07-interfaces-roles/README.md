<!-- forgepanel-doc id=FP-07 revision=4 status=documented -->
# Portals, identities and authorization

[Français](../../fr/07-interfaces-roles/README.md) · [Index](../README.md)

## Application roles are not Linux privileges

The target roles are Super Administrator, server administrator, reseller, hosting customer and scoped collaborator. Only `ROLE_SUPER_ADMIN` on the initial account exists in SRC-03's schema; this is not a complete RBAC implementation. Linux `root`, the `forgepanel` service identity and tenant OS accounts are separate security subjects. An application role must never expose an unrestricted root shell.

The target authorization decision combines permission, tenant/resource ownership, delegated scope, resource state and sensitive-action reauthentication. UI visibility is not enforcement. Check the service boundary, API and system operation independently; deny missing or ambiguous authority. Do not claim Symfony Voters are configured when the archive only has a setup firewall and capability checks.

## Portals and sessions

Target admin direct access is 8447, customer access 8446, with configurable distinct hosts on HTTPS 443 later. The prototype accepts distinct non-privileged ports; the customer portal remains disabled. Same IP with different ports must not be treated as cookie isolation. Distinct hosts, session contexts and server-side authorization are required before opening both portals.

The setup cookie is configured as `__Host-FORGE_ADMIN`, Secure, HttpOnly, SameSite Strict, path `/`. Real HTTP tests remain pending. `PUBLIC_ACCESS` on setup routes does not remove SetupService's token/grant checks; it also does not create a permanent authenticated administrator session.

## Approvals, visual modes and sessions (Q66, Q70)

Sensitive operations require recent authentication, with **configurable extra approval** when policy requires it (Q66 C). MFA remains optional; an audited controlled emergency path is required for single-admin scenarios. The visual editor (Q70 D) only exposes validated widgets/routes; menu visibility never changes access rights. [Design](../11-design-system/visual-editor.md) · [Decisions](../00-project-control/infrastructure-decisions.md).

## Website-manager role Q136 C

For sites owned or explicitly delegated, the **website manager** may view state and manage **PHP, domain, TLS, files**, use **SFTP** and request **backup/restore** within plan, quotas and Q47 permissions. It cannot upgrade OS packages, change global security/panel settings, access another organization's websites or elevate privileges. Sensitive TLS/restore operations require preview, audit and policy-specific approval; administrator MFA stays optional. [Q131–Q140](../00-project-control/decisions-q131-q140.md). **This role is not implemented.**

## Required tests before expansion

Verify customer-to-admin denial, cross-account object access, reseller scope, direct API access without UI, stale/revoked authorization, session rotation, logout, CSRF, rate limits and recovery-code replay. Record actor and effective scope in audit without logging credentials. Reseller/user guides must remain marked future until these flows exist.

Q5 adds organization/reseller white-label themes, HTTPS domains, logos and email templates. Branding permissions never grant cross-tenant file or customer access. The [Configuration Engine](../02-architecture/configuration-engine.md) defines inheritance; no runtime exists yet.

Q58 C retains **local accounts** with **optional SSO/OIDC**. Identity-provider groups and claims cannot automatically grant administrator roles. Test token validation, account linking, organization scope and local recovery. Administrator MFA stays **optional**. See [Q56–Q60](../00-project-control/commerce-identity-release-policy.md).

[Security](../10-security/README.md) · [Setup core](../03-core/README.md) · [Design system](../11-design-system/README.md)
