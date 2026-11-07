<!-- forgepanel-doc id=FP-12-FOUNDATION-RECOVERY revision=1 status=documented -->
# R1 — Recovery of genuine Foundation source archives (7 November 2026)

[Français](../../fr/12-development/foundation-source-recovery.md) · [Pinned source evidence](../../evidence/sources.json) · [Recovery manifest](../../evidence/foundation-recovery-2026-11-07.json) · [Source-intake contract](source-archive-intake.md)

## What was recovered

The owner-generated historical files have been recovered from the owner's **private ChatGPT Library**, then copied to an owner-accessible private recovery folder; they were **not** uploaded into this public Git repository. In particular, the genuine `SRC-03` archive (`ForgePanel_Foundation_v0.7_source.zip`) has 92 regular members and SHA-256 `19479d5be9da9bb0ff9180f9b8819ea48baff785ccc3fef59deb2bb0894faf1a`, matching the previously recorded canonical digest. Its ZIP CRC and archive-name checks passed. The separate `v0.7.1_optional_MFA` archive has 93 regular members and SHA-256 `83fe6e77713f68d69595e74864aa1c33f75d88b6ba4199e03d5ef30a7060402c`; the historical `v0.6` has 14 and SHA-256 `8f800471ab4c2823ae6151ac478fe821cf26f5718e1449ad8f02ab0d430983b0`. These checks demonstrate matching bytes and valid ZIP records, not publisher authenticity, clean licensing or production safety.

## Checks actually executed on recovered sources

On 2026-11-07, the genuine v0.7 and v0.7.1 archives were unpacked into temporary, isolated directories and `bash scripts/check.sh` exited **0** for both as a **nonroot** Linux user with offline Go dependencies (`GOTOOLCHAIN=local`, `GOPROXY=off`, `GOSUMDB=off`). The supplied check script runs Go unit tests and race detector/vet, PHP syntax and standalone PHP-domain tests, builds the Go CLI and generates a **non-executable** install plan. Environment: Go 1.23.2 and PHP 8.4.24. The produced plan explicitly reports `executable=false`, `production_apply_not_implemented`, `signed_release_channel_not_configured` and `os_package_manifests_not_certified`.

**Not run / not verified:** real Symfony HTTP, PostgreSQL connections/transactions/concurrency, tenant isolation on a system host, OS/VM qualification, executable installation, restore, security penetration test, third-party provenance review, full license audit and release signing. The standalone test exit status is not a `VERIFIED` application release.

## Security and publication limits

Both historic v0.7 and v0.7.1 ZIPs contain a source path `apps/panel/.env`. The file's presence **does not prove whether any secret is live**, but it must not be committed to public Git without a specific secret/provenance audit. The private recovery set preserves unmodified originals; a separate proposed import candidate excludes `.env`, generated test results and historical artifacts. Core currently has **public visibility** and the exact AGPL/commercial/CLA legal terms and third-party distribution rights remain under review. A public source import therefore requires an explicit publication/security/legal gate. **Never transfer Core code to the private publisher Hub to evade this gate.**

## Current R1 state and handoff

**SOURCE RECOVERED / EXACT SHA CONFIRMED / OFFLINE NATIVE CHECKS PASSED / NOT IMPORTED INTO GIT.** The unchanged approved dependency order is R1 import → R2 real Symfony/PostgreSQL → R3 qualified installer/VM → R4 working PHP/HTTPS site → R5 neutral extension ABI → R6 optional private Hub. R1's remaining work: inspect source and rights, verify sanitized import against original per-file hashes, publish only with authorized visibility/rights, open a dedicated feature PR, rerun exact-commit tests, independent review, then integrate. See [source import issue #2](https://github.com/yyogas/forgepanel/issues/2). Earlier documents claiming the ZIP is physically unavailable are superseded **only on that factual point**; their implementation/security gate warnings remain valid.