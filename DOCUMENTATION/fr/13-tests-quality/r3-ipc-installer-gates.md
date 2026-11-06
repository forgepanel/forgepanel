<!-- forgepanel-doc id=FP-13-R3-IPC-INSTALL-QA revision=1 status=specified -->
# R3 — Matrice de tests : IPC typé et installateur sécurisé

[English](../../en/13-tests-quality/r3-ipc-installer-gates.md) · [Qualité](README.md) · [Contrat IPC](../08-api-contracts/symfony-go-ipc-r3.md) · [Installateur](../14-devops-releases/installer-lifecycle-r3.md)

**Tous les 24 tests sont `PLANNED`, aucun PASS fonctionnel.** Les tests Python de parité contrôlent les identifiants et les JSON candidats ; **ils n'ouvrent aucun socket IPC, ne modifient pas Linux et ne démarrent aucune VM**. Les opérations privilégées restent `BLOCKED_UNTIL_QUALIFIED`. Les scénarios exigent une véritable source Foundation SRC-03, Symfony/PostgreSQL testés, un agent sécurisé validé et un hôte VM autorisé.

## A. IPC Symfony ↔ Go — 12 cas positifs et de refus

| Test ID | Domaine | Chemin positif | Refus / incident | Statut |
|---|---|---|---|---|
| `R3-IPC-TEST-001` | Auth pair | Pair IPC valide avec identité vérifiée | Refuser pair absent/spoof et champ actor falsifié | **PLANNED** |
| `R3-IPC-TEST-002` | RBAC/tenant | Opération autorisée pour acteur+ressource | Refuser cross-tenant, permission manquante, Hub comme root | **PLANNED** |
| `R3-IPC-TEST-003` | Registre fermé | Opération ACT-FP nommée et payload typé | Rejeter shell.exec, command, argv, champs inconnus | **PLANNED** |
| `R3-IPC-TEST-004` | Compatibilité | Version de contrat supportée et négociée | Version incompatible/ancien payload = refus | **PLANNED** |
| `R3-IPC-TEST-005` | Idempotence | Même clé+digest réutilise job précédent | Même clé avec payload différent = IDEMPOTENCY_CONFLICT | **PLANNED** |
| `R3-IPC-TEST-006` | Réponse perdue | Récupérer le job durable après commit | Pas de double activation après retransmission | **PLANNED** |
| `R3-IPC-TEST-007` | Révisions et verrou | Révision et lock de ressource valides | Refus stale revision/concurrence et lease expirée | **PLANNED** |
| `R3-IPC-TEST-008` | Timeout/retry | Transitoire retenté dans politique approuvée | Timeout irréversible non rejoué aveuglément | **PLANNED** |
| `R3-IPC-TEST-009` | Crash de l'agent | Récupérer état voulu/observé après redémarrage | Refuser succès sans preuve de VERIFY | **PLANNED** |
| `R3-IPC-TEST-010` | Expurgation | Audit horodaté corrélé sans secrets | Refuser fuite cookies/tokens/credentials DB | **PLANNED** |
| `R3-IPC-TEST-011` | Plans signés | Plan et permissions vérifiés au moment de l'effet | Refuser plan altéré ou approbation expirée | **PLANNED** |
| `R3-IPC-TEST-012` | Hub indisponible | Core continue localement hors Hub | Refuser endpoint privilégié Hub, aucune dépendance forcée | **PLANNED** |

## B. Installation sécurisée — 12 cas positifs et de refus

| Test ID | Domaine | Chemin positif | Refus / incident | Statut |
|---|---|---|---|---|
| `R3-INSTALL-TEST-001` | Confiance signature | Manifest + paquets signés et octets vérifiés | Refuser racine inconnue, hash faux et clé révoquée | **PLANNED** |
| `R3-INSTALL-TEST-002` | Fraîcheur/rejeu | Métadonnées autorisées et non rétrogradées | Refuser ancien canal/rejeu/expiration | **PLANNED** |
| `R3-INSTALL-TEST-003` | Compatibilité OS | Préflight OS/version/arch sur VM autorisée | Refuser OS non qualifié sans sélection automatique | **PLANNED** |
| `R3-INSTALL-TEST-004` | Services existants | Inventaire et plan d'adoption validé | Ne pas écraser fichier, listener ou compte non géré | **PLANNED** |
| `R3-INSTALL-TEST-005` | Snapshot/backup | Point de restauration et clé accessibles | Refuser APPLY sans sauvegarde requise vérifiée | **PLANNED** |
| `R3-INSTALL-TEST-006` | Autorisation APPLY | Opération typée validée sur plan approuvé | Refuser root shell, plan expiré, autre tenant | **PLANNED** |
| `R3-INSTALL-TEST-007` | Paquets et interruption | Staging puis reprise idempotente | Coupure réseau/espace disque ne crée pas faux succès | **PLANNED** |
| `R3-INSTALL-TEST-008` | Health et HTTPS | Panneau, DB, agent, TLS, admin vérifiés | Service active mais portail inaccessible = FAIL | **PLANNED** |
| `R3-INSTALL-TEST-009` | Port/firewall | Admin reste accessible après changement | Perte de dernier accès administrateur = veto | **PLANNED** |
| `R3-INSTALL-TEST-010` | Compensation sûre | Restaurer uniquement étapes réversibles connues | DDL SQL irréversible ne produit pas rollback fictif | **PLANNED** |
| `R3-INSTALL-TEST-011` | Mises à jour/reprise | Réinstallation/upgrade et restart documentés | Crash après apply exige RECOVER ou preuve réelle | **PLANNED** |
| `R3-INSTALL-TEST-012` | Publication/évidence | Preuve VM exacte signée avant promotion | SKIP/fixtures/dossier docs ne valent pas PASS | **PLANNED** |

## Preuve requise pour toute campagne ultérieure

Chaque test exécuté doit avoir : ID, commit SHA testé, source et signatures/empreintes exactes, OS/architecture/version, profil WebStack le cas échéant, versions PHP/Go/Symfony/PostgreSQL, politique/revision/idempotency, identité du pair et acteur/tenant (pseudonymisés), étape/install plan, logs expurgés, effet Linux réellement observé, résultat négatif attendu/observé, état de récupération/cleanup, auteur de revue et verdict `PASS/FAIL/BLOCKED/SKIP`.

**Séparer au minimum :** tests unitaires de parseurs, intégration IPC réelle (socket authentifié), transactions/contraintes PostgreSQL avec concurrence, erreurs d'agent, OS disposable-VM avec systemd/permissions/AppArmor ou SELinux, vrai HTTPS/retour arrière et non-régression. Les tests conteneur et la documentation ne remplacent pas les VMs. Ne pas imposer de limites CPU/RAM/TTL commerciales inventées ; la politique de test devra être définie et approuvée.

## Gates préalables et responsabilités

**R1 :** source vraie et licences vérifiées (issue #2). **R2 :** Symfony/PG et identité avec MFA facultative (issues #3 et #6). **R3 :** contrat IPC signé/ratifié, modèle de job et utilisateurs Linux minimaux, installateur et source de packages signés ; tests VM comparatifs et critères éliminatoires Q132. **R4 :** premier site PHP/HTTPS réel, SFTP et restauration isolée ; les gates restant après R3 demeurent ouverts. Hub privé ne peut jamais déclencher du root sur les installations.

**Critère d'avancement documentaire uniquement :** les [contrats candidats](../08-api-contracts/symfony-go-ipc-r3.md) et [états de l'installateur](../14-devops-releases/installer-lifecycle-r3.md) couvrent les exigences par ID, avec [registre d'opérations](../../evidence/typed-agent-operations-v1.json). Ne fermer ni `DOC-GAP-005`, ni `DOC-GAP-006` avant revue, code et tests réels. Q1–Q170 inchangées ; Q171+ ouvertes.
