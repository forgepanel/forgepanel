<!-- forgepanel-doc id=FP-00-Q101-110 revision=1 status=specified -->
# Arbitrages Q101–Q110 — Exceptions, politiques et continuité

[English](../../en/00-project-control/decisions-q101-q110.md) · [Registre](decisions.md) · [Q91–Q100](decisions-q91-q100.md) · [Politiques d'exploitation](../02-architecture/runtime-exceptions-and-data-continuity.md)

## Décisions explicites du propriétaire — 5 novembre 2026

Les réponses **Q101 C, Q102 C, Q103 C, Q104 D, Q105 C, Q106 D, Q107 C, Q108 D, Q109 C, Q110 D** complètent **Q1–Q100**, sans les remplacer. Statut **SPECIFIED** ; aucun de ces services n'est installé, déployé ou certifié par la seule documentation. Le Core AGPL gratuit reste indépendant du Hub ; MFA administrateur **facultatif**, marque **unique par organisation**, Q47 et les autorisations RBAC restent inchangés.

| Réf. | Décision confirmée | Portée et sécurité |
|---|---|---|
| Q101 C | **Exceptions PHP EOL temporaires autorisées par un administrateur, avec migration planifiée** | Dérogation explicite, responsable, justification, échéance, visibilité et audit ; aucun renouvellement silencieux ou exemption permanente. Les versions non maintenues restent signalées comme risquées. |
| Q102 C | **Profils d'isolation sélectionnables par plan/site selon capacités Linux certifiées** | Héritage des permissions, profils typés et allowlistés ; compte Unix/pools FPM, cgroups/SELinux/AppArmor seulement si validés sur cet OS. Un profil choisi dans l'UI n'est pas une preuve de confinement. |
| Q103 C | **Déploiements Git manuels/webhook avec politique par site ET environnement, approbation configurable** | Règles distinctes staging/production, branches/ref, acteurs, événements signés et conditions de test ; aucune exécution shell root déclenchée par webhook. |
| Q104 D | **Staging avec profils de copie par site, approbation spéciale des données sensibles, rétention et audit** | Fichiers seuls, schéma ou données anonymisées selon politique ; autorisation renforcée si données sensibles, secrets et communications de production désactivés/séparés ; expurgation et suppression à échéance. |
| Q105 C | **Plusieurs autorités ACME, tentatives bornées, alertes et procédure de secours** | Contrôler émetteurs et DNS-01 autorisés, quotas/rate-limits, credentials, challenges/hostnames ; conserver le dernier certificat valide jusqu'à activation sûre d'un remplaçant. |
| Q106 D | **Services DB mutualisés ou dédiés selon plan, clusters/réplication facultatifs via pilotes certifiés** | MariaDB/MySQL et PostgreSQL, Redis/Valkey optionnels ; identités/quotas/scopes distincts, contrôles de réplication/leader/quorum selon moteur réellement certifié. |
| Q107 C | **SSH par clés, restrictions et IP autorisées, accès temporaires et certificats SSH lorsque compatibles** | Politique du plan, durée et révocation, audit, chemins/commandes autorisés, clés privées protégées ; certificats uniquement avec autorité de confiance et cycle de vie validés. |
| Q108 D | **Webmail recommandé après tests de sécurité, compatibilité et maintenance** | Pas de moteur imposé sans preuves ; choix ultérieur par serveur/fournisseur/domaine (Q98), compatibilité des boîtes, TLS, antispam/quarantaine, politiques d'accès. |
| Q109 C | **Durées de grâce et plafonds de quotas par plan ET type de ressource** | Limite soft/hard, alertes et dépassement temporaire borné ; ajustement administrateur autorisé (Q99), sans outrepasser la capacité physique ni les frontières de sécurité. |
| Q110 D | **Présynchronisation, staging, bascule DNS/proxy et réplication/failover avancés si compatibles** | Préflight source/cible, cohérence des DB et écritures, contrôle des secrets, fenêtre de maintenance, health checks, stratégie de retour ; la réplication ne garantit pas l'absence de coupure ni l'atomicité. |

## Configurabilité et séparation des responsabilités

`global → serveur → organisation → plan → compte → site → environnement` fournit des valeurs effectives et des paramètres surchargeables **uniquement dans les limites parentales**. Les exceptions EOL sont limitées dans le temps et documentées, pas des désactivations générales de sécurité. Les approbations par opération, sauvegardes, révisions, preuves de capacité et rétention sont vérifiées côté serveur/agent. Les opérations lourdes utilisent **PLAN → VALIDATE → SNAPSHOT → STAGE → APPLY → VERIFY → COMMIT/RECOVER**, y compris les migrations avec copie et bascule progressive.

Le **Core** administre PHP, confinement, Git, staging, ACME, stockage/DB, SSH, Webmail, quotas et serveurs de destination. Le **Hub privé** publie des prérequis/versions de packages et des droits premium facultatifs, mais **n'exécute pas la migration, n'émet pas de certificats SSH pour les clients et ne récupère pas leurs bases, fichiers ou messages**. Les droits commerciaux ne remplacent pas les permissions Linux.

## Matrice d'acceptation future (non exécutée)

- Exceptions PHP expirées, non renouvelables sans réexamen, site et propriétaire notifiés, migration vers version maintenue et récupération.
- Profil d'isolation indisponible sur OS/compte, contournement via overrides enfant, symlink/socket ou FPM process, tests cgroups et SELinux/AppArmor.
- Déploiement webhook de production sans approbation, replay, site/environnement confondus, build échoué, absence de fuite de secrets.
- Staging avec données sensibles : approbation manquante, anonymisation insuffisante, mails ou callbacks réels, suppression et preuve d'audit.
- ACME : rate-limit, DNS provider indisponible, autorité alternative non approuvée, échec de renouvellement et dernier certificat sain conservé.
- Bases mutualisées/dédiées ou cluster : isolation, failover, réplication en retard, split-brain, restauration cohérente, moteur non certifié refusé.
- SSH temporaire/certifié : expiration/revocation, IP non admise, clé/CA compromise et commandes hors périmètre.
- Webmail : moteur obsolète/incompatible, isolation par domaine/boîte et migration de moteur sans perte.
- Quotas : grâce différente disque/CPU/mail, capacité réelle atteinte, permission de rallonge, charge concurrente.
- Migration : présynchronisation, écriture concurrente, DNS TTL/proxy, incompatibilité applicative, échec de failover, compensation auditable.

## Points de décision encore ouverts

Durée maximale des exceptions PHP, profils d'isolation certifiés sur chaque distribution, approbations de production par défaut, classification des données sensibles et règle d'anonymisation staging, ordre des CA ACME, topologies SQL/cache par défaut, choix de CA SSH et durée des accès, critères du Webmail recommandé, quotas/chiffres et durées de grâce, RPO/RTO et seuils pour la bascule avancée. **Aucune valeur ni prestataire n'est inventé.**
