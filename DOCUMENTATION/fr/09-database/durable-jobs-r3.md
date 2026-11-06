<!-- forgepanel-doc id=FP-09-R3-DURABLE-JOBS revision=1 status=specified -->
# R3 — Jobs durables, concurrence, idempotence et verrous : contrat candidat

[English](../../en/09-database/durable-jobs-r3.md) · [Database](README.md) · [IPC typé](../08-api-contracts/symfony-go-ipc-r3.md) · [Confiance du pair](../08-api-contracts/local-peer-trust-r3.md) · [Tests R3](../13-tests-quality/r3-jobs-peer-gates.md)

**Propriétaire du modèle de données : Database / Data Model.** Revue obligatoire : API/IPC, Core, Security, DevOps et QA. **Statut SPECIFIED / CANDIDATE, non ratifié.** Les fichiers de preuve sont des **schémas JSON de conception**, pas des migrations PostgreSQL. Aucun changement à l'archive d'origine SRC-03, aucune table ni worker applicatif créé. Dépendances [R1 #2](https://github.com/yyogas/forgepanel/issues/2), [R2 #3](https://github.com/yyogas/forgepanel/issues/3), [Configuration Engine #9](https://github.com/yyogas/forgepanel/issues/9) ; `DOC-GAP-004` et `DOC-GAP-006` demeurent **OPEN**. Q1–Q170 conservées, aucune valeur numérique Q171+ inventée.

## Invariants de la persistance

**DB-FP-0001 — Identité d'une intention.** Enregistrer le périmètre tenant/ressource, type `operation_id` fermé, acteur authentifié, politique, version de contrat, révision visée, digest du payload canonique, `idempotency_key`, `request_id` et `correlation_id`. L'identité tenant doit provenir des données **autorisées côté serveur**, jamais uniquement du payload déclaré.

**DB-FP-0002 — Admission atomique.** Vérifier à nouveau autorisation, révision, absence de conflit et quota **avant** d'insérer durablement intention + décision + audit et une entrée d'outbox transactionnelle si nécessaire. N'accuser réception d'un job asynchrone `ACCEPTED` **qu'après le commit** PostgreSQL réussi. Un ACK n'est jamais une preuve d'effet Linux.

**DB-FP-0003 — Idempotence de scope.** L'unicité candidate lie `tenant_scope + resource_scope + operation_id + idempotency_key` ; mémoriser l'empreinte immuable du payload/version/politique. À clé identique et payload identique, retrouver **le même job** et son état déjà commité ; à clé identique et contenu différent, `IDEMPOTENCY_CONFLICT` sans effet. Une tentative ne doit jamais franchir une autre organisation ou ressource.

**DB-FP-0004 — Verrous ciblés et fencing.** Un job mutateur doit posséder un verrou par ressource/ensemble de ressources, avec propriétaire, génération monotone (`fencing_token` candidat), échéance et révision comparée. **Une expiration de bail ne suffit jamais à autoriser le prochain `APPLY`** : comparer état voulu/observé et vérifier l'effet antérieur. Le consommateur Linux doit rejeter un ancien token malgré le réveil d'un ancien worker.

**DB-FP-0005 — Journal d'étapes.** Conserver l'ID/ordre des étapes, plan signé ou hash de plan, entrée/fin d'étape, tentative, cible, état observé, erreur expurgée, checkpoint et décision de compensation. Changement `QUEUED → RUNNING → VERIFYING → SUCCEEDED` uniquement si l'effet a été observé et validé. Les états d'erreur `FAILED`, `COMPENSATION_REQUIRED` et `BLOCKED` sont distincts et ne doivent pas masquer l'incertitude.

**DB-FP-0006 — Reprise après crash.** Redémarrage du worker : relire job, outbox/inbox et ressources **avant** nouvelle action. Si l'effet externe peut avoir eu lieu et n'est pas prouvé, passer à `COMPENSATION_REQUIRED` / revue, **pas** à un replay silencieux. Les opérations irréversibles requièrent une vérification manuelle ou contrôlée avant suite.

**DB-FP-0007 — Inbox/outbox.** Journaliser l'intention d'envoi dans la même transaction que la transition métier ; livraison `at-least-once` acceptable seulement avec déduplication côté consommateur, et statut de livraison distinct de l'état métier. La panne entre commit/dispatch/ACK ne doit ni perdre le job ni provoquer une deuxième application.

**DB-FP-0008 — Concurrence et ordre.** Autorisation de plusieurs lectures sûres mais sérialisation/compatibilité documentée des modifications concurrentes sur tenant, site, listener, compte Linux, service, paquet et policy. Refuser révision obsolète, verrou non possédé, deadlock non résolu et collision ; les migrations et changements DDL ont une autorité distincte.

**DB-FP-0009 — Audit transactionnel, sans données sensibles.** Événements horodatés et corrélés incluant acteur/autorité/scope/identifiants de plan/étape, version, résultat attendu et observé ; aucune valeur brute de cookie, jeton, clé, credentials DB, données de client ou image de sauvegarde. Un message d'erreur SQL système ne se transmet pas tel quel au navigateur.

**DB-FP-0010 — Annulation et délai.** Une demande `cancel` est une **intention d'arrêt**, pas un effacement transactionnel d'un effet Linux. Si le job a commencé `APPLY`, identifier une frontière sûre/compensable ; timeout, retry, backoff, lease et rétention restent **sans valeur par défaut approuvée**. Un délai expiré ne devient pas `SUCCEEDED`.

**DB-FP-0011 — Migrations et disponibilité.** Prévoir migrations SQL checksumées, rôles séparés DDL/runtime, contraintes d'unicité et FK/tenant, stratégie de backup/restore et tolérance des versions lors d'upgrade. L'échec de migration ne doit pas ouvrir un port administrateur public non sécurisé ni entraîner un `install apply` incontrôlé.

**DB-FP-0012 — Droit à suppression et conservation.** Les rétentions et purges suivent les obligations légales/contrats et ne cassent pas la sécurité de l'idempotence : garder au minimum une protection contre le rejeu adaptée à l'expiration publiée, sans inventer une durée. Purger payloads secrets et métadonnées personnelles sans supprimer prématurément les preuves d'audit exigées.

## Modèle logique candidat — aucune table autorisée

| Entité conceptuelle | Champs à concevoir | Contraintes et propriétaire |
|---|---|---|
| `OperationIntent` | tenant, acteur, opération, ressource, digest, clé idem, révisions, statut | Unicité par scope/opération/clé ; Database + Security |
| `JobExecution` | référence intent, état, tentative, cible, résultat, timestamps | Transitions versionnées ; pas de faux succès |
| `ResourceLease` | ressource, owner, génération, expiry, observed revision | Fencing monotone ; vérifié au niveau agent |
| `JobStepEvent` | étape, preuve, transition, effet observé, error code, corrélation | Journal append-only redigé |
| `DispatchOutbox/Inbox` | message canonique, destination, ack et déduplication | Au moins une livraison, effet métier idempotent |
| `RecoveryCheckpoint` | plan, digest, action compensable, état, retention policy | Aucune garantie de rollback SQL/Linux atomique |

**Aucun nom ci-dessus n'est approuvé comme table `fp_*`**. Le [schéma de job candidat](../../evidence/candidate-job-record-v1.schema.json) donne la forme documentaire du **résultat d'admission** ; le [registre de transitions](../../evidence/candidate-job-transitions-v1.json) décrit les chemins autorisés, pas une machine d'état en production. Des clés étrangères, index et migrations réels ne seront proposés qu'après revue de SRC-03 et validation Database.

## Races à tester

- Deux requêtes simultanées de même clé/digest retrouvent une seule intention et un seul job ; variante même clé/payload différent → `IDEMPOTENCY_CONFLICT`.
- Après commit, la réponse HTTP ou IPC disparaît : un retry lit le job sans second `APPLY`.
- Worker A perd son bail, worker B l'obtient, A revient : A est rejeté par fencing avant tout effet ; B réconcilie l'état observé.
- Crash entre une commande Linux **bornée** et la transition `VERIFYING` : l'état reste incertain et aucune action n'est réappliquée automatiquement.
- Événements/outbox livrés en double, en retard ou dans un ordre différent : aucune élévation et aucun `SUCCEEDED` non observé.
- Restauration du PostgreSQL du panneau ou perte de clé : invalidation des grants anciens, reprise/échec explicite ; aucun journal sensible exporté.

## Dépendances et éléments ouverts

L'autorité **Database** doit proposer puis faire approuver la topologie de tables/contraintes, niveau d'isolation, stratégie SQL/outbox, FK, TTL/retry et rétention. **API/IPC** définit le protocole et l'ordre des ACK ; **Security** autorise le pair, les frontières tenant, secrets, leases et tokens ; **DevOps** formalise les effets observables et les compensations. Les [12 cas `R3-JOB-TEST-001..012`](../13-tests-quality/r3-jobs-peer-gates.md) sont tous **PLANNED**. Aucune DB réelle, agent ou installation n'a été testé dans ce lot. L'absence du Hub ne doit jamais bloquer un job Core indispensable.
