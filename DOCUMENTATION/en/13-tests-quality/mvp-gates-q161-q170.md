<!-- forgepanel-doc id=FP-13-Q161-MATRIX revision=1 status=specified -->
# Q161–Q170 MVP test matrix

[Français](../../fr/13-tests-quality/mvp-gates-q161-q170.md) · [Decisions](../00-project-control/decisions-q161-q170.md) · [Previous tests](mvp-gates-q151-q160.md)

**All actual scenarios are PLANNED, not PASS.** Future evidence identifies commit, OS/image, environment, test type, outcomes and redacted logs.

| Test ID | Stage | Expected positive | Required negative |
|---|---|---|---|
| MVP-Q161-01 | R3 | Isolated temporary KVM runner with pinned image, quota, cleanup and preserved evidence | Container-only, leftover secret, unapproved image or cleanup failure: no qualification |
| MVP-Q162-01 | R3 | Signed verified report and retrievable immutable private history | Forged signature, history tampering or unauthorized RBAC access: deny |
| MVP-Q163-01 | R3 | Expiring noncritical performance waiver with separate approver | Self-approval, out-of-scope waiver or Q132 security/restore veto: block |
| MVP-Q164-01 | R4 | Only published A, AAAA or both checked locally and by independent probe for HTTP-01 | No advertised IPv6 = N/A; broken AAAA, unreachable probe or SSRF: no false PASS |
| MVP-Q165-01 | R4 | Nondestructive recovery with checkpoint, retry bounds and health check | Infinite retry, arbitrary shell or risky action without approval: deny |
| MVP-Q166-01 | R4 | Every backup fully restored in isolation before RECOVERABLE, host/key drills scheduled | Partial/skipped isolated restore or missing key: not recoverable |
| MVP-Q167-01 | R4 | Public SFTP key possession, allowed algorithm, site scope, expiry, rotation and audit | Private key, forbidden algorithm, revoked key or cross-site escape: deny |
| MVP-Q168-01 | Post-R4 beta | Per-purpose consent and sufficient cohort, aggregated redacted report | Withdrawn consent, reidentifiable cohort or secret: no upload |
| MVP-Q169-01 | Hub R6 | Low-risk transfer under versioned rule, manual review for high risk | Replayed nonce, wrong org, lost host or suspected compromise: hold only transfer |
| MVP-Q170-01 | Hub R6 | Signed schema-valid JSON advisory in sync with FR/EN, filtered notices | Invalid schema, missing signature, FR/EN divergence or data leak: reject |

**Exit gates**: R3 actual signed KVM proof with no critical Q132 waiver; R4 local/external DNS, bounded OS remediation, isolated restoration of **every backup** and scoped public-key SFTP. Post-R4 consented beta; Hub R6 after R5 for transfers and signed JSON FR/EN. SKIP, signature alone or documentation CI never certify behavior.
