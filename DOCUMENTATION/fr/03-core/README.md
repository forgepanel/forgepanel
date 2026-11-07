<!-- forgepanel-doc id=FP-03 revision=5 status=documented -->
# Core et bootstrap

[English](../../en/03-core/README.md) · [Index](../README.md)

## Preuves actuelles du noyau

SRC-03 contient `cmd/forgepanel` et `internal/{doctor,installer,panelbridge,releases,bootstrap}`. Ce sont des packages de prototype, pas un noyau permanent complet ni un registre de modules natifs. Le store fichier historique `internal/bootstrap` reste testé mais n'est pas raccordé à l'activation web.

Le setup web utilise `SetupService`, `SetupRepository` et `SetupTransaction`. PostgreSQL porte le vérificateur de jeton, l'administrateur initial et l'état dans une transaction commune. `NEW → TOKEN_ISSUED → MFA_PENDING → CONFIGURING → REVIEWED` sont les noms de phases réels. `REVIEWED` signifie brouillon enregistré, jamais installation ou production prête.

## Sécurité et échecs

Le code génère des secrets bootstrap aléatoires de 32 octets, conserve des vérificateurs SHA-256, expire les jetons après 900 secondes et verrouille les essais après cinq échecs. Les autorisations de setup durent 1800 secondes. Le prototype v0.7 crée un administrateur en attente de MFA et impose TOTP avant configuration. **Cette obligation est maintenant obsolète** : le wizard doit offrir « activer MFA » ou « continuer sans MFA », puis passer à CONFIGURING dans les deux cas. Le code v0.7 externe demeure inchangé tant qu'il n'a pas été importé et corrigé. La reprise locale révoque l'autorisation précédente et émet un code à usage unique ; elle ne constitue pas une connexion administrateur permanente.

L'implémentation SQL verrouille `fp_setup` et écrit compte/état/audit ensemble. Les tentatives invalides persistent ; les erreurs d'infrastructure annulent la transaction. Les tests en mémoire ne prouvent ni concurrence PostgreSQL ni récupération après perte de réponse. Les reprises après commit incertain nécessitent des tests d'intégration avant exposition.

## Rôles initiaux de la v1 (Q124 B)

Le premier parcours vérifié doit fournir une connexion administrateur locale permanente avec récupération et un rôle **gestionnaire de site** qui ne peut consulter ou administrer que ses ressources autorisées. La distinction root Linux / super-administrateur application demeure. Le MFA administrateur est **facultatif** ; l'absence d'enrôlement TOTP ne doit pas bloquer le wizard. Sessions, CSRF, vérifications API/agent et refus inter-tenants seront testés sur Symfony/PG réel. [Qualification](../00-project-control/mvp-qualification.md). Il s'agit encore de critères de livraison, non de fonctions en service.

## Contrats du noyau cible

Le démarrage valide configuration et dépendances, reprend les opérations durables, enregistre les capacités, puis annonce la disponibilité. L'arrêt ferme l'admission, enregistre les étapes sûres et libère les verrous seulement après persistance. La disponibilité distingue panneau, base et agent. Aucun plugin ne doit être indispensable à l'autorisation ou à la récupération.

Les futurs jobs exigent identifiants de corrélation/idempotence, verrous par ressource, reprises limitées, classification des erreurs et compensations. La réconciliation compare états voulu et observé sans écraser les fichiers de l'administrateur. Le registre de modules refuse cycles et contrats incompatibles. Ces mécanismes sont spécifiés, pas implémentés dans l'archive.

[Fiches composants](../04-modules/components.md) · [Base](../09-database/README.md) · [Exploitation](../15-operations/README.md)

## R2 — Contrat détaillé d'identité et de bootstrap (candidat)

La [fiche R2 identité/sessions/MFA facultative](bootstrap-identity-r2.md) distingue les phases du prototype SRC-03, l'administrateur permanent, les sessions/bootstrap grants, les preuves et la récupération. Elle porte `R2-ID-001` à `R2-ID-012` ; les routes exactes, valeurs de durée et règles de reprise nécessitent ratification Security/API/Database puis tests réels. **Aucun runtime Symfony ni correctif MFA historique importé** par cette fiche.

## Core — Intention durable et séparation du pont IPC (candidat)

Les futures mutations Core nécessiteront un [journal durable PostgreSQL](../09-database/durable-jobs-r3.md) et un [canal Symfony ↔ Go au pair authentifié](../08-api-contracts/local-peer-trust-r3.md). L'interface Symfony n'accorde pas root ; le bridge doit isoler le code tenant/plugin et Go revalider scopes/permissions. Le succès HTTP/ACK ne prouve jamais une mutation Linux ; les anciens workers ne doivent pas passer un fencing expiré. [Tests PLANNED](../13-tests-quality/r3-jobs-peer-gates.md). Aucun agent, socket ou modèle physique SQL n'est livré par ces documents.

## Candidat R2 de session administrateur en lecture seule

La [prévisualisation d'identité administrateur non opérationnelle](admin-identity-r2.md) détaille Argon2id sur SQL, TOTP/code de secours facultatifs, session liée aux credentials, CSRF et limites. **`REVIEWED` n'est PAS installé ; aucun droit root ni hébergement.** Le lot reste une branche candidate empilée, pas une connexion Core/production approuvée.
