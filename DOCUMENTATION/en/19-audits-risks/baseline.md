<!-- forgepanel-doc id=FP-19-BASELINE revision=1 status=documented -->
# Initial audit and source provenance

[Français](../../fr/19-audits-risks/baseline.md) · [Audit index](README.md)

Audit date: 2026-11-05. Scope: the connected `yyogas/forgepanel` repository, the visible project conversation and mounted source attachments. No other discussion, external server or private project service was assumed accessible.

## Live repository observations before modification

The connector resolved the repository and reported private visibility and read/write permissions. The contents endpoint returned `This repository is empty`; commits returned `Git Repository is empty`; branches, issues, PRs and releases returned empty collections. Actions runs returned total_count=0. No source, workflow definition or existing instruction file could therefore be read from a repository tree.

Ruleset inspection returned HTTP 403 with a plan/visibility requirement. After initialization, main protection inspection returned HTTP 403 `Resource not accessible by integration`. These results do not prove that protections are absent. The workflows-list and tags-list URLs were rejected by the connector; the Git tag-ref query reported an empty repository. No setting was relaxed or visibility changed.

The minimum initialization commit is `26b7c773a0831c20e7f14bb86ef8c2697a19d523` (README only), followed by creation of the requested branch references. The documentation PR targets `develop`; no product promotion or deployment follows automatically.

## Source inventory

| ID | Input | Authority / limitation |
|---|---|---|
| SRC-01 | Owner attachment `Texte collé.txt` | Immediate documentation/governance mandate; not a technical test report |
| SRC-02 | Visible ForgePanel/WCP360 conversation | Explicit requests and proposed architecture; earlier assistant claims require corroboration |
| SRC-03 | `ForgePanel_Foundation_v0.7_source.zip` | 92 files; CLI/setup prototype, schema, tests and reports; not tracked or released in GitHub |
| SRC-04 | `ForgePanel_Core_Foundation_v0.6_source.zip` | 14 files plus directory entries; historical CLI/doctor/file-token prototype |
| SRC-05 | `ForgePanel_v0.7_README.md`, `ForgePanel_v0.7_Test_Report.md`, `.zip.sha256` | Supplied delivery claims/checksum; distinguished from tests rerun now |

Exact hashes are in [source evidence](../../evidence/sources.json). The supplied v0.7 checksum matched the archive. The current source inspection used safe extraction rejecting path escape and symlink entries. No source archive, generated binary, dependency vendor tree or live secret is added to Git by this documentation change.

## v0.7 content map

| Path in archive | Observed content |
|---|---|
| `cmd/forgepanel`, `internal/*` | CLI, doctor, non-executable planner, fixed console bridge, release verifier and legacy token store |
| `apps/panel/src`, `config`, `templates` | Symfony setup sources, domain services, SQL repositories, routes and Twig views |
| `apps/panel/migrations/001_setup.sql` | Three bootstrap tables and uniqueness constraints |
| `contracts`, `examples` | Install-intent schema and example |
| `tests/fixtures`, `apps/panel/tests` | OS fixtures, PHP memory tests and separately gated PostgreSQL test |
| `docs`, `tests/results` | Architecture, boundaries, next milestone and historical test outputs |

No `composer.lock`, full agent daemon, package installer, WebStack provisioning, full RBAC or third-party plugin engine is present. Source names/hashes permit later exact matching; archive prose alone must not be used to reconstruct missing source. The next importer must verify the supplied bytes and record the imported commit.
