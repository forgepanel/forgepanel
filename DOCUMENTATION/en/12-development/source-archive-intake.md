<!-- forgepanel-doc id=FP-12-SOURCE-INTAKE revision=1 status=documented -->
# Secure source ZIP preflight before R1 import

[Français](../../fr/12-development/source-archive-intake.md) · [Development](README.md) · [Provenance](../19-audits-risks/baseline.md) · [Roadmap](../00-project-control/implementation-roadmap.md)

## Purpose and status

**Read-only ZIP verifier: IMPLEMENTED. Synthetic archive tests: 16 local PASS. Core source import: BLOCKED.** The original SRC-03 archive \`ForgePanel_Foundation_v0.7_source.zip\` is unavailable among currently accessible files and has not been imported.

Pinned [\`sources.json\`](../../evidence/sources.json) records SRC-03 as **92 files** with SHA-256 \`19479d5be9da9bb0ff9180f9b8819ea48baff785ccc3fef59deb2bb0894faf1a\`. **A matching hash establishes identity against that record, not publisher authenticity, licensing or safety.**

## Usage once the genuine archive bytes are available

\`\`\`bash
python3 scripts/verify_source_archive.py --archive /local/path/ForgePanel_Foundation_v0.7_source.zip
python3 -m unittest discover -s tests/source_intake -p 'test_*.py' -v
\`\`\`

The utility performs **no extraction, execution, installation, Linux modification or network request**. Local JSON reports the ZIP checksum, file count, per-member digests, warnings, blockers and \`PASS\`/\`BLOCKED\` status. Exit **0** = preflight passed; **2** = blocked. A preflight \`PASS\` never authorizes \`install apply\` or publishing a release.

## Implemented safety properties

- **Provenance**: compare exact SHA against SRC-03 **before member inspection**; reject missing or changed archives.
- **Paths**: deny ZIP Slip (\`..\`), absolute/Windows paths, empty components, casefold collisions, duplicates and file/directory conflicts.
- **Types**: reject symbolic links, Unix special entries, encrypted members and unapproved compression methods.
- **Bounds**: limit size/count/compression ratio, stream data with CRC checks and SHA-256 per member.
- **Secrets**: block a small set of recognizable private-key/token signatures and \`.env\` files without echoing values; warn on key/certificate extensions.

Current **defensive implementation limits**: 64 MiB ZIP, 2,048 entries, 32 MiB/entry, 160 MiB total expanded, compression ratio 500. These are **not owner-approved commercial ForgePanel quotas**; changing them requires a review and tests.

## Limits and next gates

All 16 cases use **synthetic ZIP fixtures only**. Pattern-based secret screening is not exhaustive or a legal review, a hash is not a publisher trust chain, and a valid ZIP does not establish PHP/Go/Symfony/PostgreSQL or operating-system safety. **No genuine SRC-03 scan occurred in this lot because the bytes are absent.**

Next R1 under [issue #2](https://github.com/yyogas/forgepanel/issues/2): recover exact archive → run preflight → manually review files/license/secrets/history → import only approved source in \`features/* → develop\` → run Go/race/vet/PHP tests on imported commit → R2 Symfony/PostgreSQL. [Handover](../18-contributing/handover.md).
