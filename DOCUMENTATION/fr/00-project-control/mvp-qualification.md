<!-- forgepanel-doc id=FP-00-MVP-QUAL revision=3 status=specified -->
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

## Bêta privée Q127 B — passage après tests internes

Ordre : VM internes isolées et tests négatifs → revue des résultats/risques → correction des défauts bloquants → vérification des licences/obligations de distribution pour **chaque destinataire externe**, documents de sécurité et contact privé fonctionnel → validation propriétaire de la liste des testeurs et des limites → ouverture d'une **bêta privée** avec consignes de restauration, remontée d'incidents, retrait et arrêt de test.

La bêta privée n'est ni une publication stable, ni une exemption aux obligations de la licence applicable. Ne pas utiliser l'accès bêta pour demander des identifiants root ou des données réelles de tiers sans consentement et mesures adaptées.

## Responsabilités

Le responsable sécurité et le **suppléant** (Q130 C), leurs accès, procédure de triage, escalade, journaux et notifications coordonnées doivent être **effectivement nommés et vérifiés** avant diffusion. Les deux voies Q118 (GitHub privé + email sécurité dédié) doivent être configurées/testées ; n'inventer ni noms, adresses, garanties de réponse ou rôles opérationnels.

**État : plan de qualification uniquement. Aucun candidat OS, WebStack, fournisseur ACME ou équipe de bêta n'est encore validé.**
