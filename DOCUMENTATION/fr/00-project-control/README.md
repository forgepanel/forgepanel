<!-- forgepanel-doc id=FP-00 revision=14 status=documented -->
# Pilotage du projet

[English](../../en/00-project-control/README.md) · [Index](../README.md)

## Mission et autorité

ForgePanel est un nouveau panneau Linux d'hébergement. Le propriétaire fixe la direction produit et n'écrit pas le code. L'agent technique transforme ses demandes en spécifications, implémentations, tests et résultats compréhensibles. Les travaux courants, réversibles et autorisés avancent de manière autonome ; licence, dépenses, changements destructifs, visibilité et publications sensibles nécessitent la décision appropriée du propriétaire. Une validation technique ne peut dépendre de sa capacité à lire du code.

La conversation sert de MASTER / Project Control ; les décisions deviennent durables après réconciliation dans le dépôt. WCP360 est un contexte historique, pas un nom de release ni un héritage automatique de code ou de licence.

## Responsabilités

| Domaine | Livrable attendu |
|---|---|
| MASTER, PRODUCT & MODULES | Périmètre, critères d'acceptation, priorités et dépendances |
| ARCHITECTURE, API & CONTRACTS, DATABASE | Frontières, contrats versionnés et impacts des migrations |
| SECURITY, ENGINEERING / CODE REVIEW, AUDIT | Analyse de menace, revue et risques non résolus |
| SOURCE CODE, TESTS & QA | Implémentation et preuves reproductibles |
| DESIGN SYSTEM, DOCUMENTATION | Interfaces accessibles et langues synchronisées |
| DEVOPS / RELEASE, OBSERVABILITY & PERFORMANCE | Reprise, preuves de livraison, mesures et capacité |

Il s'agit de responsabilités, pas de l'affirmation que des agents ou services distincts existent déjà. Une seconde revue est requise pour les changements sensibles de production lorsque possible ; son absence est signalée sans inventer d'indépendance.

## Critères de réalisation

Chaque tâche identifie son périmètre et ses composants, fixe les critères d'acceptation, réalise un changement borné, le vérifie, actualise les deux langues et le changelog, puis indique branche/commit/PR et limites. Un test unitaire réussi n'est ni une release ni un déploiement.

[Décisions Q56–Q60](commerce-identity-release-policy.md) · [Décisions Q151–Q160](decisions-q151-q160.md) · [Contrats de qualification](../02-architecture/qualification-and-security-contracts.md) · [Décisions Q141–Q150](decisions-q141-q150.md) · [Contrats de certification et sauvegarde](../02-architecture/certification-backup-security.md) · [Décisions Q131–Q140](decisions-q131-q140.md) · [Décisions Q121–Q130](decisions-q121-q130.md) · [Qualification MVP](mvp-qualification.md) · [Décisions Q111–Q120](decisions-q111-q120.md) · [Roadmap technique](implementation-roadmap.md) · [Décisions Q101–Q110](decisions-q101-q110.md) · [Décisions Q91–Q100](decisions-q91-q100.md) · [Décisions Q81–Q90](decisions-q81-q90.md) · [Décisions Q71–Q80](decisions-q71-q80.md) · [WebStack par site](../02-architecture/site-webstack-advisor.md) · [État et roadmap](status.md) · [Arbitrages commerciaux et personnalisation](product-policy.md) · [Double licence et protection commerciale](license-commerce.md) · [Registre de décisions](decisions.md) · [Matrice de couverture](coverage.md) · [Audit](../19-audits-risks/README.md)

## Nouveaux arbitrages Q161–Q170

[Décisions Q161–Q170](decisions-q161-q170.md) · [Contrats de qualification et reprise](../02-architecture/evidence-and-recovery-q161-q170.md) · [Tests MVP planifiés](../13-tests-quality/mvp-gates-q161-q170.md). **Q1–Q160 restent en vigueur ; Q171+ sont ouverts**, aucun code ou OS certifié par ces documents.

## Audit de complétude et traçabilité

[Registre des lacunes et priorités documentaires](documentation-readiness.md) · [Matrice de traçabilité des 22 exigences de clôture](requirements-traceability.md) · [Manifest JSON versionné](../../evidence/documentation-readiness-v1.json) · [Statut réconcilié R1/R3](status.md). Les statuts `OPEN`/`BLOCKED` concernent la **documentation et ses preuves manquantes**, pas de nouveaux arbitrages Q171+. Aucune étape R2/R3/R4 n'est déclarée certifiée par ces tableaux.

## Contrats documentaires R3 — IPC, installateur et refus privilégiés

Les [contrats IPC typés](../08-api-contracts/symfony-go-ipc-r3.md), le [cycle d'installation sécurisé](../14-devops-releases/installer-lifecycle-r3.md) et les [24 tests planifiés](../13-tests-quality/r3-ipc-installer-gates.md) précisent `DOC-GAP-005/006` sans fermer leurs dépendances. Le [registre des 7 opérations candidates](../../evidence/typed-agent-operations-v1.json) interdit toute action root arbitraire et maintient **2 opérations privilégiées bloquées**. Les schémas JSON sont des contrats candidats, pas des endpoints.
