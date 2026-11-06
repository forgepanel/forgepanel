<!-- forgepanel-doc id=FP-14-APP-HOST-HINTS revision=1 status=specified -->
# App Center — observation Linux Go en lecture seule, sans capacité certifiée

[English](../../en/14-devops-releases/app-center-host-observation.md) · [DevOps](README.md) · [Sources](../../../tools/app-center-host-probe/README.md)

**État : SOURCE GO AUTONOME, INTÉGRATION CORE NON IMPLÉMENTÉE.** Cet outil Go 1.23 utilise uniquement la bibliothèque standard et peut lire des indices du système Linux **sans privilège**. Ce n'est ni l'import Foundation v0.7, ni un agent Go authentifié, ni une API Symfony, ni un installateur, ni un service qualifié ou une version de production.

## Informations relevées et limites

| Champ | Source et signification | Ce qui n'est PAS prouvé |
|---|---|---|
| `logical_cpu_count_hint` | Nombre logique de CPU vu par le processus Go | quotas cgroups, CPU disponibles à un tenant, réservation ou limitation effective |
| `memory_total_bytes_hint`, `memory_available_bytes_hint` | Parsing borné de `MemTotal`/`MemAvailable` dans `/proc/meminfo` | RAM autorisée au tenant, budget conteneur, capacité réservable ou protection OOM |
| `cgroup_v2_controllers` | Lecture des tokens dans `/sys/fs/cgroup/cgroup.controllers` | délégation au client, application des quotas ou compatibilité rootless |
| `docker_binary_candidate` / `podman_binary_candidate` | `lstat` de chemins exécutables fixes ; présence, lien symbolique ou erreur | fonctionnement réel de Docker/Podman, socket, fournisseur Compose, compatibilité des images |

Les lectures sont limitées ; aucune entrée ne permet de choisir un chemin ou une commande. L'outil ne lance ni Docker/Podman, ni shell, ni réseau, ni opération privilégiée ; il ne lit pas les sites clients et ne change pas les ports/pare-feu. Un résultat absent/invalide est `INCONCLUSIVE` ou `NOT_OBSERVED`, avec codes d'avertissement expurgés. Un système non Linux produit `NOT_APPLICABLE`.

Tout rapport contient `driver_qualification=NOT_EXECUTED`, `qualified_container_drivers=[]` et **false** pour l'identité vérifiée, l'autorisation de l'acteur, le budget exploitable, le confinement cgroups, les tests runtime, la signature, les privilèges Linux et la possibilité d'installer. Un lien symbolique vers Docker reste `SYMLINK_UNVERIFIED`.

## Sources et tests

[Module et mode d'emploi](../../../tools/app-center-host-probe/README.md) · [20 tests unitaires Go](../../../tools/app-center-host-probe/probe/probe_test.go) · [CI dédiée](../../../.github/workflows/app-center-host-probe.yml).

Les tests injectent des lecteurs de fichiers fictifs et couvrent mémoire corrompue/trop grande, overflow entier, cgroups, binaire/symlink, erreurs d'accès, installations absentes, refus de fuite de secrets, chemins bornés et absence d'autorisation. La CI contrôle également `go test -race`, `go vet`, `gofmt`, le refus d'arguments et les constantes d'interdiction sur un runner Linux **qui n'est pas un serveur ForgePanel client certifié**.

## Contrats à valider avant intégration

- Le [contrat IPC Go typé](../08-api-contracts/symfony-go-ipc-r3.md) devra définir un pair/serveur authentifié, la provenance, la fraîcheur, la signature et l'anti-rejeu, toujours ouverts.
- Le [contrat des quatre sources](../08-api-contracts/app-center-admission-evidence.md) liera l'observation **vérifiée** à des droits Symfony tenant/site indépendants, une politique Core à jour et une demande client non fiable. Le JSON CLI **ne constitue jamais une preuve de confiance**.
- Les CPU/RAM/PIDs/volumes et les ports réservés **FORGE 8447 / PANEL 8446** nécessitent des contrôles physiques et verrous séparément approuvés. `MemAvailable` ne doit **jamais** être converti directement en quota client disponible.
- Le **ONE-CLICK INSTALL** natif gratuit reste utilisable sans Docker/Podman/Hub ; **CONTAINER APPS** est distinct et soumis à qualification. Q1–Q220 restent en vigueur.

**Blocages :** import réel Foundation #2, Symfony/PostgreSQL #3, agent/IPC authentifié, DB versionnée et vrais tests Linux/VM/tenants. Les [12 tests futurs](../13-tests-quality/app-center-evidence-gates.md) restent **PLANNED**, jamais PASS. Cette sonde Go autonome ne lève aucun de ces prérequis.
