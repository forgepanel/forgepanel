<!-- forgepanel-doc id=FP-02 revision=6 status=documented -->
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

Les nouvelles décisions Q63–Q69 sont détaillées dans [services et HA](service-drivers-and-ha.md) : DNS/mail locaux ou distants, sauvegardes répliquées/immuables, orchestration multi-serveurs, alertes et ingress par IP/port. Les signatures et dépôts de paquets sont décrits par [Q61–Q70](../00-project-control/infrastructure-decisions.md). Ces drivers sont spécifiés, non livrés.

Conformément à Q79, un [conseiller de WebStack par site](site-webstack-advisor.md) proposera des profils compatibles à la création et un changement ultérieur avec plan de transition, contrôle de `.htaccess`, des listeners et récupération. Q72 permettra l'adoption contrôlée de services préexistants sans écraser leur configuration ; Q77 prévoit l'extension progressive multi-serveurs vers HA. [Décisions Q71–Q80](../00-project-control/decisions-q71-q80.md).

Le nouveau [cycle de vie des sites](website-lifecycle.md) précise Q81–Q90 : WebStack conseillée en tenant compte de l'isolation, des ressources et des listeners ; transition avec fenêtre de maintenance et route temporaire/bascule progressive **si faisable** ; PHP-FPM/extensions, TLS ACME, Git staging, moteurs SQL/cache, fichiers/SSH, webmail, quotas et clonage/restauration. Il reste spécifié et non opérationnel.

Les choix Q91–Q100 ajoutent des [politiques PHP, staging, ACME, accès et quotas](php-staging-and-access-policy.md), ainsi qu'une [migration entre serveurs avec préflight et récupération](cross-server-migration.md). Ils complètent le [cycle de vie des sites](website-lifecycle.md), sans rendre les composants disponibles à l'exécution. Les administrateurs pourront choisir les versions PHP et le mode Git par site dans les limites des politiques et de l'isolation réellement vérifiée.

Les nouveaux [contrats de continuité Q101–Q110](runtime-exceptions-and-data-continuity.md) détaillent exceptions PHP temporaires, confinement Linux qualifié, politiques Git par environnement, staging sensible, ACME multi-CA, bases mutualisées/dédiées avec réplication facultative, SSH temporaire, Webmail recommandé, grâce de quotas et pré-synchronisation/bascule conditionnelle. La cible est **spécifiée seulement**, les disponibilités restent à prouver sur chaque OS et profil. [Registre](../00-project-control/decisions-q101-q110.md).

[Décisions](../00-project-control/decisions.md) · [Contrats](../08-api-contracts/README.md) · [Sécurité](../10-security/README.md)
