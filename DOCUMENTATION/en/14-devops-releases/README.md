<!-- forgepanel-doc id=FP-14 revision=1 status=documented -->
# Installation, Git promotion and releases

[Français](../../fr/14-devops-releases/README.md) · [Index](../README.md)

## Git workflow

`features/*` → `develop` → `stable` → `main` → `production` is the owner's required promotion sequence. Temporary feature branches include docs and fixes. Reuse a relevant branch, open a scoped PR, respect checks/reviews and preserve history. Delete obsolete temporary branches only after integration and according to repository rules. No force push or bypass is part of this workflow.

Because the repository was empty, commit `26b7c773a0831c20e7f14bb86ef8c2697a19d523` initialized `main` with a README. The other permanent branches and `features/documentation-foundation` start from that commit. This narrowly scoped bootstrap exception is documented; it is not a precedent for committing implementation directly to `main`. Protection/ruleset reads were denied, so their requirements are not assumed absent.

## Installation gates

The one-command outcome is required but no official installer URL exists. SRC-03 produces a non-executable plan with blockers for missing production apply, signed release channel and certified OS package manifests. Before releasing: verify package origin, dedicated users/runtime, schema migrations, mandatory security policies, HTTPS, local recovery and interruption/reinstall behavior on every target VM. Do not adopt existing customer services silently or perform a full OS upgrade while creating a site.

Signature verification in the prototype does not establish a production trust root, key rotation/revocation policy, persistent anti-rollback state or an installed updater. The CLI manifest check does not validate artifact bytes itself.

## Release evidence

A release must map version, tag, commit, build inputs/toolchains, dependency lockfiles, checksums, signatures, tests, OS/profile support and upgrade/rollback instructions. Keep application and documentation checks separate. No tag, release, publication or deployment is created merely by this documentation PR or by the `production` branch.

The documentation workflow is designed with read-only repository permission, pinned official actions and no deployment secrets. Its actual execution status belongs to PR checks, not an assumed badge. Runtime CI and protected promotion still need implementation after source import.
