<!-- forgepanel-doc id=FP-18 revision=1 status=documented -->
# Human and AI contribution workflow

[Français](../../fr/18-contributing/README.md) · [Index](../README.md)

## Onboarding

Read [AGENTS.md](../../../AGENTS.md), project status, decisions, audit and [handover](handover.md). Confirm repository access, current refs, open work and protections. Use the current repository as the durable reference; do not require the owner to repeat unavailable conversations. Distinguish archive inputs from tracked source.

## A coherent change

Describe the need, acceptance criteria, affected components/contracts and risks in a task or PR. Reuse or create `features/<topic>` from the appropriate `develop` baseline. Keep code, tests, bilingual docs and changelog together. Commit messages are English. Do not mix unrelated redesigns or unreviewed third-party code into an import. No license choice is implied by accepting the documentation workflow.

A PR states its base/head, scope, evidence commands/results, security/data/installation impact, missing checks and rollback/recovery. Respect required checks and approvals, including human approvals imposed by GitHub. An author or AI self-review is not independent review. Do not force refs or merge against a changed head without rechecking it.

## Parallel work and handover

Assign named responsibility domains and explicit file ownership. Avoid simultaneous edits to shared contracts, migrations and root governance. The integration owner reconciles conflicts, reruns checks and updates both languages. Every handover records completed changes, remaining work, commit/PR references, exact evidence, blockers and the next bounded task.

The owner decides product outcomes, licensing, spending and sensitive/destructive actions, not technical patch details. Prepare alternatives and a recommendation before asking for an indispensable decision. Unsupported tool access must be reported accurately without fabricating completion.

Use the [PR template](../../../.github/pull_request_template.md). Before application import, only documentation checks are runnable at repository root. Delete temporary branches after integration only according to applicable repository rules.
