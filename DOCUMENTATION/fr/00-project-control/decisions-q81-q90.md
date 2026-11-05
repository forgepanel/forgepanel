<!-- forgepanel-doc id=FP-00-Q81-90 revision=1 status=specified -->
# Arbitrages Q81–Q90 — Hébergement, sites et récupération

[English](../../en/00-project-control/decisions-q81-q90.md) · [Registre](decisions.md) · [WebStack par site](../02-architecture/site-webstack-advisor.md) · [Cycle des sites](../02-architecture/website-lifecycle.md)

## Décisions du propriétaire — 5 novembre 2026

Les dix réponses **Q81 C, Q82 D, Q83 C, Q84 C, Q85 C, Q86 D, Q87 B, Q88 C, Q89 C, Q90 D** sont confirmées et s'ajoutent à Q1–Q80. Elles sont **spécifiées seulement**, aucun module d'hébergement opérationnel ou tests VM/navigateur n'est démontré. Le Core gratuit AGPL reste indépendant du Hub et des abonnements. MFA administrateur facultatif, une seule marque par organisation, réauthentification sensible et plan de récupération Q47 demeurent applicables.

| ID | Décision confirmée | Exigences et limites |
|---|---|---|
| Q81 C | **Conseiller WebStack selon application, .htaccess, PHP, OS, isolation, sécurité, ressources et listeners** | Recommendation **par site** (Q79), raisons traçables, profils incompatibles refusés, pas de promesse de performance sans mesures. |
| Q82 D | **Changement de WebStack avec prévisualisation, sauvegarde, maintenance/notifications, test temporaire ou bascule progressive si faisable** | Plan à autoriser et versionner ; route de test isolée, TLS/contrôle d'accès conservés, cutover/recovery sans perturber les autres sites. La bascule progressive n'est pas toujours possible et zéro interruption n'est pas garanti. |
| Q83 C | **PHP par site : versions, extensions, paramètres PHP-FPM, quotas et ressources** | Pools Unix isolés, sécurité des directives, règles de versions et héritage plan/compte/site. Le PHP du panneau reste séparé. Un site n'obtient pas des droits système par modification de PHP-FPM. |
| Q84 C | **ACME automatique + certificats personnalisés + DNS-01 + wildcards + renouvellement et alertes** | Possession du domaine, DNS/ACME compatibles, stockage protégé des clés et politique de renouvellement ; les wildcards nécessitent un challenge admissible, typiquement DNS-01. |
| Q85 C | **Fichiers/SFTP + Git Deploy + staging/preview + sauvegarde et récupération contrôlée** | Déploiement versionné et permissionné ; secrets, migration SQL et données distingués du code. Blue-green/canary et pipelines avancés ne sont **pas décidés** ici. |
| Q86 D | **MariaDB/MySQL, PostgreSQL, Redis/Valkey facultatifs par pilotes** | MariaDB/MySQL et PostgreSQL pour les bases ; Redis/Valkey pour cache/queues si capacités. Comptes/quotas/scopes isolés ; PostgreSQL du Core ne devient pas la base client par défaut. |
| Q87 B | **Gestionnaire de fichiers web + SFTP + SSH réservé aux comptes autorisés** | Identité OS par tenant, chemins sécurisés, quotas, audit et règles SSH limitées. **Aucun terminal web** demandé par ce choix. |
| Q88 C | **SPF/DKIM/DMARC/TLS + antispam/antivirus + webmail/quarantaine/règles/rapports par domaine** | Protections et UI bornées par propriétaire du domaine/boîte, secrets chiffrés, isolation ; disponibilité du backend mail à confirmer. Archivage légal avancé non choisi. |
| Q89 C | **Plans et quotas (stockage, domaines, emails, DB, CPU/RAM/processus/PHP) avec héritage, alertes et consommation** | Politiques parentales non contournables, consommation effective/limites soft-hard, transparence du calcul et refus de dépassement côté service/agent. |
| Q90 D | **Restaurations complètes/sélectives, tests de récupération, clonage staging et restauration entre environnements contrôlés** | Consentement du propriétaire, planification, identité/secret/environnement cible distincts, aucune copie automatique de credentials production ; protection des données et bases avant overwrite. |

## Modèle administrable et dépendances

`organization → hosting plan → account → website/application` gouverne versions PHP, extensions autorisées, quotas, WebStack, certificats, storage, bases, accès fichiers et restauration. Chaque paramètre déclare valeur effective/origine, permission et capacité OS/service. Une capacité non disponible est signalée, non simulée.

Le **Configuration Engine** applique les modifications à impact : `PLAN → VALIDATE → SNAPSHOT → STAGE → APPLY → HEALTH CHECK → FINALIZE / RECOVER`. La configuration Linux n'est pas une transaction atomique ; les effets sur bases ou données peuvent nécessiter une intervention manuelle. La priorité Q54 reste **hébergement mutualisé + VPS**, puis fonctions avancées par phases. Les services optionnels ne sont pas tous installés sur chaque serveur.

## Sécurité et séparation Core/Hub

Les contenus clients (fichiers, messages, données, clés TLS/SSH, dumps SQL et credentials) demeurent dans le **Core ou le fournisseur explicitement choisi**. Le Hub privé peut publier des recettes/plugins compatibles et des informations de version, **pas lire ni administrer les données des sites**. Les droits commerciaux premium ne remplacent ni RBAC du Core ni permissions Linux. Un quota ou un déploiement ne doit pas permettre de sortir du tenant.

## Vérifications requises

- Recommandations/routage par site, besoins `.htaccess`, listeners, bascule temporaire/progressive, échec pendant cutover et récupération.
- PHP 8.x validé par OS et FPM pools séparés, directives bloquées, isolation et quotas réellement appliqués.
- ACME DNS-01/wildcard, challenge échoué, clé divulguée, renouvellement et certificat importé.
- Git Deploy, staging, rollback de code distinct des migrations SQL non réversibles et protection des secrets.
- MariaDB/MySQL, PostgreSQL, Redis/Valkey : scopes, sockets, permissions, backup/restore et absence d'accès transversal.
- Gestionnaire de fichiers, SFTP et SSH : chemins symlink/traversal, permissions et comptes suspendus.
- Mail : relai ouvert, SPF/DKIM/DMARC, quarantaine privée et webmail par boîte/domaine.
- Plans : héritage, limites enfants, consommation concurrente, dépassement et alertes.
- Clonage/restauration : base cohérente, credentials renouvelés, DNS sortant désactivé en staging, données sensibles et rollback.

## Encore ouverts

Choix exacts de fournisseurs DNS, ACME, storage et webmail ; version PHP du panneau et politique EOL des PHP clients ; prestataire Git et clés SSH d'accès ; pilote base par défaut ; mécanismes d'isolation/quotas certifiés ; calendrier et limites de stockage ; traitement des données personnelles et courriels lors du clonage. Ces points feront l'objet de choix ultérieurs : aucune valeur implicite n'est décidée.
