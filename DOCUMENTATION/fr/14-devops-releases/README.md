<!-- forgepanel-doc id=FP-14 revision=2 status=documented -->
# Installation, promotion Git et releases

[English](../../en/14-devops-releases/README.md) · [Index](../README.md)

## Workflow Git

`features/*` → `develop` → `stable` → `main` → `production` est l'ordre demandé par le propriétaire. Les branches temporaires incluent documentation et corrections. Réutiliser une branche pertinente, ouvrir une PR bornée, respecter contrôles/revues et préserver l'historique. Supprimer une branche temporaire obsolète seulement après intégration selon les règles du dépôt. Aucun push forcé ou contournement n'est prévu.

Le dépôt étant vide, le commit `26b7c773a0831c20e7f14bb86ef8c2697a19d523` initialise `main` avec un README. Les autres branches permanentes et `features/documentation-foundation` partent de ce commit. Cette exception d'amorçage limitée est documentée ; elle n'autorise pas les futurs commits applicatifs directs sur `main`. Les lectures de protections/rulesets ont été refusées ; leurs exigences ne sont pas supposées absentes.

## Critères d'installation

L'installation en une commande reste exigée, mais aucune URL officielle n'existe. SRC-03 produit un plan non exécutable : application de production, canal signé et manifestes de paquets certifiés manquent. Avant livraison, vérifier origine des paquets, comptes/runtime dédiés, migrations, sécurité obligatoire, HTTPS, récupération locale et interruption/réinstallation sur chaque VM cible. Ne pas adopter silencieusement des services clients ni mettre à niveau tout l'OS pour créer un site.

La vérification de signatures du prototype n'établit ni racine de confiance de production, ni rotation/révocation des clés, ni anti-retour arrière persistant, ni updater installé. La commande de manifeste ne vérifie pas elle-même les octets des artefacts.

## Application des paramètres sensibles (Q47)

L'installateur et les gestionnaires de services devront présenter le plan et son impact, valider les préconditions et les signatures, sauvegarder l'état nécessaire, appliquer avec verrous, vérifier le fonctionnement et documenter récupération/compensation. Préserver un accès de secours lors de modifications de ports ou de pare-feu. Les éléments non réversibles doivent être annoncés avant confirmation. Voir [Configuration Engine](../02-architecture/configuration-engine.md).

## Canaux et déploiements progressifs (Q57)

La cible propose **Stable, Beta, Dev** avec groupes pilotes, déploiement progressif, signatures/compatibilité et récupération contrôlée. Le Hub publie les métadonnées ; le Core local autorise et applique. Un rollback de code ne suffit pas pour une migration de base irréversible. La politique d'automatisation reste ouverte ; aucune mise à jour réelle n'est implémentée. Voir [Q56–Q60](../00-project-control/commerce-identity-release-policy.md).

## Preuves de livraison

Une release relie version, tag, commit, entrées/outils de build, lockfiles, empreintes, signatures, tests, support OS/profil et procédures upgrade/rollback. Séparer tests applicatifs et documentaires. Cette PR et la branche `production` ne créent à elles seules aucun tag, release, publication ou déploiement.

Le workflow documentaire est conçu avec permission de lecture seule, actions officielles figées et aucun secret de déploiement. Son exécution réelle se constate dans les contrôles de PR, pas dans un badge présumé. CI applicative et promotion protégée restent à implémenter après import.
