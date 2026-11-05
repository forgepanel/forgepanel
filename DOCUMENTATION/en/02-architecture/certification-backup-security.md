<!-- forgepanel-doc id=FP-02-Q141-150 revision=1 status=specified -->
# VM certification, performance budgets, backup recovery, access and updates — Q141–Q147

[Français](../../fr/02-architecture/certification-backup-security.md) · [Q141–Q150 decisions](../00-project-control/decisions-q141-q150.md) · [MVP qualification](../00-project-control/mvp-qualification.md)

## VM adapters and consistent evidence (Q141 D)

Candidate `QualificationDriver`: `capabilities`, `provisionDisposableVM`, `snapshot`, `restoreSnapshot`, `injectFailure`, `collectEvidence`, `destroy`. Support interchangeable **local VMs** and **cloud VMs** without silently choosing vendors. CI runners must demonstrably run real Linux kernels, systemd, package managers, firewall and SELinux/AppArmor where applicable. Skipped or unavailable VM work reports `SKIP`, not certification.

A versioned `QualificationReport` includes VM image identity, OS/architecture/version, WebStack, Go/Symfony/PHP, commit/signatures, resource allocation, test suites and individual results, redacted logs, network/disk/reboot fault injection and **restoration proof**. Reports must state their exact tested scope. Never infer OS compatibility from fixtures or tests on a different distribution.

## Comparable performance and security veto (Q142 D)

Define **application-class** workload profiles: basic PHP and representative transaction/CMS scenarios when implemented, with appropriate WebStack workloads. Pin/load-record VM environment, versions, request mix, duration, median/p95/p99 latency, throughput, error rate, CPU/RAM, saturation and reload/failure recovery. **Configurable versioned performance budgets** enable cross-version regression analysis in comparable conditions; do not invent acceptable numbers or falsely precise scores.

Always **reject** a candidate exposing protected files, bypassing `.htaccess`, crossing tenant boundaries, colliding on shared listeners, failing TLS or lacking verified recovery, even if it benchmarks faster. Initial profile selection awaits this evidence.

## External DNS advisor (Q143 C)

UI proposes **expected DNS records** for the site's IP/IPv6/listener, observed zone problems and instructions, then offers **recheck** of A/AAAA, IPv6 routing, **port 80**, **HTTP-01** challenge, HTTPS **443** and certificate/hostname. Local authorization applies. The selected Q143 C **does not permit automatic DNS provider writes**. Diagnostics must be actionable without leaking ACME tokens.

## Per-server OS update policy (Q144 D)

Candidate `ServerUpdatePolicy`: allowed package sources/versions, security/functional update groups, windows, privileged approvals, `plan_hash`, recoverable backup/snapshot and job states `PENDING → APPLYING → REBOOT_REQUIRED → VERIFYING → COMPLETED/RECOVERING`. Preview impact, dependent services, capacity and possible downtime, and revalidate before execution. UI intent cannot become arbitrary root shell. **Multi-server progressive orchestration remains later** (Q67/Q77), not required for the single-server MVP.

## Encryption and usable backup keys (Q145 D)

Q126/Q135 initial backups cover **panel configuration plus PHP website files**, with separate coherent recovery of necessary internal PostgreSQL state when relevant. Encrypt archives, verify integrity/versioned manifests and separate **data key**, wrapping keys, vault and a protected **off-failure-domain recovery copy**. Gate access to qualified roles, audit and rotate keys. Optional future **external KMS** and **multiple recovery authorities/custodians** may enforce policy-selected quorum and emergency access. Free Core should permit authorized local recovery without Hub or mandatory cloud KMS. Test failed disk, lost/unavailable vault, restoration on another authorized VM and limits of local-only archives; no promise of decryption when all recovery keys are gone.

## Scoped SFTP with audit and expiry (Q146 C)

Each SFTP identity has authorized websites/roots, **key-based** access, shell **disabled by default**, expiry/revocation and enforced quotas. Canonicalize paths, Unix permissions and symlinks at service boundary, not just UI. Audit allowed/denied access and important operations without logging secrets; revocation does not delete hosted files. Website manager Q136 gains no system administrator privilege.

## Private-beta pause gates (Q147 C)

Candidate `BetaRolloutPolicy` stores invited cohorts, signed version/channel, **configurable health gates**, pause thresholds, critical incident classification, pause/resume authority and recovery procedures. Pause blocks **new rollout installs/updates**, not deleting data or extinguishing rights already granted to legitimate recipients. Diagnostics remain **opt-in or narrowly contractual** (Q6) and sanitized, never mandatory for basic free Core operations. Q130 security lead/deputy coordinate any needed notices.

## Exit gates

Automate RBAC denials, VM/backup restoration with retrieved key, regression/security veto, DNS/IPv6/challenge failures, interrupted OS update and cross-tenant SFTP. These drivers and workflows are **proposals, not running implementations**. Documentation tests do not replace execution evidence.
