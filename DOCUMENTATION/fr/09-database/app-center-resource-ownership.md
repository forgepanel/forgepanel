<!-- forgepanel-doc id=FP-09-APP-OWNERSHIP revision=1 status=specified -->
# App Center — modèle conceptuel de propriété et de réservation des ressources

[English](../../en/09-database/app-center-resource-ownership.md) · [Database](README.md) · [Contrats de recettes](../08-api-contracts/app-center-recipe-contracts.md)

**DRAFT / PROPOSÉ UNIQUEMENT.** Cette étude est un modèle de données conceptuel, **pas une migration DDL PostgreSQL, une table approuvée, une implémentation ni un nouvel arbitrage produit**. Le modèle physique, les contraintes, les migrations, la rétention et les mécanismes de récupération nécessitent les revues Database/Security/API. Q1–Q170 restent autoritaires ; Q171+ restent ouverts.

## Identités propres à chaque variante d'installation

| Concept candidat | Fonction | Frontière obligatoire |
|---|---|---|
| `AppDefinition` | Nom commun, famille applicative, éditeur et traductions | Ce n'est **pas** une installation exécutable |
| `AppRecipeVariant` | Version immuable, `recipe_kind`, digest/licence/compatibilité, revue éditeur | `native_script` et `container_stack` **ne peuvent pas partager** une clé de variante ou de recette d'exécution |
| `AppInstallation` | Hôte, tenant, compte/site, version de recette et états désiré/observé | Un seul moteur ; pas de conversion silencieuse par UPDATE |
| `AppNativeResources` | Site possédé, fichiers document-root, droits SQL limités, quotas PHP/site | Pas de dépendance implicite à l'image OCI ou au réseau conteneur |
| `AppContainerResources` | Pilote vérifié, images, volumes, réseaux, ports et limites cgroups | Pas de prise de contrôle des fichiers/DB des sites natifs ni des ports FORGE/PANEL |
| `AppOperation` | Demande durable, identité/tenant, transition, révision, idempotence/corrélation | Espace et autorisation distincts pour les deux moteurs |
| `AppBackupReference` | Cible, ressource/tenant/engine, portée restauration, rétention | Contrôle cohérent fichiers+SQL natifs distinct de volumes/stack+SQL conteneurs |
| `AppResourceReservation` | Verrous et réservations de capacités proposées : disque, base, ports, ressources | Aucune double allocation ; acquittement ≠ effet Linux appliqué |

Ces noms représentent des **entités logiques candidates**, pas des noms de tables physiques décidés. Le PostgreSQL interne du Core n'est pas le SQL des sites clients. Le Hub privé peut publier des métadonnées révisées, mais ne possède ni installations locales, ni fichiers, ni mots de passe SQL, ni volumes persistants des clients.

## Contraintes à revoir avant DDL

- Une installation référence **exactement un** `recipe_kind` et une version/digest immuable. Passer de natif à conteneur nécessite un **nouveau processus de migration qualifié** et une nouvelle identité d'installation.
- Un plan `native_script` ne réserve que les ressources de son site/tenant autorisé. Un plan `container_stack` suit son propre quota, moteur Docker/Podman, réseau et permissions.
- L'unicité d'idempotence candidate inclut tenant, moteur, ressource cible, opération et clé client. Une relance ne peut pas modifier silencieusement auteur, portée, digest ou destination.
- La propriété d'un port ou d'une ressource Linux doit être vérifiée dans l'**état observé**, pas seulement en PostgreSQL. Protéger 8447 FORGE et 8446 PANEL contre les collisions de ports hôte des conteneurs.
- La suppression d'une recette/installation **n'efface pas** automatiquement fichiers, bases, volumes, sauvegardes ; demander le choix de conservation et assurer une restauration testée.
- Capacité absente, artefact non signé, éditeur non vérifié ou quotas insuffisants => refus sans élévation commerciale/système.
- Les états d'échec partiel et les migrations irréversibles sont explicités ; une transaction SQL ne restaure pas automatiquement le filesystem ou les conteneurs.
- Une panne du Hub n'interrompt pas le catalogue natif gratuit du Core local.

## États et journalisation

`DRAFT → PREFLIGHT → APPROVAL_REQUIRED? → STAGED → APPLYING → VERIFYING → SUCCEEDED / FAILED / RECOVERY_REQUIRED` est un **workflow candidat**, pas un enum validé. Journaliser transitions, identité d'autorisation, traces expurgées, corrélation et preuve de récupération. Toute restauration respecte strictement tenant et moteur, sans conversion automatique.

## Statut et tests

Les [exemples et le validateur candidat](../08-api-contracts/app-center-recipe-contracts.md) n'effectuent que des **contrôles hors ligne** ; les [32 tests fonctionnels et VM](../13-tests-quality/app-center-engine-gates.md) restent PLANNED. Aucune DDL, migration, index, stratégie de verrou, garantie transactionnelle ni durée de conservation n'est approuvée ici.
