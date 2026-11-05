<!-- forgepanel-doc id=FP-00-CIRP revision=1 status=specified -->
# Q56–Q60 decisions — Payments, channels, identity, retention and offers

[Français](../../fr/00-project-control/commerce-identity-release-policy.md) · [ADR register](decisions.md) · [Configuration Engine](../02-architecture/configuration-engine.md)

## State and scope

On 5 November 2026 the owner **confirmed Q56 C, Q57 C, Q58 C, Q59 C and Q60 C**. Questions **Q61–Q70 are unanswered** and remain open. These are product requirements, **not** operational services, an operative license text or a published release. The Core's AGPL-3.0/commercial model remains pending exact license texts; essential Core capabilities remain free and private Hub delivers optional commercial functions.

## Confirmed decisions

| ID | Choice | Requirement and responsible component |
|---|---|---|
| Q56 C | **Multiple payment providers with independent drivers** | Hub owns provider adapters, orders and callbacks; no live integration, key or specific provider selected. Free Core never requires payment. |
| Q57 C | **Stable, Beta, Dev** channels, progressive rollout and rollback | Core locally verifies signatures, version, compatibility and authorization before updates; Hub can publish metadata/campaigns. Irreversible database migrations are not reversed by rolling back binaries alone. |
| Q58 C | **Local accounts + optional SSO/OIDC** | Core retains a local administrator and controlled recovery path; an OIDC provider may be configured separately for an organization and/or publisher staff. Administrator MFA remains **optional**. |
| Q59 C | **Configurable retention by category**, subject to law and security | Operational logs, audit, sessions, metrics, diagnostics, payments and personal information use distinct policies. No universal day count has been selected. |
| Q60 C | **Perpetual purchases + recurring subscriptions + trials, coupons, bundles and add-ons** | Hub owns product offers, commercial grants and billing; confirmed verified server-side payment events lead to idempotent entitlement grants. “Perpetual” does not implicitly mean perpetual support/updates. |

## Configuration Engine: domain boundaries

### Payment and commercial offers (Hub only)

Independent payment adapters should declare provider identity/capabilities and operations for creating checkout sessions, verifying signed notifications, retrieving transactions, reconciliation, refund events and subscription status. Capture/refund operations require explicitly supported capabilities and operator permission. Secrets stay in protected storage. No provider is assumed or set as default.

Commercial offers must allow purchase kind (perpetual/subscription/trial), SKU, currency, price and terms version, duration/renewal, included rights, bundles, add-ons, discount coupons with constraints, audit and expiry policy. Taxes, geographic markets, invoices and refunds still require legal/technical decisions. Never grant rights based solely on a browser success URL.

### Publishing and updates

Proposed channel identifiers are `stable`, `beta`, `dev`. Allowed server/account channel selection requires Core/OS/WebStack compatibility and authorization. Progressive rings and pilot cohorts are configurable. Every update requires verified metadata/artifacts, backup and recovery planning; local application goes through authorization and the Configuration Engine. Dev/Beta channels are not automatically suitable for production. Automatic update defaults and rollout percentages are not decided (Q61–Q70).

### Accounts and access

Local login must remain functional without any external provider. Optional OIDC must validate token issuer, audience, integrity and scoped account identity; group claims are **not automatically grants of Linux or Core permissions**. Do not silently merge accounts by email alone. IdP outage must not eliminate controlled, audited local recovery. Administrator MFA may be enabled or skipped. Session configuration, trust, provisioning and organization-specific settings require implementation and tests.

### Retention

Proposed categories: privileged audit logs, system logs, limited metrics, jobs, backups, support tickets, consented diagnostics, session identifiers and commercial records. Each category declares purpose, legal/security basis, ownership, allowable minimum/maximum retention, anonymization, scheduled deletion, archive policy and execution evidence. Operator configuration must not enable deletion in breach of law, litigation hold, audit requirements or restoration needs. Commercial-category policies remain Hub-owned.

## Cross-project invariants

Hub communication is optional or contractually bounded for paid services, with separate registration/communication preferences (Q6). Payment, IdP or update delivery outages cannot stop free Core startup, hosting or repair. After the eligible 60-day commercial offline grace, only **new premium operations** are blocked; existing state/data are preserved (Q52).

## Required tests (not performed)

- Duplicate/out-of-order webhooks, post-payment crash, provider outage, coupon limits, trial expiry, exactly-once effective grants.
- Wrong/incompatible update channel, invalid signature, rollout rings, faulty release, config recovery and irreversible SQL migration.
- SSO/local identity confusion, misconfigured OIDC, cross-organization access, IdP outage and safe local recovery.
- Contradictory retention windows, partial purges, statutory holds, backup retention and secret redaction.

## Open decisions

Q61–Q70: signing/distribution, installer, DNS, email, backups, sensitive operations, multi-server, monitoring, WebStack and panel design. Also undecided: actual payment providers, tax setup, automatic update policy, OIDC multi-tenant boundaries, per-category retention durations, and perpetual-purchase versus maintenance rights. Do not silently assign defaults.
