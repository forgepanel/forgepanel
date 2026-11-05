<!-- forgepanel-doc id=FP-04 revision=6 status=documented -->
# Catalogue des modules natifs

[English](../../en/04-modules/README.md) · [Index](../README.md)

## Sens de « natif »

Un module natif appartient au produit revu et utilise les contrats du Core. Son activation peut être facultative, mais l'hébergement essentiel ne dépend pas de code tiers de marketplace. Un service est le logiciel Linux piloté par un module ; une interface est son point d'entrée utilisateur. Ces notions ne sont pas interchangeables.

| Module | Dépendances et périmètre | Preuve actuelle |
|---|---|---|
| Identity / Authorization | État Core, sessions, permissions, périmètre du compte | Prototype d'enrôlement initial ; RBAC complet absent |
| Infrastructure / WebStack | Adaptateurs OS, listeners, pilotes de services | Identifiants de planification uniquement |
| Hosting / Websites / Domains | Identité, quotas, WebStack, TLS | Prévu ; aucun provisionnement de site |
| DNS / Mail / Database | Domaines, adaptateurs, secrets, sauvegardes | Uniquement les choix `dns`, `mail`, `database` |
| Files / SFTP | Identité client, chemins sûrs, quotas | Choix `sftp` ; aucun code de file manager fourni |
| Backup / Restore | Stockage, secrets, cohérence des ressources | Choix `backup` ; aucun moteur de sauvegarde |
| Monitoring / Jobs / Updates | Observabilité, exécution durable, racines de confiance | Doctor en lecture seule et prototype de vérification de signatures |

## Décisions Q63–Q68 et responsabilités natives

La cible prévoit pilotes DNS local/externe (Q63), mail natif/externe (Q64), sauvegardes chiffrées répliquées/immuables avec restauration (Q65), monitoring/alertes intégrables (Q68) et agents multi-serveurs/HA (Q67). Les modules partagent des contrats de capacités, autorisations et états ; aucune fonction n'est installée automatiquement sans choix/prérequis. La HA viendra progressivement, pas nécessairement avec le premier lot d'hébergement. [Architecture](../02-architecture/service-drivers-and-ha.md).

## Sélection et adaptation des modules (Q72–Q79)

L'installateur peut détecter/adopter des services présents après inventaire, permission et plan de récupération (Q72), mais ne prend jamais automatiquement possession de fichiers externes. DNS local multi-pilotes conseillé par tests (Q73) ; premier mail natif Postfix/Dovecot et services/relais externes (Q74) ; politiques 3-2-1 avec exercices de restauration (Q75) ; connecteurs Prometheus/OpenTelemetry (Q78). Pour chaque site, recommander une WebStack sans l'imposer, puis permettre un **changement contrôlé** plus tard (Q79) via le Core. [Détails](../00-project-control/decisions-q71-q80.md).

## Nouveaux modules et capacités Q81–Q90

Le périmètre d'hébergement prévoit : conseiller WebStack et changement sécurisé, PHP-FPM version/extensions/quotas **par site**, ACME et certificats importés, Git Deploy avec staging, pilotes MariaDB/MySQL et PostgreSQL, cache Redis/Valkey facultatif, gestionnaire de fichiers/SFTP/SSH limité, webmail et quarantaine par domaine, plans/quotas hérités, restauration sélective et clonage vers staging. Les capacités restent facultatives selon le serveur et le plan ; la souscription commerciale Hub n'est pas requise pour la sécurité de base. Les services actuels ne sont **pas implémentés**. [Architecture](../02-architecture/website-lifecycle.md).

## Modules retenus dans Q91–Q100

La gestion de sites visera : **catalogue PHP maintenu avec alertes EOL et migration** (Q91), **pools PHP-FPM isolés par site et profils Linux renforcés** (Q92), **Git Deploy manuel et webhook validé** (Q93), staging avec contrôle des données/secret/rétention (Q94), **ACME multi-CA/DNS-01** (Q95), moteurs SQL/cache multiples séparés par compte (Q96), SSH limité par plan avec révocation/expiration (Q97), webmail sélectionnable selon fournisseur (Q98), quotas avec alertes/grâce et rallonge autorisée (Q99), et migration entre serveurs avec staging/sauvegarde/récupération (Q100). Le Core n'inclut pas de terminal web par implicite et ne stocke pas les données de site dans Hub. [Décisions](../00-project-control/decisions-q91-q100.md).

## Politiques modules Q101–Q110

Les modules devront publier leurs capacités par OS/plan/site : dérogations PHP EOL de durée bornée avec migration (Q101), profils d'isolation Linux certifiés (Q102), Git Deploy manuel/webhook et approbations par environnement (Q103), staging privé nécessitant parfois une approbation spéciale (Q104), ACME multi-CA et secours (Q105), bases mutualisées/dédiées avec réplication **optionnelle certifiée** (Q106), SSH temporaire/certificats selon fournisseur (Q107), moteur Webmail conseillé après qualification (Q108), grâces de quota par ressource (Q109), migration présynchronisée et bascule avancée conditionnelle (Q110). Le Core reste propriétaire de l'exécution et du stockage client. [Décisions](../00-project-control/decisions-q101-q110.md).

## Contrat de cycle de vie

Un module déclare ID, version, contrat Core supporté, dépendances, capacités exigées, permissions, données/migrations, contrôles de santé et politique de suppression. Installation, activation, désactivation, mise à jour et retrait sont distincts. Une désactivation ne supprime pas silencieusement les données clientes. Un retrait exige inventaire, décision de conservation et plan de restauration.

Un échec identifie ressource et compensation restante ; les autres modules ne déduisent pas la réussite d'une simple mise en file. La configuration passe par génération et validation Core, pas par des hooks shell arbitraires. Les tests couvrent refus inter-clients, dépendances absentes, échec de mise à jour et récupération.

Les [fiches composants](components.md) décrivent les unités du prototype et le format requis. Aucun manifeste/parser ou registre de modules à l'exécution n'est implémenté dans l'archive inspectée. Un futur module est accepté seulement avec contrats, migrations, tests, supervision et désinstallation documentés dans les deux langues.
