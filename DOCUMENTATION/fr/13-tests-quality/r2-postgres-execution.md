<!-- forgepanel-doc id=FP-13-R2-POSTGRES revision=1 status=specified -->
# R2 — Candidat de tests réels PostgreSQL sur environnement jetable

[English](../../en/13-tests-quality/r2-postgres-execution.md) · [Matrice R2](r2-integration-gates.md) · [Sources R1](../12-development/foundation-v07-source-import.md)

## Objectif et prérequis des sources

Exécuter les **véritables transactions PostgreSQL** de Foundation v0.7 et le correctif séparé **MFA administrateur facultative v0.7.1**, sans accès aux bases clients. Il s'agit d'une proposition empilée sur la PR d'import R1 et la PR MFA v0.7.1. **Ni leur fusion ni les revues licence/sécurité/migrations ni la validation globale R2 ne sont présumées.**

Le workflow `.github/workflows/r2-postgres-disposable.yml` lance PostgreSQL 16, limité à une **base de test jetable** sur un runner GitHub `ubuntu-24.04`, installe `pdo_pgsql` et lance deux scripts PHP. Aucun daemon système, shell root ou service client n'est touché. Les migrations historiques 001/002, le dépôt PDO et SetupService sont utilisés sans modification. Docker sert exclusivement à la **CI GitHub** : aucune dépendance Docker n'est introduite dans le Core ForgePanel.

## Scénarios SQL réellement visés

| Référence | Assertion | Preuve attendue |
|---|---|---|
| R2-DB-TEST-001 (partiel) | Exécuter `001_setup.sql` puis `002_optional_admin_mfa.sql` dans un schéma de test aléatoire | SQL réel et nettoyage |
| R2-DB-TEST-003 (partiel) | Un seul singleton et état durable observé par deux connexions | Données SQL validées |
| R2-DB-TEST-004 (partiel) | Unicité du premier administrateur imposée par la base | Deuxième insertion refusée |
| R2-DB-TEST-005 (partiel) | Test historique : erreur d'audit forcée, rollback compte/jeton | Trigger et transaction réels |
| R2-DB-TEST-006 (partiel) | Tentative invalide enregistrée et visible depuis l'autre session | Compteur durable |
| R2-DB-TEST-007 (partiel) | Rejeu d'un jeton consommé et révision obsolète rejetés | Aucun deuxième compte |
| R2-DB-TEST-008 (partiel) | Conflit de verrou borné `55P03`, transaction annulée et jeton conservé | Deux sessions SQL |
| R2-DB-TEST-009 (partiel) | Saut explicite de MFA : suppression du secret et des codes, audit conservé | Colonne nullable, compte et audit |

Le script historique `tests/postgres.php` couvre aussi l'activation TOTP, la sauvegarde de configuration et un échec transactionnel simulé. Le nouveau script couvre explicitement le parcours **sans MFA**. Une exécution PASS ne vaut preuve que pour ces scénarios SQL, jamais pour les 20 cas R2 complets. Un test ignoré avec code 77 n'est jamais compté comme PASS. Aucun résultat GitHub n'est présumé tant que la CI n'a pas terminé.

## Garde-fous obligatoires

- Refus sans `pdo_pgsql`, `FORGE_TEST_ALLOW_SCHEMA_CREATE=1`, `FORGE_TEST_PG_DSN` explicite et base dont le nom se termine par `_test`.
- Création d'un schéma aléatoire, nettoyage en `finally` après annulation des transactions ouvertes. Aucune base client ni secret de production, aucune action Linux privilégiée.
- Un conflit de verrou contrôlé n'est **pas** un test complet de deux créations simultanées. Les crashs à l'instant du commit, restauration PG, registre de migrations, séparation migrateur/runtime, reprise des clés et données réelles restent **NON EXÉCUTÉS** ; ils nécessitent la revue Database/Security/QA.
- `install apply` reste interdit. Le Core reste utilisable sans Hub et la MFA administrateur est facultative.
- Les traces du dépôt public ne doivent pas contenir de véritables mots de passe ou données clients ; l'identifiant de test CI est un exemple visiblement non productif dans un service local éphémère.

## Étapes indépendantes suivantes

Verrouiller et auditer Composer/Symfony (`composer.lock`), faire démarrer le véritable HTTP Symfony, vérifier Host/Origin/CSRF, session initiale et authentification permanente. Exécuter les autres cas PostgreSQL/concurrence/redémarrage/restauration avec des environnements autorisés. Ne pas déclarer la matrice R2 entière validée sur la base de ce sous-ensemble.