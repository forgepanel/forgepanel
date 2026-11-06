<!-- forgepanel-doc id=FP-13-APP-CONFIG revision=2 status=specified -->
# App Center Configuration Center — critères de tests réels

[English](../../en/13-tests-quality/app-center-configuration-gates.md) · [QA](README.md) · [Spécification d'héritage](../02-architecture/app-center-config-inheritance.md) · [Q180/Q220](../00-project-control/decisions-q171-q220.md)

**PLANNED / NON EXÉCUTÉS.** Ces 16 cas spécialistes complètent les 50 critères de haut niveau Q171–Q220 validés par le propriétaire. Ils ne les remplacent pas et le fichier Python fictif ne prouve aucune fonction produit.

| ID | Famille | Résultat attendu | Statut |
|---|---|---|---|
| TEST-CONFIG-FP-0001 | Inheritance and provenance | Héritage global→serveur→organisation→plan→site et provenance réelle par scope | PLANNED |
| TEST-CONFIG-FP-0002 | No widening of parent policy | Un site ne réactive pas les conteneurs interdits par le plan parent | PLANNED |
| TEST-CONFIG-FP-0003 | Physical quota enforcement | Quota tenant/site plafonné par CPU/RAM/PIDs/stockage réellement disponibles | PLANNED |
| TEST-CONFIG-FP-0004 | Immutable native-free Core policy | Natif gratuit sans entitlement, Docker/Podman, connexion Hub ou paiement | PLANNED |
| TEST-CONFIG-FP-0005 | Immutable Linux security controls | RBAC, isolation, IPC Go typé, signatures et ports ne peuvent être désactivés | PLANNED |
| TEST-CONFIG-FP-0006 | Revision and concurrency | Deux modifications concurrentes, révision périmée refusée et auditée | PLANNED |
| TEST-CONFIG-FP-0007 | Effective policy explanation | L'UI affiche provenance, délégation, impact et verrouillage sans secrets | PLANNED |
| TEST-CONFIG-FP-0008 | Tenant privilege separation | PANEL n'édite ni FORGE/global, ni serveur, ni autre client ni Hub privé | PLANNED |
| TEST-CONFIG-FP-0009 | Trusted host capability provenance | Capacités hôte authentifiées, fraîches et liées au serveur, pas à la demande client | PLANNED |
| TEST-CONFIG-FP-0010 | Plan vs apply isolation | Simulation sans allocation port, job, écriture SQL/fichier ou lancement conteneur | PLANNED |
| TEST-CONFIG-FP-0011 | Q47 guarded apply | Q47 : plan, validation, snapshot, approbation, santé et récupération/compensation | PLANNED |
| TEST-CONFIG-FP-0012 | Port collision and recovery | Ports FORGE 8447/PANEL 8446 réservés ; changement préserve l'accès de secours | PLANNED |
| TEST-CONFIG-FP-0013 | Signature and catalog policy | Recette non revue malgré signature ne contourne ni moteurs ni politique partenaires | PLANNED |
| TEST-CONFIG-FP-0014 | Optional consent/telemetry | Consentements Hub séparés ; retrait ne bloque pas One-Click natif gratuit | PLANNED |
| TEST-CONFIG-FP-0015 | Scope extension contract | Overrides compte/utilisateur ne diminuent pas les protections serveur/plan ni isolation | PLANNED |
| TEST-CONFIG-FP-0016 | Rollback under partial failure | Reprise de config versionnée signale irréversibilité, conserve données et enregistre état partiel | PLANNED |

## Preuves nécessaires

Chaque PASS exige commit Core/Go/PostgreSQL, acteur/tenant, OS/capacités mesurées, révisions, essais positifs/négatifs, verrous, audit expurgé, backup/restauration ou récupération et revue indépendante. SKIP/BLOCKED ne signifie pas PASS. One-Click natif reste gratuit sans Hub et les droits Docker/Podman séparés. Aucun de ces tests n'a été exécuté sur app, port HTTPS, tenant ou VM réels.
