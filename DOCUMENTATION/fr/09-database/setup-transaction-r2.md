<!-- forgepanel-doc id=FP-09-TRANSACTION-R2 revision=1 status=specified -->
# R2 — Contrat candidat PostgreSQL : bootstrap, concurrence et récupération

[English](../../en/09-database/setup-transaction-r2.md) · [Database](README.md) · [Identité R2](../03-core/bootstrap-identity-r2.md) · [Tests R2](../13-tests-quality/r2-integration-gates.md)

**Autorité :** Database / Data Model avec Core, Security, API/IPC. **SPECIFIED — CANDIDATE** : aucun nouveau schéma SQL, aucune migration ni table n'est créé. Le code Foundation v0.7 SRC-03 est absent de `develop` (issue #2) ; les observations suivantes viennent de l'inventaire déjà documenté, **pas d'une base PostgreSQL exécutée**. Identifiants `R2-DB-001` à `R2-DB-012`.

## Inventaire observé, sans fiction

Le fichier historique `apps/panel/migrations/001_setup.sql` définit **trois tables uniquement** : `fp_setup` (singleton, JSONB état/révision/jeton), `fp_admins` (UUID, email unique, hash, rôle, MFA et état d'activation) et `fp_setup_audit` (événements horodatés). L'index partiel `initial_admin=true` impose un administrateur initial unique ; le dépôt PDO du prototype verrouille `fp_setup` avec `SELECT … FOR UPDATE`. **Ce schéma n'existe actuellement pas comme migration appliquée dans le dépôt Core.** Un modèle d'hébergement multi-tenant n'est ni implanté ni défini jusqu'aux contraintes finales.

## Propriétés transactionnelles requises

| ID | Règle candidate | Preuve et cas de refus |
|---|---|---|
| R2-DB-001 | Migrations **versionnées et ordonnées**, checksum, auteur, statut et dépendance, rôle DDL distinct du runtime | Installation vierge, reprise, migration altérée, double exécution concurrente |
| R2-DB-002 | Un seul `fp_setup` singleton avec vérificateurs cryptographiques et révision monotone | Création parallèle, corruption JSONB, version obsolète |
| R2-DB-003 | Un seul administrateur initial actif selon contrainte unique DB ; emails normalisés et comptes durables | Deux requêtes concurrentes, doublon d'email, conflit de rôle |
| R2-DB-004 | Échange bootstrap : mise à jour jeton/tentatives/grant/état **dans la même transaction**, sous verrou précis | Jeton rejoué, compteurs perdus, abandon transactionnel |
| R2-DB-005 | Événement d'audit critique et résultat métier commités ensemble quand sémantiquement atomiques | Crash entre mutation et audit, audit sans succès fictif |
| R2-DB-006 | Révision (optimistic concurrency) + verrou de ligne pour changements de setup ; transitions hors ordre bloquées | Perte de mise à jour, anciennes pages, doubles POST |
| R2-DB-007 | Idempotence contrôlée des retries : une réponse perdue après commit ne doit créer ni deuxième compte ni nouveau grant arbitraire | Réexécution même clé/opération, réponse en retard |
| R2-DB-008 | Les erreurs SQL renvoient un code métier sûr ; détails de connexion et secrets ne quittent pas les logs privés redigés | DB inaccessible, deadlock, timeout, données malformées |
| R2-DB-009 | Migrations et rollback/compensations : pas de promesse de downgrade SQL après DDL non réversible | Migrations partiellement appliquées, fichier manquant, rollback impossible |
| R2-DB-010 | Session/grant persistent : séparation bootstrap et login, expiration et révocation, aucune dépendance Hub | Redémarrage applicatif, ancienne session, horloge décalée |
| R2-DB-011 | Chiffrement des secrets MFA seulement si activés, clés de récupération **hors domaine de panne commun** | MFA ignorée, restauration sans clé, ancien secret |
| R2-DB-012 | Pas de table métier hébergement nouvelle avant modèle validé avec tenant/foreign keys/RBAC/rétention | Accès croisé, cascade abusive, données orphelines |

## Scénarios atomiques et races

**Activation initiale.** Démarrer transaction ; verrouiller le singleton ; vérifier preuve et révision ; vérifier le statut d'activation ; insérer compte sous contrainte initial-admin et hash Argon2id ; enregistrer transition et audit ; commit ; répondre. **Aucune action Linux privilégiée dans cette transaction**. Si conflit/erreur, rollback global, puis journal technique redigé. La MFA est un **choix** et son état ne doit pas être une condition DB qui exige un secret TOTP lorsque le propriétaire choisit `skip`.

**Échec de réseau après commit.** Le client n'a pas reçu la réponse, mais la DB a commité. La demande réessayée identifie l'état et l'issue durables sans créer un second administrateur ni prolonger le grant à répétition ; une éventuelle clé d'idempotence et sa conservation sont des **contrats à valider**, pas une nouvelle colonne décidée.

**Concurrence/double POST.** Deux sessions tentent de créer l'administrateur en parallèle : un seul chemin peut réussir ; l'autre reçoit conflit sûr. Tester sous isolation transactionnelle PostgreSQL réellement configurée, et non uniquement via le dépôt mémoire.

**Indisponibilité, crash, restauration.** Les grants de bootstrap ne doivent pas être ressuscités de manière non autorisée après un snapshot/restore. Le modèle de restauration doit préserver identité/permissions et la validité des clés ; ne jamais promettre récupération à partir d'une archive chiffrée dont la clé est perdue. Les exigences plus larges Q166 sur chaque backup restent un gate R4.

## Hors périmètre et décisions à ratifier

- **DDL exact / SQL final, migrations et extensions :** uniquement après récupération et inspection de la source SRC-03 et revue Database.
- **Isolation SQL et verrouillage :** déterminer niveau d'isolation, stratégie deadlock/retry, advisory locks éventuels, TTL de grants, limites de tentatives, rétention et schéma d'idempotence à partir de tests. Aucun chiffre par défaut n'est créé ici.
- **Hébergement :** entités organisations/tenants/sites/comptes/quotas/revisions à spécifier séparément ; aucune colonne inventée.
- **Maintenance :** migrations et backups sous identité distincte du runtime Symfony ; jamais de DDL via HTTP, privilège système ou Hub.

## Matrice des tests

Voir [`R2-DB-TEST-001` à `R2-DB-TEST-010`](../13-tests-quality/r2-integration-gates.md). Tous restent **PLANNED**. Les tests historiques PHP mémoire et le PostgreSQL `SKIP` ne peuvent valider ni rollback réel, concurrence ni récupération. Gate : récupérer ZIP source original → réimplémenter/adapter contrats après revue → démarrer Symfony + PostgreSQL de test autorisé → tests SQL/integration concurrents sur SHA nommé → revue de sécurité/API et mise à jour FR/EN.

[Aide au suivi #3](https://github.com/yyogas/forgepanel/issues/3) · [Registre de lacunes](../00-project-control/documentation-readiness.md). La fermeture de `DOC-GAP-004` exige un modèle approuvé et des preuves SQL ; ce document ne suffit pas.
