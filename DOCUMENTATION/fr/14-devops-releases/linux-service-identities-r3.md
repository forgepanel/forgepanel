<!-- forgepanel-doc id=FP-14-R3-LINUX-IDENTITY revision=2 status=specified -->
# R3 — Comptes et services Linux : séparation des responsabilités candidate

[English](../../en/14-devops-releases/linux-service-identities-r3.md) · [DevOps](README.md) · [Confiance IPC](../08-api-contracts/local-peer-trust-r3.md) · [Exécution typée](../08-api-contracts/typed-execution-recovery-r3.md) · [QA](../13-tests-quality/r3-physical-execution-gates.md)

**Autorité : DevOps / Build / Release et Security / Hardening, avec API/IPC et Database. Statut SPECIFIED / CANDIDATE.** Aucun compte Linux, groupe, socket systemd, unité de service ou privilège n'est créé. Les noms des comptes, chemins filesystem, règles LSM et versions de distributions restent **à ratifier sur une VM autorisée**, après R1 Foundation v0.7 et R2 Symfony/PG. Les 12 exigences `LINUX-FP-0001..0012` décrivent les **frontières de sécurité**, pas une configuration appliquée. Q1–Q170 et l'autonomie du Core hors Hub demeurent obligatoires.

## Douze invariants de séparation

**LINUX-FP-0001 — Acteurs séparés.** Distinguer administrateur système Linux, rôle DDL PostgreSQL, runtime Symfony, processus pont IPC, agent Go non-root, exécuteur minimal privilégié *futur*, lecteur de supervision et utilisateur Unix d'un site client. **Un Super Administrateur dans Symfony n'est pas Linux root**. Il n'existe jamais de privilège déduit automatiquement d'une licence/du Hub.

**LINUX-FP-0002 — Frontière Symfony/browser.** Symfony reçoit HTTPS/session/CSRF et vérifie RBAC, organisation et propriétaire de la ressource avant émission de l'intention. Les travailleurs PHP des sites hébergés, scripts d'un tenant, plugins et webhooks **n'ont pas accès** au canal de contrôle du serveur. La séparation effective du runtime panneau/tenants doit être vérifiée.

**LINUX-FP-0003 — Pont IPC isolé.** Un processus de pont **distinct des pools PHP clients et des applications tierces** détient si nécessaire le droit de connexion au socket privé. Son UID/GID et son périmètre filesystem doivent être minimalistes ; son existence ne remplace pas la validation indépendante de l'acteur par Go. L'accès direct du runtime web général est un **risque à auditer**, pas un privilège accordé par défaut.

**LINUX-FP-0004 — Agent Go sans privilège global.** Le service agent observe les capacités, vérifie schémas, plan/digest, identité du pair et périmètre, sans shell générique, `sudo` libre ni `CAP_SYS_ADMIN`. N'accorder aucun groupe large donnant accès aux contenus clients. Les actions sensibles éventuelles sont déléguées à des handlers dédiés, soumis à autorité explicite.

**LINUX-FP-0005 — Exécuteur privilégié bloqué.** Un exécuteur minimal *pourra* être conçu uniquement après revue d'architecture et threat model ; il n'existe pas aujourd'hui. Il n'accepte que **l'identifiant d'une opération ACT-FP approuvée et son plan/version/ressource**. Les deux opérations `ACT-FP-0005` et `ACT-FP-0007` restent `BLOCKED_UNTIL_QUALIFIED`. Aucun champ shell, script libre, chemin exécutable téléchargé ou argument brut QEMU.

**LINUX-FP-0006 — Comptes PostgreSQL distincts.** Provisionner potentiellement un rôle de migration DDL, un utilisateur DB runtime Symfony, un service job/dispatcher et un lecteur d'audit séparés. Le runtime ne doit posséder ni table ni privilège de migration ou de création de rôle. Les rôles SQL ne doivent pas être confondus avec les UID Linux ou sessions d'administration.

**LINUX-FP-0007 — Socket et filesystem.** Candidat : socket de domaine Unix dans un **répertoire d'exécution privé** contrôlé par systemd, avec owner/type/mode et groupes revus. Tout path est canonique, contrôlé contre symlinks et remplacement de nœud ; une permission de groupe ne donne pas confiance si ses membres sont inconnus. La forme d'exemple `/run/forgepanel/agent.sock` est **illustrative seulement** ; aucun chemin officiel retenu.

**LINUX-FP-0008 — Identité du pair.** Vérifier sur Linux des credentials **rapportés par le noyau** (`SO_PEERCRED` candidat) et l'identité de l'instance du processus, sans se fier à un UID/PID dans le JSON. En cas de redémarrage/PID réutilisé/FD transféré/credential rotation, le canal doit revoir les droits. UID de service validé ≠ permission d'un utilisateur final : obligation de mandat scoped séparé.

**LINUX-FP-0009 — Sandbox systemd/LSM.** Prévoir un profil **à tester** avec `NoNewPrivileges`, `PrivateTmp`, `ProtectSystem`, `ProtectHome`, `RestrictAddressFamilies`, `CapabilityBoundingSet`, limites CPU/mémoire/tâches, AppArmor ou SELinux selon OS. Les paramètres concrets doivent être mesurés et vérifiés : une option cassant l'accès au socket, au réseau nécessaire ou à la récupération doit être refusée. `DynamicUser` **n'est pas choisi** implicitement (besoin possible d'UID stable pour socket/état).

**LINUX-FP-0010 — Fencing au point d'effet.** Un ancien worker ne doit pas pouvoir réussir après transfert de bail. Le handler système revalide l'identité de la ressource, la révision, le propriétaire du lock et la génération de fencing **à l'instant de la mutation**, avec un mécanisme réellement applicable (pas un simple champ JSON). Sinon **bloquer la mutation**, même si PostgreSQL indique un nouveau propriétaire.

**LINUX-FP-0011 — Secrets, logs, recovery.** Identité de service et clés IPC dans un stockage non partagé et avec rotation/révocation ; aucune clé privée de signature éditeur dans le Core distribué. Journaux corrélés mais expurgés, rétention réglable validée ; la voie d'administration locale de secours doit survivre à l'arrêt de l'agent, de PostgreSQL ou du Hub et rester auditée.

**LINUX-FP-0012 — Install/update/revoke.** N'introduire compte/unité/permission que par package signé et plan de changement revu, réversible si possible, avec sauvegarde, vérification et fermeture des anciennes connexions. La désinstallation/réinstallation ne doit ni supprimer arbitrairement des UID clients, ni réutiliser une identité de service non approuvée. Tester les modes échoués sur Debian/Ubuntu/AlmaLinux **avant d'affirmer un OS supporté**.

## Matrice des identités candidates — aucune création aujourd'hui

| Identité logique (nom Unix final ouvert) | Propriété | Ne doit pas posséder |
|---|---|---|
| `panel_http` | Symfony/Core HTTP, sessions et RBAC utilisateur | root, DDL, API shell, fichiers tenant hors scope |
| `panel_ipc_bridge` | Transport privé, preuve d'instance, demandes bornées vers Go | droits tenant hébergé, clé de signature éditeur, package manager |
| `panel_agent` | Go non-root, validation typed operations, observations/readiness | pouvoir root global, arbitraire `exec`, secrets hébergement |
| `panel_privileged_handler` | **FUTUR BLOQUÉ** : effet système allowlisté et audité | shell libre, accès Hub, opérations non approuvées |
| `panel_migrator` | Migrations PostgreSQL checksumées sous maintenance | session web, droits runtime permanents |
| `panel_db_runtime` | Écritures SQL autorisées de l'application avec tenant scope | DDL/ownership, superuser SQL, tables hors domaine |
| `hosted_site_user` | Site client, fichiers/worker PHP/SFTP dans sa portée | socket Go, config du panneau, autres tenants |
| `panel_observer` | Métriques/health/logs expurgés selon autorisation | secrets, mutation, grant d'installation |

Les étiquettes sont des **alias logiques** sans réservation de comptes système. L'identité `panel_privileged_handler` n'autorise **aucune activation** dans ce lot. Les permissions DB et groupes Linux demandent des preuves d'isolation en VM, notamment avec PHP-FPM et les groupes SFTP.

## Installation et révocation — séquence candidate

1. Inventorier comptes, GIDs, services, socket/ports, fichiers non gérés et permissions sur la cible **sans mutation**.
2. Valider l'OS précis et le plan de package signé, les dépendances, l'absence de collision de compte/groupe et la sauvegarde/voie d'urgence.
3. Soumettre l'ajout de services/comptes à un contrat typé, approuvé et durable sous Q47 : `PLAN → PREFLIGHT → SNAPSHOT → STAGE → APPLY → VERIFY/RECOVER`. Les handlers privilégiés restent bloqués.
4. Tester par utilisateur hébergé malveillant : impossibilité d'atteindre le socket et les journaux; par bridge compromis : impossibilité d'élever ses droits sans mandat.
5. Après rotation, vérifier rejet des anciennes sessions, nettoyage des permissions **seulement celles appartenant au produit**, sauvegardes conservées selon règles approuvées.
6. Un système non récupérable ou le dernier accès administrateur perdu produit veto Q132, jamais PASS.

## Preuves nécessaires et HANDOFF

[Les 12 scénarios `R3-LINUX-TEST-001..012`](../13-tests-quality/r3-physical-execution-gates.md) sont tous **PLANNED**. Un test de permission dans un conteneur ou un fichier Markdown ne certifie ni confinement SELinux/AppArmor ni séparation tenant. Security doit signer la revue d'UID/canal/LSM ; DevOps les packages/systemd/OS; API/IPC l'identité observée; Database la séparation DDL/runtime; QA les VMs et tests de régression. **Aucune action root n'est produite ici.**

## R3 — Gestion des générations après restore et reprise de services

La [revue d'intégrité des jobs](../19-audits-risks/r3-job-integrity-audit.md) exige qu'un service Linux ne réaccepte **jamais** une ancienne capacité de mutation après restauration PostgreSQL, suppression d'un bail, redémarrage de l'agent ou remplacement de son socket. Le futur handler devra vérifier l'époque/génération **au point d'effet**, dans un domaine de confiance ne pouvant être rétrogradé silencieusement avec la DB. Le mécanisme est **à concevoir et tester**, pas fourni par `fencing_epoch_ref`. En attendant : `ACT-FP-0005/0007` bloquées et aucune reprise privilégiée automatique.
