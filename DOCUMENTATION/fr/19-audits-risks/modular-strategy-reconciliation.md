<!-- forgepanel-doc id=FP-19-MODULAR-RECONCILIATION revision=1 status=proposed -->
# ForgePanel — Réconciliation des stratégies transversales avec les baselines existantes

[English](../../en/19-audits-risks/modular-strategy-reconciliation.md) · [Stratégie](../00-project-control/modular-development-strategy.md) · [Modules](../04-modules/progressive-release-policy.md) · [Releases](../14-devops-releases/release-lifecycle-plan.md)

**Audit interne de cohérence (proposé, sans revue indépendante).** Les documents génériques FR/EN sont des **propositions transversales** et ne remplacent pas les arbitrages historiques ForgePanel Q1–Q220 ni l'ordre R1→R6. Les résolutions ci-dessous sont candidates et devront être ratifiées dans la gouvernance du projet.

| Point | Source transversale / ancien plan | Règle spécifique ForgePanel proposée | État |
|---|---|---|---|
| Versions avant 1.0 | Ancien exemple utilisant `v0.1.0-prealpha.1`, `v0.3.0-alpha.1`, `v0.8.0-beta.1` | Conserver ces noms comme **anciens exemples non publiés** ; nouveau train `v1.0.0-{0..5}` avec ordre SemVer. Exploration `0.x` permise tant que la cible 1.0 n'est pas gelée | À réconcilier |
| Pre-Alpha | La stratégie générique évoque « installateur et premier parcours complet » | R2 : parcours bootstrap/identité réel en laboratoire et plan d'install non exécutable ; **l'installateur Linux est validé au R3**, jamais proclamé prêt en Pre-Alpha | À réconcilier |
| Première Stable | Le libellé « Core minimal » pourrait être interprété comme une simple maquette | R4 **installable et exploitable**, site PHP/HTTPS, SFTP, RBAC, diagnostic VPS et restauration réussie ; sécurité non reportable | Aligné sous réserve des tests |
| 1.x/2.x/3.x | 2.0/3.0 présentés comme jalons d'enrichissement | SemVer MAJOR seulement si contrat public incompatible ; ne pas bloquer des ajouts compatibles dans une mineure | À réconcilier |
| Branches de production | La source générique préfère un environnement `production`, pas nécessairement une branche | **Conserver** la branche permanente `production` déjà requise dans ForgePanel ; elle ne prouve pas un déploiement | Alignement projet prioritaire |
| Catalogue/modules | 40 entrées du pack candidat précédent et « in development » affichable | Conserver **40 (15 Core, 25 facultatifs)** ; `SPECIFIED` tant qu'aucun code prouvé ; cartes non exécutables et statut « developing » fondé sur preuves | À implémenter |
| App Center | Risque de confusion entre moteurs | **ONE-CLICK gratuit, natif, indépendant** ; **CONTAINER APPS Docker/Podman séparés**, pas de conversion silencieuse | Décisions produit conservées |
| Hub/licences | Le Hub pourrait être pris pour un composant Core obligatoire | R5 SDK neutre d'abord, R6 Hub privé facultatif ensuite ; Core gratuit jamais conditionné au Hub | Alignement projet prioritaire |
| Sécurité et qualification | Risque de décaler l'essentiel dans des modules futurs | MFA admin facultative mais RBAC, isolation, audit, HTTPS, restauration, sécurité Linux, obligations de diffusion indispensables dès le parcours concerné | Alignement projet prioritaire |
| OS/WebStack | Risque de déclarer six OS supportés avec des fixtures | Premier OS/WebStack sélectionné par **tests VM comparatifs** et rapport exact ; autres OS supportés progressivement après essais réels | À qualifier |
| Source Foundation | Ancienne documentation Core affirme archive originale manquante | Archives v0.7/v0.7.1 retrouvées **hors Git**, mais l'import sur `develop` et les tests exact-head restent à effectuer ; ne pas qualifier R1 de fusionné | État réel à corriger après import |
| Q171–Q220 | Les orientations validées vivent dans la PR #53 en brouillon | Préserver les choix approuvés et signaler `SPECIFIED / NOT MERGED`; les contrats techniques restent ouverts | PR à réconcilier |

## Blocages vérifiés

Le dépôt de l’organisation `forgepanel` refusait auparavant la création de branches (**403**). L’intégration GitHub dispose désormais de droits d’écriture vérifiés sur les dépôts distincts `yyogas/forgepanel` et `yyogas/forgepanel-hub`. Cette réconciliation est proposée sur une branche `features/*` vers `develop`, sans prétendre à une revue de sécurité indépendante, à un import du Core ni à une release. Fournir aux autorités MODULES / Security / API / Database / DevOps / QA un delta ciblé.