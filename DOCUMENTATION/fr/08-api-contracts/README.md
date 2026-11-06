<!-- forgepanel-doc id=FP-08 revision=11 status=documented -->
# API et contrats

[English](../../en/08-api-contracts/README.md) · [Index](../README.md)

## Contrat candidat FORGE / PANEL

Le [contrat de routage, d'hôtes et de sessions](portal-route-boundary.md) formalise les surfaces **FORGE `/forge` sur 8447** et **PANEL `/panel` sur 8446**, avec des hôtes HTTPS 443 configurables. Le [registre de référence non opérationnel](../../../evidence/portal-access-registry-v1.json), son [validateur statique](../../../scripts/validate_portal_access_registry.py) et les [tests de contrat](../../../tests/documentation/test_portal_access_contract.py) ne remplacent pas des essais Symfony/HTTPS. Aucune API/route active n'en découle.

## Contrats observés dans SRC-03

L'archive contient `contracts/install-config.schema.json` (JSON Schema 2020-12, schema_version 1), des validateurs Go/PHP et des routes de setup. Aucune API REST publique d'hébergement, description OpenAPI, communication socket d'agent, diffusion de webhooks ou file distribuée n'est implémentée.

| Champ | Contrat existant |
|---|---|
| `schema_version` | Exactement 1 |
| `admin_port`, `user_port` | Entiers 1024–65535 ; nécessairement distincts |
| `admin_host`, `user_host` | Chaînes jusqu'à 253 caractères ; validation ASCII dans le code ; user_host non vide impose admin_host non vide et distinct |
| `webstack` | Une valeur parmi `nginx_apache_fpm`, `nginx_fpm`, `apache_fpm`, `caddy_fpm`, `caddy_frankenphp` |
| `modules` | Valeurs uniques parmi `dns`, `mail`, `database`, `sftp`, `backup` |

Tous les champs sont obligatoires ; les champs supplémentaires sont refusés. Les contraintes croisées sont dans le code, pas entièrement dans le schéma. Une intention valide ne prouve pas une infrastructure disponible. Ne pas changer silencieusement le sens d'un champ en ajoutant l'exécution.

Routes : `/setup`, `/setup/resume`, `/setup/mfa`, `/setup/recovery`, `/setup/configuration` utilisent les méthodes GET/POST déclarées ; `/setup/review` et `/setup/configuration.json` sont des vues/exports GET. Les mutations POST contrôlent CSRF et autorisation temporaire. Ce sont des routes sources, pas des endpoints déployés.

Codes CLI du code : 0 réussite, 2 échec des prérequis, 64 usage invalide/non supporté, 70 erreur interne/opération absente, 77 refus permission/TTY. `install apply` est refusé ; `release verify` vérifie la signature du manifeste, pas les octets d'artefacts téléchargés.

## Nouveaux contrats proposés (Q61–Q70)

Registre d'artefacts signés et métadonnées anti-retour arrière (Q61), capacités de pilotes DNS/mail/sauvegarde/monitoring (Q63–Q65/Q68), objets d'opérations multi-serveurs idempotents et états observés (Q67), propriété des listeners et générations WebStack (Q69), composants de navigation/widgets versionnés (Q70). Toutes les actions ont paramètres typés et scopes RBAC ; l'API d'agent ne permet aucune commande shell arbitraire. [Spécification](../00-project-control/infrastructure-decisions.md). **Contrats candidats**, aucun endpoint opérationnel ajouté.

## Contrat par site du conseiller WebStack (Q79)

Le contrat candidat `webstack.recommend(site_draft,server_facts,policy_revision)` renvoie profils compatibles, justifications, prérequis et avertissements ; `webstack.planSwitch(site_id,target,revision)` prépare un changement pour un site existant, soumis à idempotence, autorisation, vérification des listeners, sécurité `.htaccess` et sauvegarde. Un changement ne peut pas être une simple modification d'un champ de base ou du profil global du serveur. [Spécification](../02-architecture/site-webstack-advisor.md). Aucune API de ce type n'est opérationnelle.

## Contrats candidats d'hébergement Q81–Q90

`site.webstack.recommend`, `site.webstack.planSwitch`, `site.php.planConfig`, `site.tls.issueOrImport`, `site.deploy.planGit`, `site.staging.clone`, `tenant.database.allocate`, `tenant.cache.provision`, `tenant.files.list/write`, `tenant.ssh.configure`, `mail.domain.rules`, `hosting.plan.effectiveQuotas`, `site.restore.plan`. Tous exigent identité, tenant/organisation, plan, capacités réelles, révision, idempotence et audit, sans root arbitraire. Aucun n'est opérationnel. [Cycle du site](../02-architecture/website-lifecycle.md).

## Nouveaux contrats proposés Q91–Q100

`php.catalog.supportedVersions`, `site.php.planMigration`, `site.isolation.capabilities`, `site.git.deployManual`, `site.git.acceptWebhook`, `site.staging.privacyPolicy`, `site.tls.listIssuers`, `site.tls.dns01Driver`, `tenant.data.engineQuota`, `tenant.ssh.rotateOrRevoke`, `mail.webmail.capabilities`, `hosting.quota.graceGrant` et `site.migration.planTransfer`. Identité, organisation, ressource, politique, version, idempotence et audit obligatoires ; signaux Git et commandes distantes ne sont pas des instructions shell. Les contrats sont des **candidats non implémentés**. [Q91–Q100](../00-project-control/decisions-q91-q100.md).

## Contrats candidats Q101–Q110

`php.exception.request/approve/expire`, `site.isolation.listCertifiedProfiles`, `site.deploy.environmentPolicy`, `staging.sensitiveData.approve`, `acme.issuer.retryOrRecover`, `database.topology.plan`, `ssh.access.tempGrant/revoke`, `webmail.driver.recommend`, `quota.grace.planGrant`, `migration.preSync.planFailover` sont des **candidats non implémentés**. Ils doivent porter acteur, organisation/compte/site/environnement, capacité OS certifiée, paramètres typés, approbations, expiration, révision, idempotence, logs expurgés et état de récupération. Une approbation ne transforme pas un webhook en commande root ; l'échec de failover doit préserver une voie de reprise. [Décisions Q101–Q110](../00-project-control/decisions-q101-q110.md).

## Exigences du futur protocole

Définir une enveloppe avec version, ID d'opération, acteur/périmètre, ressource, corrélation/idempotence et paramètres typés. Authentifier les pairs locaux ou agents distants ; ne jamais accepter de commande shell. Persister l'admission avant d'accuser réception d'une tâche asynchrone. Définir reprises, annulation, expiration des verrous, doublons et échecs partiels. Un événement est un fait enregistré, pas la preuve du succès de tous les consommateurs.

Compatibilité et tests de migration précèdent toute nouvelle API publique. Les endpoints proposés dans les échanges antérieurs restent des exemples, pas des contrats publiés.

[Core](../03-core/README.md) · [Base](../09-database/README.md)

## R3 — Contrat candidat d'IPC typé Symfony ↔ Go

Le [contrat R3 IPC](symfony-go-ipc-r3.md) décrit `IPC-FP-0001..0012` : authentification du pair, double autorisation RBAC/tenant, opérations allowlistées, demandes/réponses strictement typées, erreurs, idempotence, journaux durables, locks, Q47 et récupération. Les [7 opérations candidates](../../evidence/typed-agent-operations-v1.json) et leurs [schémas JSON de requête](../../evidence/candidate-ipc-request-v1.schema.json)/[réponse](../../evidence/candidate-ipc-response-v1.schema.json) sont **documentaires et non activés**. Deux opérations privilégiées restent **`BLOCKED_UNTIL_QUALIFIED`** ; aucune API `shell.exec` ou route publique nouvelle. [Tests R3](../13-tests-quality/r3-ipc-installer-gates.md).

## R3 — Frontière de confiance du pair local

La [fiche d'identité du pair](local-peer-trust-r3.md) ajoute PEER-FP-0001..0012 : canal Unix privé **candidat**, identité du pair issue du noyau à vérifier, comptes séparés, ressources/permissions revérifiées par Go, lutte anti-rejeu et mode dégradé après rupture. Le [modèle d'attestation candidat](../../evidence/candidate-peer-binding-v1.schema.json) **n'est ni une preuve signée ni une API disponible**. Il ne faut pas faire confiance à un actor_claim, UID/PID JSON ou simple permission de socket pour autoriser Linux. [Jobs durables](../09-database/durable-jobs-r3.md) et [tests R3](../13-tests-quality/r3-jobs-peer-gates.md).

## R3 — Contrats d'effet système et compensation ciblée

Les [12 règles `EXEC-FP-0001..0012`](typed-execution-recovery-r3.md) détaillent les vérifications par opération (mandat, plan signé/révision, fencing au point d'effet, effets observés, VERIFY et récupération), sans créer de processus privilégié. Le [registre de garde-fous](../../evidence/candidate-typed-execution-guards-v1.json) reprend les **7 actions ACT-FP** ; `ACT-FP-0005/0007` restent **`BLOCKED_UNTIL_QUALIFIED`**. Les payloads arbitraires et shell.exec sont interdits ; un schéma JSON valide n'authentifie ni acteur ni pair. [12 tests de refus R3](../13-tests-quality/r3-physical-execution-gates.md).

## R3 — Admission, déduplication et preuve d'effet : revue critique

La [revue ciblée](../19-audits-risks/r3-job-integrity-audit.md) documente que l'audit d'une admission `DENIED` ne doit pas créer de job, que l'ACK inbox n'est pas preuve d'effet Linux et qu'un ancien token de fencing doit être refusé y compris **après restore PostgreSQL**. Un `actor_claim` et un `scope_ref` seuls ne prouvent jamais le tenant. **RISK-033..036 OPEN**, deux opérations privilégiées bloquées, [8 tests PLANNED](../19-audits-risks/r3-job-integrity-audit.md).
