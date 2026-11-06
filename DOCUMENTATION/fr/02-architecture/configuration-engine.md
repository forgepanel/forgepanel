<!-- forgepanel-doc id=FP-02-CONFIG revision=10 status=specified -->
# Configuration Engine — spécification des réglages administrables

[English](../../en/02-architecture/configuration-engine.md) · [Architecture](README.md) · [Politique produit](../00-project-control/product-policy.md)

## Compléments Q180/Q220 approuvés (2026-11-06)

Le propriétaire a confirmé [Q180 D et Q220 D](../00-project-control/decisions-q171-q220.md) : règles de configuration héritées, versionnées, simulables et soumises aux droits. L'[exemple candidat App Center](app-center-config-inheritance.md) simule **sans exécuter** l'origine des valeurs, des plafonds restrictifs et les garde-fous immuables ; [16 tests réels](../13-tests-quality/app-center-configuration-gates.md) restent PLANNED. Valeurs par défaut, ressources OS, rétention, fournisseurs, langage final de règles, signatures, schéma et tables physiques ne sont pas décidés.

Pour les **portails système**, l'IP de la machine et un éventuel FQDN existant vérifié sont détectés automatiquement, avec **FORGE `/forge:8447` et PANEL `/panel:8446` fixes**. Aucun nom de domaine système personnalisable ni création automatique des sous-domaines `forge.`/`panel.`. Les **domaines des sites hébergés** et la **marque unique par organisation Q5/Q55** restent des fonctions configurables distinctes, sous DNS/TLS et permissions. Le tableau historique « ports/réseau/hôtes » n'autorise pas à modifier ces constantes système explicitement confirmées.

## Objectif et périmètres

Chaque réglage possède : `key` stable, schéma/type/units, valeur par défaut, documentation, groupe, scope, révision, origine, état calculé, capacité OS/WebStack, dépendances, niveau d'autorisation, secret ou non, classe d'impact, validateur et politique de reprise.

**Hiérarchie ciblée** : valeurs du produit → politique globale administrateur → serveur → organisation/revendeur → plan d'hébergement → compte → site/application → paramètre individuel autorisé. Un niveau inférieur peut surcharger seulement si son parent délègue la clé et si la valeur respecte ses contraintes. Les limitations globales de sécurité s'appliquent toujours ; un « mode Expert » change l'affichage, jamais les droits effectifs.

Les secrets sont des références à un stockage protégé, non des valeurs lisibles dans les réponses API, journaux, exports, vues, backups accessibles ou manifests.

## Catalogue de familles configurable

| Famille | Réglages exposés | Autorité et limites |
|---|---|---|
| Interface générale | Langue, fuseau horaire, densité, thème clair/sombre, widgets, annonces | Préférences utilisateur ou organisation ; aucune modification de droits |
| Branding / white-label | Logo, palettes, favicon, nom, domaine, templates d'email, identité revendeur | Organisation ayant permission, vérification DNS/TLS, pas de partage de cookies |
| Identité et RBAC | Rôles, permissions, sessions, accès API, MFA **facultatif**, paramètres de connexion | Autorité serveur/super-admin ; garde-fous et réauthentification |
| Ports et réseau | IP/IPv6, ports des portails, listeners, noms d'hôtes, reverse proxy | Administrateur système ; maintien de l'ancien accès jusqu'au succès du nouveau |
| WebStack et PHP | Profils Nginx/Apache/Caddy, versions PHP-FPM/FrankenPHP, limites et règles compatibles | Politique du serveur, capacité réelle et isolation tenant |
| Runtimes applicatifs | PHP, Node.js, Python, versions et extensions, déploiement de conteneurs | Comptes/serveurs autorisés ; limites cgroups, images signées et restrictions |
| Bases, DNS et mail | Fournisseurs, quotas, zones, boîtes, stockage, sauvegardes | Service natif/compte, sans élévation de privilège |
| Sécurité système | Firewall, SELinux/AppArmor, SSH, SFTP, verrouillage, audit | Administrateur ; **pas de désactivation implicite des contrôles** |
| Sauvegardes | Destinations, rétention, chiffrement, planifications et tests de restauration | Permissions serveur/compte, règles anti-effacement |
| Jobs et mises à jour | Créneaux, canaux stable/beta, retries, verrous, alertes | Permissions dédiées et vérification des signatures |
| Modules et extensions | Activation, version, paramètres, sources de packages, contrats et permissions | Confiance signée ; Core autonome sans extension |
| Connectivité Hub | Enregistrement volontaire, droits premium, vérification de versions, données techniques minimales, support et marketing **séparés** | Consentements distincts ; Core gratuit indépendant |
| Licences commerciales | État des droits, échéances, dernière preuve, délai hors ligne 60 jours, alertes | État **affiché**, politique d'émission de droits fixée par éditeur ; le client ne peut prolonger seul sa licence |

Les réglages de performance ne doivent pas exposer des variables arbitraires permettant une commande shell ou la suppression de l'isolation.

## Cycle de changement et garanties Q47

1. `DRAFT` — modification locale, diff en lecture seule, auteur et périmètre.
2. `PLAN` — compiler les changements selon les adaptateurs de l'OS, dépendances, conflits, propriétés de listeners, permissions et compatibilité.
3. `PREFLIGHT` — vérifier ressources, syntaxe, certificats, sauvegardes préexistantes et préconditions.
4. `SNAPSHOT` — sauvegarder configuration et données pertinentes avant mutation ; chiffrer et définir restauration et limites.
5. `APPLY` — verrouiller les ressources, préparer un ensemble versionné, appliquer en étapes idempotentes ; journal d'opérations durable.
6. `VERIFY` — contrôler statut systemd, santé du panneau, disponibilité locale et effective des services.
7. `COMMIT` — enregistrer version appliquée/audit, publier état et notifications.
8. `RECOVER` — si échec, restaurer ce qui est réversible et proposer une compensation explicite pour les effets non réversibles.

Les changements purement visuels peuvent s'appliquer immédiatement. Une modification de ports, firewall, WebStack, droits ou de storage exige au minimum PLAN/PREFLIGHT/SNAPSHOT/APPLY/VERIFY. Préserver un accès d'administration de secours lors des modifications réseau ; aucune garantie de rollback global d'une suppression de base/installation de paquet.

## Nouveaux réglages Q56–Q60

Le Core propose une politique de canaux **Stable/Beta/Dev**, avec contrôle d'accès et compatibilité (Q57) ; comptes locaux et SSO/OIDC facultatif avec MFA administrateur optionnel (Q58) ; conservation par catégorie et plafonds légaux/de sécurité (Q59). Prestataires de paiement et offres achat définitif/abonnements/essais/coupons/packs/options relèvent du **Hub**, pas du Core (Q56/Q60). Tous ces réglages restent à implémenter. [Spécification](../00-project-control/commerce-identity-release-policy.md).

## Paramètres nouveaux liés à Q61–Q70

Contrôle des canaux/signatures/approbations de publication (Q61) ; installation DEB/RPM vérifiée (Q62) ; DNS/mail par fournisseur et capacité (Q63–Q64) ; destinations, chiffrement, rétention, réplication et immutabilité des backups (Q65) ; réauthentification et approbation supplémentaire (Q66) ; politiques de groupes et clusters (Q67) ; seuils/destinataires d'alertes (Q68) ; propriété des IP/ports et profils par site (Q69) ; édition visuelle versionnée (Q70). Les modifications sensibles restent soumises à PLAN/VALIDATE/SNAPSHOT/APPLY/VERIFY/RECOVER. [Détails](../00-project-control/infrastructure-decisions.md).

## Politique Q71–Q80 et choix par site

Le registre de configuration devra afficher l'autorité du prestataire de clés et la rotation, les services Linux existants admissibles à l'adoption, les pilotes DNS et mail vérifiés, les sauvegardes 3-2-1 et leurs tests, les demandes d'approbation et secours, les groupes de serveurs, les exports Prometheus/OpenTelemetry et les widgets déclaratifs approuvés. **Q79** ajoute une `recommended_webstack` **par site** et une opération `webstack.planSwitch(site_id,target_profile,revision)` distincte du choix initial, soumise à PLAN/VALIDATE/SNAPSHOT/STAGE/VERIFY/RECOVER ; ne pas changer les autres vhosts. [Détails](../02-architecture/site-webstack-advisor.md).

## Réglages de site Q81–Q90

Proposer des clés typées/allowlistées : `site.webstack.profile`, `site.webstack.recommendation_revision`, `site.php.version`, `site.php.extensions`, `site.php.fpm_limits`, `site.tls.mode`, `site.tls.acme_challenge`, `site.deploy.git_ref`, `site.staging.policy`, `account.database.drivers`, `account.cache.drivers`, `account.ssh.access`, `mail.domain.filters`, `plan.quota.*` et `site.restore.scope`. Aucune valeur non autorisée ne peut contourner le plan/serveur. Les champs sont des exemples de contrat, non une API implémentée.

Q82 exige pour un changement de WebStack : `PLAN → PREFLIGHT → SNAPSHOT → STAGE → TEMP_ROUTE_TEST (si disponible) → CUTOVER (progressif si sûr) → VERIFY → FINALIZE/RECOVER`. Les fenêtres de maintenance, notifications, interruptions possibles et limites de rollback sont affichées. Q90 exige le même contrôle avant restauration/clonage vers staging. [Cycle d'hébergement](website-lifecycle.md) et [Q81–Q90](../00-project-control/decisions-q81-q90.md).

## Configurations Q91–Q100 et mécanismes sensibles

Ajouter des schémas candidats : `site.php.support_policy` (versions maintenues, avis EOL, fenêtre de migration), `site.php.isolation_profile` (capacité Linux certifiée), `site.deploy.trigger_policy` (manuel/webhook signé, branches autorisées), `site.staging.data_policy` (redaction, SMTP/webhooks, secrets, rétention), `site.tls.issuer` et `site.tls.dns01_provider`, `account.data_services` (droits/quotas par moteur), `account.ssh.policy` (clés/révocation/expiration), `mail.domain.webmail_driver`, `plan.quota.grace_policy` (seuils et rallonge administrateur) et `site.migration.plan` (compatibilité source/cible). Toutes les données sensibles sont des références à des secrets protégés. Les overrides enfants ne lèvent pas de limites du serveur.

Les opérations de migration inter-serveurs et de création de staging sont soumises à idempotence, verrous et plan/backup/test/commit ou compensation. **Q99 ne permet pas de contourner les limites physiques**. [Q91–Q100](../00-project-control/decisions-q91-q100.md) · [Cycle des sites](website-lifecycle.md).

## Politiques configurables Q101–Q110

Déclarer en schémas versionnés : `site.php.eol_exception` (autorité, durée, migration), `site.isolation.profile` (profil admissible par plan/site et OS), `site.environment.deploy_policy` (manuel/webhook, approbation), `site.staging.copy_policy` (classification, consentement spécial, rétention/audit), `site.tls.acme_fallback` (CA autorisées, reprises/alerte/secours), `account.database.topology` (partagée/dédiée, cluster certifié optionnel), `account.ssh.temporary_grants` (IP, durée, CA compatible), `mail.webmail.recommendation` (preuves de maintenance/sécurité), `plan.quota.grace_by_resource` (délai et plafond) et `site.migration.advanced_cutover` (pré-synchronisation, preuve de cohérence et bascule).

Les effets de toute configuration dérivent des permissions RBAC, de la politique du parent et des capacités OS **vérifiées**. Les exceptions, approbations et droits temporaires nécessitent révision, expiration et audit. Le Configuration Engine ne garantit ni dépassement de quota dur ni zéro interruption d'une migration. [Q101–Q110](../00-project-control/decisions-q101-q110.md) · [Règles techniques](runtime-exceptions-and-data-continuity.md). **Non implémenté**.

## API cible et critères de validation

Opérations envisagées : `config.readEffective(scope)`, `config.plan(changes,expected_revision)`, `config.apply(plan_id,idempotency_key)`, `config.history(resource)`, `config.recover(generation_id)`. Versionner les schémas ; erreurs ciblées `PERMISSION_DENIED`, `POLICY_LOCKED`, `CAPABILITY_UNAVAILABLE`, `CONFLICT`, `PLAN_STALE`, `PARTIAL_RECOVERY`.

Tests : aucune escalade via scope enfant ; permission refusée sur CLI et API ; rejeter révision obsolète ; config invalide non activée ; conflit port détecté ; nouveau port testé avant ancien retiré ; panne après snapshot ; compensation partielle explicite ; drift détecté sans écraser les fichiers externes ; permissions/valeurs visibles sans divulgation de secrets.

**Statut : entièrement spécifié, aucun Configuration Engine exécutable dans le dépôt actuel.**

## Q47 → R3 : articulation avec les opérations du futur agent

Le [contrat candidat Symfony ↔ Go](../08-api-contracts/symfony-go-ipc-r3.md) expose les enveloppes plan/révision/idempotence/audit, et le [contrat d'installateur](../14-devops-releases/installer-lifecycle-r3.md) applique les phases Q47 avec séparation des actions de lecture, staging et opérations privilégiées. Le [registre ACT-FP](../../evidence/typed-agent-operations-v1.json) est une **proposition documentaire** : aucune clé de configuration ne devient une commande système, aucun formulaire ne désactive les contrôles d'isolation et les deux opérations privilégiées restent bloquées. La persistance du job, les vérifications Linux, les TTL et les retries doivent être définis par les autorités avant code.

## Q47 — Distinguer l'intention, l'effet et sa preuve dans le modèle physique proposé

Le moteur de configuration doit persister une **intention** avec scope/acteurs/politique dans le [modèle PostgreSQL candidat](../09-database/physical-jobs-model-r3.md), puis soumettre l'action au [contrat typé](../08-api-contracts/typed-execution-recovery-r3.md) après validation de l'[identité Linux](../14-devops-releases/linux-service-identities-r3.md). Les phases `PLAN/PREFLIGHT/SNAPSHOT/STAGE` n'annoncent aucun effet ; l'ACK IPC ne devient pas `SUCCEEDED` ; les compteurs de fencing doivent être validés au point d'effet. Ces fichiers sont candidats, et tout changement de configuration en production reste interdit sans contrat/implémentation/VM réelle qualifiés. [Tests PLANNED](../13-tests-quality/r3-physical-execution-gates.md).
