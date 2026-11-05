<!-- forgepanel-doc id=FP-05 revision=1 status=documented -->
# Plugins et frontières de confiance

[English](../../en/05-plugins/README.md) · [Index](../README.md)

Aucun chargeur de plugins, marketplace, catalogue signé ou plugin tiers n'est implémenté dans SRC-03. Les cases de modules du wizard n'installent pas de plugins. Ce chapitre fixe des exigences ; il ne décrit pas une API d'extension disponible.

## Contrat proposé

Un futur manifeste déclare identité de l'éditeur, ID/version, versions Core/API compatibles, dépendances, points d'entrée, capacités demandées, migrations, limites, origine des mises à jour et règles de conservation/désinstallation. Une signature relie un artefact à son éditeur, sans prouver l'innocuité du code. Le schéma exact reste à concevoir et versionner.

Une extension Symfony de confiance exécutée dans le processus partage la frontière de l'application ; un manifeste n'empêche pas du PHP arbitraire d'utiliser ses privilèges. Le code non fiable nécessite une isolation séparément conçue et des API authentifiées limitées. Aucun modèle ne reçoit automatiquement root. Templates, scripts et hooks fournis sont des entrées exécutables, pas une simple configuration inoffensive.

## Cycle de vie et acceptation

L'installation prépare et vérifie l'artefact sans l'activer. L'activation exige revue des dépendances et permissions. Une mise à jour nécessite migrations et récupération ; la désactivation arrête les nouveaux travaux en conservant les données. Le retrait distingue suppression du code et destruction des données clientes. Une dépendance défaillante ou une requête malveillante ne doit empêcher ni démarrage ni récupération du Core.

L'acceptation exige tests de refus de capacités, signature/intégrité invalides, incompatibilité de version, cycles de dépendances, migration interrompue et retrait sûr. L'audit indique acteur, identité du plugin, permissions approuvées, artefact et résultat, sans secrets.

ForgePanel-Hub est désormais spécifié dans le dépôt privé `yyogas/forgepanel-hub` comme une extension éditeur détachée et facultative. **Aucun chargeur compatible ou plugin réellement actif n'existe encore.** Le catalogue (Q8, Q53 B) accepte seulement les composants **officiels et partenaires recrutés sur candidature avec vérification manuelle** ; identité, signatures, compatibilité, revue par version, retrait et permissions doivent être vérifiés. Une approbation commerciale n'est pas une sandbox. Les services privés de catalogue, licence ou facturation ne sont pas encore des composants opérationnels. S'ils sont introduits, leurs secrets, autorité de signature et données d'exploitation restent hors du dépôt public ; seuls les contrats versionnés y figurent. Cette documentation n'autorise aucun achat, compte de service ou publication de plugin.

[Modules natifs](../04-modules/README.md) · [Sécurité](../10-security/README.md) · [Critères de livraison](../14-devops-releases/README.md)
