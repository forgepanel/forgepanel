<!-- forgepanel-doc id=FP-10 revision=3 status=documented -->
# Modèle de sécurité et signalement

[English](../../en/10-security/README.md) · [Index](../README.md)

## Actifs, acteurs et frontières

Protéger privilèges Linux, données clientes, identifiants SQL, clés MFA/chiffrement, autorisations de setup, autorité de signature et intégrité de l'audit. Considérer appelants réseau anonymes, code client hostile, plugins compromis, entrées non fiables et interruptions privilégiées. Un processus déjà compromis comme utilisateur applicatif peut employer ses droits SQL ; le drapeau d'environnement bootstrap n'est pas une sandbox contre cet attaquant.

| Frontière | Exigence |
|---|---|
| Navigateur → Symfony | HTTPS vérifié, hôte/origine de confiance exacts, CSRF sur mutations, sessions sûres, limites d'essais, autorisation des ressources |
| Symfony → agent | Canal privé authentifié et versionné ; opérations typées autorisées ; aucune API `exec(command)` |
| Agent → Linux | Moindre privilège, exécuteur borné, chemins sûrs, verrous par ressource, audit système |
| Client → client | Identités/permissions distinctes et limites explicites ; un pool PHP-FPM seul ne suffit pas |
| Artefact → installation | Racine de confiance indépendante, signatures/empreintes vérifiées, anti-retour arrière et rotation sûre des clés |

SRC-03 n'implémente que les contrôles métier du setup et des protections HTTP dans les sources. Durcissement systemd, contrôles obligatoires, isolation client, rotation de secrets en production, connexion/RBAC complets et restauration ne sont pas démontrés.

## Politique MFA facultatif

Le MFA administrateur est **facultatif**, pas une condition de création du premier compte ni d'accès au wizard. Proposer TOTP et, plus tard, WebAuthn ; permettre activation différée, désactivation contrôlée et codes de récupération si activé. Protéger les actions sensibles par réauthentification et autorisations contextualisées. Le code v0.7 encore obligatoire nécessite une correction et des tests.

## Hub, communication et licences commerciales

Conformément à Q6, l'enregistrement Hub est volontaire, les vérifications premium, la recherche de versions, les diagnostics/support et les communications marketing ont des consentements ou bases de traitement distincts. Aucune collecte par défaut de fichiers, emails, bases ou secrets. Selon Q7, la durée hors ligne commerciale est de **60 jours** pour les droits premium éligibles déjà vérifiés, sous réserve des dates contractuelles ; un refus ou une révocation doit être explicite et non destructif pour l'hébergement de base. Voir la [politique produit](../00-project-control/product-policy.md).

## Identité, paiements et conservation (Q56, Q58, Q59)

Les prestataires de paiement sont des pilotes Hub indépendants : webhooks authentifiés et dédoublonnés, jamais de droit accordé par la seule redirection navigateur. L'authentification SSO/OIDC est **facultative**, avec récupération locale sécurisée ; MFA administrateur facultatif. Les rétentions par catégorie restent contraintes par la loi, les audits et les sauvegardes. Ces composants ne sont pas opérationnels.

## Chaîne de confiance et opérations sensibles (Q61, Q65, Q66)

Paquets et métadonnées de publication signés avec racines de confiance protégées, anti-rétrogradation et approbations. Sauvegardes chiffrées, distantes/immuables et récupérables, avec tests de restauration réels. Réauthentification des opérations sensibles et approbation supplémentaire selon politique ; **MFA administrateur facultatif**, non imposé comme prérequis. Ni signature, ni sauvegarde, ni deuxième validation ne remplacent un contrôle de permissions indépendant. [Q61–Q70](../00-project-control/infrastructure-decisions.md).

## Critères minimaux de livraison

Ne jamais demander le mot de passe root Linux dans le panneau. Maintenir USER fermé avant validation des autorisations et sessions. Ne pas désactiver SELinux/AppArmor ou le pare-feu pour réussir un test. Éviter les secrets dans URL, logs et artefacts. Exiger diagnostic en lecture seule avant réparation proposée et autorisation explicite avant destruction. Les tests de restauration couvrent les clés, pas seulement SQL/fichiers.

Le verrouillage après cinq essais bootstrap peut servir au déni de service ; restrictions réseau et tests de récupération restent nécessaires. Des vecteurs TOTP validés ne constituent pas un audit cryptographique. Un port n'est pas une frontière d'autorisation.

## Signalement et revue

Aucune release de production supportée, adresse privée de signalement ou garantie de réponse n'est établie. Utiliser le signalement privé GitHub seulement s'il est disponible ; sinon demander un canal privé sans publier exploitation ou secrets. Établir ce canal avant distribution publique. La revue sensible doit être distincte de l'implémentation ; aucun relecteur indépendant n'était disponible pour cet audit documentaire. Voir le [registre des risques](../19-audits-risks/README.md).
