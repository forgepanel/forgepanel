<!-- forgepanel-doc id=FP-00 revision=1 status=documented -->
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

[Status and roadmap](status.md) · [Commercial/customization decisions](product-policy.md) · [Decision register](decisions.md) · [Coverage matrix](coverage.md) · [Audit](../19-audits-risks/README.md)
