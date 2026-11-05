<!-- forgepanel-doc id=FP-12-SOURCE-AUDIT revision=1 status=documented -->
# Independent R1 quarantine verification

[Français](../../fr/12-development/source-staging-audit.md) · [Preflight](source-archive-intake.md) · [Private staging](source-staging.md) · [Audit and risks](../19-audits-risks/README.md)

## Purpose and status

`scripts/audit_staged_archive.py` is a **read-only** consistency check for privately staged files before human review. It compares **three objects**: (1) the original ZIP pinned in `DOCUMENTATION/evidence/sources.json`, (2) staging receipt `.forgepanel-intake-receipt.json`, and (3) actual on-disk files. Genuine `ForgePanel_Foundation_v0.7_source.zip` (SRC-03, 92 files) remains **unavailable** in the current context: no real-archive, imported PHP/Go or runtime test is claimed.

## Commands

```bash
# The exact original ZIP must still be available.
python3 scripts/audit_staged_archive.py \
  --archive /local/path/ForgePanel_Foundation_v0.7_source.zip \
  --directory "$HOME/forgepanel-intake/foundation-v07"

# Synthetic-only unit tests for preflight, staging and verification:
python3 -m unittest discover -s tests/source_intake -p 'test_*.py' -v
```

The CLI uses **canonical** SRC-03 evidence. It extracts, executes and changes nothing. `CONSISTENT_FOR_MANUAL_REVIEW` means archive/receipt/member **consistency at verification time**, **not** safe source code, approved import or certified production. Any discrepancy returns `BLOCKED` with exit code 2.

## Invariants and denials

| Area | Check |
|---|---|
| Original ZIP | Full SHA-256 and file count must match SRC-03; publisher trust, license and provenance still need independent review |
| Receipt | Strict schema/types, `import_approved=false`, `executed=false`, `STAGED_FOR_MANUAL_REVIEW`; receipt digest entries must exactly match **actual** source ZIP member hashes |
| Private target | Canonical absolute path, privately owned directory and no symlink aliases or shared directory modes |
| Inventory | Every expected regular file must exist; deny unexpected, missing or replaced files/directories and unsafe names |
| File integrity | Compare SHA-256/size and pre/post-read metadata; reject symlinks, extra hardlinks, FIFOs, executable files, shared permissions or ownership changes |
| Fail closed | Limit receipt/file sizes and never claim a valid state after concurrent changes or vanished members |

## Additional staging hardening

The quarantine tool now rejects **relative destinations**, shared intermediate directories and alternate CLI `--source-id` values during `--stage`. Failure cleanup is anchored to its **private parent directory descriptor** and the created directory's **device/inode identity**. If the target was replaced, cleanup is **skipped with a blocker** rather than risking deletion of an unrelated directory. A successful staging attempt also rechecks its directory identity before returning a receipt.

## Limits and remaining risks

All branch tests use **synthetic archives**; there is no real SRC-03, Symfony/PostgreSQL or Linux installer verification. This is not an antivirus, exhaustive secret scan or license audit; it **cannot prevent a malicious process under the same user identity from modifying files after the check**. A later import PR must re-open and re-hash files during its own import transaction and retain versioned evidence; the audit status is not an authorization token.

**Required sequence:** exact source ZIP → pinned archive preflight → private staging → independent byte audit → human security/license review → Core source import PR with actual Go/PHP checks → R2 integration. No generic `shell.exec`, no elevated Linux privileges and no Hub dependency.
