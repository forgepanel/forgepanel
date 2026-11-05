<!-- forgepanel-doc id=FP-18-HANDOVER revision=2 status=documented -->
# Passage de relais

[English](../../en/18-contributing/handover.md) · [Guide de contribution](README.md)

## Lot actuel

Fondation documentaire/gouvernance, pas développement applicatif. Branche : `features/documentation-foundation` ; base : `develop` ; commit d'amorçage : `26b7c773a0831c20e7f14bb86ef8c2697a19d523`. Lire tête et PR actuelles avant d'éditer ; ne pas supposer ce document attaché à la dernière révision. Les identifiants commit/PR du lot terminé figurent dans sa discussion GitHub et le compte rendu.

Périmètre réalisé : examen du dépôt ; état privé/vide consigné ; branches permanentes initialisées sans déploiement ; documentation parallèle sur 20 catégories ; inventaire, décisions, couverture et risques ; changelog bilingue unique ; consignes racine contributeurs/sécurité/agents ; outillage de validation documentaire. Les tests natifs v0.7 ont été relancés séparément. Aucun import applicatif ni release produit n'est effectué.

## Prochain lot borné : import du code

Retrouver l'archive SRC-03 exacte parmi les pièces projet et vérifier son SHA-256 enregistré. Ne pas reconstruire le code manquant depuis la prose ni supposer qu'un espace de travail le contient déjà. Examiner licence/provenance, emplacements de secrets, sorties générées et documentation historique. Importer uniquement sources/contrats/tests voulus dans une PR distincte. Garder l'identité de l'archive dans commit/PR, identifier les preuves historiques et intégrer les règles utiles à la documentation centrale sans second changelog.

Répéter les tests sur le commit effectivement importé. Préparer ensuite l'intégration Symfony/PostgreSQL avec verrouillage/audit des dépendances, tests HTTP/SQL/concurrence réels et environnement explicitement non productif. Ne pas sauter vers un installateur root exposé au réseau.

## Critères non résolus

Licence/contributions et contact privé de sécurité nécessitent un arbitrage propriétaire avant publication externe. Politique runtimes/paquets, identité complète, exécution agent, TLS, certification six OS et distribution signée restent des travaux techniques. Les lectures de protections sont refusées ; ne pas les contourner. Aucune revue indépendante n'a été réalisée dans ce lot.

Rapporter changements, commandes/résultats exacts, branche/commit/PR, blocages et prochaine tâche concrète. Le propriétaire n'a pas à programmer, corriger les fichiers ou valider techniquement le code.

## Suivi des prochaines tâches

Le lot documentaire est la [PR nº 1](https://github.com/yyogas/forgepanel/pull/1). L’[issue nº 2](https://github.com/yyogas/forgepanel/issues/2) suit l’import du code ; l’[issue nº 3](https://github.com/yyogas/forgepanel/issues/3) suit l’intégration Symfony/PostgreSQL et dépend de la nº 2 ; l’[issue nº 4](https://github.com/yyogas/forgepanel/issues/4) suit licence et signalement privé. Ces issues décrivent des travaux à faire, pas des implémentations terminées. Avant de poursuivre, lire l’état réel de la PR et la tête actuelle de `develop` ; créer la PR ne la fusionne pas.
