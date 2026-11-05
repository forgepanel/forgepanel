<!-- forgepanel-doc id=FP-12 revision=2 status=documented -->
# Development environment and conventions

[Français](../../fr/12-development/README.md) · [Index](../README.md)

## Repository work available now

The repository has no imported application source, but now includes both documentation checks and read-only R1 source-intake tooling. From the repository root, run `python3 scripts/check_documentation.py`. Python is documentation tooling only; the product runtime remains PHP/Go. Review [AGENTS.md](../../../AGENTS.md) and the [handover](../18-contributing/handover.md) before taking a task.

Code, identifiers, technical comments, commit messages and technical paths are English. Owner communication is French. Official documents are mirrored with common IDs/revisions; any translation delay must be recorded with scope and a completion task. Do not duplicate normative rules across root entry files.

## Supplied archive development

After a separately reviewed import, SRC-03 supports `go test ./...`, `go test -race ./...`, `go vet ./...`, `php apps/panel/tests/run.php`, `make build` and `bash scripts/check.sh`. These are not currently root-repository commands. The PHP runner is custom, not PHPUnit. PHP requires Sodium and Argon2id for these native tests. The archive manifest requires PHP >=8.2 and Symfony 7.4 packages; `go.mod` declares 1.23.0. Lab tool versions are not release support policy.

Composer dependencies are not locked or installed in the archive. Resolve, inspect, lock and audit them in an isolated integration environment without bypassing platform requirements. Add actual Symfony container, YAML, Twig and routing checks before exposing HTTP. PostgreSQL tests require a dedicated authorized test database; never substitute production credentials.

## Change boundaries

Keep business rules out of controllers and OS-specific details out of domain contracts. Add bounded types and error semantics before privileged operations. Do not import third-party code without license/provenance assessment. Generated binaries, caches, vendor trees and real secrets do not belong in this initial source baseline.

A new agent must inspect the current working tree and remote heads, reuse relevant branches, avoid overlapping shared-file edits and leave exact evidence. A development container does not certify systemd, firewall, quota or mandatory-access-control behavior on target VMs.

## R1 intake: testable code tooling

`scripts/verify_source_archive.py` verifies the genuine SRC-03 archive **read-only** before any import. It compares checksum and inventory against pinned evidence, inspects ZIP safety and emits a JSON report, never executing or installing archived code. **16 synthetic-only unit tests** run in CI. The PHP/Go application Core remains **unimported**. [Contract and usage](source-archive-intake.md).
