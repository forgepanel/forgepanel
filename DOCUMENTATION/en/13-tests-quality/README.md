<!-- forgepanel-doc id=FP-13 revision=5 status=documented -->
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

## Q119 B first-release acceptance gate

The first usable release needs an **end-to-end test on an authorized VM**: verified artifact install, optional-MFA initial setup, permanent admin login, real PostgreSQL, create PHP website, validate domain, valid HTTPS certificate, successful HTTPS request, RBAC denials, diagnosis and recovery from failed config. Include TLS failure, IP:port conflict and denied permission tests. Name OS/WebStack/commit and exact results; Go fixtures, in-memory PHP tests and documentation CI do not certify hosting. [Q120 D roadmap](../00-project-control/implementation-roadmap.md).

## Revised qualification gate (Q121–Q127)

Before choosing **the first OS/WebStack**, compare VMs/profiles for security, packages, PHP, listeners, HTTP/TLS and recovery (Q121/122). Verify **external** DNS, HTTP-01 challenge on **port 80**, HTTPS success and bad DNS/IPv6/port cases (Q123). Test admin/website-manager permission separation, local recovery, sessions/CSRF and optional MFA (Q124); planned/authorized/audited/recoverable OS package operations (Q125); **real restore** of panel config and PHP-site files with coherent panel PG state where needed (Q126). Only then consider **private beta** after external-distribution and verified security-reporting gates (Q127). [MVP matrix](../00-project-control/mvp-qualification.md). **No such integration test was run in this docs PR.**

## Additional Q131–Q132 certification gates

Automate **full system VMs** locally and in CI with snapshots, fault injection and **OS/version/WebStack/commit** reports per scenario. Report recovery and distinguish `SKIP` from success. **Initial WebStack** selection compares measured load, tenant/`.htaccess` security, service maintenance, TLS/ports and restore; **reject** profiles causing listener collisions, tenant disclosure or unrecoverable failure even with high benchmark scores.

## Q133–Q136 MVP DNS, OS, backup and role tests

Test A/AAAA including IPv4/IPv6, port 80, HTTP-01 routing, external domain and HTTPS 443; OS updates with impact/backup/health/recovery including interruption/reboot; **encrypted local** panel/PHP-file backups with real restoration and usable recovery key, **optional** remote destination; site-manager RBAC denials for OS packages, other sites, quota bypass and foreign backups. [Detailed matrix](../00-project-control/mvp-qualification.md). **None of these tests was run by this docs PR.**

## Q141–Q143 comparable tests and Q146 SFTP

**Q141 D**: local/cloud VM drivers and CI runners emit a **common** OS/version/architecture/commit/WebStack report with scenario results, snapshots, simulated failures and restore evidence. Never count `SKIP` as `PASS` or a container as a full Linux VM.

**Q142 D**: configure **performance budget per application type** and version baseline, compare throughput/errors/latency/CPU/RAM on equivalent infrastructure, and track regressions. **Q132 disqualifying** `.htaccess`/tenant/TLS/listener/recovery faults override speed. No invented numbers.

**Q143 C**: test suggested external DNS records and recheck A/AAAA/IPv6, 80/HTTP-01, 443/HTTPS and certificate **after manual changes**, without granting automatic provider DNS writes.

**Q145 D/Q146 C**: restore an encrypted archive on a separate VM using genuinely accessible recovery keys; simulate lost host/vault and optional KMS outage. Verify shell-disabled SFTP roots, expiry/revocation, quotas, cross-tenant denial and real access audit. [Q141–Q150 matrix](../00-project-control/decisions-q141-q150.md). **Docs changes do not create VM evidence.**

## Definition of done

Acceptance criteria pass at the appropriate layer; denied operations and failure recovery are tested; data/API compatibility and rollback impacts are recorded; both documentation languages and changelog are updated; evidence is attached to the exact change; risks and missing checks are visible. Product publication additionally requires release gates and authorized promotion.

A separate security review is needed before sensitive production functionality. This documentation task has an author self-review, not a second independent agent or external audit. Automated metadata equality cannot prove the translations say the same thing; manual semantic checking remains part of review.
