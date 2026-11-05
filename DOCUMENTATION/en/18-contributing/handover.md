<!-- forgepanel-doc id=FP-18-HANDOVER revision=4 status=documented -->
# Handover to the next contributor

[Français](../../fr/18-contributing/handover.md) · [Contribution guide](README.md)

## Current lot

Documentation/governance foundation, not application development. Work branch: `features/documentation-foundation`; integration base: `develop`; bootstrap commit: `26b7c773a0831c20e7f14bb86ef8c2697a19d523`. Read the live branch head and PR before editing; do not assume this document's creation commit is still current. PR/commit identifiers for the completed lot are recorded in its GitHub discussion and task report.

Completed scope: live repository inspection; private/empty baseline recorded; requested permanent refs initialized without deployment; paired documentation for 20 categories; component inventory, decisions, coverage and risks; single bilingual changelog; root contribution/security/agent instructions; documentation validation tooling. Supplied v0.7 native tests were rerun separately. Application sources were not imported and no product release was created.

## Next bounded task: source import

Recover the exact SRC-03 archive from the supplied project inputs and verify its recorded SHA-256. Do not recreate missing code from prose or presume a working tree already contains it. Review license/provenance, secret placeholders, generated outputs and historical documentation. Import only intended source/contracts/tests in a separate feature PR. Preserve archive identity in the commit/PR, keep historical evidence clearly labeled and migrate useful rules into the central bilingual documentation without creating another changelog.

Repeat tests on the actual imported commit. Then prepare Symfony/PostgreSQL integration with dependency lock/audit, real HTTP/SQL/concurrency tests and explicit non-production environment. Do not skip ahead to a network-exposed root installer.

## Unresolved gates

License/contribution terms and private security reporting contact need owner decisions before external publication. Runtime/package policy, full identity, agent execution, TLS, six-OS certification and signed distribution remain technical work. Repository protection reads were denied; do not bypass them. There was no independent review in this lot.

Report what changed, exact commands/results, branch/commit/PR, remaining blockers and a concrete next task. The owner is not expected to program, correct files or approve code technically.

## Tracked follow-up

The documentation lot is [PR #1](https://github.com/yyogas/forgepanel/pull/1). [Issue #2](https://github.com/yyogas/forgepanel/issues/2) tracks source import; [issue #3](https://github.com/yyogas/forgepanel/issues/3) tracks Symfony/PostgreSQL integration and depends on #2; [issue #4](https://github.com/yyogas/forgepanel/issues/4) tracks licensing and private reporting decisions. These issues describe work to do, not completed implementations. Before continuing, read the actual PR state and current `develop` head; creation of the PR did not merge it.

## Updated R1 handover — intake safety

The read-only `scripts/verify_source_archive.py` and 16 synthetic tests are available with [bilingual instructions](../12-development/source-archive-intake.md). It **imports nothing**. Next priority remains obtaining genuine SRC-03 ZIP, SHA-256/92 files recorded in [evidence](../../evidence/sources.json), then manual license/secret review and versioned source import PR into `develop`. Real Go/race/vet/PHP checks and R2 must follow; keep `install apply` disabled until qualified. The owner is not expected to code.

## R1 handover — quarantine preparation complete, actual import still open

Source intake now includes `verify_source_archive.py` and `stage_source_archive.py`, **33 synthetic tests**, [FR/EN documentation](../12-development/source-staging.md) and CI. Preview mode writes nothing; `--stage` only copies verified files into a fresh nonroot private off-repository destination and receipt requires **manual review**, not automatic import. Next real work: recover **original SRC-03 ZIP**, verify checksum, inspect licensing/diffs/secrets, then open a **separate source-import PR** with actual Go/PHP checks. R2 Symfony/PostgreSQL depends on that import. V3 UI stays a candidate, Hub separate.
