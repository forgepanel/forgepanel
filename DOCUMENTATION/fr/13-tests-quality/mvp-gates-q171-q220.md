<!-- forgepanel-doc id=FP-13-Q171-220 revision=1 status=specified -->
# Q171–Q220 — matrice des tests liés aux décisions

[English](../../en/13-tests-quality/mvp-gates-q171-q220.md) · [Index QA](README.md) · [Décisions](../00-project-control/decisions-q171-q220.md)

**PLANNED — NON EXÉCUTÉS.** Les cinquante orientations produit approuvées génèrent cinquante critères d'acceptation. Ce sont des tests à réaliser, pas des PASS ; ils ne remplacent ni la CI documentaire ni les 32 tests VM App Center prévus. [Registre des cas](../../evidence/acceptance-q171-q220-v1.json).

| Cas | Choix | Objectif de validation | Statut |
|---|---|---|---|
| ACCEPT-Q171-01 | D | Seules les recettes natives approuvées et compatibles entrent progressivement au catalogue | PLANNED |
| ACCEPT-Q172-01 | D | Création/suspension/réessai API sous scopes typés, idempotence, audit et refus inter-tenant | PLANNED |
| ACCEPT-Q173-01 | D | Scanner multiengine borné, quarantaine/réintégration, faux positifs, aucune suppression arbitraire | PLANNED |
| ACCEPT-Q174-01 | C | WAF candidat en détection avant tests de blocage et récupération qualifiée | PLANNED |
| ACCEPT-Q175-01 | D | Refus inter-portails routes/cookies/sessions/API et isolation des thèmes/droits | PLANNED |
| ACCEPT-Q176-01 | D | R4 PHP/HTTPS vérifié avant natif, puis conteneurs par jalons qualifiés distincts | PLANNED |
| ACCEPT-Q177-01 | D | Catégories administrables sans publier de recette incompatible/non revue | PLANNED |
| ACCEPT-Q178-01 | D | Import local signé et partenaire refusé sans revue manuelle par version | PLANNED |
| ACCEPT-Q179-01 | D | Assistant simple/avancé soumis à droits, backup et préflight avant application | PLANNED |
| ACCEPT-Q180-01 | D | Override inférieur incapable de dépasser les plafonds de sécurité ni d'effacer historique | PLANNED |
| ACCEPT-Q181-01 | D | Moteur SQL incompatible refusé, comptes et autorisations par tenant | PLANNED |
| ACCEPT-Q182-01 | D | Version épinglée, EOL et migration par site ; refus de version non prise en charge | PLANNED |
| ACCEPT-Q183-01 | D | Fenêtres, staging et approbations respectés ; pas d'update auto non approuvé | PLANNED |
| ACCEPT-Q184-01 | D | Fichiers+SQL restaurables et migration irréversible explicitement annoncée | PLANNED |
| ACCEPT-Q185-01 | D | Désinstallation avec conservation explicite ; refus de purge fichiers/DB/backups non autorisée | PLANNED |
| ACCEPT-Q186-01 | D | Détection en lecture seule avant adoption explicitement autorisée | PLANNED |
| ACCEPT-Q187-01 | D | Installations groupées sous limites de concurrence, quotas, annulation et reprise | PLANNED |
| ACCEPT-Q188-01 | D | Staging masqué, emails/webhooks réels bloqués, secrets indépendants | PLANNED |
| ACCEPT-Q189-01 | D | Coffre par site/acteur avec rotation et journalisation sans fuite de secret | PLANNED |
| ACCEPT-Q190-01 | D | Délégation incapable d'agir sur site/organisation/plan tiers | PLANNED |
| ACCEPT-Q191-01 | D | Hôte non qualifié ou plan insuffisant incapable d'activer des conteneurs | PLANNED |
| ACCEPT-Q192-01 | D | Recette Docker non substituable à Podman ni inversement sans qualification | PLANNED |
| ACCEPT-Q193-01 | D | Rootless privilégié ; exception rootful refusée sans approbation bornée et audit | PLANNED |
| ACCEPT-Q194-01 | C | Compose arbitraire et fournisseur inconnu refusés malgré demande du client | PLANNED |
| ACCEPT-Q195-01 | D | Digest/signature invalide, version révoquée ou registre non approuvé refusés | PLANNED |
| ACCEPT-Q196-01 | D | Privilèges, socket moteur et montages sensibles bloqués par défaut | PLANNED |
| ACCEPT-Q197-01 | D | Réseaux segmentés ; ingress/egress inter-tenants refusés hors politique | PLANNED |
| ACCEPT-Q198-01 | D | Quotas volumes, backup chiffré, rétention et restauration réelle vérifiés | PLANNED |
| ACCEPT-Q199-01 | D | Plafonds physiques prioritaires face aux quotas tenant CPU/RAM/PIDs/I/O/stockage | PLANNED |
| ACCEPT-Q200-01 | C | Export/import assisté avec backup et confirmation ; conversion automatique aveugle refusée | PLANNED |
| ACCEPT-Q201-01 | D | Catalogue altéré, rejoué ou rétrogradé refusé selon clés et versions | PLANNED |
| ACCEPT-Q202-01 | D | Éditeur ou version partenaire non approuvés interdits de publication | PLANNED |
| ACCEPT-Q203-01 | D | Vulnérabilité version installée : alerte et correction approuvée, sans auto-fix dangereux | PLANNED |
| ACCEPT-Q204-01 | D | Retrait des nouvelles installations sans effacer les données des installations existantes | PLANNED |
| ACCEPT-Q205-01 | D | Élément infecté en quarantaine : examen et restauration après procédure autorisée | PLANNED |
| ACCEPT-Q206-01 | D | Règles WAF héritées simulées, exceptions limitées et retour au dernier état sain | PLANNED |
| ACCEPT-Q207-01 | D | Journaux secrets expurgés, RBAC, rétention et export soumis aux droits | PLANNED |
| ACCEPT-Q208-01 | D | Opération sensible avec step-up/approbation selon risque ; MFA facultative | PLANNED |
| ACCEPT-Q209-01 | D | Plans concurrents ne doublent pas ressources/ports, revalidation anti-TOCTOU à l'effet | PLANNED |
| ACCEPT-Q210-01 | D | Téléchargement refuse SSRF/redirections dangereuses/cache corrompu/reprise non validée | PLANNED |
| ACCEPT-Q211-01 | D | Espaces natif/conteneurs distincts, recherche commune uniquement en lecture | PLANNED |
| ACCEPT-Q212-01 | D | Moteur natif gratuit clairement distingué des licences tiers, ressources et offres | PLANNED |
| ACCEPT-Q213-01 | D | Hub absent : catalogue natif sûr accessible hors ligne, pas de cache non signé | PLANNED |
| ACCEPT-Q214-01 | D | Revendeur cantonné à serveur/tenant/plan/catégorie/moteur ; phases respectées | PLANNED |
| ACCEPT-Q215-01 | D | Sponsor visible et séparé du classement organique sécurité/compatibilité | PLANNED |
| ACCEPT-Q216-01 | D | Connecteurs facturation vérifient événements tiers sans accorder de droit Linux | PLANNED |
| ACCEPT-Q217-01 | D | Webhook signé, anti-rejeu, filtres et destinations approuvées | PLANNED |
| ACCEPT-Q218-01 | D | API publique refuse appels arbitraires ou hors scope, rate-limit et audit | PLANNED |
| ACCEPT-Q219-01 | D | Métriques locales sans télémétrie Hub forcée ; diagnostics sur consentement | PLANNED |
| ACCEPT-Q220-01 | D | Règles versionnées héritées et simulées ; retour arrière sans désactiver invariants | PLANNED |

## Critère de sortie

Chaque PASS éventuel devra citer le commit d'implémentation, OS/VM qualifiés, droits tenant, manifestes versionnés, cas positif et refus, preuve réelle de backup/reprise si nécessaire, logs expurgés et revue spécialisée. SKIP/BLOCKED ne vaut jamais PASS. Cette matrice n'affirme aucune exécution des 50 tests.

Les prérequis Core R1/R2/R3/R4, l'ABI neutre R5 puis Hub privé R6 restent inchangés. Aucun fournisseur, tarif, seuil ou réglage par défaut n'est inventé.
