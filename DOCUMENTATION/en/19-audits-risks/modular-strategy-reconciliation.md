<!-- forgepanel-doc id=FP-19-MODULAR-RECONCILIATION revision=1 status=proposed -->
# ForgePanel — Cross-project strategy versus existing baseline reconciliation

[Français](../../fr/19-audits-risks/modular-strategy-reconciliation.md) · [Strategy](../00-project-control/modular-development-strategy.md) · [Modules](../04-modules/progressive-release-policy.md) · [Releases](../14-devops-releases/release-lifecycle-plan.md)

**Internal consistency review (proposed; not independently audited).** The uploaded generic FR/EN source documents are **cross-project proposals**, not an automatic override of ForgePanel Q1–Q220 or R1→R6. The candidate resolutions below require ratification through existing project governance.

| Topic | Cross-project / earlier proposal | ForgePanel-specific candidate resolution | Status |
|---|---|---|---|
| Prerelease names | Earlier illustrative `v0.1.0-prealpha.1`, `v0.3.0-alpha.1`, `v0.8.0-beta.1` | Retain as **unpublished historical examples**; normalize target train to SemVer-ordered `v1.0.0-{0..5}`; `0.x` exploration still allowed before 1.0 scope freeze | Pending reconciliation |
| Pre-Alpha | Generic text says an installable demonstration and first complete workflow | R2: real **bootstrap/identity** end to end in lab plus non-executable install plan; **actual Linux installer is R3**, not Pre-Alpha | Pending reconciliation |
| First stable scope | “Minimal Core” can be mistaken for a UI-only prototype | R4 **installable/usable** PHP/HTTPS site with scoped SFTP/RBAC/VPS diagnosis and tested restoration; security cannot be deferred | Aligned, evidence missing |
| 1.x / 2.x / 3.x | Major numbers appear as product milestones | MAJOR only for incompatible public contract; compatible additions can ship as MINOR | Pending reconciliation |
| Production branch | Generic strategy prefers production as deployment environment, not necessarily a branch | **Keep** permanent `production` branch already required by ForgePanel; branch existence is not deployed-state proof | Owner baseline prevails |
| Catalog | Prior draft preserves 40 candidate modules and a developing-status preview | Retain **40 (15 Core, 25 optional)**; mark `SPECIFIED` without code evidence, no executable cards, require proof before claiming Developing | Not implemented |
| App Center | Risk of mixing native and container engines | **Free independent native ONE-CLICK**; distinct **Docker/Podman CONTAINER APPS**, never silent format conversion | Product decisions preserved |
| Hub/licensing | Private publisher may be mistaken for Core runtime dependency | R5 neutral SDK first; R6 optional private Hub later; free Core not gated by Hub | Owner baseline prevails |
| Security qualification | Risk of treating essential safeguards as future modules | Optional admin MFA but required RBAC, audit, Linux isolation, TLS, restoration and external-distribution obligations for all advertised workflows | Owner baseline prevails |
| OS/WebStack | Six OS targets could be mistaken for qualified environments | Select first OS/WebStack from **comparative real VM evidence** with exact hash/commit; add others only after qualification | Pending tests |
| Foundation source | Earlier Core docs say historical ZIP absent | v0.7/v0.7.1 archives recovered **outside Git**, but actual import into `develop` and exact-commit tests remain undone | Must correct live status after import |
| Q171–Q220 | Approved directions recorded in draft PR #53 | Preserve approved product selections, show `SPECIFIED / NOT MERGED`; detailed implementation contracts remain open | PR reconciliation pending |

## Observed blocker

Earlier writes to the `forgepanel` organization failed with **403**. The connected GitHub App now has verified write access to the separate `yyogas/forgepanel` and `yyogas/forgepanel-hub` repositories; this review is proposed on a dedicated `features/*` branch against `develop`. No independent security review, application import or release is implied. Send targeted deltas to MODULES / Security / API / Database / DevOps / QA without rescanning the full historical corpus.