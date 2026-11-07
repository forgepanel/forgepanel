<!-- forgepanel-doc id=FP-00-MODULAR-STRATEGY revision=1 status=proposed -->
# ForgePanel — Modular development and progressive release strategy through 3.x

[Français](../../fr/00-project-control/modular-development-strategy.md) · [Module roadmap](../04-modules/progressive-release-policy.md) · [Release lifecycle](../14-devops-releases/release-lifecycle-plan.md) · [QA gates](../13-tests-quality/modular-release-gates.md)

**Status: candidate project adaptation in a review PR, not merged into develop.** Source owner documents dated 7 November 2026: `STRATEGIE_DEVELOPPEMENT_MODULAIRE.md` and `MODULAR_DEVELOPMENT_STRATEGY.md`. Preserve decisions Q1–Q220, R1→R6 prerequisites and Git history; this document must not silently replace an unreconciled decision or baseline. Unspecified vendors, prices, periods, limits, dates and final version numbers remain open.

## 1. Engineering outcome

Ship an **intentionally small yet complete, secure and usable v1.0**: on a genuinely qualified OS/WebStack, an administrator installs ForgePanel, creates an independent account, manages at least one PHP site/domain/HTTPS configuration with scoped files/SFTP and permissions, observes basic VPS state, and can actually restore configurations and data. The Core operates **without** private Hub, optional modules, App Center, Docker/Podman, local authoritative DNS, a mail stack, marketplace or HA.

Non-deferable protections include authentication, authorization and tenant separation, audit, Linux isolation, artifact verification, real backup/restore, and applicable external-distribution obligations. **Admin MFA remains optional**, available later and with separately approved step-up controls. Never introduce an arbitrary privileged shell API.

Preserve project architecture: **Symfony/PHP + Twig/UX**, **PostgreSQL** control data, **Go** typed system operations, separate FORGE `/forge:8447` and PANEL `/panel:8446` sessions/RBAC/UI. Historic source archives and design mockups are not a deployed runtime.

## 2. Four separate notions of version and readiness

| Dimension | Example | Does NOT prove |
|---|---|---|
| Core / contract version | `v1.0.0`, `v1.1.0` | An independently qualified plugin |
| Build maturity | Dev, Pre-Alpha, Alpha, Preview, Beta, RC, GA | Distribution access or actual installation |
| Distribution | `Dev`, `Beta`, `Stable` with internal/closed/public audience | Compatibility with untested operating systems |
| Module progress | `PLANNED`, `SPECIFIED`, `DEVELOPING`, `TESTING`, `AVAILABLE` | Install or runtime authorization |

**SemVer 2.0:** compatible fixes increment PATCH, compatible capabilities increment MINOR, public-contract breaking changes increment MAJOR with an explicit migration/deprecation plan. `2.0` / `3.0` are **aspirational product milestones**, not automatic obligations to break compatibility. Experiments may stay in `v0.x`; after freezing 1.0 scope use the train `v1.0.0-0.dev.N` → `-1.prealpha.N` → `-2.alpha.N` → `-3.preview.N` → `-4.beta.N` → `-5.rc.N` → `v1.0.0`. The numeric stage prefix preserves SemVer ordering; internal/closed alpha and private/public beta are different **audiences**, not separate SemVer stages. None of these tags is claimed published.

## 3. Required implementation order R1 → R6

| Gate | Verifiable result | Release effect |
|---|---|---|
| **R1** | Source v0.7 verified/reviewed for provenance, rights/secrets and imported to Git; reviewed v0.7.1 optional-MFA delta; checks run on imported commit SHA | Internal development only until integrated |
| **R2** | Real Symfony/PostgreSQL bootstrap, initial account/recovery, optional MFA, HTTP/CSRF/session/RBAC, real SQL rollback/concurrency | Lab Pre-Alpha with **non-executable install plan** |
| **R3** | Typed authorized Go agent and authenticated IPC, signed/verified installer actually executed and recovered in disposable VMs | Internal Alpha, real OS evidence required |
| **R4** | Isolated PHP site, external-DNS checks, HTTP-01/HTTPS, site-manager, files/SFTP, bounded VPS maintenance, encrypted backup and **actual isolated restore** | First functional MVP; then Closed Alpha, Beta, RC and GA |
| **R5** | Versioned neutral extension API/SDK tested with a **non-Hub** test extension | Candidate compatible `1.x` feature, never a Core boot dependency |
| **R6** | Private detached Hub with licensing/catalog/distribution optional to standard Core | After R5, never a prerequisite of free Core |

**Cross-document reconciliation:** the generic strategy expects a demonstrable end-to-end Pre-Alpha workflow. ForgePanel R2 must demonstrate **bootstrap/identity end to end in a laboratory**, not claim the full Linux installer is working before its R3 gate. This sequencing exception preserves Q119/Q120 and does not weaken Beta/GA installation requirements.

## 4. Stable v1.0 / essential MVP scope

- Verified installer and recovery, demonstrated on **at least one** OS+WebStack combination selected by comparative VM/security/recovery evidence (Q121/Q122); not invented six-OS support.
- Accounts, auth, sessions, scoped RBAC/site-manager, **optional MFA**, auditing, protected secrets and transactional PostgreSQL control plane.
- Isolated PHP/FPM site, external DNS **guidance without automatic changes**, actual published A/AAAA checks, port 80/ACME HTTP-01 and real HTTPS.
- Files/site-scoped shell-disabled SFTP with tenant-negative tests, one qualified site SQL engine.
- VPS diagnosis/safe planned upgrades, logs, encrypted backups with accessible recovery keys and **proved isolated restore**.
- **Read-only module catalog** showing truthful status, documentation and planned targets, whose UI outage cannot prevent Core bootstrap, website serving or recovery.

Stable v1.0 **does not depend on** ONE-CLICK INSTALL, Docker/Podman, native DNS, mail server, theming editor, reseller, multi-server or Hub. Future modules may appear as informational cards but must not be represented as shipped. v1.0 remains production-grade for its **declared** small scope.

## 5. Deferred optional trains — candidates, not commitments

| Indicative train | Candidate scope | Independent entry gate |
|---|---|---|
| `v1.1.x` | **Free native ONE-CLICK INSTALL**, Git Deploy, generic extension ABI R5 | Verified native recipes, tenancy, backup, provenance; no container/Hub prerequisite |
| `v1.2.x` | **Docker CONTAINER APPS**, staging, additional SQL/cache, WebStack switch, advanced observability; Hub R6 **after R5** | Driver-specific containers/network/volume/quotas/restore tests, neutral ABI |
| `v1.3.x` | Independent **Podman CONTAINER APPS**, local DNS, Postfix/Dovecot, candidate detection-first WAF, malware scanning | Each OS/driver, signature, isolation and failure/recovery qualified separately |
| `v1.4.x+` | Webmail, reseller, visual layout editor, advanced Configuration Center, cross-server migration, billing connectors | Scoped RBAC/decisions, migration and real recovery |
| `2.x` | Multi-server, HA/DR, orchestration/VM features **when justified** | Measured capacity, distributed consistency, failover and restore |
| `3.x` | Ecosystem governance, multi-version compatibility, measured scaling/cross-region resilience | No required new MAJOR version solely for product positioning |

**Unfinished independent modules move to a later release train without delaying the Core**, provided their absence breaks no promised essential workflow and their runtime is absent or disabled. The [40-entry candidate registry](../../evidence/forgepanel-modular-roadmap-proposed-v2.json) preserves the earlier 15 essential Core capabilities and 25 optional modules/extensions. Every registry entry is a **non-operational** candidate: no installation or activation authority.

## 6. Contracts and failure containment

Start with a **modular Symfony monolith** (rather than mandatory premature microservices), a least-privilege Go executor boundary and separate detached services where required. Future server-side capability resolution evaluates dependencies, proven OS profiles, API versions, permissions, plan limits, conflicts and actual resource availability. **Visibility, availability and activation remain independent controls**. A “Developing” card is never permission to execute.

Do not load optional routes, workers, jobs, service hooks or SQL migrations in mandatory Core bootstrap when a module is absent/unqualified. A failed optional service must not stop existing sites, login or local recovery. Security-critical invariants are always Core guards. Disable/uninstall follows retention, backup and recovery policy and never deletes tenant data silently. No general privileged command execution is allowed.

## 7. Delivery process, release quality and Git

Prioritize `MUST / SHOULD / COULD / LATER` and limit concurrent WIP. Deliver small complete slices **UI → authorization → business logic → API/data → audit → tests → docs**; a genuine PHP site matters more than many decorative screens. Retain **ForgePanel-specific, owner-approved** `features/* → develop → stable → main → production` Git branches: the generic document's suggestion that `production` could be environment-only does **not** override the already-existing permanent branch. A branch is not a deployment. Build one digest-bound artifact, then promote identical signed bytes. Scoped PRs, exact commit QA, no force pushes or review bypass; hotfixes are reviewed/backported on supported lines.

Release checks have explicit PASS / FAIL / BLOCKED / NOT RUN states on **shipped** functionality. Before external release review AGPL/commercial/CLA and third-party rights, verify a confidential security-reporting channel, run genuine VM/HTTP/SQL/restore/security tests, document support and FR/EN changelog. LTS/EOL periods and specific provider values remain open. **Owner-approved product directions Q171–Q220 are on Core draft PR #53, not merged into develop**, and do not grant runtime approval.

## 8. Observed state and targeted handoffs

- Original Foundation v0.7/v0.7.1 archives were **recovered and prepared outside Git**; this is not an authorized/imported Core commit.
- Core `develop` still does not evidence a fully installable, qualified hosting product. Standalone preparatory Go/JSON tooling does not change this.
- GitHub feature-branch creation in the `forgepanel` organization currently fails with **403**. This is a **locally prepared proposal**, not merged/adopted as the canonical baseline, published, deployed or tested as an operating module system.
- Handoffs: **MASTER** for release adoption, **Modules/Architecture** for manifests/resolver, **Security/API/Database** for scopes/migrations/IPC, **QA/DevOps** for real gate evidence, **Design** for informational catalog, and **Hub** for separate R6 scope after R5.

[Release-train proposals](../../evidence/forgepanel-release-trains-proposed-v2.json) · [Planned modular QA](../../evidence/forgepanel-modular-qa-proposed-v1.json). **No operating functionality or certification is established by these documents.**