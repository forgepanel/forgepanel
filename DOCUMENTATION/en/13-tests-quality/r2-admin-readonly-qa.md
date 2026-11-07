<!-- forgepanel-doc id=FP-13-R2-ADMIN-QA revision=2 status=specified -->
# R2 — real SQL administrator authentication and Symfony session smoke candidate

[Français](../../fr/13-tests-quality/r2-admin-readonly-qa.md) · [Identity contract](../03-core/admin-identity-r2.md) · [Full R2 matrix](r2-integration-gates.md)

**VERIFIED PARTIAL EVIDENCE — 2026-11-07:** [PR #63](https://github.com/yyogas/forgepanel/pull/63), commit `97cfbf73100b237b8781e9c34bb0038ce7ccc1e4`, [push CI #42389509528](https://github.com/yyogas/forgepanel/actions/runs/42389509528) and [PR CI #42389514939](https://github.com/yyogas/forgepanel/actions/runs/42389514939): **29 real PostgreSQL assertions** and **31 real Symfony HttpKernel + PostgreSQL session assertions** PASS. Seven initial static policy cases also PASS. These prove only read-only login/session behavior; they do **not** complete R2, Symfony Security authenticator/tenant RBAC, full browser/TLS cookie tests or any hosted-server operation. CI uses isolated PostgreSQL 16 (`forgepanel_test`, explicit opt-in, random test schemas, teardown), PHP 8.3, locked Composer packages, real Symfony HttpKernel and MockArraySessionStorage. Test credentials and signing inputs are synthetic and must never be reused. No Linux host/systemd or privileged executor is invoked.

Test scripts:
- `apps/panel/tests/admin_identity_r2.php`: SQL-backed optional-MFA-disabled password login; deny before `REVIEWED`, unknown principal and wrong password; credential seal/rotation; MFA-enabled TOTP single-step replay rejection, one-time recovery and audit redaction. Real data is isolated in temporary schemas.
- `apps/panel/tests/admin_http_r2.php`: Symfony GET `/login` CSRF, anonymous `/admin` 401, invalid CSRF 403, generic login failures, session ID rotation after valid login, read-only `/admin`, CSRF-only POST logout, subsequent session denial and auditable actions. This simulates a session via MockArraySessionStorage rather than a browser cookie jar or an HTTPS termination proxy.
- `tests/r2/test_admin_readonly_contract.py`: source/contract checks that cannot be used as runtime proof.

Pending after this step: real Symfony Security authenticator/RBAC, multi-tenant constraints, browser TLS/cookie evaluation, two-process login race, global rate limiting/DoS across nodes, persistent authenticated administrator lifecycle/recovery, backup/restore epochs, actual panel apply, all R2 full acceptance cases. R1 source, MFA, PostgreSQL and Symfony PRs remain stacked drafts; **PASS does not imply merge, release or Pre-Alpha readiness**.
