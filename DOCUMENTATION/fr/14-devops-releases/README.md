<!-- forgepanel-doc id=FP-14 revision=5 status=documented -->
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

## Installation et publication sécurisées (Q61, Q62)

Cible : commandes d'installation simples avec vérification de provenance et **DEB/RPM signés** pour les six OS visés ; builds CI/CD, artefacts et métadonnées signés, anti-retour arrière et barrières d'approbation. Une signature de paquet n'est pas une preuve de test de compatibilité. Les clés privées d'éditeur ne doivent pas être embarquées dans l'installateur. Tester l'installation interrompue, la relance idempotente et la récupération. Voir [Q61–Q70](../00-project-control/infrastructure-decisions.md). Aucune publication opérationnelle n'a été réalisée.

## Adoption et chaîne de confiance (Q71, Q72)

La stratégie Q71 précise l'utilisation d'un KMS/HSM ou service de clés protégé, métadonnées anti-rétrogradation et rotation contrôlée, sans choisir un prestataire. Q72 élargit l'installation à un serveur contenant des services existants : **détection en lecture seule → plan d'adoption → sauvegarde → confirmation → validation et reprise**, en plus du cas serveur vierge. L'installateur doit refuser de remplacer des fichiers/service tiers sans propriété explicite. Ces modes ne seront supportés qu'après tests sur VM avec conflits réels. [Spécification](../00-project-control/decisions-q71-q80.md).

## Périmètre première version et ordre d'exécution (Q119 B, Q120 D)

**R1 sources importées avec provenance → R2 tests réels Symfony/PostgreSQL/identité/MFA optionnel → R3 installateur vérifié et testé → R4 premier site PHP administrable, domaine et HTTPS, administration VPS minimale → R5 contrat d'extension générique → R6 Hub privé.** La [roadmap](../00-project-control/implementation-roadmap.md) fixe les critères VM/HTTP/SQL et les cas de reprise ; les étapes Hub sont **après** le premier produit Core utilisable. La décision Q119 B n'exige pas toutes les WebStacks/OS ni DNS/mail natifs dès le premier jalon. Avant diffusion publique : finaliser licences/CLA après revue (Q111/Q112) et les deux canaux de signalement privés vérifiés (Q118). Aucun de ces résultats n'est présumé opérationnel.

## Preuves de livraison

Une release relie version, tag, commit, entrées/outils de build, lockfiles, empreintes, signatures, tests, support OS/profil et procédures upgrade/rollback. Séparer tests applicatifs et documentaires. Cette PR et la branche `production` ne créent à elles seules aucun tag, release, publication ou déploiement.

Le workflow documentaire est conçu avec permission de lecture seule, actions officielles figées et aucun secret de déploiement. Son exécution réelle se constate dans les contrôles de PR, pas dans un badge présumé. CI applicative et promotion protégée restent à implémenter après import.
