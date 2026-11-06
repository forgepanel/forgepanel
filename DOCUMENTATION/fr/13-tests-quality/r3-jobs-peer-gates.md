<!-- forgepanel-doc id=FP-13-R3-JOBS-PEER-QA revision=1 status=specified -->
# R3 — Matrice QA des jobs durables et de l'identité du pair

[English](../../en/13-tests-quality/r3-jobs-peer-gates.md) · [Qualité](README.md) · [Jobs PostgreSQL](../09-database/durable-jobs-r3.md) · [Identité IPC](../08-api-contracts/local-peer-trust-r3.md)

**État : 24 scénarios `PLANNED` et 0 `PASS` d'intégration.** Ce sont des plans d'essais et de refus, **pas des tests PHP/Go/PostgreSQL exécutés**. Le [modèle d'états candidat](../../evidence/candidate-job-transitions-v1.json), le [schéma de job](../../evidence/candidate-job-record-v1.schema.json) et le [schéma d'attestation de pair](../../evidence/candidate-peer-binding-v1.schema.json) sont des données documentaires, jamais des preuves d'authentification.

## A. Transactions, idempotence, fencing et récupération — 12 cas

| Test ID | Domaine | Cas positif | Refus / incident négatif | Statut |
|---|---|---|---|---|
| `R3-JOB-TEST-001` | Identité de job | Même clé/digest crée un seul job durable | Requête double simultanée ne crée pas deux jobs | **PLANNED** |
| `R3-JOB-TEST-002` | Conflit de digest | Nouvelle clé associée à une nouvelle intention | Même clé, contenu différent = IDEMPOTENCY_CONFLICT | **PLANNED** |
| `R3-JOB-TEST-003` | Isolation tenant | Scope vérifié depuis l'identité serveur | Même clé d'un autre tenant n'accède jamais au job | **PLANNED** |
| `R3-JOB-TEST-004` | Commit puis ACK | Réponse ACCEPTED seulement après commit durable | Commit échoué ne produit ni ACCEPTED ni succès | **PLANNED** |
| `R3-JOB-TEST-005` | Réponse perdue | Retry retrouve exactement le même job | Aucun APPLY doublé après perte d'ACK | **PLANNED** |
| `R3-JOB-TEST-006` | Fencing expiré | Worker courant présente la génération attendue | Worker ancien réveillé refusé avant effet | **PLANNED** |
| `R3-JOB-TEST-007` | Changement de révision | Mutation utilise verrou et révision actuels | Deux APPLY concurrents/stale refusés | **PLANNED** |
| `R3-JOB-TEST-008` | Effet externe incertain | Effet vérifié passe par VERIFYING | Crash après effet ne rejoue ni ne déclare SUCCEEDED | **PLANNED** |
| `R3-JOB-TEST-009` | Doubles outbox | Inbox déduplique message déjà connu | Doublon/réordonnancement ne déclenche pas deux effets | **PLANNED** |
| `R3-JOB-TEST-010` | Annulation et timeout | Annulation avant effet bloque proprement | Timeout pendant APPLY ne signifie pas échec sans effet | **PLANNED** |
| `R3-JOB-TEST-011` | Audit redigé | Transition et corrélation sans secrets | Logs/erreurs ne divulguent pas creds DB ou tokens | **PLANNED** |
| `R3-JOB-TEST-012` | Restore/reprise | Retrouver jobs/revisions et réconcilier après restauration | Stale grants/replays ou perte de clé ne valident rien | **PLANNED** |

## B. Canal privé et autorisation du pair Symfony ↔ Go — 12 cas

| Test ID | Domaine | Cas positif | Refus / incident négatif | Statut |
|---|---|---|---|---|
| `R3-PEER-TEST-001` | Processus bridge isolé | Pont dédié accède au canal privé autorisé | Code PHP d'un tenant ne se connecte pas au socket | **PLANNED** |
| `R3-PEER-TEST-002` | Identité de service | UID/GID et instance du pair conformes à la politique | Même UID partagé ne suffit pas, faux binaire refusé | **PLANNED** |
| `R3-PEER-TEST-003` | Identité déclarée | Credentials issus du noyau contrôlés | UID/PID inscrit dans JSON non reconnu | **PLANNED** |
| `R3-PEER-TEST-004` | Chemin socket sûr | Socket privé, owner/type/inode conformes | Symlink, remplacement, groupe trop large refusés | **PLANNED** |
| `R3-PEER-TEST-005` | Autorisation acteur | Mandat lié à acteur + demande après session Symfony | Claim non signé ou acteur non authentifié refusé | **PLANNED** |
| `R3-PEER-TEST-006` | Périmètre ressources | Droits tenant/ressource revérifiés par Go | Site d'un autre tenant ou rôle insuffisant refusé | **PLANNED** |
| `R3-PEER-TEST-007` | Rotation et restart | Reconnexion avec identité fraîche autorisée | Ancienne session/FD réutilisée refusée | **PLANNED** |
| `R3-PEER-TEST-008` | Rejeu/digest | Même demande retrouve décision durable | Nonce seul, payload modifié ou replay refusés | **PLANNED** |
| `R3-PEER-TEST-009` | Saturation | Limites approuvées et queue bornée | Trop de connexions/jobs ne crée pas de privilège | **PLANNED** |
| `R3-PEER-TEST-010` | Transport en panne | État durable consultable après restart | Timeout IPC n'entraîne pas retry d'APPLY aveugle | **PLANNED** |
| `R3-PEER-TEST-011` | Registre interdit | Nom connu et payload typé autorisé | shell.exec/raw argv et ACT-FP-0005/0007 refusés | **PLANNED** |
| `R3-PEER-TEST-012` | Versioning et Hub | Protocole local compatible et Core sans Hub | Version inconnue, Hub root et route réseau refusés | **PLANNED** |

## Prérequis d'une future exécution

**R1** : retrouver et auditer SRC-03 ; **R2** : Symfony/PG/identité réelle et MFA administrateur facultative ; **R3** : socket authentifié, compte bridge isolé, protocole/versions ratifiés, service Go, schéma durable de jobs avec migrations approuvées, autorisations en deux étapes et VM autorisée avant mutation Linux. Jamais de script shell privilégié générique. Les tests d'intégration doivent séparer les scénarios SQL sur PostgreSQL jetable, peer credentials Linux sur hôte de test, API HTTP/Symfony et vrais effets Linux en VM isolée.

**Preuve à joindre par ID** : version/commit SHA, OS/architecture/versions PHP-Go-Symfony-PostgreSQL, policy/révision, identifiants de ressource et tenant pseudonymisés, identité authentifiée du pair, scénario positif/négatif, requête/erreur typée, traces redigées, état PostgreSQL avant/après, génération de fencing, observation de l'effet Linux, compensation et nettoyage, décision de sécurité, verdict `PASS/FAIL/BLOCKED/SKIP`. Absence d'environnement réel = `SKIP`, **jamais PASS**.

## Points de veto

Une permission de fichier Unix ne suffit pas à prouver l'acteur. Un payload JSON « valide » n'autorise aucune action `ACT-FP-0005/0007`. Un verrou expiré ne garantit pas l'absence d'effet ; un job `SUCCEEDED` sans `VERIFYING` et preuve d'effet est invalide. Les règles de Q132 contre fuite tenant, collision de port, perte d'accès admin ou impossibilité de récupération restent bloquantes, indépendamment des performances.

**Statut de suivi :** `DOC-GAP-004` et `DOC-GAP-006` restent **OPEN** ; [issues #3](https://github.com/yyogas/forgepanel/issues/3) et [#9](https://github.com/yyogas/forgepanel/issues/9) ouvertes. Les contrôles Python documentaires valident la parité des ID et les schémas, pas les fonctions de production. Q1–Q170 conservées ; Q171+ sans décision.
