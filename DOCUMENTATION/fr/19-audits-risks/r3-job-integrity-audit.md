<!-- forgepanel-doc id=FP-19-R3-JOB-INTEGRITY-AUDIT revision=1 status=specified -->
# Revue ciblée R3 — Idempotence, restauration et isolation des jobs

[English](../../en/19-audits-risks/r3-job-integrity-audit.md) · [Risques](README.md) · [Modèle physique](../09-database/physical-jobs-model-r3.md) · [Jobs durables](../09-database/durable-jobs-r3.md) · [QA R3](../13-tests-quality/r3-physical-execution-gates.md)

**Nature : revue technique interne ciblée du modèle documentaire R3, non audit indépendant de sécurité.** Baseline examinée : Core `develop` au commit `0af257ce362e01f5ef590d05b01a376d9e36cee8`, PR #48, schéma `candidate-r3-physical-data-model-v1.json`, modèle d'exécution `candidate-job-transitions-v1.json`. Aucun système Linux, socket Go, PostgreSQL ou logiciel Foundation n'a été exécuté dans cette revue. **Verdict : quatre constats OPEN ; modèle non approuvé pour migrations ou effets privilégiés.** Q1–Q170 inchangées, MFA admin facultative, Core autonome sans Hub, R1 toujours bloqué par SRC-03 absent.

## AUDIT-FP-0033 / RISK-033 — Audit d'admission refusée sans job

**Severity : HIGH. Status : OPEN.** Scope : Database / API / Observability. **Constat :** le contrat exige un audit pour `DENIED/REJECTED` **sans** création de job admis, alors que la table candidate `fp_job_audit_events` ne décrivait qu'un `job_id uuid FK`, sans distinguer les admissions refusées. Une implémentation pourrait perdre l'audit de refus, forcer un faux job `ACCEPTED`, ou inventer une valeur de FK.

**Preuve :** [modèle physique](../09-database/physical-jobs-model-r3.md), `DBPH-FP-0004/0011` ; [contrats d'admission](../08-api-contracts/symfony-go-ipc-r3.md) ; [schéma de job admis](../../evidence/candidate-job-record-v1.schema.json).

**Recommandation et changement requis :** définir un sujet d'audit indépendant de l'existence d'un job. La **proposition** ajoute `request_ref`, `subject_kind`, `decision_code` et rend `job_id` **candidat nullable uniquement si le sujet est refus/rejet** ; un événement lié à un job accepté requiert une vraie référence. Exiger une règle conditionnelle DB/contrat, corrélation sûre, absence de secret, résistance aux événements reçus deux fois et une rétention ratifiée. **Aucun DDL approuvé.**

**Owner : Database / API / Observability / Security. Tests requis : `R3-AUDIT-TEST-001/002`.**

## AUDIT-FP-0034 / RISK-034 — Fencing réinitialisé après suppression/restauration SQL

**Severity : CRITICAL pour l'activation privilégiée, HIGH pour documentation non exécutée. Status : OPEN.** Scope : Database / Security / DevOps. **Constat :** `fencing_generation bigint` dans la ligne courante du bail est insuffisant à lui seul : si la ligne est supprimée/recréée ou si PostgreSQL est restauré vers une ancienne sauvegarde, une génération anciennement émise peut être réutilisée. Un worker suspendu pourrait alors revenir et produire un effet Linux avec un jeton obsolète.

**Preuve :** modèle `fp_resource_leases` avec unicité du scope et génération ; `DBPH-FP-0006/0012` ; [contrat d'exécution](../08-api-contracts/typed-execution-recovery-r3.md), `EXEC-FP-0005` ; [RISK-028](README.md).

**Recommandation et changement requis :** garantir un **high-water mark monotone persistant** pour chaque ressource et interdire sa réinitialisation sur suppression/recréation. Définir une **époque de récupération indépendante** capable d'invalider toutes les capacités pré-restauration, contrôlée **au point d'effet** et pas uniquement dans PostgreSQL restauré. Le champ candidat `fencing_epoch_ref` est un **placeholder non sécurisé**, **pas** un mécanisme approuvé ou implémenté. Tant que la stratégie d'époque, de synchronisation et de crash n'est pas démontrée, **refuser ACT-FP-0005/0007** et toute reprise `APPLY`.

**Owner : Database / Security / DevOps / API. Tests requis : `R3-AUDIT-TEST-003/004`.**

## AUDIT-FP-0035 / RISK-035 — Déduplication de message confondue avec l'effet Linux

**Severity : HIGH. Status : OPEN.** Scope : Database / IPC / Engineering / SRE. **Constat :** une ligne de `fp_agent_inbox` prouve au mieux qu'un message a été reçu. Si elle est écrite **avant** l'effet puis qu'un crash survient, un consommateur pourrait ignorer un effet jamais réalisé. Si elle est écrite **après** l'effet puis que l'ACK disparaît, il pourrait exécuter deux fois. Une contrainte `UNIQUE(consumer_ref,message_id)` ne garantit pas le « exactly once » des effets externes.

**Preuve :** `fp_agent_outbox/inbox`, `DBPH-FP-0007`, [modèle des transitions](../../evidence/candidate-job-transitions-v1.json).

**Recommandation et changement requis :** proposer des états distincts `RECEIVED`, `IN_PROGRESS`, `EFFECT_UNCERTAIN`, `EFFECT_VERIFIED`, `PROVEN_NO_EFFECT` et une référence de verdict **observé indépendamment**. Tout message rejoué pendant une incertitude est réconcilié avec l'état Linux, sous autorisation courante/fencing, **sans réappliquer automatiquement**. Les noms/colonnes restent candidats et exigent machine d'états DB et tests de crash réels.

**Owner : Database / API-IPC / SRE / Security. Tests requis : `R3-AUDIT-TEST-005/006`.**

## AUDIT-FP-0036 / RISK-036 — Source de vérité des scopes et contexte SQL

**Severity : HIGH. Status : OPEN.** Scope : Database / Security / Core. **Constat :** le modèle admet plusieurs valeurs futures de `scope_kind` et `scope_ref uuid`, sans entités/fk réelles. Une valeur NULL ou un scope forgé dans le JSON, ou un contexte SQL configurable par un même runtime non isolé (session GUC sans preuve), pourrait mélanger les jobs de tenants distincts. RLS seul n'authentifie pas l'acteur.

**Preuve :** `DBPH-FP-0002/0003/0010`, [modèle physique](../09-database/physical-jobs-model-r3.md), [confiance IPC](../08-api-contracts/local-peer-trust-r3.md), [RISK-030](README.md).

**Recommandation et changement requis :** choisir le catalogue de scopes et les FK via le propriétaire du modèle d'hébergement ; imposer des références non nulles, une identité **liée à la session Core authentifiée côté serveur** et des contraintes composites tenant/ressource. Les opérations serveur demandent une autorité serveur distincte, jamais un tenant vide/wildcard. Évaluer RLS comme défense additionnelle avec tests de spoofing de contexte SQL.

**Owner : Database / Security / Core. Tests requis : `R3-AUDIT-TEST-007/008`.**

## Registre des huit contre-tests obligatoires

| ID | Refus ou événement à reproduire | État |
|---|---|---|
| `R3-AUDIT-TEST-001` | Refus d'admission journalisé sans job fictif ; référence de requête durable | **PLANNED** |
| `R3-AUDIT-TEST-002` | Événement accepté sans vrai job, audit sans scope ou contenu secret refusés | **PLANNED** |
| `R3-AUDIT-TEST-003` | Bail supprimé puis recréé : ancienne génération **ne doit pas** redevenir valide | **PLANNED** |
| `R3-AUDIT-TEST-004` | Restaurer une vieille DB et réveiller un ancien worker : aucun `APPLY` | **PLANNED** |
| `R3-AUDIT-TEST-005` | Crash après réception de message et avant effet : pas de faux effet vérifié | **PLANNED** |
| `R3-AUDIT-TEST-006` | Crash après effet et avant ACK : déduplication et réconciliation sans nouvel APPLY | **PLANNED** |
| `R3-AUDIT-TEST-007` | Scope NULL ou forged tenant dans payload/SQL context → refus cross-tenant | **PLANNED** |
| `R3-AUDIT-TEST-008` | Tentative de scope serveur via rôle tenant ou RLS forgé → refus | **PLANNED** |

Les huit scénarios ci-dessus sont **des exigences de futurs tests d'intégration**, distinctes des tests Python statiques de cohérence JSON. **Aucun test fonctionnel exécuté.** Enregistrer pour tout PASS futur : commit, migration, OS/PG, acteur/scope, requête, état SQL, état Linux avant/après, tentative, génération/époque, erreur, audit sans secret et preuve de compensation. Utiliser `SKIP/BLOCKED` si un environnement réel n'est pas disponible.

## Décision de revue et HANDOFF

- **Verdict : REVIEW REQUIRED / OPEN.** Le document propose quatre corrections de **spécification**. Il ne valide pas la conformité, n'autorise pas un `CREATE TABLE` et ne ferme aucun risque.
- **Database :** choix d'audit des refus, FK scopes, génération monotone hors reset, inbox/outbox et migrations réelles.
- **Security :** preuve de mandat, rejeu, fencing post-restore, RLS et droits au point d'effet.
- **API/IPC :** ACK distinct du résultat Linux, idempotence, états de reprise et erreurs typées.
- **DevOps/QA :** crash/restore/worker concurrents sur OS VM et PG test autorisé, vérification de l'absence d'effet privilégié.
- **MASTER :** arbitrer les contradictions ; aucune adoption automatique de schéma physique. `DOC-GAP-004/005/006` restent OPEN, [source SRC-03 #2](https://github.com/yyogas/forgepanel/issues/2) toujours bloquante.
