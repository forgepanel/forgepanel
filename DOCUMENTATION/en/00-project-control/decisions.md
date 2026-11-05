<!-- forgepanel-doc id=FP-00-DECISIONS revision=2 status=documented -->
# Decision register

[Français](../../fr/00-project-control/decisions.md) · [Project control](README.md)

Source IDs refer to the [baseline](../19-audits-risks/baseline.md). A decision adopted as a design baseline is not evidence of implementation.

| ID | Decision and authority | State / consequence |
|---|---|---|
| ADR-001 | ForgePanel is the new product; WCP360 is historical context (SRC-02) | Confirmed identity; no automatic WCP360 code/licensing/commercial inheritance |
| ADR-002 | Symfony/PHP + Twig/UX; Go for system operations; PostgreSQL (SRC-02, SRC-03 manifest) | Design baseline; archive has Twig but not installed UX/Tailwind/Messenger dependencies |
| ADR-003 | Multi-OS from the start (explicit owner request, SRC-02) | Required: Debian 12/13; Ubuntu and AlmaLinux; archive planning matrix selects 24.04/26.04 and 9/10; no certification |
| ADR-004 | Composable web engines, five profile IDs (SRC-02/03) | Specified; profile selection exists, service provisioning does not |
| ADR-005 | One-command installation followed by web setup and CLI recovery (owner, SRC-02) | Required outcome; not delivered by `install plan` |
| ADR-006 | Bootstrap token instead of Linux password in browser (SRC-02/03) | Retained security baseline; application super-admin is not Linux root |
| ADR-007 | PostgreSQL owns web bootstrap transaction (SRC-03) | Archive implementation supersedes v0.6 file-token integration; SQL integration unverified |
| ADR-008 | Direct ports 8447/8446 and distinct portal hosts (SRC-02/03) | Prototype defaults; 446/447 suggestion not retained; USER remains closed; port changes do not isolate cookies |
| ADR-009 | Bilingual documentation, one changelog, four permanent branches (explicit owner, SRC-01) | Governs this change; no release/deployment is authorized merely by branch creation |
| ADR-010 | Application runtime policy | Open: archive accepts PHP >=8.2; earlier PHP 8.4 preference is not a certified six-OS package policy |
| ADR-011 | Licensing and contributions | **AGPL-3.0 + commercial (Q48)**; only/or-later variant and commercial terms require approval; audit third-party rights before publishing LICENSE |
| ADR-012 | Documentation tooling uses Python standard library only | New bounded tooling choice; does not make Python a product runtime dependency |
| ADR-013 | Administrator MFA optional (explicit owner decision, 2026-11-05) | Initial account without mandatory TOTP; enroll now or later, sensitive step-up; v0.7 source still blocks setup until corrected on import. |
| ADR-014 | ForgePanel-Hub as private detached publisher extension in `yyogas/forgepanel-hub` | Same standard Core with or without Hub; generic ABI absent; never inject private PHP or grant root. |

| ADR-015 | Full free Core, optional premium/support (Q2, Q50 B) | Specialist plugins, managed/cloud services, verified-partner offers and paid support; never gate the AGPL Core |
| ADR-016 | Phased audiences (Q3, Q54 D) | Shared hosting + VPS administration first; developer/container and reseller work later, once verified |
| ADR-017 | Customer runtimes (Q4, Q51 C) | **Docker and Podman** as separate drivers with OS/security validation, independent of panel runtime |
| ADR-018 | White-label (Q5, Q55 A) | **One brand per organization**, configurable logo/domain/theme/email/portal, bounded by permissions; no multiple brands in same organization |
| ADR-019 | Separate Hub enrollment and communication consent (Q6) | Distinct opt-ins for registration, premium rights, versions, support diagnostics and marketing; no implicit collection |
| ADR-020 | 60-day commercial offline grace (Q7, Q52 A) | Once exhausted, **block new premium operations but preserve the existing state/data**; never stop free Core hosting; explicit revocation/expiry handling still needs policy |
| ADR-021 | Official and verified-partner catalog (Q8, Q53 B) | **Apply + manual verification** before partner approval; review/sign/withdraw per version; no open publishing |
| ADR-022 | Sensitive changes: plan, validate, back up and recover (Q47) | Future Configuration Engine; no universal OS/SQL rollback guarantee |

| ADR-023 | Contributor policy (Q49 A) | **CLA** permitting dual licensing, with verified acceptance/evidence; legal text, entity and signing still open |
| ADR-024 | Commercial protection of modules and subscriptions (owner clarification) | Access controls for independently licensable paid packages/services, no restriction of AGPL Core freedoms; Hub/plugin coupling requires legal review |

| ADR-025 | Multiple independent payment providers (Q56 C) | Hub provider adapters; no vendor or credentials selected; authenticated/idempotent payment callbacks |
| ADR-026 | Stable, Beta, Dev channels (Q57 C) | Progressive rollout, signatures, compatibility checks and recovery; automatic update policy still open |
| ADR-027 | Local accounts plus optional SSO/OIDC (Q58 C) | Retain local authentication/recovery; external identity scoped and permissioned, MFA still optional |
| ADR-028 | Per-category configurable retention (Q59 C) | Durations configurable within legal/security bounds; no exact periods yet |
| ADR-029 | Perpetual purchases, subscriptions, trials/coupons/bundles/add-ons (Q60 C) | Hub commercial model; server-verified events grant rights, not browser redirects |

## Replaced or unresolved proposals

Vue as the main frontend and Debian-only delivery were replaced by the later Symfony-native frontend and multi-OS requirement. Python and Redis remain optional, not mandatory core services. TOTP enrollment exists in the archive; WebAuthn and permanent authentication remain future work. Prior claims of a working agent, full installer or official public release are not supported by the observed repository.

New decisions must record context, alternatives, rationale, affected contracts, validation and any replaced decision. Changing a requirement requires explicit reconciliation rather than quietly editing history.
