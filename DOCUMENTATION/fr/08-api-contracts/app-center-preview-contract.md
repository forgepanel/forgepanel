<!-- forgepanel-doc id=FP-08-APP-PREVIEW revision=1 status=specified -->
# App Center — prévisualisation hors ligne des installations, deux moteurs

[English](../../en/08-api-contracts/app-center-preview-contract.md) · [Contrats de recettes](app-center-recipe-contracts.md) · [App Center](../06-apps-recipes/app-center-engines.md)

**CANDIDAT / NON DÉPLOYABLE.** Le [planificateur Python pur](../../../scripts/preview_app_center_install.py) n'est **ni un installateur, ni un agent Go, ni une API Symfony, ni un service de capacités hôte**. Il lit uniquement des fichiers JSON fictifs inclus dans [le dossier d'exemples synthétiques](../../../evidence/app-center-fixtures/install-request.synthetic.json). Il ne réalise aucun inventaire Linux réel, contrôle d'identité tenant, téléchargement d'archive, vérification de signature, requête SQL, appel Docker/Podman, réservation de ressources, sonde réseau ou opération privilégiée. Ses sorties contiennent toujours `execution_allowed=false` et `apply_available=false`.

## Séquence de prévisualisation typée

Le [validateur des recettes candidates](../../../scripts/validate_app_center_recipe.py) refuse en premier les `recipe_kind` inconnus ou mélangés et les champs d'exécution non examinés. La prévisualisation valide la **structure entière des données de test** : identifiant d'hôte fictif, liste des sites présumés possédés, PHP-FPM/bases compatibles disponibles, pilotes conteneurs déclarés et hypothétiques budgets CPU/RAM/PIDs. La demande contient un site cible, des ports TCP hôte sollicités et un indicateur informatif `hub_available` ; elle **n'accorde jamais de permission** et n'accepte ni secret ni commande libre.

- **ONE-CLICK INSTALL, `native_script` :** simulation des contrôles de site possédé, PHP-FPM et SQL natif ; aperçu des futures validations fichiers/quotas et sauvegarde/restauration. Ni Docker/Podman ni licence Hub ne sont nécessaires. L'exemple ne traite que PHP-FPM ; il **n'annule pas** les runtimes Node.js/Python prévus par ailleurs.
- **CONTAINER APPS, `container_stack` :** contrôle du pilote exact Docker **ou** Podman déclaré et des budgets synthétiques **distincts** CPU/RAM/PIDs ; étapes prévues pour image épinglée, réseau/volume et récupération. Une recette Docker seule ne devient pas Podman automatiquement. Aucune image téléchargée, aucun conteneur lancé.
- **Dans les deux cas :** l'absence du site dans les données fictives signale un blocage de portée **sans prétendre avoir vérifié l'identité réelle**. La publication d'un port hôte n'est jamais automatiquement acceptée : 8447 (FORGE) et 8446 (PANEL) restent réservés, même si omis dans le fichier hôte ; les autres ports réservés/occupés sont refusés et les ports libres demandent une politique d'exposition encore non validée.

## Interprétation du résultat

Le plan candidat contient `recipe_kind`, `app_id`, `variant_id`, `preview_steps`, `blocking_reasons`, `compatibility` et `next_action=SPECIALIST_REVIEW_AND_REAL_INTEGRATION_REQUIRED`. Le statut `compatibility=MATCHES_SYNTHETIC_FACTS_ONLY` signifie **uniquement que les données fictives ne se contredisent pas** ; il ne confère aucun droit d'installation. Les champs `tenant_authorization_verified`, `artifact_signature_verified`, `runtime_capabilities_verified`, `port_probe_executed`, `resource_reservations_created` et `external_reachability_verified` restent toujours à `false`.

Les codes proposés `NATIVE_PHP_FPM_UNAVAILABLE`, `NATIVE_DATABASE_UNAVAILABLE`, `CONTAINER_DRIVER_NOT_AVAILABLE`, `CONTAINER_*_BUDGET_UNAVAILABLE`, `FORGEPANEL_OR_OTHER_RESERVED_PORT`, `HOST_PORT_ALREADY_CLAIMED`, `HOST_PORT_PUBLICATION_NOT_APPROVED` et `SITE_OWNERSHIP_UNVERIFIED` sont **des valeurs de prévisualisation**, pas des erreurs officielles de l'API Core ni des observations d'un serveur.

Les champs inconnus, commandes injectées, confusions booléen/entier, ports dupliqués et statuts `VERIFIED` auto-attribués sont refusés. Aucun journal d'audit réel n'est écrit ; le planificateur de production devra utiliser un registre de jobs durable, l'identité vérifiée et des corrélations sans secret.

## Démonstration et preuves hors ligne

Sur la branche contenant les exemples :

```sh
python3 scripts/preview_app_center_install.py --fixture native
python3 scripts/preview_app_center_install.py --fixture container
python3 tests/documentation/test_app_center_preview.py -v
```

Les [tests de régression](../../../tests/documentation/test_app_center_preview.py) couvrent la séparation des moteurs, la gratuité native hors Hub, l'absence de PHP/SQL/pilote, la portée du site, CPU/RAM/PIDs, ports réservés/libres, champs malveillants, déterminisme et impossibilité d'exécuter. **Ils ne remplacent pas les [32 tests fonctionnels/VM PLANNED](../13-tests-quality/app-center-engine-gates.md).**

## HANDOFF avant intégration

- **Architecture :** choisir si un aperçu commun en lecture seule encapsule deux planificateurs revus indépendamment ; ne jamais réunir leurs moteurs d'exécution.
- **Security :** les booléens de capacité/propriété transmis par un client ne valent pas authentification ; recueillir l'état hôte auprès de services fiables et appliquer réservations/quotas atomiquement.
- **API/IPC :** lier les droits au tenant/site/serveur, digest, permission effective, idempotence et recontrôles à l'instant d'application ; aucun shell ou Compose libre.
- **Database :** jobs durables, verrous et mesures de ressources nécessitent des contrats de migration validés ; ce prototype n'en contient aucun.
- **DevOps/QA :** import authentique R1, Symfony/PostgreSQL réel R2, installateur qualifié R3, premier site PHP/HTTPS R4 et essais VM sécurité/récupération restent préalables à une livraison.

Q1–Q170 conservés ; Q171+ attendent des réponses explicites. Le moteur One-Click natif gratuit ne dépend pas du Hub ni de Docker/Podman ; ce prototype n'installe rien.
