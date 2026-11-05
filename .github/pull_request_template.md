## Need and scope

Describe the requested outcome, affected components and acceptance criteria. Link the task/decision; distinguish archive inputs from tracked code.

## Changes

Explain implementation/documentation changes, API/data/installation impact and compatibility. State what is intentionally not included.

## Verification

Record exact commands, input commit/archive, environment, results and skipped checks. Link evidence. Do not equate unit tests, merge, release and deployment.

## Security and recovery

Describe permissions, secrets, tenant isolation, migrations and rollback/compensation impact. State whether an independent review occurred; do not invent one.

## Documentation and workflow

- [ ] French and English references have matching IDs, revisions and requirements.
- [ ] The central bilingual changelog reflects actual changes only.
- [ ] Relative links and documentation checks were run.
- [ ] No operational secret or unreviewed third-party code is included.
- [ ] Base/head follow `features/*` → `develop` → `stable` → `main` → `production`.
- [ ] Required checks/approvals and repository protections are respected.

## Handover

State remaining risks, owner decisions only where indispensable, and the next bounded task. Do not ask the owner to program or review code technically.
