<!-- forgepanel-doc id=FP-00-COVERAGE revision=1 status=documented -->
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
| 12 Development | Conventions, applicable commands, import boundary | Locked dependency environment pending |
| 13 Tests/quality | Evidence layers and definition of done | Integration/browser/VM campaigns absent |
| 14 DevOps/releases | Branch workflow, bootstrap exception, gates | Packages, installer, signing lifecycle absent |
| 15 Operations | Present CLI limits and future incident procedure | Working repair/backup/restore engine absent |
| 16 Performance | Measurement protocol and security constraints | Benchmarks and capacity thresholds absent |
| 17 User guides | Current limitations and intended journeys | Verified customer/reseller guides pending implementation |
| 18 Contributing | Human/AI onboarding, PR and handover | Required-review/protection visibility unresolved |
| 19 Audit/risks | Repository/archive provenance and contradictions | No exhaustive code/security/production audit |

Update this matrix whenever a gap changes state. Every `VERIFIED` feature needs named evidence on an identified input; every publication needs a real release/tag/artifact trail. Translation metadata is checked automatically; meaning is reviewed separately.
