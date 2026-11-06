<!-- forgepanel-doc id=FP-08-R3-TYPED-EXECUTION revision=2 status=specified -->
# R3 — Exécution typée, observation d'effets et contrat de récupération

[English](../../en/08-api-contracts/typed-execution-recovery-r3.md) · [API / IPC](README.md) · [Registre d'actions](../../evidence/typed-agent-operations-v1.json) · [Jobs PostgreSQL](../09-database/physical-jobs-model-r3.md) · [Comptes Linux](../14-devops-releases/linux-service-identities-r3.md) · [QA](../13-tests-quality/r3-physical-execution-gates.md)

**Autorité : API / IPC / Contracts avec Security, Database, DevOps et QA. État : SPECIFIED / CANDIDATE.** Aucun exécuteur, socket Unix, endpoint HTTP, binaire privilégié, commande Linux ou changement système n'est produit ici. Les contrats sont **des modèles de validation**, pas une permission de root. `EXEC-FP-0001..0012` complètent IPC-FP-0001..0012 et INST-FP-0001..0012 sans modifier Q1–Q170. `DOC-GAP-005/006` restent **OPEN** ; R1 source et R2 runtime non intégrés.

## Douze règles d'exécution candidates

**EXEC-FP-0001 — Registre fermé et typage.** Seul un `operation_id` explicitement déclaré et approuvé dans [ACT-FP-0001..0007](../../evidence/typed-agent-operations-v1.json) peut être évalué. Un payload valide est **nécessaire mais insuffisant**. Aucune option `command`, `argv`, `script_path`, `shell`, `raw_args`, interpréteur ou exécutables téléchargés ; les handlers sont codés par opération, sans résoudre dynamiquement un nom vers un processus Linux.

**EXEC-FP-0002 — Identité/permission à l'effet.** Le pont transmet une identité acteur authentifiée et un mandat borné à une ressource, une opération, un plan et une révision. Go valide **indépendamment** le pair Unix, la portée tenant/ressource et le droit actuel de la mutation. Un formulaire Expert, rôle administrateur Symfony ou licence du Hub ne peut pas supplanter ce contrôle.

**EXEC-FP-0003 — Digest et version d'un plan figé.** L'opération est liée à un `plan_digest` calculé sur représentation canonique versionnée et à la preuve de l'origine des artefacts, cible et autorisation ; vérifier le digest/signature/approbation à l'admission **et au point d'effet**. Un plan modifié, expiré ou fondé sur une version obsolète est refusé, pas réutilisé.

**EXEC-FP-0004 — Autorité système minimale.** Un composant privilégié éventuel doit être un handler au droit précisément déclaré (paquet signé, service nommé, génération vérifiée), jamais un exécuteur root générique. Tant qu'aucune implémentation et qualification n'a validé ce confinement, **ACT-FP-0005 et ACT-FP-0007 = `BLOCKED_UNTIL_QUALIFIED`**.

**EXEC-FP-0005 — Fencing lié à la ressource.** Chaque effet mutateur vérifie `resource_ref`, appartenance, révision observée, propriétaire/lease et génération monotone **au moment exact de la modification**. Un vieux worker ne peut pas continuer après prise de bail par un nouveau worker. Si l'OS/handler ne peut garantir l'absence d'effet concurrent sur la même cible, **`BLOCKED`**, pas mise en production.

**EXEC-FP-0006 — PREPARE/PREFLIGHT sans effet.** L'opérateur doit voir l'impact, les dépendances, droits/permissions, fichiers non gérés, collisions listener et provenance des paquets. Les contrôles de lecture n'autorisent pas APPLY. `STAGE` crée au maximum un dossier privé borné et vérifié, jamais une activation automatique ni une installation non signée.

**EXEC-FP-0007 — APPLY conditionnel et preuves.** Avant APPLY sensible : autorisation récente, Q47 PLAN/PREFLIGHT/SNAPSHOT, sauvegarde vérifiée quand requise, preuve de chaîne signée et plans non expirés, autorité locale/tenant, verrou actuel. Le handler doit déclarer effets voulus/observés sans secret et produire un identifiant d'étape durable. Un ACK IPC ou un code retour zéro n'est **pas** une preuve suffisante de succès.

**EXEC-FP-0008 — VERIFY fonctionnel avant SUCCESS.** Vérifier l'effet métier et la santé du service réel (vhost, TLS/HTTP, login du panneau, connexion DB, plan exact selon opération), y compris refus cross-tenant et conservation du dernier accès administrateur. `SUCCEEDED` est interdit tant que `VERIFYING` ou la preuve d'effet validée sont absents.

**EXEC-FP-0009 — Crash, perte d'ACK et état inconnu.** Si un job a pu modifier Linux avant perte de réponse/timeout/restart, **ne jamais rejouer aveuglément**. Lire état durable PG + observation OS, distinguer effet absent, effectué, partiel et inconnu. Si inconnu : `COMPENSATION_REQUIRED` ou état de blocage avec récupération contrôlée ; les deadlines/retries attendent une politique ratifiée.

**EXEC-FP-0010 — Compensation et irréversibilité.** Compensations **uniquement** des étapes réellement réversibles et dont le checkpoint est accessible et intègre ; une migration SQL, une clé perdue ou un package/service non géré ne sont pas remis en état par un simple rollback du binaire. Les opérations irréversibles sont signalées avant approbation et la récupération peut nécessiter une action humaine indépendante.

**EXEC-FP-0011 — Audit et protection des secrets.** Journaliser plan/version/commit, acteur/tenant/ressource pseudonymisés, pair authentifié, décision, checkpoint, fencing, observation de santé et corrélation, sans secrets bruts ni données client. Les droits de visualiser/exporter les preuves sont distincts de l'autorité d'exécution ; signé Q152 et stockage privé Q162 restent **non implémentés**.

**EXEC-FP-0012 — Compatibilité et délégation.** Un handler ne s'active que pour un OS, un profil WebStack, une version de contrat et un jeu de dépendances testés précisément sur VM. Incompatibilité ou perte de Hub => aucune élévation ; le Core libre doit continuer localement, ou bloquer **l'opération particulière** si son propre prérequis manque. Les mises à jour de schéma/contract doivent préserver idempotence et récupération sans contourner Q132.

## Contrats par opération existante — tous documentaires

| ID | Fonction candidate | Effet/condition de preuve | Autorité aujourd'hui |
|---|---|---|---|
| `ACT-FP-0001` | `host.capabilities.observe` | Lecture de faits bornée ; résultat d'observation, **pas** support OS certifié | CANDIDATE, aucun service branché |
| `ACT-FP-0002` | `artifact.signature.verify` | Racine de confiance indépendante + signature + **octets** de l'artefact ; échec = `TRUST_FAILURE` | CANDIDATE, aucun trust store d'éditeur actif |
| `ACT-FP-0003` | `installer.plan.compile` | Diff sans effet + provenance, identités et révisions | CANDIDATE, plan non appliqué |
| `ACT-FP-0004` | `installer.stage_verified_packages` | Copie privée bornée, digest exact, sans service actif modifié | CANDIDATE, aucun installateur intégré |
| `ACT-FP-0005` | `installer.activate_signed_generation` | **FUTUR privilégié** : plan/signatures/checkpoint/lease/fencing/approbations/VM qualifiée | **BLOCKED_UNTIL_QUALIFIED** |
| `ACT-FP-0006` | `installer.health.check` | Preuves health scoped service/PG/panneau, pas seulement `active` | CANDIDATE, aucun endpoint |
| `ACT-FP-0007` | `installer.compensate_generation` | **FUTUR privilégié** : compensation bornée, checkpoint, autorité nouvelle et audit | **BLOCKED_UNTIL_QUALIFIED** |

Le [registre d'exécution candidat](../../evidence/candidate-typed-execution-guards-v1.json) décrit pour chaque action le type d'effet et les veto. **Il n'est ni une table d'actions exécutable, ni une politique root signée.** Aucune opération nouvellement inventée ne peut être ajoutée dans ce lot à l'API publique ou à Go.

## Machine d'état et observations distinctes

~~~text
INTENT committed in PostgreSQL (admission ACCEPTED ≠ Linux applied)
      → QUEUED (no resource lease)
      → RUNNING (verified lease + fencing at effect boundary)
      → VERIFYING (record actual observed effect, then functional health)
      → SUCCEEDED (only after verified observation and durable audit)
               or FAILED (proven no effect)
               or COMPENSATION_REQUIRED (partial/uncertain effect)
               or BLOCKED (authorization/trust/revision veto)
~~~

Une transition doit garder `request_id`, `job_ref`, `step_ref`, `correlation_id`, `policy_revision` et le digest du plan de façon durable et expurgée. Si le handler ne sait pas classer un effet, il **ne peut pas** convertir `UNKNOWN` en `SUCCEEDED`. Un ancien `lease` expiré ne redonne aucune autorité.

## Erreurs, revue et tests ouverts

| Échec | Réponse candidate | Compensation/reprise |
|---|---|---|
| Pair non authentifié, acteur hors tenant, opération inconnue | `UNAUTHENTICATED/FORBIDDEN/SCOPE_DENIED/INVALID_INPUT` | Aucun job mutateur/effet |
| Plan/signature non fiable ou version périmée | `TRUST_FAILURE/STALE_REVISION` | Arrêt avant APPLY |
| Clé idempotente utilisée avec un autre digest | `IDEMPOTENCY_CONFLICT` | Lire le job existant sans mutation |
| Bail ancien, verrou occupé, ressource non gérée | `RESOURCE_LOCKED` ou `BLOCKED` | Réconcilier et demander un nouveau plan |
| Timeout/crash après effet possible | `PARTIAL_FAILURE/RECOVERY_REQUIRED` | Lire PG et OS, compensation séparée |
| Health échoue malgré service `active` | `RECOVERY_REQUIRED` | Restaurer uniquement effets réversibles prouvés |
| DDL irréversible ou clé de sauvegarde manquante | `RECOVERY_REQUIRED` | Intervention humaine, pas de faux rollback |

[Les 12 tests `R3-EXEC-TEST-001..012`](../13-tests-quality/r3-physical-execution-gates.md) restent **PLANNED**. API/IPC doit ratifier format/auth/erreurs, Database les jobs durables, Security les droits/fencing/root, DevOps les handlers et compatibilité OS, QA les effets réels en VMs. R1/R2 préalables, aucune commande système lancée par cette documentation.

## Revue R3 — aucun fencing garanti après restauration

La [revue ciblée des jobs](../19-audits-risks/r3-job-integrity-audit.md) identifie **RISK-033..036**, notamment une génération de fencing susceptible d'être réutilisée après restauration PostgreSQL, une inbox pouvant cacher un effet Linux incertain et un scope tenant non authentifié. Les [garde-fous candidats](../../evidence/candidate-typed-execution-guards-v1.json) indiquent explicitement `post_restore_privileged_apply_authorized=false` et `effect_boundary_fence_epoch_reconciliation_approved=false`. **Il s'agit de flags documentaires, pas d'une protection du handler**. Maintenir les opérations `ACT-FP-0005/0007` bloquées jusqu'à un design de l'époque indépendante et des tests d'effets réels. Les [8 nouveaux tests négatifs](../19-audits-risks/r3-job-integrity-audit.md) restent PLANNED.
