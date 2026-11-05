<!-- forgepanel-doc id=FP-18-HANDOVER revision=7 status=documented -->
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

## Relais R1 mis à jour — sécurité d'import

Le préflight `scripts/verify_source_archive.py` est disponible avec 16 tests synthétiques, et sa documentation [FR/EN](../12-development/source-archive-intake.md). Il **n'importe rien**. La priorité reste l'obtention du ZIP authentique SRC-03, SHA-256/92 fichiers dans [le registre](../../evidence/sources.json), puis revue manuelle de licence/secrets et import source versionné en PR sur `develop`. Les tests Go/race/vet/PHP sur code réel et R2 doivent suivre ; ne pas débloquer `install apply` avant qualification. Aucune action de codage n'est demandée au propriétaire.

## Relais R1 — préparation en quarantaine terminée, import toujours ouvert

La chaîne de préparation source comprend désormais `verify_source_archive.py` et `stage_source_archive.py`, **33 tests synthétiques**, documentation [FR/EN](../12-development/source-staging.md) et CI. Le mode par défaut n'écrit pas, `--stage` copie uniquement après contrôle vers un dossier privé neuf hors dépôt sous utilisateur nonroot ; le reçu exige une **revue manuelle**, pas un import automatique. Prochain véritable travail : récupérer **le ZIP original** SRC-03 et sa preuve SHA-256, analyser licences/diff/secrets, puis produire une **PR distincte d'import** avec tests Go/PHP réels. R2 Symfony/PostgreSQL dépend de cet import. La V3 UI reste candidate, Hub séparé.

## Prochain contrôle R1 — reçu indépendant

Avant toute PR d'import de sources PHP/Go, obtenir l'archive SRC-03 exacte ; exécuter préflight et staging privé ; puis lancer [l'audit en lecture seule](../12-development/source-staging-audit.md) avec la **même archive originale**, et examiner chaque fichier/licence/secret. L'audit ne rend pas l'import automatiquement autorisé et doit être revalidé lors de la copie finale dans Git. Le design V3 n'est pas une baseline approuvée. L'utilisateur ne doit pas coder ni manipuler root pour ce flux.

## Relais R3 — pilote de VM toujours ouvert

Le nouveau vérificateur d'[admission QCOW2](../14-devops-releases/kvm-image-admission.md) est un module Go de **préparation** séparé du Core historique et du Hub. Ne jamais convertir son verdict `REVIEW_REQUIRED` en PASS de certification ou autorisation root. Le prochain pilote QEMU/KVM devra avoir contrats typés, snapshot immuable des octets utilisés, isolation réelle, quotas et timeout/cleanup testés, signatures/stockage Q152/Q162 et tests VM sur hôte autorisé. La priorité officielle d'import Foundation v0.7 (issue #2) reste ouverte ; ni code historique ni Design System V3 n'est automatiquement validé.

## Relais R3 : copie d'image épinglée, suite du runner

Le module [Image Staging](../14-devops-releases/kvm-image-staging.md) réalise une copie privée non exécutable et re-hashée, avec reçu documentant la politique et l’état `NOT_EXECUTED`. Prochain développement : valider la provenance/signature de l'image, épingler les **octets réellement utilisés au lancement**, implémenter un pilote QEMU avec liste blanche et isolation, quotas cgroups effectivement contrôlés, durée/cleanup et tests sur hôte autorisé, puis signer les preuves Q152 et les archiver selon Q162. Aucun droit privilégié générique ; ne pas réintroduire une source Foundation v0.7 inventée. L’issue #2 d'import Core reste ouverte.
