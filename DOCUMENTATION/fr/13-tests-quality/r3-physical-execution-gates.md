<!-- forgepanel-doc id=FP-13-R3-PHYSICAL-QA revision=1 status=specified -->
# R3 — QA du modèle PostgreSQL, des identités Linux et des effets typés

[English](../../en/13-tests-quality/r3-physical-execution-gates.md) · [QA](README.md) · [Modèle DB](../09-database/physical-jobs-model-r3.md) · [Comptes Linux](../14-devops-releases/linux-service-identities-r3.md) · [Exécution](../08-api-contracts/typed-execution-recovery-r3.md)

**Les 36 scénarios suivants sont TOUS `PLANNED`. Aucun test SQL, IPC, Linux ou VM opérationnel n'a été exécuté dans ce lot.** Les tests Python de la CI GitHub vérifient uniquement la cohérence des contrats et des registres JSON proposés : ils ne remplacent ni un test de concurrence PostgreSQL ni une revue indépendante. Q1–Q170 inchangées, Q171+ sans réponse.

## A. PostgreSQL physique et jobs — 12 cas

| Test | Domaine | Chemin positif | Refus ou panne | État |
|---|---|---|---|---|
| `R3-PHYS-TEST-001` | Concurrence d'admission | Une intention et un job après deux demandes identiques | Double INSERT ne produit pas deux APPLY | **PLANNED** |
| `R3-PHYS-TEST-002` | Conflit clé/digest | Même clé/digest retrouve le même job | Même clé payload différent -> IDEMPOTENCY_CONFLICT | **PLANNED** |
| `R3-PHYS-TEST-003` | Scopes tenants | Scope serveur et tenant explicites/séparés | Null/wildcard et cross-tenant refusés | **PLANNED** |
| `R3-PHYS-TEST-004` | Commit avant ACK | Intent, job, audit, outbox atomiques | Échec commit n'émet jamais ACCEPTED | **PLANNED** |
| `R3-PHYS-TEST-005` | Unique par ressources | Une seule génération verrou par cible et scope | Deux workers mutateurs ne possèdent pas même lease | **PLANNED** |
| `R3-PHYS-TEST-006` | Fencing périmé | Worker actuel validé jusqu'à point d'effet | Ancien worker réveillé bloqué même si SQL bail expiré | **PLANNED** |
| `R3-PHYS-TEST-007` | Transition vers succès | VERIFYING et effet observé avant SUCCEEDED | QUEUED/RUNNING -> SUCCEEDED sans preuve refusé | **PLANNED** |
| `R3-PHYS-TEST-008` | Outbox double | Transport retry dédupliqué côté agent | ACK perdu n'applique pas de nouveau Linux | **PLANNED** |
| `R3-PHYS-TEST-009` | Deadlock / disponibilité | Transaction courte, reprise bornée après conflit | DDL/runtime SQL mélangés ou lock long refusés | **PLANNED** |
| `R3-PHYS-TEST-010` | Audit sans secrets | Journal d'étape corrélé et append-only | Credentials/cookies/tokens non journalisés | **PLANNED** |
| `R3-PHYS-TEST-011` | Rollback impossible | Rétablir uniquement étape réversible prouvée | SQL DDL irréversible ne produit pas faux rollback | **PLANNED** |
| `R3-PHYS-TEST-012` | Restauration d'état | Vérifier jobs et leases après restore PG | Vieilles identités/replays invalidés avant APPLY | **PLANNED** |

## B. Utilisateurs et services Linux — 12 cas

| Test | Domaine | Chemin positif | Refus ou panne | État |
|---|---|---|---|---|
| `R3-LINUX-TEST-001` | Inventaire non destructif | Détecter UID/GID/service existants sans mutation | Collision utilisateur/groupe refusée | **PLANNED** |
| `R3-LINUX-TEST-002` | Tenant vs panel | PHP-FPM tenant isolé du service Core | Tenant ne lit pas socket et secrets panel | **PLANNED** |
| `R3-LINUX-TEST-003` | Pont IPC isolé | Bridge identité exclusive et permissions contrôlées | Web runtime/plugin compromis ne s'approprie pas bridge | **PLANNED** |
| `R3-LINUX-TEST-004` | Agent non root | Go valide le canal et op sans privilège général | CAP_SYS_ADMIN, sudo et shell libre refusés | **PLANNED** |
| `R3-LINUX-TEST-005` | Exécuteur désactivé | Handler non créé ou désactivé par défaut | ACT-FP-0005/0007 ne deviennent pas disponibles | **PLANNED** |
| `R3-LINUX-TEST-006` | DB DDL/runtime | Rôle migrateur distinct du runtime SQL | Runtime ne possède pas tables et ne fait pas DDL | **PLANNED** |
| `R3-LINUX-TEST-007` | Socket protégé | Répertoire privé owner/type/mode validés | Symlink/inode remplacé/groupe partagé refusés | **PLANNED** |
| `R3-LINUX-TEST-008` | Peer UID et mandat | UID noyau ET preuve acteur/scope revérifiés | UID valide seul ne confère aucune autorisation | **PLANNED** |
| `R3-LINUX-TEST-009` | Profil systemd/LSM | Profil OS testé sans perte d'accès sûr | Profil cassant socket/recovery est refusé | **PLANNED** |
| `R3-LINUX-TEST-010` | Fencing au handler | Handler revalide generation/revision au point d'effet | Worker ancien ou plan stale ne mutent jamais Linux | **PLANNED** |
| `R3-LINUX-TEST-011` | Rotation / restart | Reconnexion seulement si nouvelle identité approuvée | Ancien FD/session/certificat refusé | **PLANNED** |
| `R3-LINUX-TEST-012` | Uninstall sécurité | Retirer uniquement comptes/services possédés | Détruire UID tenant ou dernier accès admin = veto | **PLANNED** |

## C. Autorisation par opération, effet et reprise — 12 cas

| Test | Domaine | Chemin positif | Refus ou panne | État |
|---|---|---|---|---|
| `R3-EXEC-TEST-001` | Action dans registre | Opération ACT-FP approuvée et handler dédié | shell.exec/argv/script_path impossible | **PLANNED** |
| `R3-EXEC-TEST-002` | Pair + acteur + scope | Vérifier pair/mandat/ressource avant effet | Hub licence, admin UI ou autre tenant refusé | **PLANNED** |
| `R3-EXEC-TEST-003` | Plan digest courant | Digest/signature/revision vérifiés au moment effet | Plan modifié/expiré => refus | **PLANNED** |
| `R3-EXEC-TEST-004` | Actions privilégiées | Handlers privilégiés restent bloqués | ACT-FP-0005/0007 ne passent jamais sans qualification | **PLANNED** |
| `R3-EXEC-TEST-005` | Fencing d'effet | Lock et génération revalidés par handler | Ancien worker/conflit ne produit pas second APPLY | **PLANNED** |
| `R3-EXEC-TEST-006` | PLAN/PREFLIGHT | Plan et impact sans mutation Linux | Port non géré/paquet inconnu => refus | **PLANNED** |
| `R3-EXEC-TEST-007` | Backup et approbation | Avant APPLY, backup/approval/digest vérifiés | Backup absent/clé inaccessible bloque | **PLANNED** |
| `R3-EXEC-TEST-008` | Vérification réelle | Santé fonctionnelle et effet observé avant SUCCESS | Code retour zéro ou service active ne suffit pas | **PLANNED** |
| `R3-EXEC-TEST-009` | Perte ACK/crash | Reprendre selon état PG + Linux réconciliés | APPLY incertain non rejoué aveuglément | **PLANNED** |
| `R3-EXEC-TEST-010` | Compensation sûre | Étape réversible avec checkpoint prouvé | SQL DDL/clé perdue ≠ rollback complet | **PLANNED** |
| `R3-EXEC-TEST-011` | Observabilité expurgée | Audit acteur/plan/effet sans secrets | Exporter token ou preuve privée interdit | **PLANNED** |
| `R3-EXEC-TEST-012` | Hub et compatibilité | Core fonctionne sans Hub et sur cible qualifiée | OS non qualifié, Hub root et version inconnue refusés | **PLANNED** |

## Conditions d'exécution réelle de cette campagne

**Préconditions successives :** source originale SRC-03 vérifiée/importée (R1) → runtime Symfony/PG avec MFA admin facultative validé (R2) → modèles Database/API/Security approuvés → packages/services signés, comptes/permissions dédiés, vrais sockets et handlers confinés → VMs jetables autorisées avec observations système et restauration.

**Par test exécuté** enregistrer : ID, commit SHA, environnement exact OS/arch/versions, image VM, policy/digest, acteur/tenant pseudonymisé, credential de pair vérifié (sans secret), acteur/permissions, requête et outbox/inbox, transaction avant/après, génération de fencing, changements Linux observés, logs expurgés, résultat positif/négatif, incident provoqué, cleanup/rollback/recovery et verdict `PASS/FAIL/BLOCKED/SKIP`. Un scénario marqué `SKIP` ou simplement décrit **n'est jamais PASS**.

**Veto absolus Q132 :** fuite inter-tenant, collision de ports, accès administrateur perdu, opération root arbitraire, absence de rollback récupérable quand promis et faux succès après crash. Pas de valeur numérique de timeout ou quotas inventée. Le Core public doit fonctionner sans Hub, et les deux opérations privilégiées `ACT-FP-0005/0007` sont toujours **bloquées**. Les lacunes `DOC-GAP-004/005/006` restent **OPEN** et les tests demeurent candidats avant les validations spécialisées.
