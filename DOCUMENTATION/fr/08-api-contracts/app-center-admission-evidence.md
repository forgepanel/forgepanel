<!-- forgepanel-doc id=FP-08-APP-EVIDENCE revision=1 status=specified -->
# App Center — liaison des preuves, révisions et fraîcheur avant installation

[English](../../en/08-api-contracts/app-center-admission-evidence.md) · [Contrats API](README.md) · [Configuration Q180/Q220](../02-architecture/app-center-config-inheritance.md) · [Frontière sécurité](../10-security/app-center-admission-trust-boundary.md)

**SPÉCIFICATION CANDIDATE / NON IMPLÉMENTÉE / TESTS RÉELS NON EXÉCUTÉS.** Q180 et Q220 approuvées imposent la configuration héritée, des droits et une application sécurisée. Ce contrat propose des preuves **séparées** hôte/autorisation/politique/demande pour App Center. Ce n'est ni un IPC authentifié, ni un Voter Symfony réel, ni une API de production, ni un agent Go, ni un contrôle de signature ou une permission d'installation.

## Quatre sources distinctes

| Preuve | Future source de confiance | Contrôles candidats | Jamais fourni par |
|---|---|---|---|
| **Observation du serveur** | Agent Go local authentifié et borné au serveur | ID hôte, version/snapshot, ressources libres mesurées, moteurs qualifiés, ports protégés/en écoute, heure/fraîcheur | Navigateur, catalogue Hub, licence commerciale |
| **Autorisation Core** | Symfony authentifié et RBAC tenant/acteur/site réel | Acteur, organisation, hôte, droits site, scopes distincts natif/conteneurs, révision et durée | Sonde Linux, rôle fourni par client, métadonnées Hub |
| **Politique effective Core** | Configuration Center versionné local, autorisé | Hôte, révision, moteurs autorisés, pilotes qualifiés, plafonds effectifs, fraîcheur | Règles éditeur Hub, texte du client, recette non signée |
| **Intention utilisateur** | Demande navigateur/API non fiable, normalisée par Core | Références hôte/tenant/acteur/site, famille de recette/pilote, révisions attendues, ressources et ports, identifiant idempotence | Jamais preuve d'un droit ou d'une capacité matérielle |

L'égalité de références hôte/tenant/révision **ne prouve pas l'identité des producteurs**. L'intégration réelle devra vérifier identité IPC/agent et hôte cible, session et droits actuels, provenance/signature, révisions et horloge de confiance. Le One-Click natif reste gratuit sans Hub/Docker/Podman ; Container Apps conserve ses ressources et pilotes qualifiés indépendants.

## Exigences candidates avant APPLY

| ID | Frontière à respecter |
|---|---|
| EVID-FP-0001 | Provenance par observation hôte, autorisation Symfony et politique Core authentifiées séparément, jamais JSON client |
| EVID-FP-0002 | Acteur, tenant, site et serveur concordants après contrôle des droits et de la propriété des ressources |
| EVID-FP-0003 | Versions host/RBAC/policy et révisions attendues comparées, non rejouables |
| EVID-FP-0004 | Durées de validité et dérive d'horloge bornées, mais **TTL/stratégie d'horloge précis OUVERTS** |
| EVID-FP-0005 | Source périmée, absente, future, incohérente ou non fiable → refus sûr ; JSON correct ≠ autorisation |
| EVID-FP-0006 | Droits natif/conteneurs séparés, sans fallback ni mélange de ressources |
| EVID-FP-0007 | Compatibilité Docker/Podman et capacité réellement qualifiées sur hôte ; Docker seul ne certifie pas Podman |
| EVID-FP-0008 | Ports système **FORGE 8447** et **PANEL 8446** réservés même si omis dans une demande |
| EVID-FP-0009 | Exposition réseau et réservation nécessitent politique locale revue et contrôle atomique |
| EVID-FP-0010 | Un aperçu ne devient jamais autorisation APPLY, job Linux, jeton de capacité, signature ou preuve de pose |
| EVID-FP-0011 | APPLY revalide identité/politique/capacités, utilise verrous/fencing DB/ressources et jobs durables idempotents ; **non implémenté** |
| EVID-FP-0012 | Core conserve données et droits Linux ; Hub ne remplace ni observation serveur, ni RBAC Core, ni gratuité native |

Aucune API générique `shell.exec`, commande root libre ou action directe Hub→Go. Une empreinte SHA-256 syntaxiquement correcte ou un snapshot local plausible ne prouve aucune signature. L'idempotence réelle nécessitera stockage atomique de la clé et du digest canonique ; le prototype vérifie seulement la forme.

## Référence synthétique autonome

Le [contrôle hors ligne](../../../scripts/check_app_center_candidate_evidence.py) lit seulement deux exemples fictifs embarqués : [natif](../../../evidence/app-center-fixtures/admission-native.synthetic.json) et [conteneurs](../../../evidence/app-center-fixtures/admission-container.synthetic.json). Tous utilisent une **horloge fictive**, des sources `SYNTHETIC_UNVERIFIED` pour hôte/droits/politique et une intention `UNTRUSTED_CLIENT_FIXTURE`. Horodatages, révisions, CPU/RAM et identités sont **des valeurs QA fictives**, pas des paramètres de production.

```sh
python3 scripts/check_app_center_candidate_evidence.py --fixture native
python3 scripts/check_app_center_candidate_evidence.py --fixture container
python3 tests/documentation/test_app_center_evidence_binding.py -v
```

Le validateur pur refuse structures/types inattendus, horodatages synthétiques périmés, discordances hôte/tenant/acteur/site, révisions différentes, scopes de planification manquants, mélanges de moteurs et ports réservés. Il produit uniquement `MATCHES_SYNTHETIC_CONTEXT_ONLY` ou `BLOCKED_SYNTHETIC`, avec `actor_authenticated=false`, `host_identity_verified=false`, `policy_signature_verified=false`, `authorization_approved=false`, `resource_reservations_created=false`, `execution_allowed=false`, `apply_available=false`. Un résultat cohérent **n'est jamais une autorisation**. Aucun réseau, probe OS, écriture, SQL, Docker, Podman, TLS ou action privilégiée.

Les cas de fausses provenances, preuves expirées, révisions rejouées, autres tenants, champs inconnus, commandes privilégiées et ports en conflit ne sont que des **tests unitaires hors ligne**. La [matrice d'intégration](../13-tests-quality/app-center-evidence-gates.md) reste **PLANNED / NON EXÉCUTÉS**.

## Handoffs et décisions techniques ouvertes

- **Security :** vraie authentification du pair/agent, anti-rejeu, signatures/racines de confiance, modèle horloge/TTL/nonce, isolation tenants et droits Linux.
- **API/IPC :** contrats typés versionnés `observeCapabilities`, `readEffectivePolicy`, `planInstall`, éventuel `applyInstall` séparément approuvé ; aucun shell libre ni instruction Hub directe à Go.
- **Database :** révisions approuvées, références des snapshots signées si retenues, idempotence durable, propriété, verrous et fencing ; **aucune table ou migration approuvée**.
- **QA/DevOps :** vrais essais PHP/site, SQL, pilotes Docker/Podman, cohérence ports, firewall et restauration sur OS/VM nommés. Import Foundation R1 et Symfony/PostgreSQL R2 nécessaires.
- **Hub :** uniquement métadonnées catalogue signées/versionnées facultatives, jamais preuves des ressources ni rôles des utilisateurs. Core autonome sans Hub.

TTL, signature, transport, seuils, rôles, OS/pilotes, prix, noms API publics et codes d'erreur restent **OUVERTS** après revue spécialisée. Q1–Q220 conservées ; Q221+ non répondues.
