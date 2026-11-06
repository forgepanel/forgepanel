<!-- forgepanel-doc id=FP-00 revision=15 status=documented -->
# Project control

[Français](../../fr/00-project-control/README.md) · [Index](../README.md)

## Mandate and authority

ForgePanel is a new Linux hosting control panel. The owner sets product direction and does not write code. The technical agent translates requests into specifications, implementation, tests and understandable results. Routine authorized reversible work proceeds autonomously; licensing, spending, destructive changes, visibility changes and sensitive releases require the appropriate owner decision. A technical validation cannot be delegated to the owner's ability to read code.

The conversation is MASTER / Project Control; decisions become durable only when reconciled into the repository. WCP360 is historical context, not a release name or an automatic code/license inheritance.

## Responsibilities

| Domain | Required output |
|---|---|
| MASTER, PRODUCT & MODULES | Scope, acceptance criteria, priorities and dependencies |
| ARCHITECTURE, API & CONTRACTS, DATABASE | Boundaries, versioned contracts and migration impact |
| SECURITY, ENGINEERING / CODE REVIEW, AUDIT | Threat assessment, review and unresolved risks |
| SOURCE CODE, TESTS & QA | Implementation and reproducible evidence |
| DESIGN SYSTEM, DOCUMENTATION | Accessible interfaces and synchronized languages |
| DEVOPS / RELEASE, OBSERVABILITY & PERFORMANCE | Recovery, release evidence, metrics and capacity |

These are responsibilities, not claims that separate agents or services already exist. A second reviewer is required for sensitive production changes where available; record its absence rather than inventing independence.

## Work gates

A task identifies scope and affected components, specifies acceptance criteria, implements a bounded change, verifies it, updates both languages and changelog, and records branch/commit/PR plus limitations. A passing unit test is not a release or deployment.

[Q56–Q60 decisions](commerce-identity-release-policy.md) · [Q151–Q160 decisions](decisions-q151-q160.md) · [Qualification contracts](../02-architecture/qualification-and-security-contracts.md) · [Q141–Q150 decisions](decisions-q141-q150.md) · [Qualification and backup contracts](../02-architecture/certification-backup-security.md) · [Q131–Q140 decisions](decisions-q131-q140.md) · [Q121–Q130 decisions](decisions-q121-q130.md) · [MVP qualification](mvp-qualification.md) · [Q111–Q120 decisions](decisions-q111-q120.md) · [Technical roadmap](implementation-roadmap.md) · [Q101–Q110 decisions](decisions-q101-q110.md) · [Q91–Q100 decisions](decisions-q91-q100.md) · [Q81–Q90 decisions](decisions-q81-q90.md) · [Q71–Q80 decisions](decisions-q71-q80.md) · [Per-site WebStack](../02-architecture/site-webstack-advisor.md) · [Status and roadmap](status.md) · [Commercial/customization decisions](product-policy.md) · [Dual licensing and commercial protection](license-commerce.md) · [Decision register](decisions.md) · [Coverage matrix](coverage.md) · [Audit](../19-audits-risks/README.md)

## Approved Q171–Q220 product directions

[All 50 decisions](decisions-q171-q220.md) · [Reconciliation/technical handoffs](reconciliation-q171-q220.md) · [50 PLANNED acceptance gates](../13-tests-quality/mvp-gates-q171-q220.md). The owner approved 47 D and 3 C (Q174/Q194/Q200) on 6 November 2026, not runtime implementation or VM certification. Existing Q1–Q170 remain in force. The free native One-Click installer and separate container execution are planned independently of Hub; pricing, vendor, default thresholds and technology contracts remain open.

## New Q161–Q170 decisions

[Q161–Q170 decisions](decisions-q161-q170.md) · [Qualification and recovery contracts](../02-architecture/evidence-and-recovery-q161-q170.md) · [Planned MVP tests](../13-tests-quality/mvp-gates-q161-q170.md). **Q1–Q170 remain effective; Q171–Q220 are owner-approved directions; Q221+ remain open**, no application code or certified OS is implied.

## Documentation readiness and traceability

[Gap and editorial priority register](documentation-readiness.md) · [Traceability for 22 closure records](requirements-traceability.md) · [Versioned JSON data](../../evidence/documentation-readiness-v1.json) · [Reconciled R1/R3 status](status.md). `OPEN`/`BLOCKED` describe **documentation and missing evidence**, not new Q171+ owner decisions. No R2/R3/R4 release gate is certified by these tables.

## R3 documentary IPC and installer contracts

[Typed IPC](../08-api-contracts/symfony-go-ipc-r3.md), [secure installer lifecycle](../14-devops-releases/installer-lifecycle-r3.md) and [24 planned tests](../13-tests-quality/r3-ipc-installer-gates.md) further detail `DOC-GAP-005/006` without closing their upstream prerequisites. The [seven candidate typed operations](../../evidence/typed-agent-operations-v1.json) prohibit generic root commands and keep **two privileged actions blocked**. JSON schemas describe candidates, not endpoints.
