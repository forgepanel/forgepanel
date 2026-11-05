<!-- forgepanel-doc id=FP-02-CONTAINERS revision=1 status=specified -->
# Pilotes Docker et Podman

[English](../../en/02-architecture/container-drivers.md) · [Architecture](README.md)

## Décision Q51 C : deux moteurs distincts

ForgePanel vise **Docker et Podman**, disponibles via deux adaptateurs indépendants derrière une interface Go générique. Le choix de l'agent ne requiert pas que les deux technologies soient installées. Les tests de compatibilité sont effectués par distribution, version et ressources disponibles.

Les conteneurs hébergent des **applications clientes**, non le runtime Symfony du panneau. Les runtimes PHP, Node.js et Python classiques restent également possibles lorsqu'ils sont autorisés.

## API envisagée et paramètres

Un contrat `ContainerRuntimeDriver` devra fournir `Capabilities`, `PlanDeploy`, `Start`, `Stop`, `Inspect`, `Metrics`, `Backup` et `PlanRemove`. Chaque action est typée, liée à un compte, auditée et validée par les autorisations du Core.

Paramètres administrables : choix du moteur, images et versions autorisées, CPU/RAM, quotas, ports et réseau, stockage, logs, redémarrage, secrets et sauvegardes. La configuration est appliquée via [Configuration Engine](configuration-engine.md) avec prévisualisation, contrôles, restauration lorsque possible et historique.

## Sécurité et état

L'accès aux services de gestion de conteneurs doit être strictement autorisé ; les exécutions privilégiées ou les montages sensibles ne sont pas autorisés par défaut. Le mode rootless est à privilégier s'il est compatible. Préserver SELinux/AppArmor et vérifier les mécanismes d'isolation. Les tests doivent couvrir séparation des clients, quotas, réseau, sauvegardes et erreurs.

**Aucun pilote n'est implémenté ou certifié.** Les deux pilotes constituent une cible produit confirmée, et le choix du moteur par défaut sur chaque distribution demeure technique. Les pilotes d'hébergement essentiels sont prévus dans le Core gratuit ; les services cloud managés sont des prestations distinctes facultatives.
