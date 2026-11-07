<!-- forgepanel-doc id=FP-13-R2-HTTP-SMOKE revision=3 status=specified -->
# R2 — Symfony HttpKernel smoke and origin/CSRF boundary tests

[Français](../../fr/13-tests-quality/r2-symfony-http-smoke.md) · [R2 test matrix](r2-integration-gates.md) · [R2 PostgreSQL subset](r2-postgres-execution.md)

## Scope

This stacked candidate adds a test that boots the **actual Symfony HttpKernel** from the R1 Foundation source, rather than treating syntax validation or a standalone PHP domain test as a functioning web application. The candidate is based on R1 source (#59), optional-MFA patch (#60) and the disposable PostgreSQL QA (#61). No source deployment, network listener, reverse proxy, permanent login or production installer is authorized.

An ephemeral GitHub Actions runner installs the pinned Symfony 7.4 / Twig 3 dependencies from `composer.lock`, checks the real route table and service container, and sends synthetic **Symfony HTTP Request objects through the real kernel**. It asserts a successful initial `/setup` GET and denial of insecure HTTP, foreign Host, wrong administrator port, unsupported methods, cross-origin POST, oversized POST and missing CSRF; it checks `no-store` and response hardening headers. PostgreSQL is **test-only**, to satisfy the source's explicit PDO dependency.

## Evidence and limits

A passing workflow constitutes a **partial R2 Symfony HTTP boundary smoke test only** on its exact Git commit. The **candidate Composer lock is now versioned in this draft PR**; no `vendor/`, live credentials or signing keys are committed. Independent provenance/licensing/security review, compatibility across target PHP/OS versions and real installation/recovery tests remain **open release blockers**.

The test does not demonstrate: a browser-driven positive CSRF POST, valid bootstrap token exchange through HTTP, signed TLS / reverse-proxy integration, permanent administrator login, session persistence across browser requests, complete RBAC, site creation, a privileged daemon, production updates or real VM backup/recovery. These remain **NOT RUN**, along with the remaining R2 master matrix.

The source `SetupBoundary` keeps strict exact HTTPS origin checks and no trusted client-provided forwarding headers. Any actual reverse proxy must undergo separate Security/DevOps qualification. Never weaken Host/Origin checks merely to make a test pass. Keep the Core usable without Hub.

## Bootstrap environment defect found in first CI run

The initial real Symfony runner failed at `config/bootstrap.php`: historical `Dotenv::bootEnv()` attempted to read a non-existent local `.env` even though the workflow supplied explicit environment variables. This is a real R2 configuration defect, not a database problem. The revised bootstrap loads `.env` **only when present**, preserves the protected `/etc/forgepanel/panel.env` override, and still refuses to boot if `APP_SECRET` is absent or too short. This does not permit using `.env.example` as a credential source. The later [real Symfony CI run #42384745856](https://github.com/yyogas/forgepanel/actions/runs/42384745856) confirmed the environment and DI fixes, the router and 12 HTTP boundary assertions on the prior commit. The new pinned-lock revision must pass CI independently.

## Pinned candidate dependency set — 2026-11-07

After the first successful real Symfony HttpKernel CI, the CI-produced `composer.lock` was recovered from artifact `13578779233`, inspected and checked byte-for-byte (SHA-256 `b1f9e5104c2749acc4fabaddb6a24e094f309c0a38d81f8af8cc7dda20204b68`). It contains **47 packages**, no Composer plugins, with declared MIT/BSD-3-Clause licenses; Symfony framework-bundle was resolved as `v7.4.23`. The lock is now included in the proposed PR branch and the CI uses `composer install`, not dynamic update. Full legal audit and compatibility across all target PHP/OS versions remain pending. This candidate lock is not a released binary or permission to deploy.