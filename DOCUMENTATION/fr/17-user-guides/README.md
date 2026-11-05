<!-- forgepanel-doc id=FP-17 revision=1 status=documented -->
# Guides utilisateurs et administrateurs

[English](../../en/17-user-guides/README.md) · [Index](../README.md)

## Ce que le propriétaire utilise aujourd'hui

Cette documentation sert à exprimer les priorités et examiner les résultats produit. L'agent technique assure code, tests et corrections. Ce dépôt ne fournit encore ni commande d'installation publiée, ni portail d'hébergement fonctionnel, ni procédure de support de production. Les archives sont des entrées de développement, pas des installateurs clients.

## Parcours initial visé

Un futur installateur vérifié en une commande contrôle le serveur, installe le panneau indépendamment des stacks clientes et affiche un accès HTTPS vérifié. Le propriétaire reçoit un code à usage unique dans son terminal local privilégié, crée un administrateur indépendant de root Linux, active le MFA et choisit les services dans un wizard reprenable. Le plan explique les modifications avant application. La fin du wizard distingue services sélectionnés, réellement installés et en bonne santé.

L'archive actuelle ne prototype que l'enrôlement et l'export de configuration. Ne pas saisir le mot de passe Linux dans un formulaire web non vérifié. Ne pas ignorer un avertissement d'identité TLS pour terminer le bootstrap. Les domaines d'exemple sont documentaires, pas des services officiels.

## Parcours client et revendeur

Actions sur sites/domaines/fichiers/bases/mail/sauvegardes et délégation revendeur sont visées, pas disponibles dans cette référence. Leurs guides seront accompagnés d'écrans vérifiés et de cas d'autorisation/erreur après implémentation. Un client ne doit pas devenir administrateur en changeant le port ou l'URL.

## Aide et récupération

Transmettre symptômes non sensibles, révision et erreurs expurgées au propriétaire/mainteneur. Ne jamais publier mots de passe, codes bootstrap, secrets MFA, données clientes ou clés de signature. Un accès ou arbitrage produit peut demander une intervention du propriétaire ; pas les corrections de programmation. Les limites CLI du prototype sont décrites dans l'[exploitation](../15-operations/README.md). La roadmap indique les livrables sans demander au propriétaire de modifier du code.
