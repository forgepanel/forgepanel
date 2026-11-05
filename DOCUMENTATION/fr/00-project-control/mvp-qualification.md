<!-- forgepanel-doc id=FP-00-MVP-QUAL revision=6 status=specified -->
# Qualification du premier ForgePanel PHP/HTTPS — Q121–Q127

[English](../../en/00-project-control/mvp-qualification.md) · [Roadmap](implementation-roadmap.md) · [Décisions Q121–Q130](decisions-q121-q130.md)

## Profil du pilote : à sélectionner, non prédéfini

La sélection du **premier OS (Q121 D)** et de la **première WebStack (Q122 D)** découle d'une comparaison réelle de VM jetables. Consigner versions, sources de paquets, installabilité, PHP-FPM, services, firewall, SELinux/AppArmor, permissions, compatibilité TLS, `.htaccess`, ports, récupération et échecs. Le profil choisi pour la première qualification n'interdit pas les autres WebStacks ou OS envisagés dans Q1–Q120.

| Cas d'essai | Preuve minimale avant qualification |
|---|---|
| Matrice OS/WebStack | VM propre, versions identifiées et commit de build, plan d'installation, compatibilité, tests HTTP/TLS/PHP, restauration et diagnostic, erreurs négatives ; décision motivée seulement **après** comparaison |
| DNS externe et HTTP-01 | Domaine de test dont le DNS est géré **à l'extérieur** ; vérification A/AAAA/CNAME et autorité ; accessible sur port 80 pour challenge HTTP-01, route vers le site et HTTPS 443 ; tester échecs, résolution erronée/IPv6 et renouvellement |
| Installation (R3) | Commande vérifiée, contrôles d'origine, privilèges système limités, préflight, étapes idempotentes et récupération en cas d'échec |
| Identité et rôles (R2/R4) | Setup sans mot de passe Linux root, administrateur local permanent et **récupération**, MFA proposé ou ignoré ; rôle gestionnaire de site aux permissions bornées ; CSRF/session/tenant refusés |
| VPS essentiel (R4) | État système/services, consommation de ressources, lecture de journaux expurgés ; **mise à jour des paquets OS contrôlée** via plan/diff, source de paquets fiable, autorisation, étape préalable, avertissement de reboot, audit et récupération |
| Site PHP (R4) | Création/admin du site, identité isolée, répertoire, version PHP compatible, listener/domain/TLS, requête HTTPS réussie et tests de refus d'accès |
| Backup v1 (R4) | Sauvegarde de la **configuration du panneau** et des **fichiers du site PHP** avec manifeste et intégrité, restauration réelle testée après modification/perte simulée ; reprise cohérente de l'état PostgreSQL du panneau si elle est requise pour que le site/identité redevienne disponible |
| Panne et récupération | Simuler conflit port, challenge inaccessible, certificat erroné, package manquant, mise à jour interrompue, corruption config, backup incomplet, utilisateur non autorisé |

**Portée initiale** : Q126 B n'impose pas encore les backups de bases de données hébergées, les mailboxes, la réplication distante ou l'immutabilité, tout en conservant les ambitions Q65/Q75/Q90. **DNS autoritatif intégré, DNS-01 et wildcard ne bloquent pas le premier site** ; leurs interfaces restent prévues après le MVP. Ne pas prétendre que ces capacités ont été testées avant la réalisation.

## Qualification VM et reprise — Q131 D, Q132 D

La **matrice de certification** repose sur **VM locales et automatisation CI** lorsque le runner sait exécuter des **VM système complètes** ; conserver un **snapshot de départ**, des tests avec **injection de pannes** (réseau, disque, installation et services), un snapshot/plan de récupération et un rapport par **OS/version/WebStack/commit**, incluant commandes, logs expurgés, `PASS`, `FAIL`, `SKIP` et limites. Une simulation Go ou un conteneur ne certifie pas systemd, firewall, SELinux/AppArmor et package managers Linux (Q131).

Pour la **première WebStack Q132**, comparer compatibilité PHP/app/`.htaccess`, sécurité TLS/listeners/isolation, **charge mesurée**, opérations de maintenance/reload et **récupération après panne**. Les critères **éliminatoires** priment sur les résultats de performance : exposition de fichiers protégés, accès inter-clients, collision IP:port, impossibilité de reprise et perte de l'accès admin. Les seuils de charge/temps ne sont pas inventés ici. Garder Q121/Q122 : **aucun OS/profil choisi avant résultats**.

## Diagnostic DNS/HTTP-01 et HTTPS — Q133 C

L'assistant vérifie la résolution **A et AAAA** des noms du site, les écarts de destinations IPv4/IPv6, le port **80 publiquement accessible**, le routage du chemin ACME **HTTP-01**, l'appartenance au vhost, puis la disponibilité HTTPS sur **443**, chaîne, nom DNS, période et renouvellement du certificat. Afficher causes/corrections possibles sans divulguer secrets ACME. L'autorité DNS reste **externe** pour le MVP ; DNS natif et DNS-01 ne bloquent pas R4.

## Mises à jour, sauvegardes et droits du gestionnaire — Q134–Q136

- **Q134 C** : mises à jour OS avec prévisualisation des paquets/impact, autorisation par rôle, créneau de maintenance, **sauvegarde récupérable**, état de tâche/éventuel reboot, vérification des services et **procédure de récupération**. Refuser commandes root libres.
- **Q135 B** : sauvegardes **locales chiffrées**, avec **destination distante facultative** si un pilote est qualifié ; inclure configuration du panneau et **fichiers PHP du site**, tests de restauration réels et clés accessibles en secours. Prévoir reprise cohérente de PostgreSQL du panneau si nécessaire. Ne pas prétendre que la copie locale résiste à la perte du disque ; la cible distante/3-2-1 reste extensible.
- **Q136 C** : rôle **gestionnaire de site** limité à ses sites : lecture d'état, PHP/domaines/TLS/fichiers, **SFTP et sauvegarde/restauration** sous quotas, droits et politiques admin. Tester **un SFTP réel autorisé sur le bon site et refusé sur un site tiers**, puis les refus de changement de quotas, paquets OS et actions root ; appliquer Q47 pour TLS/restauration.

## Compléments de qualification Q141–Q146

**Q141 D** : le pilote de qualification fournit des adaptateurs VM **locales et cloud**, les runners CI réellement compatibles et un **rapport commun versionné** par OS/arch/WebStack/commit, snapshots, simulations de pannes et restauration. Un test ignoré `SKIP` n'est pas une certification. Ne pas déclarer une VM système testée en se fondant seulement sur des conteneurs.

**Q142 D** : définir des **budgets de performance configurables par classe d'application**, faire des mesures reproductibles de débit/latence/erreurs/CPU/RAM et suivre les **régressions entre versions**, avec baseline et environnement identifiés. Les critères éliminatoires de sécurité Q132 (fuite tenant, `.htaccess`, collision de port ou absence de reprise) passent avant toute performance. Aucun seuil chiffré n'est fixé.

**Q143 C** : assistant proposant **les enregistrements DNS externes attendus**, diagnostic A/AAAA (dont IPv6), port **80**, HTTP-01, port **443** et validité du certificat, puis **revérification** après correction. **Ne pas modifier automatiquement le DNS** : la décision C retient aide et retest, non l'option D d'intégration fournisseur.

**Q144 D** : règles de mises à jour OS **par serveur** : inventaire, origine des paquets, créneau, plan d'impact, autorisation, sauvegarde récupérable, application, reboot si nécessaire, santé et récupération. **Multi-serveurs progressif plus tard**, selon Q67/Q77, sans bloquer le MVP.

**Q145 D** : sauvegarde **locale chiffrée** Q135 avec coffre de secrets, copie de récupération protégée **hors domaine de panne**, restauration sur VM distincte, **KMS externe facultatif** et plusieurs gardiens/autorités lorsque politique autorise. Tester absence/perte de clé : une sauvegarde chiffrée irrécupérable est un échec ; pas de dépendance obligatoire au Hub.

**Q146 C** : SFTP **sans shell par défaut**, compte/chemin site isolé, accès expirables/révocables, quotas appliqués et audit, tests de traversée/symlink et refus inter-tenants. Ces contrôles doivent être exécutés sur le serveur réel, pas uniquement simulés dans l'UI.

[Décisions Q141–Q150](decisions-q141-q150.md) · [Contrats techniques](../02-architecture/certification-backup-security.md). **Aucune preuve d'exécution VM n'est créée par ce document.**

## Choix Q151–Q158 — preuve de fonctionnement du MVP

**Q151 A** : démarrer avec **QEMU/KVM local** pour obtenir une vraie VM système et des snapshots ; la couche pilote Q141 gardera les VM cloud pour plus tard. Ne pas marquer le job CI `PASS` si le runner ne dispose pas de KVM. **Q152 C** : exiger rapport **signé**, provenance de l'image/build, snapshots et **historique de résultats** (matrice interne). Une signature ne suffit pas à prouver la sécurité.

**Q153 C** : définir budgets de latence/erreurs/ressources **par catégorie d'application** ; bloquer une régression selon criticité et seuils, avec exception de **performance uniquement** validée, bornée et auditée. Une fuite inter-tenants, un défaut `.htaccess`, un conflit de listener ou un échec de restauration Q132 restent **inacceptables**, sans dérogation de score.

**Q154 C** : pour ACME **HTTP-01**, contrôler **uniquement les familles IP A/AAAA réellement publiées**. A seul : tester IPv4 et ne pas exiger AAAA ; AAAA seul : tester IPv6 ; A+AAAA : vérifier les deux sur port 80 et HTTP-01 avant le HTTPS 443. L'assistant propose les corrections puis revérifie **sans écriture DNS automatique**.

**Q155 C** : politiques de **reboot par serveur** avec approbation autorisée, plan d'impact, sauvegarde utilisable, health-check après redémarrage et procédure de récupération. L'orchestration multi-serveurs est ultérieure. **Q156 C** : sauvegarde locale chiffrée Q135 et **clé de récupération exportée de manière sûre**, accès vérifié périodiquement et **restauration déchiffrée en VM isolée** avant le statut « récupérable ». KMS externe/multi-gardiens demeurent facultatifs.

**Q157 C** : sur le site autorisé, gestionnaire capable de **déposer/révoquer ses clés publiques SFTP** dans les limites du compte, expiration, droits par site, quota et audit ; action sensible revalidée, aucun shell ni clé privée collectée. Tester accès à son site et refus inter-tenants **réellement**.

**Q158 C** : après validation interne, la bêta privée Q137/Q147 repose sur rapports manuels, **santé locale** et diagnostics **minimisés avec consentements distincts Q6**, seuils par cohorte et plan de suspension/récupération. La bêta continue de fournir des fonctions Core sans exiger le partage de données diagnostics.

[Décisions](decisions-q151-q160.md) · [Contrats d'implémentation](../02-architecture/qualification-and-security-contracts.md). **Aucun benchmark, VM ou restore réel n'est déjà exécuté par cette documentation.**

## Bêta privée Q127 B — passage après tests internes

Ordre : VM internes isolées et tests négatifs → revue des résultats/risques → correction des défauts bloquants → vérification des licences/obligations de distribution pour **chaque destinataire externe**, documents de sécurité et contact privé fonctionnel → validation propriétaire de la liste des testeurs et des limites → ouverture d'une **bêta privée** avec consignes de restauration, remontée d'incidents, retrait et arrêt de test.

La bêta privée n'est ni une publication stable, ni une exemption aux obligations de la licence applicable. Ne pas utiliser l'accès bêta pour demander des identifiants root ou des données réelles de tiers sans consentement et mesures adaptées.

## Responsabilités

Le responsable sécurité et le **suppléant** (Q130 C), leurs accès, procédure de triage, escalade, journaux et notifications coordonnées doivent être **effectivement nommés et vérifiés** avant diffusion. Les deux voies Q118 (GitHub privé + email sécurité dédié) doivent être configurées/testées ; n'inventer ni noms, adresses, garanties de réponse ou rôles opérationnels.

**État : plan de qualification uniquement. Aucun candidat OS, WebStack, fournisseur ACME ou équipe de bêta n'est encore validé.**

## Qualification opérationnelle complémentaire — Q161–Q168

Sur VM **QEMU/KVM locale éphémère et isolée** Q161, fixer image/commit/ressources et nettoyer les secrets runner ; archiver les rapports de qualification **internes signés** dans un espace privé immuable à historique et droits contrôlés Q162. Les dérogations Q163 concernent exclusivement les budgets de **performance non critiques**, avec séparation des approbateurs, portée/expiration/revue et **veto Q132 irrévocable**.

**DNS Q164 B** : vérifier chaque famille A/AAAA effectivement publiée depuis le serveur **et une sonde indépendante extérieure** pour 80/HTTP-01 et TLS, avec protection anti-SSRF et refus du faux succès si sonde indisponible. **Reprise OS Q165 C** : fonctions non destructives spécifiquement autorisées, retry plafonné, checkpoints et approbation des actes sensibles. **Backup Q166 C** : chaque archive restaurée sur environnement isolé avant de recevoir la mention récupérable ; vérifier clé exportée protégée et accès périodique, ajouter tests fonctionnels profonds et exercices perte hôte/clé selon criticité. **SFTP Q167 C** : possession de la clé publique, algorithmes autorisés, expiration/rotation, périmètre site et audit. **Bêta Q168 C** : diagnostics par finalité facultatifs et agrégats de cohorte empêchant la réidentification. [Tests planifiés](../13-tests-quality/mvp-gates-q161-q170.md) — **aucun test réel exécuté**.
