<!-- forgepanel-doc id=FP-00-DOC-READINESS revision=4 status=documented -->
# Registre des lacunes et conditions de complétude — ForgePanel

[English](../../en/00-project-control/documentation-readiness.md) · [Pilotage](README.md) · [Matrice](requirements-traceability.md) · [Couverture](coverage.md)

**Audit ciblé des dépôts `develop`** : la présence d'indexes bilingues ne signifie pas que les spécifications ou les tests d'intégration sont complets. Le registre de données [v1](../../evidence/documentation-readiness-v1.json) conserve les identifiants et dépendances stables. Snapshot Core `a6a924370ef2c4b922b38d148594ed50d08f3b6e`, Hub `243d1ebb99649372ccc931deb603d172b2e17e18` ; toute modification ultérieure nécessite une nouvelle revue. **Q1–Q170 conservées, Q171+ sans décision.**

## Interprétation du registre

`BLOCKED` = une entrée indispensable manque réellement ; `OPEN` = spécification/contrat/preuve à compléter. `P0` = dépendance prioritaire pour la première version fonctionnelle ou sa publication ; `P1` = phase ultérieure/dépendance. **Ces priorités sont une proposition d'organisation documentaire, pas de nouvelles décisions produit.** `DOCUMENTED`/`VERIFIED` ne doivent jamais être attribués sans preuve liée ; une CI Markdown verte n'est pas un test applicatif.

## Lacunes et responsabilités

| ID | Phase / priorité | Autorité | Règles | Lacune à résoudre | Ticket / état |
|---|---|---|---|---|---|
| DOC-GAP-001 | R1 / P0 | Project Control / Engineering | Q120 | Archive Foundation v0.7 d'origine, import du code avec provenance et revue du correctif MFA facultatif | [#2](https://github.com/yyogas/forgepanel/issues/2) · **BLOCKED** |
| DOC-GAP-002 | R2 / P0 | Core / Security | Q124, Q130 | Identité administrateur permanente, MFA facultative et parcours activation/ignorance/reprise/récupération | [#6](https://github.com/yyogas/forgepanel/issues/6) · **OPEN** |
| DOC-GAP-003 | R2 / P0 | Engineering / Core | Q119, Q120 | Runtime Symfony démarrable avec dépendances verrouillées, contrats HTTPS/sessions/CSRF/navigateur | [#3](https://github.com/yyogas/forgepanel/issues/3) · **OPEN** |
| DOC-GAP-004 | R2 / P0 | Database / Core | Q126 | Modèle PostgreSQL persistant, migrations, propriétaires tenant, concurrence et sémantique sauvegarde/restauration | [#3](https://github.com/yyogas/forgepanel/issues/3) · **OPEN** |
| DOC-GAP-005 | R3 / P0 | DevOps / Security | Q61, Q62, Q119 | Installateur en une commande signé, origine des paquets, compatibilité OS et reprise interruption/réinstallation | [#15](https://github.com/yyogas/forgepanel/issues/15) · **OPEN** |
| DOC-GAP-006 | R3 / P0 | API/IPC / Security | Q47, Q120 | Opérations PHP→Go typées, privilèges minimaux, jobs/erreurs/audit/verrous sans shell arbitraire | [#9](https://github.com/yyogas/forgepanel/issues/9) · **OPEN** |
| DOC-GAP-007 | R4 / P0 | Modules / Hosting | Q83, Q91, Q119 | Premier site PHP-FPM isolé, conseiller WebStack par site, plan de configuration et santé | [#22](https://github.com/yyogas/forgepanel/issues/22) · **OPEN** |
| DOC-GAP-008 | R4 / P0 | Services / Security | Q123, Q164 | DNS externe A/AAAA publiés, sonde indépendante bornée, HTTP-01 port 80 puis HTTPS | [#29](https://github.com/yyogas/forgepanel/issues/29) · **OPEN** |
| DOC-GAP-009 | R4 / P0 | Security / Modules | Q136, Q167 | Rôles gestionnaire de site, clés publiques SFTP restreintes, révocation et refus inter-tenant | [#22](https://github.com/yyogas/forgepanel/issues/22) · **OPEN** |
| DOC-GAP-010 | R4 / P0 | Recovery / Database | Q126, Q145, Q166 | Backups panneau/sites chiffrés, disponibilité des clés et restauration isolée complète par sauvegarde | [#23](https://github.com/yyogas/forgepanel/issues/23) · **OPEN** |
| DOC-GAP-011 | R3 / P0 | DevOps / QA | Q132, Q151, Q152, Q161, Q162 | Runner KVM éphémère réel, octets lancés épinglés, quotas réels, snapshots, pannes et preuves privées signées | [#42](https://github.com/yyogas/forgepanel/issues/42) · **OPEN** |
| DOC-GAP-012 | R4 / P0 | DevOps / Operations | Q125, Q155, Q165 | Maintenance OS/paquets par serveur, réparation bornée autorisée et compensation locale | [#15](https://github.com/yyogas/forgepanel/issues/15) · **OPEN** |
| DOC-GAP-013 | R5 / P1 | Architecture / API | Q120 | ABI neutre d'extension détachée et signée, cycle de vie, compatibilité, droits et Core autonome | [#7](https://github.com/yyogas/forgepanel/issues/7) · **OPEN** |
| DOC-GAP-014 | R6 / P1 | Hub / API | Q168, Q169, Q170 | Runtime Symfony éditeur détaché, handshake signé Core et identités/bases éditeur séparées | [#2](https://github.com/yyogas/forgepanel-hub/issues/2) · **OPEN** |
| DOC-GAP-015 | R6 / P1 | Hub / Commerce | Q56, Q60, Q169, Q170 | Catalogue publié, paiement sandbox, droits idempotents, transfert à risque et avis signés FR/EN | [#3](https://github.com/yyogas/forgepanel-hub/issues/3) · **OPEN** |
| DOC-GAP-016 | PRE-PUBLIC / P0 | Legal / Governance | Q111, Q112, Q118 | Choix AGPL-only/or-later, licence commerciale, CLA/droits contributeurs et canaux sécurité vérifiés | [#11](https://github.com/yyogas/forgepanel/issues/11) · **OPEN** |
| DOC-GAP-017 | DESIGN / P0 | Design System / Product | Q55, Q70, Q80 | Auditer puis valider ou rejeter la maquette V3 ; tokens/composants versionnés, layouts par rôle et accessibilité | [#18](https://github.com/yyogas/forgepanel/issues/18) · **OPEN** |
| DOC-GAP-018 | POST-MVP / P1 | Modules / Plugins | Q51, Q80, Q81 | Fiches modules/plugins/apps/recipes complètes et manifests signés sans code extension arbitraire | [#7](https://github.com/yyogas/forgepanel/issues/7) · **OPEN** |
| DOC-GAP-019 | POST-MVP / P1 | Observability / Performance | Q67, Q68, Q142 | SLO, logs structurés/rétention, santé, capacité et budgets performance par application | [#17](https://github.com/yyogas/forgepanel/issues/17) · **OPEN** |
| DOC-GAP-020 | POST-MVP / P1 | Recovery / Architecture | Q90, Q100 | Migration inter-serveurs et restauration sélective autorisées, staging et plan compatibilité/rollback | [#26](https://github.com/yyogas/forgepanel/issues/26) · **OPEN** |
| DOC-GAP-021 | RELEASE / P0 | QA / Release | Q119, Q127, Q132 | Preuve réelle VM propre→site PHP HTTPS, builds signés, bêta privée et arrêt sur incident | [#29](https://github.com/yyogas/forgepanel/issues/29) · **OPEN** |
| DOC-GAP-022 | GUIDES / P1 | Documentation / Support | Q119, Q124 | Guides opérateur/client validés, procédures de reprise, dépannage, terminologie UI FR/EN et accessibilité | [#29](https://github.com/yyogas/forgepanel/issues/29) · **OPEN** |

## Exigences pour fermer une lacune

**Contrat de clôture obligatoire d'une lacune :** fiche fonctionnelle, scénarios positifs/négatifs, dépendances, interfaces et erreurs, rôles et permissions, données/migrations, sécurité, audit/observabilité, panne/récupération, tests traçables, versions et documents FR/EN. Les validations inapplicables doivent être marquées N/A avec justification ; aucune valeur métier non décidée ne sera inventée.

## Limites de preuve

**Blocages matériels :** SRC-03 original absent ; aucun Core Symfony/PostgreSQL opérationnel, installateur ou site PHP HTTPS vérifié ; pas d'ABI détachée utilisable ; Hub candidat uniquement. Les outils R1 de ZIP et R3 d'inspection/admission/staging KVM existent dans `develop` (PR #37–#43), mais leurs tests sont synthétiques et ne certifient aucun OS. [État](status.md) · [Roadmap](implementation-roadmap.md) · [QA](../13-tests-quality/README.md).

## Progression documentaire ciblée sur DOC-GAP-005 et DOC-GAP-006

[Le contrat IPC candidat R3](../08-api-contracts/symfony-go-ipc-r3.md), [la machine d'états d'installation](../14-devops-releases/installer-lifecycle-r3.md), [les schémas/registre fermés](../../evidence/typed-agent-operations-v1.json) et [24 tests planifiés](../13-tests-quality/r3-ipc-installer-gates.md) rendent les lacunes plus traçables. **États conservés : OPEN / OPEN**, car aucun IPC Symfony↔Go, installateur, modèle SQL de jobs ou test VM réel n'a été approuvé/exécuté. Ce lot ne ferme aucun gap et ne fixe aucun nombre de retries, timeout ou quota.

## Compléments candidats R3 pour DOC-GAP-004 et DOC-GAP-006

Les [12 exigences de jobs durables](../09-database/durable-jobs-r3.md), les [12 exigences de confiance du pair](../08-api-contracts/local-peer-trust-r3.md), les [24 cas QA planifiés](../13-tests-quality/r3-jobs-peer-gates.md) et leurs [schémas candidats](../../evidence/candidate-job-record-v1.schema.json) précisent les lacunes. **Elles restent toutes deux OPEN**, puisque le modèle physique PostgreSQL, les migrations, le daemon/IPC authentifié et les essais de concurrence/OS ne sont pas validés. Les durées, retries, protocole, comptes et quotas restent des choix techniques ouverts. Q1–Q170 conservées, Q171+ sans décision.

## Candidats supplémentaires pour DOC-GAP-004/005/006 — sans clôture

Le [modèle physique DB](../09-database/physical-jobs-model-r3.md), les [identités de services](../14-devops-releases/linux-service-identities-r3.md) et l'[exécution typée](../08-api-contracts/typed-execution-recovery-r3.md) détaillent les pistes d'implémentation et relient [36 tests candidats](../13-tests-quality/r3-physical-execution-gates.md). Les preuves JSON sont **non approuvées** ; **DOC-GAP-004, DOC-GAP-005 et DOC-GAP-006 restent OPEN** tant que PostgreSQL, Linux et VM réels n'ont pas été qualifiés. Le total des 22 lacunes initiales n'est pas modifié.
