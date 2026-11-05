<!-- forgepanel-doc id=FP-00-POLICY revision=8 status=documented -->
# Product decisions of 5 November 2026 — free Core, commercial model and configuration

[Français](../../fr/00-project-control/product-policy.md) · [ADR register](decisions.md) · [Configuration Engine](../02-architecture/configuration-engine.md)

## Owner decisions (confirmed, not implemented)

| Reference | Decision | Scope and invariants |
|---|---|---|
| Q1, Q48 | **AGPL-3.0 + commercial license** | Dual licensing confirmed; only/or-later variant, copyright ownership and commercial agreement remain to approve before adding LICENSE. |
| Q2, Q50 | **Full free Core + paid specialist plugins, managed/cloud services, partner offers and support** | Core bootstrap, essential hosting and recovery never depend on commercial entitlement or Hub. |
| Q3, Q54 | **Shared hosting + VPS administration first** | Developers/containers and resellers follow through tested milestones. |
| Q4, Q51 | PHP, Node.js, Python and **Docker + Podman** | Two independent drivers and compatible host selection; customer runtimes separate from Symfony; Python remains optional for automation. |
| Q5, Q55 | **One brand per organization** | Configurable logo, theme, HTTPS domain, messages and portal for one unique brand identity within each organization; no internal multi-brand. |
| Q6 | Separate consent for registration and Hub communications | Standard installation operates independently; explicit choices for enrollment, premium-right verification, update metadata, limited metrics, support diagnostics and marketing notices. No implicit hosting-data collection. |
| Q7, Q52 | **60 days**, then block new premium operations, preserve existing | For eligible previously verified premium rights within contractual expiry; no data removal or free Core disruption. Explicit revocation/expiry needs further policy. |
| Q8, Q53 | **Official + partner applications subject to manual verification** | No self-publication without approval, even after applying; per-version artifact review and signature required. |
| Q47 | Plan, validate, back up and recover sensitive changes | Present impact, run configuration tests, back up before alteration, perform health checks and compensate/recover where possible. No universal SQL/OS rollback guarantee. |

These decisions complement ADR-013: **administrator MFA remains optional**, including first setup. A commercial right or UI mode cannot bypass local Core authorization or Linux permissions.

## Product and subscription protection

The owner wants paid packages and subscriptions protected. Hub may enforce verified purchases, authorized downloads, renewals, hosted services and commercial update entitlements for **legally independent** premium products. AGPL recipients may exercise the rights of lawfully obtained AGPL copies without a new license fee; an alternative commercial license does not erase those freedoms. Review the actual coupling of proprietary packages. See [licensing and commercial boundary](license-commerce.md).

## Free Core versus commercial services

The Core covers installation, initial administrator, account and site management, isolation, domains, SSL, file access, native service administration, quotas, backup and recovery. The precise first-release functionality list needs component-level acceptance tests.

Premium offers may cover non-essential extensions, managed services, priority support, approved partner packages, hosted catalog services and specialized tooling. A security function essential to the Core must not be rebranded into a paywall. Billing and commercial entitlements belong to Hub, not Core bootstrap or recovery.

## 60-day rule — principle

Hub may issue locally verifiable entitlement evidence. The client retains the last authentic, known-valid grant; if the network disappears, entitlement enters `offline-grace` for **at most 60 days since the last successful verification**, without extending a documented commercial expiration date. Behavior after expiration, explicit revocation, clock anomalies, or no first validation requires a separate product decision. Remote control may not stop customer hosting. This period applies to optional entitlements, never the full free Core.

## Customization and authorization

Organization UI overrides are bounded by server policy. Sensitive settings require effective authorization and audit: white-label permission does not grant access to private TLS keys or other tenants. Operators can inspect inherited values and why settings are locked.

## Confirmed Q56–Q60

Q56 **C** — independent payment provider drivers; Q57 **C** — Stable/Beta/Dev channels, progressive rollout and controlled rollback; Q58 **C** — local accounts plus optional SSO/OIDC; Q59 **C** — per-category configurable retention within legal/security bounds; Q60 **C** — perpetual purchases, subscriptions, trials, coupons, bundles and add-ons.

Core remains free and complete. Hub owns payments/offers; Core owns local update verification and execution. No particular vendor, rollout percentage, retention day count or automatic-update default has been chosen. See [Q56–Q60 technical decisions](commerce-identity-release-policy.md).

## Confirmed Q61–Q70

The owner approved Q61 C, Q62 C, Q63 C, Q64 C, Q65 D, Q66 C, Q67 D, Q68 C, Q69 D and Q70 D: signed publishing and universal installer, modular local/external DNS/mail, replicated/immutable backups, sensitive action approvals, phased multi-server/HA, external monitoring, multiple web ingresses and visual customization. **One brand per organization** (Q55) and **optional admin MFA** remain unchanged. HA and advanced functions are phased, not mandatory for the first release. [Q61–Q70 requirements](infrastructure-decisions.md).

## Confirmed Q71–Q80

New choices specify protected key infrastructure with rotation/anti-rollback (Q71), reversible adoption of existing Linux services (Q72), a local DNS engine recommended after qualification (Q73), Postfix/Dovecot with external providers (Q74), 3-2-1 backups and recovery testing (Q75), per-action extra approval (Q76), phased HA/orchestration (Q77), Prometheus/OpenTelemetry (Q78), **per-site WebStack recommendation with later switching** (Q79), and controlled declarative widgets (Q80). None is implemented. [Q71–Q80 specification](decisions-q71-q80.md).

## Confirmed Q81–Q90

ForgePanel will offer an explainable **per-site WebStack** based on application, PHP, OS, security, isolation and listeners, with later controlled switching: maintenance, notification and temporary testing/progressive cutover **only when topology permits**. Other selected features include per-site PHP-FPM/extensions, ACME/DNS-01/wildcards, Git Deploy/staging, MariaDB/MySQL/PostgreSQL with optional Redis/Valkey, file manager/SFTP with restricted SSH, webmail/quarantine, inherited quotas and secure clone/restore. One brand per organization (Q55) and optional admin MFA are unchanged. [Q81–Q90 specification](decisions-q81-q90.md).

## Confirmed Q91–Q100

The owner approved maintained PHP with EOL alerts and per-site migration (Q91), stronger PHP-FPM isolation (Q92), validated manual/webhook Git Deploy (Q93), staging masking/secrets/retention/audit (Q94), multiple ACME issuers and DNS-01 drivers (Q95), multiple tenant SQL/cache engines (Q96), scoped expiring/audited SSH (Q97), Webmail chosen by provider/domain (Q98), bounded quota grace and authorized allocation (Q99), and secure cross-server migration/restore with privacy/recovery (Q100). These requirements **do not create working services** or Core dependence on Hub. [Q91–Q100 decisions](decisions-q91-q100.md).

## Confirmed Q101–Q110

The choices add **time-limited** PHP exceptions and planned migration (Q101), OS-certified plan/site isolation profiles (Q102), Git manual/webhook with per-environment approval (Q103), specially approved sensitive staging copies (Q104), bounded retries/recovery across ACME issuers (Q105), shared/dedicated DB and optional certified clusters (Q106), temporary/certificate-based SSH where available (Q107), Webmail recommendation after tests (Q108), quota grace by plan/resource (Q109) and conditional pre-sync/replication/failover (Q110). Core remains standalone; Hub has no access to hosted resources. [Q101–Q110](decisions-q101-q110.md).

## Confirmed Q111–Q120

Exact AGPL variant follows **legal review** (Q111 C); electronic CLA and verification of individual/corporate signing rights precede merge (Q112 C). Hub plans organization license pools/transfers/server replacement (Q113 D), manual review of every partner release and withdrawal (Q114 C), sandbox payment adapters before per-market provider selection (Q115 D), per-jurisdiction/category retention (Q116 C), and reason-scoped premium revocations without stopping free Core (Q117 C). Security channels chosen are **private GitHub reporting plus verified dedicated email**, with triage/notices (Q118 C); no such address/channel is automatically configured.

**Q119 B first functional version** covers verified installer, CLI, wizard, identity/PostgreSQL and manageable PHP site/domain/HTTPS. **Q120 D specifies the dependency order**: sources → Symfony/PG → installer → first site/VPS → neutral Core ABI → Hub. [Decisions](decisions-q111-q120.md) · [Roadmap](implementation-roadmap.md). All other Q1–Q110 functions remain phased goals.

## Open follow-ups — no default assumed

Q48–Q55 are **confirmed** (see table). Open details include AGPL only/or-later and commercial grant text, CLA and copyright ownership, precise independent premium-package conditions, OS default runtime and containment, explicit revocation/expiry versus network loss, partner review criteria, exact delivery milestones and verified domain ownership for one brand per organization. Operational details for Q56–Q70 (providers, policies, security and operations) still need design and validation.

**State: documented owner decisions, no implementation.** See [project status](status.md) and [modules](../04-modules/README.md).
