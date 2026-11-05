<!-- forgepanel-doc id=FP-14 revision=5 status=documented -->
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

## Release evidence

A release must map version, tag, commit, build inputs/toolchains, dependency lockfiles, checksums, signatures, tests, OS/profile support and upgrade/rollback instructions. Keep application and documentation checks separate. No tag, release, publication or deployment is created merely by this documentation PR or by the `production` branch.

The documentation workflow is designed with read-only repository permission, pinned official actions and no deployment secrets. Its actual execution status belongs to PR checks, not an assumed badge. Runtime CI and protected promotion still need implementation after source import.
