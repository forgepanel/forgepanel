<!-- forgepanel-doc id=FP-19 revision=7 status=documented -->
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

## Risques de quarantaine R1 : contrôles sans import

- **RISK-015** — Écrasement ou exécution involontaire lors d'une extraction : staging interdit sous root, dossier privé neuf hors dépôt, fichiers 0600 et chemins Linux `O_NOFOLLOW` ; arrêt/nettoyage en cas de changement d'empreinte. Une revue humaine reste impérative avant tout import.
- **RISK-016** — Noms d'entrées trompeurs et registre de preuves personnalisable : préflight refuse Unicode non canonique/bidi, `.git`, fichiers d'environnement sensibles et modes setuid/setgid ; le CLI `--stage` refuse la substitution de `--evidence`. Des contrôles heuristiques ne prouvent pas l'absence de secrets.

Les 33 tests synthétiques valident les garde-fous de code, **pas l'archive originale ou l'intégration du Core**. [Spécification](../12-development/source-staging.md).

## Constat ciblé de revue R1 — contrôle indépendant de la quarantaine

- **RISK-017** — Le reçu de staging peut être altéré après génération : audit en lecture seule imposant **archive originale et SHA canonique**, comparaison stricte des fichiers/reçu et refus des permissions exécutables, liens et éléments ajoutés/manquants.
- **RISK-018** — Risque de substitution du répertoire lors d'un échec de staging : nettoyage ancré dans un descripteur de parent privé et vérification inode/dev ; abandon signalé du nettoyage si l'identité change. Le **même UID** peut encore modifier la quarantaine **après l'audit** ; révalidation dans l'importeur final indispensable.

Ces mesures ne remplacent pas l'audit de code source ou la preuve de signature éditeur. [Contrat FR/EN](../12-development/source-staging-audit.md).

## Observation R3 : risque de qualification abusive

- **RISK-019** — La présence de `/dev/kvm` ou des drapeaux VMX/SVM ne prouve ni l'accès effectif au device, ni le lancement sécurisé de QEMU/KVM, ni isolation/quotas/snapshot/récupération. L'outil séparé [KVM Host Probe](../14-devops-releases/kvm-host-probe.md) expose donc exclusivement `qualification=NOT_EXECUTED`, plusieurs indicateurs `false` et des états `INCONCLUSIVE`/refus. Aucun résultat de CI sur runner sans KVM ne vaut certification Debian, Ubuntu ou autre OS. Le vrai pilote R3 et les rapports signés Q152/Q162 restent à implémenter.

## Risques identifiés — admission locale d'image R3

- **RISK-020** — Une politique locale **non signée** et une correspondance SHA-256 ne prouvent ni la confiance de l'éditeur ni le droit de lancer une VM ; le statut reste `REVIEW_REQUIRED`, avec `qualification=NOT_EXECUTED`. Établir identité/autorisation, provenance, signature, immutabilité et revue indépendante avant exécution.
- **RISK-021** — L'en-tête QCOW2 vérifié ne prouve pas l'intégrité **structurelle** du format ; après admission, même UID peut encore modifier l'image. Un futur runner doit valider format, verrouiller/capturer les octets et imposer les vrais quotas/isolements, en testant la reprise. Les tests synthétiques ne ferment pas RISK-019.

[Contrat préparatoire](../14-devops-releases/kvm-image-admission.md).

## R3 — Nouveaux risques de copie d'image de laboratoire

- **RISK-024** — Une image QCOW2 vérifiée puis copiée en mode 0400 **n'est pas immuable** contre un processus du même UID. Le reçu est non signé et un futur exécuteur doit faire un nouveau SHA-256 sous une frontière d’isolation/autorisation indépendante, sans accepter le reçu comme un permis QEMU.
- **RISK-025** — En cas d'interruption, une copie partielle peut rester sur disque sous le nouveau `run_id` ; échec `PARTIAL_STAGE_REQUIRES_MANUAL_CLEANUP`, sans nettoyage récursif automatique susceptible de supprimer des données substituées. Le futur runner devra tester et documenter un nettoyage atomique/sûr, des quotas réels et la récupération de pannes.

[Spécification et limitations](../14-devops-releases/kvm-image-staging.md). Ne ferme ni RISK-019, ni RISK-020/021, ni l'issue #42.
