<!-- forgepanel-doc id=FP-03-IDENTITY-R2 revision=1 status=specified -->
# R2 — Contrat candidat de bootstrap, identité et sessions

[English](../../en/03-core/bootstrap-identity-r2.md) · [Core](README.md) · [Transactions R2](../09-database/setup-transaction-r2.md) · [Matrice R2](../13-tests-quality/r2-integration-gates.md)

**Autorité :** Core / Security, avec revue Database et API/IPC. **État : SPECIFIED — CANDIDATE, non APPROVED pour implémentation.** Ce document affine les exigences existantes, **sans modifier Q1–Q170**. Il ne prouve aucun HTTP Symfony opérationnel ; l'archive SRC-03 originale manque toujours (R1, [issue #2](https://github.com/yyogas/forgepanel/issues/2)). Identifiants R2-ID-001 à R2-ID-012 : exigences documentaires, pas code exécuté.

## Frontières et acteurs

| Acteur | Droits cibles | Refus explicites |
|---|---|---|
| Visiteur non authentifié | Accéder au point d'entrée bootstrap **local** seulement quand le serveur est éligible | Configuration après activation, état ou secrets d'un autre utilisateur |
| Détenteur du jeton bootstrap | Échanger une preuve éphémère contre un grant borné | Création de plusieurs super-administrateurs initiaux, prolongation infinie, opérations Linux |
| Administrateur initial | Terminer l'identité permanente après validation des politiques | Confusion avec Linux root, accès arbitraire aux autres tenants |
| Super Administrateur de l'application | Accéder au panneau sous session autorisée et récente pour opérations sensibles | Shell root générique et contournement des permissions de ressources |
| Gestionnaire de site | Gérer **uniquement** les sites autorisés après R4 | Changement global de serveur, attribution de rôle, SFTP/backup inter-tenant |
| Administrateur du Hub | **Aucun droit privilégié Core** par simple licence | Accès aux sessions Core, clés privées, récupération OS ou contenu client |

**R2-ID-001 — Séparation :** identité Linux root, opérateur système privilégié et identité administrateur Symfony sont différentes ; un compte commercial Hub n'autorise aucune action Core.

## Cycle du bootstrap observé et cible

SRC-03 décrit `NEW → TOKEN_ISSUED → MFA_PENDING → CONFIGURING → REVIEWED`. Les noms de phases sont historiques, **pas** la preuve d'une activation permanente. Le chemin v0.7 qui rend TOTP obligatoire est **supplanté** par l'arbitrage propriétaire : **MFA facultative**, et l'absence de MFA ne bloque pas la fin du wizard.

- **R2-ID-002 — Entrée bootstrap :** accessible uniquement dans une configuration locale de confiance et avec protection contre l'exposition sur un listener public ; vérifier origin/host/proxy de confiance. Aucun jeton root n'est transmis au navigateur.
- **R2-ID-003 — Jeton/grant :** générés cryptographiquement, vérificateurs stockés sans secret brut ; expiration et limites de tentatives issues du prototype à confirmer par tests ; redaction complète dans logs, exceptions, URLs et rapports. Réponse identique face à valeur inconnue ou expirée lorsque possible.
- **R2-ID-004 — Échange atomique :** une seule transaction SQL sous verrou contrôle le jeton, ses tentatives et l'émission de grant ; réutilisation de jeton ou activation concurrente refusée. Le commit SQL précède toute réponse qui prétend qu'une étape est accomplie.
- **R2-ID-005 — Compte durable :** création d'un unique administrateur initial avec email normalisé/unique, mot de passe Argon2id et état d'activation explicite ; les contraintes DB garantissent la cardinalité même en concurrence.
- **R2-ID-006 — Choix MFA explicite :** proposer « Activer MFA » et « Continuer sans MFA ». Si activation : TOTP/enrôlement avec preuve et récupération protégée ; si refus : aucun secret TOTP inventé ni blocage. Le retour ultérieur au paramétrage MFA est un parcours authentifié et audité.
- **R2-ID-007 — Reprise :** un redémarrage/échec du wizard conserve seulement l'étape durablement enregistrée ; le nouveau grant révoque l'ancien. Les demandes hors ordre ou sur révision ancienne sont refusées sans supprimer l'administrateur valide.
- **R2-ID-008 — Séparation des sessions :** session bootstrap distincte des sessions de login permanent. Rotation d'identifiant lors de login/changement de privilège, cookie Secure/HttpOnly/SameSite adapté au flux, protection fixation/CSRF, logout et expiration côté serveur. Aucune durée numérique finale n'est imposée.
- **R2-ID-009 — Autorisation côté serveur :** RBAC + portée organisation/site + vérification d'appartenance **pour chaque API et action** ; visibilité d'un bouton ≠ autorisation. Résultat neutre entre ressources absentes/non autorisées si nécessaire contre énumération.
- **R2-ID-010 — Opérations sensibles :** authentification récente et éventuelle double validation selon politique et risque ; MFA **ne devient jamais obligatoire** par défaut, même pour l'admin, sans nouvelle décision explicite. Autorisation Core indépendante des entitlements premium.
- **R2-ID-011 — Audit :** corrélation des flux bootstrap, erreurs, réussites, renouvellement de grant, MFA activée/ignorée, récupération, login/logout et refus ; événements horodatés, tenant et acteur lorsqu'applicable, aucun token, cookie ou secret.
- **R2-ID-012 — Récupération :** définir et tester le chemin de reprise administrateur sans ouvrir un endpoint root/public, sans supprimer l'identité active et sans dépendance Hub ; les preuves et politiques du mode « accès perdu » restent un **arbitrage technique ouvert** soumis à revue Security.

## Contrats d'échange candidats (sans routes publiques nouvelles)

| Opération logique | Préconditions | Résultat métier | Échecs/reprise |
|---|---|---|---|
| `bootstrap.exchange` | Contexte local, jeton à usage borné, origine autorisée | Grant éphémère lié à un état durable | `DENIED`, `EXPIRED`, `LOCKED`, `CONFLICT`, `UNAVAILABLE` |
| `bootstrap.admin.create` | Grant valable, unicité initiale, révision courante | Compte durable inactif/configurant | `CONFLICT`, `INVALID`, rollback SQL |
| `bootstrap.mfa.choose` | Grant courant, action explicite `enable` ou `skip` | Transition persistée, secret TOTP **seulement** si choisi | `STALE_REVISION`, preuve TOTP invalide, rollback |
| `bootstrap.resume` | Autorité locale et preuve de reprise définies | Ancien grant révoqué, nouveau grant | `DENIED`, `CONFLICT`, indisponibilité DB |
| `identity.login/logout` | Identité permanente et session durcie | Session locale créée/révoquée | `DENIED`, `RATE_LIMITED`, `EXPIRED` |

**Schéma, endpoints, TTL, seuils et statuts HTTP exacts restent à ratifier** par les autorités API/IPC, Security et Database sur l'archive source importée. Une spécification candidate ne crée aucun endpoint opérationnel.

## Tests et portes de sortie

La [matrice R2](../13-tests-quality/r2-integration-gates.md) contient les cas `R2-AUTH-001` à `R2-AUTH-010`. Exiger success/failure : MFA activée ou ignorée, TOTP invalide, replay, expiration, CSRF, origine/proxy, concurrence, perte de réponse après commit, restart, session et cross-tenant denial. **État de chaque test d'intégration : PLANNED**, aucun Symfony/PDO PostgreSQL réel n'a été exécuté dans cette documentation.

**Dépendances et HANDOFF :** R1 import issue #2 → Core/Identity [#6](https://github.com/yyogas/forgepanel/issues/6) → Symfony/PG [#3](https://github.com/yyogas/forgepanel/issues/3). Toute modification de schéma requiert revue Database ; tout endpoint/IPC requiert API/IPC ; mécanisme de récupération/secret requiert Security. Pas de code, de migration ou de valeur de configuration inventée.
