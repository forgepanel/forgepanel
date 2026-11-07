<!-- forgepanel-doc id=FP-13-R2-GATES revision=2 status=specified -->
# R2 — Matrice d'intégration Symfony, identité et PostgreSQL

[English](../../en/13-tests-quality/r2-integration-gates.md) · [Qualité](README.md) · [Identité](../03-core/bootstrap-identity-r2.md) · [Transactions](../09-database/setup-transaction-r2.md)

**Statut : PREUVES R2 PARTIELLES — les 20 scénarios complets d'acceptation restent `PLANNED`.** Des tests PostgreSQL réels et un contrôle du noyau HTTP Symfony ont réussi sur des branches candidates ; ils ne couvrent pas toutes les branches positives et négatives de la matrice. L'archive authentique SRC-03 a été retrouvée, mais son import (#59) et le correctif MFA facultative (#60) ne sont pas fusionnés et restent à revoir. Aucun scénario incomplet n'est converti artificiellement en PASS. Les orientations Q1–Q220, la MFA administrateur facultative et l'autonomie vis-à-vis du Hub restent valables.

## Preuves partielles vérifiées sur branches candidates — 07/11/2026

| Sous-ensemble | Commit Git et CI réussie | Résultat vérifié | Ce qui **n'est pas** établi |
|---|---|---|---|
| PostgreSQL / PDO | [`66447a0ef88e`](https://github.com/yyogas/forgepanel/commit/66447a0ef88e323411ad14edfa9b80cd550c955f), [CI #42383929498](https://github.com/yyogas/forgepanel/actions/runs/42383929498), [PR brouillon #61](https://github.com/yyogas/forgepanel/pull/61) | PostgreSQL **16.15**, PHP **8.3.6**, migrations `001_setup.sql` et `002_optional_admin_mfa.sql` sur une base `*_test` jetable, **23 assertions SQL réelles**, timeout de verrou, unicité admin, rollback, MFA ignorée et vérifications de rejeu | Course de deux inscriptions HTTP valides, rôles SQL séparés, crash/redémarrage et restauration |
| Symfony HttpKernel | [`d34dba52405c`](https://github.com/yyogas/forgepanel/commit/d34dba52405c7cb7b450da989c3e8977ae8e0332), [CI #42385350165](https://github.com/yyogas/forgepanel/actions/runs/42385350165), [PR brouillon #62](https://github.com/yyogas/forgepanel/pull/62) | Noyau/conteneur/routes Symfony **7.4**, installation des **47 paquets Composer verrouillés**, `composer audit --locked` (aucun avis de vulnérabilité signalé), **12 assertions HTTP** : origine HTTPS, Host/port, méthodes, Origin, taille, absence CSRF, en-têtes | Vrai serveur HTTPS, navigateur et sessions, CSRF positif authentifié, connexion permanente, récupération et installateur opérationnel |

**Portée des preuves :** ces sous-ensembles sont **VERIFIED sur les commits candidats nommés**, et non `R2 COMPLETE`, pas une release ni une certification OS/WebStack. L'absence de CSRF entraîne un refus (HTTP 401 ou 403) avant finalisation de l'authentification permanente. Tests statiques, audit Composer et CI ne remplacent pas la revue de sécurité indépendante. Les PR dépendent de l'import #59 et de la MFA facultative #60. [Détails PostgreSQL](r2-postgres-execution.md) · [Détails HTTP Symfony](r2-symfony-http-smoke.md).



## Campagne A — Authentification et sécurité HTTP

| ID test | Contrat | Scénario positif | Refus / négatif | État |
|---|---|---|---|---|
| `R2-AUTH-001` | Compte initial et MFA ignorée | Succès wizard sans TOTP ; login permanent après commit | Refuser champ TOTP requis lors de skip | **PLANNED** |
| `R2-AUTH-002` | Enrôlement MFA activé | Preuve TOTP et récupération protégée | TOTP erroné/rejeu ne valide pas l'étape | **PLANNED** |
| `R2-AUTH-003` | Jeton bootstrap expiré/rejoué | Échange unique du jeton valide | Échec indistinguable/borne pour expiré ou déjà consommé | **PLANNED** |
| `R2-AUTH-004` | CSRF/Host/Origin/proxy | Origine confiable + CSRF valide | Refus Host spoofé, proxy non fiable, CSRF manquant | **PLANNED** |
| `R2-AUTH-005` | Concurrence création initiale | Un seul compte durable | Deux activations concurrentes ne créent pas deux comptes | **PLANNED** |
| `R2-AUTH-006` | Réponse perdue après commit | Lire résultat durable et reprendre sans duplicat | Retenter ne prolonge pas le grant arbitrairement | **PLANNED** |
| `R2-AUTH-007` | Reprise et révocation de grant | Nouveau grant autorisé, ancien invalidé | Ancien grant/revision refusé | **PLANNED** |
| `R2-AUTH-008` | Session permanente | Rotation login/logout et expiration côté serveur | Fixation, cookie non Secure et session bootstrap réutilisée refusés | **PLANNED** |
| `R2-AUTH-009` | Autorisation organisation/site | Gestionnaire autorisé limité à ses sites | Cross-tenant, API hors rôle et shell générique refusés | **PLANNED** |
| `R2-AUTH-010` | Accès admin perdu et panne Hub | Reprise locale autorisée auditée sans Hub | Preuve faible, endpoint root public, effacement admin refusés | **PLANNED** |

**Préconditions de campagne A :** code Foundation original importé et audité ; Composer lock vérifié avec Symfony réellement démarré, secrets/hosts de test, HTTPS local de test, navigateur HTTP capable de cookie/CSRF, PostgreSQL dédié. Un scénario ne passe que si chaque branche positive **et** négative est observée, avec logs redigés.

## Campagne B — Transactions et récupération PostgreSQL

| ID test | Contrat | Scénario positif | Refus / négatif | État |
|---|---|---|---|---|
| `R2-DB-TEST-001` | Installation initiale | Appliquer migration dans PostgreSQL de test dédié | Migration divergente ou invalidée refusée | **PLANNED** |
| `R2-DB-TEST-002` | Migrations concurrentes | Une seule prise de verrou | Double DDL ou table partielle refusés | **PLANNED** |
| `R2-DB-TEST-003` | Singleton de setup | Une seule ligne et révision cohérente | Double singleton et révision périmée refusés | **PLANNED** |
| `R2-DB-TEST-004` | Unicité admin | Un compte initial après deux transactions | Second `initial_admin=true` refusé par DB | **PLANNED** |
| `R2-DB-TEST-005` | Rollback preuve/état/audit | Commit atomique succès + audit | Erreur volontaire ne laisse ni grant ni audit de réussite | **PLANNED** |
| `R2-DB-TEST-006` | Tentatives invalides persistantes | Compteur/limites maintenus entre requêtes | Rollback ne réinitialise pas blocage intentionnel | **PLANNED** |
| `R2-DB-TEST-007` | Réponse perdue/idempotence | Retry retrouve transition commitée | Aucun compte/grant dupliqué | **PLANNED** |
| `R2-DB-TEST-008` | Crash/restart/concurrence | État durable récupéré proprement | Deadlock, interruption ou base absente produisent erreur sûre | **PLANNED** |
| `R2-DB-TEST-009` | MFA ignorée/secret | Aucun secret TOTP si skip, secret chiffré si enable | Secrets DB, logs, export et réponse HTTP ne fuient pas | **PLANNED** |
| `R2-DB-TEST-010` | Restauration et perte de clé | Reprise SQL/identité cohérente si clé disponible | Sans clé, état non récupérable déclaré explicitement | **PLANNED** |

**Préconditions B :** rôle migrateur distinct du rôle runtime, DB PostgreSQL de test autorisée, migrations étiquetées/checksummées, transaction isolation et point de restauration contrôlé. Les tests de corruption/interruption s'exécutent **seulement dans des environnements jetables autorisés** ; pas sur un hôte client ou en production.

## Registre de preuves requis pour chaque cas

Le rapport de test réel devra inclure **commit SHA, version OS/PHP/Symfony/PostgreSQL, migration ID/checksum, test ID, acteur/tenant, prérequis, commande/HTTP, résultat observé, résultat attendu, code erreur, état transactionnel, corrélation, logs expurgés, cleanup et état `PASS/FAIL/BLOCKED/SKIP`**. Une absence de DB réelle impose `SKIP`, jamais `PASS`. Mesures de performance/latence et réglages commerciaux restent ouverts : ne pas inventer de seuil.

## Garde-fous de revue et ordre

1. **Import des sources R1 non fusionné** : l'archive SRC-03 a été retrouvée ; les sources figurent dans la [PR brouillon #59](https://github.com/yyogas/forgepanel/pull/59) et la MFA facultative dans la [PR brouillon #60](https://github.com/yyogas/forgepanel/pull/60). Revue indépendante sécurité/licences encore requise.
2. **R2 candidats** : ratifier schémas et contrats, puis démarrer Symfony + PostgreSQL avec identité locale et MFA facultative.
3. **Exécuter les 20 cas**, notamment rollback, concurrence et perte de réponse ; attester l'état sur commit/OS identifié.
4. Les autorités Database, Security et API/IPC examinent toute modification de schéma, récupération ou endpoint.
5. Le Core reste autonome sans Hub ; aucune API générique `shell.exec`, aucune installation privilégiée, aucune promotion `stable/main/production` sans gates supplémentaires.

[Issue Identity #6](https://github.com/yyogas/forgepanel/issues/6) · [Issue Symfony/PG #3](https://github.com/yyogas/forgepanel/issues/3) · [Lacunes `DOC-GAP-002`–`DOC-GAP-004`](../00-project-control/documentation-readiness.md). La clôture documentaire dépend de preuves et d'une revue ; ce tableau ne ferme aucune issue.
