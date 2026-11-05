<!-- forgepanel-doc id=FP-02-SITE-WEBSTACK revision=2 status=specified -->
# Per-site WebStack recommendation and safe profile switching

[Français](../../fr/02-architecture/site-webstack-advisor.md) · [Architecture](README.md) · [Q71–Q80 decisions](../00-project-control/decisions-q71-q80.md)

## Owner decision — Q79 D, clarified

**When creating each website**, ForgePanel computes one or more **recommended WebStack profiles for that individual site** based on declared requirements and actual server capabilities. The UI displays a recommendation, reasons, and feasible alternatives. An administrator may **accept or select any other compatible profile**.

**After creation**, site settings allow the operator to **request a WebStack switch**. It must pass authorization, preview, validation and a staged transition. The selection becomes active only after checks; no blind switch, zero-downtime guarantee or server-wide change to unrelated websites.

## Q81 C and Q82 D — compatibility and transition

The advisor Q81 **must** account for `.htaccess`, PHP version/extensions, OS, tenant isolation, security constraints, resource quotas and IP:port listener ownership. Ineligible profiles are rejected; recommendations are **specific to each site** under Q79.

For changes Q82 permits an **isolated temporary test route** or **progressive cutover only when supported by topology**, following preview, backup, validation and maintenance window/notification planning. Cookies, sessions, application writes and protected files must stay consistent. Otherwise warn about a potentially interrupted controlled cutover. No unrelated site sharing 443 may be altered. [Site lifecycle](website-lifecycle.md).

## Recommendation criteria (future)

Inputs: verified OS/installable packages, available frontends and listeners (IP/port/TLS), requested PHP and extensions, application rules, `.htaccess` needs, CGI/rewrites/access control, tenant isolation, permitted FrankenPHP worker mode, hosting plan and quotas. Each condition records provenance and rule version, plus state: eligible, incompatible, dependency required, or not verified. Performance claims require actual benchmarks.

Five proposed profiles: `nginx_apache_fpm`, `nginx_fpm`, `apache_fpm`, `caddy_fpm`, `caddy_frankenphp`. **Strict Nginx→Apache** forwards requests governed by `.htaccess` to Apache. Accelerated Nginx static serving needs equivalent front-door access controls or it can bypass protected resources. Direct Nginx/Caddy configurations do not interpret `.htaccess`. FrankenPHP worker requires verified app and tenant compatibility.

## Recommendation contract

Candidate request: `webstack.recommend(site_draft,server_facts,policy_revision)`. Response ordered by `profile_id`, `eligibility`, `reasons`, `warnings`, `required_components`, `listener_plan`, `confidence_evidence`, `estimated_impact`, `policy_revision`. Explain all reasons; incompatibilities must block unsafe selections, not only warn. Rankings are not speed guarantees.

Every selection requires RBAC permission and **explicit operator confirmation**. Server policy may disallow a profile for a tenant/reseller even when technically installable; capability is not authorization.

## Existing-site transition

1. **INVENTORY**: active profile and config ownership, shared listeners, PHP versions, TLS, document root, rewrites, access rules, caches and jobs.
2. **PLAN/PREVIEW**: compare profiles, dependencies, package installation, ports, security and possible downtime. Distinguish frontend change from routing/runtime change.
3. **VALIDATE**: permissions, quotas, OS capabilities, IP:port ownership, syntax, `.htaccess` and application/PHP compatibility; fail closed if unknown.
4. **SNAPSHOT**: preserve managed config generation and relevant data when mutated; document recovery limits.
5. **STAGE**: prepare separate configs, pools and routes; preserve panel listeners and unrelated sites; test before cutover.
6. **CUTOVER/VERIFY**: change route/listener **according to topology**, test HTTP(S), TLS, PHP, access protection and app health. Public shared ingress has one owner; a per-site switch cannot replace another site's frontend.
7. **COMMIT/RECOVER**: persist generation, operation state, audit and recovery/compensation procedure. Application code or SQL migrations might not be reversible.

Target state machine: `RECOMMENDED → SELECTED → PLANNED → VALIDATING → STAGING → SWITCHING → VERIFYING → ACTIVE`, or `FAILED/RECOVERING/MANUAL_INTERVENTION`. Jobs are idempotent with site/listener locks, drift detection and sanitized diagnostics. Panel rescue access and certificates must be preserved.

## Acceptance before release

- New plain PHP site: five profiles filtered by real capabilities with explained and changeable recommendations.
- `.htaccess`-protected site: reject unsafe direct profiles or require an equivalent validated rewrite/access migration; never expose sensitive static content.
- Existing site moves between Nginx/Apache and Caddy on supported IP/listeners without impacting other vhosts.
- TLS, PHP version/extensions, busy jobs, denied permissions, stale plan, crash after snapshot and recovery.
- One shared public ingress on 443 with multiple backend profiles: tested routing and listener ownership, no implicit ingress replacement.
- Truly per-site recommendations, not merely a global default; preserve hosting account scope, quotas and secrets.

**State: specified only. No working advisor, live WebStack switcher or certified VM deployment exists in the Core.**
