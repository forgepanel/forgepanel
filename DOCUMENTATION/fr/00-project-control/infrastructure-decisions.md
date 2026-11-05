<!-- forgepanel-doc id=FP-00-INFRA revision=1 status=specified -->
# Décisions Q61–Q70 — Infrastructure, administration et interface

[English](../../en/00-project-control/infrastructure-decisions.md) · [Décisions précédentes](commerce-identity-release-policy.md) · [Registre ADR](decisions.md)

## Source et statut

Le propriétaire a confirmé les **dix arbitrages Q61–Q70 le 5 novembre 2026**. Ils s'ajoutent sans remplacement aux choix Q1–Q60 et à la sécurité du Core gratuit, indépendant du Hub. Ce texte est **une spécification** : aucune installation multi-OS, distribution signée, cluster, service DNS/mail, sauvegarde ou interface avancée n'est certifiée en production.

| ID | Choix | Portée fonctionnelle et contraintes |
|---|---|---|
| Q61 C | Builds CI/CD signés avec **clés protégées**, **anti-rétrogradation** et approbations | Publication contrôlée par rôles, artefacts/métadonnées immuables, racines de confiance, rotation/révocation ; la signature ne garantit pas la qualité. |
| Q62 C | **Installateur universel + dépôts DEB/RPM signés** | Commande initiale simple, vérification de la provenance avant opérations privilégiées, préflight, installation idempotente, migration/reprise et diagnostic. Cibles Debian 12/13, Ubuntu 24.04/26.04 LTS, AlmaLinux 9/10 après tests VM. |
| Q63 C | **DNS local + fournisseurs externes par pilotes** | Choix par zone ou délégation, vérification d'autorité DNS, pilotes avec capacités, propagation/états et prévention des propriétaires concurrents. Le logiciel local (p. ex. PowerDNS) n'est pas encore choisi. |
| Q64 C | **Messagerie native + fournisseurs externes** | Boîtes, domaines, routage, SMTP/IMAP, DKIM/SPF/DMARC, TLS, quotas et état des fournisseurs ; mécanisme anti-spam, vérification DNS et réputation à planifier. Backend local non figé. |
| Q65 D | **Sauvegardes multi-destinations, chiffrement, tests de restauration, réplication distante, immutabilité et reprise avancée** | Politiques par ressource, copies chiffrées, protection contre suppression par compte compromis, rétention et procédures DR testées ; RPO/RTO mesurés ultérieurement. |
| Q66 C | **Réauthentification des actions sensibles + approbation supplémentaire configurable** | MFA administrateur reste facultatif ; politiques de réauthentification, séparation des tâches quand plusieurs admins, contrôle des permissions, traçabilité et procédure de secours auditée. |
| Q67 D | **Agents multi-serveurs, groupes/politiques, orchestration, haute disponibilité, clustering et reprise** | Gestion centralisée, états voulus/observés, coordination, quorum/fencing selon besoin, tolérance aux partitions et restauration. Le clustering est une **cible progressive**, non un prérequis à la v1. |
| Q68 C | **Supervision locale, email/webhooks, intégrations externes, règles d'alerte configurables** | Metrics, health, seuils, destinataires et acquittements configurables par rôle ; pas de secrets/clients exportés implicitement. L'analyse prédictive n'est pas sélectionnée. |
| Q69 D | **Choix du profil à l'installation et par site ; plusieurs frontaux selon IP/port** | Nginx, Apache, Caddy, PHP-FPM et FrankenPHP selon capacités ; propriété exclusive des listeners, TLS/routage, contrôle de `.htaccess` et validation/reload avant activation. |
| Q70 D | **Une marque par organisation avec éditeur visuel, widgets et navigation personnalisables** | Design system Symfony Twig/UX, thèmes/aperçu/historique et permissions ; blocs et routes allowlistés, pas d'injection libre de code dans le Core. |

## Administrabilité et priorités

L'objectif est **tout administrable quand cela peut l'être sans franchir les limites de confiance**. Chaque paramètre possède type, valeur effective, niveau de surcharge, dépendances, autorisation, audit, contrôle de compatibilité et classe d'impact. Les changements sensibles suivent la décision Q47 : **PLAN → VALIDATE → SNAPSHOT → APPLY → VERIFY → RECOVER si besoin**. Les actions visuelles simples peuvent être immédiates et annulables.

**Phase 1** : fondations, CLI, installateur signé, administration VPS + hébergement mutualisé, profils web, DNS/mail et sauvegarde selon besoins minimaux testés. **Phase 2** : pilotes externes avancés, monitoring et UX personnalisable. **Phase 3+** : orchestration/HA/DR et extensions multi-serveurs selon ressources et preuves. L'ordre exact des fonctions au sein des phases est ouvert ; aucune des dix décisions ne garantit leur disponibilité simultanée au premier lancement.

## Frontières de responsabilité Core / Hub

Le **Core** gère OS, ports, services DNS/mail locaux ou distants, WebStacks, contrôles d'accès, agents, monitoring local, sauvegardes/restauration et application de mises à jour. Le **Hub privé**, facultatif, peut gérer catalogue de versions et artefacts signés, campagnes progressives et annonces liées aux installations volontairement enregistrées. Le Hub ne commande pas un shell root chez les clients ; le Core reste fonctionnel hors ligne. Les communications Hub, métriques et diagnostics restent séparées selon Q6.

Les modules DNS/mail et les pilotes externes doivent pouvoir être désactivés sans détruire les données existantes. Une compatibilité annoncée requiert un test par OS, version, WebStack et pilote pertinent.

## Critères de validation futurs

- **Chaîne de publication Q61–Q62** : signatures falsifiées/révoquées, versions anciennes, paquets non disponibles sur un OS, coupure pendant l'installation, relance idempotente, blocage des portes d'approbation.
- **DNS/mail Q63–Q64** : zone possédée par fournisseur inattendu, propagation partielle, enregistrement incohérent, relais ouvert, certificats et isolation de domaines.
- **Sauvegardes Q65** : restauration réelle et clés, suppression/compromission, copies distantes indisponibles, test d'immutabilité et redémarrage documenté.
- **RBAC Q66** : approbation contournée, compte unique sans second approbateur, réauthentification expirée, récupération locale.
- **Multi-serveurs Q67** : partition réseau, double agent, reprise de leader, incohérences, garanties de quorum et tests sur VM.
- **Monitoring Q68** : alertes répétées, boucle de notifications, absence de secrets et consentement aux exportateurs.
- **Web Q69** : collision IP:port, TLS, session admin, règles Apache `.htaccess` non contournées, restauration de génération.
- **Design Q70** : permission refusée, composants invalides, XSS, contraste, accessibilité, sauvegarde/révision et une seule marque par organisation.

## Non décidés à ce jour

Choix concrets des fournisseurs DNS/mail/stockage/monitoring, moteurs et clés de signature, mécanisme d'approbation par défaut, topologie exacte de cluster, RPO/RTO, nombre de copies, stratégie d'installation automatique, contenu prédéfini des widgets et limites de personnalisation. **Aucune valeur, fournisseur ou certification n'est présumé.**
