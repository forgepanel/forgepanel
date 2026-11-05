<!-- forgepanel-doc id=FP-02-PHP-STAGING revision=2 status=specified -->
# Politique PHP, staging Git, ACME, accès et quotas par site

[English](../../en/02-architecture/php-staging-and-access-policy.md) · [Cycle du site](website-lifecycle.md) · [Q91–Q100](../00-project-control/decisions-q91-q100.md)

## PHP maintenu et confinement réel (Q91 C, Q92 D)

Le contrôleur recense les versions PHP clientes **effectivement disponibles et maintenues** sur chaque OS/canal signé : version, date de fin de support amont et du fournisseur, EOL, origine, extensions et compatibilité de la WebStack. Le **PHP Symfony du panneau n'est pas sélectionnable par les clients**. Alertes et fenêtres de migration sont configurables par plan/site ; ne pas appliquer silencieusement un changement incompatible ou supprimer les données d'un site en fin de support.

Chaque site peut disposer d'un **pool PHP-FPM propre**, socket/identité Unix distincts, quotas CPU/mémoire/processus et politique renforcée selon capacités certifiées (cgroups, SELinux/AppArmor, sandbox systemd, namespaces ou autres technologies après tests). Les chemins non publics et secrets d'un autre client sont inaccessibles, y compris en cas de confusion de symlinks ou de sockets. Une directive FPM autorisée n'annule pas une restriction du serveur. Isolations proposées via profils `standard`/`hardened` sont des **propositions**, pas des garanties déjà vérifiées.

## Déploiement Git manuel/webhook (Q93 C) et staging privé (Q94 D)

Par site, choisir explicitement manuel, webhook ou les deux. Une notification Git n'est admise qu'après validation de son secret/signature, audience, fenêtre de validité, ref autorisée, idempotence, quotas et permission du propriétaire ; la branche de staging peut différer de celle de production. Les artefacts immuables, logs expurgés, révisions de config et contrôles de santé permettent de reprendre un job sans exécuter des scripts libres en root.

Le clone de production vers staging suit une politique par site : données fichiers seuls ou DB limitée, demande d'approbation, masquage/anonymisation sensible, rotation des secrets, URLs/identités séparées, non-indexation et suppression/neutralisation par défaut des **envois SMTP, callbacks/webhooks, transactions et tâches destructives**. Régler rétention/expiration, export et effacement sous les obligations légales et conserver un journal d'accès. Une base en lecture seule n'est pas automatiquement anonymisée.

## Plusieurs CA ACME et DNS-01 (Q95 C)

Gérer les comptes ACME, autorités autorisées, challenge HTTP-01/DNS-01 selon propriété de domaine et compatibilité, pilotes DNS-01 signés/versionnés, secrets de token API protégés. Wildcards via challenge admissible (DNS-01 généralement). Renouvellements avec politique de délai, retries bornés, alertes, vérification de certificat/clé/hostnames et rollback de génération de conf ; ne pas supprimer l'ancien certificat avant validation effective du nouveau.

## Données, SSH et Webmail (Q96 D, Q97 C, Q98 C)

Plusieurs moteurs MariaDB/MySQL et PostgreSQL peuvent être associés au même compte avec **identités, quotas, permissions et secrets séparés** ; Redis/Valkey pour cache/queues facultatifs selon capacité, pas d'accès réseau ouvert par défaut. Ne pas mélanger stockage de données clientes avec PostgreSQL du panneau.

SSH utilise des clés d'accès autorisées au niveau plan/compte, restrictions d'identité/chemins/commandes, expiration et révocation contrôlées ; l'option Q97 n'autorise pas un terminal web, et un mode secours n'ouvre aucun shell root aux clients. Les mécanismes de confinement SSH requièrent une matrice de tests Linux.

Webmail sélectionnable selon les capacités du serveur et du fournisseur mail, droits par domaine/boîte, protection des contenus, filtrage, quarantaine et TLS. Les moteurs choisis doivent être annoncés comme pilotes qualifiés et leur configuration reprise dans le Configuration Engine. Une interface cliente n'affiche pas une fonction absente du fournisseur.

## Quotas avec grâce contrôlée (Q99 D)

Les limites **hard** sont liées aux capacités réelles de l'hôte (disque, inode, CPU, RAM, processus, SMTP/DB selon fournisseur). Les limites **soft** et seuils d'alerte peuvent déclencher un délai de grâce ou une rallonge bornée, traçable et accordée par une permission administrateur dédiée, avec expiration/reprise. Aucune rallonge ne peut autoriser une consommation dépassant la capacité physique, les contraintes de sécurité ou les allocations d'autres clients. Quotas décomptés au niveau plan/compte/site, usage mesuré et facturation premium séparée des droits systèmes.

## Précisions obligatoires Q101–Q109

- **PHP obsolète (Q101 C)** : l'exception ne peut être accordée que pour un site, un responsable, un motif, une date d'expiration et un plan de migration ; avertir du risque résiduel et journaliser la revue. Aucun renouvellement automatique non validé.
- **Confinement (Q102 C)** : profils par plan/site, uniquement selon capacités Linux **certifiées** ; un pool PHP-FPM isolé ne remplace pas les contrôles OS nécessaires.
- **Déploiements (Q103 C)** : distinguer `production` et `staging` dans les règles manuel/webhook, tests et approbation par action ; un webhook ne constitue jamais une élévation de privilège.
- **Données sensibles staging (Q104 D)** : profils fichiers/schéma/données anonymisées, approbation spéciale pour les données sensibles, secrets distincts, durée de conservation et piste d'audit.
- **ACME (Q105 C)** : CA alternatives approuvées, tentatives bornées, alertes, secours et dernier certificat validé conservé.
- **DB (Q106 D)** : mutualisé/dédié au choix du plan, clusters/réplication facultatifs **uniquement après certification** du pilote, sans franchir le scope.
- **SSH (Q107 C)** : clés, restrictions, IP autorisées, accès temporaires et certificats SSH si infrastructure de confiance compatible, révocation/audit.
- **Webmail (Q108 D)** : moteur conseillé uniquement après tests de sécurité, compatibilité et maintenance, sans imposer un fournisseur non qualifié.
- **Quotas (Q109 C)** : grâce **par plan et ressource**, expiration/plafond/configuration, jamais au-delà des limites physiques/sécurité.

[Contrats et tests Q101–Q110](runtime-exceptions-and-data-continuity.md) · [Décisions](../00-project-control/decisions-q101-q110.md). **Aucun de ces composants n'est implémenté**.

## Contrats candidats et échecs attendus

Objets `PHPVersionCatalog`, `SiteIsolationPolicy`, `GitDeployTrigger`, `StagingPrivacyPolicy`, `AcmeIssuerAdapter`, `TenantDataService`, `SSHAccessPolicy`, `WebmailDriver`, `QuotaGraceGrant`, tous avec `schema_version`, `scope`, `effective_policy`, `owner`, `capability` et `audit`. Refuser versions EOL sans exception documentée, webhook rejoué, source Git non autorisée, copie staging non consentie, provider DNS non disponible, SSH périmé, moteur Webmail incompatible, quota dépassant la capacité.

**Statut : spécification de contrats, aucun runtime PHP/SSO/mail/SSH/ACME/Git validé par des VM.**
