<!-- forgepanel-doc id=FP-14-KVM-IMAGE-ADMISSION revision=2 status=specified -->
# R3 — Admission des images QEMU/KVM avant toute exécution

[English](../../en/14-devops-releases/kvm-image-admission.md) · [Sonde KVM](kvm-host-probe.md) · [Roadmap](../00-project-control/implementation-roadmap.md) · [Tests](../13-tests-quality/README.md)

## Objet et statut

Le composant autonome `tools/kvm-host-probe/admission/` et la commande `cmd/forgepanel-kvm-image-admit` contrôlent **en lecture seule** l'identité d'une image QCOW2 locale et les paramètres d'un futur essai. Il s'agit d'un **filtre préparatoire de sécurité**, cohérent avec Q151 A, Q152 C, Q161 C, Q162 B et les veto Q132. **Aucune VM n'est démarrée, aucun quota réellement appliqué, aucune signature ou certification produite**. Le pilote QEMU/KVM éphémère reste à développer et qualifier sur un hôte autorisé. Cela ne remplace pas l'import Foundation v0.7 toujours bloqué en R1 (issue #2), ni ne dépend du Hub.

## Contrats JSON versionnés

- [Politique](../../../tools/kvm-host-probe/schemas/policy.v1.schema.json) : ID/révision, répertoire privé d'images, plafonds **explicites** vCPU, mémoire, durée et taille d'image. **Aucun nombre par défaut ni quota commercial inventé** ; une politique locale non signée n'est pas une autorisation d'exécution.
- [Demande](../../../tools/kvm-host-probe/schemas/request.v1.schema.json) : ID d'essai, seul nom de fichier `.qcow2`, SHA-256 complet en minuscules, vCPU/RAM/durée demandés. Les paramètres `network_enabled`, `host_shares_enabled`, `privileged` sont obligatoirement `false`.
- [Résultat](../../../tools/kvm-host-probe/schemas/result.v1.schema.json) : `BLOCKED` (code 2) ou `REVIEW_REQUIRED` (code 0), **toujours `qualification=NOT_EXECUTED`** et indicateurs faux pour VM exécutée, isolation, quotas imposés, validité QCOW2 complète, signature et critères Q132.

## Utilisation préparatoire non privilégiée

```bash
cd tools/kvm-host-probe
# Deux fichiers JSON privés (0600) conformes aux schémas.
# Image sous répertoire canonique privé (0700), propriété du même compte non-root.
GOTOOLCHAIN=local GOPROXY=off go run ./cmd/forgepanel-kvm-image-admit \
  /chemin/absolu/prive/policy.json /chemin/absolu/prive/request.json
```

Le programme refuse root, documents non privés ou symboliques, champs JSON inconnus, multiples objets/tailles excessives, absence de valeurs explicites, dépassements, requêtes réseau/partage/privilèges et chemins d'image dangereux. Le répertoire doit être absolu et canonique ; le fichier doit être régulier, privé, non exécutable, sans lien symbolique ni lien physique supplémentaire. `openat` avec `O_NOFOLLOW`, contrôle de l'en-tête QCOW2 version 2/3 puis SHA-256 **des octets entiers** ; le rapport n'expose pas le chemin local privé.

## Frontières et risques non résolus

L'en-tête QCOW2 **ne constitue pas une validation intégrale du format**. L'empreinte identifie les octets par rapport au manifest, **pas le fournisseur, la licence ni l'innocuité** de l'image. Les plafonds ne sont que **comparés**, jamais imposés au CPU/RAM/I/O. Un acteur contrôlant le même UID peut modifier l'image après le scan : le futur exécuteur doit conserver un objet immuable validé ou revérifier les octets au moment du lancement. Sans isolation jetable, réseau désactivé, quotas réellement imposés, snapshots, nettoyage, contrôle d'échec, rapports signés Q152 et stockage immuable Q162, **R3 reste non qualifié**. Les tests utilisent des fichiers QCOW2 synthétiques non bootables et ne sélectionnent aucun premier OS.

Aucune API shell générique, aucun privilège Linux, aucune interaction avec le Hub ; les défaillances critiques Q132 restent bloquantes. [Décisions Q161–Q170](../00-project-control/decisions-q161-q170.md).

## Étape suivante : staging privé vérifié

Le composant distinct [Image Staging](kvm-image-staging.md) réouvre les octets après l'admission, recopie et vérifie leur empreinte dans un dossier neuf non-root. Un reçu `STAGED_FOR_MANUAL_REVIEW` peut être produit, **jamais** une autorisation de démarrage QEMU ni une garantie d'immutabilité. Les quotas effectifs, snapshots, pilotes OS et signature restent à implémenter.
