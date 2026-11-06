<!-- forgepanel-doc id=FP-14 revision=17 status=documented -->
# Installation, Git promotion and releases

[Français](../../fr/14-devops-releases/README.md) · [Index](../README.md)

## Git workflow

`features/*` → `develop` → `stable` → `main` → `production` is the owner's required promotion sequence. Temporary feature branches include docs and fixes. Reuse a relevant branch, open a scoped PR, respect checks/reviews and preserve history. Delete obsolete temporary branches only after integration and according to repository rules. No force push or bypass is part of this workflow.

Because the repository was empty, commit `26b7c773a0831c20e7f14bb86ef8c2697a19d523` initialized `main` with a README. The other permanent branches and `features/documentation-foundation` start from that commit. This narrowly scoped bootstrap exception is documented; it is not a precedent for committing implementation directly to `main`. Protection/ruleset reads were denied, so their requirements are not assumed absent.

## Installation gates

The one-command outcome is required but no official installer URL exists. SRC-03 produces a non-executable plan with blockers for missing production apply, signed release channel and certified OS package manifests. Before releasing: verify package origin, dedicated users/runtime, schema migrations, mandatory security policies, HTTPS, local recovery and interruption/reinstall behavior on every target VM. Do not adopt existing customer services silently or perform a full OS upgrade while creating a site.

Signature verification in the prototype does not establish a production trust root, key rotation/revocation policy, persistent anti-rollback state or an installed updater. The CLI manifest check does not validate artifact bytes itself.

## Sensitive configuration apply (Q47)

The installer and service controllers must show impact plans, validate prerequisites and signatures, preserve relevant state, apply under locks, verify health and document recovery/compensation. Preserve a safe admin path when changing ports or firewall. Irreversible operations require explicit disclosure before confirmation. See [Configuration Engine](../02-architecture/configuration-engine.md).

## Channels and progressive rollouts (Q57)

The target provides **Stable, Beta, Dev**, pilot cohorts, progressive rollout, verified artifacts and controlled recovery. Hub may publish metadata; local Core authorizes updates. Code rollback alone cannot undo an irreversible database migration. Automation defaults remain open; no real update engine is implemented. See [Q56–Q60](../00-project-control/commerce-identity-release-policy.md).

## Secure installation and release (Q61, Q62)

Target: simple verified bootstrap and signed **DEB/RPM** repositories for all six OS targets, CI/CD builds with signed artifacts/metadata, anti-rollback and approval gates. Package signatures alone do not prove compatibility. Keep publisher private signing keys out of the installer. Test interrupted installs, idempotent retry and recovery. See [Q61–Q70](../00-project-control/infrastructure-decisions.md). No operational release has occurred.

## Controlled adoption and trust chain (Q71, Q72)

Q71 adds protected KMS/HSM or signing service, anti-rollback metadata and key rotation, without selecting a provider. Q72 supports servers already running services via **read-only discovery → takeover plan → backup → confirmation → validation/recovery**, alongside clean install. Installer must refuse to overwrite unmanaged files/services without explicitly verified ownership. Both paths require real conflict/VM testing before declared supported. [Specification](../00-project-control/decisions-q71-q80.md).

## First-release scope and order (Q119 B, Q120 D)

**R1 provenance-preserving source import → R2 real Symfony/PostgreSQL/identity/optional-MFA tests → R3 verified tested installer → R4 manageable PHP site, domain and HTTPS plus minimal VPS administration → R5 generic detached-extension ABI → R6 private Hub.** The [roadmap](../00-project-control/implementation-roadmap.md) defines VM/HTTP/SQL and recovery gates; Hub follows the first usable Core release. Q119 B does not require all OSes/WebStacks or native DNS/mail in the first gate. Before public distribution complete license/CLA review (Q111/Q112) and verify both private security-report channels (Q118). None is operationally completed by this documentation.

## Qualification and private distribution (Q121–Q127)

**Q121/122:** no default first OS/WebStack; select only from VM/security comparison. **Q123:** externally managed DNS, ACME HTTP-01 on port 80 and automatic HTTPS. **Q124:** local admin plus website-manager role/recovery. **Q125:** VPS observation and allowlisted, planned, authorized, verified OS package upgrades, never arbitrary root shells. **Q126:** real panel-config/PHP-site-files backup and restore, consistently restoring needed panel PG state. **Q127:** test internally first, then **private** beta after evidence, software distribution/recipient rights and actually verified security channels. Docs do not authorize any production deployment. [MVP qualification](../00-project-control/mvp-qualification.md).

## Q131–Q137 VMs, OS updates and beta gates

Full system **local/CI VMs**, snapshots, fault injection and OS/WebStack reports distinguish `SKIP` from PASS. First stack selection requires compatibility, security, measured load, maintenance, recovery and hard rejection. MVP verifies DNS **A/AAAA**, **port 80/HTTP-01**, **HTTPS**, actionable diagnostics and site-manager rights (including **real SFTP allowed on owned site and cross-tenant denial**), planned OS updates with backup/health/recovery, and restored **encrypted local** backup (optional remote). Private beta proceeds by waves only after legal/security prerequisites and pause/recovery capability. [Decisions](../00-project-control/decisions-q131-q140.md).

## Q141–Q147 — first-release qualification and controls

**Local/cloud VM drivers** with compatible CI and common snapshot/failure reports (Q141); **per-application performance budgets** and cross-version regressions (Q142) subject to Q132 security veto. Initial assistant **suggests external DNS records** and rechecks A/AAAA/80/HTTP-01/HTTPS **without automatic DNS writes** (Q143). OS updates use **per-server policies** with impact, backup, health and recovery (Q144); mandatory multi-server orchestration is not an MVP gate. Encrypted local backups need **off-failure-domain recoverable keys**, vault and optional external KMS/multi-custodian policy (Q145). Test shell-disabled expiring/revocable/quota-audited SFTP (Q146). Private beta waves pause on configurable health/critical incident gates with recovery, not data erasure (Q147). [Requirements](../00-project-control/decisions-q141-q150.md).

## Q151–Q158 release qualification

First test driver is **local QEMU/KVM**, preserving Q141 abstraction for later cloud VMs. Keep **signed provenance**, snapshots/history and explicit `SKIP` (Q152), without assuming public compatibility publication. Per-app regressions block according to severity/budget unless an **audited performance-only exception** is authorized; security vetoes cannot be waived (Q153). External DNS HTTP-01 validates **published A/AAAA families** only (Q154). OS upgrade/reboot is **per server** with approval/backup/health/recovery (Q155); encrypted archives are recoverable only with **checked key availability and actual isolated restore** (Q156). Test expiring/audited public SFTP keys on real host (Q157). Beta waves under Q158 use **local health + manual reports + separately opted-in minimal diagnostics** and cohort thresholds without forced collection. [Q151–Q160](../00-project-control/decisions-q151-q160.md).

## Release evidence

A release must map version, tag, commit, build inputs/toolchains, dependency lockfiles, checksums, signatures, tests, OS/profile support and upgrade/rollback instructions. Keep application and documentation checks separate. No tag, release, publication or deployment is created merely by this documentation PR or by the `production` branch.

The documentation workflow is designed with read-only repository permission, pinned official actions and no deployment secrets. Its actual execution status belongs to PR checks, not an assumed badge. Runtime CI and protected promotion still need implementation after source import.

## R1 source archive intake gate

The new `scripts/verify_source_archive.py` preflight reads genuine SRC-03 **without extracting, installing or executing anything**, checking checksum, paths and bounded expansion. It is not an installer and never authorizes `install apply`. A PASS must be followed by licensing/secret review and tests on the actual imported commit; the genuine archive remains missing in this lot. [Procedure](../12-development/source-archive-intake.md).

## R1 — quarantine is not deployment

`stage_source_archive.py` only copies verified regular source files to a private **off-repository** directory as nonroot, with read-only preview by default and explicit `--stage`. Existing target, other-user-writable parent, suspicious metadata or changed source → deny. Receipt `STAGED_FOR_MANUAL_REVIEW` includes `import_approved=false`: no install, release signing, migration or privileged execution can follow automatically. Genuine ZIP remains unavailable; R1 import and R2–R6 gates remain blocked. [Procedure](../12-development/source-staging.md).

## R1 — integrity receipt is neither a release nor import approval

`audit_staged_archive.py` can **read-only** confirm the quarantine still matches pinned SRC-03 source ZIP. Even `CONSISTENT_FOR_MANUAL_REVIEW` never authorizes `install apply`, compilation, deployment or automated Git import: manual license/secret review and re-hashing at final source import remain necessary. [Procedure](../12-development/source-staging-audit.md).

## R3 — Read-only local QEMU/KVM preparation

A **standalone Go module outside historical Core** provides a [KVM candidate host observation](kvm-host-probe.md) (Q151 A, Q161 C). It reads fixed Linux metadata and prints JSON without booting any VM, root commands or collecting host identity. **It runs no isolation, snapshot, quotas, evidence signature or OS installation test.** The ephemeral QEMU/KVM runner and immutable reports remain future R3 work; R1 Foundation source import remains blocked by the missing original archive.

## R3 — Pinned local QEMU/KVM image admission

The standalone Go [R3 Image Admission](kvm-image-admission.md) tool read-only verifies a local QCOW2 image using a full SHA-256 and a private nonroot-owned directory. CPU/RAM/duration must have explicitly versioned local policy ceilings; guest network, host shares and privilege flags are refused. Its positive state is **`REVIEW_REQUIRED`**, not proof of any QEMU boot or enforced quota. Q151 A/Q161 C only prepare ephemeral KVM runners; Q152/Q162 signed immutable evidence remains unimplemented.

## R3 — Preparatory private QCOW2 staging

After [KVM host observation](kvm-host-probe.md) and [SHA-256 admission](kvm-image-admission.md), [verified private staging](kvm-image-staging.md) copies pinned image bytes into a **fresh per-run 0700 directory** as nonroot. The 0400 copy/receipt are re-hashed and bind versioned policy/request digests, but no guest is booted, durable immutability or real quotas enforced, or report signed. Failed partial directories require controlled manual cleanup. R3, Q152/Q162, R1 and R2 gates remain unqualified.

## R3 — Secure installer lifecycle candidate contract

[R3 installer lifecycle](installer-lifecycle-r3.md) specifies `INST-FP-0001..0012`, publisher trust/signatures/revocation/anti-rollback, per-OS VM qualification and `DRAFT → PLAN → PREFLIGHT → SNAPSHOT → STAGE → APPLY → VERIFY → COMMIT` or `RECOVER`, subject to Q132 critical vetoes. Candidate [ACT-FP-0005/0007](../../evidence/typed-agent-operations-v1.json) remain **blocked**: no working `install apply`, installation URL, signed package or privileged executor is supplied. [24 planned R3 scenarios](../13-tests-quality/r3-ipc-installer-gates.md).

## R3 — Candidate Linux service identity and privilege matrix

[Linux identity specification](linux-service-identities-r3.md) defines `LINUX-FP-0001..0012` for **8 logical roles**: Symfony HTTP, private bridge, nonroot Go, disabled privileged handler, DB migrator/runtime, hosted site and observer. [Candidate register](../../evidence/candidate-r3-linux-service-boundaries-v1.json) creates **no Unix UID, group, socket or systemd unit**. `DynamicUser`, socket path, service accounts, LSM profiles and DB grants need real VM qualification. [12 Linux tests planned](../13-tests-quality/r3-physical-execution-gates.md).
