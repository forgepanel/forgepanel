<!-- forgepanel-doc id=FP-08-R3-PEER-TRUST revision=1 status=specified -->
# R3 — Authentification du pair local Symfony ↔ Go et portée des droits

[English](../../en/08-api-contracts/local-peer-trust-r3.md) · [API / IPC](README.md) · [Contrats IPC](symfony-go-ipc-r3.md) · [Jobs durables](../09-database/durable-jobs-r3.md) · [Matrice QA](../13-tests-quality/r3-jobs-peer-gates.md)

**Autorité : API / IPC / Contracts et Security / Hardening (revue conjointe obligatoire).** État **SPECIFIED / CANDIDATE**, **transport non sélectionné**, aucun socket, daemon, certificat, token ou identité Linux créé. Les choix définitifs relèvent des revues Security, DevOps et Database, pas de cette fiche. Exigences `PEER-FP-0001` à `PEER-FP-0012` ; Q47/Q66/Q120 et veto Q132 respectés ; Q1–Q170 inchangées. [Issue #9](https://github.com/yyogas/forgepanel/issues/9) et [DOC-GAP-006](../00-project-control/documentation-readiness.md) restent **OPEN**. SRC-03 original non importé.

## Pourquoi le socket privé ne suffit pas

Un nom de socket, l'UID du processus PHP-FPM, un `actor_id` dans une requête ou la présence d'un certificat **ne constituent pas à eux seuls** une autorisation d'opération. La sécurité exige simultanément : (a) pair/processus vérifié, (b) message borné et authentique, (c) permission/tenant/ressource **indépendamment revalidés**, (d) plan de travail approuvé avec révision et hash, (e) opération Go dans un registre fermé, (f) preuve d'effet et journalisation.

## Douze exigences de frontière locale

**PEER-FP-0001 — Surface d'exposition.** Transport local candidat : **Unix domain socket sur chemin privé**, non accessible publiquement, non écouté sur TCP/HTTP, créé par un service dédié et fermé en absence de trust/configuration. Éviter abstract namespace ou FD passage implicite sans analyse ; les propriétés exactes du socket restent à ratifier.

**PEER-FP-0002 — Comptes et propriétaires.** Isoler processus Symfony, service pont client dédié, agent Go non-root et exécuteur minimal privilégié **si et seulement si ultérieurement approuvé**. Ne jamais réutiliser l'UID général des tenants, mail, webserver ou Hub comme preuve suffisante. Le compte PHP-FPM, un plugin ou un webhook ne doit pas écrire sur le socket privilégié.

**PEER-FP-0003 — Identification du pair.** Sur Linux, envisager les **credentials obtenus du noyau** (`SO_PEERCRED` ou mécanisme équivalent qualifié), vérification UID/GID, identité d'instance/processus, éventuel `pidfd`/démarrage du processus pour éviter confusion de PID. **Ne jamais faire confiance à un UID/PID fourni dans un payload** ou inférer qu'un UID partagé prouve le binaire attendu. La méthode exacte est une décision technique encore ouverte.

**PEER-FP-0004 — Protection du chemin.** Chemin parent possédé par compte système validé, permissions fermées, refus symlinks/hardlinks, `openat`/`O_NOFOLLOW` lorsque pertinent, gestion explicite des permissions du socket et de sa rotation. Ne pas réutiliser un chemin préexistant sans vérification propriétaire, type et dev/inode. Une permission 0660 à un groupe n'est permise qu'après revue des membres.

**PEER-FP-0005 — Cycle de vie de session.** Lier handshake à identité du pair, version/protocole et configuration effective ; rejeter connexions anciennes après redémarrage/rotation, fd réutilisés, reconnection non autorisée et activation avant `readiness`. Une connexion ouverte ne signifie pas qu'un acteur utilisateur final est authentifié.

**PEER-FP-0006 — Identité et mandat utilisateur.** Symfony prouve la session et l'autorisation **serveur** de l'acteur ; un grant/mandat borné lié au type d'opération, tenant, ressource, révision, plan et demande peut être proposé à Go. Go valide sa provenance et son contexte ; une assertion JSON `actor_claim` seule ne vaut **ni signature ni mandat**. Algorithme, format, durée et racine de confiance sont **à spécifier** sans code source inventé.

**PEER-FP-0007 — Authz indépendante et registre fermé.** Go revalide l'appartenance tenant/ressource et les droits effectifs pour l'opération `ACT-FP-*` ; rejette `shell.exec`, commande/arguments/scripts libres, opérations inconnues ou désactivées. Les opérations `ACT-FP-0005` et `ACT-FP-0007` restent **`BLOCKED_UNTIL_QUALIFIED`** malgré un schéma JSON valide. Entitlement Hub ≠ droit Linux.

**PEER-FP-0008 — Anti-rejeu et idempotence.** Lier `request_id`, `idempotency_key`, digest canonique et décision durable avec preuve de fraîcheur adaptée ; rejeter nouveau payload réutilisant la clé. Un timestamp/nonce présenté par l'attaquant ne suffit pas. Le mécanisme de replay cache, fenêtre temporelle et politiques de rotation sont ouverts ; voir [DB](../09-database/durable-jobs-r3.md).

**PEER-FP-0009 — Resource bounds.** Limiter taille et profondeur des messages, canaux/connexions concurrents, jobs/admissions par scope, file d'attente et délais sous politique explicitement approuvée. Parsing strict : version négociée, champs inconnus rejetés, aucun secret brut, aucune URL arbitraire, aucun chemin système non autorisé. Les seuils numériques ne sont **pas** décidés ici.

**PEER-FP-0010 — Erreurs et disponibilité.** Une rupture de transport, saturation, permission modifiée ou redémarrage Go renvoie `DEPENDENCY_UNAVAILABLE`/`BLOCKED` **sans masquer un effet Linux possible** ; réinterroger le job durable via endpoint autorisé, jamais relancer aveuglément `APPLY`. Distinguer `liveness` et `readiness` de la DB, du canal privé et de l'agent ; conserver la voie de récupération administrateur.

**PEER-FP-0011 — Audit et anti-fuite.** Traçage structuré de décision pair/acteur/scope/opération/ressource, version, refus, corrélation et statut réel ; **ne jamais** exposer jeton, cookie, certificat privé, secret de mandat, détail de credentials PostgreSQL ou contenu tenant. Signalement de compromission et rotation d'identité sans élévation de privilèges. Le canal n'est pas une voie de collecte privée par le Hub.

**PEER-FP-0012 — Versioning et futur distant.** Le seul contrat envisagé pour R3 est **local et privé**. Une connexion multi-serveur nécessiterait contrats séparés avec identité mutuelle forte (`mTLS` éventuel), PKI/rotation, anti-rejeu, gestion des pannes de partition et autorisation locale explicite. **Aucun port distant, CA ou protocole n'est approuvé** par cette spécification.

## Séquence logique candidate : aucun service opérationnel

```text
Symfony (auth/session/RBAC/scope) → intention durable PostgreSQL
        → demande strictement typée (schema candidate-1)
        → connexion au chemin socket privé
        → Go observe l'identité du pair via noyau et vérifie la session du canal
        → Go revalide opération, scope, politique, plan, révision et preuve d'acteur
        → ACCEPTED/DENIED/REJECTED persisté ; job distinct (pas de succès Linux)
        → Linux uniquement si une opération spécifique est un jour implémentée/validée
        → observation d'effet → VERIFY → SUCCEEDED ou état d'échec/récupération
```

**Aucune API Go actuelle n'exécute cette séquence.** Les [JSON Schema requête](../../evidence/candidate-ipc-request-v1.schema.json)/[réponse](../../evidence/candidate-ipc-response-v1.schema.json) sont des formes syntaxiques **candidates**. La [fiche de contexte du pair](../../evidence/candidate-peer-binding-v1.schema.json) est un **modèle documentaire d'attestation observée** : elle ne fabrique pas `SO_PEERCRED`, ne signe rien et ne valide aucune authentification à elle seule.

## Matrice de menaces et preuves attendues

| Menace | Refus requis | Test futur |
|---|---|---|
| Script PHP tenant ou plugin compromis | Aucun accès au socket agent ni possibilité d'usurper compte système | `R3-PEER-TEST-001/002` |
| Faux UID/PID déclaré dans JSON | Ignorer toute identité non issue du noyau/canal | `R3-PEER-TEST-003` |
| Socket remplacé, symlink, permission élargie | Fail closed avant échange, audit | `R3-PEER-TEST-004` |
| Pair autorisé mais `actor_claim` inter-tenant | Vérification indépendante de portée, aucune fuite | `R3-PEER-TEST-005/006` |
| Reconnexion après rotation, replay | Nouvelle preuve, ID/digest/état vérifiés | `R3-PEER-TEST-007/008` |
| Saturation, crash, protocole incompatible | Refus borné, état durable et récupération | `R3-PEER-TEST-009/010` |
| Commande générique ou version inconnue | Refus avant privilège | `R3-PEER-TEST-011/012` |

**HANDOFF :** Security doit ratifier identité du pair, compte Linux, politique de credentials et threat model ; API/IPC le schéma/versions/erreurs ; Database les grants et replays durables ; DevOps le socket systemd/filesystem et capacité de redémarrage ; QA les [12 cas `R3-PEER-TEST-001..012`](../13-tests-quality/r3-jobs-peer-gates.md), tous **PLANNED**. Aucun secret créé, aucune opération privilégiée, aucun endpoint réseau ou canal Hub.
