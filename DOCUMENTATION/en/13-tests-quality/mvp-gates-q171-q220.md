<!-- forgepanel-doc id=FP-13-Q171-220 revision=1 status=specified -->
# Q171–Q220 — decision-linked acceptance matrix

[Français](../../fr/13-tests-quality/mvp-gates-q171-q220.md) · [QA index](README.md) · [Decisions](../00-project-control/decisions-q171-q220.md)

**PLANNED — NOT EXECUTED.** Fifty owner-approved product directions generate fifty planned acceptance cases. These rows are test requirements, not passing tests, and must not be confused with documentation CI or 32 previous App Center VM tests. [Machine-readable acceptance register](../../evidence/acceptance-q171-q220-v1.json).

| Case | Choice | Acceptance target | Status |
|---|---|---|---|
| ACCEPT-Q171-01 | D | Only approved qualified native recipes enter staged categories; incompatible versions remain unavailable | PLANNED |
| ACCEPT-Q172-01 | D | Provisioning create/suspend/retry enforces typed scopes, idempotency, audit and denied unrelated tenants | PLANNED |
| ACCEPT-Q173-01 | D | Bound multiscanner jobs, quarantine/release and false-positive handling without destructive effects | PLANNED |
| ACCEPT-Q174-01 | C | WAF candidate stays in detect mode until qualified blocking test and controlled recovery | PLANNED |
| ACCEPT-Q175-01 | D | Cross-portal route, cookie/session, API and theme separation; no privilege leakage | PLANNED |
| ACCEPT-Q176-01 | D | Core PHP/HTTPS R4 verified before staged native then independent container rollout | PLANNED |
| ACCEPT-Q177-01 | D | Admin categories adapt without accepting an incompatible or unreviewed recipe | PLANNED |
| ACCEPT-Q178-01 | D | Signed local import and partner versions fail closed until manual approval | PLANNED |
| ACCEPT-Q179-01 | D | Simple/advanced wizard preview cannot bypass permissions, backup or preflight | PLANNED |
| ACCEPT-Q180-01 | D | Lower-scope config override cannot exceed global/server safety constraints or lose revision history | PLANNED |
| ACCEPT-Q181-01 | D | Unsupported SQL engine for selected app is rejected, with tenant-scoped DB grants | PLANNED |
| ACCEPT-Q182-01 | D | Version pinning, EOL warning and per-site upgrade policy cannot force unsupported releases | PLANNED |
| ACCEPT-Q183-01 | D | Per-app maintenance window, staging and approvals respected; no unapproved auto-update | PLANNED |
| ACCEPT-Q184-01 | D | Consistent files/SQL restore checked and irreversible migration warning shown | PLANNED |
| ACCEPT-Q185-01 | D | Uninstall prompts explicit retention; unauthorized file/SQL/backup purge refused | PLANNED |
| ACCEPT-Q186-01 | D | Existing app detected read-only; no adoption or takeover before authorization | PLANNED |
| ACCEPT-Q187-01 | D | Bulk installation respects concurrency, quotas, cancellation and crash recovery | PLANNED |
| ACCEPT-Q188-01 | D | Staging data masked; live mail/webhook blocked; independent credentials verified | PLANNED |
| ACCEPT-Q189-01 | D | Secrets access by site/actor limited and audited; rotation never leaks credentials | PLANNED |
| ACCEPT-Q190-01 | D | Delegated operator cannot install outside owned site/organization/plan | PLANNED |
| ACCEPT-Q191-01 | D | Unqualified host or plan cannot activate container engine by bypass | PLANNED |
| ACCEPT-Q192-01 | D | Docker-only recipe cannot silently run under Podman or vice versa | PLANNED |
| ACCEPT-Q193-01 | D | Rootless preferred; rootful exception denied without scoped qualified approval and audit | PLANNED |
| ACCEPT-Q194-01 | C | Raw arbitrary Compose/unknown provider disallowed even if user requests it | PLANNED |
| ACCEPT-Q195-01 | D | Digest/signature mismatch, revoked version or unapproved registry blocks image use | PLANNED |
| ACCEPT-Q196-01 | D | Privileged container/socket/sensitive host mounts denied by default | PLANNED |
| ACCEPT-Q197-01 | D | Cross-tenant network traffic/egress/ingress denied outside approved network policy | PLANNED |
| ACCEPT-Q198-01 | D | Volume quotas, encrypted backup, retention and real restore verified | PLANNED |
| ACCEPT-Q199-01 | D | Physical host caps defeat higher tenant quotas for CPU/RAM/PIDs/I/O/storage | PLANNED |
| ACCEPT-Q200-01 | C | Assistant export/import requires approved backup and confirmation; blind auto-conversion denied | PLANNED |
| ACCEPT-Q201-01 | D | Tampered, replayed or downgraded catalog rejected through trust-root and version policy | PLANNED |
| ACCEPT-Q202-01 | D | Unapproved publisher or single partner release cannot self-publish | PLANNED |
| ACCEPT-Q203-01 | D | Installed-version vulnerability risk prompts scoped alert/remediation approval, no unsafe auto-fix | PLANNED |
| ACCEPT-Q204-01 | D | High-risk recipe withdrawn for new installs without deleting existing tenant data | PLANNED |
| ACCEPT-Q205-01 | D | Quarantined malware item can be reviewed/restored after authorized false-positive procedure | PLANNED |
| ACCEPT-Q206-01 | D | Inherited WAF detect/block policies simulate, contain exception scope and recover last-known-good | PLANNED |
| ACCEPT-Q207-01 | D | Sensitive logs are redacted, scoped, retained and export-controlled | PLANNED |
| ACCEPT-Q208-01 | D | Sensitive action respects effective risk-based step-up/approval; MFA still optional | PLANNED |
| ACCEPT-Q209-01 | D | Concurrent plans cannot double-reserve ports/resources; apply-time checks prevent TOCTOU | PLANNED |
| ACCEPT-Q210-01 | D | Artifact download rejects SSRF, unsafe redirects, cache corruption and unverified resumes | PLANNED |
| ACCEPT-Q211-01 | D | Native and Container spaces separate, with shared *read-only* compatible catalog search | PLANNED |
| ACCEPT-Q212-01 | D | Free native engine distinguished from third-party app license, resource cost and optional offers | PLANNED |
| ACCEPT-Q213-01 | D | Hub outage permits trusted offline free native catalog, without unsigned stale takeover | PLANNED |
| ACCEPT-Q214-01 | D | Reseller account confined by server/tenant/plan/category/engine policy; phase gates respected | PLANNED |
| ACCEPT-Q215-01 | D | Paid placements labeled and separated from security/compatibility-first organic results | PLANNED |
| ACCEPT-Q216-01 | D | Billing adapters validate independent provider events without granting Core Linux rights | PLANNED |
| ACCEPT-Q217-01 | D | Signed webhook verifies issuer, anti-replay, per-destination filters and safe destinations | PLANNED |
| ACCEPT-Q218-01 | D | Public API rejects untyped/unauthorized calls with rate limits and audited scopes | PLANNED |
| ACCEPT-Q219-01 | D | Local per-engine metrics/alerts work without forced Hub telemetry; diagnostics require consent | PLANNED |
| ACCEPT-Q220-01 | D | Versioned inherited rule simulation and rollback cannot disable immutable safety invariants | PLANNED |

## Release gate

Every eventual PASS requires actual implementation commit, approved OS/VM, tenant/permission context, versioned manifests, positive and denied-path evidence, real backup/recovery outcome when relevant, redacted logs and specialist review. A SKIP/BLOCKED does not count as PASS. No implementation or testing of any of these 50 cases is asserted by writing this matrix.

The initial R1/R2/R3/R4 Core gates, R5 neutral ABI and later private Hub R6 remain unchanged. No product decision silently selects vendors, prices, defaults or numeric thresholds.
