<!-- forgepanel-doc id=FP-02-SERVICES revision=2 status=specified -->
# Services natifs et externes, sauvegardes, orchestration multi-serveurs

[English](../../en/02-architecture/service-drivers-and-ha.md) · [Architecture](README.md) · [Décisions Q61–Q70](../00-project-control/infrastructure-decisions.md)

## Choix précis Q73–Q75 et Q77–Q79

La famille DNS reste **multi-pilotes** et le moteur local recommandé sera déterminé **après essais par OS et capacité** (Q73 D) ; aucun choix définitif PowerDNS/BIND/Knot n'est implicite. Le premier pilote de messagerie native visé est **Postfix + Dovecot**, avec fournisseur ou relais externe configurable (Q74 C). La sauvegarde propose un profil **3-2-1**, exercice de restauration planifié et réplication autorisée (Q75 C), en plus des objectifs immutables Q65. L'administration multi-serveurs précède les modules HA et les orchestrateurs externes (Q77 D). Prometheus/OpenTelemetry sont des interfaces d'observabilité séparées (Q78 C). Voir [Q71–Q80](../00-project-control/decisions-q71-q80.md).

## Drivers DNS et mail (Q63 C, Q64 C)

Chaque service expose un contrat de **capabilités** avant de permettre sa configuration. Les adaptateurs DNS doivent décrire : fournisseur, zones gérées, lecture/modification de RRsets, TTL, validation, propagation, DNSSEC s'il est réellement supporté et opérations de retrait sans perte involontaire. Une zone a un propriétaire logique à un instant donné ; le moteur refuse les mises à jour concurrentes de deux fournisseurs non coordonnés. Les modes local/externe nécessitent une migration explicite de l'autorité et des enregistrements.

Les pilotes mail exposent boîtes, alias, domaines, quotas, transport, politiques TLS, antispam/antivirus selon capacité, et préparation DNS (SPF, DKIM, DMARC, MX). Ils doivent distinguer mail local, relais sortant, service externe et limites du fournisseur. Un fournisseur ne peut pas être choisi implicitement ; les ports, certificats, secrets, réputation et risques de relais ouvert sont validés lors du PLAN. Aucun moteur Postfix/Dovecot/PowerDNS n'est encore choisi comme unique backend.

## Backups et DR (Q65 D)

Le moteur devra traiter séparément :
- portée : configuration ForgePanel, PostgreSQL du panneau, clés de chiffrement, comptes, sites, bases client, emails et volumes;
- stockage : destination locale ou distante, réplication, versions et chiffrement, rétention/immutabilité, quotas et coûts;
- intégrité et restauration : manifestes/version, test de récupération dans un environnement isolé, preuve d'accès aux clés, vérification des données;
- incidents : plan de reprise d'un nœud, étape manuelle/automatique autorisée, RPO/RTO **mesurés**, jamais inventés.

L'immuabilité peut empêcher la suppression avant échéance mais ne remplace ni plusieurs emplacements ni restauration régulière. Aucune interface ne doit accorder des droits de suppression que le fournisseur ne peut réellement garantir.

## Gestion multi-serveurs et HA (Q67 D)

Le Core central définit des **états désirés** et chaque agent Go rapporte l'état **observé**. Les opérations ont ID unique, idempotence, scope, verrous et suivi durable. Les groupes de serveurs, politiques, rôles, migrations de charge, bascule et réplication exigent des contrats explicites. La disponibilité des sites doit être découplée du contrôleur central.

Un scénario HA nécessite définir frontières de quorum, détection des partitions, fencing/leases valides, cohérence des sauvegardes et mécanismes de récupération. Une base PostgreSQL distribuée, un DNS répliqué et un stockage partagé ne sont **pas automatiquement** disponibles par simple installation de ForgePanel. Le clustering reste une phase future (Q54), et ses composants seront activables selon capacité et profil.

## WebStacks et listeners (Q69 D)

Les profils documentés `nginx_apache_fpm`, `nginx_fpm`, `apache_fpm`, `caddy_fpm`, `caddy_frankenphp` sont des identifiants de planification. Plusieurs frontaux peuvent coexister **sur des IP/listeners distincts** ou derrière un ingress dont le routage est explicite. Un couple IP:port/protocole doit avoir un propriétaire. Un profil peut être choisi par site uniquement si la topologie écoute/route réellement le trafic. Les règles Apache `.htaccess` n'affectent pas les fichiers statiques servis en direct par Nginx ; l'accès reste protégé au premier frontal, ou un profil strict route les requêtes nécessaires via Apache.

Chaque génération suit plan, tests de configuration des services, validation TLS/ports, activation, reload, health-check et compensation. La panne d'un frontal client ne doit pas mettre hors service l'accès d'administration.

## Observabilité (Q68 C)

Mesures locales, règles d'alertes, emails/webhooks et exportateurs tiers selon permission et consentement. Le moteur traite la suppression des doublons, l'anti-tempête, le silencement, les escalades et les accusés de réception. Les métadonnées clientes sensibles, identifiants et secrets ne doivent pas partir automatiquement vers des services externes.

**État : document de conception uniquement.** Les pilotes, le HA et les restaurations nécessitent tests OS/VM réels avant tout statut VERIFIED.
