<!-- forgepanel-doc id=FP-00-Q121-130 revision=1 status=specified -->
# Q121–Q130 decisions — Initial qualification, private beta and governance

[Français](../../fr/00-project-control/decisions-q121-q130.md) · [Q111–Q120 decisions](decisions-q111-q120.md) · [MVP test plan](mvp-qualification.md)

## Owner decisions (5 November 2026)

**Q121 D, Q122 D, Q123 A, Q124 B, Q125 B, Q126 B, Q127 B, Q128 D, Q129 C, Q130 C** extend Q1–Q120 without superseding the larger product vision. State **SPECIFIED**, not implemented, verified or published.

| ID | Confirmed choice | Scope and constraints |
|---|---|---|
| Q121 D | Select first OS **after comparison of VM tests and prerequisites** | Compare six target OSes for installability, dependencies, isolation, update handling, diagnostics and recovery. **No first OS chosen**. Qualify each OS separately. |
| Q122 D | Select first WebStack **after compatibility/security tests** | Compare available profiles, TLS, PHP-FPM, `.htaccess`, listener ownership, isolation and recovery. **No initial stack imposed**; Q79 per-site advice remains. |
| Q123 A | **Preconfigured external DNS + ACME HTTP-01 + automatic HTTPS** in MVP | Explain required records; verify public DNS resolution, domain control, HTTP challenge reachability on port 80 and valid HTTPS. **Native authoritative DNS and DNS-01 driver are not MVP gates**, but remain planned. |
| Q124 B | **Secure local admin/recovery plus website-manager role** | Permanent login, sessions, CSRF, admin versus site-manager permissions, deny other sites; administrator MFA remains **optional**. SSO/OIDC not mandatory for v1. |
| Q125 B | **System state, resources, services/logs plus controlled OS package updates** | Read-only diagnostics and permissioned, planned, verified/audited package operations with reboot and recovery implications. **No unrestricted root terminal**. |
| Q126 B | **Panel/config backup plus PHP-site file backup and real restore tests** | Preserve data, manifests, access/secrets, integrity and restore on isolated environment. Hosted SQL, remote immutable 3-2-1 and mail backup are later goals; any panel PostgreSQL state required to recover functionality needs a consistent recovery method. |
| Q127 B | **Internal isolated tests, then private beta for authorized testers** | Beta only after real MVP evidence, permissions, live security contact, recovery procedures and review of distribution conditions. **Private distribution to third parties may still carry license obligations**. No assumed public beta. |
| Q128 D | **Controlled self-service license transfers plus manual lost-server recovery** | Verify ownership/organization, grants, caps, audit, anti-replay/double assignment; controlled recovery without Linux root password. Hub feature **after extension API**. |
| Q129 C | **Partner maintenance/security duties with contractual timeframes, alerts and withdrawal** | Human review of every release (Q114), vulnerability contact and remediation/withdrawal; **no invented contract timing**. Deferred Hub. |
| Q130 C | **Named security owner plus deputy, triage and coordinated notices** | Permissioned roles, escalation, tracking, confidentiality and actually verified private GitHub/email channels (Q118). **No person, email or SLA assigned by this specification**. |

## Reconciliation

**Q119 B MVP** remains installer, CLI, wizard, identity/PG, PHP website with external domain and HTTPS, expanded by Q124–Q126. **Q120 D dependency order** remains source → Symfony/PG → installer → website/VPS → neutral ABI → Hub. **Q121/Q122 choose no first OS/stack**: qualification evidence must precede selection. Q123 does not cancel local/external DNS (Q63/Q73) or DNS-01/wildcard (Q84/Q95); it defers them beyond first website. Advanced 3-2-1/DR (Q65/Q75) remains a target while Q126 bounds the first restore.

Before external private beta, review AGPL/commercial distribution rights and required notices (Q111), contributor/third-party rights (Q112), supplied terms and **verified security reporting** (Q118/Q130). A private repository alone does not waive license/contract requirements.

Hub implements Q128–Q129 after neutral Core ABI: premium licensing and partner rules never gate free Core hosting.

## Evidence and tests to gather

Compare OS VMs and stacks before choosing a candidate; test external A/AAAA DNS, HTTP-01, real HTTPS and failed port-80/443 challenges, bad IPv6/DNS and certificate errors. Test local login/recovery, admin/site-manager denial, safe package handling without generic commands, config and site-file backup/restore on VM. Verify actual security role/deputy, both channels, access rules and private-beta recovery before inviting external testers. Later Hub tests: concurrent transfers/lost host/ownership, partner contractual alerts and withdrawal.

[MVP acceptance plan](mvp-qualification.md) · [R1–R6 roadmap](implementation-roadmap.md). **No live system or commercial certification is claimed.**
