<!-- forgepanel-doc id=FP-17 revision=4 status=documented -->
# Guides utilisateurs et administrateurs

[English](../../en/17-user-guides/README.md) · [Index](../README.md)

## Ce que le propriétaire utilise aujourd'hui

Cette documentation sert à exprimer les priorités et examiner les résultats produit. L'agent technique assure code, tests et corrections. Ce dépôt ne fournit encore ni commande d'installation publiée, ni portail d'hébergement fonctionnel, ni procédure de support de production. Les archives sont des entrées de développement, pas des installateurs clients.

## Parcours initial visé

Un futur installateur vérifié en une commande contrôle le serveur, installe le panneau indépendamment des stacks clientes et affiche un accès HTTPS vérifié. Le propriétaire reçoit un code à usage unique dans son terminal local privilégié, crée un administrateur indépendant de root Linux, peut choisir d'activer ou non le MFA et sélectionne les services dans un wizard reprenable. Le plan explique les modifications avant application. La fin du wizard distingue services sélectionnés, réellement installés et en bonne santé.

L'archive actuelle ne prototype que l'enrôlement et l'export de configuration. Ne pas saisir le mot de passe Linux dans un formulaire web non vérifié. Ne pas ignorer un avertissement d'identité TLS pour terminer le bootstrap. Les domaines d'exemple sont documentaires, pas des services officiels.

## Choix de WebStack pour un site (Q79)

Dans le parcours utilisateur visé, le nouveau site affiche une **WebStack conseillée pour ce site**, pourquoi elle convient et quelles alternatives sont compatibles. L'administrateur du site peut choisir avant la création, puis demander un **changement de profil ultérieur** avec prévisualisation, tests des règles et chemins de récupération ; le changement ne touche pas tous les sites du serveur. [Spécification](../02-architecture/site-webstack-advisor.md). Ces écrans ne sont pas encore réalisés.

## Gestion d'un site visée (Q81–Q90)

Pour chaque site, l'utilisateur autorisé pourra consulter la WebStack recommandée (application/`.htaccess`/PHP/isolation/ressources/ports), choisir un profil compatible et demander un changement ultérieur avec prévisualisation, fenêtre de maintenance, route de test ou bascule progressive **si techniquement possible**. Les écrans visés couvriront PHP/extensions/FPM, certificats ACME et wildcard, Git Deploy/staging, bases/cache, fichiers/SFTP/SSH limité, mail/webmail, quotas et restauration sélective ou clonage. **Aucun de ces écrans n'est encore disponible comme parcours opérationnel.** [Spécifications](../00-project-control/decisions-q81-q90.md).

## Paramètres de site Q91–Q100 (futurs écrans)

L'administrateur du site pourra consulter les versions PHP maintenues et alertes EOL, sélectionner un profil d'isolation FPM réellement supporté, régler Git Deploy manuel ou webhook validé, et définir le staging privé avec rétention, anonymisation et secrets propres. Les certificats pourront être issus de plusieurs CA ACME/DNS-01, les moteurs SQL/cache attribués par compte, les clés SSH bornées/révoquées, le Webmail choisi si compatible, les quotas avec grâce autorisée et les migrations vers d'autres serveurs prévisualisées. **Aucun écran actif n'est livré** ; aucune opération ne s'exécute sans permission/validation. [Spécification Q91–Q100](../00-project-control/decisions-q91-q100.md).

## Parcours client et revendeur

Actions sur sites/domaines/fichiers/bases/mail/sauvegardes et délégation revendeur sont visées, pas disponibles dans cette référence. Leurs guides seront accompagnés d'écrans vérifiés et de cas d'autorisation/erreur après implémentation. Un client ne doit pas devenir administrateur en changeant le port ou l'URL.

## Aide et récupération

Transmettre symptômes non sensibles, révision et erreurs expurgées au propriétaire/mainteneur. Ne jamais publier mots de passe, codes bootstrap, secrets MFA, données clientes ou clés de signature. Un accès ou arbitrage produit peut demander une intervention du propriétaire ; pas les corrections de programmation. Les limites CLI du prototype sont décrites dans l'[exploitation](../15-operations/README.md). La roadmap indique les livrables sans demander au propriétaire de modifier du code.
