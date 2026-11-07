<!-- forgepanel-doc id=FP-13-R2-HTTP-SMOKE revision=1 status=specified -->
# R2 — Symfony HttpKernel smoke and origin/CSRF boundary tests

[Français](../../fr/13-tests-quality/r2-symfony-http-smoke.md) · [R2 test matrix](r2-integration-gates.md) · [R2 PostgreSQL subset](r2-postgres-execution.md)

## Scope

This stacked candidate adds a test that boots the **actual Symfony HttpKernel** from the R1 Foundation source, rather than treating syntax validation or a standalone PHP domain test as a functioning web application. The candidate is based on R1 source (#59), optional-MFA patch (#60) and the disposable PostgreSQL QA (#61). No source deployment, network listener, reverse proxy, permanent login or production installer is authorized.

An ephemeral GitHub Actions runner resolves the declared Symfony 7.4 / Twig 3 dependencies via Composer, checks the real route table and service container, and sends synthetic **Symfony HTTP Request objects through the real kernel**. It asserts a successful initial `/setup` GET and denial of insecure HTTP, foreign Host, wrong administrator port, unsupported methods, cross-origin POST, oversized POST and missing CSRF; it checks `no-store` and response hardening headers. PostgreSQL is **test-only**, to satisfy the source's explicit PDO dependency.

## Evidence and limits

A passing workflow constitutes a **partial R2 Symfony HTTP boundary smoke test only** on its exact Git commit. Framework dependency resolution is *temporary* here: this lot deliberately does **not** add `composer.lock`, production vendor code or secret values to public Git. Dependency locking, provenance/audit, vendor compatibility and complete test reproducibility are **open release blockers**. A future pinned `composer.lock` must be generated, reviewed and committed separately before any claimed production release.

The test does not demonstrate: a browser-driven positive CSRF POST, valid bootstrap token exchange through HTTP, signed TLS / reverse-proxy integration, permanent administrator login, session persistence across browser requests, complete RBAC, site creation, a privileged daemon, production updates or real VM backup/recovery. These remain **NOT RUN**, along with the remaining R2 master matrix.

The source `SetupBoundary` keeps strict exact HTTPS origin checks and no trusted client-provided forwarding headers. Any actual reverse proxy must undergo separate Security/DevOps qualification. Never weaken Host/Origin checks merely to make a test pass. Keep the Core usable without Hub.