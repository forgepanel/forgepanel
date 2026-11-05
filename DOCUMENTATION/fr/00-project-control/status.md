<!-- forgepanel-doc id=FP-00-STATUS revision=15 status=documented -->
# État et roadmap ordonnée par dépendances

[English](../../en/00-project-control/status.md) · [Pilotage](README.md)

## Niveaux de preuve

`PROPOSED` : option à examiner. `SPECIFIED` : exigences/contrats rédigés. `IMPLEMENTED` : code existant dont l'emplacement est précisé. `VERIFIED` : vérification nommée exécutée sur une entrée et un environnement identifiés. `PUBLISHED` : release et artefacts identifiables. `DEPLOYED` : environnement et révision déployée identifiés. `MERGED` décrit seulement l'intégration Git. Le statut documentaire est distinct du statut fonctionnel.

## État initial au 2026-11-05

| Périmètre | État réel |
|---|---|
| GitHub avant ce lot | Privé, vide ; aucune branche, commit, issue, PR ou release retournée |
| Dépôt après ce lot documentaire | Documentation, gouvernance et validation documentaire ; aucun import applicatif |
| Foundation v0.6/v0.7 | Archives de développement fournies ; provenance enregistrée dans l'audit |
| Tests natifs v0.7 | Réexécutés avec succès dans le conteneur local ; pas de certification VM |
| Intégration HTTP Symfony et PostgreSQL | Sources/test fournis ; non exécutés dans cet audit |
| Installateur, agent complet, WebStacks, RBAC complet, plugins | Non disponibles comme produit fonctionnel |
| Release et production | Aucune preuve ; licence non décidée |

Les six OS et cinq profils sont des entrées de planification. Trente combinaisons de fixtures ne sont pas trente installations. La branche `production` pointe initialement vers un commit d'amorçage contenant uniquement un README et ne déploie rien.

## Roadmap — décision Q120 D, objectif Q119 B

**Ordre technique approuvé : import des sources → intégration Symfony/PostgreSQL et identité/MFA facultatif testés → installateur sûr → premier site PHP/domaine/HTTPS et administration VPS de base → ABI générique d'extension → Hub privé.** La [roadmap détaillée](implementation-roadmap.md) définit R1 à R6 et leurs preuves. **La première version fonctionnelle Q119 B s'arrête au premier site PHP en HTTPS vérifié** : pas de DNS autoritatif, mail, HA, marketplace ou six OS certifiés d'emblée. Le Core n'est pas encore importé ; aucune étape n'est déclarée livrée.

## Roadmap

| Priorité | Livrable | Dépendance et preuves de sortie |
|---|---|---|
| P0 | Référence documentaire et PR relue | Contrôles liens/parité ; faits et risques consignés |
| P1 | Import du code avec provenance | Inventaire v0.7 revu ; aucun secret/binaire généré ; statut de licence explicite ; tests répétés sur le commit importé |
| P2 | Intégration Symfony + PostgreSQL | Résolution/verrouillage/audit des dépendances ; tests HTTP, rollback/concurrence SQL et navigateur réels |
| P3 | Identité permanente et récupération | Connexion/déconnexion, MFA facultatif (activation/désactivation/récupération), autorisation contextualisée, isolation des sessions ; corriger le setup v0.7 |
| P4 | Paquets et services sur six OS | Origines de paquets fiables, politique runtime, systemd et contrôles obligatoires validés en VM |
| P5 | Exécution des plans et installation en une commande | Étapes durables, reprises sûres, TLS, rollback/compensation, distribution signée et tests réinstallation/mise à jour |
| P6 | Modules d'hébergement et autres stacks | Isolation, limites, sauvegardes/restaurations et preuves VM par profil |
| P7 | Écosystème tiers | Modèle de confiance, contrats, isolation et maintenance validés avant exécution |

Décisions complémentaires Q48–Q55 du 2026-11-05 : **AGPL-3.0 + licence commerciale**, contributions sous **CLA**, premium plugins/cloud/managé/partenaires/support, **Docker et Podman**, après 60 jours hors ligne blocage des nouvelles opérations premium et conservation de l'existant, **partenaires sur candidature et vérification manuelle**, priorité hébergement + VPS, **une marque par organisation**. [Licences et protection](license-commerce.md) · [Pilotes conteneurs](../02-architecture/container-drivers.md). Aucune de ces options n'est une implémentation disponible.

Nouvelles décisions produit Q1–Q8 et Q47 du 2026-11-05 : **double licence (textes non choisis)**, Core gratuit complet + premium/support facultatifs, toutes cibles par phases, runtimes clients PHP/Node.js/Python/conteneurs, white-label par organisation, Hub avec consentements séparés, grâce commerciale hors ligne **60 jours**, catalogue officiel/partenaires vérifiés, changements sensibles contrôlés. [Politique détaillée](product-policy.md). Elles ne constituent pas des fonctionnalités implémentées.

Décisions Q56–Q60 confirmées : **prestataires de paiement indépendants**, **Stable/Beta/Dev + diffusion progressive/récupération**, **identité locale + SSO/OIDC facultatif**, **rétention par catégorie**, **achat définitif + abonnement + essai/coupons/packs/options**. Ces fonctionnalités restent **spécifiées**, non opérationnelles. Q61–Q70 sont maintenant décidées, mais pas implémentées. Voir [Q56–Q60](commerce-identity-release-policy.md).

Q61–Q70 sont **confirmées (2026-11-05)** : signatures CI/CD avec anti-rétrogradation/approbations ; installateur universel + DEB/RPM signés ; DNS et mail locaux/externes ; sauvegardes chiffrées immuables et réplication ; réauthentification/approbation sensibles ; multi-serveurs/HA ; monitoring/alertes intégrables ; WebStacks par site/IP/port ; éditeur visuel/widgets et marque unique. [Spécification Q61–Q70](infrastructure-decisions.md). **État : spécifié, aucun service ou cluster certifié.**

Les décisions **Q71–Q80** sont confirmées : protection/rotation des clés, adoption contrôlée, DNS conseillé après tests, Postfix/Dovecot + relais, 3-2-1 et restaurations, approbation par action, HA/orchestrateurs progressifs, Prometheus/OpenTelemetry, **WebStack conseillée par site et modifiable ensuite**, widgets déclaratifs. [Référence produit](decisions-q71-q80.md) · [WebStack par site](../02-architecture/site-webstack-advisor.md). Ce sont des spécifications, sans aucune release ni certification supplémentaires.

**Q81–Q90 sont confirmées (2026-11-05)** : WebStack recommandée selon compatibilité/sécurité/ressources et transition temporaire/progressive si admissible ; PHP et extensions/FPM par site ; ACME/wildcard/DNS-01 ; Git Deploy avec staging ; bases MariaDB/MySQL + PostgreSQL, Redis/Valkey facultatifs ; gestionnaire de fichiers/SFTP et SSH limité ; webmail/antispam/quarantaine ; quotas hérités ; restauration sélective et clonage staging. [Spécification Q81–Q90](decisions-q81-q90.md). **Tout est spécifié, non livré**.

**Q91–Q100** sont confirmées : PHP maintenu et migration planifiée ; pools PHP-FPM isolés et Linux renforcé ; Git manuel/webhook validé ; staging par site avec confidentialité/rétention ; ACME multi-autorités et DNS-01 ; plusieurs moteurs de bases/cache par compte ; SSH limité par plan ; webmail configurable ; quotas avec grâce et allocations autorisées ; restauration/migration inter-serveurs sécurisée. [Registre Q91–Q100](decisions-q91-q100.md). Ces composants sont **spécifiés, pas implémentés ou certifiés**.

**Q101–Q110 confirmées (2026-11-05)** : PHP EOL dérogatoire temporaire et migration planifiée, isolation par profils certifiés selon plan/site, Git manuel/webhook avec approbation par environnement, staging sensible sous autorisation spéciale, ACME multi-CA avec secours, DB mutualisées/dédiées et clusters optionnels certifiés, SSH temporaire/certificats, Webmail conseillé après tests, délais/plafonds de quotas par ressource et migration présynchronisée avec réplication/bascule **conditionnelles**. [Décisions Q101–Q110](decisions-q101-q110.md). **Spécifications seulement ; aucune nouvelle fonctionnalité ni certification VM.**

**Q121–Q130 confirmées (2026-11-05)** : premier OS/WebStack **après comparaison des tests VM et sécurité** (aucun présélectionné), domaine géré via **DNS externe** et certificat ACME **HTTP-01**, rôle administrateur + gestionnaire de site, VPS observable avec paquets/mises à jour contrôlés, backup configuration panneau/fichiers PHP et restauration réellement testée, tests internes puis **bêta privée autorisée** après prérequis, licences premium transférables et récupération manuelle de serveur perdu, obligations partenaires contractuelles/alertes/retrait, responsable sécurité + suppléant/triage. [Décisions Q121–Q130](decisions-q121-q130.md) · [Qualification MVP](mvp-qualification.md). **Spécification uniquement, pas de VM/logiciel livré.**

**Q131–Q140 confirmées (2026-11-05)** : qualification VM locales/CI avec snapshots, pannes et rapport par OS ; WebStacks comparées sur charge, maintenance, reprise et critères éliminatoires ; diagnostic A/AAAA/80/HTTP-01/HTTPS ; mises à jour OS avec impact/backup/santé/reprise ; backup MVP chiffré local + destination distante facultative ; gestionnaire de site autorisé à PHP/domaines/TLS/fichiers/SFTP/backup dans son périmètre ; bêta privée par vagues/suspension/récupération ; transferts premium antifraude à validation supplémentaire selon risque ; alertes/escalade/retrait partenaires ; avis de sécurité coordonnés. [Décisions](decisions-q131-q140.md) · [Qualification MVP](mvp-qualification.md). **Tous les services restent à réaliser et tester.**

**Q141–Q150 confirmées (2026-11-05)** : VM **locales + cloud** par pilotes, runners CI et rapports communs ; budgets de performance **par classe d'application** et régressions entre versions ; assistant proposant les enregistrements DNS puis revérifiant A/AAAA/80/HTTP-01/HTTPS (**sans correction automatique**) ; politiques de mises à jour OS par serveur, multi-serveurs ultérieur ; clés de backup en coffre avec récupération hors panne commune, KMS externe/multi-autorité facultatifs ; SFTP sans shell avec révocation/expiration/quotas/audit ; bêta privée avec seuils de santé, pause et récupération ; futur Hub : preuve crypto de possession/organisation, clauses partenaires par gravité et avis de sécurité signés coordonnés selon risque. [Décisions Q141–Q150](decisions-q141-q150.md). **Aucune certification ni fonctionnalité livrée.**

**Q151–Q160 confirmées (2026-11-05)** : QEMU/KVM **local d'abord**, pilotes cloud plus tard ; matrice interne/rapports VM signés et historisés ; blocage des régressions de performances selon criticité avec dérogation auditée **sans lever les veto sécurité** ; A/AAAA contrôlés **uniquement si publiés** pour HTTP-01 ; politiques reboot OS **par serveur** avec approbation/backup/reprise ; archives chiffrées déclarées récupérables **après restauration isolée** et vérification des clés ; clés publiques SFTP gérées par site avec expiration/audit ; bêta par cohorte avec santé locale et diagnostics sous **consentements distincts** ; futur Hub : transfert risqué identifié (serveur perdu, répétition, identité) et avis signés **FR/EN + données machine**. [Décisions](decisions-q151-q160.md) · [Qualification](mvp-qualification.md). **Aucune VM/feature déclarée livrée.**

Ces priorités n'engagent aucune date ni version. Arbitrages produit nécessaires : licence du logiciel/des contributions et canal privé de sécurité autorisé. Les choix paquets/runtimes nécessitent une proposition technique étayée, pas une nouvelle architecture implicite.

## Décisions Q161–Q170 adoptées — aucune fonctionnalité livrée

**Q161 C, Q162 B, Q163 C, Q164 B, Q165 C, Q166 C, Q167 C, Q168 C, Q169 C, Q170 B** sont SPECIFIED, sans remise en cause de Q1–Q160. Les jalons R3 incluent KVM éphémère et preuves privées immuables ; R4 inclut sonde DNS externe, reprise OS bornée, restauration isolée de chaque backup, clés publiques SFTP ; bêta à cohortes privées, Hub R6 après ABI R5 pour transferts sous règles versionnées et avis JSON signés FR/EN. [Décisions](decisions-q161-q170.md) · [Tests](../13-tests-quality/mvp-gates-q161-q170.md). Aucun runtime Core n'a été importé ou testé du seul fait de cette documentation.

## R1 — Progrès vérifiable, sources applicatives toujours absentes

Un vérificateur de provenance SRC-03 en lecture seule est **implémenté** et validé sur 16 ZIP synthétiques ; voir [préflight R1](../12-development/source-archive-intake.md). Il bloque archives modifiées, chemins dangereux, liens, collisions, décompression excessive et quelques formats secrets, **sans import ni effet système**. L'archive v0.7 originale requise par [l'issue #2](https://github.com/yyogas/forgepanel/issues/2) n'est toujours pas disponible ici : **R1 source import = BLOCKED**, R2 Symfony/PG et suites R3–R6 non réalisées. Le prototype UI V3 demeure une proposition visuelle séparée, non une base Core validée.

## État de l'outillage R1 : quarantaine de provenance

Le Core contient maintenant les outils autonomes `verify_source_archive.py` et `stage_source_archive.py`, permettant de vérifier puis de **préparer sans privilèges** une copie source hors du dépôt. **33 tests unitaires synthétiques locaux ont réussi** ; la CI du commit de PR doit être vérifiée séparément. La quarantaine et son reçu `STAGED_FOR_MANUAL_REVIEW` ne sont pas un import ; **aucun Core Symfony/Go ni installateur n'a été importé ou mis en service**. L'archive Foundation v0.7 reste absente ; l'issue #2 reste ouverte. [Procédure](../12-development/source-staging.md).
