<!-- forgepanel-doc id=FP-00-Q141-150 revision=1 status=specified -->
# Q141–Q150 decisions — Technical certification, recovery and secure disclosure

[Français](../../fr/00-project-control/decisions-q141-q150.md) · [Q131–Q140](decisions-q131-q140.md) · [MVP qualification](mvp-qualification.md) · [Detailed requirements](../02-architecture/certification-backup-security.md)

## Owner-confirmed choices — 5 November 2026

**Q141 D, Q142 D, Q143 C, Q144 D, Q145 D, Q146 C, Q147 C, Q148 C, Q149 C, Q150 D** are selected and **extend Q1–Q140**. They do not replace the free Core, optional Hub, security policy or MVP scope. State **SPECIFIED, not IMPLEMENTED/VERIFIED**. Documentation does not create working VMs, backups, betas, cryptographic proofs or security advisories.

| ID | Confirmed choice | Implementation and security boundary |
|---|---|---|
| Q141 D | **Local/cloud VM drivers, compatible CI runners and common reports** | Provider-neutral interface for authorized QEMU/KVM or cloud **full system VMs**, snapshots/fault injection, OS/version/architecture/WebStack/commit and PASS/FAIL/SKIP plus recovery evidence. Container tests never qualify an OS. |
| Q142 D | **Performance budgets by application type and cross-version regression detection** | Benchmarks for PHP app classes, throughput, percentile latency, errors, CPU/RAM and recovery with fixed environments. Configurable limits and baseline comparisons. **Q132 security/recovery disqualifiers override speed**. No numerical threshold chosen. |
| Q143 C | **Suggest DNS records and recheck A/AAAA, ports and TLS certificate** | Diagnostic wizard for **external** DNS, port 80 and ACME HTTP-01, port 443 and valid HTTPS. Show expected values/instructions then recheck after authorized action. **Automatic DNS provider mutation is not selected** by Q143 C. |
| Q144 D | **OS update policy per server**, with **later** progressive multi-server orchestration | Per-server allowed sources/packages, maintenance, impact, backup, authorization, reboot, health/recovery, audit and policy revision. Multi-server coordination follows Q67/Q77 once tested; not a single-host MVP prerequisite. |
| Q145 D | **Secret vault + protected recovery copy, optional external KMS and multiple recovery authorities** | Encrypted local backup key custody Q135: separate data/keys, rotation, access and off-host recovery, optional multi-custodian approvals. **External KMS is not mandatory**, free Core must remain recoverable without Hub. Local encryption plus key on same failed disk is insufficient disaster recovery. |
| Q146 C | **Scoped SFTP with no shell, expiry/revocation, quotas and audit** | Q136 site manager uses authorized key/identity and canonical root/paths, no symlink/traversal to other tenants, quota and redacted access logging. Revocation/expiry does not delete hosted files. No web terminal or root access. |
| Q147 C | **Beta pause on critical incidents, configurable health thresholds and recovery** | Q137 private beta waves with per-version/cohort failure gates, suspend new installs/updates, notices and recovery plan. Tester telemetry remains consented or narrowly contractual under Q6; no mandatory collection. |
| Q148 C | **Local key pair, signed challenge, rotation/anti-replay, organization verification and manual lost-server recovery** | Q128/Q138 premium transfer identity in Hub: fresh challenge/nonce, organization/target binding and key rotation/revocation, controlled lost-host verification. **Risk-based additional approval under Q138 D remains**. A private key alone does not prove a full server was not cloned. |
| Q149 C | **Partner severity- and contract-based response terms, escalation, alerts and withdrawal** | Keep Q114/Q129/Q139 manual review per release and maintenance/security obligations, tracked severity, negotiated deadlines, reminders, escalation, withdrawal and customer notices. **No invented response time or SLA.** |
| Q150 D | **Signed, historical advisories, configurable notifications, coordinated partner disclosure and risk-based timeline** | Q130 lead/deputy and Q140 triage, authenticated/versioned advisories, affected versions, fixes and coordinated publication. No universal disclosure date and no automatic publication of unpatched exploit details. No forced telemetry or Core shutdown. |

## Initial MVP and Q120 sequence

**Q119 B/R4** remains verified installer/CLI/wizard/permanent PostgreSQL identity and one PHP site with **external DNS + ACME HTTP-01** and HTTPS, scoped website manager, controlled VPS updates, encrypted local backup and actual restore. Q141/Q142 strengthen VM/performance evidence before selecting first OS/WebStack (Q121/Q122), Q143 improves diagnostics without automatically writing DNS records, Q144 scopes OS updates to each host, Q145 requires usable backup key recovery, and Q146 adds real SFTP denials/audit. **Cloud KMS or multi-server update orchestration is not mandatory at R4.**

**After MVP**, Q147 refines internal→wave-based authorized private beta, pause/recovery and minimized consented telemetry. **After neutral R5 ABI**, Hub R6 may add Q148–Q150 cryptographic transfer proof, partner compliance and signed/coordinated advisories. Free Core operations must never require Hub connectivity.

## Tests and negative gates

- Full local/cloud VMs, restored snapshots and install/network/disk failures; identical reporting schema for different drivers, explicit skips.
- Benchmarks with fixed app/OS/resources/version, meaningful regressions and security disqualifiers.
- Wrong A/AAAA/IPv6, blocked 80, misrouted challenge, TLS validation and recheck after **manual** DNS correction.
- Interrupted OS upgrades/reboot, stale server policy, unusable backups; no accidental changes on other servers.
- Lost host/vault, missing recovery key, failed multiple-custodian approval, external KMS outage, offline Core recovery.
- Expired/revoked SFTP key, symlink/traversal, disk quota and cross-organization denial, redacted logs.
- Critical beta health triggers halt of a wave, proven recovery, no deletion of customer data or already granted software rights.
- Hub replayed nonce, stolen key, wrong org, concurrent transfers/lost host, late partner remediation, invalid signatures and unauthorized disclosures.

[Certification/recovery contracts](../02-architecture/certification-backup-security.md) · [Roadmap](implementation-roadmap.md).

## Still open

CI/cloud vendor/cost, workload profiles and numeric budgets, actual expected DNS values, default maintenance schedule, vault/KMS and recovery-custodian mechanism, SFTP lifetimes, beta pause thresholds, proof wire format, partner negotiated timelines and exact disclosure policy. **No vendor, days, custodian count or performance number is inferred.**
