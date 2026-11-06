<!-- forgepanel-doc id=FP-00-RECON-Q171-220 revision=2 status=specified -->
# Q171–Q220 — consistency review, authority and implementation handoffs

[Français](../../fr/00-project-control/reconciliation-q171-q220.md) · [Approved decisions](decisions-q171-q220.md) · [Planned tests](../13-tests-quality/mvp-gates-q171-q220.md)

**Status: REVIEW / CONDITIONAL CONSISTENCY, not production approval.** All 50 decisions were **explicitly owner-approved on 6 November 2026**. Earlier Q1–Q170 remain valid. The adoption of a broad administrable platform does not waive specialized security, architecture, database, API/IPC or VM gates. This report is a **technical cross-check**, not independent external sign-off.

## Reconciled or conditional findings

| Reference | Result | Existing baseline preserved / required action |
|---|---|---|
| Q171 / Q176 vs Q3, Q54, Q119, Q120 | **Consistent, phased** | Large One-Click catalog is a long-term extensible goal. Deliver proven PHP site/HTTPS in R4 first; then native recipes and later certified containers. Do not imply 20 shipped apps or first-release deadline. |
| Q172 / Q216 / Q218 vs Q47, Q66, typed IPC | **Consistent if typed** | Provisioning, billing adapters and public API share versioned primitives; no duplicate uncontrolled API, arbitrary shell/root operation or client-selected authorization. Rate-limit, idempotency, scoped audit and recovery. |
| Q173 / Q205 and Q174 / Q206 | **Complementary** | Multi-scanner malware service and WAF are different controls. Q174 **C** is a proposed Coraza + OWASP CRS driver, detection-first; block mode, false-positive handling and OS/WebStack compatibility require qualification, no implied production deployment. |
| Q175 vs ADR-008 and later portal correction; Q5/Q55 | **Targeted ADR-008 amendment drafted, requires review/merge** | Historical ADR-008 now preserves the original prototype wording but records the owner's later system-portal correction. The owner later clarified system portal access should autodetect machine IP/verified existing FQDN, without a *custom system-portal hostname*. Keep **FORGE `/forge` :8447** and **PANEL `/panel` :8446**, separate sessions; organization one-brand white label and tenant website domains remain separate, unchanged. No auto-created `forge.`/`panel.` subdomains. Security review of cookies across ports still needed. |
| Q177 / Q178 / Q202 vs Q8/Q53/Q114 | **Consistent with review** | A locally imported signed recipe is not automatically trusted. Publisher identity, per-release manual approval, license, digest and withdrawal apply; never use arbitrary catalog hooks. |
| Q180 / Q220 / Q190 / Q214 vs Q55/Q66 and tenancy | **Consistent with hard ceilings** | Inheritance and delegated reseller controls are bounded by effective server/tenant security, true physical quotas and one brand per organization. Resellers remain on later roadmap, not silently enabled. |
| Q181 / Q182 vs Q83/Q86/Q91/Q101 | **Consistent if app-compatible** | SQL engine selection, PHP/extensions, pinned versions and EOL rules must respect certified app/runtime combinations. No new default PHP/DB versions selected. |
| Q183 / Q184 / Q185 vs Q47/Q65/Q75/Q90/Q156/Q166 | **Consistent; verify recovery** | Site/app update policy, consistent files+SQL backup and retention do not claim SQL rollback or successful restoration without real drills; no automatic update default selected. |
| Q188 / Q189 vs Q94/Q104 | **Consistent with privacy** | Mask staging data, isolate credentials and prevent live email/webhooks; sensitive copies need qualified approval. Tenant secrets never enter Hub. |
| Q191–Q199 vs Q4/Q51/Q102/Q132 | **Consistent if certified** | Rootless is a preference, not an untested universal guarantee. Docker/Podman drivers, Compose provider, volumes, networks, cgroups, exceptions and image provenance need independent OS/security/VM checks. Never treat a Docker Compose file as an approved Podman execution plan. |
| Q194 **C** vs unselected D | **Explicit non-adoption** | Controlled qualified manifests/providers only; no approval of a generic raw Compose executor or an advanced graphical stack-editor feature. |
| Q200 **C** vs unselected D | **Explicit non-adoption** | Assisted, reviewed export/import with backup is approved product direction; bulk automatic native↔container conversion is **not** approved. |
| Q201–Q204 / Q210 vs Q61/Q71/Q113/Q114 | **Consistent with local authority** | Signed catalog, protected keys, versioned alerts, staged withdrawal and SSRF-safe artifact transport; Hub never decides Core Linux effects and cannot erase hosted data on withdrawal. |
| Q207 / Q219 vs Q6/Q158/Q168 | **Consistent only with consent** | Local metrics/logs are administrable; Hub telemetry, support diagnostics or cross-organization aggregates remain separately consented, minimized and anti-reidentification protected. |
| Q208 vs Q66/Q76/Q163 | **Consistent** | Scoped reauthentication/extra approval and audited emergency recovery; administrator **MFA stays optional**. Performance-only waivers never override security/recovery veto. |
| Q211–Q215 vs Q2/Q50 | **Consistent if free Core unaffected** | Two catalogs, common read-only search and clearly disclosed third-party prices. Any sponsorship remains separate and clearly labeled, cannot override safety/compatibility or gate native One-Click. |
| Q217 / Q218 vs permission model | **Consistent only when scoped** | Signed events with anti-replay and destination validation; public API grows incrementally by predefined operations, no generic privileged command. |
| Q220 Config Center | **Approved goal; architecture open** | Audited hierarchical/versioned rule administration, preview and recovery. The UI cannot change immutable safety controls. No approved implementation schema, rule language or rollout. |

## Authority allocation

- **CORE / Product + Modules:** Q171–Q220 are canonical as product directions; execution and tenant operations remain Core-local.
- **Security + Audit:** WAF/scanner false positives, SFTP/SSH boundaries, container privileges, SSRF, signed artifacts, telemetry, anti-TOCTOU and cross-tenant scenarios. No implicit exception to Q132 veto.
- **API/IPC + Database:** Provisioning/billing interfaces, typed Go agent operations, separate native/container manifests, idempotency, resource reservation, migrations and distributed recovery.
- **Design + QA + DevOps:** Two App Center navigation spaces, compatibility previews, 50 decision-linked future QA cases, runtime/VM qualification and installer sequencing.
- **Hub (detached publisher):** Approved versioned catalog metadata, partner review, license/pricing disclosures, optional promotions, limited event/diagnostic distribution and billing-side adapters. **Hub does not own Core installation, site data, private keys, Docker socket, Linux root or mandatory native app entitlement.**

## Still open — not silently selected

Exact app/recipe list and release order; scanner engines or maintenance feeds; WAF release/version and detection-to-blocking criteria; Docker/Podman rootless exceptions and Compose provider; quotas, retention and update intervals; supported billing/identity vendors and payload schemas; actual pricing, licenses and sponsor contracts; catalog signing roots, cache freshness, SSRF restrictions, trusted proxies, backup/restore coverage, API scopes, test environments and qualified operating systems. A configurable parameter **must** still have a safe constraint, a known default only after adoption, an authorized editor and versioned audit.

## Evidence and next gates

This update records choices, cross-domain scope and **PLANNED** acceptance tests. Passing a static FR/EN registry check would verify only document consistency, **not** implementation, WAF, malware protection, API, container security or actual server behavior. Work remains gated by authentic Foundation source import R1, actual Symfony/PostgreSQL R2, secure installer R3 and verified R4 PHP/HTTPS site; the neutral extension ABI R5 precedes Hub R6. The parallel App Center PRs must be reviewed and reconciled before merge. No historical decision or protected branch is silently overwritten.
