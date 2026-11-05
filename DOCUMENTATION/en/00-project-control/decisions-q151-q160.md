<!-- forgepanel-doc id=FP-00-Q151-160 revision=1 status=specified -->
# Q151–Q160 decisions — Reproducible qualification, access and security advisories

[Français](../../fr/00-project-control/decisions-q151-q160.md) · [Q141–Q150](decisions-q141-q150.md) · [MVP qualification](mvp-qualification.md) · [Technical contracts](../02-architecture/qualification-and-security-contracts.md)

## Owner-confirmed choices — 5 November 2026

**Q151 A, Q152 C, Q153 C, Q154 C, Q155 C, Q156 C, Q157 C, Q158 C, Q159 C, Q160 C** extend **Q1–Q150** without superseding them. Status **SPECIFIED**, not IMPLEMENTED/VERIFIED/RELEASED. Complete AGPL Core remains Hub-independent, administrator MFA optional, one brand per organization.

| Ref | Explicit choice | Requirements and limits |
|---|---|---|
| Q151 A | **QEMU/KVM local first, cloud VM drivers later** | Implement/qualify local full-system QEMU/KVM driver first, retaining Q141 D multi-driver contract. Check local/runners' actual virtualization capabilities before asserting VM CI qualification; cloud is not an initial gate. |
| Q152 C | **Internal matrix plus signed reports, provenance, snapshots and results history** | Bind each test to OS/arch image, commit, toolchain, resource config, PASS/FAIL/SKIP, snapshot/failure case, verifiable digest/signature and revision history. **Public compatibility-matrix publication is not selected** under Q152 C (D was not chosen). |
| Q153 C | **Block performance regressions by criticality/budget, with approved audited exceptions** | Q142 per-app workloads and comparable environment; deny according to severity/threshold/policy. Exceptions scoped, time-bound and logged; **never waive Q132 security, tenant-isolation or recovery vetoes**. No numeric thresholds assumed. |
| Q154 C | **Check only published address families (A/AAAA) for HTTP-01 compatibility** | Only A: validate IPv4; only AAAA: IPv6; both: verify **both** published routes. Missing unadvertised AAAA is not a fault and a bad published IPv6 route cannot be ignored. Suggest records under Q143, recheck without auto-editing provider DNS. |
| Q155 C | **Per-server update/reboot policy with approval, backup, health and recovery** | Preflight, authorized approver, host-specific maintenance/reboot window, recoverable snapshot, panel/site health, audit and rescue. Future multi-server orchestration under Q144, not mandatory in MVP. |
| Q156 C | **Export protected backup recovery key, periodically verify accessibility AND restore in isolation** | Encrypted Q135 backup earns « recoverable » status only after decryption and isolated VM/environment restore with data/permissions checks, using protected off-failure-domain key custody. **External KMS/multi-custodian drills remain optional** under Q145 D, rather than mandatory Q156 D. |
| Q157 C | **Site-manager public-key self-management for SFTP, expiry, site limits, audit and sensitive-action validation** | Register/revoke **public keys** within account policy, verify grant where appropriate, canonical site roots, quotas, expiration and logs, with step-up for sensitive operations. No client private key upload, shell by default or other-tenant access. |
| Q158 C | **Manual tester reports + local health + minimized separately consented diagnostics and cohort thresholds** | Q137/Q147 beta uses local checks and manual reports, additional explicitly selected data only; distinct Q6 opt-ins for diagnostics/version/other purposes. Gate pause per wave/cohort without forced telemetry or customer files/SQL/mail collection. |
| Q159 C | **High-risk premium transfer indicators: lost source, repeated/unusual transfers, identity/org mismatch or suspected compromise** | Invoke **Q138 D configurable extra approval for risk**, Q148 C key-based proof and org identity, preserve rejection/decision audit and manual lost-host recovery. Do not silently add per-product rule engines/unrestricted waivers (Q159 D not selected). Hub after ABI. |
| Q160 C | **Signed FR/EN human-readable site/Panel notices AND structured machine-readable advisories**, configurable notifications | Include versioned ID/signature, severity, affected packages, fix, coordinated Q150 disclosure, protected exploit details. **Advanced interoperability formats are not mandatory** (D not selected), and standalone Core may not be required to connect to Hub. |

## Release implications

Q119/Q120 R3 qualification begins with **local QEMU/KVM**; Q141 cloud/CI drivers remain future options depending on runner capabilities. Signed common reports permit comparison without treating unexecuted VMs as passed. Performance exceptions never waive security disqualifiers. Initial PHP website continues with **external DNS, ACME HTTP-01 and HTTPS**; Q154 checks **actually published A/AAAA** only. R4 also requires per-server reboot controls, encrypted backups with **isolated restoration evidence**, and shell-disabled scoped SFTP with authorized public-key management.

**Private beta** follows tested R4 and Q127 distribution gates, with cohort-based health thresholds, minimized diagnostics and **separate consents**. **Hub after neutral R5 ABI** owns future Q159 premium transfer risk alongside Q128/Q138/Q148 and Q160 signed coordinated advisories alongside Q140/Q150.

## Negative tests and blockers

- No KVM, unqualified runner, failed snapshot, forged/stale report, `SKIP` shown as success: deny certification.
- App-budget performance regression; permit signed/audited limited *performance* exemption where policy allows but always reject tenant leakage or failed recovery.
- Published A without AAAA: no fake IPv6 failure. Both A/AAAA: fail if **either advertised path** reaches wrong host or breaks HTTP-01; manual DNS then recheck.
- Unsafe reboot outside policy, missing approval or backup/health failure: deny or use explicit recovery.
- Lost key/vault or incomplete isolated recovery: archive is **not declared recoverable**.
- Unauthorized public SFTP key, expired/revoked access, symlink escape, quota or skipped step-up.
- Beta without diagnostic opt-in: Core stays usable with local/manual signals; cohort can pause under health policy.
- Hub lost host, burst of transfers, wrong organization or suspected compromise: require policy-triggered second approval. Reject unsigned/misdirected advisory or disclosure of private exploit.

[Q151–Q160 technical contracts](../02-architecture/qualification-and-security-contracts.md).

## Open implementation parameters

Actual VM images/runners, report signing infrastructure, per-app numeric budgets and severity, default maintenance/reboot, backup recovery-key export method, SFTP lifetime, beta telemetry fields and consent per cohort, fraud trigger thresholds, machine-readable advisory schema, publisher endpoint and disclosure timing. **No provider, limit, protocol or domain is silently chosen.**
