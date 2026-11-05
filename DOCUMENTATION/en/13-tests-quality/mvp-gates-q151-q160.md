<!-- forgepanel-doc id=FP-13-Q151-MATRIX revision=1 status=specified -->
# MVP Q151–Q160 tests — qualification matrix

[Français](../../fr/13-tests-quality/mvp-gates-q151-q160.md) · [Decisions](../00-project-control/decisions-q151-q160.md) · [MVP](../00-project-control/mvp-qualification.md)

**All tests are PLANNED, not PASS.** Log commit, OS/version, runner, image/snapshots, tools, PASS/FAIL/SKIP and real evidence; documentation CI is not VM or recovery testing.

| Test ID | Phase | Positive scenario | Mandatory negative case |
|---|---|---|---|
| MVP-Q151-01 | R3 | Real QEMU/KVM VM, snapshot, install/recovery | Container-only or SKIP cannot qualify an OS |
| MVP-Q152-01 | R3 | Signed report, digest, provenance and traceable history | Invalid signature/missing artifact/inconsistent history → reject |
| MVP-Q153-01 | R3 | Noncritical threshold with approved scoped waiver | Expired waiver or critical Q132 veto → FAIL, never PASS |
| MVP-Q154-01 | R4 | A only, AAAA only and A+AAAA: per-published-family HTTP-01/TLS | Broken advertised AAAA or port 80 challenge → fail; absent IPv6 is irrelevant |
| MVP-Q155-01 | R4 | Approved per-server update, proven recoverable backup and health | Unverified backup/failed update/other server affected → halt and audit |
| MVP-Q156-01 | R4 | PASS isolated VM restore with keys and coherent PHP/panel/PG | Skipped/failed restore → recoverable claim prohibited |
| MVP-Q157-01 | R4 | Expiring per-site grants, shell-free SFTP, sensitive approval | Expired access, tenant symlink or unapproved operation → deny |
| MVP-Q158-01 | Post-R4/Hub R6 | Purpose-based consent and thresholded aggregated cohorts | Tiny cohort, withdrawn consent or sensitive payload → suppress |
| MVP-Q159-01 | Hub R6 | Valid transfer and risk-based approvals | Mismatched org/identity, compromise suspicion or nonce replay → targeted hold |
| MVP-Q160-01 | Hub R6 | Signed notice through approved channel | Leaked secret, wrong recipient or invalid signature → reject/escalate |

**R3**: qualified KVM, signed proof, severity policy and Q132 vetoes. **R4**: HTTP-01 on advertised IPs, actually restored isolated backups, approved OS updates and scoped SFTP. **R5**: independent neutral extension without Hub. **Hub R6**: consent, commercial-risk and protected notices. Thresholds, durations and vendors remain OPEN. Static document tests verify this matrix only, not actual execution. [Contracts](../02-architecture/qualification-gates-q151-q160.md).
