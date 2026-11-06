<!-- forgepanel-doc id=FP-13 revision=26 status=documented -->
# Tests, quality and definition of done

[Français](../../fr/13-tests-quality/README.md) · [Index](../README.md)

## Q171–Q220 owner decisions: planned qualification, not PASS

The [50 owner-approved directions](../00-project-control/decisions-q171-q220.md) now map to [50 PLANNED acceptance scenarios](mvp-gates-q171-q220.md), with exact bilingual option parity and C choices Q174/Q194/Q200. The accompanying JSON/documentation validation is **static only**; no real malware scanner, WAF, API, app installer, VM recovery or Hub integration test was executed. Q1–Q170 remain authoritative and Q221+ open.

## App Center: mock trust-origin separation tests

The [preflight trust boundary](../10-security/app-center-admission-trust-boundary.md) now has **three distinct synthetic input fixtures** (host facts, Core authorization claims and client intent). [39 offline preview tests](../../../tests/documentation/test_app_center_preview.py) cover unauthorized fields, spoofed host/tenant references, fake VERIFIED claims, free native installs without Docker/Hub and reserved control-plane ports. No real RBAC, host attestation or app installation is tested.

## App Center: synthetic installation preview checks

The [read-only preview prototype](../08-api-contracts/app-center-preview-contract.md) and [offline negative tests](../../../tests/documentation/test_app_center_preview.py) check runtime/driver separation, fictional CPU/RAM/PID budgets, denied site claims and hard-reserved ports 8447/8446. No real listener, OS capability, authorization or installation has been validated. The 32 HTTP/VM tests remain PLANNED.

## App Center: candidate manifest checks versus runtime tests

The [offline recipe checks](../../../tests/documentation/test_app_center_recipe_contracts.py) validate only synthetic candidate JSON and reject a selection of unsafe manifest fields, **without any installation**. The [32 app runtime/VM scenarios](app-center-engine-gates.md) remain PLANNED. No app/OS/Docker/Podman certification follows from static CI.

## App Center: native and container gates

The [APP-NAT / APP-CTR / APP-X matrix](app-center-engine-gates.md) defines **32 planned scenarios** for free native installs, Docker/Podman separation, engine-specific resources/quotas/backups, cross-engine rejection, tenant isolation, offline Hub and artifact trust. All remain **PLANNED**; no real app installation testing has been run. [Product boundaries](../06-apps-recipes/app-center-engines.md).

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

## Q151–Q156 qualification — denials and evidence

First test driver is **local QEMU/KVM** (Q151 A). A runner unable to launch a full VM reports `SKIP`/`BLOCKED`, not certification. Reports have **signature/integrity, OS/image/commit provenance, snapshots and scenario history** (Q152 C); internal matrix is not automatically published. Exercise **per-app performance budgets and version regressions** (Q153 C); approved, bounded, audited performance exceptions never waive Q132 safety vetoes. For HTTP-01 verify **only actually published A/AAAA families**, **all** present paths, without a fake missing-IPv6 failure (Q154 C). Reboot follows per-server approval, backup, health and recovery (Q155). Mark an encrypted backup « recoverable » **only after protected key export, periodic accessibility checks and a passed isolated restoration** (Q156 C); simulate unavailable vault/host. [Decisions](../00-project-control/decisions-q151-q160.md).

## Definition of done

Acceptance criteria pass at the appropriate layer; denied operations and failure recovery are tested; data/API compatibility and rollback impacts are recorded; both documentation languages and changelog are updated; evidence is attached to the exact change; risks and missing checks are visible. Product publication additionally requires release gates and authorized promotion.

A separate security review is needed before sensitive production functionality. This documentation task has an author self-review, not a second independent agent or external audit. Automated metadata equality cannot prove the translations say the same thing; manual semantic checking remains part of review.

## Q151–Q160 qualification traceability

The [positive/negative MVP test matrix](mvp-gates-q151-q160.md) defines **MVP-Q151-01 through MVP-Q160-01**, each initially **PLANNED**, with R3/R4/beta/Hub gates and evidence requirements. Priorities: genuine KVM VM, signed internal report, performance-only waiver with Q132 vetoes, HTTP-01 checks for published IP families, per-server reboot, isolated restore with key-access validation, public-key SFTP, separate consents, premium transfer risk, and signed bilingual/machine-structured advisories. The new Python test checks **case and language consistency only**, not running services.

## Q161–Q170 QA matrix

[The ten MVP-Q161-01 through MVP-Q170-01 cases](mvp-gates-q161-q170.md) remain **PLANNED**, with positive/negative behavior, R3/R4/beta/Hub phase and required evidence. Veto cases include leaked runner secret, tampered signed report, Q132 critical waiver, probe SSRF, unbounded OS recovery, backup without isolated restore, disallowed SFTP algorithm, reidentifiable cohort, suspect premium transfer and inconsistent JSON/FR/EN advisory. Static Python checks decisions/ADR/bilingual coverage; **no real hardware, Linux or restore test**.

## Real R1 preflight tool tests (and limitations)

`python3 -m unittest discover -s tests/source_intake -p 'test_*.py' -v`: **16 local unit tests PASS**, on synthetic ZIPs only. Cases: valid archive, bad SHA, missing file, dangerous paths, collisions, symlink, size/ratio controls, `.env`, private-key marker, member count and source evidence. CI integration does not certify the genuine SRC-03 archive, Go/PHP, PostgreSQL/HTTP/VM or restore. [Source provenance procedure](../12-development/source-archive-intake.md).

## Expanded R1 synthetic tests — 33 scenarios

[Provenance quarantine](../12-development/source-staging.md) and R1 preflight now have **33 synthetic unit tests**: 16 previous ZIP tests, 6 new negative cases (spoofed Unicode, embedded `.git`, privileged modes, live `.env` variants) and 11 staging cases (read-only default, private destination/modes, root and overwrite denial, staging blocked with custom `--evidence`, source mutation detection/cleanup). CI command: `python3 -m unittest discover -s tests/source_intake -p 'test_*.py' -v`. **This is not evidence of actual SRC-03 import or running application**.

## Post-staging integrity negative tests — R1

Added `tests/source_intake/test_audit_staged_archive.py` and regression cases in `test_stage_source_archive.py`. Using **only synthetic archives**, they cover ZIP/receipt/file consistency, symlinks/hardlinks, missing/unexpected files/directories, excessive permissions, forged receipts and concurrent directory substitution during staging failure. [Specification](../12-development/source-staging-audit.md). CI must run all `tests/source_intake` cases on the final SHA. Passing them does not establish a completed R1 import, HTTP/SQL, VM or real restore.

**PR #39 branch result: 60 synthetic R1 tests succeeded.** The exact commit's GitHub Actions run is authoritative; the original archive tracked by issue #2 has not been accessible or scanned. No production certification claim.

## Go KVM observation tests — preparatory R3 lot

Standalone [KVM Host Probe](../14-devops-releases/kvm-host-probe.md) has **14 synthetic Go unit tests**: character/missing/fake/symlink KVM device, exact VMX/SVM flags, other architectures, read failures, sanitized OS values and **no false VM qualification**. Its separate CI workflow runs `go test ./...`, `go test -race ./...`, `go vet ./...` and checks the real host JSON still has `qualification=NOT_EXECUTED`. **The GitHub runner is not a certified KVM system; real VMs, snapshots, failure injections, quotas, backups and restores remain PLANNED.**

## R3 — QCOW2 admission tests without real VM runs

Synthetic Go tests under `tools/kvm-host-probe/admission` and its CLI cover SHA-256, filename, private file permissions, symlink/hardlink/wrong format refusal, explicit resource ceilings, denial of network/host shares/privileges, and parity of three JSON Schemas. Existing Go CI runs **`go test ./...`, `go test -race ./...`, `go vet ./...` and `gofmt`**; check exact PR SHA results. Fixtures are not bootable Linux systems, and no real KVM run, enforced quotas, snapshot, signed report or restore has been shown. [Contract](../14-devops-releases/kvm-image-admission.md).

**PR #41 CI evidence**: [Go, race, vet, gofmt and three-schema checks](https://github.com/yyogas/forgepanel/actions/runs/42116200478) and [documentation checks](https://github.com/yyogas/forgepanel/actions/runs/42116200493) passed at commit `4a71d2fb8e0258879bcf5c621dfc29677f5e5380`. **41 Go test functions** in the module overall (14 host-probe and 27 new image/CLI/contract cases). QCOW2 fixtures are synthetic, not booted VMs or signed/isolation evidence.

## R3 — Private pinned-copy tests

New Go tests for [image staging](../14-devops-releases/kvm-image-staging.md) verify identical SHA-256 copy, 0700/0400 permissions, overwrite/symlink/nested/shared path denial, unsafe requests, source mutation, interruptions and no receipt after partial copying. CLI tests include private policy/request input gates and schema-to-Go field parity. The standalone module has **62 Go test functions total** and locally passed `go test ./...`, `go test -race ./...`, `go vet ./...`. Exact-SHA GitHub CI remains to confirm; **no QEMU guest boot or actual quota enforcement**.

## R2 — HTTP, optional MFA and PostgreSQL test matrix

[R2 integration matrix](r2-integration-gates.md) adds **20 planned scenarios**: `R2-AUTH-001..010` and `R2-DB-TEST-001..010`, each with positive and negative/denial path. [Identity](../03-core/bootstrap-identity-r2.md) and [SQL transaction](../09-database/setup-transaction-r2.md) documents remain candidates. **None of these 20 functional tests ran** on Symfony/PostgreSQL in this lot; Python documentation checks validate only FR/EN coverage/parity.

## R3 — IPC and installer matrix: 24 unexecuted cases

[R3 planned test matrix](r3-ipc-installer-gates.md) adds `R3-IPC-TEST-001..012` and `R3-INSTALL-TEST-001..012`, **24 positive/negative cases all `PLANNED`**. Python static checks validate IDs, FR/EN parity, two candidate JSON Schemas and the [closed operation registry](../../evidence/typed-agent-operations-v1.json). **No real Symfony↔Go, Linux installer, PostgreSQL or VM integration test runs as part of this matrix.**

## R3 — 24 planned durable-job and IPC-peer scenarios

[R3 matrix](r3-jobs-peer-gates.md) adds **R3-JOB-TEST-001..012** and **R3-PEER-TEST-001..012**, all PLANNED. Cases cover commit-before-ACK, same-key/different-digest, expired fencing, worker crash/recovery and uncertain Linux effect; UID/PID spoofing, socket replacement, isolated bridge, independent tenant/role authorization, saturation and version incompatibility. Candidate JSON and Python static checks prove only **document consistency**; no running PostgreSQL integration, real socket, VM or privileged effect is exercised.

## R3 — New physical, service identity and execution QA remains planned

[R3 physical QA matrix](r3-physical-execution-gates.md) specifies **36 PLANNED cases** `R3-PHYS-TEST-001..012`, `R3-LINUX-TEST-001..012` and `R3-EXEC-TEST-001..012`. Python documentation tests validate eight proposed physical DB objects, eight logical Linux identities, seven closed typed operations, both blocked privileged handlers and FR/EN parity. **No live PostgreSQL, Linux isolation or systemd effect is exercised**; real VM/HTTP/DB evidence remains a separate gate.

## R3 — Eight additional negative tests from integrity review

[R3 job integrity review](../19-audits-risks/r3-job-integrity-audit.md) adds `R3-AUDIT-TEST-001..008` **PLANNED** for denied admissions without fake jobs, fencing after deletion/restore, inbox crash before/after effect and tenant/RLS spoofing. `tests/documentation/test_r3_job_integrity_review.py` checks **only documentary guards**, including in-memory mutation regression fixtures. **Zero real PostgreSQL/Linux tests**; no automatic resolution of RISK-033..036.
