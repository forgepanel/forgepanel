<!-- forgepanel-doc id=FP-02-Q151-GATES revision=1 status=specified -->
# Candidate qualification contracts and control gates Q151–Q160

[Français](../../fr/02-architecture/qualification-gates-q151-q160.md) · [Decisions](../00-project-control/decisions-q151-q160.md) · [Tests](../13-tests-quality/mvp-gates-q151-q160.md)

These are **proposed contracts**, not installed endpoints. CI produces evidence; Core makes local decisions. Hub receives no root, tenant backup keys or arbitrary shell command power.

| Proposed contract | Technical invariants |
|---|---|
| VmQualificationRun (Q151/152) | run_id, driver=local-kvm/cloud-later, OS/version/arch, WebStack, commit/image digest, before/after snapshots, fault plan, PASS/FAIL/SKIP, artifact hashes, signing key/version, report signature, result history; verify signatures/provenance. |
| QualificationGateDecision (Q153) | policy/version, severity, threshold, FAIL/BLOCK/PASS, waiver approver/scope/expiry/audit; never waive Q132 critical disqualifiers. |
| PublishedAddressCheck (Q154) | Observed A/AAAA, advertised family, target, port 80/HTTP-01, 443/TLS, timestamp, outcome; absent family=NOT_APPLICABLE, broken published family=FAIL; no DNS writes. |
| ServerUpdatePlan (Q155) | server_id, allowlisted packages/repos, approval, proven recoverable backup, window, health check, recovery path; never shell.exec. |
| BackupRecoveryEvidence (Q156) | backup_id/digest, off-host key recovery, isolated_restore_run_id, panel/PG/PHP verification, timestamped PASS; recoverable=true only after restore of exact backup. |
| SiteDelegationPolicy (Q157) | identity/site_ids/permissions, expiry/revocation, shell-free canonical-root SFTP, quota, sensitive-action approval, secret-free audit. |
| DiagnosticConsentAndCohort (Q158) | Separate purpose/version/withdrawal consents, minimized fields/retention, cohort_id/configurable threshold, small-cohort suppression. |
| SensitiveTransferReview/SecurityNotice (Q159/160) | Identity/org checks and compromise signals, hold only premium action, Q138 risk-based second approval and audit; signed notice, approved recipients/channels, redaction. |

Qualification requires a **real system VM and verified signed evidence**; SKIP never counts as PASS. Only noncritical, expiring audited waivers may apply; Q132 critical vetoes persist. Isolated restoration gates recoverable status. OS updates/delegation remain Core-local. Hub diagnostics/notices are post-R5, consented and minimized. Numeric thresholds are still open.
