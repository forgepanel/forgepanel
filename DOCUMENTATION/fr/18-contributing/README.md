<!-- forgepanel-doc id=FP-18 revision=1 status=documented -->
# Contribution humaine et IA

[English](../../en/18-contributing/README.md) · [Index](../README.md)

## Accueil

Lire [AGENTS.md](../../../AGENTS.md), état, décisions, audit et [relais](handover.md). Vérifier accès, branches, travaux ouverts et protections. Utiliser le dépôt comme référence durable ; ne pas exiger que le propriétaire répète des conversations indisponibles. Distinguer archives fournies et sources versionnées.

## Lot cohérent

Décrire besoin, critères d'acceptation, composants/contrats et risques dans une tâche ou PR. Réutiliser ou créer `features/<sujet>` depuis la référence `develop` appropriée. Regrouper code, tests, documentation bilingue et changelog. Les commits sont en anglais. Ne pas mêler refontes sans rapport ou code tiers non revu à un import. Le workflow documentaire ne décide aucune licence.

Une PR indique base/head, périmètre, commandes/résultats, impacts sécurité/données/installation, tests manquants et retour arrière/récupération. Respecter contrôles et approbations exigés, y compris humains imposés par GitHub. Une auto-revue d'auteur ou d'IA n'est pas indépendante. Ne pas forcer les références ni fusionner une tête modifiée sans la revérifier.

## Travail parallèle et relais

Attribuer domaines de responsabilité et propriété des fichiers. Éviter les éditions simultanées des contrats, migrations et règles communes. Le responsable d'intégration réconcilie les conflits, relance les contrôles et met à jour les deux langues. Chaque relais note changements accomplis, suite, commit/PR, preuves exactes, blocages et prochaine tâche bornée.

Le propriétaire décide produit, licence, dépenses et actions sensibles/destructives, pas les détails de correction technique. Préparer alternatives et recommandation avant tout arbitrage indispensable. Signaler exactement les accès indisponibles sans inventer de réalisation.

Utiliser le [modèle de PR](../../../.github/pull_request_template.md). Avant import applicatif, seuls les contrôles documentaires s'exécutent à la racine. Supprimer les branches temporaires après intégration uniquement selon les règles applicables.
