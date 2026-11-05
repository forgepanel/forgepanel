<!-- forgepanel-doc id=FP-00-DECISIONS revision=4 status=documented -->
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

| ADR-030 | Signed CI/CD + anti-rollback + approvals (Q61 C) | Signed metadata/artifacts, protected trust keys and publication gates; not implemented |
| ADR-031 | Universal installer + signed DEB/RPM repositories (Q62 C) | Verified bootstrap, resumable installer and OS-specific packages; not yet functional |
| ADR-032 | Local DNS and external-provider drivers (Q63 C) | Zone authority, record validation and controlled migration |
| ADR-033 | Native mail and external providers (Q64 C) | Local/external drivers, tenancy and DNS/TLS validation |
| ADR-034 | Encrypted replicated immutable remote backup with recovery (Q65 D) | Restore tests, storage constraints and measured recovery targets |
| ADR-035 | Sensitive reauthentication and optional extra approval (Q66 C) | Admin MFA remains optional; approval policy, audit and emergency recovery |
| ADR-036 | Multi-server and HA/clustering/DR (Q67 D) | Phased target; no certified cluster or Hub runtime dependency |
| ADR-037 | Local monitoring, email/webhooks and external integrations (Q68 C) | Configurable rules and controlled external data |
| ADR-038 | Per-site WebStacks and ingress by IP/port (Q69 D) | Exclusive listeners, TLS, `.htaccess` and planned changes; Q79 specifies **per-site** recommendation and later switching |
| ADR-039 | Visual widget/navigation editor with one brand (Q70 D, Q55 A) | Approved components, theme/history, scoped rights and no arbitrary code |

| ADR-040 | Protected keys, anti-rollback and rotation (Q71 C) | CI signing with KMS/HSM or protected key service, trusted metadata, rotation/recovery; vendor open |
| ADR-041 | Clean install plus controlled existing-service adoption (Q72 C) | Read-only inventory, plan, conflicts, approval and backup/restore; no silent takeover |
| ADR-042 | Multi-driver DNS with local recommendation after tests (Q73 D) | No mandatory local DNS engine; certify capability before recommending |
| ADR-043 | Postfix + Dovecot first native mail driver plus external (Q74 C) | Initial local backend, provider/relay adapters and tested security |
| ADR-044 | 3-2-1 backups, tested restores and configurable replication (Q75 C) | Target backup profile, cadence/destinations by capabilities, Q65 immutability preserved |
| ADR-045 | Per-action approvals and audited recovery (Q76 C) | Reauthentication, separation of duties and safe break-glass; MFA still optional |
| ADR-046 | Multi-server first, phased HA/external orchestrators as optional modules (Q77 D) | Later phase, no cluster needed for initial hosting |
| ADR-047 | Prometheus + OpenTelemetry adapters (Q78 C) | Configurable exporters, data filtering and outbound consent |
| ADR-048 | **Per-site** recommended WebStack, changeable after creation (Q79 D, owner clarification) | Explicit initial choice; future switch uses PLAN/VALIDATE/STAGE/HEALTH/RECOVER; preserve `.htaccess` and listeners |
| ADR-049 | Official/partner widgets plus declarative custom widgets (Q80 C) | Authorized data sources, manifests, RBAC, safe rendering, one brand per org, no arbitrary code |

## Replaced or unresolved proposals

Vue as the main frontend and Debian-only delivery were replaced by the later Symfony-native frontend and multi-OS requirement. Python and Redis remain optional, not mandatory core services. TOTP enrollment exists in the archive; WebAuthn and permanent authentication remain future work. Prior claims of a working agent, full installer or official public release are not supported by the observed repository.

New decisions must record context, alternatives, rationale, affected contracts, validation and any replaced decision. Changing a requirement requires explicit reconciliation rather than quietly editing history.
