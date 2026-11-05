<!-- forgepanel-doc id=FP-03 revision=1 status=documented -->
# Core et bootstrap

[English](../../en/03-core/README.md) · [Index](../README.md)

## Preuves actuelles du noyau

SRC-03 contient `cmd/forgepanel` et `internal/{doctor,installer,panelbridge,releases,bootstrap}`. Ce sont des packages de prototype, pas un noyau permanent complet ni un registre de modules natifs. Le store fichier historique `internal/bootstrap` reste testé mais n'est pas raccordé à l'activation web.

Le setup web utilise `SetupService`, `SetupRepository` et `SetupTransaction`. PostgreSQL porte le vérificateur de jeton, l'administrateur initial et l'état dans une transaction commune. `NEW → TOKEN_ISSUED → MFA_PENDING → CONFIGURING → REVIEWED` sont les noms de phases réels. `REVIEWED` signifie brouillon enregistré, jamais installation ou production prête.

## Sécurité et échecs

Le code génère des secrets bootstrap aléatoires de 32 octets, conserve des vérificateurs SHA-256, expire les jetons après 900 secondes et verrouille les essais après cinq échecs. Les autorisations de setup durent 1800 secondes. Le prototype v0.7 crée un administrateur en attente de MFA et impose TOTP avant configuration. **Cette obligation est maintenant obsolète** : le wizard doit offrir « activer MFA » ou « continuer sans MFA », puis passer à CONFIGURING dans les deux cas. Le code v0.7 externe demeure inchangé tant qu'il n'a pas été importé et corrigé. La reprise locale révoque l'autorisation précédente et émet un code à usage unique ; elle ne constitue pas une connexion administrateur permanente.

L'implémentation SQL verrouille `fp_setup` et écrit compte/état/audit ensemble. Les tentatives invalides persistent ; les erreurs d'infrastructure annulent la transaction. Les tests en mémoire ne prouvent ni concurrence PostgreSQL ni récupération après perte de réponse. Les reprises après commit incertain nécessitent des tests d'intégration avant exposition.

## Contrats du noyau cible

Le démarrage valide configuration et dépendances, reprend les opérations durables, enregistre les capacités, puis annonce la disponibilité. L'arrêt ferme l'admission, enregistre les étapes sûres et libère les verrous seulement après persistance. La disponibilité distingue panneau, base et agent. Aucun plugin ne doit être indispensable à l'autorisation ou à la récupération.

Les futurs jobs exigent identifiants de corrélation/idempotence, verrous par ressource, reprises limitées, classification des erreurs et compensations. La réconciliation compare états voulu et observé sans écraser les fichiers de l'administrateur. Le registre de modules refuse cycles et contrats incompatibles. Ces mécanismes sont spécifiés, pas implémentés dans l'archive.

[Fiches composants](../04-modules/components.md) · [Base](../09-database/README.md) · [Exploitation](../15-operations/README.md)
