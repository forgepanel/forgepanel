<!-- forgepanel-doc id=FP-02-Q151-GATES revision=1 status=specified -->
# Contrats candidats et portes de contrôle Q151–Q160

[English](../../en/02-architecture/qualification-gates-q151-q160.md) · [Décisions](../00-project-control/decisions-q151-q160.md) · [Tests](../13-tests-quality/mvp-gates-q151-q160.md)

Ces objets sont des **contrats proposés**, pas des APIs installées. Le runner CI produit des preuves ; le Core décide localement. Le Hub ne reçoit ni root, ni clés des sauvegardes clientes, ni commande shell arbitraire.

| Contrat proposé | Invariants techniques |
|---|---|
| VmQualificationRun (Q151/152) | run_id, driver=local-kvm/cloud-later, os/version/arch, webstack, commit/image digest, snapshot before/after, fault plan, PASS/FAIL/SKIP, artifacts, signing key/version, report signature, result history ; vérifier signature/provenance. |
| QualificationGateDecision (Q153) | policy/version, severity, threshold, FAIL/BLOCK/PASS, exception approver/scope/expiry/audit ; ne jamais autoriser une dérogation aux veto critiques Q132. |
| PublishedAddressCheck (Q154) | A/AAAA observés, famille publiée, cible, port 80/HTTP-01, 443/TLS, timestamp, résultat ; non publiée=NOT_APPLICABLE, publiée défaillante=FAIL ; pas d'écriture DNS. |
| ServerUpdatePlan (Q155) | server_id, packages/dépôts allowlistés, approbation, backup déclaré récupérable après test, fenêtre, health check, recovery path ; jamais shell.exec. |
| BackupRecoveryEvidence (Q156) | backup_id/digest, état des clés off-host, isolated_restore_run_id, preuve panneau/PG/fichiers PHP, PASS horodaté ; recoverable=true seulement après succès sur backup exact. |
| SiteDelegationPolicy (Q157) | identity/site_ids/permissions, expiry/revocation, SFTP sans shell/chroot canonique, quota, approbation action sensible, audit sans secrets. |
| DiagnosticConsentAndCohort (Q158) | consentement distinct par finalité, date/version/retrait, champs minimisés, rétention, cohort_id/seuil configurable, suppression petite cohorte. |
| SensitiveTransferReview/SecurityNotice (Q159/160) | vérification identité/org et indice de compromission, gel action premium, deuxième approbation selon risque, audit ; avis signé, destinataires/canaux autorisés, redaction. |

La qualification exige **VM système réelle et preuve signée** ; un SKIP n'est jamais PASS. Les exceptions non critiques expirent et sont auditables ; les veto de sécurité Q132 restent non contournables. La restauration isolée conditionne le statut récupérable. Les mises à jour et les délégations appartiennent au Core local. Les diagnostics et notifications Hub sont différés après R5, consentis et minimisés. Toutes les valeurs de seuil sont à arbitrer.
