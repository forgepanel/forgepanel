<!-- forgepanel-doc id=FP-00-Q71-80 revision=1 status=specified -->
# Q71–Q80 decisions — Configurable operations and per-site WebStacks

[Français](../../fr/00-project-control/decisions-q71-q80.md) · [Decision register](decisions.md) · [WebStack architecture](../02-architecture/site-webstack-advisor.md)

## Confirmed decisions (5 November 2026)

These choices **extend Q1–Q70 without superseding them**. They are **specified product requirements, not implemented features**. Free AGPL Core remains operational without Hub; optional administrator MFA, one brand per organization and Q47 safe changes still apply.

| ID | Choice | Contract / limits |
|---|---|---|
| Q71 C | **KMS/HSM or protected signing service, anti-rollback metadata and key rotation** | Root trust, role-separated keys, signatures, offline verification, controlled delegation/rotation/revocation. Exact vendor and protocol remain open. |
| Q72 C | **New-server install plus controlled adoption of existing services** | Read-only discovery, resource ownership inventory, plan/conflict check, backup, explicit takeover approval, health tests and recovery. Reject uncontrolled adoption. |
| Q73 D | **Multiple DNS drivers; local engine recommended after testing** | Detect actual OS/capabilities and zone needs; compare engines/providers without locking one in. Zone delegation/migration and DNSSEC according to capabilities. |
| Q74 C | **Postfix + Dovecot first local driver; external providers and relays** | Controlled local mail with interchangeable providers; validate MX/SPF/DKIM/DMARC, TLS, antispam, reputation and secrets. |
| Q75 C | **3-2-1 backup profile with scheduled restore tests and configurable replication** | Multiple copies/media/locations and an offsite copy, ideally immutable; show hardware, cost, RPO/RTO constraints and restore evidence. |
| Q76 C | **Per-action configurable approval plus secure emergency recovery** | Recent authentication by risk, independent extra approval when required, actor separation and audit; secure local recovery when approvers unavailable. MFA remains optional. |
| Q77 D | **Multi-server first, then phased HA and external orchestrators** | Go agents/controller, groups, policies, desired/observed state; add HA/orchestrators only after quorum/partition/recovery validation. |
| Q78 C | **Prometheus and OpenTelemetry through adapters** | Supported metrics/traces/events according to capabilities, configurable exporters and receivers. No tenant-data harvesting or nonconsensual Hub export. |
| Q79 D + owner clarification | **Initial per-site recommendation, free selection and later switching** | Do not force a server-wide profile; explain reasons/prerequisites/incompatibilities. Switching a live site requires a verified recoverable plan, not a simple toggle. |
| Q80 C | **Official/partner widgets plus declarative custom widgets** | Versioned manifest, authorized data sources, RBAC, query limits and safe rendering. No arbitrary PHP/JS/shell execution or access to other tenants' secrets. |

## Shared configuration rules

Actual OS capabilities, global server policy and organization/plan/account/site scope govern each setting. Low-risk presentation changes may be immediate. Service/network/identity/storage changes follow Q47: **PLAN → VALIDATE → SNAPSHOT/BACKUP → APPLY → HEALTH CHECK → COMMIT or RECOVER/COMPENSATE**. Partial failures and irreversible migrations must be visible; universal rollback is not promised.

## Phased priorities without simultaneous-delivery promises

1. **Foundation**: Symfony/Go/PostgreSQL Core, verified installer, identities, VPS, first websites, safe config, web profiles and recovery tools.
2. **Services**: Postfix/Dovecot, qualified DNS default chosen by tests, external adapters, 3-2-1 backups, recovery drills and metrics.
3. **Ecosystem**: HA, external orchestrators, partner widgets, full distribution/instrumentation when tested.

Exact OS/service certification order is open. Q73 does not name a final local DNS product; Q71 does not select a KMS/HSM vendor; Q75 does not prescribe backup intervals or storage provider.

## Required verification

- Key rotation: stale keys, forged signatures, rollback, overlapping signing windows.
- Adoption: foreign config, down network, listener collision, non-overwriting external files, recovery.
- DNS/mail: delegation, open-relay defense, duplicate records, TLS/DNSSEC and provider outage.
- Backups: claimed 3-2-1 copies versus reality, isolated restore including keys, immutability/replication.
- Approvals: single admin, independent approver, audited emergency access, CSRF and bypass.
- HA/telemetry: partitions, outgoing data, agent versions and missing metrics.
- WebStack: recommendation correctness, incompatible denial, `.htaccess`, PHP isolation, listeners, TLS and recovery after switches.
- Widgets: cross-tenant separation, XSS, authorized data sources and permissions.

[Per-site WebStack recommendation and switching](../02-architecture/site-webstack-advisor.md) · [Configuration Engine](../02-architecture/configuration-engine.md) · [Q61–Q70 decisions](infrastructure-decisions.md)
