<!-- forgepanel-doc id=FP-00-DECISIONS revision=10 status=documented -->
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

| ADR-050 | Application/security/resource/listener-aware WebStack advisor (Q81 C) | Per-site suggestion based on .htaccess, PHP, OS and isolation; deny incompatible profiles |
| ADR-051 | WebStack switch with temporary route/progressive cutover when feasible (Q82 D) | Plans, snapshots, notice, maintenance, TLS/access checks, recovery; no zero-downtime guarantee |
| ADR-052 | Per-site PHP versions/extensions/FPM/quotas (Q83 C) | Separate panel runtime and validated, scoped pools/settings |
| ADR-053 | ACME, custom certificates, DNS-01, wildcard and renewal (Q84 C) | Domain ownership, compatible DNS provider, secrets and expiry alerts |
| ADR-054 | Files/SFTP + Git Deploy + staging/preview/backup/rollback (Q85 C) | SQL migrations not automatically reversible; no full blue-green/canary requirement |
| ADR-055 | MariaDB/MySQL, PostgreSQL, optional Redis/Valkey (Q86 D) | Tenant-scoped drivers, optional cache/queues and separate panel PostgreSQL |
| ADR-056 | File manager/SFTP + restricted SSH for authorized accounts (Q87 B) | Unix scopes, safe paths, quotas, no implicit web terminal |
| ADR-057 | Protected email, webmail, quarantine, per-domain rules/reports (Q88 C) | SPF/DKIM/DMARC/TLS, antispam/AV and mailbox/domain authorization |
| ADR-058 | Inherited hosting plans/quotas with alerts/usage (Q89 C) | Disk, domain, mailbox, DB, CPU/RAM/PHP/process constraints enforced |
| ADR-059 | Selective restore, staging clone, controlled cross-environment recovery (Q90 D) | Scope, target backup, isolated URLs/secrets and real recovery tests |

| ADR-060 | Maintained PHP, EOL notices and planned migrations (Q91 C) | Per-site PHP/extension inventory and alerts, separate panel PHP, nondestructive transition |
| ADR-061 | Per-site PHP-FPM with stronger Linux confinement (Q92 D) | Separate pools/identities/quotas and verified SELinux/AppArmor/cgroups; pool alone insufficient |
| ADR-062 | Manual or validated webhook Git Deploy per-site policy (Q93 C) | Webhook/ref checks, idempotency, RBAC and redacted logs |
| ADR-063 | Private site-scoped staging, masking/secrets/retention/audit (Q94 D) | Suppress live email/webhooks, authorize copying and controlled expiry/purge |
| ADR-064 | Multiple ACME CAs, DNS-01 and controlled renewal (Q95 C) | DNS adapters, domain ownership, wildcard, protected credentials and alerts |
| ADR-065 | Multiple tenant data engines with separate rights/quotas (Q96 D) | MariaDB/MySQL, PostgreSQL and optional Redis/Valkey; separate Core SQL |
| ADR-066 | Restricted SSH with keys, plan policy, expiry/revocation/audit (Q97 C) | Scoped Linux identities/paths, no implicit web terminal |
| ADR-067 | Swappable Webmail per server/provider and domain policies (Q98 C) | Qualified engines, mailbox isolation, compatible Webmail/quarantine |
| ADR-068 | Soft/hard quotas, grace and admin-approved extension (Q99 D) | Explicit permission, real hard limits, audit/expiry |
| ADR-069 | Audited secure cross-server migration/restore (Q100 D) | OS/WebStack/PHP/DB preflight, encrypted transfer, staging, rotated secrets, recovery |

| ADR-070 | Temporary PHP EOL exception with planned migration (Q101 C) | Admin-authorized per-site scoped expiry, audit, no silently permanent waiver |
| ADR-071 | Isolation profiles selected by certified Linux capabilities (Q102 C) | Plan/site scoped, reject unavailable profiles; FPM pools are not full confinement |
| ADR-072 | Git Deploy per site AND environment with configurable approval (Q103 C) | Separate staging/production ref, signed webhook, rights and approval policies |
| ADR-073 | Extra approval for sensitive data copied into staging (Q104 D) | Files/schema/masked profiles, distinct secrets, retention, purge and audit |
| ADR-074 | Multiple ACME CAs with bounded retry, alert and recovery (Q105 C) | Preapproved alternatives, compatible DNS-01, preserve known-good certificate |
| ADR-075 | Shared/dedicated DB per plan plus optional certified cluster/replication (Q106 D) | Verified drivers and tenant isolation; Core not implicitly clustered |
| ADR-076 | Restricted SSH/allowed IPs, temporary grants and compatible certificates (Q107 C) | Qualified SSH CA, expiry/revocation/audit; neither root nor web terminal |
| ADR-077 | Webmail recommended after security/compatibility/maintenance tests (Q108 D) | No unverified Roundcube/SnappyMail default; server/provider/domain choice |
| ADR-078 | Quota grace duration/cap per plan and resource type (Q109 C) | Limits, expiry and Q99 admin grants never exceed physical capacity |
| ADR-079 | Conditional pre-sync and advanced migration cutover (Q110 D) | Staging/DNS-proxy; replication/failover only when app/infrastructure support, no zero-downtime promise |

| ADR-080 | AGPL-3.0 + commercial; exact variant after legal review (Q111 C) | Strategy retained; only/or-later and commercial text unselected, no operative LICENSE |
| ADR-081 | Electronic CLA with individual/corporate authority checks before merge (Q112 C) | Legal text/entity/signatures/evidence and dual-license grants to approve |
| ADR-082 | Organization license pools, controlled transfers and server replacement (Q113 D) | Audited caps/assignments/recovery, no Linux privilege |
| ADR-083 | Per-partner-release review, maintenance/security and withdrawal (Q114 C) | Continuing manual review, provenance/signatures and incident response |
| ADR-084 | Sandbox payment adapters, providers selected later per market (Q115 D) | No assumed live vendor, region, currency or tax rule |
| ADR-085 | Retention by category and jurisdiction within law (Q116 C) | Configurable limits, legal hold and audit; no invented durations |
| ADR-086 | Reason-scoped premium revocation without stopping Core (Q117 C) | Security/fraud/refund/expiry; known revocation not automatically 60-day grace |
| ADR-087 | GitHub private reports plus verified security email with triage/notices (Q118 C) | Configure and test both before distribution, no fabricated contact |
| ADR-088 | First testable installer/CLI/wizard/identity/PG + PHP site/domain/HTTPS (Q119 B) | Real VM/HTTP/TLS/RBAC/recovery proof, advanced modules not prerequisite |
| ADR-089 | Source → Symfony/PG → installer → first site/VPS → ABI → Hub (Q120 D) | Explicit roadmap gates; commercial Hub cannot gate Core MVP |

| ADR-090 | Choose first OS after prerequisite/VM comparison (Q121 D) | No preselected OS; qualify each supported OS independently |
| ADR-091 | Choose first WebStack after compatibility/security tests (Q122 D) | No mandatory default; per-site recommendation (Q79) remains |
| ADR-092 | MVP external DNS and ACME HTTP-01 for HTTPS (Q123 A) | Verify port-80 challenge/HTTPS; native DNS/DNS-01 remain later |
| ADR-093 | MVP local admin plus website-manager role (Q124 B) | Permanent identity, recovery, sessions/RBAC and optional MFA |
| ADR-094 | MVP VPS observation plus controlled OS package upgrades (Q125 B) | PLAN/preflight/permissions/audit/recovery; no arbitrary root shell |
| ADR-095 | MVP panel-config and PHP-site-file backup with real restore (Q126 B) | Verified integrity/recovery and consistent needed panel PG state, no mandatory 3-2-1 at MVP |
| ADR-096 | Isolated internal tests then authorized private beta (Q127 B) | VM evidence, external-recipient license review, verified security channels and owner approval |
| ADR-097 | Self-service premium transfers plus manual lost-server recovery (Q128 D) | Ownership/possession proof, caps, audit, no duplicate allocation; deferred Hub |
| ADR-098 | Partner contractual maintenance/security duties, alerts and withdrawal (Q129 C) | Review each version and define responsibilities; no invented SLA |
| ADR-099 | Security lead plus deputy and coordinated triage (Q130 C) | Actually verified roles/channels before beta; no invented contact |

| ADR-100 | Local/CI VMs, snapshots, failure injection and OS reports (Q131 D) | Reproducible comparison before OS choice; SKIP ≠ PASS, real system VMs |
| ADR-101 | WebStack load, maintenance, recovery and hard rejection criteria (Q132 D) | No selected first stack; tenant leak/.htaccess bypass/port conflicts disqualify |
| ADR-102 | External DNS A/AAAA, port 80, HTTP-01 and HTTPS diagnosis (Q133 C) | Check IP/vhost, challenge/cert, no required native DNS |
| ADR-103 | OS updates with impact plan, backup, health and recovery (Q134 C) | Authorized idempotent work, no generic root shell |
| ADR-104 | Encrypted local MVP backup plus optional remote destination (Q135 B) | Panel config/PHP files and real restore; later remote/3-2-1 |
| ADR-105 | Website manager can manage PHP/domain/TLS/files/SFTP and scoped restore (Q136 C) | Site RBAC/quotas; no root package updates or other tenants |
| ADR-106 | Private beta by waves, suspension and recovery (Q137 D) | Invites/terms, private bug/release channel, preserve already granted software rights |
| ADR-107 | Premium transfer with crypto evidence and risk-based second approval (Q138 D) | Fraud controls, audit, lost-host recovery, Hub after ABI |
| ADR-108 | Partner severity, automated alerts, escalation and withdrawal (Q139 C) | Q114/Q129 per-release manual review and contracts |
| ADR-109 | Vulnerability triage, fixes, advisories/coordinated customer notices (Q140 C) | Real lead/deputy and verified private channels Q118/Q130 |

## Replaced or unresolved proposals

Vue as the main frontend and Debian-only delivery were replaced by the later Symfony-native frontend and multi-OS requirement. Python and Redis remain optional, not mandatory core services. TOTP enrollment exists in the archive; WebAuthn and permanent authentication remain future work. Prior claims of a working agent, full installer or official public release are not supported by the observed repository.

New decisions must record context, alternatives, rationale, affected contracts, validation and any replaced decision. Changing a requirement requires explicit reconciliation rather than quietly editing history.
