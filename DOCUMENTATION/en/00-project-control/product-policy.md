<!-- forgepanel-doc id=FP-00-POLICY revision=1 status=documented -->
# Product decisions of 5 November 2026 — free Core, commercial model and configuration

[Français](../../fr/00-project-control/product-policy.md) · [ADR register](decisions.md) · [Configuration Engine](../02-architecture/configuration-engine.md)

## Owner decisions (confirmed, not implemented)

| Reference | Decision | Scope and invariants |
|---|---|---|
| Q1 | Dual licensing | Model confirmed; **exact license texts, rights holders, contributions and exceptions remain undecided**. No LICENSE file has been chosen. |
| Q2 | Full free Core + premium components + support | Essential hosting and recovery remain usable without a paid license or Hub. Premium offers concern clearly distinguished optional services or components. |
| Q3 | All target audiences in phases | Shared hosting and VPS first; developers and resellers later, with extensible contracts rather than claims of shipped functions. |
| Q4 | PHP + Node.js + Python + containers | Configurable application runtimes, distinct from the panel's PHP runtime; Core automation stays Go/Symfony, Python is not mandatory. Container runtime remains a choice. |
| Q5 | Full white-label by organization | Organization/reseller-specific name, logo, favicon, palette, themes, domains/HTTPS, email templates and portals; subject to RBAC, separate cookie/session origins and domain validation. |
| Q6 | Separate consent for registration and Hub communications | Standard installation operates independently; explicit choices for enrollment, premium-right verification, update metadata, limited metrics, support diagnostics and marketing notices. No implicit hosting-data collection. |
| Q7 | **60 days** of offline grace | For previously verified premium entitlements, subject to contractual validity and expiry; never shut down essential Core services or delete customer data. Revocation, time source and expiry remain to define. |
| Q8 | Official + verified partners | Publisher-governed catalog, approved partner identities, signatures, compatibility and review; no unrestricted public publishing now. |
| Q47 | Plan, validate, back up and recover sensitive changes | Present impact, run configuration tests, back up before alteration, perform health checks and compensate/recover where possible. No universal SQL/OS rollback guarantee. |

These decisions complement ADR-013: **administrator MFA remains optional**, including first setup. A commercial right or UI mode cannot bypass local Core authorization or Linux permissions.

## Free Core versus commercial services

The Core covers installation, initial administrator, account and site management, isolation, domains, SSL, file access, native service administration, quotas, backup and recovery. The precise first-release functionality list needs component-level acceptance tests.

Premium offers may cover non-essential extensions, managed services, priority support, approved partner packages, hosted catalog services and specialized tooling. A security function essential to the Core must not be rebranded into a paywall. Billing and commercial entitlements belong to Hub, not Core bootstrap or recovery.

## 60-day rule — principle

Hub may issue locally verifiable entitlement evidence. The client retains the last authentic, known-valid grant; if the network disappears, entitlement enters `offline-grace` for **at most 60 days since the last successful verification**, without extending a documented commercial expiration date. Behavior after expiration, explicit revocation, clock anomalies, or no first validation requires a separate product decision. Remote control may not stop customer hosting. This period applies to optional entitlements, never the full free Core.

## Customization and authorization

Organization UI overrides are bounded by server policy. Sensitive settings require effective authorization and audit: white-label permission does not grant access to private TLS keys or other tenants. Operators can inspect inherited values and why settings are locked.

## Open follow-ups — no default assumed

- **Q48**: precise open-source arm of dual licensing (AGPL-3.0-only / GPL-3.0-only / other) and commercial conditions.
- **Q49**: contributor rights/CLA, third-party licenses and documented ownership required for dual licensing.
- **Q50**: precise free-Core/premium component boundaries.
- **Q51**: Docker vs Podman vs multiple adapters and client container isolation.
- **Q52**: grace behavior for expired, revoked or never-verified grants, alerts and no destruction.
- **Q53**: partner review standards and update responsibility.
- **Q54**: exact module priority order within phases.
- **Q55**: reseller white-label domain constraints, certificate rules and anti-impersonation.

**State: documented owner decisions, no implementation.** See [project status](status.md) and [modules](../04-modules/README.md).
