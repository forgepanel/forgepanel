<!-- forgepanel-doc id=FP-12-SOURCE-STAGING revision=1 status=documented -->
# Controlled source quarantine staging — R1

[Français](../../fr/12-development/source-staging.md) · [Preflight](source-archive-intake.md) · [Roadmap](../00-project-control/implementation-roadmap.md) · [Risks](../19-audits-risks/README.md)

## Purpose and status

**Implemented Python utility:** \`scripts/stage_source_archive.py\` prepares a copy of **regular files** from a verified ZIP in a private, entirely new directory. **Default mode writes nothing.** It is not a Linux installer, Git import or extension loader.

The original \`ForgePanel_Foundation_v0.7_source.zip\` remains unavailable here. Canonical [SRC-03 evidence](../../evidence/sources.json) pins 92 files and SHA-256 \`19479d5be9da9bb0ff9180f9b8819ea48baff785ccc3fef59deb2bb0894faf1a\`. **No PHP/Go application source has been imported or executed.**

## Two separate commands

\`\`\`bash
# Preview mode: read-only, does not create destination.
python3 scripts/stage_source_archive.py \
  --archive /local/path/ForgePanel_Foundation_v0.7_source.zip \
  --destination "$HOME/forgepanel-intake/foundation-v07"

# After manually preparing a privately owned, non-shared parent,
# explicitly copy into a destination that does not already exist:
mkdir -m 700 -p "$HOME/forgepanel-intake"
python3 scripts/stage_source_archive.py \
  --archive /local/path/ForgePanel_Foundation_v0.7_source.zip \
  --destination "$HOME/forgepanel-intake/foundation-v07" --stage
\`\`\`

\`--stage\` enables copying; it **rejects root execution, parent directories writable by others, existing destinations and destinations inside the source repository**. The \`--evidence\` option is available for read-only diagnostics and tests but **cannot override the canonical evidence for CLI \`--stage\`**.

## Implemented controls

- **Verify before writing:** match ZIP SHA-256 and 92-file count against SRC-03, reusing read-only R1 preflight.
- **Reject unsafe metadata:** traversal, absolute paths, duplicate/casefold collisions, noncanonical/spoofed Unicode names, embedded \`.git\`, sensitive \`.env\` variants, symlinks/special entries and setuid/setgid modes.
- **Copy conservatively:** use Linux directory descriptors with \`O_NOFOLLOW\`, files created with \`O_EXCL\` and mode **0600**, directories mode **0700**, never preserve archived execute bits.
- **Recheck exact bytes:** compare staged member sizes/digests to preflight entries and recheck original ZIP checksum; stop and remove partial destination when data changes.
- **Retain provenance:** create private \`.forgepanel-intake-receipt.json\` (0600) with ZIP checksum, sorted member hashes, \`STAGED_FOR_MANUAL_REVIEW\`, \`import_approved=false\` and \`executed=false\`. Receipt is **not** security authorization.

**Never** run staging as root or copy the entire staging directory directly into Core. Work in a separately owned nonprivileged directory. Licensing, secret, dependency and code review and any source transformations are separate gates.

## Evidence and limitations

\`python3 -m unittest discover -s tests/source_intake -p 'test_*.py' -v\` runs **33 synthetic unit tests**: 16 existing, 6 extra unsafe ZIP-member checks and 11 quarantine cases. Local checks passed; the exact CI result must be verified in the PR. Genuine SRC-03 bytes, real Go/PHP code, Symfony/PostgreSQL, operating systems and restore testing are **not verified by this change**.

A private, never-overwritten target reduces side effects but cannot replace manual review or publisher trust. Next: recover genuine archive → preflight → private staging → review files/licensing → separate R1 source-import PR → real Go/PHP checks → R2 integration. [Source issue #2](https://github.com/yyogas/forgepanel/issues/2).
