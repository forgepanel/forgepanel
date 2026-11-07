<!-- forgepanel-doc id=FP-04-PROGRESSIVE revision=2 status=proposed -->
# ForgePanel — Modules facultatifs, visibilité et disponibilité indépendantes

[English](../../en/04-modules/progressive-release-policy.md) · [Catalogue actuel](README.md) · [Stratégie](../00-project-control/modular-development-strategy.md) · [Registre 40 éléments](../../evidence/forgepanel-modular-roadmap-proposed-v2.json)

**Version candidate de la politique progressive antérieure, sans intégration runtime.** Le registre préserve 15 capacités Core cibles V1 et 25 modules/extensions facultatifs. Leur `target_release` est indicatif. Aucun composant de ce registre n'est déclaré installé, exécutable ou vérifié par cette documentation.

## Classification obligatoire

| Classe | Exemple | Effet d'une absence |
|---|---|---|
| **Core obligatoire** | Identity/RBAC, PHP/TLS, SQL de contrôle, files/SFTP, backup/restore, opérations Linux typées | Bloque le jalon du **parcours promis** s'il n'existe pas ou n'est pas testé |
| **UI Core non critique** | Catalogue en lecture seule | Afficher une page dégradée, mais ne jamais bloquer sites, sessions ou réparation |
| **Module facultatif public** | ONE-CLICK INSTALL, Container Apps, serveur mail, WAF | Aucun effet sur le Core/les sites existants sans ce module |
| **Extension privée éditeur** | ForgePanel-Hub | Core, hébergement, sauvegarde et authentification fonctionnent hors ligne, sans Hub |

Ne pas traiter un firewall, une validation TLS, des droits d'accès, l'audit de sécurité ou une vraie restauration comme un simple plugin reportable s'ils protègent des fonctions annoncées.

## Cycle de vie et contrôles **distincts**

- **Documentation / développement** : `PLANNED`, `SPECIFIED`, `DEVELOPING`, `IN_REVIEW`, `TESTING`, `RELEASE_READY`, `RELEASED`, `DEPRECATED`. Un état `DEVELOPING` nécessite un commit/issue/PR lié vérifiable ; de simples plans ne suffisent pas.
- **Disponibilité sur l'hôte** : paquet réellement présent, signature valide, Core/API/OS compatibles, dépendances présentes, ressources et prérequis techniques démontrés. La présence d'une carte n'établit aucun de ces faits.
- **Activation** : droits serveur/tenant/site, contrat/politique de plan, consentement si applicable, test des migrations, backup/reprise, état health et audit. Activation exclusivement par une opération locale autorisée.
- **Visibilité** : `HIDDEN`, `ADMIN_PREVIEW`, `CUSTOMER_INFO`, `CUSTOMER_AVAILABLE`. La configuration d'affichage ne peut pas modifier les droits d'exécution.

**Effet UI** : `En développement` / `Planifié` ouvre uniquement une fiche descriptive (catégorie, fonction, dépendances, jalon indicatif, statut justifié, limitations, prochaine étape). Aucun bouton installer/activer, aucune URL vide, aucun lien d'exécution. Éviter les sous-menus non fonctionnels : préférer **Module Manager → À venir**, puis filtres par statut, catégorie, version. Afficher `Disponible` uniquement lorsque paquet, compatibilité, permission et route fonctionnelle sont vérifiés. L'interface est bilingue et accessible.

## Contrat de manifest de module — requis avant exécution, pas encore implémenté

Chaque module doit déclarer : `id`, `owner`, `type`, `status`, `business_value`, `target_release`, `core_version_range`, `api_contract_version`, `dependencies`, `conflicts`, `permissions`, `data_migrations`, `feature_flag`, `default_enabled`, `installable`, `public_visibility`, `distribution_channel`, `rollback_strategy`, `tests`, `documentation`, `support_level`, `license_entitlement` si nécessaire. Le contrat candidat consigne ces clés dans le registre JSON, **sans faire passer ces métadonnées pour un manifest d'installation certifié**.

Règles à faire appliquer **côté serveur** : IDs uniques, versions/contraintes strictes, graphe acyclique, dépendance interdite Core→optionnel, migrations isolées et interdites pendant le bootstrap obligatoire, capacité OS qualifiée, droits RBAC/tenants au point d'effet, policy revision et idempotence, quotas, provenance/signatures/anti-rollback, journaux sans secrets, relance et rétention. Une licence commerciale n'accorde jamais de droit Linux. Aucun `shell.exec` ou équivalent privilégié générique.

### Cas d'indisponibilité et défaillances

- Module **absent** : route non enregistrée ou fiche informative, aucun service/worker/job/SQL optionnel chargé.
- Module **désactivé** : plus de nouveaux effets, données conservées, jobs en cours traités selon un contrat de drain/rollback, pas de suppression implicite.
- Module **incompatible** : refus d'activation, raison affichée, Core continue, éventuel plan de migration explicite.
- Module **en panne** : confinement de l'erreur, erreur corrélée et auditée ; aucune panne en cascade vers la santé du Core.
- Hub privé **indisponible** : refus/état inconnu des **nouvelles** opérations premium selon politique, sans arrêt des fonctions Core gratuites ni destruction des données existantes.

## ONE-CLICK INSTALL / CONTAINER APPS

**ONE-CLICK INSTALL** = moteur classique gratuit, scripts/applications compatibles PHP/hébergement natif, **aucune dépendance Docker/Podman ni Hub premium** ; licences tierces séparées. **CONTAINER APPS** = moteur distinct de stacks avec pilotes **Docker** et **Podman indépendants**, images signées/pinnées, volumes, ports/réseau, CPU/RAM/PIDs/I/O, sauvegarde/restauration et isolation vérifiées ; ne pas utiliser les recettes natives pour appliquer des conteneurs. Une application ayant les deux formats possède **deux recettes indépendantes**. Recherche globale lecture seule autorisée, conversions silencieuses interdites. Conserver les arbitrages Q171/Q176/Q191–Q213 et le candidat Coraza détection-first Q174, sans autoriser automatiquement WAF ni malware scanner.

## Roadmap candidate (aucune date fixée)

| Release indicative | Exemples facultatifs | État réel |
|---|---|---|
| `1.0` | Catalogue informatif, pas de nouveaux moteurs facultatifs | Core R1–R4 **non encore certifié** |
| `1.1.x` | ONE-CLICK, Git Deploy, ABI d'extensions R5 | Spécifié, non exécutable |
| `1.2.x` | Docker, staging, SQL/cache avancés, Hub R6 après ABI | Spécifié, non exécutable |
| `1.3.x` | Podman, DNS local, mail, WAF, antivirus | Spécifié, non exécutable |
| `1.4.x+` | Webmail, revendeur, éditeur, Configuration Center, billing | Spécifié, non exécutable |
| `2.x` | Multi-serveurs/HA/VM clients | Selon preuves de capacité/risque, non exécutable |
| `3.x` | Gouvernance de l'écosystème et grande échelle | Objectif prospectif, pas de majeure imposée |

Chaque composant n'entre dans une release que via PR de livraison, contrat API/DB/sécurité approuvé, tests E2E et régression, version OS/ressource qualifiée et changelog. Le travail en cours peut continuer après une publication sans être exposé à l'utilisateur final.

## Gouvernance et preuves

Le registre documentaire [v2](../../evidence/forgepanel-modular-roadmap-proposed-v2.json) porte des indicateurs de **non-exécution** explicites. Il ne peut pas être lu par un agent privilégié comme source d'autorisations. Les [35 cas QA prévus](../13-tests-quality/modular-release-gates.md) devront être réellement exécutés avant de déclarer un module qualifié. R5 (neutral SDK) et R6 (Hub) demeurent postérieurs au MVP R4, sans présence obligatoire dans Core 1.0. **MFA reste facultative, protection et audit restent obligatoires.**