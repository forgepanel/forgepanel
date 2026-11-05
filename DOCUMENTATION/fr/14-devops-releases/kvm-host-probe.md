<!-- forgepanel-doc id=FP-14-KVM-HOST-PROBE revision=1 status=specified -->
# Inspection locale QEMU/KVM — outil préparatoire R3

[English](../../en/14-devops-releases/kvm-host-probe.md) · [Installation et releases](README.md) · [Roadmap](../00-project-control/implementation-roadmap.md) · [Tests](../13-tests-quality/README.md)

## Objet et séparation des étapes

ForgePanel Core dispose d'un **outil Go indépendant de lecture seule**, dans `tools/kvm-host-probe/`, préparant l'orientation **Q151 A, Q161 C** : qualifier les premiers environnements de test en QEMU/KVM local, avec runners éphémères, isolation, images figées, quotas et nettoyage. **Cet outil ne lance aucune VM et ne constitue pas un runner.** Il ne fait pas partie de la Foundation historique v0.7, dont l'import demeure bloqué par l'absence du ZIP original (R1, issue #2). Il ne modifie aucune décision Q1–Q170 et n'active pas Hub.

## Utilisation sans privilèges

```bash
cd tools/kvm-host-probe
GOTOOLCHAIN=local GOPROXY=off go test ./...
GOTOOLCHAIN=local GOPROXY=off go test -race ./...
GOTOOLCHAIN=local GOPROXY=off go vet ./...
GOTOOLCHAIN=local GOPROXY=off go run ./cmd/forgepanel-kvm-probe
```

Le programme inspecte uniquement des informations **fixes** et locales : `/etc/os-release` (ID/version), `/dev/kvm` par `lstat` (type caractère, symlink refusé), `/proc/cpuinfo` (drapeaux exacts VMX/SVM pour x86), `/sys/module/kvm` (présence de répertoire). Les lectures de fichiers sont bornées, sans commande shell, `ioctl`, ouverture de `/dev/kvm`, installation de paquet, écriture, accès réseau, secret, IP ou hostname. Le JSON affiche les états inconnus au lieu de fabriquer un PASS.

## Contrat de sortie JSON v1

Les champs `schema_version`, `runtime_os`, `runtime_arch`, `os_id`, `os_version`, `kvm_device`, `cpu_virtualization`, `kvm_kernel_module`, `host_assessment`, `qualification`, `warnings` et les indicateurs booléens décrivent **des observations**, pas une certification. `host_assessment=CANDIDATE_FOR_ISOLATED_VM_TESTS` signifie seulement qu'un périphérique caractère KVM et des flags CPU compatibles ont été observés sur x86. Sur ARM ou lorsqu'un renseignement manque : `INCONCLUSIVE` ; si le périphérique manque ou est un faux fichier : `NO_TRUSTED_KVM_DEVICE` ; hors Linux : `NOT_APPLICABLE`.

**Valeurs imposées par le code :** `qualification=NOT_EXECUTED`, `vm_executed=false`, `vm_image_pinned=false`, `snapshot_tested=false`, `resource_quotas_verified=false`, `failure_recovery_tested=false` et `report_signed=false`. La permission effective d'ouvrir le device n'est pas testée. Le rapport ne porte **aucune signature** Q152/Q162 et n'alimente pas automatiquement le stockage de preuves privées immuables.

## Contrôles présents et non réalisés

**Présent :** 14 tests Go synthétiques, `go test -race`, `go vet`, tests de flags/symlinks/faux périphérique, échecs de lecture et absence de fausse certification ; CI sur PR. **Non réalisé :** démarrage QEMU/KVM, preuve d'isolation, images épinglées, plafonds CPU/RAM/I/O, nettoyage de VM, snapshots, injection de pannes, signatures de rapports, stockage immuable, charge/benchmarks, validations de backup et restauration. Tous ces éléments relèvent de **R3/R4 futurs** et des gates Q132/Q152/Q161–Q166.

Cet outil ne sélectionne **aucun OS privilégié** Q121, ne confirme aucune distribution supportée, n'autorise pas de contournement des veto Q132 et n'exécute jamais d'action privilégiée sur le système. Aucun Hub ou service central n'est requis. [Références Q161–Q170](../00-project-control/decisions-q161-q170.md).
