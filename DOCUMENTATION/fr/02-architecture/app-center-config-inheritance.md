<!-- forgepanel-doc id=FP-02-APP-CONFIG revision=2 status=specified -->
# App Center — Q180/Q220, héritage Configuration Center et règles immuables

[English](../../en/02-architecture/app-center-config-inheritance.md) · [Moteur de configuration](configuration-engine.md) · [QA](../13-tests-quality/app-center-configuration-gates.md) · [Q171–Q220 approuvées](../00-project-control/decisions-q171-q220.md)

**Statut : SPÉCIFICATION CANDIDATE / NON INTÉGRÉE / TESTS RUNTIME PLANNED.** Q180 D et Q220 D approuvent un centre de configuration administrable, versionné, avec héritage, simulation, RBAC, historique et récupération. Les valeurs par défaut, seuils, rôles autorisés, schéma et langage des règles restent des **choix techniques ouverts**. Ce document ne constitue **ni une implémentation ni une permission de modifier les paramètres réels**.

## Une autorité par règle et héritage restrictif

| Ordre | Niveau | Propriétaire prévu | Limite |
|---|---|---|---|
| 0 | Invariants immuables du produit | Contrats Core audités | Aucun niveau ne peut les désactiver |
| 1 | Politique globale | Administrateur FORGE autorisé | Contraint par les invariants et capacités hôte |
| 2 | Serveur | Administrateur du serveur concerné | Ne peut élargir la politique globale ni les limites physiques |
| 3 | Organisation | Autorité de l'organisation | Ne peut contourner RBAC/sécurité ni l'autorité serveur |
| 4 | Plan d'hébergement | Administrateur habilité | Quotas et moteurs bornés selon délégation parent |
| 5 | Site/application | Responsable autorisé de son site | Peut restreindre/désactiver certaines options, jamais contourner les limites |

Le Configuration Engine général prévoyait aussi les niveaux *compte* et les préférences **d'affichage par utilisateur**. La hiérarchie abrégée de Q180 **ne les annule pas** : leur ajout au moteur complet exige des contrats spécialisés. Un utilisateur ne pourra pas réactiver un conteneur interdit au niveau serveur/plan ni augmenter un quota physique. Ce prototype ne simule volontairement **que les cinq niveaux de Q180**.

**Attention :** les accès système FORGE `/forge:8447`, PANEL `/panel:8446` et l'IP machine/FQDN existant détectés et vérifiés **ne constituent pas des domaines système personnalisables**. Les **domaines des sites clients** et la **marque unique par organisation Q5/Q55** restent des fonctions distinctes, soumises aux contrats DNS/TLS et aux droits. Les anciens textes « hôtes des portails système personnalisables » nécessitent un delta documentaire ciblé, pas la création automatique d'un sous-domaine.

## Familles administrables et garde-fous non contournables

Le [résolveur de politique hors ligne](../../../scripts/preview_app_center_inheritance.py) reconnaît une **petite liste illustrative**, pas l'ensemble des paramètres du produit :

- `app.native.allowed`, `app.container.allowed`, `app.catalog.verified_partner_allowed` : booléens restrictifs (un niveau inférieur peut désactiver, jamais réactiver ce que le parent a désactivé).
- `app.container.max_cpu_millicores`, `app.container.max_memory_mib`, `app.container.max_pids` : plafonds décroissants (un descendant ne peut qu'abaisser). Capacités et pilotes réels devront être mesurés et revérifiés par un canal fiable.
- Invariants immuables de démonstration : `app.native.premium_required=false`, `app.native.container_runtime_required=false`, `app.core.hub_required=false`, `app.security.generic_shell_allowed=false`, `app.security.tenant_isolation_required=true`, `app.security.signed_artifacts_required=true`, `app.container.privileged_by_default=false` et ports du panneau **8446/8447** réservés.

Ces invariants expliquent les politiques et ne remplacent ni cgroups Linux, ni signatures, ni autorisation côté serveur. Les plafonds physiques, interdictions des sockets/montages privilégiés et règles de consentement s'appliquent même si un administrateur tente un override. Le moteur ne doit pas exécuter d'expressions, de scripts ou de hooks arbitraires entrés par l'utilisateur.

## Aperçu candidat en lecture seule — exemple synthétique

La [fiche de politique fictive](../../../evidence/app-center-fixtures/config-inheritance.synthetic.json) illustre des restrictions global→site avec des nombres de QA arbitraires **non adoptés comme valeurs par défaut**. Un plafond CPU global est réduit par le serveur, l'organisation, le plan et le site, tandis que le plan désactive l'accès conteneurs. Une tentative du site de réactiver l'accès ou de dépasser son plafond est refusée.

```sh
python3 scripts/preview_app_center_inheritance.py --fixture app-center
python3 tests/documentation/test_app_center_inheritance.py -v
```

La sortie décrit pour chaque clé la **provenance** (niveau et valeur illustrative), la valeur finale fictive et les invariants. Les indicateurs restent systématiquement `policy_status=SYNTHETIC_CANDIDATE_ONLY`, `authorization_verified=false`, `policy_signature_verified=false`, `physical_capacity_verified=false`, `audit_written=false`, `resource_reservations_created=false`, `execution_allowed=false` et `apply_available=false`.

L'outil Python ne lit qu'une fiche embarquée ; aucun réseau, SQL, secret de production, job, modification Linux ou site PHP n'est utilisé. Un résultat conforme **n'autorise jamais** un changement de paramètre réel. Les drapeaux « allowed » fictifs ne prouvent ni la compatibilité Docker/Podman ni un droit utilisateur.

## Interface Configuration Center proposée

**FORGE** doit afficher la source d'héritage, la valeur effective, l'éditeur autorisé, l'impact, les capacités du serveur, les sites concernés, le diff, les changements refusés, l'historique et la récupération. **PANEL** ne pourra modifier que les options du site/compte explicitement déléguées, sans voir les paramètres hôte/globaux. Les composants graphiques peuvent être réutilisés, pas les droits serveur.

Les futures familles comprennent : versions et qualification des scripts natifs, catalogue local/cache/signatures, Docker vs Podman par hôte, CPU/RAM/PIDs/volumes, exposition réseau, WAF détection/blocage, antivirus/quarantaine, mises à jour progressives, rétention, secrets/émetteurs, notifications et placements sponsorisés facultatifs. **Aucun prix, fournisseur, seuil, durée de rétention ni activation par défaut n'est fixé ici.** La gratuité du moteur natif ne rend pas toutes les applications tierces gratuites.

Les changements affectant Linux/données suivent Q47 **DRAFT → PLAN/DIFF → PREFLIGHT → SNAPSHOT → APPLY → VERIFY → COMMIT/RECOVER**, avec contrôle acteur/scope, audit et version. Une simulation UI ne doit jamais lancer APPLY. Les effets privilégiés passent par des opérations Go typées limitées, sans `shell.exec`. Concurrence, révisions périmées, verrous et jobs durables nécessitent des contrats API/IPC et DB validés séparément.

## Preuves requises à la future frontière APPLY

Le [contrat candidat de liaison des preuves](../08-api-contracts/app-center-admission-evidence.md) distingue **quatre sources** : observation Linux authentifiée par agent, droits acteur/tenant/site Symfony, révision de politique effective Core et demande client non fiable. Le [contrôleur hors ligne](../../../scripts/check_app_center_candidate_evidence.py) compare des **horodatages et révisions fictifs**, sans établir la provenance ni autoriser une action. Ni les métadonnées Hub ni l'aperçu UI ne peuvent remplacer ces preuves ; les [12 tests réels hôte/RBAC/politique](../13-tests-quality/app-center-evidence-gates.md) restent PLANNED.

## Revue et preuves

Les [tests hors ligne](../../../tests/documentation/test_app_center_inheritance.py) contrôlent héritage restrictif, invariants, mauvais types, scopes forgés et refus d'application. La [matrice runtime distincte](../13-tests-quality/app-center-configuration-gates.md) reste **PLANNED / NON EXÉCUTÉE**. Avant tout développement réel : Security pour garde-fous et isolation, API/IPC pour read/plan/apply/recover, Database pour migrations, QA pour vrais essais Symfony/Go/Linux et récupération, après prérequis R1–R4.

**Le Core reste seul propriétaire des politiques runtime tenant. Le Hub privé ne gère que ses propres règles d'édition/catalogue/offres/consentements ; il ne peut imposer une politique qui dépasse les limites Core, facturer le moteur natif gratuit ni obtenir de privilège Linux.**
