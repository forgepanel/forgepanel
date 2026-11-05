<!-- forgepanel-doc id=FP-19-VERIFICATION revision=2 status=documented -->
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
