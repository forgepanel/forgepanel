<!-- forgepanel-doc id=FP-08-APP-RECIPE revision=1 status=specified -->
# App Center — contrats de recettes distincts et contrôles d'admission

[English](../../en/08-api-contracts/app-center-recipe-contracts.md) · [Index API](README.md) · [Deux moteurs](../06-apps-recipes/app-center-engines.md)

**Statut : SPÉCIFICATION DRAFT / CANDIDATE-ONLY.** Aucun parseur de manifestes de production, installateur, exécuteur Docker/Podman, endpoint Symfony ni catalogue actif n'est implémenté. Les choix produit confirmés sont le **One-Click natif gratuit**, les **Container Apps séparées** et l'absence de mélange entre moteurs. Les schémas et limites ci-dessous sont des propositions techniques soumises aux revues spécialisées. Q171+ restent ouverts.

## Enveloppe commune — version candidate 1

Chaque manifeste candidat est un objet JSON contenant `schema_version=1`, `contract_status=CANDIDATE_ONLY` et `execution_allowed=false`. Il identifie `app_id`, `variant_id`, `app_version`, `publisher_id`, `recipe_kind` et `artifact` (origine HTTPS, SHA-256 et identifiant de licence du logiciel tiers), avec **un seul** objet propre au moteur :

- `recipe_kind=native_script` : présence exclusive de `native`, jamais `container`. Le bloc `native` décrit le site/tenant autorisé, le runtime natif **compatible**, la base SQL éventuelle et les extensions nécessaires. Il s'agit d'un **plan abstrait**, jamais d'un script shell libre. L'installateur futur devra se limiter à des opérations typées approuvées et cantonnées à l'identité du site.
- `recipe_kind=container_stack` : présence exclusive de `container`, jamais `native`. Le bloc `container` déclare le pilote **DOCKER** ou **PODMAN** qualifié, des images OCI épinglées par digest, des volumes persistants et des demandes CPU/RAM/PIDs positives et bornées. Privilèges root, sockets Docker/Podman, montage racine hôte, fournisseurs Compose non approuvés, réseau hôte et ports non contrôlés restent interdits par défaut. Un fichier Docker Compose brut **n'est pas** un manifeste ForgePanel exécutable.

Un `app_id` peut être commun aux deux, mais `variant_id` et `recipe_kind` désignent **deux installations distinctes**. Historique, quotas, jobs, sauvegardes et autorisations ne fusionnent pas et ne se migrent jamais silencieusement.

## Deux exemples synthétiques non exécutables

Les fichiers [recette native fictive](../../../evidence/app-center-fixtures/native-cms.v1.json) et [recette conteneur fictive](../../../evidence/app-center-fixtures/container-worker.v1.json) utilisent **des identités inventées, des URL example.invalid sans résolution et des empreintes de forme seulement**. Ils ne constituent pas de véritables téléchargements approuvés. **Ne jamais installer, publier ni accorder de droits depuis ces exemples.**

Le [validateur hors ligne](../../../scripts/validate_app_center_recipe.py) contrôle seulement la forme candidate et quelques invariants de refus. Il n'exécute aucune commande, n'utilise ni Docker/Podman ni SQL, ne télécharge rien, ne vérifie aucune signature et ne valide ni les quotas du serveur ni un droit d'installation. Il ne pourra **jamais** être la seule protection d'un système de production.

## Frontières futures des contrats et du cycle de vie

La future API Core distinguera `native.planInstall` de `container.planInstall` et dirigera les demandes vers des exécuteurs typés séparés. Exiger identité authentifiée, propriété du site/serveur, capacités hôte, digest/version de recette, révision d'opération, idempotence, corrélation et provenance signée/validée. Le Core **réautorise localement** même si le Hub marque une entrée « approuvée ». L'absence du Hub ne bloque pas le One-Click gratuit.

La validation d'une **fiche descriptive** n'autorise aucun effet Linux. Aucun futur exécuteur n'accepte de champ inconnu, commande shell, Compose brut, code PHP libre, chemin arbitraire, argument privilégié fourni par le client ou URL de script non audité.

### Ressources et sécurité natives

Un site natif requiert identité Linux cantonnée, PHP-FPM ou autre runtime qualifié, quotas espace/inodes, compte SQL limité à sa base, extraction d'archive protégée et résolution canonique des chemins. Contrôler symlinks, traversées, fichiers de configuration privés, secrets, uploads et workers. La sauvegarde couvre **fichiers + base SQL cohérente** ; le rollback du code ne restaure pas automatiquement un schéma SQL. One-Click reste **gratuit sans Hub et sans Docker/Podman**.

### Ressources et sécurité conteneurs

Une stack exige un pilote Docker **ou** Podman testé avec le fournisseur Compose exact (si employé). Faire appliquer namespaces, stratégie rootless/capabilities, cgroups CPU/RAM/PIDs, stockage d'images, quotas de volumes, réseaux, ports, logs et secrets. Le lancement d'un conteneur ne prouve pas la santé applicative. Les volumes et données sont conservés à la désinstallation sauf choix autorisé. Conteneurs privilégiés, sockets moteur et montages sensibles sont refusés par défaut.

## Refus explicites entre moteurs

- `recipe_kind` inconnu, deux blocs `native` et `container`, ou bloc inadapté : **REJECT_TYPE_MISMATCH**, avant toute ressource.
- Champ inconnu comme `command`, `shell`, `compose_file`, `env_file`, `host_path`, `privileged` ou `hooks` non qualifiés : **REJECT_UNREVIEWED_FIELD**.
- Image sans digest, origine non HTTPS, checksum invalide, licence ou provenance absente : **REJECT_UNTRUSTED_ARTIFACT**.
- Pilote/runtime indisponible, quotas insuffisants : **BLOCKED_CAPABILITY**, sans recours automatique à l'autre moteur.
- `execution_allowed=true` ou faux statut de publication : **REJECT_UNAPPROVED_EXECUTION**.

Ces codes d'erreur sont **proposés**, pas des enums API existantes. Un refus ne doit jamais altérer Linux ni effacer site/SQL/volumes. Tout effet réel exigera plus tard jobs durables, révision de politique, audit et récupération. Un acquittement HTTP n'est pas un succès d'installation.

## Autorités et validations restantes

- **API/IPC** : contrats typés versionnés et refus par moteur.
- **Database** : identité logique commune de l'application, mais variantes, installations, quotas, jobs, ressources et sauvegardes séparés ; aucune table/migration approuvée.
- **Security** : aucun shell root générique, provenance/signatures et isolation tenant ; tests d'archives malveillantes, Compose/chemins et épuisement de ressources.
- **QA** : [32 scénarios d'intégration](../13-tests-quality/app-center-engine-gates.md) **PLANNED** ; succès éventuel des tests de manifeste hors ligne indépendant.
- **Operations** : le premier site PHP/HTTPS R4 du Core passe avant les deux installateurs ; aucun service, OS, paiement ou release ne découle du présent document.

[Étude des deux moteurs](../06-apps-recipes/app-center-engines.md) · [Pilotes de conteneurs](../02-architecture/container-drivers.md).
