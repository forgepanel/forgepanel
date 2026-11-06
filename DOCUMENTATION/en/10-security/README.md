<!-- forgepanel-doc id=FP-10 revision=20 status=documented -->
# Security model and disclosure

[Français](../../fr/10-security/README.md) · [Index](../README.md)

## Assets, actors and boundaries

Protect Linux privileges, tenant data, database credentials, MFA/encryption keys, setup capabilities, signing authority and audit integrity. Consider unauthenticated network callers, hostile tenant code, compromised plugins, untrusted inputs and interrupted privileged work. A process already compromised as the application user can use that user's database privileges; the bootstrap environment flag is not a sandbox against that attacker.

| Boundary | Requirement |
|---|---|
| Browser → Symfony | Verified HTTPS, exact trusted host/origin, CSRF on mutations, secure session lifecycle, rate limits, resource authorization |
| Symfony → agent | Authenticated versioned private channel; typed allowlisted operations; no `exec(command)` API |
| Agent → Linux | Least privilege, bounded executor, safe path resolution, resource locks, system audit |
| Tenant → tenant | Separate identities/permissions and explicit resource controls; a PHP-FPM pool alone is not sufficient |
| Artifact → installation | Independent trust anchor, verified signatures/hashes, anti-rollback policy and safe key rotation |

SRC-03 implements setup-domain checks and source-level HTTP guards only. Systemd hardening, mandatory access controls, tenant isolation, production secret rotation, full login/RBAC and backup restoration are not demonstrated.

## Optional administrator MFA policy

Administrator MFA is **optional**, not a condition of initial account creation or wizard access. Offer TOTP and later WebAuthn, allow later enrollment, controlled disablement and recovery codes when enabled. Sensitive operations still require recent authentication and contextual permissions. The mandatory v0.7 source path needs a tested code fix.

## Hub communications and commercial entitlements

Under Q6, Hub enrollment is voluntary; premium checks, version discovery, diagnostics/support and marketing have separate permissions/consents or legal processing grounds. No automatic collection of hosting files, email, databases or secrets. Under Q7, the commercial offline grace is **60 days** for eligible previously verified premium rights, subject to contract dates; refusal/revocation must be explicit and non-destructive for essential hosting. See [product policy](../00-project-control/product-policy.md).

## Identity, payments and retention (Q56, Q58, Q59)

Hub payment providers use independent drivers with authenticated and deduplicated webhooks, never rights based only on browser redirects. SSO/OIDC is **optional**, with secure local recovery; administrator MFA stays optional. Per-category retention is limited by law, audit and backup requirements. These components are not operational.

## Trust chain and sensitive operations (Q61, Q65, Q66)

Signed packages/release metadata with protected trust roots, anti-rollback and approvals; encrypted replicated/immutable backup and real restore tests; recent authentication and configurable extra approval for sensitive operations. **Administrator MFA stays optional**, including setup. Signatures, backups and approval are not substitutes for independent permission enforcement. [Q61–Q70](../00-project-control/infrastructure-decisions.md).

## Keys, adoption and approvals (Q71, Q72, Q76)

Signed releases need protected key custody, rotation and anti-rollback (Q71); never distribute publisher private keys in code/packages. Adopting existing services (Q72) requires permissions, ownership inventory, snapshots and protection of unmanaged configurations. Sensitive actions (Q76) may require an independent approver; local emergency access remains audited. **Admin MFA remains optional** and approvals do not replace RBAC. [Decisions](../00-project-control/decisions-q71-q80.md).

## Website isolation, certificates and data — Q81–Q90

WebStack switching needs permission, safe listeners/`.htaccess`, HTTP/TLS and no disclosure via temporary test routes (Q81/Q82). Per-site PHP-FPM version/directives/extensions are allowlisted and quotas enforced (Q83). ACME/wildcard/imported TLS requires domain proof, DNS-01 and protected keys (Q84). Git Deploy/staging, clone and restore must never silently copy credentials/private data (Q85/Q90). Tenant-scoped MariaDB/MySQL/PostgreSQL/Redis/Valkey (Q86), restricted file manager/SFTP/SSH without root or implicit web terminal (Q87), private webmail/quarantine (Q88) and enforceable plan quotas (Q89). [Details](../02-architecture/website-lifecycle.md). **Not implemented.**

## Runtime and migration security (Q91–Q100)

Each website PHP pool/identity and actual Linux confinement require testing, with EOL notices and planned safe upgrade (Q91/Q92). Manual/webhook Git needs auth, anti-replay, allowed refs and secret-safe logs (Q93). Staging needs data masking, distinct secrets/URLs, blocked real outbound actions, retention/audit (Q94). ACME uses multiple issuers/DNS-01 with domain proof and protected tokens (Q95). Per-tenant DB/cache/SSH require quotas and expiry/revocation (Q96/Q97); Webmail and quarantine require authorized mailbox/domain access (Q98). Quota grace never bypasses host capacity or tenant separation (Q99). Cross-server migration requires both-side permissions, encryption, secret rotation and audited recovery (Q100). [Reference](../00-project-control/decisions-q91-q100.md). **Not implemented.**

## Q101–Q110 trust boundaries

EOL PHP exceptions are **temporary, site-scoped, authorized and audited**, with planned migration (Q101), never overriding isolation selected only from **OS-certified** Linux capabilities (Q102). Manual/webhook deployment policy applies by site and environment, with configurable approval and anti-replay (Q103); sensitive staging copies require **special approval** and isolated secrets (Q104). Multiple ACME CAs have bounded retries, alerts and last-good recovery (Q105). Shared/dedicated DB plus optional certified clusters enforce tenant scope (Q106). SSH keys/IPs and temporary/certified access include revocation (Q107). Webmail advice must show maintenance/security proof (Q108). Per-plan/resource quota grace never overrides host security or capacity (Q109). Advanced migration is allowed only with tested source/target consistency (Q110). [Specification](../00-project-control/decisions-q101-q110.md). **Tests not performed**.

## Minimum release gates

Never request the Linux root password through the panel. Keep the customer portal closed until authorization/session isolation is tested. Do not disable SELinux/AppArmor or firewall rules to make tests pass. Avoid secret-bearing URLs, logs and artifacts. Require read-only diagnosis before a proposed repair and explicit authorization for destructive changes. Restore tests must cover encryption keys, not just SQL/files.

Five-attempt bootstrap lockout can itself be abused for denial of service; network restrictions and recovery tests remain needed. TOTP code vectors do not equal a cryptographic audit. A port number is not an authorization boundary.

## Owner-approved vulnerability reporting (Q118 C)

Before public distribution **configure and verify** two channels: **GitHub private vulnerability reporting** if supported on the actual repository, plus a **dedicated security email with authorized recipients**. Define triage, severity, acknowledgement, restricted access, patch tracking and responsible notifications. No email address, contractual response time or bounty program is established by this document; verify the actual account configuration before advertising a reporting route. [Q111–Q120 decisions](../00-project-control/decisions-q111-q120.md).

## Security lead/deputy and private beta (Q127/Q130)

Q130 C requires an **appointed security lead and deputy** with authorized vulnerability access, incident triage, patch/notice coordination and escalation during absence. No such individuals are **appointed by this document**. Verify both Q118 private GitHub reporting and dedicated email before allowing external private-beta testers. Q127 never authorizes collection of customer secrets, public exploit details or skipping distribution-license obligations. [Decisions](../00-project-control/decisions-q121-q130.md).

## Private beta and vulnerability communication — Q137/Q140

Q137 D requires **invited testers, accepted terms, staged waves, a private bugs/releases channel, access suspension and documented recovery**. Pausing beta invites/updates cannot automatically delete users' data or extinguish AGPL rights already granted to recipients. Q140 C requires an **actually appointed security lead/deputy**, severity triage, tracked fixes, advisories and coordinated customer notices, with **both Q118 reporting routes (GitHub private + verified dedicated email) tested** before external beta. These gates are **specified, not configured or operational**. [Q131–Q140](../00-project-control/decisions-q131-q140.md).

## Access, recovery keys and advisories — Q145–Q150

**Q145 D**: separate backup keys/archive and keep an **off-failure-domain protected recovery copy**, vault and policy-scoped multiple custodians, with **optional external KMS**. Loss of all keys is a material irreversible risk, not a recoverable promise. **Q146 C**: site-scoped shell-disabled SFTP, enforced quotas, audited expiry/revocation; test symlinks/traversal. **Q147 C**: critical beta incidents/configured health thresholds **pause new waves** and trigger recovery, not hosted data erasure or revocation of previously granted software rights. **Q148 C**: future signed challenge with key rotation/anti-replay, org verification and manual lost-host recovery, preserving Q138 conditional approval. **Q149 C/Q150 D**: severity/contract partner duties and **signed** advisories with **risk-coordinated** disclosure, requiring actually appointed lead/deputy and verified Q118 contacts. [Decisions](../00-project-control/decisions-q141-q150.md).

## Q151–Q160 safeguards — reports, backup, access and advisories

**Q152 C** requires signed provenance/snapshot/history certification reports, not mandatory public compatibility publication. **Q153 C** permits scoped authorized audited *performance* exceptions, **never** Q132 tenant/access/recovery safety exceptions. **Q154 C** tests all **actually published** A/AAAA families without requiring absent IPv6. **Q155 C/Q156 C** require approved per-server reboot, usable backup/health/recovery and protected exported/checked recovery key before an **isolated restore**. **Q157 C** scopes SFTP **public-key** management by site/policy, quota/expiry/audit and sensitive step-up; never collect customer private keys. **Q158 C** minimizes beta diagnostics with **separate Q6 consents** and per-cohort gates, no forced collection. **Q159 C** retains Q138 extra approval for lost/repeated/mismatched/compromised transfers; **Q160 C** requires signed **human FR/EN and structured machine** advisories, optional notifications and protected sensitive data, without mandatory advanced formats or unverified reporting routes. [Decisions](../00-project-control/decisions-q151-q160.md).

## Reporting and review

No supported production release, private reporting email or response SLA has been established. Use GitHub private reporting only when available; otherwise request a private channel without posting exploit details or secrets publicly. Establish that channel before public distribution. Review sensitive code separately from implementation; no independent reviewer was available in this documentation audit. See [risk register](../19-audits-risks/README.md).

## Q161–Q170 security and exceptions

Ephemeral KVM runners are isolated and cleaned of secrets; signed Q162 evidence persists outside VM in private immutable RBAC-controlled storage. Q163 permits only separately approved, scoped, expiring, audited **noncritical performance** exceptions; Q132 critical failures remain FAIL. External Q164 DNS probe is SSRF protected and bounded; Q165 OS repair is explicit/allowlisted, nondestructive and retry-limited; Q166 backup is never recoverable without full isolated PASS restore and verified keys; Q167 SFTP public keys require possession/rotation/site scoping. Q168 prevents cohort reidentification/forced collection; Hub Q169–170 protects premium transfers and signed notices without disrupting free Core or revealing secrets. [Decisions](../00-project-control/decisions-q161-q170.md).

## R1 source intake security boundary

Source import requires exact SRC-03 bytes matched to canonical evidence. New `stage_source_archive.py` offers **unprivileged quarantine** after preflight, with no network, execution, Core overwrite or system deployment. Defenses include rejection of deceptive Unicode paths/Git metadata/setuid modes, separated validate/copy steps, private directory, 0600 regular files and provenance receipt. These controls are not a sandbox for running untrusted code: staged sources must not be executed/deployed. Neither Hub nor a plugin may authorize or bypass R1 source intake. [Contract](../12-development/source-staging.md).

## R1 security review — staged integrity and safe cleanup

Staged sources can be independently checked against **original ZIP + receipt + on-disk content**. [Audit contract](../12-development/source-staging-audit.md). Reject forged receipts, symlinks, hardlinks, nonprivate/executable modes, extra/missing files and altered originals. Failure cleanup uses a **private parent directory descriptor** and `dev/inode` identity to avoid removing an unrelated renamed directory. A same-UID attacker can still change staged data **after** auditing; final source importer must recheck bytes. Never root, generic shell, automatic import or Hub privilege.

## Q161 — KVM host pre-inspection security

[`tools/kvm-host-probe`](../14-devops-releases/kvm-host-probe.md) is an **unprivileged** Go tool: no arbitrary Linux command API, `ioctl`, opening `/dev/kvm`, VM execution, file creation, network, hostname/IP collection. It only inspects four **fixed** Linux paths with bounded reads and denies device symlink spoofing. A positive device observation never bypasses Q132 critical security vetoes, Q156 restore requirements or Q152/Q162 signed evidence. This tool is separate from the privileged daemon and Hub.

## Q161 — Admission never authorizes VM execution

The [R3 tool](../14-devops-releases/kvm-image-admission.md) is **read-only, nonroot and QEMU-free**: policy/request files must be private bounded regular files; QCOW2 must be owned with no symlink/hardlink, and all bytes are SHA-256 checked through file descriptors. No generic command/argument field exists; network/host shares/privilege requests are denied. `REVIEW_REQUIRED` grants **no privilege or Q132 PASS**, and declared resource ceilings are not enforcement. A future executor must revalidate bytes and isolate potentially malicious guests. No Hub signing keys or secrets are collected.

## R3 — Private staging security and immutability limit

[QCOW2 staging](../14-devops-releases/kvm-image-staging.md) has **no arbitrary shell/root API, QEMU or network access**. It requires separated canonical paths, nonroot account, 0700 directories, private source, `openat`/`O_NOFOLLOW`, non-executable copied files, full SHA-256 and receipt without secrets/private paths. A positive state proves **neither publisher identity, actual immutable storage, nor sandbox/real quota enforcement**: the same UID can alter even a 0400 file. Partial directories stay private for review and never count as qualification. Future launch requires another hash check; Q132 vetoes remain.

## R3 — Future IPC and installer trust boundary

[Typed IPC contract](../08-api-contracts/symfony-go-ipc-r3.md) requires independent transport-peer **and** actor/tenant/resource authorization by Symfony and Go, a [closed operation register](../../evidence/typed-agent-operations-v1.json) and redacted events. Both privileged activation/compensation actions remain **not authorized**, even if their payload passes JSON Schema. [Installer lifecycle](../14-devops-releases/installer-lifecycle-r3.md) requires signatures, anti-rollback, backup, emergency admin access and health evidence before success. **No generic shell API, running privileged daemon or browser-to-root endpoint; Q132 vetoes remain absolute.** Transport/privilege specifics require independent Security review.

## R3 — Peer authentication is not business authorization

[Local Symfony ↔ Go trust contract](../08-api-contracts/local-peer-trust-r3.md) separates kernel-observed peer process identity from an actor mandate derived from a verified authorized Symfony session. A shared Linux UID, group-mode socket or JSON actor_claim does not authenticate an end user. Recheck tenant, role, resource, plan/revision and the [closed operations registry](../../evidence/typed-agent-operations-v1.json). A [candidate peer-binding record](../../evidence/candidate-peer-binding-v1.schema.json) is not signed attestation. Privileged operations stay blocked. **RISK-028/029 unresolved**, no generic root API.
