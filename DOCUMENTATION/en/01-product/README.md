<!-- forgepanel-doc id=FP-01 revision=6 status=documented -->
# Product scope and journeys

[Français](../../fr/01-product/README.md) · [Index](../README.md)

## Users and boundaries

ForgePanel targets server owners, hosting operators, agencies, resellers and hosting customers. These personas are product targets; only initial administrator enrollment is prototyped in SRC-03. The product owner communicates in natural language and is not responsible for technical implementation or review.

## Required journeys

| ID | Journey | Acceptance criterion |
|---|---|---|
| REQ-001 | Install from one command | On a supported clean VM, verify origin/signatures, preflight, install isolated panel services, report verified HTTPS access; interruption and rerun must not corrupt state |
| REQ-002 | Claim the installation | Local privileged proof issues a short-lived one-use token; create an independent panel account, offer optional MFA (now or later) and close initial registration |
| REQ-003 | Configure through a resumable wizard | Explain service dependencies and system changes; save progress; validate the plan before applying it; no ambiguous success after partial failure |
| REQ-004 | Host a site without marketplace plugins | Native account, domain, PHP runtime, TLS, database/files and backup capabilities work under explicit resource permissions |
| REQ-005 | Diagnose and recover locally | Read-only diagnosis works without the web UI; repairs are previewed, bounded, audited and preserve unrelated data |
| REQ-006 | Offer multiple OS/web profiles | Publish support only for individually tested combinations; unavailable profiles are not selectable as working capabilities |

The archive reaches a reviewed configuration draft, not installation completion. DNS, certificates, mail, file management, reseller operations and service provisioning remain outside its implementation.

## Q61–Q70 infrastructure decisions

The target experience combines verified universal installation, configurable web/DNS/mail adapters, replicated backup and restore, eventually multi-server administration, monitoring and a visual editor. **Shared hosting + VPS administration remain first priorities** (Q54), without claiming full HA is shipped first. Optional MFA and one brand per organization remain unchanged. See [Q61–Q70](../00-project-control/infrastructure-decisions.md).

## Q81–Q90 hosting journeys

The target site can have a **per-site recommended WebStack and later controlled switching**, per-site PHP-FPM/extensions/limits, ACME/wildcard TLS, Git Deploy/staging, MariaDB/MySQL/PostgreSQL with optional Redis/Valkey, file manager/SFTP/restricted SSH, webmail/quarantine, hosting plans/alerts and selective restore/staging clones. Temporary test routes or progressive WebStack cutover apply **only when supported**; zero downtime is not guaranteed. [Q81–Q90 contract](../00-project-control/decisions-q81-q90.md). Not implemented.

## First PHP/HTTPS website and private beta — Q121–Q127

The first functional experience targets **one PHP site with an externally managed DNS domain and ACME HTTP-01 HTTPS**, without requiring native DNS. First OS and WebStack are **chosen after comparative VM testing**, never assumed defaults. Include local admin and website-manager roles, VPS diagnostics with **controlled OS updates**, backed-up panel/site files and **tested restores**. Private beta follows only after isolated internal tests and verified distribution/security reporting prerequisites. None of these journeys is **implemented**. [MVP](../00-project-control/mvp-qualification.md).

## Q141–Q147 MVP qualification and safeguards

The first PHP/HTTPS site will require **local/cloud VMs with common CI reports**, app-class performance/security tests and cross-release regression checks (Q141/Q142). With **external DNS**, the advisor suggests records and rechecks A/AAAA/80/HTTP-01/HTTPS without automatic provider edits (Q143). Planned **per-server** OS updates (Q144), **encrypted local** backup with recoverable keys and optional remote destination plus optional external KMS/multiple recovery custodians (Q145), shell-disabled SFTP with expiry/quota/audit (Q146). After internal tests, private beta may pause waves on configurable health gates and recover (Q147). Hub commerce Q148–Q150 follows neutral ABI. [Q141–Q150](../00-project-control/decisions-q141-q150.md). **Not shipped.**

## Q151–Q158 practical MVP requirements

**Local QEMU/KVM** is the first qualification driver, with full VM CI only where available and later cloud drivers (Q151). Evidence is **signed, historical and internal** with snapshots (Q152); performance budgets/regressions are configurable and waivers cannot bypass **security vetoes** (Q153). Initial site DNS/HTTP-01 checks **only actually published A/AAAA families** (Q154), OS reboots require **per-server** approval, backup/health/recovery (Q155). Encrypted local backups earn recoverable status only after protected key accessibility checks and **real isolated restoration** (Q156). Site managers administer own-site **SFTP public keys** under expiry/quota/audit (Q157). Private beta uses local health and **separately opted-in minimal diagnostics** with cohort thresholds (Q158). [Decisions](../00-project-control/decisions-q151-q160.md).

## Scope discipline

Core foundations are mandatory; native service modules may be selected without depending on third-party plugins. Plugins extend capabilities rather than provide basic authorization or safety. Recipes install customer applications; they are neither core modules nor privileged extensions.

The owner has now confirmed a **complete free Core plus optional premium components/services and paid support (Q2)**, a dual-license model requiring exact texts (Q1), official/verified-partner catalog (Q8) and 60 days offline grace for relevant premium rights (Q7). Pricing, trials, entitlement mechanisms and older WCP360 rules are not presumed. See [product policy](../00-project-control/product-policy.md). Success is verified operation and recovery, not a large number of dashboard screens.

[Module catalog](../04-modules/README.md) · [Priorities](../00-project-control/status.md)
