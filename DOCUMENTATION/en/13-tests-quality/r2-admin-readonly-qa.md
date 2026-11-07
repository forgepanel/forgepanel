<!-- forgepanel-doc id=FP-13-R2-ADMIN-QA revision=1 status=specified -->
# R2 — real SQL administrator authentication and Symfony session smoke candidate

[Français](../../fr/13-tests-quality/r2-admin-readonly-qa.md) · [Identity contract](../03-core/admin-identity-r2.md) · [Full R2 matrix](r2-integration-gates.md)

**Status: PLANNED until exact-head GitHub Actions logs are observed.** CI uses isolated PostgreSQL 16 (`forgepanel_test`, explicit opt-in, random test schemas, teardown), PHP 8.3, locked Composer packages, real Symfony HttpKernel and MockArraySessionStorage. Test credentials and signing inputs are synthetic and must never be reused. No Linux host/systemd or privileged executor is invoked.

Test scripts:
- `apps/panel/tests/admin_identity_r2.php`: SQL-backed optional-MFA-disabled password login; deny before `REVIEWED`, unknown principal and wrong password; credential seal/rotation; MFA-enabled TOTP single-step replay rejection, one-time recovery and audit redaction. Real data is isolated in temporary schemas.
- `apps/panel/tests/admin_http_r2.php`: Symfony GET `/login` CSRF, anonymous `/admin` 401, invalid CSRF 403, generic login failures, session ID rotation after valid login, read-only `/admin`, CSRF-only POST logout, subsequent session denial and auditable actions. This simulates a session via MockArraySessionStorage rather than a browser cookie jar or an HTTPS termination proxy.
- `tests/r2/test_admin_readonly_contract.py`: source/contract checks that cannot be used as runtime proof.

Pending after this step: real Symfony Security authenticator/RBAC, multi-tenant constraints, browser TLS/cookie evaluation, two-process login race, global rate limiting/DoS across nodes, persistent authenticated administrator lifecycle/recovery, backup/restore epochs, actual panel apply, all R2 full acceptance cases. R1 source, MFA, PostgreSQL and Symfony PRs remain stacked drafts; **PASS does not imply merge, release or Pre-Alpha readiness**.
