<!-- forgepanel-doc id=FP-02-WEBSITE revision=3 status=specified -->
# Architecture du site — WebStack, PHP, TLS, déploiement, données et restauration

[English](../../en/02-architecture/website-lifecycle.md) · [Conseiller WebStack](site-webstack-advisor.md) · [Arbitrages Q81–Q90](../00-project-control/decisions-q81-q90.md)

## Frontières d'un site

Un site appartient à un compte/organisation et à un serveur identifié. Son état versionné déclare : domaines, utilisateur Unix isolé, root HTTP, WebStack, runtime PHP/PHP-FPM, versions/extensions/droits, limites CPU/RAM/processus/disk, certificats, bases, fichiers et SFTP/SSH autorisés, références de déploiement, backup, staging et état observé. La configuration du **panneau Symfony** reste séparée de celle des applications clientes.

Les plans d'hébergement fixent une **politique supérieure** non contournable par le site ; les paramètres par site héritent du plan/compte et peuvent être surchargés uniquement avec capacité et permission. Un refus d'opération est vérifié au service/API/agent, pas uniquement par le masquage d'un champ UI.

## WebStack recommandée et changement (Q81 C, Q82 D et Q79)

Lors de chaque création, le conseiller construit une recommandation explicable basée sur : application et version, besoin `.htaccess`, PHP/extensions, OS/services certifiés, sécurité/isolation, ressources et disponibilité des listeners. Proposer les profils admissibles parmi `nginx_apache_fpm`, `nginx_fpm`, `apache_fpm`, `caddy_fpm`, `caddy_frankenphp`. Une suggestion ne peut pas rendre possible un profil incompatible ; le propriétaire du couple IP/port est unique. Le profil du panneau n'est pas modifié.

Pour un site existant, `webstack.planSwitch(site,target,expected_revision)` inventorie les routes et effets, propose une fenêtre de maintenance et des notifications, prépare un snapshot et une **route temporaire de test** si l'infrastructure l'autorise. Une **bascule progressive** n'est utilisée que si la topologie peut router des parties du trafic sans violer les sessions, les écritures applicatives ou les règles d'accès. Sinon, bascule contrôlée avec interruption éventuelle clairement annoncée. Validation syntaxe, TLS, PHP, `.htaccess`, contrôle de santé et retour compensatoire avant finalisation. Ne jamais promettre zéro interruption ou rollback SQL général.

## PHP par site (Q83 C)

Un site sélectionne une **version PHP supportée/qualifiée** parmi celles autorisées par le serveur et le plan. Ses extensions et directives PHP-FPM configurables sont des clés **allowlistées et typées** (ex. mémoire, temps d'exécution, limites de requêtes, workers, upload) bornées par les ressources du compte, les permissions et les capacités OS. Pools et sockets/sessions protégés par identité OS distincte ; pas de variables de configuration librement injectées dans des commandes, templates ou chemins. Le moteur de politique refuse d'affaiblir les limites système ou d'accéder au runtime du panneau.

## DNS, certificats et renouvellement (Q84 C)

ACME via HTTP-01 ou DNS-01 selon compatibilité réelle. Pour un wildcard, une preuve appropriée (notamment **DNS-01**) est nécessaire ; vérifier propriété du domaine et capacités du fournisseur DNS. Les certificats personnalisés sont importés avec vérification de correspondance clé/certificat, périodes, hostnames et droits. Les clés privées ne sont ni affichées dans les logs ni partagées avec Hub. Renouvellement avec alertes, retries bornés, détection de dérive, sauvegarde de l'ancienne génération et reload/health check ; ne pas accepter un domaine non autorisé.

## Déploiement Git et staging (Q85 C)

Fichiers/SFTP restent disponibles ; Git Deploy est un mode additionnel. Dépôt, ref/tag/commit, empreinte et identifiants de déploiement sont versionnés, et les clés d'accès sont protégées hors logs. Déployer dans un dossier isolé, valider le runtime/dépendances, créer l'aperçu staging, sauvegarder l'état pertinent, puis activer sous contrôle de santé. Une migration SQL, les uploads utilisateurs et les données persistantes exigent leur propre stratégie de récupération : **réinstaller l'ancien commit n'annule pas leurs modifications**.

Le staging est une **ressource distincte** avec URL/certificat, configuration, données et secrets séparés ; emails sortants, webhooks et indexation publics doivent être désactivés ou explicitement autorisés. L'option blue-green/canary et les pipelines avancés ne sont pas exigés par Q85, contrairement à la **bascule WebStack progressive** de Q82 lorsque faisable.

## Bases de données, cache et accès fichiers (Q86 D, Q87 B)

Pilotes pour MariaDB/MySQL et PostgreSQL en services clients ; Redis et Valkey sont des modules facultatifs cache/queue qui ne doivent pas être exposés publiquement sans sécurité adaptée. Des comptes et schémas/bases distincts par ressource et tenant sont requis. Le PostgreSQL de ForgePanel Core reste **séparé des bases hébergées**. Secrets, quotas, backup et autorisations de connexion sont configurables sans divulgation.

Le gestionnaire de fichiers et SFTP respectent la propriété Unix, les chemins canonisés, les symlinks et le quota. **SSH limité et optionnel** pour un compte disposant d'une autorisation explicite, sans shell root générique et sans ouvrir un terminal web implicite. Les comptes suspendus et les sessions/répertoires non autorisés doivent être bloqués.

## Email et plans d'hébergement (Q88 C, Q89 C)

Le pilote mail fournit si capacité réellement démontrée : SPF/DKIM/DMARC, TLS, antispam/antivirus, webmail, quarantaine, filtres et rapports **par domaine**, avec permissions par boîte et secrets protégés. Le fournisseur externe peut offrir un sous-ensemble des fonctions ; une UI ne doit pas prétendre gérer une fonction absente.

Les plans comprennent stockage, domaines, bases, boîtes, CPU/RAM/processus, versions/extensions PHP et ressources associées. Valeurs effectives héritées, limites hard/soft, alertes et consommation réelle mesurée sont visibles. L'agent applique les limites selon système (cgroups/quotas) réellement validé ; un compteur graphique seul ne garantit pas l'isolation.

## Clonage, restauration et contrôle de données (Q90 D)

Un site peut recevoir des sauvegardes **complètes ou sélectives** (fichiers, base, configuration) et un **clone vers staging**. La sélection de source/destination déclenche plan, permissions tenant, vérification d'espace, snapshot cible avant écrasement, redaction des données selon droits, rotation des secrets/URLs et contrôle de santé. La restauration entre environnements n'accorde pas de nouveaux droits sur les données. Exiger tests de reprise et un suivi d'échec partiel ; les copies immuables et leur rétention restent applicables selon Q65/Q75.

## Précisions des arbitrages Q91–Q100

- **PHP Q91/Q92** : maintenir le catalogue PHP clients avec dates EOL amont/fournisseur et alertes ; migrations planifiées et tests de compatibilité ; pools PHP-FPM distincts par site, profils renforcés lorsque Linux fournit des mécanismes certifiés. Ne jamais imposer le PHP du panneau.
- **Git/Staging Q93/Q94** : mode manuel et/ou webhook authentifié selon site ; référentiel/ref autorisé, anti-rejeu, contrôle des jobs ; staging avec copie sous consentement, anonymisation, secrets distincts, rétention/audit et sorties SMTP/webhooks neutralisées.
- **TLS Q95** : plusieurs ACME CA et pilotes DNS-01 interchangeables, wildcards sous preuve de domaine, alertes et renouvellement contrôlé, sans perte prématurée de la configuration précédente.
- **Ressources Q96/Q97/Q98/Q99** : plusieurs moteurs SQL/cache par compte avec quotas distincts ; SSH limité par plan, clé, expiration et révocation ; webmail choisi parmi les backends compatibles serveur/fournisseur avec règles de domaine ; soft/hard quotas, grâce bornée et allocations supplémentaires seulement par administrateur habilité, sans franchir la capacité réelle.
- **Migration Q100** : sauvegarde de source/cible, préflight OS/WebStack/PHP/DB/mail, staging isolé, transfert authentifié, secret rotation, cutover et reprise auditée. [Processus inter-serveurs](cross-server-migration.md).

[Détails PHP, staging et accès](php-staging-and-access-policy.md) · [Registre Q91–Q100](../00-project-control/decisions-q91-q100.md). Ces fonctions restent des cibles non implémentées.

## Extensions Q101–Q110

Le cycle des sites intègre **exceptions PHP EOL temporaires/migration** (Q101) et profils d'isolation par plan/site certifiés (Q102) ; les déclencheurs Git **par site ET environnement**, avec approbation configurable (Q103), et les copies de staging avec approbation spéciale pour données sensibles, rétention et audit (Q104). Renouvellement ACME via plusieurs CA, retries bornés et secours (Q105). Bases **mutualisées ou dédiées** avec clusters/replication **facultatifs après certification** (Q106). SSH temporaire/certificats autorisés et IP bornées (Q107), Webmail conseillé par tests (Q108), grâce de quotas par plan et ressource (Q109), migration présynchronisée avec réplication/bascule **uniquement si compatible** (Q110).

Les droits de copie, d'exécution ou de bascule sont distincts. Une fenêtre de maintenance reste nécessaire si la cohérence applicative ne peut être conservée ; aucune fonction premium du Hub n'est nécessaire aux opérations essentielles du Core. [Décisions](../00-project-control/decisions-q101-q110.md) · [Politique technique](runtime-exceptions-and-data-continuity.md).

## État, tests et non-implémentation

Chaque étape s'exécute par job idempotent et journalisé : `PLAN → VALIDATE → SNAPSHOT → STAGE → APPLY/SWITCH → VERIFY → COMMIT/RECOVER`. Tester les erreurs à chaque frontière, interruption/reprise, cross-tenant, inaccessibilité ACME/DNS/Git, extensions incompatibles, PHP-FPM isolé, données non réversibles, route temporaire publique accidentelle, secrets clonés, et restauration partielle. Le Hub n'a ni les données hébergées ni des privilèges Linux sur les installations clientes.

**Spécification uniquement : ni moteur de site, ni Git Deploy, ni webmail, ni système de sauvegarde, ni interface de staging n'est actuellement opérationnel.**
