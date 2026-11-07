<!-- forgepanel-doc id=FP-00-MODULAR-STRATEGY revision=1 status=proposed -->
# ForgePanel — Stratégie de développement modulaire et de releases jusqu'à 3.x

[English](../../en/00-project-control/modular-development-strategy.md) · [Roadmap modules](../04-modules/progressive-release-policy.md) · [Cycle de release](../14-devops-releases/release-lifecycle-plan.md) · [Critères QA](../13-tests-quality/modular-release-gates.md)

**Statut : adaptation candidate à valider, non fusionnée.** Deux sources utilisateur datées du 7 novembre 2026 : `STRATEGIE_DEVELOPPEMENT_MODULAIRE.md` et `MODULAR_DEVELOPMENT_STRATEGY.md`. Conserver les décisions Q1–Q220, les spécifications R1→R6 et l'historique Git ; ne remplacer aucune baseline ou décision non réconciliée par ce texte. Les montants, fournisseurs, dates, plafonds et versions définitives non décidés restent ouverts.

## 1. Objectif d'ingénierie

Publier une **V1.0 stable à petit périmètre, mais entièrement utilisable et sûre** : un administrateur installe ForgePanel sur une combinaison OS/WebStack réellement qualifiée, crée un compte autonome, gère au moins un site PHP avec domaine et HTTPS, gère fichiers/SFTP et droits, observe son VPS et sait restaurer sa configuration et ses données. Le Core reste opérationnel **sans** Hub privé, modules facultatifs, App Center, Docker/Podman, DNS autoritaire local, serveur mail, marketplace ou HA.

Les fonctions de sécurité nécessaires à ces parcours ne deviennent pas « facultatives » : authentification, autorisation et séparation des tenants, audit, isolation Linux, validation des artefacts, reprise et sauvegardes réellement restaurées, obligations légales liées à la distribution. **MFA facultative** pour l'admin, possibilité de l'activer ultérieurement, avec contrôle renforcé des actions sensibles suivant les décisions existantes. Aucun shell privilégié générique.

Rester fidèle au périmètre du projet : **Symfony/PHP + Twig/UX** pour le panneau, **PostgreSQL** pour l'état de contrôle, **Go** pour les actions système typées, FORGE `/forge:8447` et PANEL `/panel:8446` avec frontières de session/RBAC. Ne pas supposer que le prototype UI ou une archive source historique est déjà un runtime déployé.

## 2. Ce que l'on appelle « version »

Quatre axes **indépendants** :

| Axe | Exemple | Ce que cela ne prouve pas |
|---|---|---|
| Version du Core / contrat | `v1.0.0`, `v1.1.0` | La conformité d'un plugin séparé |
| Maturité d'une build | Dev, Pre-Alpha, Alpha, Preview, Beta, RC, GA | Son canal ou son installation réelle |
| Distribution | `Dev`, `Beta`, `Stable` avec audience interne/fermée/publique | La qualification d'un OS non testé |
| État d'un module | `PLANNED`, `SPECIFIED`, `DEVELOPING`, `TESTING`, `AVAILABLE` | Droit d'installation ou d'exécution |

**SemVer 2.0 :** un correctif compatible augmente PATCH, une fonctionnalité compatible augmente MINOR, une rupture d'API publique augmente MAJOR avec migration et dépréciation. `2.0` / `3.0` sont **des objectifs produits indicatifs** : ne pas forcer une majeure uniquement pour déplacer une fonctionnalité. `v0.x` reste possible en exploration ; après gel du périmètre 1.0, utiliser le train `v1.0.0-0.dev.N` → `-1.prealpha.N` → `-2.alpha.N` → `-3.preview.N` → `-4.beta.N` → `-5.rc.N` → `v1.0.0`. L'ordre lexicographique des mots ne sert pas de règle SemVer. Alpha interne/fermée et Beta privée/publique sont des **audiences**, non des types de version différents. Aucun de ces tags n'est déclaré publié.

## 3. Ordre de travail non négociable R1 → R6

| Jalon | Résultat réel exigé | Impact sur les releases |
|---|---|---|
| **R1** | Code Foundation v0.7 récupéré, intégrité, provenance/licences/secrets examinés, import Git exact avec delta MFA v0.7.1 revu, tests sur le SHA importé | Développement interne seulement tant que non fusionné |
| **R2** | Symfony + PostgreSQL réellement démarrés, premier admin et récupération, MFA facultative, HTTP/CSRF/RBAC/session, SQL transactionnel et concurrence testés | Pre-Alpha de laboratoire, installateur de **planification** uniquement |
| **R3** | Agent Go à opérations autorisées, IPC/identité/permissions, installateur signé/fiable réellement exécuté en VM jetable, échecs/reprises | Alpha interne ; aucun OS déclaré compatible sans VM |
| **R4** | Site PHP isolé, DNS externe contrôlé, HTTP-01/HTTPS, site-manager, fichiers/SFTP, maintenance VPS bornée, backup chiffré et restauration isolée réelle | Premier MVP fonctionnel, Alpha fermée puis cycles Beta/RC/GA |
| **R5** | API/SDK d'extension neutre et versionnée, démontrée avec un plugin de test **non-Hub** | Peut être livré en `1.x` ; Core fonctionne sans extension |
| **R6** | ForgePanel-Hub privé comme service éditeur autonome, licensing/catalogue/distribution facultatifs avec tests d'indépendance du Core | Après R5, jamais une dépendance du Core gratuit |

**Réconciliation des documents transversaux :** ils demandent en Pre-Alpha un Core démarrable et un parcours complet démontrable. Pour ForgePanel, R2 donne le **parcours complet de bootstrap/identité en laboratoire**. Il ne faut pas prétendre disposer de l'**installateur Linux opérationnel** avant R3. Cette exception de mise en séquence évite une contradiction avec Q119/Q120 ; elle n'abaisse aucun test requis pour une Beta ou une Stable.

## 4. Version 1.0 — socle indispensable / MVP

- Installateur vérifié et circuit de récupération, avec démonstration réelle sur **au moins une** combinaison OS + WebStack sélectionnée par comparaison VM/Q121-Q122, pas une matrice des six OS supposée certifiée.
- Comptes, sessions, authentification, RBAC, séparation admin/gestionnaire de site, **MFA optionnelle**, audit, secrets protégés et PostgreSQL transactionnel.
- Site PHP/FPM isolé, domaine externe, conseils DNS **sans modification automatique**, validation A/AAAA réellement publiés, port 80/ACME HTTP-01 et HTTPS effectif.
- Fichiers/SFTP de site, restrictions de chemins, absence de shell par défaut, permissions vérifiées avec tests tenant croisés et une base SQL de site qualifiée.
- Diagnostic et opérations VPS nécessaires, maintenance/upgrade planifiés et non destructifs, journaux, sauvegarde chiffrée avec clés accessibles et **restauration effectivement testée**.
- **Catalogue de modules en lecture seule** dans l'interface, sans que cette page UI devienne une dépendance au démarrage du Core. Chaque carte à venir est informationnelle.

La Stable 1.0 **n'exige pas** ONE-CLICK INSTALL, Docker/Podman, DNS local, serveur mail, éditeur de thèmes, revendeur, multi-serveurs ou le Hub. Les déclarer livrés sans code et preuves serait trompeur. La V1 doit néanmoins être maintenable, installable, testée et exploitable sur son périmètre annoncé.

## 5. Trains facultatifs : cibles, non engagements

| Train indicatif | Modules candidats | Condition d'entrée |
|---|---|---|
| `v1.1.x` | **ONE-CLICK INSTALL** natif et gratuit ; Git Deploy ; API d'extension générique R5 | Recettes signées, tests d'installation/récupération, droits et sécurité ; aucun Docker ou Hub requis |
| `v1.2.x` | **CONTAINER APPS Docker**, staging, SQL/cache additionnels, WebStack switch, observabilité enrichie ; Hub R6 **après R5** | Qualification distincte driver/réseau/volume/quotas/sauvegarde, isolation, contrat d'extension |
| `v1.3.x` | **CONTAINER APPS Podman** indépendant, DNS local, Postfix/Dovecot, WAF candidat en détection, antivirus | Essais OS/driver, signatures, rollback/quarantaine et compatibilité |
| `v1.4.x+` | Webmail, revendeur, éditeur visuel, Configuration Center avancé, migration interserveurs, connecteurs de facturation | RBAC/règles/configuration versionnée, migrations et plans de reprise |
| `2.x` | Multi-serveurs, HA/DR, services d'orchestration/virtualisation **si démontrés nécessaires** | Mesures de capacité, cohérence distribuée, isolation, failover/restore réels |
| `3.x` | Maturité écosystème, compatibilité multi-versions, haute échelle / multi-régions **selon besoins mesurés** | Aucune obligation de rupture MAJOR pour ces seules fonctions |

**Un module incomplet glisse à un train ultérieur, sans repousser la release du Core**, à condition de ne pas être essentiel au parcours annoncé et d'être absent/désactivé dans l'artefact livré. Le registre de [40 entrées candidates](../../evidence/forgepanel-modular-roadmap-proposed-v2.json) conserve les 15 capacités du socle et 25 éléments futurs du lot documentaire précédent ; tous restent non installables/non exécutables dans ce registre documentaire.

## 6. Architecture et conditions de progression

Démarrer par un **monolithe Symfony modulaire**, sans microservices obligatoires : contrats, services et migrations versionnés ; agent Go à frontière de privilèges ; extensions exécutées séparément lorsqu'exigé. Le `CapabilityResolver` doit évaluer côté serveur les dépendances, l'OS réellement qualifié, les versions d'API, les autorisations, le plan, les conflits et les ressources. **La visibilité, la disponibilité et l'activation sont trois états distincts**. Une carte « En développement » n'est jamais une permission.

Le Core n'injecte ni route, ni worker, ni migration, ni service optionnel en l'absence du paquet et des validations ; l'échec d'un module ne stoppe ni les sites existants ni l'accès local ou la restauration. Une dépendance de sécurité essentielle ne peut pas être rendue facultative. Désactivation et désinstallation ne suppriment pas les données sans plan explicite de conservation/reprise. Toute action privilégiée passe par des opérations typées et autorisées, **jamais un shell arbitraire**.

## 7. Priorisation et livraisons incrémentales

Classer `MUST / SHOULD / COULD / LATER` ; limiter le travail en parallèle ; livrer des tranches **UI → permission → domaine → API/données → audit → test → documentation**. Une démonstration complète d'un vrai site PHP est prioritaire sur vingt écrans simulés. `features/* → develop → stable → main → production` reste le workflow **déjà approuvé par ForgePanel** : contrairement à la suggestion transversale, conserver la branche `production` existante, sans prétendre qu'une branche signifie déploiement. Construire un artefact identifié une fois, signer/horodater sa provenance puis promouvoir les **mêmes octets**. Aucun push forcé ni contournement de revues. `hotfix/*` suit les branches maintenues avec tests/backports.

La CI documente PASS / FAIL / BLOCKED / NOT RUN pour les cas du périmètre livré. Avant diffusion externe : revue AGPL/commercial/CLA/tiers, canal confidentiel de sécurité réellement vérifié, audits et tests VM/HTTP/SQL/backup/restore, support et changelog bilingues. LTS/EOL, durées de support, fournisseurs et dates restent ouverts. **Q171–Q220 sont adoptées comme orientations produit dans la PR Core #53 encore brouillon ; aucune qualification ne découle de cette PR.**

## 8. État vérifié et handoffs

- Les sources Foundation v0.7/v0.7.1 ont été **récupérées hors Git et préparées localement** dans des archives séparées. Elles ne constituent pas un import officiel dans `forgepanel/forgepanel`.
- Sur le `develop` observable, le Core n'est pas encore un hébergeur Symfony/PostgreSQL installable et certifié ; certains outils Go/JSON isolés ne changent pas ce constat.
- La création d'une branche GitHub dans l'organisation `forgepanel` est actuellement refusée (**403**). Cette adaptation est **préparée localement**, pas fusionnée, ni publiée, ni adoptée automatiquement comme baseline.
- Handoffs ciblés : **MASTER** (ratifier cible et versions), **Modules/Architecture** (manifest/resolver), **Security/API/Database** (permissions, IPC, migrations), **QA/DevOps** (releases et VMs), **Design** (catalogue informatif) et **Hub** (contrat privé après ABI).

[Registre des releases candidates](../../evidence/forgepanel-release-trains-proposed-v2.json) · [Matrice QA planifiée](../../evidence/forgepanel-modular-qa-proposed-v1.json). **Aucune fonctionnalité supplémentaire n'est déclarée implémentée ou vérifiée par ces documents.**