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

R3 preflight separation: `tools/kvm-host-probe` is a standalone, nonprivileged, read-only QEMU/KVM host observation utility. It does not execute or certify VMs, does not sign Q152/Q162 reports, is not historical Foundation Core source and must not bypass R1/R2 gates. Tests are synthetic, and the GitHub Actions runner is not a supported-host certificate. See `DOCUMENTATION/en/14-devops-releases/kvm-host-probe.md`.

R3 image admission is a **read-only review gate**, not QEMU execution authority. `tools/kvm-host-probe/admission` accepts only pinned private QCOW2 files under explicit versioned test limits, never root or guest network/shares/privileges. `REVIEW_REQUIRED` and `artifact_verified=true` never mean VM/isolation/recovery certification or Q132 PASS. Future runner must preserve immutable verified bytes and enforce quotas independently. See `DOCUMENTATION/en/14-devops-releases/kvm-image-admission.md`.

R3 private image staging: `tools/kvm-host-probe/staging` copies admitted QCOW2 bytes into a new per-run 0700 directory with read-only 0400 files and SHA-256-bound review receipt. This is **not immutable storage or QEMU execution permission**: same-UID mutation remains possible after checking; future runner must pin and rehash exact bytes at launch. A partial stage requires manual controlled cleanup, never automatic recursive deletion. See `DOCUMENTATION/en/14-devops-releases/kvm-image-staging.md`.

R2 documentation candidate contracts live at `DOCUMENTATION/en/03-core/bootstrap-identity-r2.md`, `DOCUMENTATION/en/09-database/setup-transaction-r2.md` and `DOCUMENTATION/en/13-tests-quality/r2-integration-gates.md` (mirrored in FR). All 20 HTTP/SQL tests are PLANNED, not PASS; database schema, migration, API routes, recovery proof, TTL and limits remain subject to specialized review after original SRC-03 import. Admin MFA remains explicitly optional. Documentation CI proves parity only.

R3 contract candidates: `DOCUMENTATION/en/08-api-contracts/symfony-go-ipc-r3.md` and `DOCUMENTATION/en/14-devops-releases/installer-lifecycle-r3.md` (FR mirrored), with documentary-only `DOCUMENTATION/evidence/typed-agent-operations-v1.json` and strict IPC request/response JSON Schemas. **No executable agent or installer was created; ACT-FP-0005/0007 are BLOCKED_UNTIL_QUALIFIED**, no shell.exec or raw command args. All 24 R3 QA scenarios remain PLANNED; DOC-GAP-005/006 remain OPEN. Do not adopt candidate values as owner decisions, or authorize Q47 APPLY before R1/R2 and specialized security/VM reviews.

R3 documentary job and peer trust candidates are at `DOCUMENTATION/en/09-database/durable-jobs-r3.md` and `DOCUMENTATION/en/08-api-contracts/local-peer-trust-r3.md` (mirrored FR), with strict candidate JSON Schemas, a job-state transition registry and 24 PLANNED QA cases. Do not create SQL tables, socket services, Unix accounts, new numeric TTL/retry policy or grant privileges solely from these documents. Security must independently validate actual kernel peer credentials, actor authorization, fencing at the effect boundary and Linux/SQL recovery before implementation. The Core must operate without Hub; administrator MFA remains optional.

Leave a factual handover: completed work, remaining work, evidence, unresolved decisions, branch/commit/PR and checks not run. Never ask the owner to patch code.
