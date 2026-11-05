<!-- forgepanel-doc id=FP-08 revision=3 status=documented -->
# API et contrats

[English](../../en/08-api-contracts/README.md) · [Index](../README.md)

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

## Exigences du futur protocole

Définir une enveloppe avec version, ID d'opération, acteur/périmètre, ressource, corrélation/idempotence et paramètres typés. Authentifier les pairs locaux ou agents distants ; ne jamais accepter de commande shell. Persister l'admission avant d'accuser réception d'une tâche asynchrone. Définir reprises, annulation, expiration des verrous, doublons et échecs partiels. Un événement est un fait enregistré, pas la preuve du succès de tous les consommateurs.

Compatibilité et tests de migration précèdent toute nouvelle API publique. Les endpoints proposés dans les échanges antérieurs restent des exemples, pas des contrats publiés.

[Core](../03-core/README.md) · [Base](../09-database/README.md)
