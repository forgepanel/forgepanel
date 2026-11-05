<!-- forgepanel-doc id=FP-06 revision=4 status=documented -->
# Applications et recettes d'installation

[English](../../en/06-apps-recipes/README.md) · [Index](../README.md)

Le prototype fourni ne contient ni catalogue applicatif, ni exécuteur de recettes, ni installation automatique de CMS. Les mentions WordPress, Symfony ou Laravel de la conversation décrivent des usages visés, pas une compatibilité testée ou des logiciels embarqués.

## Fiche de recette obligatoire

Chaque recette identifie application, origine et intégrité de l'artefact, licence, runtime/extensions, profils web supportés, besoins stockage/base, secrets d'entrée, commandes de cycle de vie, contrôles de santé et chemin de mise à jour. Préciser les exigences `.htaccess`, worker, tâches de fond et répertoires inscriptibles. Ne jamais déduire la compatibilité du seul nom de l'application.

Une recette consomme un compte d'hébergement, un runtime approuvé, une base et un stockage attribués. Elle s'exécute avec l'identité du compte/de l'application, pas root. Document root et fichiers non publics sont explicites. Aucune saisie arbitraire ne devient commande shell ou chemin libre. Un identifiant SQL ne doit apparaître ni dans les journaux de commandes, ni dans les artefacts, ni dans Git.

## Cycle de vie

Planifier prérequis et quotas ; préparer des entrées immuables ; valider ; sauvegarder avant migration ; activer sous verrous ; contrôler la santé ; enregistrer artefact et version. Un retour arrière du code est distinct d'une migration SQL : ne pas promettre un rollback lorsque schéma ou données sont modifiés irréversiblement. Le retrait précise la conservation des données, bases et sauvegardes.

## Déploiements et staging (Q83–Q85, Q90)

Les recettes précisent PHP/extensions, WebStack/TLS, déploiement fichiers/SFTP/Git, staging, rollback de code **distinct des migrations DB**, clonage et restauration sélective. Comptes, secrets, données et URL staging restent isolés. Q85 C demande Git Deploy, aperçu, sauvegarde et récupération ; blue-green/canary et pipelines avancés ne sont pas sélectionnés. [Cycle du site](../02-architecture/website-lifecycle.md).

## Déclencheurs Git et staging confidentiel (Q91–Q94)

Une recette précise le PHP maintenu, extensions et migrations compatibles (Q91), les restrictions PHP-FPM du site (Q92) et son mode de déploiement Git **manuel, webhook signé ou les deux** selon politique du site (Q93). L'environnement staging doit limiter les copies de données, anonymiser selon règles, utiliser des secrets distincts, neutraliser les envois mails/webhooks et appliquer audit/rétention (Q94). La recette ne peut ni lancer une commande root arbitraire depuis un webhook ni supposer le retour arrière automatique d'une migration SQL. [Politique](../02-architecture/php-staging-and-access-policy.md).

## Recettes et politiques Q101–Q110

Une recette doit préciser versions PHP maintenues et exceptions EOL bornées, isolement Linux requis, branches/environnements/manual-webhook et barrières d'approbation, traitement des données staging sensibles et rétention. Elle décrit CA/DNS-01 compatibles, topologie SQL/cache attendue, besoin SSH temporaire et compatibilité Webmail. Les exigences de quota peuvent donner lieu à une grâce bornée approuvée sans dépasser la capacité physique. Pour une migration, distinguer présynchronisation, test de staging, bascule et réplication **seulement si prise en charge et testée**. Le manifeste est une déclaration, pas une permission root. [Règles](../02-architecture/runtime-exceptions-and-data-continuity.md).

## Acceptation et observabilité

Tester installation vierge, requête dupliquée, téléchargement interrompu, signature/empreinte invalide, runtime incorrect, migration SQL échouée, restauration et suppression dans un client isolé. Observer identifiants de job/corrélation, artefact, durée et erreurs expurgées. Chaque future entrée de catalogue référence ces tests et la combinaison OS/profil/runtime qualifiée. Aucune recette exécutable n'est annoncée sans ces preuves.

La décision Q4 ajoute **PHP, Node.js, Python et applications conteneurisées** aux runtimes clients visés, chacun isolé, quota contrôlé, versionnable et configurable. **Docker + Podman sont retenus via deux pilotes indépendants (Q51 C)**. Les images signées, le réseau et les volumes nécessitent encore spécifications et tests ; cette capacité n'est pas encore livrée.

[Modules](../04-modules/README.md) · [Contrats](../08-api-contracts/README.md) · [Exploitation](../15-operations/README.md)
