<!-- forgepanel-doc id=FP-14 revision=9 status=documented -->
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

## Qualification et diffusion privée (Q121–Q127)

**Q121/122 :** aucun OS ni profil WebStack choisi par défaut : premier pilote après comparaison VM et sécurité. **Q123 :** domaine DNS externe, ACME HTTP-01/port 80 puis HTTPS automatique. **Q124 :** admin local + gestionnaire de site et récupération. **Q125 :** observation VPS et opérations de paquets/mises à jour OS allowlistées, planifiées, autorisées et vérifiées, sans root shell arbitraire. **Q126 :** backup du panneau et fichiers PHP avec restauration réelle et reprise cohérente du PG du panneau si nécessaire. **Q127 :** tester en interne, puis bêta **privée** uniquement après validation des preuves, consentements/conditions de distribution, droits logiciels et canaux sécurité. Aucun déploiement en production n'est autorisé par ces spécifications. [Qualification MVP](../00-project-control/mvp-qualification.md).

## Qualification VM, mises à jour et bêta — Q131–Q137

Tests sur VM système **locales et CI**, snapshots, simulations de pannes, rapports par OS et WebStack ; `SKIP` n'est pas une preuve de réussite. La sélection du premier profil exige compatibilité, sécurité, charge mesurée, maintenance, récupération et critères éliminatoires. Le MVP vérifie DNS **A/AAAA**, **port 80/HTTP-01**, **HTTPS**, diagnostics actionnables, gestionnaire de site (y compris **SFTP réel autorisé et refus inter-tenant**), mise à jour OS contrôlée avec plan/backup/santé/récupération et backup **local chiffré** restauré (distant facultatif). La bêta privée par vagues n'est accessible qu'après prérequis juridiques/sécurité et possibilité de suspension/récupération. [Décisions](../00-project-control/decisions-q131-q140.md).

## Q141–Q147 — qualifications et contrôles de la première diffusion

**VM locales/cloud par pilotes** (Q141) + runners CI compatibles et rapports communs, snapshots/pannes ; **budgets de performance par application** et régression version à version (Q142), avec veto sécurité Q132. L'assistant initial fournit des **propositions d'enregistrements DNS** et revérifie A/AAAA/80/HTTP-01/HTTPS **sans mise à jour DNS automatique** (Q143). L'OS est mis à jour selon **une politique par serveur**, avec plan, sauvegarde, santé/reprise (Q144), et non une orchestration multi-serveurs imposée au MVP. Le chiffrement du backup local doit s'accompagner d'une **clé récupérable hors panne commune**, coffre et KMS externe/multi-gardiens facultatifs (Q145). Les tests incluent SFTP sans shell/expiration/révocation/quotas/audit (Q146). Les vagues de bêta privée sont suspendues selon seuils de santé/incident configurables, avec récupération (Q147), jamais au détriment des données. [Exigences](../00-project-control/decisions-q141-q150.md).

## Publications et qualification Q151–Q158

Le premier pilote de test est **QEMU/KVM local** ; conserver l'abstraction Q141 pour d'autres VM cloud. Conserver **rapports signés**, provenances, snapshots, historiques et `SKIP` explicites (Q152), sans publication publique de matrice exigée. Les régressions dépassant les budgets applicatifs bloquent selon gravité, sauf **exception performance auditée** ; les veto sécurité ne sont pas levés (Q153). Le domaine DNS externe se valide sur les **familles A/AAAA publiées** (Q154). L'upgrade/reboot OS est **par serveur** avec approbation/backup/santé/récupération (Q155), et les archives chiffrées ne sont récupérables qu'après **accès à la clé vérifié et restauration isolée réelle** (Q156). Les clés SFTP publiques expirables et auditées (Q157) doivent être testées réellement. Pour les vagues de bêta, Q158 accepte **santé locale + signalements manuels + diagnostics minimisés aux consentements séparés**, seuils par cohorte, sans collecte forcée. [Q151–Q160](../00-project-control/decisions-q151-q160.md).

## Preuves de livraison

Une release relie version, tag, commit, entrées/outils de build, lockfiles, empreintes, signatures, tests, support OS/profil et procédures upgrade/rollback. Séparer tests applicatifs et documentaires. Cette PR et la branche `production` ne créent à elles seules aucun tag, release, publication ou déploiement.

Le workflow documentaire est conçu avec permission de lecture seule, actions officielles figées et aucun secret de déploiement. Son exécution réelle se constate dans les contrôles de PR, pas dans un badge présumé. CI applicative et promotion protégée restent à implémenter après import.
