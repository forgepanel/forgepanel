<!-- forgepanel-doc id=FP-19 revision=2 status=documented -->
# Audit, contradictions et risques

[English](../../en/19-audits-risks/README.md) · [Index](../README.md)

[État observé et provenance](baseline.md) · [Vérifications et limites](verification.md)

## Registre des risques et réconciliations

| ID | Preuve / contradiction | Impact et action suivante |
|---|---|---|
| RISK-001 | Le texte propriétaire dit public ; le connecteur indique privé | Conserver la visibilité ; rédiger des documents publiables ; tout changement relève du propriétaire |
| RISK-002 | Les échanges décrivent du code ; GitHub était vide | Une archive implémentée n'est pas du code versionné ; prochain lot : import revu avec provenance |
| RISK-003 | Préférence PHP 8.4 contre archive >=8.2 ; pas de politique de paquets sur six OS | Conserver les faits du manifeste ; qualifier runtime et provenance avant installation |
| RISK-004 | Twig présent, UX/Tailwind/Messenger seulement cibles | Ne pas annoncer de dépendances ou fonctions absentes |
| RISK-005 | Code SQL/HTTP existant sans intégration testée | Bloquer l'exposition avant tests réels de transaction, concurrence, sessions et navigateur |
| RISK-006 | Bootstrap local et verrouillage global après cinq essais | Tester récupération et déni de service ; le drapeau local n'est pas une sandbox |
| RISK-007 | Agent complet, réparation et adaptateurs système absents | Ne pas annoncer installation en une commande, réparation ou WebStacks certifiées |
| RISK-008 | Bootstrap fichier v0.6 contre SQL v0.7 | Documenter l'incompatibilité ; aucun repli silencieux vers l'ancien store |
| RISK-009 | Licence/contributions et contact privé de sécurité non décidés | Arbitrages propriétaire avant redistribution externe/contributions et support public |
| RISK-010 | Lecture des protections refusée ; rulesets refusés avec message de formule | Préserver les paramètres ; ne pas déduire absence de protections ni contourner une approbation |
| RISK-011 | Vérificateur de release sans cycle complet de confiance | Prévoir clés de confiance, vérification d'artefacts, anti-retour arrière persistant, rotation/révocation |
| RISK-012 | Aucun relecteur indépendant ni benchmark de production | Auto-revue et tests limités, pas audit/certification/preuve de performance |

## Politique de résolution

Consigner source, documents/contrats affectés, risque, proposition et responsable de décision. Réconcilier les exigences explicites récentes sans effacer la provenance historique. Ne pas décider implicitement licence, architecture, visibilité publique ou déploiement pour lever un blocage.

Les numéros v0.1–v0.5 des échanges concernent la conception, pas une chronologie de releases. `0.7.0-dev` est l'identifiant propre à l'archive. Seuls les changements réels du dépôt entrent au changelog central ; la roadmap ne devient pas une release.

L'audit a examiné métadonnées du dépôt, structure des archives, code/contrats clés et tests natifs. Il n'est ni une revue de sécurité exhaustive, ni un audit des dépendances, ni un pentest ou une certification six OS. Ajouter les nouveaux constats et répercuter leurs effets dans les deux langues.

## Risques de préflight et blocage de l'import R1

- **RISK-013** — Archive authentique SRC-03 indisponible : pas d'import ni réécriture de code depuis des documents ; restaurer les vrais octets et valider l'empreinte épinglée.
- **RISK-014** — SHA-256 de provenance et signatures de secrets détectées ne valent ni authentification éditeur, ni audit exhaustif ; maintenir revue juridique, dépendances, secrets, diff et architecture avant import.

Le [préflight R1](../12-development/source-archive-intake.md) réduit certains risques d'archive, **sans fermer RISK-002 ni valider la production**.
