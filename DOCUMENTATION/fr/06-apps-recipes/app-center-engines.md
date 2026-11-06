<!-- forgepanel-doc id=FP-06-APP-CENTER-ENGINES revision=2 status=specified -->
# ForgePanel App Center — séparation des moteurs natif et conteneurs

[English](../../en/06-apps-recipes/app-center-engines.md) · [Catalogue Apps/Recipes](README.md) · [Tests](../13-tests-quality/app-center-engine-gates.md)

**Statut : SPECIFIED / DRAFT TECHNIQUE.** Le propriétaire confirme le **6 novembre 2026** deux familles distinctes sous App Center et la gratuité totale du moteur **ONE-CLICK INSTALL**. Cette orientation complète Q2/Q50 (Core gratuit), Q4 (runtimes clients), Q8/Q53 (catalogue officiel et partenaires vérifiés), Q47 (plan/validation/récupération), Q51 (pilotes Docker et Podman séparés) et Q81–Q110 (PHP, bases, staging, quotas). Elle ne vaut **ni installation fonctionnelle ni validation de toutes les caractéristiques candidates ci-dessous**. Q171+ restent non approuvés.

## Règles produit confirmées

1. **App Center est un conteneur de navigation, pas un moteur d'exécution unique.** Il présente deux sous-espaces indépendants : **ONE-CLICK INSTALL** (scripts natifs, type Softaculous) et **CONTAINER APPS** (applications en environnement isolé Docker/Podman, type catalogue 1Panel).
2. **ONE-CLICK INSTALL est toujours gratuit pour l'utilisateur ForgePanel** et ne demande aucun droit premium, paiement, abonnement, licence ForgePanel-Hub, conteneur Docker/Podman ou connectivité au Hub. Les coûts de serveur et les licences éventuelles des applications tierces sont **distincts** : la gratuité du moteur ne rend pas des logiciels commerciaux gratuits.
3. Chaque application/édition/version doit déclarer son **mode d'installation explicitement** : \`native_script\` ou \`container_stack\`. Ne jamais utiliser automatiquement une recette de conteneur pour remplacer une installation native, ni l'inverse. Une application peut avoir **deux fiches/recettes**, avec dépendances et support distincts.
4. La gestion de conteneurs utilise les pilotes indépendants Docker et Podman de Q51, sélectionnés **après test réel des capacités du serveur**. Ne pas installer le moteur de conteneurs simplement pour un site PHP standard. Une recette Compose Docker n'est pas présumée compatible Podman.
5. Le Core local est seul habilité à autoriser et exécuter les installations. Le Hub privé peut publier des **métadonnées** d'un catalogue d'éditeur selon des contrats versionnés, mais ne possède ni les fichiers clients, ni les secrets DB/volumes, ni les droits Linux, ni les clés privées. Le catalogue essentiel natif doit rester utilisable sans Hub.

## Comparatif de responsabilités

| Domaine | ONE-CLICK INSTALL — natif | CONTAINER APPS — Docker/Podman |
|---|---|---|
| Usage | CMS, boutique, forum, scripts installables dans un hébergement classique | Services applicatifs, outils de développement, stacks multi-services et applications exigeant des images |
| Précondition | Compte/site, WebStack compatible, PHP ou autre runtime natif qualifié, base SQL si nécessaire | Moteur Docker **ou** Podman qualifié, réseau, images, volumes, limites et politique d'exposition |
| Unité d'isolation | Identité Linux du site, PHP-FPM dédié, répertoires/ACL, quotas et autorisation par tenant | Identité conteneur, namespaces, seccomp/capabilities, cgroups, réseau/ports, volumes et comptes hôte |
| Ressources | Espace hébergement, PHP workers, I/O, DB utilisateurs/quotas, espace du site | Images et stockage de couches, volumes, CPU/RAM/PIDs, réseaux virtuels, ports hôte, secrets, dépendances multi-services |
| Installation | Artefact applicatif vérifié → fichier/DB/configuration → contrôles → activation | Image(s) vérifiée(s) → projet de stack approuvé → réseau/volumes/quotas → lancement → santé |
| Sauvegarde | Fichiers du site + DB + secrets nécessaires à une restauration | Volumes persistants + DB/service + manifeste de stack + état/recréation des secrets ; snapshot cohérent |
| Upgrade | Version des fichiers, migrations DB, versions runtime, sauvegarde préalable | Digest d'images, changement Compose/app, volumes/migrations, remplacement contrôlé |
| Désinstallation | Inventaire site/DB et choix explicite de rétention | Inventaire conteneurs/réseaux/volumes et choix explicite de rétention |
| Autorisations | Gestionnaire de site borné et plan d'hébergement | Permissions distinctes \`app.container.*\` soumises à politique serveur, ressources et RBAC |
| Quotas | Quotas hébergement/sites/base/fichiers | Quotas CPU/RAM/PIDs/stockage image/volume/ports et réseau |
| Prix du moteur ForgePanel | **Gratuit et inconditionnel** | Usage Core de base conforme Q2/Q50 ; aucun prix premium additionnel décidé pour ce moteur |
| Disponibilité initiale | **Roadmap après R4**, pas incluse dans le premier site PHP/HTTPS R4 | Phase avancée après pilotes Docker/Podman qualifiés et règles de sécurité approuvées |

## Exemple WordPress : deux installations totalement différentes

- **Natif** : application sur l'hébergement du client, fichiers sous identité du site, PHP-FPM compatible, MariaDB/MySQL, génération sécurisée de la configuration WordPress, ACL limitées, restauration site+DB. **Pas de Docker nécessaire.**
- **Conteneurisé** : image WordPress et, selon recette, base conteneurisée ou base explicitement provisionnée séparément ; image, volume persistant, réseau et port dédiés. Cette version consomme des ressources d'un moteur de conteneurs.
- Le site installé en natif **ne devient pas** un conteneur par simple changement de menu. Migration inter-moteurs = projet technique distinct avec export/import, DNS, secrets, sauvegarde et récupération.

## Architecture candidate (à approuver par spécialistes)

\`\`\`text
ForgePanel App Center (interface uniquement)
├── ONE-CLICK INSTALL [gratuit]
│   └── NativeRecipeRegistry → NativeInstallPlanner → NativeInstallExecutor
│                                 └── site/PHP-FPM/SQL/files/ACL/quota
└── CONTAINER APPS
    └── ContainerRecipeRegistry → ContainerInstallPlanner
                                  ├── DockerDriver
                                  └── PodmanDriver
                                        → images/volumes/networks/cgroups
                                     
Shared read-only catalog discovery, version/signature validation,
job ledger, tenant identity, audit and status conventions are possible,
but execution authority, runtime drivers, resources and recovery remain separate.
\`\`\`

Le Core ne doit pas interpréter une même recette polymorphe comme des **commandes shell**. Les manifestes sont de types distincts ; toute requête d'installation porte \`recipe_kind\`, version d'artefact, serveur, organisation/tenant/site, limites, permissions, révision, idempotency key et correlation ID. Les opérations Linux Go restent **typées, allowlistées et auditées**. Aucune API générique \`shell.exec\`, aucun script libre fourni via le catalogue.

### Manifeste natif : champs candidats

\`recipe_kind=native_script\`, ID/app/version, auteur/source et preuve d'intégrité, licence, OS/WebStack/PHP/extension(s), DB MySQL/MariaDB/PostgreSQL **uniquement si l'application les supporte**, variables secrètes, chemins relatifs confinés, compte/site cible, paramètres validés, étapes autorisées d'installation/upgrade, stratégie de rétention, sauvegarde/restore et health check. Ne jamais transformer une chaîne fournie par l'utilisateur en commande \`chown\`/\`chmod\`/PHP CLI ; traiter les permissions via des opérations typées sous identité bornée.

### Manifeste conteneur : champs candidats

\`recipe_kind=container_stack\`, ID/app/version, moteurs certifiés (\`docker\`/\`podman\`), versions/architecture, images épinglées et digests (signature/politique à spécifier), réseau/ingress/protocoles, ports et collisions, CPU/RAM/PIDs/I/O, stockage image + volumes persistants, mappings UID/GID, privilèges/capabilities, secrets, interdiction des mounts dangereux, dépendances et ordonnancement, probes de santé, upgrades/rollback et politique de rétention. Une recette \`docker-compose.yml\` de 1Panel est une **référence de recherche**, pas un manifest ForgePanel directement exécutable. Importer un Compose arbitraire avec bind-mount du disque hôte ou accès au socket Docker est interdit par défaut. **Traiter le YAML Compose comme du code non fiable** : `provider` peut exécuter un binaire côté hôte, `include`/`extends`, `env_file`, `secrets`/`configs` et les chemins relatifs peuvent accéder à d'autres fichiers. Interdire par défaut les fonctions non explicitement validées, résoudre/contrôler les chemins en sécurité et ne pas exécuter un Compose tiers brut. [Modèle de confiance Docker Compose](https://docs.docker.com/compose/trust-model/). **Podman Compose utilise un fournisseur externe de Compose** ; chaque pilote/provider exact demande une qualification séparée. [Documentation Podman](https://docs.podman.io/en/latest/markdown/podman-compose.1.html).

### Gestion des états et reprise

Pour les deux moteurs : \`DRAFT → PREFLIGHT → APPROVAL_REQUIRED (si nécessaire) → STAGED → APPLYING → VERIFYING → SUCCEEDED/FAILED/RECOVERY_REQUIRED\`. Chaque étape écrit un job durable corrélé et un état observé ; un acquittement de requête ou un conteneur simplement lancé ne suffit pas à déclarer une application saine. Pour les migrations SQL ou volumes, une restauration complète n'est pas automatiquement garantie : documenter les opérations irréversibles, préserver les données et tester une vraie reprise. Suppression de l'app **≠** suppression des données ou sauvegardes.

## Modèle d'accès et interfaces candidates

Dans PANEL \`/panel\`, le gestionnaire de site peut installer une recette native **pour ses propres sites** selon ses quotas. La gestion des conteneurs, y compris Docker/Podman, doit être attribuée séparément par des permissions tenant/serveur et par capacités réelles. FORGE \`/forge\` gère le catalogue local approuvé, les politiques, les risques réseau, les moteurs et leur disponibilité. La route précise de ces sous-écrans, leur présentation, l'activation par défaut de Container Apps et les rôles détaillés restent candidats. Un compteur de toutes les apps est possible en lecture seule, mais les **installations, backups et actions restent séparées par moteur**.

## Évaluation externe vérifiée (ne pas copier le code)

- [1Panel](https://github.com/1Panel-dev/1Panel) et [appstore/dev](https://github.com/1Panel-dev/appstore/tree/dev) : catalogue fondé sur versions \`apps/<app>/<version>/data.yml + docker-compose.yml\`, paramètres, port, DB, volumes, labels et réseaux. Exemple [WordPress 1Panel](https://github.com/1Panel-dev/appstore/blob/dev/apps/wordpress/7.1.4/docker-compose.yml) **utilise un conteneur** ; cela confirme que l'usage natif de ForgePanel exige un moteur séparé.
- [n8n 1Panel Compose](https://github.com/1Panel-dev/appstore/blob/dev/apps/n8n/2.47.2/docker-compose.yml) : démontre la dépendance aux images, port, volume et réseau. Certaines configurations amont doivent être auditées indépendamment (ex. sécurité des cookies) : **ne pas importer aveuglément**.
- [1Panel App Store Skills](https://github.com/1Panel-dev/1Panel-appstore-skills/blob/main/references/appstore-format.md) documente manifestes \`data.yml\` + Compose et scripts de cycle de vie facultatifs : ces scripts ne confèrent pas d'autorisation d'exécution à ForgePanel.
- [Softaculous](https://www.softaculous.net/docs/enduser/install-a-script/) illustre l'installation classique de scripts web (nom de domaine, répertoire, base, compte admin), non l'usage d'un moteur Docker.
- Le dépôt 1Panel App Store déclare une licence **GPL-3.0** ; ForgePanel ne réutilise ni copie son code, ses manifests ou ses logos sans revue juridique de licence/provenance et conformité. Les marques et licences des apps tierces doivent être respectées.

## Choix techniques ouverts, sans approbation implicite

- Inventaire et liste de lancement des recettes natives ; maintenance/signature, cadence d'upgrade, versions et compatibilité réellement testées.
- Isolation Linux du natif et stratégie d'exécution sécurisée des outils applicatifs (WP-CLI et équivalents), sans shell arbitraire.
- Politique Docker rootless/Podman rootless, Compose provider réellement certifié, soutien rootful sous exceptions, segmentation réseau, limites par tenant, opérations privilégiées et stockage.
- Taxonomie d'applications natives et conteneurisées, rôles revendeur, filtrage par plan/OS et interface précise.
- Compatibilité avec licences commerciales des applications tierces et règles de support ; **aucun tarif d'app ni de runtime conteneur n'est créé par cette étude**.
- Architecture de référence unique ou double registre de recettes dans PostgreSQL, migrations, signature des catalogues et preuves de certification.

**Gates** : documentation/revue Architecture → Security → API/IPC → Database → QA/VM → MASTER → Source Code. Le premier Core R4 (site PHP, domaine externe, HTTPS) **ne dépend pas** de cette fonctionnalité ; pas de développement d'installateur métier avant sources/contrats vérifiés. [Matrice de tests](../13-tests-quality/app-center-engine-gates.md).
