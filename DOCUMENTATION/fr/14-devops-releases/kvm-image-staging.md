<!-- forgepanel-doc id=FP-14-KVM-IMAGE-STAGING revision=1 status=specified -->
# R3 — Copie privée vérifiée des images de laboratoire

[English](../../en/14-devops-releases/kvm-image-staging.md) · [Admission QCOW2](kvm-image-admission.md) · [Sonde hôte KVM](kvm-host-probe.md) · [Roadmap](../00-project-control/implementation-roadmap.md)

## Périmètre et progression

Le module autonome `tools/kvm-host-probe/staging/` et le CLI `forgepanel-kvm-image-stage` préparent **une copie privée** d'une image QCOW2 préalablement admise par SHA-256 (Q151 A, Q161 C). Ils ne lancent pas de VM et ne deviennent pas un runner d'isolation, un installateur ou un plugin. L'import Foundation v0.7 reste bloqué (issue #2), le développement reste séparé du Core historique et de ForgePanel-Hub.

Le résultat positif `STAGED_FOR_MANUAL_REVIEW` indique **uniquement** que les octets copiés et relus correspondaient à l'empreinte attendue au moment des contrôles. Il conserve impérativement `qualification=NOT_EXECUTED`, `manual_review_required=true`, `execution_authorized=false`, `immutable_storage_verified=false`, `resource_quotas_enforced=false`, `vm_executed=false` et `report_signed=false`.

## Mode de fonctionnement

1. Le CLI exige **trois chemins absolus** : politique JSON privée, demande JSON privée et dossier parent privé destiné aux copies. La politique et la demande suivent les [schémas R3 existants](../../../tools/kvm-host-probe/schemas/policy.v1.schema.json) et [demande](../../../tools/kvm-host-probe/schemas/request.v1.schema.json). Aucun paramètre de CPU/RAM/durée n'est inventé.
2. L'admission existante contrôle la forme de la demande, les plafonds explicitement fournis, le SHA-256 de l'image et les refus réseau/partages/privilèges. Le staging exige un utilisateur **non-root**, Linux amd64 et des répertoires source/destination possédés et privés (0700), canoniques, séparés et non imbriqués.
3. La copie utilise des descripteurs de dossier Linux `openat`/`O_NOFOLLOW`, crée exclusivement `<parent>/<run_id>` **neuf** en 0700 et `image.qcow2` en lecture seule 0400 après écriture/synchronisation. Les fichiers source doivent être réguliers, privés, non exécutables, sans symlink ni hardlink supplémentaire. Aucun répertoire ou fichier existant n'est écrasé.
4. Les octets sont **recopiés et re-hashés** contre la demande. L'état de la source (inode, taille, modification) est revérifié et la copie est **relue et re-hashée** depuis le disque. En cas d'échec, pas de verdict positif.
5. Le reçu `stage-receipt.json` (0400) enregistre les SHA-256 de l'image, de la politique et de la demande, l'identité d'essai, la révision de politique, CPU/RAM/durée demandés, la taille de l'image et tous les indicateurs de non-exécution. [Schéma du reçu](../../../tools/kvm-host-probe/schemas/stage-result.v1.schema.json). Il n'est **pas signé**, et ne garantit pas l'immutabilité durable.

## Exécution locale par un compte non privilégié

```bash
cd tools/kvm-host-probe
GOTOOLCHAIN=local GOPROXY=off GOSUMDB=off go run ./cmd/forgepanel-kvm-image-stage \
  /chemin/prive/policy.json /chemin/prive/request.json /chemin/prive/staging-root
```

Le dossier `staging-root` doit être **créé à l'avance en 0700** par l'opérateur du laboratoire ; les JSON en 0600 et l'image source sous son propre dossier privé. Le CLI refuse root, un dossier partagé ou symbolique, un chemin relatif, des paramètres dangereux, une image différente, des limites invalides, un dossier `run_id` déjà existant et tout partage accidentel avec le dossier source.

## Gestion des échecs et statut

Un échec **avant création** produit `BLOCKED` et ne crée aucune copie. Un échec **après création** retourne `PARTIAL_STAGE_REQUIRES_MANUAL_CLEANUP` : le dossier privé partiel est conservé pour analyse et **n'est pas automatiquement supprimé** afin d'éviter un nettoyage destructeur si le chemin a été remplacé. Ne pas utiliser un reçu isolé comme autorisation ; examiner l'état du run et revérifier les fichiers juste avant tout futur lancement. La présence du mode 0400 **n'est pas** une garantie d'immutabilité : le même UID peut ultérieurement modifier les permissions/fichiers.

## Tests, limites et dépendances

La nouvelle suite ajoute **21 fonctions de test synthétiques** (copie conforme, refus d'écrasement/chemins partagés/symlinks, changements de source, échecs partiels, CLI privé, schéma et fausses promesses), portant le module à **62 fonctions Go**. Commandes de QA : `go test ./...`, `go test -race ./...`, `go vet ./...`, `gofmt -l .` ; le workflow GitHub fournit la preuve sur SHA exact.

**Non implémenté** : pilote QEMU/KVM, exécution de VM, validation structurelle complète QCOW2, vérification de signature de l'éditeur, authentification d'opérateur, sandbox/cgroups réels, quotas imposés, snapshots, pannes/reprise, nettoyage des VMs, rapports signés Q152, stockage immuable Q162, certification OS et sauvegardes/restaurations Q166. Ces jalons restent dans [l'issue #42](https://github.com/yyogas/forgepanel/issues/42), sous veto Q132. Aucune licence de code, décision Q171+, ou paramètre ouvert n'est approuvé implicitement.
