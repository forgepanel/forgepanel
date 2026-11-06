<!-- forgepanel-doc id=FP-08-R3-IPC revision=3 status=specified -->
# R3 — Contrats candidats Symfony ↔ agent Go : IPC, autorisation et opérations typées

[English](../../en/08-api-contracts/symfony-go-ipc-r3.md) · [API](README.md) · [Installateur R3](../14-devops-releases/installer-lifecycle-r3.md) · [QA R3](../13-tests-quality/r3-ipc-installer-gates.md)

**Statut : SPECIFIED / CANDIDATE — aucune route, socket, démon, requête privilégiée ou migration exécutables.** Propriétaire : API / IPC / Contracts ; revues obligatoires Security, Core, Database, DevOps et QA. Exigences `IPC-FP-0001` à `IPC-FP-0012`, reliées à Q47/Q61/Q62/Q66/Q120, [DOC-GAP-005/006](../00-project-control/documentation-readiness.md) et aux [issues #9](https://github.com/yyogas/forgepanel/issues/9) et [#15](https://github.com/yyogas/forgepanel/issues/15). **Q1–Q170 inchangées ; Q171+ sans arbitrage.** Les transports, comptes Linux, schémas PostgreSQL, valeurs numériques et versions définitives restent à ratifier après l'import des véritables sources SRC-03 (issue #2).

## Frontières de confiance et responsabilités

```text
Navigateur non fiable ─HTTPS─> Symfony (sessions, CSRF, RBAC, quotas/politiques)
                                ├── PostgreSQL : intent, job, audit durable (à définir)
                                └── IPC privé et authentifié (candidat)
                                    └── Go non-root : validation indépendante des politiques
                                        └── opérations système nommées / adaptateurs bornés
                                            └── Linux : privilèges minimaux, journalisation
Hub privé ── client externe facultatif et limité ──> contrats Core publics futurs
```

**IPC-FP-0001 — Séparation des privilèges.** L'identité du Super Administrateur Symfony n'est ni l'utilisateur Linux root, ni une identité IPC privilégiée. Un compte Hub, une extension ou un webhook ne devient jamais acteur privilégié. Aucun accès root depuis le navigateur.

**IPC-FP-0002 — Authentification du pair.** Le plan local candidat utilisera un **socket Unix privé avec vérification de l'identité du processus/pair**, protection du socket/fichiers et séparation des comptes ; un agent distant exigerait une identité mutuelle et une revue de protocole distincte. Le mécanisme précis (credentials Unix, rotation, reconnect, mTLS distant) est **ouvert**. L'assertion `actor_id` fournie par Symfony ne suffit **jamais** à authentifier un pair.

**IPC-FP-0003 — Autorisation à deux niveaux.** Symfony valide acteur, rôle, tenant/organisation, plan, consentements, approbation et propriété de la ressource avant de soumettre une intention. Go **revalide indépendamment** l'opération, la portée, la cible, la politique et les capacités du serveur. Les permissions commerciales ne confèrent aucun privilège Linux.

**IPC-FP-0004 — Registre fermé d'opérations.** Une opération existe uniquement si elle est inscrite dans le [registre candidat](../../evidence/typed-agent-operations-v1.json) et dispose d'une fiche, d'un validateur strict, d'une permission et d'un test négatif. **Interdiction absolue** : `shell.exec`, `exec arbitrary command`, `run arbitrary command`, chemins de script arbitraires, arguments QEMU ou shell transmis par API, code PHP/JS à exécuter sous root. Un nom d'opération ne peut pas être interprété dynamiquement comme une commande OS.

## Enveloppes candidates — schémas à ratifier

Deux **JSON Schema Draft 2020-12 candidats** précisent l'enveloppe d'une [requête typée](../../evidence/candidate-ipc-request-v1.schema.json) et d'une [réponse/admission/job](../../evidence/candidate-ipc-response-v1.schema.json). Ils refusent les champs inconnus et imposent un payload typé par nom d'opération ; **la validation de schéma ne remplace ni l'authentification du pair ni une autorisation Linux**, et ces fichiers ne sont pas intégrés à un endpoint. Les opérations privilégiées demeurent bloquées dans le registre même si leur forme JSON est valide.

**IPC-FP-0005 — Requête.** Toute demande porte au minimum : `contract_version`, `operation_id` **dans le registre**, `request_id`, `correlation_id`, `idempotency_key`, acteur/tenant/cible vérifiables, `expected_revision`, `policy_revision`, `deadline`, et **payload typé propre à l'opération**. Le canal ne transmet pas de mots de passe ni de secrets bruts ; seuls identifiants de références protégées sont permis. Les noms et types ci-dessus sont **candidats**, pas un endpoint disponible.

**IPC-FP-0006 — Réponse et erreurs.** Réponse typée `ACCEPTED`, `DENIED` ou `REJECTED` pour l'admission, et statut durable du job indépendant : `QUEUED`, `RUNNING`, `VERIFYING`, `SUCCEEDED`, `FAILED`, `COMPENSATION_REQUIRED`, `BLOCKED`. Aucune réponse `ACCEPTED` ne signifie que Linux a été modifié ou que `VERIFY` est passé. Nomenclature candidate des erreurs : `UNAUTHENTICATED`, `FORBIDDEN`, `SCOPE_DENIED`, `INVALID_INPUT`, `STALE_REVISION`, `IDEMPOTENCY_CONFLICT`, `RESOURCE_LOCKED`, `CAPABILITY_UNAVAILABLE`, `TRUST_FAILURE`, `TIMEOUT`, `DEPENDENCY_UNAVAILABLE`, `PARTIAL_FAILURE`, `RECOVERY_REQUIRED`. Ne jamais rendre une stack trace/chaîne SQL ou un secret au client.

**IPC-FP-0007 — Idempotence et limites.** L'identité `(operation_id, scope, idempotency_key, payload_digest)` est conservée durablement après décision de la politique et avant ACK asynchrone. Le même tuple peut retrouver l'état précédent ; **même clé avec charge différente = conflit**, pas nouvelle exécution. Les délais, taille de message, limite de jobs, période de conservation, politique de retry et bail de verrou restent **paramètres à approuver**. Retry uniquement sur codes transitoires explicitement éligibles, sous budget borné ; aucun « exactly once » garanti entre DB et Linux.

**IPC-FP-0008 — Journal durable et crash.** Chaque transition d'état doit être enregistrée avec `request_id`, acteur et autorité, version de contrat, révisions, cible, horodatage, identité du plan, étape, tentative, cause expurgée et résultat observé. Le job est récupéré après redémarrage sans relancer aveuglément une mutation irréversible. La perte de réponse après commit se résout par lecture du même job et non par second apply.

**IPC-FP-0009 — Verrous et concurrence.** Un plan/étape ciblant une ressource détient un verrou borné + vérifie sa révision/son identité observée. Les opérations concurrentes affectant listener, paquet, compte Linux, site ou service ne s'écrasent pas. Un verrou expiré n'autorise pas automatiquement un nouveau apply : reconciler état voulu/observé et vérifier le résultat précédent.

**IPC-FP-0010 — Sécurité des entrées/sorties.** Le parseur refuse champs inconnus, chemins non canoniques, symlinks/TOCTOU, injection de lignes de commande, URLs non approuvées/SSRF et valeurs hors plafonds. Les fichiers Linux préexistants non gérés ne peuvent pas être adoptés/écrasés sans plan et approbation. Logs JSON structurés avec expurgation des clés, jetons, cookies, secrets MFA et contenus clients.

**IPC-FP-0011 — Cycle Q47.** Les mutations sensibles suivent `DRAFT → PLAN → PREFLIGHT → SNAPSHOT → APPLY → VERIFY → COMMIT` ou `RECOVER`, avec étape de staging distincte si nécessaire ; chaque transition a des critères d'arrêt. Une transaction PostgreSQL **ne rend jamais un changement Linux atomique**. L'agent n'effectue que des actions explicitement autorisées dans un plan lié à un hash, une révision et une durée de validité ; les étapes non réversibles exigent approbation ciblée et chemin de récupération.

**IPC-FP-0012 — Versioning, mise à jour et santé.** Version de schéma négociée explicitement, incompatibilité = refus ; dépréciation annoncée avant changement. `liveness` n'implique pas `readiness` : DB, agent, clés et canal d'administration doivent être évalués séparément. Panne Hub = Core toujours autonome. Aucun contrat IPC « public » activé par la simple présence de ce document.

## Fiches d'opérations candidates — application interdite aujourd'hui

| ID | Opération logique | Classe | Condition principale | État |
|---|---|---|---|---|
| ACT-FP-0001 | `host.capabilities.observe` | Lecture seule | pair local autorisé, chemins de lecture fixes | CANDIDATE |
| ACT-FP-0002 | `artifact.signature.verify` | Lecture seule | clé de confiance indépendante, contenu signé + SHA | CANDIDATE |
| ACT-FP-0003 | `installer.plan.compile` | Lecture seule | schéma/politique/OS/compatibilité vérifiés | CANDIDATE |
| ACT-FP-0004 | `installer.stage_verified_packages` | Staging borné | manifeste vérifié, répertoire privé et quotas | CANDIDATE |
| ACT-FP-0005 | `installer.activate_signed_generation` | Privilégié borné, futur | plan signé/autorisé, backup, verrou, approbations, environnement qualifié | **NON AUTORISÉ** |
| ACT-FP-0006 | `installer.health.check` | Lecture seule | identité/service/plan explicités, pas de données tenant | CANDIDATE |
| ACT-FP-0007 | `installer.compensate_generation` | Privilégié borné, futur | checkpoint sûr, autorité explicite, audit, refus d'opérations irréversibles | **NON AUTORISÉ** |

Le registre décrit des *actions métier typées*, **pas** une API Go, une migration, une CLI ou un exécuteur opérationnel. Les deux actions privilégiées sont purement conceptuelles et bloquées jusqu'à autorisation architecturale/sécurité, implémentation dédiée et qualification VM. Aucun argument `command`, `argv`, `script_path` ou `shell` dans le contrat.

## HANDOFF et preuves

- **Database** : modèle concret de job/locks/idempotence/audit, migrations, rétention et concurrence **non finalisés** ; aucun schéma inventé.
- **Security** : authentification transport/pair, RBAC/tenant, secret storage, règles d'élévation et threat model à examiner ; aucune API root générique.
- **DevOps** : séparation utilisateur/paquets/release, allowlist et procédures d'install/reprise dans [l'installateur R3](../14-devops-releases/installer-lifecycle-r3.md).
- **QA** : [`R3-IPC-TEST-001..012`](../13-tests-quality/r3-ipc-installer-gates.md) **PLANNED** ; tests de refus cross-tenant, replay, crash, mutation concurrente, perte de réponse, compatibilité et sécurité.

**La clôture de `DOC-GAP-006` n'est pas acquise.** Ratifier contrats, schémas réels et périmètres, implémenter en PHP/Go après R1/R2, puis prouver les refus sur une VM autorisée ; ce document est une spécification candidate, sans revue indépendante encore obtenue.

## Précisions documentaires : pair authentifié et job durable

La [fiche de confiance du pair](local-peer-trust-r3.md) distingue la preuve du canal Unix/Linux, l'identité de processus et le mandat d'un acteur Symfony : le champ actor_claim d'une [requête candidate](../../evidence/candidate-ipc-request-v1.schema.json) n'est **pas** un credential. Le [contrat de persistance](../09-database/durable-jobs-r3.md) précise commit avant ACK, clé d'idempotence/payload digest, fencing monotone, outbox et correction d'effet incertain après crash. [24 nouveaux scénarios PLANNED](../13-tests-quality/r3-jobs-peer-gates.md) couvrent les refus. **Aucun endpoint n'est activé et ACT-FP-0005/0007 restent bloquées.**
