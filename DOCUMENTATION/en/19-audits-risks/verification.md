<!-- forgepanel-doc id=FP-19-VERIFICATION revision=7 status=documented -->
# Verification record

[Français](../../fr/19-audits-risks/verification.md) · [Audit index](README.md)

## Fresh source-archive checks

Input: SRC-03, SHA-256 `19479d5be9da9bb0ff9180f9b8819ea48baff785ccc3fef59deb2bb0894faf1a`. Linux amd64 container; Go 1.23.2; PHP CLI 8.4.24. These are actual laboratory versions, not publication recommendations. Commands ran outside the Git repository on the safely extracted supplied archive with Go network resolution disabled.

| Command / check | Observed result | Boundary |
|---|---|---|
| Archive SHA-256 comparison | PASS | Matches supplied checksum, not a trusted publisher signature |
| `bash scripts/check.sh` | Exit 0 | Native archive checks only |
| `go test ./...` | Six packages pass | No installed system services |
| `go test -race ./...` | Six packages pass | Exercised tests, not proof of all races absent |
| `go vet ./...` | Pass | Static checks of this source/toolchain |
| PHP syntax checks | 26 files/entry points pass | Syntax, not framework execution |
| `php apps/panel/tests/run.php` | 28 tests, 184 assertions, 0 failures | In-memory repository |
| `make build`, CLI version/plan | Pass | Local executable; plan remains non-executable |
| `forgepanel install apply` | Exit 64, expected refusal | No production apply engine |
| `php apps/panel/tests/postgres.php` | Exit 77, SKIP | PDO driver list empty; no authorized test database |

The original archive's historical logs are separate evidence. No Symfony boot, Composer dependency resolution/audit, PostgreSQL concurrency, browser test, six-OS install, web hosting, TLS provisioning or performance benchmark was executed in this documentation task. No production binary was published.

## Documentation checks

The repository checker validates 20 indexes per language, paired relative paths, metadata IDs/revisions/status, selected shared requirement identifiers, relative file links, one changelog, JSON syntax and a small set of secret patterns. It cannot establish semantic translation equivalence, test applications or prove absence of all secrets. The author also reviews source/statements and both languages; no independent reviewer is claimed.

Actual run status must be read from the documentation PR's checks and logs. Adding a workflow file alone is not a successful CI run. Any failed or skipped check must remain visible in the task report and be corrected or explicitly recorded before promotion.

## Observed documentation evidence

[PR #1](https://github.com/yyogas/forgepanel/pull/1) at head `04e75476fce679714429c62ac83897262b64fa45` passed [Actions run 41948356066](https://github.com/yyogas/forgepanel/actions/runs/41948356066): 10 checker tests, 28 document pairs, 64 Markdown files and 282 relative links. GitHub tested the temporary merge preview `de3b954943728538e5bcfbb0d0b3351a0ea8db87`; the PR was not merged. The downloaded snapshot passed the same checks locally.

The successful run warned that its pinned v4 actions targeted a deprecated Node runtime. This follow-up pins verified official Node 24 action commits (checkout v7.0.1 and upload-artifact v7.0.2) without increasing repository permissions. Its own CI outcome must be checked on the updated PR head, not inferred from the earlier run.

## Additional R1 verification: no real SRC-03 rescan

**Local command**: `python3 -m unittest discover -s tests/source_intake -p 'test_*.py' -v`. **Observed result**: 16/16 PASS on Linux/Python stdlib, with synthetic archives only. Negative cases: wrong SHA, missing archive, absolute/Windows/traversal paths, symlinks, duplicates, count/size/ratio and recognizable secrets. **The genuine v0.7 source archive was unavailable**; no product Go/PHP, PostgreSQL, VM or actual restore was executed in this lot. Exact SHA GitHub CI is checked independently. [Tool](../12-development/source-archive-intake.md).

## Additional verification — quarantined file integrity

`tests/source_intake` now also covers the independent `audit_staged_archive.py` utility: positive/negative synthetic ZIP/receipt/disk consistency, link/mode/content/inventory denial, and replacement-race cleanup checks. **Read results on the exact PR-head and post-merge commits**, without reusing earlier CI outcomes. No actual Foundation archive, running Core or certified OS is claimed. [Contract](../12-development/source-staging-audit.md).

**R1 extension (PR #39):** 60 synthetic preflight/staging/audit unit tests succeeded. Denial cases include same-size and different-size content drift, directory replacement during cleanup, links, executable modes and forged receipts. No Foundation runtime, PostgreSQL, VM or actual backup was tested. [Verification CI](https://github.com/yyogas/forgepanel/actions/runs/42108723238).

## R3 verification: pinned QCOW2 image admission

**PR #41 CI evidence**: [Go, race, vet, gofmt and three-schema checks](https://github.com/yyogas/forgepanel/actions/runs/42116200478) and [documentation checks](https://github.com/yyogas/forgepanel/actions/runs/42116200493) passed at commit `4a71d2fb8e0258879bcf5c621dfc29677f5e5380`. **41 Go test functions** in the module overall (14 host-probe and 27 new image/CLI/contract cases). QCOW2 fixtures are synthetic, not booted VMs or signed/isolation evidence.

This pass validates no QEMU runner, isolated VM, enforced quotas or imported Foundation Core.

## R3 evidence ledger — candidate contracts only

[R3 matrix](../13-tests-quality/r3-ipc-installer-gates.md) and [candidate IPC schemas](../08-api-contracts/symfony-go-ipc-r3.md) get **static** Python checks for FR/EN parity, required IDs, absence of generic shell fields and blocked privileged actions. Real CI results must be linked to the exact executed SHA. **None** of `R3-IPC-TEST-001..012` or `R3-INSTALL-TEST-001..012` has run on a real agent, socket, installer or VM. Earlier R1/R3 preparatory-tool PRs do not certify this protocol. No independent security review is claimed.
