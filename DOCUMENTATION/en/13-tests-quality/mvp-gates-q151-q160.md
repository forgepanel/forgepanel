<!-- forgepanel-doc id=FP-13-Q151-MATRIX revision=1 status=specified -->
# MVP: tests and qualification gates Q151–Q160

[Français](../../fr/13-tests-quality/mvp-gates-q151-q160.md) · [Decisions](../00-project-control/decisions-q151-q160.md) · [Architecture](../02-architecture/qualification-and-security-contracts.md) · [Existing MVP](../00-project-control/mvp-qualification.md)

**All cases are PLANNED, not PASS.** Static documentation checks cannot prove a VM, restoration, Hub API, ACME challenge or server update. Future evidence must name the commit, OS image, runner, WebStack, tool versions, snapshots, signed proof, PASS/FAIL/SKIP, environment and reviewer.

| Test ID | Stage | Expected success | Mandatory negative case |
|---|---|---|---|
| MVP-Q151-01 | R3 | Real local QEMU/KVM system VM, snapshot, installer and failure/recovery | Unavailable KVM or container-only tests → BLOCKED/SKIP, never qualified OS |
| MVP-Q152-01 | R3 | Signed **internal** matrix report with image/commit/tools provenance, snapshots/history | Tampered digest/signature, missing snapshot, SKIP misreported as PASS → reject evidence |
| MVP-Q153-01 | R3 | Per-app performance budget, severity/threshold regression gate | Expired/unapproved performance waiver; Q132 tenant/security/recovery disqualifier → absolute veto |
| MVP-Q154-01 | R4 | A only: IPv4; AAAA only: IPv6; A+AAAA: both, with HTTP-01 and HTTPS | Unreachable advertised family, broken port 80/challenge/TLS → FAIL; absent IPv6 is not a blocker |
| MVP-Q155-01 | R4 | Per-server packages/reboot plan, approval, recoverable backup and health check | Unapproved reboot, unverified backup, post-reboot health failure or other server affected → halt/audit/recover |
| MVP-Q156-01 | R4 | Protected recovery-key export, periodic access check, PASS isolated restore of exact backup | Lost key/vault outage, periodic access failure, incomplete isolated restore → not 'recoverable' |
| MVP-Q157-01 | R4 | Authorized site manager registers/revokes **public** SFTP keys per-site with expiry/quota/sensitive approval | Private-key collection, shell, expired grant, cross-site symlink or unapproved sensitive action → deny |
| MVP-Q158-01 | Post-R4 | Beta manual reports + local health, optional minimized separate-consent diagnostics; cohort gate | Consent denied/withdrawn, cohort under threshold, sensitive data or critical health → reject data/pause wave |
| MVP-Q159-01 | Hub R6 | Authorized transfer with correct org/installation, fresh nonce and risk-based second approval | Lost host without review, unusual repetitions, org mismatch or suspected compromise → targeted hold |
| MVP-Q160-01 | Hub R6 | One signed advisory rendered in **human FR and EN** plus **machine-structured format**, targeted notice | Invalid signature, version divergence, wrong recipient or secret payload → deny/escalate |

## Validation rules

**R3**: real KVM VM, verified provenance and signed **internal** report; no qualifying SKIPs or Q132 veto waivers. Q153 exceptions are limited to noncritical performance budgets. **R4**: test every actually advertised A/AAAA family for HTTP-01; approve per-server OS update/reboot with a **demonstrably restorable** backup; grant RECOVERABLE only after periodic key-access validation and a PASS isolated restore; SFTP accepts only scoped **public keys**. **After R4**: beta waves may rely on local health/manual reports without telemetry. **R5 then R6**: neutral extension, then real Hub Q159–Q160 integration tests.

Numeric gates, lifetimes, runners and formats remain open. This matrix is a **test specification**, not executed test evidence.
