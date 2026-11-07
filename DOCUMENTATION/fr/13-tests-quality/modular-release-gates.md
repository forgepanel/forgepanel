<!-- forgepanel-doc id=FP-13-MODULAR-GATES revision=1 status=proposed -->
# ForgePanel — Scénarios de qualification modulaire et absence de dépendances facultatives

[English](../../en/13-tests-quality/modular-release-gates.md) · [QA](README.md) · [Stratégie](../00-project-control/modular-development-strategy.md) · [Registre des tests](../../evidence/forgepanel-modular-qa-proposed-v1.json)

**35 scénarios proposés ; tous `NOT_RUN` sur un produit réellement installé.** Les tests de cohérence JSON/Python du paquet ne remplacent pas ces scénarios HTTP, SQL, VM, sécurité ou restauration. Pour chaque exécution ultérieure, conserver commit SHA, OS/WebStack, image VM et empreinte, heure, commande/harnais, résultat, preuves et responsable indépendant si applicable. `SKIP` ne vaut jamais PASS.

## 1. Parcours essentiels à garder

- Installation/reprise vérifiée du Core et de PostgreSQL, bootstrap/login, MFA facultative, RBAC, sessions et audit sur OS qualifié.
- Création d'un vrai site PHP/domain/HTTPS, isolation Linux et tenant, fichiers/SFTP, maintenance VPS bornée et restauration isolée testée.
- Refus de déployer sur OS/WebStack non qualifié ; tests d'accès refusé sur autre tenant, secret redaction, CSRF et reprise après échec.

## 2. Tests de dégradation sans modules facultatifs

| IDs | Résultat attendu | Risque observé si échec |
|---|---|---|
| MOD-QA-001..005 | Core, sessions, sites et backup/restore fonctionnent sans Hub, One-Click, Docker/Podman, catalogue distant ou module cassé | Panne en cascade |
| MOD-QA-006..010 | Absence/planifié ≠ installable : aucune route/job/migration/commande autorisée ; flags/RBAC appliqués côté serveur | Exécution de code non autorisé |
| MOD-QA-011..015 | Autorisations tenant, conservation des données, upgrade incompatible, Hub indisponible et sortie d'erreur sont maîtrisés | Isolement ou reprise insuffisants |
| MOD-QA-016..021 | Recettes native/containers séparées, carte sans faux bouton, états affichés prouvés, FR/EN accessibles et sans XSS | Confusion moteur ou UI trompeuse |
| MOD-QA-022..028 | Support OS prouvé, MFA facultative, restore réel, P0/P1 et RC/GA gates, artefact signé, patch de sécurité vérifié | Release non qualifiée |
| MOD-QA-029..035 | Hub n'accorde pas droits Linux, ne bloque pas Core gratuit, R2/VM/quorum légal/branches suivis | Dépendance commerciale ou fausse validation |

Les descriptions exactes et **tous les statuts `NOT_RUN`** sont conservés dans le [registre machine](../../evidence/forgepanel-modular-qa-proposed-v1.json). Ces plages regroupent des scénarios différents ; ne pas cocher une plage en bloc. Le noyau déclaré essentiel bloque une release s'il n'est pas testé. L'absence d'un module facultatif *réellement isolé* n'est pas un motif de blocage pour ce même jalon.

## 3. Preuves minimales pour le Module Manager

Exécuter UI + tests serveur : le catalogue en mode aperçu ne renvoie aucun `execute`, `install` ou `activate`, un statut DEVELOPING repose sur un commit/PR réel, les routes absentes ne cassent pas la navigation, aucune permission/tenant n'est inférée d'un bouton, et une carte masquée n'active pas de fonctionnalité. L'installation et l'activation future utilisent un **contrat séparé** avec droits, signature, dépendances, migrations, rollback ou récupération et audit. Tant que le Core réel n'expose pas cet API, les écrans de catalogue restent une démonstration non opérationnelle.

## 4. Gates de release et verdicts

`PASS`, `FAIL`, `BLOCKED`, `NOT_RUN` avec preuve exacte. Refuser GA si une fonction annoncée manque d'E2E, si un P0/P1 est ouvert sur son périmètre, si un restore critique a échoué, si l'origine des artefacts n'est pas validée ou si un module optionnel contamine le Core. Les risques de sécurité et d'isolation ne peuvent pas être levés par une exception de performance. Les 35 scénarios restent à **planifier et exécuter sur les véritables fichiers installés** ; ce document n'est pas une certification.