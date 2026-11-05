<!-- forgepanel-doc id=FP-00-Q151-160 revision=1 status=specified -->
# Q151–Q160 decisions — qualification, security, recovery and notifications

[Français](../../fr/00-project-control/decisions-q151-q160.md) · [Q141–Q150](decisions-q141-q150.md) · [Architecture](../02-architecture/qualification-gates-q151-q160.md) · [MVP tests](../13-tests-quality/mvp-gates-q151-q160.md)

**Owner-confirmed on 5 November 2026.** Q1–Q150 remain authoritative; no unmentioned option is silently adopted. Every item below is SPECIFIED, not IMPLEMENTED or VERIFIED. Missing details of the referred-to “B” or “A + B” options are not invented.

| ID | Choice | Decision | Boundary and control |
|---|---|---|---|
| Q151 | A | Local QEMU/KVM first, followed by cloud drivers | Q141 D still targets both local+cloud; cloud is a later independently qualified phase. |
| Q152 | C | Option B plus signed reports, provenance, snapshots and result history | Verify report signatures/digests; link run/image/commit/snapshots and maintain auditable PASS/FAIL/SKIP history. |
| Q153 | C | Block by severity/thresholds with approved, audited exceptions | Only scoped, justified, expiring noncritical waivers; Q132 critical security/isolation/recoverability vetoes still disqualify. |
| Q154 | C | Only check actually published IP families, compatible with the challenge | Public A = IPv4; published AAAA = IPv6; both if advertised, port 80/ACME HTTP-01 and TLS; no automatic DNS write Q143. |
| Q155 | C | Per-server OS update policy with approvals, backup, health and recovery | Allowlisted package plans; deny without a proven recoverable prebackup, local approval and recovery procedure. |
| Q156 | C | Option B plus isolated restore before calling a backup recoverable | Check off-host keys, control panel/config, PHP files and consistent PostgreSQL state; backup completion is not restore PASS. |
| Q157 | C | Option B plus expiry, site limits, audit and sensitive approval | Scoped site manager/shell-free SFTP, revocable expiring grants, redacted audit and contextual approval of sensitive actions. |
| Q158 | C | Option B plus minimized diagnostics, separate consents and cohort thresholds | No forced collection; Q6 purpose-specific consent, suppress small groups, exclude unnecessary customer data and secrets. |
| Q159 | C | Option B plus identity/organization mismatch or suspected compromise | Hold/review the affected premium transfer, risk-based Q138 approval and manual verification; never disable free Core. |
| Q160 | C | Combine A + B with configurable notices and protected sensitive data | Q149/Q150 partner alerts/signed advisories: authorized recipients/channels, redaction and protected history, preserving mandatory legal notices. |

## Reconciliation with previous decisions

- **Q141 D ↔ Q151 A**: retain local+cloud goal; start with real local KVM VM evidence, then separately prove cloud drivers.
- **Q132 D ↔ Q153 C**: exceptions are limited to approved, audited noncritical thresholds; critical tenant isolation, security and failed restoration remain FAIL.
- **Q123/Q143 ↔ Q154**: check only actual external public DNS; A without AAAA requires no IPv6, but a broken advertised AAAA fails the challenge.
- **Q135/Q145 ↔ Q156**: backup encryption/key vault alone is insufficient; require successful isolated restoration with keys available after correlated host loss.
- **Q136/Q146 ↔ Q157**: shell-free SFTP and local site-scoped grants/sensitive approvals; no generic privileged shell.
- **Q6/Q147 ↔ Q158**: purpose-separated consent, minimization and small-cohort privacy.
- **Q128/Q138/Q148 ↔ Q159**: review premium transfers for org/identity/compromise, retain risk-based second approval, no free Core shutdown.
- **Q149/Q150 ↔ Q160**: configurable authorized notices and signed, redacted advisories; no invented SLA or channel.

## Sequencing and still-open details

**R3**: Q151–153 and evidence-based OS/WebStack selection. **R4**: Q154–157 and usable PHP/HTTPS/recoverable-backup MVP. **After R4**: consented beta/diagnostics Q147/Q158. **After neutral R5 ABI**: Hub R6 Q159/Q160. Core remains available without Hub.

Still **OPEN**: future cloud runners/provider, signed proof algorithm/key custody/retention, threshold and waiver duration, DNS vantage, update windows, restore cadence, grant lifetimes, cohort minima, risk scoring and notice channels. No numeric defaults are invented.
