<!-- forgepanel-doc id=FP-04-COMPONENTS revision=3 status=documented -->
# Fiches composants

[English](../../en/04-modules/components.md) · [Index modules](README.md)

Les chemins de prototypes ci-dessous appartiennent à SRC-03, pas aux sources applicatives suivies dans ce dépôt. État : `IMPLEMENTED IN ARCHIVE` ; tests natifs relancés, mais ni publication ni déploiement. Cycle commun : compilation/tests en laboratoire ; aucune installation, mise à jour ou désinstallation de production automatisée. Retirer le code du prototype n'autorise jamais la suppression de comptes, clés ou bases. Ces règles communes s'appliquent à chaque fiche sauf précision contraire.

## CMP-CLI — CLI locale et prérequis

| Champ | Fiche |
|---|---|
| Objectif / utilisateurs | Entrée opérateur/ingénieur ; `cmd/forgepanel`, `internal/doctor` |
| Fonctions / acceptation | Version, inspection hôte et diagnostic JSON en lecture seule ; erreurs codifiées ; aucune modification par une opération absente |
| Dépendances / consommateurs | Go/Linux et faits hôte ; opérateurs et futur installateur, pas service web actif |
| Données / migration | Aucun schéma applicatif ; sortie de diagnostic ; aucune migration |
| Contrats / jobs | Arguments et codes CLI ; ni broker ni flux d'événements |
| Permissions / sécurité | Inspection seule pour doctor ; aucune API shell arbitraire ; expurger le diagnostic avant partage |
| Échec / cycle de vie | Erreur prérequis/usage/interne ; compilation locale ; pas d'installateur ou réparation automatique |
| Tests / supervision / limite | Tests Go et build réussis ; rapport structuré ; `status` global et réparation absents |

## CMP-PLAN — Planificateur d'intention d'installation

| Champ | Fiche |
|---|---|
| Objectif / utilisateurs | Transformer la configuration admin en plan inspectable ; `internal/installer` |
| Fonctions / acceptation | Validation stricte et sélection cible/profil ; `executable=false` tant que le moteur d'application distinct n'existe pas |
| Dépendances / consommateurs | Faits OS et schéma ; CLI et intention exportée par le wizard |
| Données / migration | Intention JSON version 1 ; aucun journal durable d'exécution ou migration |
| Contrats / jobs | Cinq profils, six cibles de fixtures, étapes symboliques et blocages ; aucun job d'installation réel |
| Permissions / sécurité | Planification sans modification privilégiée ; rejeter champs inconnus, doublons, taille excessive et conflits |
| Échec / cycle de vie | Entrée invalide refusée avant action ; aucun paquet/service/port modifié ; changements de schéma testés pour compatibilité |
| Tests / supervision / limite | Validateurs Go et 30 combinaisons de fixtures testés ; ni disponibilité des paquets ni qualification VM |

## CMP-SETUP — Métier du bootstrap et enrôlement MFA

| Champ | Fiche |
|---|---|
| Objectif / utilisateurs | Créer le premier admin sans identifiants Linux ; `apps/panel/src/Setup` |
| Fonctions / acceptation | Émission/consommation de jeton, compte initial unique, TOTP, reprise locale et brouillon révisé ; aucune configuration avant MFA |
| Dépendances / consommateurs | Horloge, transaction, chiffrement, TOTP ; contrôleurs HTTP et commandes locales |
| Données / migration | Vérificateurs/compteurs de setup, compte et audit via le schéma à trois tables |
| Contrats / jobs | Phases nommées et méthodes avec autorisation temporaire ; audit ; aucun job de provisionnement |
| Permissions / sécurité | Autorisations courtes, condensats, mots de passe Argon2id, MFA chiffré ; émission locale limitée |
| Échec / cycle de vie | Conserver les essais invalides, rollback des erreurs d'infrastructure, refuser rejeu/révision obsolète ; jetons v0.6 ni migrés ni acceptés |
| Tests / supervision / limite | 28 tests PHP/184 assertions réussis ; audit sans secrets ; login permanent et consommation des codes de secours absents |

## CMP-WIZARD — Interface de setup Symfony

| Champ | Fiche |
|---|---|
| Objectif / utilisateurs | Configuration initiale guidée pour propriétaire ; contrôleur, frontière Http et Twig |
| Fonctions / acceptation | Inscription, MFA, affichage secours, configuration et export JSON ; brouillon revu ne signifie pas installé |
| Dépendances / consommateurs | Symfony/Twig, sessions, CSRF, limiteur, CMP-SETUP ; navigateur et plan CLI |
| Données / migration | Autorisation en session et affichage de secours temporaire ; écritures SQL déléguées au métier |
| Contrats / jobs | Routes `/setup` déclarées ; vues/exports GET et mutations POST protégées ; aucun job agent distant |
| Permissions / sécurité | HTTPS/origine et autorisation temporaire ; USER fermé ; les ports n'isolent pas les cookies |
| Échec / cycle de vie | Reprise locale du setup expiré ; erreurs sûres ; dépendances et passerelle HTTPS préalables |
| Tests / supervision / limite | Syntaxe PHP vérifiée ; exécution framework/HTTP/navigateur en attente ; protections sources sans preuve d'intégration |

## CMP-STORE — Dépôt PostgreSQL du setup

| Champ | Fiche |
|---|---|
| Objectif / utilisateurs | Autorité transactionnelle unique du bootstrap ; classes infrastructure repository/transaction |
| Fonctions / acceptation | Verrouiller singleton, créer compte, persister état/audit ; jamais de jeton consommé sans compte après rollback |
| Dépendances / consommateurs | PDO PostgreSQL et base dédiée migrée ; métier du setup |
| Données / migration | `fp_setup`, `fp_admins`, `fp_setup_audit`, index partiel admin initial ; `001_setup.sql` |
| Contrats / jobs | SetupRepository/SetupTransaction ; aucune queue ou base d'hébergement |
| Permissions / sécurité | Rôle SQL dédié prévu ; pas de DDL pour le runtime de production ; clé de chiffrement hors base |
| Échec / cycle de vie | Rollback SQL des erreurs d'infrastructure ; exécuteur de migrations, sauvegarde et upgrades absents |
| Tests / supervision / limite | Test SQL fourni : sortie 77 ici ; aucune certification concurrence/restauration ; lignes d'audit non assimilées à un audit complet inviolable |

## CMP-BRIDGE — Pont console local fermé

| Champ | Fiche |
|---|---|
| Objectif / utilisateurs | Opérateur local privilégié limité à status/token/resume ; `internal/panelbridge` |
| Fonctions / acceptation | Vérifier les chemins, passer au compte `forgepanel`, exécuter une action PHP fixe ; jamais PHP applicatif sous root |
| Dépendances / consommateurs | Identités Linux, `/usr/share/forgepanel/panel/bin/console` root-owned, PHP fiable, compte dédié, PHP/SQL sains ; CLI |
| Données / migration | Aucun schéma propre ; la console accède au setup ; aucune migration propre |
| Contrats / jobs | Trois actions autorisées, environnement filtré, durée bornée ; aucun exécuteur générique |
| Permissions / sécurité | sudo/root local requis ; secrets sur terminal contrôlant ; environnement appelant non hérité |
| Échec / cycle de vie | Refus si installation absente/non fiable ; aucun repli historique ; paquets d'installation non fournis |
| Tests / supervision / limite | Tests Go des gardes réussis ; abandon des privilèges et parcours installé non vérifiés ; SQL arrêté empêche la récupération des comptes SQL |

## CMP-RELEASE — Prototype de vérification de publication

| Champ | Fiche |
|---|---|
| Objectif / utilisateurs | Vérifier métadonnées signées ; `internal/releases`, CLI `release verify` |
| Fonctions / acceptation | Signature Ed25519, expiration, séquence et empreintes via bibliothèque ; entrées altérées refusées |
| Dépendances / consommateurs | Clé publique fournie, horloge et manifeste ; futur installateur/updater |
| Données / migration | Aucun store persistant de confiance/séquence ; aucune migration |
| Contrats / jobs | Manifeste et signature détachée ; CLI limitée au manifeste, pas aux octets d'artefact ; aucun téléchargement/installation |
| Permissions / sécurité | Vérification en lecture seule ; confiance liée à la provenance indépendante de la clé ; aucune clé privée de production fournie |
| Échec / cycle de vie | Refus des manifestes invalides, expirés ou trop anciens ; cycle clés/mise à jour/installation/retrait absent |
| Tests / supervision / limite | Cas Go adverses réussis ; aucun canal officiel, rotation/révocation ou anti-retour arrière persistant |

## CMP-LEGACY — Store de jetons fichier historique

| Champ | Fiche |
|---|---|
| Objectif / utilisateurs | Conserver prototype/tests v0.6 ; `internal/bootstrap` |
| Fonctions / acceptation | Expiration, usage unique et verrous fichier ; non accepté par le web v0.7 |
| Dépendances / consommateurs | Fichiers locaux/Go ; seulement les tests dans l'intégration actuelle |
| Données / migration | État local du jeton ; aucune migration SQL automatique |
| Contrats / jobs | API de package historique ; aucun contrat web ou agent actif |
| Permissions / sécurité | Fichiers privés et contrôles de verrou ; jamais un repli SQL silencieux |
| Échec / cycle de vie | Refus des verrous dangereux/rejeux ; dépréciation/retrait explicites sans suppression d'état de production |
| Tests / supervision / limite | Tests Go réussis ; artefact historique, pas l'autorité actuelle du bootstrap |

## CMP-AGENT-TARGET — Futur agent système

État : `SPECIFIED`, non implémenté. Opérateurs et Symfony consommeront une API privée typée ; adaptateurs OS/services, jobs durables, verrous et audit sont les dépendances. Schéma du journal et contrat IPC ne sont pas finalisés. L'agent contrôle indépendamment le périmètre autorisé, isole un exécuteur privilégié minimal et reprend les opérations interrompues sans shell arbitraire. Installation/mise à jour/retrait exigent paquets signés, politiques systemd et tests par OS. L'acceptation nécessite authentification des pairs, refus, chemins sûrs, concurrence, reprise et santé des services. Aucun démon ou endpoint de supervision exécutable n'est fourni.

Toute nouvelle fiche conserve ces champs, y compris migrations/contrats absents, consommateurs, échecs, cycle de vie et limites de tests. Un détail manquant est signalé plutôt que remplacé par une fonction inventée.

## CMP-AGENT-TARGET — HANDOFF R3 des contrats candidats

Le futur agent Go et l'installateur doivent consommer uniquement des actions explicitement autorisées par les [fiches IPC `IPC-FP-0001..0012`](../08-api-contracts/symfony-go-ipc-r3.md) et le [registre `ACT-FP-0001..0007`](../../evidence/typed-agent-operations-v1.json), avec [cycle R3](../14-devops-releases/installer-lifecycle-r3.md). **Ce registre n'est pas un moteur activable** ; les deux actions système privilégiées restent bloquées et tout code exécutif dépend de R1/R2, des audits API/IPC/Security/DB, de tests de refus et de VM réelles. Aucun module ne peut s'attribuer un droit à root ou remplacer les contrats Core par ceux du Hub.

## CMP-AGENT-BOUNDARY-R3 — Fiches candidates de l'agent et du handler

La conception du Core doit suivre la [séparation des identités Linux](../14-devops-releases/linux-service-identities-r3.md) et les [garde-fous de l'agent](../08-api-contracts/typed-execution-recovery-r3.md). Aucun plugin/module ne peut contourner le [registre ACT-FP](../../evidence/typed-agent-operations-v1.json), créer des comptes root ou inscrire un handler privilégié. Un futur module de job dépend de la validation Database du [modèle physique](../09-database/physical-jobs-model-r3.md), des contrats API/IPC, de la sécurité et des tests VM ; les registres JSON ne sont pas un catalogue de fonctions exécutable. Les **deux handlers privilégiés restent bloqués**.
