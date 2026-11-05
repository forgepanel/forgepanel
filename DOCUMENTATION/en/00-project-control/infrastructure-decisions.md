<!-- forgepanel-doc id=FP-00-INFRA revision=2 status=specified -->
# Q61–Q70 decisions — Infrastructure, administration and interface

[Français](../../fr/00-project-control/infrastructure-decisions.md) · [Previous decisions](commerce-identity-release-policy.md) · [ADR register](decisions.md)

## Source and state

The owner confirmed **all ten Q61–Q70 decisions on 5 November 2026**. These extend, without overriding, Q1–Q60 and the free Core's independence from Hub. This is a **specification**, not a certified installer, signed distribution, cluster, DNS/mail deployment, backup platform or advanced panel UI.

| ID | Choice | Scope and constraints |
|---|---|---|
| Q61 C | CI/CD builds signed with **protected keys**, **anti-rollback metadata** and approvals | Scoped publishing roles, immutable artifacts/metadata, trust roots, rotation/revocation; a signature alone cannot establish code safety. |
| Q62 C | **Universal installer + signed DEB/RPM repositories** | Simple bootstrap command, provenance verified before privileged action, preflight, idempotent setup, upgrade/recovery and diagnosis. Target Debian 12/13, Ubuntu 24.04/26.04 LTS and AlmaLinux 9/10 after VM tests. |
| Q63 C | **Local DNS plus external providers via adapters** | Per-zone authority/delegation, DNS ownership checks, capability-based drivers and propagation state; avoid split ownership. Local engine (e.g. PowerDNS) is not yet selected. |
| Q64 C | **Native mail plus external providers** | Mailboxes, domains, routing, SMTP/IMAP, DKIM/SPF/DMARC, TLS, quotas and provider state; plan antispam, DNS validation and deliverability. Local backend not locked. |
| Q65 D | **Multi-destination backup, encryption, restore tests, remote replication, immutability and advanced recovery** | Resource-specific policies, encrypted copies, deletion resistance, retention and tested DR procedures; RPO/RTO to be measured later. |
| Q66 C | **Sensitive-action reauthentication plus configurable additional approval** | Administrator MFA remains optional; recent-auth policies, separation of duties with multiple admins, effective permissions, audit and secured break-glass route. |
| Q67 D | **Multi-server agents, groups/policies, orchestration, HA, clustering and recovery** | Central control, desired/observed state, coordination, quorum/fencing where needed, partitions and restoration. Clustering is a **phased goal**, not a v1 prerequisite. |
| Q68 C | **Local monitoring, email/webhooks, external integrations, configurable alert rules** | Health, metrics, thresholds, recipients and acknowledgments by role; no implicit export of tenant secrets. Predictive analytics were not selected. |
| Q69 D | **Installation/per-site profiles plus multiple frontends by IP/port** | Nginx, Apache, Caddy, PHP-FPM, FrankenPHP by capability; exclusive listener ownership, TLS/routing, `.htaccess` security and validate/reload before activation. |
| Q70 D | **One brand per organization with visual editor, widgets and configurable navigation** | Symfony Twig/UX design system, themes/preview/history and permissions; allowlisted blocks/routes, no arbitrary executable code injection into Core. |

## Q71–Q80 refinements

Q71–Q80 refine, rather than replace, these choices: key custody/rotation, existing-service adoption, tested DNS recommendations, Postfix/Dovecot first, 3-2-1 backup, per-action approval/recovery, phased HA/orchestrators, Prometheus/OpenTelemetry and declarative widgets. **Q79 now explicitly requires a WebStack recommendation for each site at creation and the option to switch later, under a safe plan.** See [Q71–Q80 decisions](decisions-q71-q80.md) and [WebStack workflow](../02-architecture/site-webstack-advisor.md).

## Administration and phased delivery

The objective is **broad configurability without crossing trust boundaries**. Every setting has a type, effective value, inheritance scope, dependencies, permissions, audit, compatibility validation and impact level. High-impact operations obey Q47: **PLAN → VALIDATE → SNAPSHOT → APPLY → VERIFY → RECOVER when feasible**. Simple cosmetic changes may apply immediately with undo.

**Phase 1**: foundations, CLI, signed installer, VPS administration + shared hosting, web profiles, DNS/mail and backup capabilities needed for a testable product. **Phase 2**: broader external drivers, monitoring and advanced UI personalization. **Phase 3+**: orchestration/HA/DR and mature multi-server extensions once verified. Exact feature order within phases remains open; decisions do not imply simultaneous v1 delivery.

## Core and Hub ownership

**Core** owns OS, ports, DNS/mail services locally and through providers, WebStacks, RBAC, agents, local monitoring, backup/restore and actual update execution. Optional **private Hub** may manage signed artifact catalog, staged campaigns and notices for voluntarily registered installations. Hub never obtains unrestricted root shell access on customer hosts; Core stays operational offline. Hub connections, metrics and diagnostic sharing remain separately controlled under Q6.

DNS/mail modules and external drivers must be disableable without silently destroying existing data. Advertised support requires tests on relevant OS versions, WebStacks and drivers.

## Future test gates

- **Q61–Q62 release chain**: forged/revoked signatures, old package metadata, missing OS packages, mid-install interruption, repeat install, approval bypass.
- **Q63–Q64 DNS/mail**: wrong authoritative zone owner, partial propagation, bad record, open relay, certificate and tenant-domain separation.
- **Q65 backups**: real restores including keys, compromised deletes, remote outage, immutable copies and documented DR restart.
- **Q66 approvals**: bypass attempt, single-admin break-glass, stale reauthentication, local recovery.
- **Q67 HA**: network partition, competing agents, leader recovery, state divergence, quorum and VM tests.
- **Q68 monitoring**: notification storms, missing metrics, leaked secrets and outbound-consent checks.
- **Q69 web routing**: IP:port collision, TLS/session isolation, Apache `.htaccess` bypass prevention, config generation recovery.
- **Q70 design**: unauthorized edits, invalid widgets, XSS, contrast, accessibility, version history and one brand per organization.

## Still open

Actual DNS/mail/backup/monitoring providers, signature tooling and keys, default approval policy, concrete cluster topology, RPO/RTO, backup copy counts, auto-install timing, widget presets and editor constraints. **No vendor, value or certification is silently chosen.**
