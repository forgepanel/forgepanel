<!-- forgepanel-doc id=FP-00-Q71-80 revision=2 status=specified -->
# Arbitrages Q71–Q80 — Exploitation configurable et WebStacks par site

[English](../../en/00-project-control/decisions-q71-q80.md) · [Registre](decisions.md) · [Architecture WebStack](../02-architecture/site-webstack-advisor.md)

## Décisions confirmées (5 novembre 2026)

Ces décisions **complètent Q1–Q70 sans les remplacer**. Il s'agit d'une politique produit et d'exigences **spécifiées, non implémentées**. Le Core AGPL gratuit demeure autonome sans Hub ; MFA administrateur facultatif, une marque par organisation et contrôles Q47 restent inchangés.

| ID | Choix | Contrat / limites |
|---|---|---|
| Q71 C | **KMS/HSM ou service sécurisé de clés + métadonnées anti-rétrogradation et rotation** | Chaîne de confiance racine, clés séparées par rôle, signatures, vérification hors ligne, délégation/rotation/révocation contrôlée. Le choix de fournisseur et le protocole exact restent ouverts. |
| Q72 C | **Installation vierge ou adoption contrôlée de services existants** | Détection sans mutation, inventaire propriétaire des ressources, plan et conflits, sauvegarde, consentement explicite avant prise en charge, test santé et récupération. Refuser l'adoption non maîtrisée. |
| Q73 D | **DNS multi-pilotes ; moteur local recommandé après tests** | Détecter OS/capacités et besoins des zones ; comparer moteurs et providers sans figer un produit. Migration de zone/délégation et DNSSEC selon capacités. |
| Q74 C | **Postfix + Dovecot en premier pilote ; fournisseurs et relais externes** | Mail local contrôlé et services externes interchangeables ; DNS (MX, SPF, DKIM, DMARC), TLS, antispam, réputation et secrets à valider. |
| Q75 C | **Profil 3-2-1 + restaurations testées et réplication configurable** | Plusieurs copies, emplacements et médias, copie distante, idéalement immuable ; contraintes matérielles, budget, RPO/RTO et tests de restauration exposés. |
| Q76 C | **Approbation configurable par action + mode de secours sécurisé** | Réauthentification selon risque, double approbation lorsque requise, séparation des acteurs, piste d'audit ; récupération locale si approbateur indisponible sans supprimer les traces. MFA reste optionnel. |
| Q77 D | **Multi-serveurs d'abord, puis HA et orchestrateurs externes par étapes** | Agent Go et contrôleur, groupes, politiques, états désirés/observés ; extensions HA et intégrations seulement après tests quorum/partitions/reprise. |
| Q78 C | **Prometheus et OpenTelemetry via adaptateurs** | Métriques, traces/événements supportés par capacités, règles d'export et destinataires configurables. Pas de collecte de données clientes ni export Hub sans consentement explicite. |
| Q79 D + précision | **Recommandation initiale par site ; sélection libre et changement ultérieur** | Ne pas imposer le même profil aux sites ; afficher raisons, prérequis, incompatibilités et impact. Le changement d'un site passe par un plan vérifié et récupérable, pas par un simple toggle. |
| Q80 C | **Widgets officiels/partenaires + widgets personnalisés déclaratifs** | Manifeste/version, sources de données autorisées, RBAC, contrôle des requêtes et rendu sûr. Aucun widget ne peut exécuter librement PHP/JS/shell ni lire des secrets d'autres tenants. |

## Précisions Q81–Q90 (sans modification de Q71–Q80)

Le choix Q79 d'une WebStack conseillée à la création de **chaque site** est désormais complété par Q81 C (application, PHP, `.htaccess`, OS, isolation, sécurité, ressources et listeners) et Q82 D (prévisualisation, maintenance/notifications, route de test ou bascule progressive **si possible**, avec sauvegarde/récupération). Les options PHP, TLS, Git, données, SSH, email, quotas et restauration sont définies dans les [décisions Q81–Q90](decisions-q81-q90.md). Aucun changement de l'ADR précédent ne promet de zéro interruption.

## Règles communes à tous les paramètres

La configuration dépend de la capacité OS réelle, de la politique globale et du périmètre organisation/plan/compte/site. Les préférences visuelles non sensibles peuvent être instantanées ; tout changement sur service, ports, identité, stockage ou réseau suit Q47 : **PLAN → VALIDATE → SNAPSHOT/BACKUP → APPLY → HEALTH CHECK → COMMIT ou RECOVER/COMPENSATE**. Les échecs partiels et migrations non réversibles doivent être explicités ; le retour arrière universel n'est pas garanti.

## Priorités sans promesse de livraison simultanée

1. **Fondation** : Core Symfony/Go/PostgreSQL, installateur, comptes, VPS, premiers sites, configuration sûre, profils web et outils de récupération.
2. **Services** : mail Postfix/Dovecot, DNS pilote recommandé selon qualification, connecteurs externes, sauvegarde 3-2-1, restauration et métriques pilotables.
3. **Écosystème** : HA, orchestrateurs, widgets partenaires, distribution et instrumentation complètes, selon preuves et capacités.

L'ordre exact de certification de tous les couples OS/services reste à établir. Q73 ne sélectionne pas un moteur DNS local définitif ; Q71 ne choisit pas un fournisseur KMS/HSM ; Q75 ne fixe pas la fréquence ni le prestataire de stockage.

## Validation attendue

- KMS/rotation : clés périmées, signatures invalides, rollback, publication pendant rotation.
- Adoption : serveur préexistant, perte réseau, conflit de listener, configuration externe non écrasée, récupération.
- Mail/DNS : délégation, relai ouvert, doublons, TLS/DNSSEC, perte de provider.
- Backup : 3-2-1 annoncé vs copies réelles, restauration isolée et clés, immutabilité et réplication.
- Approbation : compte unique, approbateur indépendant, mode secours audité, CSRF et attaques par contournement.
- HA/monitoring : partition de réseau, données exportées, version agent, métriques manquantes.
- WebStack : profil conseillé et refus incompatible, `.htaccess`, isolation PHP, listeners, TLS et reprise après changement.
- Widgets : isolation tenant, XSS, sources de données et permissions.

[Politique de recommandation et changement WebStack par site](../02-architecture/site-webstack-advisor.md) · [Configuration Engine](../02-architecture/configuration-engine.md) · [Décisions Q61–Q70](infrastructure-decisions.md)
