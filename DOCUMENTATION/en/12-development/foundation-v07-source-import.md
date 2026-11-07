<!-- forgepanel-doc id=FP-12-FOUNDATION-SOURCE-IMPORT revision=1 status=documented -->
# Foundation v0.7 — proposed source import and reproducible local checks

[Français](../../fr/12-development/foundation-v07-source-import.md) · [Development](README.md) · [R1 source intake](source-archive-intake.md) · [Manifest](../../evidence/foundation-v07-import-candidate.json)

## Scope of this draft source PR

This PR **introduces application source code** from the recovered SHA-256-pinned **SRC-03** historical Foundation v0.7 ZIP, but does **not** install, deploy, release, sign, activate or certify a hosting panel. The 66-file candidate contains 64 SHA-256-identical original source files plus two clearly adapted paths: a hardened `.gitignore` and blank-secret `apps/panel/.env.example`. The original `apps/panel/.env` and historical documentation, old test outputs and historical changelog are **excluded**. The original ZIP remains archived privately; it is not uploaded into public Git.

`DOCUMENTATION/evidence/foundation-v07-import-candidate.json` pins every selected path, size and SHA-256 and records original SRC-03 SHA-256 `19479d5be9da9bb0ff9180f9b8819ea48baff785ccc3fef59deb2bb0894faf1a`. `scripts/check_foundation_import.py` checks those exact contents and denies changed/missing files, symlink paths and local environment files. It is byte-integrity preflight, **not authenticity, license clearance or a security audit**.

## Reproducible checks on the imported commit

```sh
python3 scripts/check_foundation_import.py
python3 -m unittest discover -s tests/source_intake -p 'test_*.py' -v
GOTOOLCHAIN=local GOPROXY=off GOSUMDB=off go test ./...
GOTOOLCHAIN=local GOPROXY=off GOSUMDB=off go test -race ./...
GOTOOLCHAIN=local GOPROXY=off GOSUMDB=off go vet ./...
php apps/panel/tests/run.php
bash scripts/check.sh
```

The Go CLI's `install plan` remains explicitly **non-executable**; `install apply` is refused. The PHP setup domain tests are isolated; real Symfony HTTP, PostgreSQL transactional behavior, authorization, browser sessions, OS qualification and VM install/upgrade/restore remain **NOT RUN**. v0.7 still has mandatory TOTP enrollment; owner decision requires **optional administrator MFA**, handled in the *separate* v0.7.1 patch after reviewing its SQL and HTTP changes, before qualifying any end-to-end setup.

## Publication, review and recovery gates

- Review exact source provenance, third-party rights and AGPL/commercial licensing terms. Historical `LICENSE-NOT-SELECTED.md` does not grant a license; no production license has been applied by this PR.
- Confirm secrets are absent and no production tokens are embedded. `.env.example` is a template only. Never commit `.env`, `.env.local`, generated binaries or private signing material.
- Review root-owned privileged bridge, Linux paths, input bounds, SQL migrations, recovery and request-origin/session isolation independently; absence of a generic shell API alone is not runtime approval.
- Run named-version, exact-HEAD CI then actual Symfony/PostgreSQL/OS/VM tests in the required R2/R3/R4 order.
- Do not merge/promote until documentation baselines and this source-import contract are reconciled, and publication/security/legal blockers accepted by authorized reviewers. Core must remain free and autonomous without the private Hub. Preserve Q1–Q220 and the `features/* → develop → stable → main → production` workflow.