<!-- forgepanel-doc id=FP-00-Q161-170 revision=1 status=specified -->
# Q161–Q170 decisions — qualification, recovery and privacy

[Français](../../fr/00-project-control/decisions-q161-q170.md) · [Q151–Q160](decisions-q151-q160.md) · [Architecture](../02-architecture/evidence-and-recovery-q161-q170.md) · [Tests](../13-tests-quality/mvp-gates-q161-q170.md)

**Owner-approved 5 November 2026. Q1–Q160 are retained; unanswered questions remain open.** SPECIFIED, not IMPLEMENTED or VERIFIED.

| ID | Choice | Decision | Scope and security |
|---|---|---|---|
| Q161 | C | Isolated ephemeral local KVM runners with pinned images, quotas and automated cleanup | Q151 local before cloud. Verify KVM capabilities, pinned image/commit hashes, resources and secret cleanup; keep signed evidence outside ephemeral runner. |
| Q162 | B | Private immutable storage for signed reports with history, retention and access control | Q152 internal evidence: verify signatures, provenance, snapshots, versions, history and RBAC; option C independent replica is NOT selected. |
| Q163 | C | Severity-based performance waiver approval with separation, scope, expiry and periodic review | Only noncritical Q153/Q142 performance budgets: separate requester/approver according to policy, revoke and audit. Q132 security, isolation and recovery vetoes cannot be waived. |
| Q164 | B | Local DNS check plus one independent external probe | Q154: verify only actually published A/AAAA on port 80/HTTP-01 and HTTPS. External probe must be authorized, bounded and SSRF-safe; option C multiple probe networks not adopted. |
| Q165 | C | Bounded nondestructive repair with checkpoints and human approval for risky actions | Q155: explicit allowlisted system operations, capped retries/timeouts and health/audit; no arbitrary root shell or destructive rollback without approval. |
| Q166 | C | Isolated restore for each backup, deeper periodic functional tests and severity-based outage drills | Q156: recoverable status only after PASS isolated full-scope restore and accessible protected recovery key; host/key/outage drills cannot destroy real recovery secrets. |
| Q167 | C | SFTP public-key verification, expiry, rotation, allowed algorithms, audit and sensitive-action checks | Q157/Q146: site-manager scope, possession proof, quotas, canonical isolation, revocation and action approval; no tenant private key or shell. |
| Q168 | C | Separate consents, per-data/cohort thresholds, aggregation, redaction and anti-reidentification | Q158/Q6: telemetry never forced. Configurable data/cohort minimums and protection against differencing; local health/manual reports work without Hub. |
| Q169 | C | Versioned risk policy with low-risk automated premium transfer, additional approval and safe recovery | Q159/Q138/Q148: verify org/rights/fresh nonce before automation; suspicious repetition, lost source, mismatch or compromise triggers manual review and target-transfer hold only. No arbitrary per-product Q159 D engine. |
| Q170 | B | Signed validated versioned JSON Schema for advisory with synchronized FR/EN and history | Q160/Q150: single canonical source for structured and human versions, authorized recipients, configurable notices and protected sensitive fields; no mandatory advanced interchange option C. |

## Dependencies and limits

**R3**: Q161–Q163 = local KVM, immutable private signed reports and **noncritical performance** exceptions only. Q132 critical disqualifiers remain. **R4**: Q164–Q167 = independent external plus local probe of published IP families, bounded nondestructive recovery, isolated restoration of **every** backup before recoverable status, secure public SFTP keys. **Post-R4**: Q168 consented cohort diagnostics without forced telemetry. **After neutral R5 API**: Q169–Q170 belong to Hub R6 (premium fraud and signed FR/EN JSON advisories); free Core independent.

## Still OPEN

KVM runner sizing/quotas, storage/signing/retention, performance thresholds and approval details, independent probe selection, retry caps, deep-test/drill schedule, SFTP algorithm policy, cohort statistical minima, license risk scores, final JSON Schema and advisory channels. **No invented threshold, vendor or delivery date.**
