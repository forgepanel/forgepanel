<!-- forgepanel-doc id=FP-02-Q161-170 revision=1 status=specified -->
# Contrats techniques candidats Q161–Q170

[English](../../en/02-architecture/evidence-and-recovery-q161-q170.md) · [Décisions](../00-project-control/decisions-q161-q170.md) · [Tests](../13-tests-quality/mvp-gates-q161-q170.md)

**Contrats proposés, non exécutables aujourd'hui.** Aucune API shell arbitraire et aucun accès système Hub aux serveurs clients.

| Contrat candidat | Données et conditions de refus |
|---|---|
| EphemeralKvmRun (Q161) | runner_id, image_digest, commit, quota_cpu_ram_io, VM isolation, start/end, cleanup result ; conserver preuve Q152 en dehors du runner ; KVM indisponible = BLOCKED/SKIP. |
| SignedEvidenceStore (Q162) | report_id, schema_revision, signing_key_ref, verified_signature, snapshots, history, immutable private object, retention_policy, access_scope et audit ; pas de seconde copie obligatoire. |
| PerformanceException (Q163) | policy_revision, workload, threshold, severity, requester, different approver, scope, expiry, review, revoke, audit ; ne jamais modifier verdict critique Q132. |
| IndependentDnsProbe (Q164) | domain, A/AAAA réellement publiés, challenge HTTP-01, local_result et external_result, timestamp ; hôtes autorisés, garde-fous anti-SSRF, aucun token ACME/client. |
| BoundedOsRecovery (Q165) | server_id, action allowlistée, before_checkpoint, max_retry/time, health_result, risk_tier, human_approval pour actions sensibles, audit ; pas d'exec générique. |
| BackupRestoreEvidence (Q166) | backup_id/digest, key_export_verification, isolated_restore_id, restored_scope, PASS et date, periodic_deep_check, host/key failure_drill ; recoverable interdit sans PASS sur chaque backup exact. |
| SiteSftpKeyPolicy (Q167) | site_id, identity, public_key_fingerprint, possession proof, allowed_algorithm, expiry/revoke/rotation, audit, sensitive approval ; jamais clé privée ou shell. |
| HubPolicyReferences (Q168–Q170) | purpose/version/withdrawal cohort privacy ; versioned risk rules for transfer, Q138 approval and Q159 triggers ; signed versioned JSON Schema with FR/EN synchronized payloads. Hub R6 uniquement. |

Les seules dérogations possibles concernent les seuils de **performance non critiques**, jamais les garanties de sécurité et de récupérabilité Q132. Une sonde externe est limitée à des domaines approuvés (risques SSRF et abus). Les réparations OS sont bornées et non destructives ; actes risqués sous approbation humaine. Le backup de chaque version doit réussir la restauration isolée avant l'état RECOVERABLE. Les politiques premium/notifications sont candidates et différées après R5, non des permissions Linux. [Contrats précédents](qualification-and-security-contracts.md).
