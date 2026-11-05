<!-- forgepanel-doc id=FP-00-MVP-QUAL revision=3 status=specified -->
# First PHP/HTTPS ForgePanel qualification — Q121–Q127

[Français](../../fr/00-project-control/mvp-qualification.md) · [Roadmap](implementation-roadmap.md) · [Q121–Q130 decisions](decisions-q121-q130.md)

## Pilot profile: evidence-based, not preset

Choose the **first OS (Q121 D)** and **first WebStack (Q122 D)** only after comparing disposable VMs. Record OS versions, packages, installability, PHP-FPM, services, firewall, SELinux/AppArmor, permissions, TLS, `.htaccess`, listeners, recovery and negative results. Selecting one pilot profile does not cancel the other OS/WebStack targets from Q1–Q120.

| Test area | Minimum evidence before qualification |
|---|---|
| OS/WebStack comparison | Clean VM, named OS/toolchain/build commit, install plan, compatibility, HTTP/TLS/PHP checks, restore/diagnostics, negative scenarios; **choose after** comparing results |
| External DNS and HTTP-01 | Test domain with **externally managed** DNS; verify A/AAAA/CNAME and authority; reachable port 80 for HTTP-01, site routing and HTTPS 443; test failure, wrong DNS/IPv6, renewal |
| Installer (R3) | Verified bootstrap, trusted provenance, scoped system permissions, preflight, idempotent stages and recovery |
| Identity and roles (R2/R4) | Root Linux password never collected in web setup, permanent local administrator and **recovery**, offered or skipped admin MFA; scoped website-manager role and CSRF/session/tenant denial |
| Essential VPS (R4) | System/service state, resource usage and redacted logs; **controlled OS package upgrades** via diff/plan, trusted repository, permission, preflight, reboot warning, audit and recovery |
| PHP website (R4) | Create/manage site, isolated identity, document root, compatible PHP, listener/domain/TLS, successful HTTPS request and access-denial tests |
| First backup (R4) | **Panel configuration** and **PHP website files** included in checksummed manifest; actual restore after simulated loss/alteration; consistently recover panel PostgreSQL state when necessary to restore identity/site functionality |
| Failure and recovery | Listener conflict, unavailable challenge, bad certificate, missing package, interrupted upgrade, corrupted config, incomplete archive and unauthorized actor |

**First-release bounds:** Q126 B does not require backups of hosted SQL databases, mail, remote replication or immutability, though Q65/Q75/Q90 remain longer-term targets. **Native authoritative DNS, DNS-01 and wildcard are not first-site prerequisites**, but remain later capabilities. No tests are assumed complete.

## VM qualification and recovery — Q131 D, Q132 D

The **certification matrix** uses **local VMs and automated CI** when runners can launch **full system VMs**; preserve a clean **baseline snapshot**, inject failures (network, disk, installer and services), verify a recovery snapshot/path and produce an **OS/version/WebStack/commit** report with steps, redacted logs, `PASS`/`FAIL`/`SKIP` and limits. Go fixtures and containers are not substitutes for systemd, firewall, SELinux/AppArmor and OS package-manager tests (Q131).

For the **first WebStack Q132**, compare application/PHP/`.htaccess` compatibility, listener/TLS/tenant security, **measured load**, maintenance/reload behavior and **outage recovery**. Hard **rejection gates** override attractive benchmark numbers: exposed protected content, cross-tenant access, IP:port collisions, unrecoverable failure and loss of admin access. No invented load/latency threshold. Q121/Q122 remain: **no OS/stack selection before evidence**.

## External DNS/HTTP-01 and HTTPS diagnostic — Q133 C

Verify domain **A and AAAA** resolution, conflicting IPv4/IPv6 targets, publicly reachable **port 80**, correct ACME **HTTP-01** challenge routing and vhost ownership, then **HTTPS on 443**, cert chain, hostname, expiry and renewability. Present actionable diagnostics without revealing ACME secrets. DNS authority stays **external** for MVP; native authoritative DNS/DNS-01 are not R4 prerequisites.

## Updates, backups and website-manager rights — Q134–Q136

- **Q134 C**: planned OS updates with package/impact preview, role approval, maintenance window, **recoverable backup**, durable job/reboot warning, health checks and **recovery procedure**; never expose arbitrary root commands.
- **Q135 B**: **encrypted local backups** with **optional remote destination** only if a driver is qualified, covering panel config and **PHP website files**, real restore drills and accessible recovery keys. Recover panel PostgreSQL consistently if needed. Local copies do not survive every whole-disk failure; remote/3-2-1 targets remain planned.
- **Q136 C**: **website-manager** limited to owned websites: status, PHP/domains/TLS/files, **SFTP and backup/restore** under admin policies/quotas. Test **real SFTP allowed on the owned site and denied across tenants**, plus quota increases, OS packages and root actions; apply Q47 to TLS/restores.

## Q127 B private beta gate

Sequence: isolated internal VM tests and denial cases → result/risk review → fix blockers → verify distribution rights/license obligations for **external recipients**, security documentation and working private contact → obtain owner's approval for tester access/scope → run a **private beta** with recovery, issue-reporting, withdrawal and shutdown instructions.

Private beta is not stable/public release and does not automatically exempt software distributed to others from license obligations. Do not collect user Linux root credentials or third-party data without specific authorization and safeguards.

## Responsibility

A security owner and **deputy** (Q130 C), their access, triage workflow, escalation, audit and coordinated notices must be **actually appointed and verified** before sharing. Both Q118 routes (GitHub private reporting + dedicated security email) must be configured/tested; never invent names, mailbox, response SLA or operational team.

**Status: test plan only. No first OS/WebStack, ACME vendor or beta team has been qualified.**
