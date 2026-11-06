<!-- forgepanel-doc id=FP-00-Q171-220 revision=1 status=specified -->
# Q171–Q220 — approved product arbitration register

[Français](../../fr/00-project-control/decisions-q171-q220.md) · [Q161–Q170](decisions-q161-q170.md) · [App Center](../06-apps-recipes/app-center-engines.md) · [Reconciliation](reconciliation-q171-q220.md)

**OWNER-APPROVED 6 November 2026: all 50 recommendations explicitly adopted.** Q1–Q170 are retained; no unanswered question becomes an approval. Exactly **47 D and 3 C (Q174, Q194, Q200)**. These are product directions **SPECIFIED**, not implemented, merged, runtime-tested, released or deployed. The [machine registry](../../../evidence/decisions-q171-q220-v1.json) mirrors every choice; real prices, technical providers, default limits and rollout dates remain OPEN.

| ID | Choice | Approved product direction | Domain |
|---|---|---|---|
| Q171 | **D** | Extensible categorized native catalog, staged rollout of qualified recipes | Core + Hub metadata/publisher scope |
| Q172 | **D** | Versioned provisioning API with predefined operations, RBAC, audit and independent connectors | Core + Hub metadata/publisher scope |
| Q173 | **D** | Multiscanner malware architecture with bounded jobs, reversible quarantine, policies and audit | Core local |
| Q174 | **C** | Candidate Coraza + OWASP CRS WAF driver, detection first and blocking only after qualification | Core local |
| Q175 | **D** | Strictly separated FORGE/PANEL sessions, routes, APIs, themes, menus and permissions; isolated Hub | Core local |
| Q176 | **D** | After R4 hosting foundation, native One-Click first, containers in independently qualified milestones | Core local |
| Q177 | **D** | Administrable application categories with verified compatibility and eligibility | Core + Hub metadata/publisher scope |
| Q178 | **D** | Official recipes, approved partners and signed local imports subject to prior review | Core + Hub metadata/publisher scope |
| Q179 | **D** | Simple/advanced modes, preflight, estimates, backup, preview and administrable templates | Core local |
| Q180 | **D** | Constrained versioned configuration inheritance global → server → organization → plan → site | Core + Hub metadata/publisher scope |
| Q181 | **D** | App-compatible SQL engine recommendation, controlled choice, privileges and quotas | Core local |
| Q182 | **D** | Certified app versions, pinning, EOL, policy and migrations per app/site | Core + Hub metadata/publisher scope |
| Q183 | **D** | Configurable app/site updates with maintenance windows, staging, backup and approvals | Core + Hub metadata/publisher scope |
| Q184 | **D** | Consistent files/SQL backup, restore checks and disclosure of irreversible migrations | Core local |
| Q185 | **D** | Uninstall with per-tenant/site retention choices, confirmation and audit | Core local |
| Q186 | **D** | Detect and adopt existing apps read-only first, then reviewed explicit authorization | Core local |
| Q187 | **D** | Bulk installs governed by concurrency, quotas, cancellation and recovery | Core local |
| Q188 | **D** | Isolated staging, masked data, separate secrets and live mail/webhooks disabled by default | Core local |
| Q189 | **D** | Driver-based application secrets with site scopes, rotation, bounded access and audit | Core local |
| Q190 | **D** | Delegable RBAC by operation, site, organization and plan, bounded by server policy | Core local |
| Q191 | **D** | Container activation only on qualified hosts and scoped plan/organization rights | Core local |
| Q192 | **D** | Independent Docker/Podman drivers, selected by certified app/host compatibility | Core + Hub metadata/publisher scope |
| Q193 | **D** | Rootless preferred, approved exceptions, class-based isolation profiles and audit | Core local |
| Q194 | **C** | Compose only through specifically qualified recipes/providers, no arbitrary files | Core + Hub metadata/publisher scope |
| Q195 | **D** | Digest/signature-pinned images, allowed registries, withdrawal and version compatibility | Core + Hub metadata/publisher scope |
| Q196 | **D** | Least capabilities; deny privileged, engine sockets and sensitive mounts by default | Core local |
| Q197 | **D** | Segmented container networks, governed ingress/egress, ports and exposure | Core local |
| Q198 | **D** | Quota-bounded persistent volumes, backup, retention, encryption and actual restore | Core local |
| Q199 | **D** | CPU/RAM/PIDs/I/O/storage budget by host, plan, tenant and app, physically bounded | Core local |
| Q200 | **C** | Native↔container migration through explicit export/import wizard, backup and validation | Core + Hub metadata/publisher scope |
| Q201 | **D** | Signed catalogs, cache, key rotation, anti-rollback, provenance and withdrawal | Core + Hub metadata/publisher scope |
| Q202 | **D** | Verified publishers and releases: security, maintenance, licensing and withdrawal | Core + Hub metadata/publisher scope |
| Q203 | **D** | Track installed-version vulnerabilities with risk policies and approved remediation | Core + Hub metadata/publisher scope |
| Q204 | **D** | Risk-based unsafe-recipe response: block new installs, notify, preserve existing data | Core + Hub metadata/publisher scope |
| Q205 | **D** | Reversible malware quarantine, false-positive review and site-scoped risk/approval policy | Core local |
| Q206 | **D** | Inherited WAF policies, simulation, detection-first, qualified blocking and rollback | Core local |
| Q207 | **D** | Structured redacted logs, correlation, RBAC, filters, retention and authorized export | Core + Hub metadata/publisher scope |
| Q208 | **D** | Risk/operation/resource-based step-up, approvals and separation of duties | Core + Hub metadata/publisher scope |
| Q209 | **D** | Preflight, atomic reservations, apply-time revalidation, idempotency and recovery | Core local |
| Q210 | **D** | Approved artifact sources, signed cache, SSRF protections and verified resume | Core + Hub metadata/publisher scope |
| Q211 | **D** | Two distinct App Center sections with common read-only search and compatibility filters | Core + Hub metadata/publisher scope |
| Q212 | **D** | Distinguish free native engine, third-party licenses/costs, resources and optional offers | Core + Hub metadata/publisher scope |
| Q213 | **D** | Safe versioned offline local catalog, optional signed synchronization, Hub not required | Core + Hub metadata/publisher scope |
| Q214 | **D** | Reseller rights by tenant/plan/category/engine bounded by server policy | Core local |
| Q215 | **D** | Compatibility/security-first ranking with filters/stats; distinct labeled sponsorship if enabled | Core + Hub metadata/publisher scope |
| Q216 | **D** | Billing integrations via stable API and qualified independent connectors | Core + Hub metadata/publisher scope |
| Q217 | **D** | Versioned signed events/webhooks, idempotency, filtering and approved destinations | Core + Hub metadata/publisher scope |
| Q218 | **D** | Progressive public API of predefined operations, scopes, RBAC, rate limits and audit | Core local |
| Q219 | **D** | Per-engine observability: logs, metrics, health, events, quotas, alerts and diagnostics | Core + Hub metadata/publisher scope |
| Q220 | **D** | Versioned Configuration Center with inheritance, rules, simulation, RBAC, history and recovery | Core + Hub metadata/publisher scope |


## Interpretation and protected boundaries

- **Q171/Q176 vs R1–R4 and Q119/Q120**: a broad categorized native catalog is a **progressive target**, not a requirement to ship 20 working apps on day one. The first qualified PHP/HTTPS site and real Symfony/PostgreSQL remain prerequisites. Containers follow independent qualified drivers (Q51).
- **Q172/Q216/Q218**: one coherent versioned family of **typed and scoped** provisioning/billing/public APIs with independent adapters, never three conflicting platforms or a generic shell/root execution endpoint. Plan/site/tenant limits and idempotency remain mandatory.
- **Q173/Q205 and Q174/Q206**: malware scanning and WAF policies complement, rather than replace, one another. **Q174 C** selects Coraza+OWASP CRS as a **candidate WAF integration with detection-first rollout**, not an unreviewed universally enabled blocking engine. Scanner engines, quarantine thresholds and compatibility remain open.
- **Q175/Q5/Q55/ADR-008**: FORGE `/forge:8447` and PANEL `/panel:8446` retain separate sessions and themes. The owner's more recent **automatic machine IP/existing verified FQDN discovery** applies to **system portal access**, with **no custom system portal hostname** in the installer; one-brand-per-organization white-label and **tenant website domains** remain separate capabilities. Legacy text about independently configurable system portal hosts requires targeted migration/reconciliation, not silent overriding.
- **Q178/Q202 vs Q8/Q53/Q114**: signed local imports and partner packages **still require explicit manual review per release**, provenance/license approval and resource permission. No unreviewed self-publishing. Third-party code and trademarks are not automatically relicensed.
- **Q180/Q220/Q190/Q214**: administrative inheritance and reseller delegation never bypass tenant/server permissions, immutable security invariants, physical caps or the phased audience roadmap. Resellers are not thereby declared implemented or immediately enabled.
- **Q183/Q184/Q185/Q200**: automation, database migrations and native↔container transfers require plan/backup/verification, approved recovery and retention. **Q200 C is a controlled assisted export/import, not option D automated cross-engine conversion.** No blanket rollback guarantee.
- **Q193/Q194/Q195/Q196/Q197**: rootless and isolation are preferred subject to OS/driver certification. **Q194 C allows only specifically qualified Compose recipes/providers and does not approve an advanced visual stack editor**. Untrusted host mounts, sockets, unknown YAML and privileged execution are denied by default.
- **Q201/Q203/Q204/Q210**: signed catalogs and risk responses do not justify destructive remote actions, unsafe downloads or the Hub taking Linux authority. Core must work without Hub and preserve hosted data.
- **Q207/Q219 vs Q6/Q158/Q168**: structured local logs and monitoring do not authorize compulsory telemetry to the Hub; external diagnostics require consent, minimization, cohort protections and retention controls.
- **Q208 vs Q66/Q76/Q163**: sensitive reauthentication, approvals, noncritical performance exception workflow and audited emergency recovery remain; **MFA is still optional** and security/backup/test vetoes cannot be waived.
- **Q211/Q212/Q213/Q215**: two installation spaces remain distinct; shared read-only search and clearly labeled optional paid/sponsored listings do not gate the free native installer or corrupt compatibility-first organic rankings.

## Open technical implementation and evidence

The approved directions do **not** select concrete scanner vendors, signature keys, WAF versions, default Docker/Podman runtime, API payloads, database schema, security thresholds, pricing, app list, retention days, automatic-update defaults, network exposure or certification results. Those values must be separately approved or selected under authorized specialist technical review. [Reconciliation and handoffs](reconciliation-q171-q220.md) records the remaining validation work. **No code, runtime test, release or CI claim is implied by this register.**
