<!-- forgepanel-doc id=FP-00-TRACEABILITY revision=1 status=documented -->
# Matrice de traçabilité exigences → contrats → tests

[English](../../en/00-project-control/requirements-traceability.md) · [Pilotage](README.md) · [Statut](status.md)

Les **22 lignes** sont dérivées du [registre bilingue de lacunes](documentation-readiness.md) et de son [manifeste canonique](../../evidence/documentation-readiness-v1.json). Elles ne sont pas des tests exécutés. Les choix `Q1–Q170` restent la source des décisions produit ; `Q171+` n'est pas approuvée. Les priorités `P0/P1` indiquent seulement l'ordre proposé de normalisation documentaire. Les schémas décrits sont `CANDIDATE` sauf preuve d'exécution précise.

## Matrice initiale contrôlable

| Trace | Lacune / gap | Phase | Q validées | Autorité | Document/contrat de référence | QA **à vérifier** | État |
|---|---|---|---|---|---|---|---|
| FP-TRACE-001 | DOC-GAP-001 | R1 | Q120 | Project Control / Engineering | [Contrat](../12-development/source-staging-audit.md) | [QA](../13-tests-quality/README.md) | **BLOCKED** |
| FP-TRACE-002 | DOC-GAP-002 | R2 | Q124 Q130 | Core / Security | [Contrat](../03-core/README.md) | [QA](../13-tests-quality/README.md) | **OPEN** |
| FP-TRACE-003 | DOC-GAP-003 | R2 | Q119 Q120 | Engineering / Core | [Contrat](../03-core/README.md) | [QA](../13-tests-quality/README.md) | **OPEN** |
| FP-TRACE-004 | DOC-GAP-004 | R2 | Q126 | Database / Core | [Contrat](../09-database/README.md) | [QA](../13-tests-quality/README.md) | **OPEN** |
| FP-TRACE-005 | DOC-GAP-005 | R3 | Q61 Q62 Q119 | DevOps / Security | [Contrat](../14-devops-releases/README.md) | [QA](../13-tests-quality/README.md) | **OPEN** |
| FP-TRACE-006 | DOC-GAP-006 | R3 | Q47 Q120 | API/IPC / Security | [Contrat](../08-api-contracts/README.md) | [QA](../13-tests-quality/README.md) | **OPEN** |
| FP-TRACE-007 | DOC-GAP-007 | R4 | Q83 Q91 Q119 | Modules / Hosting | [Contrat](../02-architecture/website-lifecycle.md) | [QA](../13-tests-quality/README.md) | **OPEN** |
| FP-TRACE-008 | DOC-GAP-008 | R4 | Q123 Q164 | Services / Security | [Contrat](../02-architecture/qualification-and-security-contracts.md) | [QA](../13-tests-quality/mvp-gates-q161-q170.md) | **OPEN** |
| FP-TRACE-009 | DOC-GAP-009 | R4 | Q136 Q167 | Security / Modules | [Contrat](../02-architecture/php-staging-and-access-policy.md) | [QA](../13-tests-quality/mvp-gates-q161-q170.md) | **OPEN** |
| FP-TRACE-010 | DOC-GAP-010 | R4 | Q126 Q145 Q166 | Recovery / Database | [Contrat](../02-architecture/evidence-and-recovery-q161-q170.md) | [QA](../13-tests-quality/mvp-gates-q161-q170.md) | **OPEN** |
| FP-TRACE-011 | DOC-GAP-011 | R3 | Q132 Q151 Q152 Q161 Q162 | DevOps / QA | [Contrat](../14-devops-releases/kvm-image-staging.md) | [QA](../13-tests-quality/mvp-gates-q161-q170.md) | **OPEN** |
| FP-TRACE-012 | DOC-GAP-012 | R4 | Q125 Q155 Q165 | DevOps / Operations | [Contrat](../14-devops-releases/README.md) | [QA](../13-tests-quality/README.md) | **OPEN** |
| FP-TRACE-013 | DOC-GAP-013 | R5 | Q120 | Architecture / API | [Contrat](../05-plugins/README.md) | [QA](../13-tests-quality/README.md) | **OPEN** |
| FP-TRACE-014 | DOC-GAP-014 | R6 | Q168 Q169 Q170 | Hub / API | [Contrat](https://github.com/yyogas/forgepanel-hub/blob/develop/DOCUMENTATION/en/03-contracts/README.md) | [QA](https://github.com/yyogas/forgepanel-hub/blob/develop/DOCUMENTATION/en/07-tests/README.md) | **OPEN** |
| FP-TRACE-015 | DOC-GAP-015 | R6 | Q56 Q60 Q169 Q170 | Hub / Commerce | [Contrat](https://github.com/yyogas/forgepanel-hub/blob/develop/DOCUMENTATION/en/08-roadmap/decisions-q161-q170.md) | [QA](https://github.com/yyogas/forgepanel-hub/blob/develop/DOCUMENTATION/en/07-tests/mvp-and-hub-gates-q161-q170.md) | **OPEN** |
| FP-TRACE-016 | DOC-GAP-016 | PRE-PUBLIC | Q111 Q112 Q118 | Legal / Governance | [Contrat](license-commerce.md) | [QA](../13-tests-quality/README.md) | **OPEN** |
| FP-TRACE-017 | DOC-GAP-017 | DESIGN | Q55 Q70 Q80 | Design System / Product | [Contrat](../11-design-system/README.md) | [QA](../13-tests-quality/README.md) | **OPEN** |
| FP-TRACE-018 | DOC-GAP-018 | POST-MVP | Q51 Q80 Q81 | Modules / Plugins | [Contrat](../04-modules/components.md) | [QA](../13-tests-quality/README.md) | **OPEN** |
| FP-TRACE-019 | DOC-GAP-019 | POST-MVP | Q67 Q68 Q142 | Observability / Performance | [Contrat](../16-performance/README.md) | [QA](../13-tests-quality/README.md) | **OPEN** |
| FP-TRACE-020 | DOC-GAP-020 | POST-MVP | Q90 Q100 | Recovery / Architecture | [Contrat](../02-architecture/cross-server-migration.md) | [QA](../13-tests-quality/README.md) | **OPEN** |
| FP-TRACE-021 | DOC-GAP-021 | RELEASE | Q119 Q127 Q132 | QA / Release | [Contrat](mvp-qualification.md) | [QA](../13-tests-quality/README.md) | **OPEN** |
| FP-TRACE-022 | DOC-GAP-022 | GUIDES | Q119 Q124 | Documentation / Support | [Contrat](../17-user-guides/README.md) | [QA](../13-tests-quality/README.md) | **OPEN** |

## Niveaux de preuve et éléments déjà exécutés

**R3 :** toute sonde/admission/copie QCOW2 conserve `qualification=NOT_EXECUTED`. Aucune observation ni copie privée ne vaut démarrage de VM, certificat OS ou preuve d'isolement.

- **R1 outillage seulement** : PR [#37](https://github.com/yyogas/forgepanel/pull/37), [#38](https://github.com/yyogas/forgepanel/pull/38), [#39](https://github.com/yyogas/forgepanel/pull/39) fusionnées, CI [du dernier lot R1](https://github.com/yyogas/forgepanel/actions/runs/42109154403) réussie sur des ZIP **synthétiques**. L'archive SRC-03 originale n'a pas été importée.
- **R3 préparation seulement** : PR [#40](https://github.com/yyogas/forgepanel/pull/40), [#41](https://github.com/yyogas/forgepanel/pull/41), [#43](https://github.com/yyogas/forgepanel/pull/43) fusionnées, CI [Go](https://github.com/yyogas/forgepanel/actions/runs/42120185132) et [documentation](https://github.com/yyogas/forgepanel/actions/runs/42120185238) réussies. Les **62 tests Go synthétiques** ne démarrent aucun QEMU et ne certifient ni OS ni isolement.
- **Hub candidat** : [CI Hub du commit de référence](https://github.com/yyogas/forgepanel-hub/actions/runs/42066987234) réussie pour les documents/contrats/prototypes, pas une intégration fonctionnelle Symfony/ABI/paiement.
- **Non prouvés** : HTTP Symfony, PostgreSQL réel, installation Linux, PHP/HTTPS, SFTP réel, chaque-backup restore, VM QEMU/KVM, signature Q152, lancement du Hub. `PLANNED` et `SKIP` restent distincts de `PASS`.

## Contrat minimal d'une fiche traçable

Chaque propriétaire documentera **ID/version**, objectif et scénario utilisateur, acteur/permission/tenant, dépendances, schéma de données/migration, API/IPC/request/response/erreurs, idempotence/timeouts/retries, opération système permise (aucun shell arbitraire), secrets et risques, événement/log/audit, états et compensation, tests positifs/négatifs, preuve sur SHA/OS exact, UI accessible, documentation FR/EN, compatibilité/dépréciation et décision/ADR. Ne pas marquer `VERIFIED` sans résultats réels. Toute contradiction entre Core et Hub produit une demande de revue ; aucune modification silencieuse d'autorité.

## Écarts à fermer avant de déclarer la documentation complète

La complétude **de structure** (64 paires Core, 27 paires Hub dans le snapshot contrôlé) ne prouve pas la complétude métier. Priorité : exact SRC-03 → contrats R2 de démarrage/PG/identité → agent typé/installateur sûr → MVP PHP/ACME/permissions/restore → ABI neutre puis Hub. En parallèle, arbitrer formellement la maquette V3, la licence exécutoire/CLA, l'alerte privée, les valeurs encore ouvertes et les preuves QA. [Matrice de couverture](coverage.md).
