<!-- forgepanel-doc id=FP-00-COVERAGE revision=3 status=documented -->
# Documentation coverage matrix

[Français](../../fr/00-project-control/coverage.md) · [Project control](README.md)

All categories have substantive English/French indexes and reciprocal navigation. This is documentation coverage, not a claim that every implementation specification is complete. `Documented` means scope/evidence/acceptance are described; `Partial` names missing detail; `Absent` names missing software rather than empty documents.

| Category | Coverage delivered | Remaining specification or implementation gap |
|---|---|---|
| 00 Project control | Governance, states, decisions, roadmap | License and publication decisions open |
| 01 Product | Personas, journeys, acceptance | Detailed hosting/reseller feature stories partial |
| 02 Architecture | Boundaries, dependencies, profiles | Concrete OS/package/runtime drivers absent |
| 03 Core | Actual setup state machine, target kernel | Durable agent/jobs/module registry absent |
| 04 Modules | Catalog and component records | Native hosting implementations absent |
| 05 Plugins | Trust, lifecycle, acceptance | Versioned manifest and isolation design partial; engine absent |
| 06 Apps/recipes | Recipe record and recovery requirements | Recipe schema/catalog/executor absent |
| 07 Interfaces/roles | Portals, roles, security distinction | Full scoped RBAC and permanent login absent |
| 08 API/contracts | Existing schema/routes/CLI and future envelope | Public API/agent protocol not finalized |
| 09 Database | Actual three-table schema and migration rules | Real SQL tests pending; hosting model absent |
| 10 Security | Boundaries, threats, release gates, reporting | Private channel and independent audit absent |
| 11 Design system | Brand, states, accessibility, i18n strategy | Approved visual tokens and translation infrastructure absent |
| 12 Development | Conventions and synthetic-tested R1 ZIP preflight/copy/audit tools | Original Foundation v0.7 source missing; application dependencies unlocked |
| 13 Tests/quality | Definition of done and synthetic R1/R3 developer-tool tests | HTTP/SQL, actual VM, isolation, backup and restore campaigns not run |
| 14 DevOps/releases | Git workflow, gates and standalone R3 KVM observation/admission/staging | Packages/installer, VM execution, signatures and OS qualification missing |
| 15 Operations | Present CLI limits and future incident procedure | Working repair/backup/restore engine absent |
| 16 Performance | Measurement protocol and security constraints | Benchmarks and capacity thresholds absent |
| 17 User guides | Current limitations and intended journeys | Verified customer/reseller guides pending implementation |
| 18 Contributing | Human/AI onboarding, PR and handover | Required-review/protection visibility unresolved |
| 19 Audit/risks | Repository/archive provenance and contradictions | No exhaustive code/security/production audit |

Update this matrix whenever a gap changes state. Every `VERIFIED` feature needs named evidence on an identified input; every publication needs a real release/tag/artifact trail. Translation metadata is checked automatically; meaning is reviewed separately.

## Closure registry after the observed Git snapshot audit

The initial audited snapshot contained **64 Core FR/EN pairs** and **27 Hub FR/EN pairs**; those are **historical counts, not the current repository inventory**, but **substantive specification completeness is still partial**. The [22 prioritized gaps](documentation-readiness.md) link to issues/dependencies in the [JSON register](../../evidence/documentation-readiness-v1.json) and [traceability](requirements-traceability.md). [Reconciled status](status.md) separates merged R1/R3 developer tools from absent operational Symfony/PG/VM/hosting features. No independent legal/security certification is implied.

## Coverage growth after the original audit snapshot

[Candidate PostgreSQL physical model](../09-database/physical-jobs-model-r3.md), [Linux identities](../14-devops-releases/linux-service-identities-r3.md), [typed execution](../08-api-contracts/typed-execution-recovery-r3.md) and [36 PLANNED QA cases](../13-tests-quality/r3-physical-execution-gates.md) add four paired documentary resources, **not working-feature completion**. Obtain live counts from `scripts/check_documentation.py` rather than copying stale snapshot totals. The 22-gap readiness register still tracks unclosed functionality.
