<!-- forgepanel-doc id=FP-13 revision=1 status=documented -->
# Tests, quality and definition of done

[Français](../../fr/13-tests-quality/README.md) · [Index](../README.md)

## Evidence must name its scope

A test record identifies input commit/archive hash, tool versions, environment, command, result and untested boundaries. `SKIP` is not `PASS`. Current [verification evidence](../19-audits-risks/verification.md) separates tests rerun on SRC-03 from documentation validation and unexecuted integration work.

| Layer | Present evidence | Next gate |
|---|---|---|
| Go prototype | Six packages tested, race detector and vet | Repeat against imported commit; maintained release toolchain selection |
| PHP setup domain | Custom runner: 28 tests / 184 assertions | Expand denial/recovery cases; do not call this PHPUnit |
| Syntax | PHP lint on 26 entry points/files | Real framework/container/template checks |
| PostgreSQL | Test source exists | Rollback, concurrency, restarts and restore on real database |
| HTTP/browser | Source guards/templates only | HTTPS, CSRF, sessions, origins, rate limits and E2E |
| Six OS / five profiles | Fixture selection logic | Disposable VM installation, upgrade, reinstall, failure/recovery matrix |
| Documentation | Checker and bilingual review | Relative links, mirrored metadata, nonempty content, limited secret scan |

PHPUnit, Go testing, Playwright, Bats, static analysis and load tools remain the target quality stack where relevant. Do not claim those pipelines exist just because they were recommended. Docker-only tests do not replace VM validation of Linux service/security behavior.

## Definition of done

Acceptance criteria pass at the appropriate layer; denied operations and failure recovery are tested; data/API compatibility and rollback impacts are recorded; both documentation languages and changelog are updated; evidence is attached to the exact change; risks and missing checks are visible. Product publication additionally requires release gates and authorized promotion.

A separate security review is needed before sensitive production functionality. This documentation task has an author self-review, not a second independent agent or external audit. Automated metadata equality cannot prove the translations say the same thing; manual semantic checking remains part of review.
