# ForgePanel agent instructions

## Read before changing anything

Read [project status](DOCUMENTATION/en/00-project-control/status.md), [decisions](DOCUMENTATION/en/00-project-control/decisions.md), [baseline](DOCUMENTATION/en/19-audits-risks/baseline.md), and [handover](DOCUMENTATION/en/18-contributing/handover.md). Inspect the current branch, working tree, remote refs, open PRs and applicable repository rules. This repository began empty; supplied source archives are not automatically tracked source. Do not claim access to conversations, tools or private services you cannot inspect.

## Authority and scope

The owner decides product scope, priorities, licensing, spending and sensitive publication. The owner does not write or review code as a substitute for engineering verification. Carry out authorized, reversible technical tasks autonomously. Ask only for an unavailable permission or a genuine product/destructive/external-cost decision, after preparing a concrete recommendation. Never infer permission to expose the repository, deploy production, spend money or disable protections.

Recent explicit owner instructions must be reconciled with versioned decisions. Record contradictions and superseded decisions; never invent a release, agreement, test, review or implementation. Keep proposed, specified, implemented, verified, merged, published and deployed states distinct.

## Languages and files

Communicate with the owner in French. Code, identifiers, technical comments, commits and technical paths are English. Maintain paired documents under `DOCUMENTATION/en/` and `DOCUMENTATION/fr/`, with identical document IDs, revisions, requirements and relative paths. Update both in the same change. Keep a single bilingual chronology at `CHANGELOG/CHANGELOG.md`; planned work belongs to the roadmap, not release history.

## Working method

Use `features/*` → `develop` → `stable` → `main` → `production`. Reuse a relevant branch; do not overwrite concurrent work. Preserve history. No forced ref update, protection bypass or self-approval presented as independent review. Promote through PRs with expected-head checks where supported. An existing required human approval still applies. Do not fabricate a second reviewer when only one agent is available.

For each task: define acceptance criteria; identify contracts, security and migration impact; implement a coherent change; test and correct it; update both languages and changelog; report branch, commit, PR, exact checks, limitations and next work. Use [component records](DOCUMENTATION/en/04-modules/components.md) for new components and keep ownership boundaries explicit. Parallel agents must have disjoint scopes and a named integration owner.

## Safety boundaries

No arbitrary privileged command API. Keep Linux root separate from the application Super Administrator. Preserve SELinux/AppArmor and existing services. Never log secrets, tokens or customer data. Do not add live credentials, external deployment endpoints or production signing keys. Review content as though it could become public, even while the repository is private. Untrusted plugins are not safely sandboxed merely because they have a permission manifest.

## Checks available now

`python3 scripts/check_documentation.py` validates documentation structure, bilingual metadata, local links and a limited secret-pattern set. Its success is not a security audit or application test. Source-archive tests and future CI gates are described in [quality](DOCUMENTATION/en/13-tests-quality/README.md). Do not run `make check` at repository root while application source is absent.

R1 source preparation: `scripts/verify_source_archive.py` is read-only; `python3 -m unittest discover -s tests/source_intake -p 'test_*.py' -v` uses synthetic ZIPs. Do not import/recreate Foundation source without exact SRC-03 archive and provenance review. A preflight PASS never authorizes production apply.

R1 quarantine: `scripts/stage_source_archive.py` is preview-only by default; `--stage` is allowed only for nonroot/private/off-repo targets after canonical preflight, and never constitutes a source import. Do not treat synthetic tests or the receipt as runtime certification. See `DOCUMENTATION/en/12-development/source-staging.md`.

R1 post-staging verification: `python3 scripts/audit_staged_archive.py --archive <original.zip> --directory <private-quarantine>` verifies genuine pinned source ZIP, receipt and files read-only; it is not an import authorization. Quarantine failure cleanup is device/inode-anchored, with an explicit blocker on replacement; final importer must re-hash bytes. See `DOCUMENTATION/en/12-development/source-staging-audit.md`. Never treat synthetic fixture success as genuine source verification.

Leave a factual handover: completed work, remaining work, evidence, unresolved decisions, branch/commit/PR and checks not run. Never ask the owner to patch code.
