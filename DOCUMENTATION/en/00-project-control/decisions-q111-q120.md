<!-- forgepanel-doc id=FP-00-Q111-120 revision=1 status=specified -->
# Q111–Q120 decisions — Governance and first functional release

[Français](../../fr/00-project-control/decisions-q111-q120.md) · [ADR](decisions.md) · [Roadmap](implementation-roadmap.md)

## Owner decisions — 5 November 2026

These decisions extend **Q1–Q110** without replacement. State **SPECIFIED**, not implemented.

| Ref | Confirmed choice | Scope and constraints |
|---|---|---|
| Q111 C | AGPL-3.0 plus commercial; exact variant after legal review | Only/or-later and commercial text pending. No LICENSE chosen without approval. |
| Q112 C | Electronic CLA and individual/corporate authority verification before merge | Verify contributor identity, signing authority, consent and evidence. Text/provider not selected. |
| Q113 D | License pools per organization, controlled transfers and server replacement | Scoped assignments, audit and prevention of double allocation, including lost servers. No Linux privileges. |
| Q114 C | Manual review of every partner version, maintenance/security duties and withdrawal | Review each artifact/version, compatibility, signatures, vulnerability contact and safe withdrawal. |
| Q115 D | Sandbox payment adapters first, select real providers by market later | Verified callbacks, duplicates, refunds, concurrency; no market/currency/provider assumed. |
| Q116 C | Configurable retention by data category and jurisdiction within law | Purpose, lawful limits, legal holds, deletion and audit. No invented universal days. |
| Q117 C | Premium revocation by reason: security, fraud, refund or expiry | Reason-specific policy and notices, no interruption of free Core or data deletion. Known revocation ≠ automatic 60-day network grace. |
| Q118 C | GitHub private vulnerability reporting and dedicated verified security email with triage, tracking, notifications | Configure and test both channels before public distribution. No email address or SLA is known. |
| Q119 B | First testable product: installer, CLI, wizard, identity/PostgreSQL and PHP site with domain/HTTPS | Prove actual install→admin→PHP site→HTTPS→management/recovery on a qualified host. |
| Q120 D | Source import → Symfony/PostgreSQL → installer → first site/VPS → generic extension API → Hub | Dependency order is defined in the [roadmap](implementation-roadmap.md). |

## Preserved invariants

Full free and standalone Core, AGPL/commercial strategy pending operative license variant, optional admin MFA, one brand per organization, per-site advised/switchable WebStack and Q47 safety for impactful changes. Premium is optional, never a Linux permission. Premium 60-day offline grace is distinct from hosting resource quota grace.

## First delivery and evidence

Q119 **does not promise** all Q1–Q110 capabilities in the first release: no day-one guarantee of native authoritative DNS, mail, multi-server HA, marketplace, every WebStack or all six OSes qualified. The first PHP site with domain and HTTPS must actually respond on a **tested** OS/profile with authentication, sessions, permissions and recovery. Hub remains deferred until a neutral generic Core extension contract is proven.

The corrected v0.7.1 MFA source remains a **separate archive**, not code imported on GitHub `develop`.

## Open details

AGPL only/or-later, commercial text, CLA platform/legal terms, pool/transfer policy, partner gates, markets/providers, retention limits, revocation cases, verified security contacts, first OS/WebStack and release gate evidence. No implicit defaults are chosen.
