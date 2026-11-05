<!-- forgepanel-doc id=FP-02 revision=1 status=documented -->
# Architecture du système

[English](../../en/02-architecture/README.md) · [Index](../README.md)

## Référence de conception et implémentation

La cible est un monolithe Symfony modulaire associé à un agent Go distinct, pas une multiplication prématurée de microservices. Les publics hébergement, VPS, développeurs et revendeurs seront servis par étapes (Q3) ; le Core reste indépendant du Hub et des offres premium. Symfony porte identité, autorisation contextualisée, interface, API et workflows métier. Go porte les opérations Linux typées et les adaptateurs OS/services. PostgreSQL conserve l'état applicatif. Un exécuteur privilégié minimal est une frontière cible, pas un démon déjà présent dans l'archive.

```text
Portails Admin / Client (hôtes et autorisations distincts)
                      |
         Plan de contrôle Symfony -- PostgreSQL
                      |
         IPC privé versionné / mTLS distant (prévu)
                      |
          Agent Go et journal des opérations
                      |
       opérations privilégiées bornées + adaptateurs OS
                      |
     Services Linux / comptes d'hébergement isolés
```

SRC-03 contient réellement une CLI, un planificateur, un pont console local fermé, du code PHP de setup et du SQL. L'IPC de l'agent ci-dessus n'est pas implémenté. Le pont lance certaines commandes Symfony après abandon des privilèges root ; ce n'est pas le futur exécuteur système.

## Règles de dépendance

Le domaine/applicatif dépend de contrats, pas des noms de paquets Debian, des chemins Nginx ou d'une interface particulière. Les adaptateurs OS résolvent les différences de paquets/services/sécurité. Les profils web composent frontal, routage et runtime. Un listener a un propriétaire ; les stacks mixtes exigent routage explicite ou listeners/IP distincts.

Préserver SELinux/AppArmor et identifier le gestionnaire de pare-feu. Paquets et versions PHP du panneau ne sont pas encore qualifiés sur les six cibles. Le runtime et la passerelle du panneau doivent rester distincts des stacks clientes pour conserver l'administration lorsqu'une configuration cliente échoue.

## Profils web

`nginx_apache_fpm`, `nginx_fpm`, `apache_fpm`, `caddy_fpm`, `caddy_frankenphp` sont les identifiants présents dans l'archive. Ils ne valident qu'une intention. La compatibilité stricte `.htaccess` impose le passage des requêtes concernées par Apache ; un accès statique Nginx ne doit pas contourner les règles d'accès. FrankenPHP worker nécessite compatibilité applicative et preuves d'isolation entre clients avant activation.

Une configuration suit planification, préparation, validation, activation, reload, contrôle de santé et finalisation/compensation. C'est un protocole cible, pas une transaction Linux globalement atomique. Les modifications destructives exigent une récupération explicite.

Le futur [Configuration Engine](configuration-engine.md) encadre les réglages hérités et le parcours plan/validation/sauvegarde/récupération (Q47). Les runtimes clients PHP, Node.js, Python et conteneurs (Q4) resteront indépendants du runtime du panneau. Non implémenté.

La décision Q51 prévoit [Docker et Podman via pilotes indépendants](container-drivers.md), sans imposer l'installation des deux sur chaque serveur. C'est une cible, non une fonctionnalité livrée.

[Décisions](../00-project-control/decisions.md) · [Contrats](../08-api-contracts/README.md) · [Sécurité](../10-security/README.md)
