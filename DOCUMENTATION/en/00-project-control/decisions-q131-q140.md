<!-- forgepanel-doc id=FP-00-Q131-140 revision=1 status=specified -->
# Q131–Q140 decisions — VM qualification, MVP, private beta and security

[Français](../../fr/00-project-control/decisions-q131-q140.md) · [Q121–Q130 decisions](decisions-q121-q130.md) · [MVP qualification](mvp-qualification.md) · [Technical roadmap](implementation-roadmap.md)

## Confirmed owner choices — 5 November 2026

**Q131 D, Q132 D, Q133 C, Q134 C, Q135 B, Q136 C, Q137 D, Q138 D, Q139 C, Q140 C** extend **Q1–Q130**. Status **SPECIFIED**: not an actual OS qualification, running installer/site, or launched private beta.

| Ref | Choice | Operating rules and boundaries |
|---|---|---|
| Q131 D | **Local VMs + automated CI, snapshots, fault injection and OS-specific qualification reports** | Record OS/version/architecture, image, WebStack, commit/build, tools, steps, redacted logs, PASS/FAIL/SKIP, security and recovery. `SKIP` is not a pass; container tests are not system VM qualification. |
| Q132 D | **WebStack tests for compatibility, security, load, maintenance/recovery with hard rejection criteria** | Test PHP/app/`.htaccess`, listeners/TLS, isolation and outage recovery. Reject tenant leakage, bypassed access rules, port collision and unrecoverable failure regardless of favorable load numbers. **No initial stack preselected** (Q122). |
| Q133 C | **External DNS A/AAAA, port-80, HTTP-01 routing and HTTPS diagnosis** | Explain conflicting A/AAAA/IPv6, site/vhost ownership, publicly reachable HTTP challenge, valid cert and HTTPS on 443, without logging ACME tokens. Native DNS not an MVP dependency. |
| Q134 C | **Planned OS updates with impact diff, backup, health check and recovery** | Package/version inventory, trusted origin, RBAC, preflight, recoverable snapshot/state, confirmation, idempotent job, reboot impact and health of panel/site. No generic root shell. |
| Q135 B | **Encrypted local MVP backup with optional remote destination** | Q126 coverage: panel config and PHP-site files, integrity manifest and **real restore test**, plus consistent panel PostgreSQL state as needed for recovery. Remote is optional by certified driver; local encryption alone does not protect against whole-disk loss. Q65/Q75 immutable 3-2-1 remain phased goals. |
| Q136 C | **Website-manager role: PHP/domains/TLS/files, SFTP and backups/restores within quotas/policies** | Per-site/org rights, Q47 revalidation of sensitive operations, no root/neighboring site access; restores do not grant another account's data or quota. System admin retains OS/package privilege. |
| Q137 D | **Private beta with invitations/terms, bug/update channel, staged waves, pause and recovery** | After Q127 internal VM proof, identify authorized testers/versions and allow removal from future beta distribution with recovery process. **Revoking beta access does not automatically revoke already granted software rights or destroy users' data.** |
| Q138 D | **Premium transfers: identity/org + cryptographic proof, rate limits, configurable second approval for high-risk recovery** | Prove target server possession, prevent replay/double seat assignment, maintain audit and contractually safe release of old assignment; lost-host manual recovery needs risk-scoped extra approval. **Hub-after-ABI**, not Core MVP. |
| Q139 C | **Partner severity, automated alerts, escalation and withdrawal** | Keep Q114 per-release manual review and Q129 contractual duties, with agreed (not invented) deadlines, notice/remediation evidence and withdrawal preserving Core/data. Deferred Hub. |
| Q140 C | **Private vulnerability reporting: severity, triage, fixes, advisories and coordinated customer communication** | Q130 lead/deputy, scoped tracking and protection of technical details; Q118 GitHub private reports plus dedicated email must be **configured and tested** before external beta. |

## First usable release implications

Keep **Q120 D R1–R6 sequence**. For **R3/R4 (Q119 B MVP)**:
- **R3**: reproducible VM matrix (local plus CI where full VM capability exists), snapshots/fault injection and comparative OS/WebStack evidence with rejection gates; **do not choose** initial OS/stack without proof (Q121/Q122).
- **R4**: PHP website + **external DNS** + ACME **HTTP-01** + HTTPS, A/AAAA and port 80/443 checks; local admin + website-manager (optional MFA), VPS diagnostics, controlled recoverable OS updates, encrypted local panel-config/PHP-file backups with **real restore** and optional remote destination.
- **Distribution**: isolated internal tests, then **private beta by waves** only after license/distribution review, verified security reporting and actually appointed security lead/deputy.

Native authoritative DNS, DNS-01/wildcard, multiple WebStacks, broader SFTP/advanced backups, HA and Hub remain planned. Q136 defines **target role permissions** for first website, not evidence of a functioning SFTP implementation.

## Negative test gates

Reject unsafe WebStack despite good performance results; fail when A/AAAA lead to inconsistent unauthorized targets, port 80 is blocked, or challenge routing fails; interrupt OS update and recover panel/site; restore encrypted config/files using available keys while documenting whole-disk loss limitations; deny site-manager access to other sites, quota escalation and OS upgrades; test beta channel pause without deleting data; duplicate transfers and partner incident escalation.

## Unselected details

VM/CI platform, measured load thresholds, backup encryption and key custody, initial remote provider, domain renewal policy, OS approval defaults, first-site SFTP implementation timing, private-beta contractual caps, transfer cryptography, partner deadlines and named security personnel/mailbox. **No unapproved vendor, number, identity or address is assumed.**
