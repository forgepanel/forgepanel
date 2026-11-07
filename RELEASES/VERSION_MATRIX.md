# ForgePanel — Version matrix / Matrice des versions

**PROPOSED / PROPOSÉ — not merged, not deployed, no official tag.**

This matrix is an editorial summary of the paired detailed release plan. / Cette matrice résume la politique de release détaillée FR/EN.

| Release train / Train | Scope / Périmètre | Evidence / Preuves | Real status / État réel |
|---|---|---|---|
| Development R1 | Preserve source v0.7 + reviewed v0.7.1 optional-MFA delta | Git import + exact-head CI | BLOCKED — Git authorization |
| Pre-Alpha R2 | Symfony HTTP + PostgreSQL setup/identity + read-only planning | Real HTTP/SQL/tenant tests | NOT RUN |
| Internal Alpha R3 | Typed Go IPC, VM installer and OS qualification | Real QEMU/KVM installation and recovery | NOT RUN |
| Closed Alpha / MVP R4 | PHP website, HTTPS, SFTP, backup/restore, VPS | Real VM and tenant-negative E2E | NOT RUN |
| Preview / Private Beta | Tested site, truthful FORGE/PANEL UI, cohort/legal gates | UX, accessibility, privacy, security, restore | NOT RUN |
| Public Beta | Public authorized testing of supported matrix | Signed packages, legal/security/upgrade | NOT RUN |
| RC / Stable v1.0.0 | Frozen qualified Core, no optional dependencies | Exact SHA, docs, security, restore, approver | NOT RUN |
| 1.x features | Free ONE-CLICK, Docker/Podman independent, mail, DNS, WAF, more hosting | Qualified module-by-module | SPECIFIED ONLY |
| 2.x product goals | Multi-server, HA, optional orchestration | Measured scale, consistency and recovery | ROADMAP ONLY |
| 3.x product goals | Ecosystem governance and large-scale operations | Measured demand and real qualification | ROADMAP ONLY |

**Semantic Versioning:** 2.0/3.0 major labels only for actual incompatible public contracts; compatible enhancements remain minor versions. / Une version majeure ne se justifie que par une rupture de contrat public, pas par le numéro du jalon marketing.

**No artificial percentages and no premature dates. / Aucun pourcentage ni calendrier inventé.**

[French](../DOCUMENTATION/fr/14-devops-releases/release-lifecycle-plan.md) · [English](../DOCUMENTATION/en/14-devops-releases/release-lifecycle-plan.md) · [Module registry](../DOCUMENTATION/evidence/forgepanel-modular-roadmap-proposed-v2.json)