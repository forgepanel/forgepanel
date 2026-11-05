<!-- forgepanel-doc id=FP-04 revision=1 status=documented -->
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

## Contrat de cycle de vie

Un module déclare ID, version, contrat Core supporté, dépendances, capacités exigées, permissions, données/migrations, contrôles de santé et politique de suppression. Installation, activation, désactivation, mise à jour et retrait sont distincts. Une désactivation ne supprime pas silencieusement les données clientes. Un retrait exige inventaire, décision de conservation et plan de restauration.

Un échec identifie ressource et compensation restante ; les autres modules ne déduisent pas la réussite d'une simple mise en file. La configuration passe par génération et validation Core, pas par des hooks shell arbitraires. Les tests couvrent refus inter-clients, dépendances absentes, échec de mise à jour et récupération.

Les [fiches composants](components.md) décrivent les unités du prototype et le format requis. Aucun manifeste/parser ou registre de modules à l'exécution n'est implémenté dans l'archive inspectée. Un futur module est accepté seulement avec contrats, migrations, tests, supervision et désinstallation documentés dans les deux langues.
