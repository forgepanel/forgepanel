<!-- forgepanel-doc id=FP-02-Q151-160 revision=1 status=specified -->
# QEMU/KVM qualification, tested recovery and SFTP/beta controls — Q151–Q160

[Français](../../fr/02-architecture/qualification-and-security-contracts.md) · [Decisions](../00-project-control/decisions-q151-q160.md) · [MVP](../00-project-control/mvp-qualification.md)

## Evidence pipeline: Q151 A, Q152 C

The first implementation targets **local QEMU/KVM**, not cloud. Candidate `VmQualificationDriver`: `preflightKvm()`, `createFromPinnedImage()`, `snapshot()`, `injectFailure()`, `restore()`, `collectReport()`, `destroy()`. Detect KVM/nested virtualization and label unavailable execution `SKIP/BLOCKED`, never a false `PASS`. Q141's common driver interface enables **later cloud** VM adapters without duplicating test definitions.

Candidate `QualificationEvidence`: immutable OS image/digest, architecture, VM resources, WebStack profile, commit and signed artifact, toolchain, snapshot, scenario results, redacted logs, signer and immutable report history. A **signature** demonstrates report provenance/integrity, not that an untested system is secure. Maintain an **internal** supported/failed/not-tested matrix; Q152 C does not choose mandatory public publication.

## Performance budgets and safety vetoes (Q153 C)

`PerformanceBudgetPolicy` by application type: metric samples, pinned baseline environment, allowed budgets, severity and blocking thresholds. On regression, explain the comparison and **block** when criticality or threshold warrants it. `PerformanceException` needs requester, authorized approver, reason, scope/version, duration/revision and audit. **Never waive** Q132 tenant isolation, `.htaccess` access rules, TLS, listener safety or **recovery** hard gates. Numeric limits remain open.

## Only published IP families (Q154 C)

Read **actually published A and/or AAAA** for each hostname. Validate **each published family** for correct destination, public routing, vhost/proxy, port 80 and ACME HTTP-01 challenge, followed by valid HTTPS 443. Missing AAAA is not an error if only A is published, and vice versa. If both exist, neither may mask the other's failure. Suggest record fixes and **recheck after manual action** under Q143, without provider mutations.

## Per-host reboot policy (Q155 C)

`ServerRebootPolicy`: host/owner, approved maintenance, affected package, impact, approver, plan digest, recoverable snapshot/key, reboot state, post-health and recovery/compensation. Recheck authorization immediately before reboot; never accept generic `shell.exec`. Q144 allows **later** group orchestration; R4 is single-host with CLI/admin recovery preserved where feasible.

## Backups: actual decryption and restore proof (Q156 C)

Target states `CREATED → INTEGRITY_VERIFIED → KEY_ACCESS_VERIFIED → ISOLATED_RESTORE_PASSED → RECOVERABLE`. Q156 C requires **protected recovery key/reference export**, **periodic accessibility checks** and **real isolated restoration**, validating config/files, permissions/integrity and internal panel PostgreSQL where needed. Redact logs. A key on the same lost disk is insufficient; Q145 D external KMS/multiple custodians remain **optional**.

## Public-key management and SFTP (Q157 C)

Q136 site manager may **register/revoke SFTP public keys** within account policy, with authorized identity/site, key validation, expiry, sensitive-action approval, enforced quotas and canonical site root. **Private keys** remain customer-side; no shell by default. Revocation must deny new sessions and handle existing ones under policy, never erase hosted files. Audit approvals and login outcomes.

## Beta local health and consent (Q158 C)

`BetaCohortPolicy` combines manual reports, **local** health checks and specifically opted-in minimal diagnostics. Separate purpose consents (version/update, diagnostics, marketing) under Q6, never automatic customer files/SQL/mail collection. Configurable thresholds per **cohort** halt new waves and invoke recovery even when testers **decline telemetry**; Core remains usable offline/without Hub.

## Publisher contracts deferred (Q159 C, Q160 C)

Core can verify signed installation evidence for optional premium integration, but **transfer/fraud risk** belongs to future Hub: lost source, repeated/unusual transfers, inconsistent organization/identity or suspected compromise with Q138 risk-triggered second approver. Future **advisories** expose two views of the **same signed versioned source**: human-readable FR/EN on site/Panel and machine-readable structured payload, configurable notices and restricted sensitive details. Do not make Hub connectivity a requirement for free Core or assume advanced interoperability standards not selected.

**State: candidate contracts and test matrix only; no functioning VM, backup, SFTP or active API is delivered.**
