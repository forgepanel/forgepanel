<!-- forgepanel-doc id=FP-02-Q161-170 revision=1 status=specified -->
# Candidate Q161–Q170 technical contracts

[Français](../../fr/02-architecture/evidence-and-recovery-q161-q170.md) · [Decisions](../00-project-control/decisions-q161-q170.md) · [Tests](../13-tests-quality/mvp-gates-q161-q170.md)

**Proposed, not live contracts.** No arbitrary shell API and no Hub system access to tenant servers.

| Candidate contract | Fields and refusal rules |
|---|---|
| EphemeralKvmRun (Q161) | runner_id, image_digest, commit, cpu_ram_io quota, full VM isolation, start/end, cleanup outcome; Q152 evidence persists outside runner; unavailable KVM = BLOCKED/SKIP. |
| SignedEvidenceStore (Q162) | report_id, schema_revision, signing_key_ref, verified_signature, snapshots, history, immutable private object, retention_policy, access_scope and audit; no mandatory second copy. |
| PerformanceException (Q163) | policy_revision, workload, threshold, severity, requester, different approver, scope, expiry, review, revoke and audit; never alter Q132 critical verdict. |
| IndependentDnsProbe (Q164) | domain, actually advertised A/AAAA, HTTP-01 challenge, local_result and external_result, timestamp; allowlisted hosts, SSRF controls, no ACME/customer token. |
| BoundedOsRecovery (Q165) | server_id, allowlisted action, before_checkpoint, max_retry/time, health_result, risk_tier, human_approval for sensitive operations, audit; no generic execution. |
| BackupRestoreEvidence (Q166) | backup_id/digest, recovery key export verification, isolated_restore_id, restored_scope, PASS timestamp, periodic_deep_check, host/key failure_drill; no recoverable flag without each backup's own PASS. |
| SiteSftpKeyPolicy (Q167) | site_id, identity, public_key_fingerprint, possession proof, allowed_algorithm, expiry/revoke/rotation, audit, sensitive approval; never private key or shell. |
| HubPolicyReferences (Q168–Q170) | purpose/version/withdrawal cohort privacy; versioned transfer risk rules, Q138 approval and Q159 signals; signed versioned JSON Schema with synchronized FR/EN. Hub R6 only. |

Only **noncritical performance** thresholds admit exceptions; Q132 security/recovery gates are never waived. External probes restrict destinations (SSRF and misuse). OS remediation is bounded and nondestructive, with approval for risky actions. Every backup revision requires an isolated restore PASS before RECOVERABLE. Premium/notices are deferred candidate Hub contracts, never Linux permissions. [Previous contracts](qualification-and-security-contracts.md).
