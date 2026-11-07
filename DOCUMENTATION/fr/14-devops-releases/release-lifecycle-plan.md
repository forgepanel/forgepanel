<!-- forgepanel-doc id=FP-14-RELEASE-LIFECYCLE revision=2 status=proposed -->
# ForgePanel — Versions, canaux et critères de publication 1.0 → 3.x

[English](../../en/14-devops-releases/release-lifecycle-plan.md) · [Stratégie projet](../00-project-control/modular-development-strategy.md) · [DevOps](README.md) · [Registre des trains](../../evidence/forgepanel-release-trains-proposed-v2.json)

**Version candidate de l'ancien Release Lifecycle Proposal (non fusionné).** La présente adaptation remplace uniquement **les exemples** de tags de la proposition précédente : ni les archives historiques `Foundation v0.7/v0.7.1`, ni les commits déjà existants ne sont renommés. Un numéro indiqué ici ne signifie ni tag, ni build signée, ni release, ni production.

## 1. Convention version/SemVer

Préversions **du même train 1.0** (numéros numériques préfixés pour préserver l'ordre SemVer) :

| ID | Stade | Exemple de tag | Canal installable proposé | Audience | Sortie vérifiable |
|---|---|---|---|---|---|
| FP-REL-01 | Development | `v1.0.0-0.dev.1` | Dev | Interne | R1 commit source exact, provenance et tests |
| FP-REL-02 | Pre-Alpha | `v1.0.0-1.prealpha.1` | Dev | Interne | R2 Symfony/PG, identité, première tranche HTTP/SQL ; **pas d'installateur Linux opérationnel** |
| FP-REL-03 | Alpha interne | `v1.0.0-2.alpha.1` | Dev | Équipe | R3 IPC/agent/installeur en VM, erreurs et récupération |
| FP-REL-04 | Alpha fermée | `v1.0.0-2.alpha.2` | Dev | Testeurs privés | R4 premier site isolé PHP/HTTPS, SFTP, restore |
| FP-REL-05 | Technical Preview | `v1.0.0-3.preview.1` | Beta | Limitée | Périmètre honnête, UX FORGE/PANEL et accessibilité |
| FP-REL-06 | Beta privée | `v1.0.0-4.beta.1` | Beta | Sur invitation | R4 qualifié, sécurité/légal et reprises de cohortes |
| FP-REL-07 | Beta publique | `v1.0.0-4.beta.2` | Beta | Public informé | Licence, signatures, mises à jour et OS matrice qualifiés |
| FP-REL-08 | Release Candidate | `v1.0.0-5.rc.1` | Beta | Validation | Gel V1.0, régressions, sécurité, backups/upgrade réels |
| FP-REL-09 | Stable / GA | `v1.0.0` | Stable | Production autorisée | RC acceptée, artefacts immuables signés, support et docs |

Les `.1/.2` sont des exemples et non des numéros réservés. L'audience est définie par autorisation de distribution distincte du tag. Les fixes compatibles utilisent PATCH (`1.0.1`), les fonctionnalités compatibles MINOR (`1.1.0`), les ruptures publiques MAJOR avec migration. **Aucun `v2.0.0` ou `v3.0.0` ne doit être créé pour des raisons de marketing seulement** ; ces étiquettes sont des jalons de trajectoire. Un hotfix de sécurité n'attend pas neuf étapes. Aucun calendrier de support ou LTS n'est fixé.

## 2. Critères bloquants par jalon

R1 : empreinte SHA et inventaire, licences/secrets, import en `features/*` puis `develop`, tests Go/PHP et FR/EN sur **SHA importé**, sans installateur actif. R2 : Symfony HTTP, PostgreSQL transactions, création du compte initial, sessions/CSRF, MFA facultative, RBAC/tenant tests, migrations/concurrence/rollback. R3 : IPC typé avec identité de pair et droits, installateur signé, mesures en vraies VMs QEMU/KVM et récupération, premier OS/WebStack choisi selon preuves. R4 : domaine et DNS externe, validation A/AAAA publiés et une sonde indépendante, HTTP-01/HTTPS, site PHP/FPM, SFTP de site sans shell, VPS maintenance bornée, sauvegarde chiffrée et restauration isolée **réussie**, cohérence de PostgreSQL panneau. R5 : API neutre avec extension test non-Hub, Core valide sans elle. R6 : Hub privé sans droits Linux et sans dépendance Core.

Preview et Beta ne contournent ni sécurité, ni légalité, ni droits tiers. Beta privée : accord de distribution, canal confidentiel sécurité vérifié, prévention de pertes de données, cohortes, arrêt/reprise. Beta publique : provenance, versions supportées et tests upgrade. RC : gel et fermeture des P0/P1, audits indépendants requis, publication des limitations. GA : approbation de publication, test exact de l'artefact signé, notes FR/EN, sécurité et support. Une release ne revendique **que les modules réellement qualifiés et distribués**. Un module facultatif non prêt est désactivé/absent et son jalon glisse à une mineure ultérieure.

## 3. Git et canaux : règle ForgePanel prioritaire

`features/* → develop → stable → main → production` reste le **workflow propriétaire et les branches permanentes existantes**. La proposition transversale préfère parfois `production` comme environnement seul ; ForgePanel **conserve sa branche** jusqu'à décision explicite contraire. `main` reçoit le tag `vX.Y.Z` après contrôles, et `production` représente un état de promotion/déploiement autorisé, **jamais une preuve que le serveur tourne**. Artefact construit une seule fois depuis un commit fixé, digest signé, mêmes octets promus. Des PR révisées/testées et des checks exact-head sont obligatoires ; pas de push forcé/auto-approbation. `hotfix/*` et backports adaptés aux séries officiellement maintenues.

## 4. Manifest de release et preuve

Version+tag+SHA, référence DOC/DESIGN, exigences/versions API, SBOM/licences/droits tiers, OS/WebStack réellement qualifiés, toolchain/build reproductible, hash/signature, migrations et sauvegarde, scénarios PASS/FAIL/BLOCKED/NOT RUN, tests restauration et sécurité, audit indépendant si requis, compatibilité extensions/langues/thèmes, conditions de rollback **ou de récupération**, risques connus, canal/audience, notes FR/EN, autorisation, statut `PUBLISHED` séparé de `DEPLOYED`. Pas de métrique de progrès inventée. Aucun test `SKIP` ne vaut qualification.

Le [registre de release](../../evidence/forgepanel-release-trains-proposed-v2.json) est explicitement non publié. Le [plan modulaire](../04-modules/progressive-release-policy.md) permet de reporter les modules optionnels, jamais les contrôles critiques. L'API neutre R5 et le Hub R6 n'entravent pas la première Stable Core R4. Diffusion publique à vérifier juridiquement pour AGPL/commercial/CLA, canaux privés de sécurité, provenance et droits de tiers.