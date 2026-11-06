<!-- forgepanel-doc id=FP-00-TRACEABILITY revision=2 status=documented -->
# Requirements → contracts → tests traceability matrix

[Français](../../fr/00-project-control/requirements-traceability.md) · [Project control](README.md) · [Status](status.md)

All **22 rows** are grounded in the [bilingual gap register](documentation-readiness.md) and its [canonical data manifest](../../evidence/documentation-readiness-v1.json). These are not executed tests. Owner choices `Q1–Q170` remain product authority; `Q171+` is not approved. `P0/P1` solely propose an editorial documentation sequence. Described schemas are `CANDIDATE` unless exact execution evidence is supplied.

## Auditable initial matrix

| Trace | Lacune / gap | Phase | Q validées | Autorité | Document/contrat de référence | QA **à vérifier** | État |
|---|---|---|---|---|---|---|---|
| FP-TRACE-001 | DOC-GAP-001 | R1 | Q120 | Project Control / Engineering | [Contract](../12-development/source-staging-audit.md) | [QA](../13-tests-quality/README.md) | **BLOCKED** |
| FP-TRACE-002 | DOC-GAP-002 | R2 | Q124 Q130 | Core / Security | [Contract](../03-core/README.md) | [QA](../13-tests-quality/README.md) | **OPEN** |
| FP-TRACE-003 | DOC-GAP-003 | R2 | Q119 Q120 | Engineering / Core | [Contract](../03-core/README.md) | [QA](../13-tests-quality/README.md) | **OPEN** |
| FP-TRACE-004 | DOC-GAP-004 | R2 | Q126 | Database / Core | [Contract](../09-database/README.md) | [QA](../13-tests-quality/README.md) | **OPEN** |
| FP-TRACE-005 | DOC-GAP-005 | R3 | Q61 Q62 Q119 | DevOps / Security | [Contract](../14-devops-releases/installer-lifecycle-r3.md) | [QA](../13-tests-quality/r3-ipc-installer-gates.md) | **OPEN** |
| FP-TRACE-006 | DOC-GAP-006 | R3 | Q47 Q120 | API/IPC / Security | [Contract](../08-api-contracts/symfony-go-ipc-r3.md) | [QA](../13-tests-quality/r3-ipc-installer-gates.md) | **OPEN** |
| FP-TRACE-007 | DOC-GAP-007 | R4 | Q83 Q91 Q119 | Modules / Hosting | [Contract](../02-architecture/website-lifecycle.md) | [QA](../13-tests-quality/README.md) | **OPEN** |
| FP-TRACE-008 | DOC-GAP-008 | R4 | Q123 Q164 | Services / Security | [Contract](../02-architecture/qualification-and-security-contracts.md) | [QA](../13-tests-quality/mvp-gates-q161-q170.md) | **OPEN** |
| FP-TRACE-009 | DOC-GAP-009 | R4 | Q136 Q167 | Security / Modules | [Contract](../02-architecture/php-staging-and-access-policy.md) | [QA](../13-tests-quality/mvp-gates-q161-q170.md) | **OPEN** |
| FP-TRACE-010 | DOC-GAP-010 | R4 | Q126 Q145 Q166 | Recovery / Database | [Contract](../02-architecture/evidence-and-recovery-q161-q170.md) | [QA](../13-tests-quality/mvp-gates-q161-q170.md) | **OPEN** |
| FP-TRACE-011 | DOC-GAP-011 | R3 | Q132 Q151 Q152 Q161 Q162 | DevOps / QA | [Contract](../14-devops-releases/kvm-image-staging.md) | [QA](../13-tests-quality/mvp-gates-q161-q170.md) | **OPEN** |
| FP-TRACE-012 | DOC-GAP-012 | R4 | Q125 Q155 Q165 | DevOps / Operations | [Contract](../14-devops-releases/README.md) | [QA](../13-tests-quality/README.md) | **OPEN** |
| FP-TRACE-013 | DOC-GAP-013 | R5 | Q120 | Architecture / API | [Contract](../05-plugins/README.md) | [QA](../13-tests-quality/README.md) | **OPEN** |
| FP-TRACE-014 | DOC-GAP-014 | R6 | Q168 Q169 Q170 | Hub / API | [Contract](https://github.com/yyogas/forgepanel-hub/blob/develop/DOCUMENTATION/en/03-contracts/README.md) | [QA](https://github.com/yyogas/forgepanel-hub/blob/develop/DOCUMENTATION/en/07-tests/README.md) | **OPEN** |
| FP-TRACE-015 | DOC-GAP-015 | R6 | Q56 Q60 Q169 Q170 | Hub / Commerce | [Contract](https://github.com/yyogas/forgepanel-hub/blob/develop/DOCUMENTATION/en/08-roadmap/decisions-q161-q170.md) | [QA](https://github.com/yyogas/forgepanel-hub/blob/develop/DOCUMENTATION/en/07-tests/mvp-and-hub-gates-q161-q170.md) | **OPEN** |
| FP-TRACE-016 | DOC-GAP-016 | PRE-PUBLIC | Q111 Q112 Q118 | Legal / Governance | [Contract](license-commerce.md) | [QA](../13-tests-quality/README.md) | **OPEN** |
| FP-TRACE-017 | DOC-GAP-017 | DESIGN | Q55 Q70 Q80 | Design System / Product | [Contract](../11-design-system/README.md) | [QA](../13-tests-quality/README.md) | **OPEN** |
| FP-TRACE-018 | DOC-GAP-018 | POST-MVP | Q51 Q80 Q81 | Modules / Plugins | [Contract](../04-modules/components.md) | [QA](../13-tests-quality/README.md) | **OPEN** |
| FP-TRACE-019 | DOC-GAP-019 | POST-MVP | Q67 Q68 Q142 | Observability / Performance | [Contract](../16-performance/README.md) | [QA](../13-tests-quality/README.md) | **OPEN** |
| FP-TRACE-020 | DOC-GAP-020 | POST-MVP | Q90 Q100 | Recovery / Architecture | [Contract](../02-architecture/cross-server-migration.md) | [QA](../13-tests-quality/README.md) | **OPEN** |
| FP-TRACE-021 | DOC-GAP-021 | RELEASE | Q119 Q127 Q132 | QA / Release | [Contract](mvp-qualification.md) | [QA](../13-tests-quality/README.md) | **OPEN** |
| FP-TRACE-022 | DOC-GAP-022 | GUIDES | Q119 Q124 | Documentation / Support | [Contract](../17-user-guides/README.md) | [QA](../13-tests-quality/README.md) | **OPEN** |

## Evidence levels and work actually verified

**R3:** all KVM observation/QCOW2 admission and staging results remain `qualification=NOT_EXECUTED`. No host observation or private copy proves VM execution, OS certification or isolation.

- **R1 tooling only**: PR [#37](https://github.com/yyogas/forgepanel/pull/37), [#38](https://github.com/yyogas/forgepanel/pull/38), [#39](https://github.com/yyogas/forgepanel/pull/39) merged; [latest R1 CI](https://github.com/yyogas/forgepanel/actions/runs/42109154403) passed on **synthetic** ZIPs. Original SRC-03 source has not been imported.
- **R3 preparation only**: PR [#40](https://github.com/yyogas/forgepanel/pull/40), [#41](https://github.com/yyogas/forgepanel/pull/41), [#43](https://github.com/yyogas/forgepanel/pull/43) merged; [Go](https://github.com/yyogas/forgepanel/actions/runs/42120185132) and [documentation](https://github.com/yyogas/forgepanel/actions/runs/42120185238) CI passed. **62 synthetic Go test functions** boot no QEMU guest and certify no OS or isolation.
- **Hub candidate only**: [Hub baseline CI](https://github.com/yyogas/forgepanel-hub/actions/runs/42066987234) passed docs/contracts/prototype checks, not working Symfony/ABI/payment integration.
- **Not demonstrated**: running Symfony HTTP, PostgreSQL integration, Linux install, PHP/HTTPS, real SFTP, each-backup restore, QEMU/KVM guest, Q152 signing, deployed Hub. `PLANNED` and `SKIP` never equal `PASS`.

## Minimum traceable component record

Every owner must document **ID/version**, purpose and user flow, actor/permission/tenant, dependencies, data schema/migration, typed API/IPC request/response/errors, idempotency/timeouts/retries, allowed system action (no arbitrary shell), secrets/risks, event/log/audit, failure states/compensation, positive and negative tests, evidence on exact SHA/OS, accessible UI, FR/EN docs, compatibility/deprecation, and decision/ADR. Do not mark `VERIFIED` without actual results. Any Core ↔ Hub conflict requires review, never silently change another authority.

## Remaining documentary readiness blockers

**Structural** parity (64 Core pairs, 27 Hub pairs in inspected snapshot) is not complete business specification. Priorities: genuine SRC-03 → R2 boot/PG/identity contracts → typed agent/secure installer → PHP/ACME/permissions/restore MVP → neutral ABI, then Hub. In parallel: formally adopt/reject V3 visual baseline, finalize operative license/CLA and private reporting route, resolve undecided values, and collect real QA evidence. [Coverage](coverage.md).

## Targeted R3 candidate contract links

`FP-TRACE-005` now links to [trusted installer lifecycle](../14-devops-releases/installer-lifecycle-r3.md) and `FP-TRACE-006` to [typed Symfony↔Go IPC](../08-api-contracts/symfony-go-ipc-r3.md), with [24 PLANNED R3 scenarios](../13-tests-quality/r3-ipc-installer-gates.md). [Operation registry](../../evidence/typed-agent-operations-v1.json) is candidate data only; `DOC-GAP-005` and `DOC-GAP-006` remain **OPEN**. No Q171+ decision has been taken.
