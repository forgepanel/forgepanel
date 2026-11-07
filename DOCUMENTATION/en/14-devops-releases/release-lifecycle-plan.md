<!-- forgepanel-doc id=FP-14-RELEASE-LIFECYCLE revision=2 status=proposed -->
# ForgePanel — Release trains, channels and gates from 1.0 through 3.x

[Français](../../fr/14-devops-releases/release-lifecycle-plan.md) · [Project strategy](../00-project-control/modular-development-strategy.md) · [DevOps](README.md) · [Release registry](../../evidence/forgepanel-release-trains-proposed-v2.json)

**Updated candidate of the earlier unmerged Release Lifecycle proposal.** This adaptation supersedes only its **illustrative tag examples**; it does not rename historical `Foundation v0.7/v0.7.1` archives or existing Git commits. A version here never proves a Git tag, signed build, public release or deployment.

## 1. SemVer-compatible stage scheme

Prereleases of a **single 1.0 train**, using numeric stage prefixes for SemVer ordering:

| ID | Stage | Example tag | Proposed installed channel | Audience | Evidence needed |
|---|---|---|---|---|---|
| FP-REL-01 | Development | `v1.0.0-0.dev.1` | Dev | Internal | R1 exact-head source import/provenance/tests |
| FP-REL-02 | Pre-Alpha | `v1.0.0-1.prealpha.1` | Dev | Internal | R2 real Symfony/PG setup and HTTP/SQL identity slice; **not** a working Linux installer |
| FP-REL-03 | Internal Alpha | `v1.0.0-2.alpha.1` | Dev | Engineering | R3 verified agent/IPC/installer in disposable VMs |
| FP-REL-04 | Closed Alpha | `v1.0.0-2.alpha.2` | Dev | Private testers | R4 isolated PHP/HTTPS site, SFTP, restored backup |
| FP-REL-05 | Technical Preview | `v1.0.0-3.preview.1` | Beta | Limited | Honest scope, FORGE/PANEL UX and accessibility |
| FP-REL-06 | Private Beta | `v1.0.0-4.beta.1` | Beta | Invitation only | Qualified R4, security/legal review and cohort recovery |
| FP-REL-07 | Public Beta | `v1.0.0-4.beta.2` | Beta | Informed public | Licenses, signed artifacts, upgrades, actual OS support matrix |
| FP-REL-08 | Release Candidate | `v1.0.0-5.rc.1` | Beta | Controlled | Frozen 1.0 scope, real regression/security/upgrade/restore |
| FP-REL-09 | Stable / GA | `v1.0.0` | Stable | Authorized production | Accepted RC, immutable signed artifacts, support/docs |

`.1/.2` numbers are illustrative, not reserved. Distribution audience is separate from the tag. Compatible fixes are PATCH (`1.0.1`), new compatible modules MINOR (`1.1.0`) and breaking public contracts MAJOR with a documented migration/deprecation. **Never create a `v2.0.0` or `v3.0.0` solely to mark a marketing milestone**; they are aspirational product trains. Security hotfixes do not need nine stages. Support/LTS windows are not yet fixed.

## 2. Non-waivable gates

R1: source SHA/inventory, license/secret review, actual feature PR into `develop`, Go/PHP and FR/EN tests on the **imported SHA**, no active installer. R2: running Symfony HTTP and PostgreSQL transactions, initial enrollment, CSRF/sessions, optional MFA, tenant RBAC, migration, concurrency/rollback. R3: typed authorized IPC/peer identity, signed installer, genuine QEMU/KVM VM evidence and recovery; evidence-based pilot OS/WebStack selection. R4: externally hosted DNS, published A/AAAA validation including independent external probing, HTTP-01/HTTPS, isolated PHP/FPM, scoped shell-disabled SFTP, safe planned VPS operations, encrypted backup with an **actually successful isolated restore**, and consistent panel PostgreSQL recovery. R5: neutral API tested with a non-Hub extension, Core remains standalone. R6: private detached Hub without Linux root or Core availability dependency.

Preview/Beta do not waive security, licenses, privacy or third-party rights. Private Beta needs authorized distribution, verified confidential reporting, actual data-protection/recovery and stoppable cohorts. Public Beta needs signed provenance, documented supported versions and upgrades. RC freezes features and closes P0/P1, including required independent review and known limitations. GA requires explicit publication authorization, exact signed-artifact testing, FR/EN notes, support and security. Claim **only independently qualified modules actually shipped**. Defer incomplete optional modules to compatible MINOR releases rather than blocking the Core train.

## 3. Owner-specific Git flow takes precedence

`features/* → develop → stable → main → production` remains ForgePanel's **existing permanent branch policy**. The cross-project strategy sometimes prefers `production` as an environment only; ForgePanel **retains the branch** until an explicit future decision. The immutable `vX.Y.Z` tag belongs on the approved `main` SHA; `production` tracks authorized promotion/deployment **but is not deployment evidence**. Build one digest-bound artifact and promote the same signed bytes. Exact-head checks, reviews and PRs are mandatory, with no force push or self-approval. `hotfix/*` and backports apply to supported release lines.

## 4. Release manifest and evidence

Require version/tag/SHA; DOC/DESIGN baselines; requirements/API versions; SBOM, third-party rights/licenses; actually qualified OS/WebStack; reproducible toolchain/build; artifact hash/signature; migrations and backups; PASS/FAIL/BLOCKED/NOT RUN cases; restore/security evidence; independent audit where required; extension/locale/theme compatibility; rollback **or recovery**; limitations, channel/audience, FR/EN notes, approval, and separate `PUBLISHED` / `DEPLOYED` status. Never invent completion percentages; `SKIP` is not qualification.

The [release registry](../../evidence/forgepanel-release-trains-proposed-v2.json) is explicitly unpublished. The [module roadmap](../04-modules/progressive-release-policy.md) permits deferral of independent optional modules, never a critical safeguard. R5 ABI and R6 Hub do not block the first R4-based Core Stable. External distribution remains subject to AGPL/commercial/CLA legal, verified private security channels, package provenance and third-party rights review.