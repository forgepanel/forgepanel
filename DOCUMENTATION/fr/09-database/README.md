<!-- forgepanel-doc id=FP-09 revision=8 status=documented -->
# Base de données, transactions et migrations

[English](../../en/09-database/README.md) · [Index](../README.md)

## Schéma réel du prototype

SRC-03 `apps/panel/migrations/001_setup.sql` définit trois tables, pas le vaste modèle d'hébergement proposé précédemment.

| Table | Données et contraintes |
|---|---|
| `fp_setup` | Ligne unique singleton=1 ; payload JSONB versionné avec vérificateurs de jeton/autorisation/reprise, expirations, compteurs, phase et révision du brouillon |
| `fp_admins` | UUID, email unique, mot de passe haché, indicateur admin initial, rôle super-admin restreint, secret MFA chiffré, activation, compteur TOTP et condensats de secours |
| `fp_setup_audit` | Clé primaire bigint générée, événement, métadonnées JSONB et horodatage |

Un index unique partiel autorise un seul `initial_admin=true`. `PdoSetupRepository` verrouille le setup par `FOR UPDATE` ; compte/état/audit sont écrits dans la même transaction. C'est une implémentation inspectée, pas une garantie concurrente démontrée dans cet environnement.

## Services de données Q86/Q90 — cibles

Les **bases clients MariaDB/MySQL et PostgreSQL** utiliseront des pilotes distincts et identités/quotas dédiés ; **Redis/Valkey** restent facultatifs pour le cache/queues. Ces ressources ne figurent pas dans le schéma actuel, limité au setup. Le clonage staging et la restauration sélective nécessitent snapshots cohérents, protection des secrets, autorisations tenant et contrôle avant écrasement. Le PostgreSQL du panneau reste séparé des DB clientes. [Cycle du site](../02-architecture/website-lifecycle.md).

## Moteurs clients et migrations inter-serveurs (Q96, Q100)

Un même compte d'hébergement pourra posséder des ressources **MariaDB/MySQL et PostgreSQL** distinctes, et des Redis/Valkey cache/queue facultatifs selon capacité, avec quota/permission/secret par moteur (Q96). Le PostgreSQL interne du panneau n'est **pas** mutualisé avec les bases clientes. Migration inter-serveurs Q100 : préflight versions et schémas, snapshot cohérent, transfert authentifié/chiffré, mapping de comptes SQL, secrets régénérés et restauration auditée. Aucun pilote DB client ou migrateur inter-serveurs n'existe dans le schéma prototype de setup. [Détails](../02-architecture/cross-server-migration.md).

## Topologies SQL/cache et migration Q106/Q110

Au-delà des multiples moteurs DB par compte (Q96), **Q106 D** prévoit des moteurs **mutualisés ou dédiés par plan** et des modules clusters/réplication **facultatifs, disponibles uniquement après certification réelle**. Préciser pour chaque pilote : isolation des schémas/comptes, quorum/leader/failover éventuel, latence de réplication, sauvegarde cohérente, secrets et restauration. Redis/Valkey ne sont pas automatiquement un cluster ni une base SQL. **Q110 D** autorise présynchronisation et bascule avancée seulement si les écritures applicatives et transactions peuvent être réconciliées, sinon maintenance/gel et procédure de restauration. PostgreSQL du panneau reste distinct. [Migration](../02-architecture/cross-server-migration.md) · [Décisions](../00-project-control/decisions-q101-q110.md).

## Migrations et responsabilités

Le SQL n'est pas appliqué à chaque requête HTTP. Aucun exécuteur complet de migrations ni système upgrade/rollback n'est fourni. Les futurs paquets séparent rôle de migration et rôle applicatif sans DDL, suivent identifiants/empreintes des migrations et empêchent les migrations concurrentes. Tester installation vierge et mise à jour depuis chaque révision supportée. Une migration destructive exige sauvegarde, conservation et plan de réparation ; rétrograder le code n'annule pas automatiquement les données.

La récupération des secrets exige base et clé de chiffrement. Ne pas placer la clé dans la même sauvegarde publiquement lisible que les données MFA chiffrées. Rétention de l'audit, suppression, schéma client et contrôle des requêtes par client restent à spécifier avant les fonctions d'hébergement.

## Preuves requises

Exécuter le test PostgreSQL fourni uniquement sur une base `_test` dédiée et explicitement autorisée. Il couvre rollback forcé et persistance, pas tous les modes de concurrence/panne. Ajouter activations simultanées, réponse perdue après commit, redémarrage SQL, révision obsolète et restauration/perte de clé. Aucun pilote PDO PostgreSQL/serveur n'était disponible pour cet audit ; les tests en mémoire ne sont pas des tests SQL.

[Core](../03-core/README.md) · [Qualité](../13-tests-quality/README.md)

## R2 — Contrat transactionnel candidat, sans migration

Le [contrat R2 PostgreSQL/transactions](setup-transaction-r2.md) trace `R2-DB-001` à `R2-DB-012` : singleton, unicité administrateur initial, verrous/révisions, retries après réponse perdue, rollback/audit et récupération des clés. **Aucune nouvelle table, colonne, migration, niveau d'isolation ou TTL n'est arrêté** par ce document. Revue Database indispensable après import SRC-03, puis tests PostgreSQL réels [R2](../13-tests-quality/r2-integration-gates.md).

## R3 — HANDOFF : jobs, idempotence et verrous IPC (non modélisés)

La future API [Symfony ↔ Go](../08-api-contracts/symfony-go-ipc-r3.md) exige intent/approbation/job/audit durables, révisions, idempotence et locks, tandis que le [cycle installateur](../14-devops-releases/installer-lifecycle-r3.md) doit reprendre après crash sans rejouer une étape Linux. **Aucune table/colonne/migration PostgreSQL n'est créée dans ce lot**. L'autorité Database doit définir et tester : schémas transactionnels, index uniques `(scope,operation,idempotency_key)` ou équivalent validé, cohérence digest, bail, audit/outbox, concurrence, reprise et rétention, en coordination avec Security et API/IPC. Les noms ci-dessus sont des exemples candidats, pas du DDL approuvé.

## R3 — Modèle candidat des jobs durables et des verrous

La [fiche R3 sur les jobs PostgreSQL](durable-jobs-r3.md) établit 12 exigences DB-FP-0001..0012 sur l'intention durable, l'idempotence par scope, les leases et fencing, les transitions d'états, l'outbox/inbox, les ACK perdus, la concurrence, l'audit expurgé et la récupération. Le [registre d'états candidat](../../evidence/candidate-job-transitions-v1.json) et le [schéma de job](../../evidence/candidate-job-record-v1.schema.json) ne sont **ni du DDL, ni des tables installées**. Aucune durée, isolation SQL, migration ou valeur de retry n'est approuvée sans revue Database/API/Security. [Tests QA](../13-tests-quality/r3-jobs-peer-gates.md).

## R3 — Proposition physique des jobs PostgreSQL, sans DDL

La [fiche de modèle PostgreSQL proposé](physical-jobs-model-r3.md) détaille `DBPH-FP-0001..0012`, **8 objets de tables candidats**, contraintes d'unicité, relations, isolation tenant, idempotence, outbox/inbox, verrous avec fencing et récupération. Le [registre de structure candidat](../../evidence/candidate-r3-physical-data-model-v1.json) **n'est pas une migration** et ne modifie aucune des 3 tables historiques observées de SRC-03. Tous les types/FK/index, rôles SQL et seuils doivent être ratifiés par Database/Security après récupération des sources. [36 tests R3 prévus](../13-tests-quality/r3-physical-execution-gates.md).
