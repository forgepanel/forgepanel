<!-- forgepanel-doc id=FP-08-APP-PREVIEW revision=1 status=specified -->
# App Center — offline installation plan preview, two engines

[Français](../../fr/08-api-contracts/app-center-preview-contract.md) · [Recipe contracts](app-center-recipe-contracts.md) · [App Center](../06-apps-recipes/app-center-engines.md)

**CANDIDATE / NOT DEPLOYABLE.** The [pure Python preview](../../../scripts/preview_app_center_install.py) is **not** an installer, Go agent, Symfony API or host capability service. It reads only bundled, deliberately fictional JSON fixtures from [the synthetic fixture directory](../../../evidence/app-center-fixtures/install-request.synthetic.json). No actual system inventory, tenant authorization, artifact download, signature check, SQL query, Docker/Podman call, resource reservation, network probe or privileged action takes place. Its output always has `execution_allowed=false` and `apply_available=false`.

## Typed preview sequence

The existing [candidate recipe validator](../../../scripts/validate_app_center_recipe.py) first rejects unknown or mixed `recipe_kind` fields and unreviewed execution syntax. The preview validates the **entire synthetic input structure**: fake host ID, list of candidate owned-site IDs, available PHP-FPM/database engines, available container drivers and hypothetical CPU/RAM/PID budgets. The candidate request carries a target site, requested host TCP ports and an informational `hub_available` flag; it **never grants authorization** and contains no credentials or custom scripts.

- **ONE-CLICK INSTALL, `native_script`:** simulate checking owned-site scope, PHP-FPM availability and native database compatibility; show proposed file/quota and backup/restore check steps. No Docker/Podman presence and no Hub entitlement is needed. This fixture covers PHP-FPM only; it does **not** cancel the previously approved Node.js/Python native-runtime targets.
- **CONTAINER APPS, `container_stack`:** check the exact declared Docker **or** Podman driver and **separate synthetic** CPU, RAM and PID budgets; list image digest, network/volume and recovery preview steps. A Docker-only fixture does not silently switch to Podman. No image is pulled and no stack launched.
- **Both:** if the target site is absent from the synthetic list, report a scope blocker **without claiming real ownership verification**. Requested host-port publication is never automatically approved: ports 8447 (FORGE) and 8446 (PANEL) are hard-reserved even if omitted from host facts; other reserved/claimed ports are blocked, and unclaimed ports remain subject to an unapproved exposure policy.

## Output interpretation

The candidate plan contains `recipe_kind`, `app_id`, `variant_id`, `preview_steps`, `blocking_reasons`, `compatibility` and a fixed `next_action=SPECIALIST_REVIEW_AND_REAL_INTEGRATION_REQUIRED`. `compatibility=MATCHES_SYNTHETIC_FACTS_ONLY` means **only that the provided fictional inputs do not conflict**; it is never a permission to install. Every plan explicitly reports false for `tenant_authorization_verified`, `artifact_signature_verified`, `runtime_capabilities_verified`, `port_probe_executed`, `resource_reservations_created` and `external_reachability_verified`.

The proposed error codes `NATIVE_PHP_FPM_UNAVAILABLE`, `NATIVE_DATABASE_UNAVAILABLE`, `CONTAINER_DRIVER_NOT_AVAILABLE`, `CONTAINER_*_BUDGET_UNAVAILABLE`, `FORGEPANEL_OR_OTHER_RESERVED_PORT`, `HOST_PORT_ALREADY_CLAIMED`, `HOST_PORT_PUBLICATION_NOT_APPROVED` and `SITE_OWNERSHIP_UNVERIFIED` are **preview-only**, not official Core API errors or OS observations.

The preview disallows unknown fields, untrusted shell/command text, boolean-integer confusion, duplicate ports and self-claimed `VERIFIED` state. It does not write an audit record; future real planning needs a durable ledger, actor/tenant verification and redacted correlation IDs.

## Offline demonstration and evidence

On the branch containing the fixtures:

```sh
python3 scripts/preview_app_center_install.py --fixture native
python3 scripts/preview_app_center_install.py --fixture container
python3 tests/documentation/test_app_center_preview.py -v
```

The [regression tests](../../../tests/documentation/test_app_center_preview.py) cover independent runtimes, free native operation without Hub, missing PHP/SQL/driver, site-scope claims, CPU/RAM/PIDs, known and unknown ports, malicious input fields, deterministic output and non-execution invariants. **They are not the [32 PLANNED functional/VM tests](../13-tests-quality/app-center-engine-gates.md).**

## Required implementation handoff

- **Architecture:** decide whether a common read-only preview interface wraps two independently reviewed planners; do not combine their execution engines.
- **Security:** do not treat caller-supplied capability/ownership booleans as authentication; verify host facts and policies from trusted services, enforce hard port reservations and quotas atomically.
- **API/IPC:** bind authorizations to tenant/site/server, artifact digest, effective permission, idempotency and execution-time revalidation; never accept free-form shell/Compose.
- **Database:** durable jobs, locks and resource accounting require independently approved versioned schema/migrations; this preview has none.
- **DevOps/QA:** source import R1, live Symfony/PostgreSQL R2, qualified installer R3, first PHP/HTTPS site R4 and actual VM recovery/security testing remain prerequisites for product capability.

Q1–Q170 remain intact; Q171+ still need explicit owner answers. The entirely free native One-Click engine does **not** require Hub, Docker or Podman; the synthetic tool cannot install anything.
