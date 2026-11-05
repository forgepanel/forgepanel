<!-- forgepanel-doc id=FP-02-CONTAINERS revision=1 status=specified -->
# Docker and Podman runtime drivers

[Français](../../fr/02-architecture/container-drivers.md) · [Architecture](README.md)

## Q51 C: two independent engines

ForgePanel targets **Docker and Podman**, each behind its own adapter conforming to a common Go interface. Neither distribution nor host must install both at the same time. Compatibility is checked against the detected OS, version and available capabilities.

Containers host **customer applications**, not the panel's Symfony runtime. Conventional PHP, Node.js and Python application runtimes also remain supported goals where permitted.

## Candidate API and settings

A `ContainerRuntimeDriver` contract should provide `Capabilities`, `PlanDeploy`, `Start`, `Stop`, `Inspect`, `Metrics`, `Backup` and `PlanRemove`. Every operation is typed, tenant-scoped, logged and subject to Core authorization.

Administrable settings: engine choice, approved images and versions, CPU/memory, quotas, ports and networking, volumes, logs, restart policies, secrets and backups. The [Configuration Engine](configuration-engine.md) plans changes with preflight, validation, recovery where possible and audit.

## Security and status

Container-management service access must be strictly controlled; privileged workloads and sensitive mounts are forbidden by default. Prefer rootless when compatible, preserve SELinux/AppArmor and test isolation boundaries. Tests must cover tenancy, quotas, network, backups and failure cases.

**Neither driver is implemented or certified.** Both are confirmed targets; default selection per distribution remains a technical question. Essential hosting drivers belong to the proposed free Core; managed cloud container services are optional commercial offerings.
