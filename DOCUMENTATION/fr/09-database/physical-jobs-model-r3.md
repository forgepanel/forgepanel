<!-- forgepanel-doc id=FP-09-R3-PHYSICAL-JOBS revision=2 status=specified -->
# R3 — Modèle physique PostgreSQL candidat pour les jobs du Core

[English](../../en/09-database/physical-jobs-model-r3.md) · [Database](README.md) · [Jobs logiques](durable-jobs-r3.md) · [IPC/exécution](../08-api-contracts/typed-execution-recovery-r3.md) · [QA](../13-tests-quality/r3-physical-execution-gates.md)

**Autorité : Database / Data Model. Statut : SPECIFIED / CANDIDATE — aucun DDL approuvé, aucune migration exécutée.** Ce modèle concrétise les exigences DB-FP-0001..0012 et IPC-FP-0001..0012 sans les remplacer. Les noms `fp_*`, colonnes, types, index et règles de verrouillage **sont des propositions**, pas des décisions de schéma. SRC-03 Foundation v0.7 reste indisponible (issue #2), Symfony/PG R2 non fonctionnel (issue #3). **DOC-GAP-004 et DOC-GAP-006 restent OPEN.** Q1–Q170 maintenues ; Q171+ et valeurs numériques non approuvées.

## Douze exigences physiques candidates

**DBPH-FP-0001 — Inventaire et séparation des données.** Préserver les trois tables historiques **observées dans SRC-03** (`fp_setup`, `fp_admins`, `fp_setup_audit`) comme références de provenance, pas comme tables appliquées dans le dépôt. Créer de nouveaux objets seulement après comparaison avec l'archive réelle, ADR et revue Database/Security. Le PostgreSQL interne du panneau ne se confond pas avec les bases des clients.

**DBPH-FP-0002 — Périmètre immuable.** Chaque intention référence `scope_kind` (serveur/organisation/compte/site, selon un catalogue **à valider**), `scope_ref`, `resource_kind`, `resource_ref` et `operation_id` du registre fermé. Éviter un `tenant_id` null qui deviendrait implicitement un wildcard ; un scope serveur exige une autorité serveur vérifiée. Les références d'organisation/site devront correspondre à de vraies FK **seulement après** approbation du modèle d'hébergement.

**DBPH-FP-0003 — Admission et idempotence transactionnelle.** Proposition d'unicité `(scope_kind, scope_ref, resource_kind, resource_ref, operation_id, idempotency_fingerprint)` avec `payload_sha256` + `contract_version` et `policy_revision` conservés. Sous transaction : vérifier identité/permission/révision, insérer ou verrouiller l'intention existante ; même clé et même digest → **même job**, même clé et digest différent → `IDEMPOTENCY_CONFLICT`. Ne jamais faire un second APPLY comme effet de `ON CONFLICT`.

**DBPH-FP-0004 — Commit puis ACK.** Insérer atomiquement l'intention autorisée, son état initial `QUEUED`, l'événement de décision et l'entrée d'outbox **avant** tout ACK `ACCEPTED`. Si le commit échoue, ne retourner aucun job admis. Un `DENIED/REJECTED` est une réponse et un audit refusé, **pas** un job `ACCEPTED` fabriqué.

**DBPH-FP-0005 — Journal d'exécution et transitions.** Le job réfère une intention unique ; états `QUEUED/RUNNING/VERIFYING/SUCCEEDED/FAILED/COMPENSATION_REQUIRED/BLOCKED`. Une preuve d'effet observé et de vérification de santé est requise pour `SUCCEEDED`. Ne jamais confondre retour IPC, code de sortie de processus ou service systemd `active` avec cette preuve.

**DBPH-FP-0006 — Bail et fencing monotone.** Une seule génération valide peut posséder un verrou mutateur sur une ressource ; `fencing_generation` croît lors d'un transfert d'autorité. Le validateur **au point d'effet Linux** rejette tout token de génération ancienne ; expiration d'un bail et libération SQL ne prouvent pas qu'un effet antérieur n'est pas en cours. `QUEUED` n'a pas de bail, `RUNNING` doit en posséder un.

**DBPH-FP-0007 — Outbox/inbox contre perte de message.** La livraison peut être `at-least-once` ; dispatcher et agent dédupliquent par référence de message/journal. L'ACK de transport est séparé du statut de job, et la reprise après crash consulte l'effet Linux réellement observé. Le modèle ne promet **aucun exactly-once atomique entre PostgreSQL et Linux**.

**DBPH-FP-0008 — Étapes et points de compensation.** Chaque étape porte identité, ordre, digest de plan, autorisation, démarrage, observation, checkpoint et type de compensation (réversible, incertain, irréversible). Les effets irréversibles ne doivent jamais être masqués par un rollback SQL. Le checkpoint n'est utilisable que si son contenu et ses clés sont disponibles et vérifiés.

**DBPH-FP-0009 — Transactions et concurrence.** Verrouiller les lignes de job/intent et leases dans un **ordre déterministe** ; gérer conflits et deadlocks, isolation et retries selon politique encore non ratifiée. Ne pas tenir de transaction SQL ouverte pendant un appel long à Linux ; préférer transitions courtes, outbox, revalidation après effet et récupération.

**DBPH-FP-0010 — Comptes/permissions DB.** Identités séparées migration DDL, runtime Symfony, lecture d'observation et worker/dispatcher. Le runtime applicatif ne possède pas les tables et ne peut pas faire de DDL. Permissions par vues/requêtes fortement scoppées ; RLS et `FORCE ROW LEVEL SECURITY` peuvent compléter la défense mais **ne remplacent jamais** RBAC et la preuve de tenant ni la validation du contexte de connexion.

**DBPH-FP-0011 — Audit, secrets et rétention.** L'audit est ordonné, append-only logique et corrélé ; ne pas enregistrer plaintext du token d'idempotence s'il peut être sensible, credentials, cookies, jetons, payloads secrets ou contenus clients. Protection contre un effacement non autorisé, archivage et purge par catégorie sous politiques **encore à ratifier**, en maintenant la défense anti-rejeu sur la période promise.

**DBPH-FP-0012 — Migrations/restore.** Planifier migration checksumée, forward-only si rollback SQL dangereux, backups vérifiés, tests de concurrence, récupération de clés et restauration isolée. Un snapshot PostgreSQL restauré peut ressusciter un ancien job/bail : invalider les credentials/grants expirés et **réconcilier l'état observé Linux avant toute reprise**.

## Proposition concrète de tables et contraintes — PAS un fichier SQL

| Objet `fp_*` proposé | Colonnes logiques et types proposés | Contraintes candidates |
|---|---|---|
| `fp_operation_intents` | `intent_id uuid PK`, `scope_kind text`, `scope_ref uuid`, `resource_kind text`, `resource_ref uuid`, `operation_id text`, `actor_ref uuid`, `idempotency_fingerprint bytea`, `payload_sha256 bytea`, `contract_version text`, `policy_revision text`, `expected_revision text`, `created_at timestamptz` | UNIQUE sur scope+ressource+opération+clé; valeurs non nulles ; opération dans registre approuvé, **jamais comme commande** |
| `fp_job_executions` | `job_id uuid PK`, `intent_id uuid FK`, `state text`, `state_revision bigint`, `attempt_count integer`, `observed_effect text`, `updated_at timestamptz` | UNIQUE(`intent_id`), CHECK état et compteur; transition contrôlée; FK |
| `fp_resource_leases` | `scope_kind text`, `scope_ref uuid`, `resource_kind text`, `resource_ref uuid`, `owner_job_id uuid FK`, `fencing_generation bigint`, `expires_at timestamptz`, `resource_revision text` | UNIQUE(scope_kind,scope_ref,resource_kind,resource_ref), fencing monotone; compare-and-swap |
| `fp_job_step_events` | `event_id bigint PK`, `job_id uuid FK`, `step_seq bigint`, `step_ref text`, `transition text`, `effect_verdict text`, `plan_sha256 bytea`, `audit_ref text`, `created_at timestamptz` | UNIQUE(job_id,step_seq) ; append-only logique ; payload secret interdit |
| `fp_agent_outbox` | `message_id uuid PK`, `job_id uuid FK`, `channel text`, `payload_digest bytea`, `delivery_status text`, `attempts integer`, `next_attempt_at timestamptz` | indexes de reprise, déduplication et statut distinct du résultat Linux |
| `fp_agent_inbox` | `consumer_ref text`, `message_id uuid`, `observed_job_id uuid FK`, `receipt_at timestamptz` | UNIQUE(consumer_ref,message_id), résultat du consommateur conservé |
| `fp_recovery_checkpoints` | `checkpoint_id uuid PK`, `job_id uuid FK`, `artifact_digest bytea`, `recovery_class text`, `storage_ref text`, `verified_at timestamptz` | ne stocke aucun secret de restauration brut ; erreur si clés introuvables |
| `fp_job_audit_events` | `audit_id bigint PK`, `job_id uuid FK`, `actor_ref uuid`, `correlation_ref text`, `outcome text`, `created_at timestamptz` | append-only logique ; expurgation + droit de lecture limité |

**Les noms, colonnes, types, FK et index ci-dessus sont UNIQUEMENT candidats.** Aucun `CREATE TABLE`, `ALTER TABLE`, seed, migration `MIG-*`, privilège DB ni API n'est ajouté. Les `uuid` indiqués supposent une future décision cohérente avec le modèle des ressources ; aucune relation inter-table n'est validée sans son schéma propriétaire.

## Admission atomique : algorithme candidat, non exécutable

~~~text
BEGIN;
  authorize actor/tenant/resource on trusted Core context;
  verify operation policy and expected revision;
  INSERT intent ON CONFLICT(scope, resource, operation, key) ...;
  lock the selected intent and compare payload/contract/policy digests;
  if mismatch: ABORT -> IDEMPOTENCY_CONFLICT;
  if existing: return durable original job after COMMIT (no new external side effect);
  else INSERT QUEUED job, decision audit and outbox under same transaction;
COMMIT;
return ACCEPTED(job_ref) only if commit succeeded;
dispatcher and verified Go consumer later perform guarded, fenced steps.
~~~

La requête est un **pseudo-algorithme**, pas une transaction SQL prête à exécuter : la sémantique exacte d'UPSERT, isolation, sérialisation du scope, idempotence, outbox et contraintes doit être éprouvée sur une DB de test après autorité Database.

## Cas de panne, revue et HANDOFF

Requérir des essais PostgreSQL réels sur DB jetable autorisée : deux premiers clients concurrents, requête identique rejouée, payload différent, rollback forcé, perte ACK post-commit, ancien worker après bail, outbox double, partition agent, restore d'une sauvegarde et perte de clé. **Tous les 12 cas `R3-PHYS-TEST-001..012` sont PLANNED**, voir [QA](../13-tests-quality/r3-physical-execution-gates.md). Security doit examiner le fencing à l'effet et RLS/tenants ; API/IPC le protocole de remise ; DevOps les pannes/cleanup ; Database doit valider DDL/permissions, puis produire des migrations **dans une PR séparée** après import SRC-03 et intégration R2. Le modèle PostgreSQL ne constitue jamais une preuve de sécurité Linux.
