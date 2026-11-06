<!-- forgepanel-doc id=FP-19 revision=10 status=documented -->
# Audit, contradictions and risks

[Français](../../fr/19-audits-risks/README.md) · [Index](../README.md)

[Observed baseline and provenance](baseline.md) · [Executed checks and limits](verification.md)

## Risk and reconciliation register

| ID | Evidence / conflict | Impact and next action |
|---|---|---|
| RISK-001 | Owner text calls the repository public; connector reports private | Keep visibility unchanged; write publication-safe docs; owner decides any future visibility change |
| RISK-002 | Earlier conversation describes a code foundation; GitHub was empty | Archive implementation is not tracked implementation; reviewed provenance-preserving import is the next code task |
| RISK-003 | PHP 8.4 preference versus archive >=8.2; no six-OS package policy | Preserve manifest facts; qualify panel runtime/package provenance before installation |
| RISK-004 | Twig exists, UX/Tailwind/Messenger are architectural targets | Do not advertise dependencies or functions absent from the archive |
| RISK-005 | SQL/HTTP implementation exists but integration untested | Block exposure until actual transaction, concurrency, session and browser tests pass |
| RISK-006 | Local bootstrap and global five-attempt lockout | Recovery and denial-of-service tests needed; local privilege flag is not a sandbox |
| RISK-007 | Full agent, recovery engine and system adapters absent | Do not claim one-command install, repair or certified WebStacks |
| RISK-008 | File bootstrap v0.6 versus SQL bootstrap v0.7 | Document incompatibility; never silently fall back to the old token store |
| RISK-009 | License/contribution terms and private security contact unresolved | Owner decisions before external redistribution/contributions and public support |
| RISK-010 | Branch-protection read denied; ruleset read denied with plan message | Preserve settings; do not infer no protections or bypass required approval |
| RISK-011 | Prototype release verifier lacks full distribution trust lifecycle | Need trusted key provisioning, artifact checks, anti-rollback persistence and rotation/revocation |
| RISK-012 | No independent reviewer or production benchmark | Self-review and tests are limited evidence, not audit/certification/performance claims |

## Resolution policy

Record source, affected documents/contracts, risk, proposed resolution and decision owner. Recent explicit owner requirements are reconciled without deleting historical provenance. No licensing, architecture, public-visibility or deployment decision is silently made to remove a blocker.

Documentation numbering v0.1–v0.5 in the conversation is design history, not a software release timeline. The archive's `0.7.0-dev` is its own identifier. Only actual repository changes enter the central changelog; roadmap intentions do not become release entries.

This audit examined repository metadata, supplied archive structure, key code/contracts and native tests. It is not an exhaustive source security review, dependency audit, penetration test or six-OS certification. Add new findings to this register and propagate their effects to both languages.

## R1 import blockers and preflight limitations

- **RISK-013** — Original SRC-03 archive unavailable: no import or prose-based code recreation; recover genuine bytes and verify pinned checksum.
- **RISK-014** — Evidence SHA-256 and limited secret signatures are not publisher authentication or exhaustive audit; legal, dependencies, secrets, diff and architecture review still required before import.

[R1 preflight](../12-development/source-archive-intake.md) mitigates certain archive risks but **does not close RISK-002 or qualify production**.

## R1 quarantine risks: controls without source import

- **RISK-015** — Accidental overwriting or execution on extraction: refuse root, use fresh private off-repo directory, file mode 0600 and Linux `O_NOFOLLOW` path traversal, stop/clean on changed member digests. Human review still precedes any import.
- **RISK-016** — Spoofed archive names and overridden evidence: preflight rejects noncanonical/bidi Unicode, embedded `.git`, live environment files and setuid/setgid modes; CLI `--stage` refuses a custom `--evidence` override. Heuristic controls cannot guarantee no secrets.

The 33 synthetic checks test tooling guardrails, **not genuine source or Core integration**. [Specification](../12-development/source-staging.md).

## Targeted R1 review — independent quarantine integrity

- **RISK-017** — Staging receipt can change after creation: require read-only comparison to **genuine pinned source ZIP**, strict receipt/member matching and denial of executable modes, links and unexpected/missing entries.
- **RISK-018** — Directory-substitution risk during failure cleanup: anchor cleanup to private parent descriptor and verify created inode/device; skip and report cleanup if target identity changes. An attacker under the **same UID** may still alter quarantine **after verification**; final importer must revalidate bytes.

These protections do not replace source code or publisher-signature review. [FR/EN contract](../12-development/source-staging-audit.md).

## R3 observation: false-qualification risk

- **RISK-019** — A `/dev/kvm` node or VMX/SVM CPU flags cannot prove device access, safe QEMU/KVM boot, isolation, quotas, snapshots or recovery. Standalone [KVM Host Probe](../14-devops-releases/kvm-host-probe.md) therefore only emits `qualification=NOT_EXECUTED`, explicit `false` gates and `INCONCLUSIVE`/deny states. CI success on a runner without KVM certifies no Debian, Ubuntu or other OS. Real R3 drivers and Q152/Q162 signed reports remain pending.

## R3 local image admission risks

- **RISK-020** — An **unsigned** local policy and matching SHA-256 establish neither publisher trust nor execution permission; status remains `REVIEW_REQUIRED` with `qualification=NOT_EXECUTED`. Define identity/authorization, provenance, signature, immutability and independent review before executing guests.
- **RISK-021** — A QCOW2 header does not prove full format **structural** integrity; same-UID processes may modify an image after admission. A future runner must validate format, pin the exact launched bytes, enforce actual quotas/isolation and test recovery. Synthetic tests do not close RISK-019.

[Preparatory contract](../14-devops-releases/kvm-image-admission.md).

## R3 — Additional lab image copy risks

- **RISK-024** — A QCOW2 image copied and marked mode 0400 is **not immutable** against a same-UID process. The receipt is unsigned, and a future runner must rehash bytes under an independently authorized isolation boundary, never using the receipt as QEMU permission.
- **RISK-025** — After interruption a private, incomplete `run_id` directory may remain; `PARTIAL_STAGE_REQUIRES_MANUAL_CLEANUP` avoids dangerous recursive deletion of substituted paths. The future runner must test and document safe bounded teardown, real quotas and failure recovery.

[Specification and limits](../14-devops-releases/kvm-image-staging.md). Does not close RISK-019, RISK-020/021 or issue #42.

## AUDIT-DOC-001 — Stale documentation status and false-completeness risk

**Finding:** some status pages still showed R1/R3 as candidate `features/*` branches after PRs #37–#43 had merged into `develop`; the [coverage matrix](../00-project-control/coverage.md) did not separately track bilingual structure and executable specifications. **Documentation severity: medium; state: proposed fix in this PR.** The [versioned 22-gap register](../00-project-control/documentation-readiness.md), [traceability](../00-project-control/requirements-traceability.md) and [reconciled status](../00-project-control/status.md) correct the status narrative without clearing real SRC-03/HTTP/SQL/VM/ABI blockers. **Required checks:** FR/EN ID parity, acyclic dependency graph, exact PR/CI references and targeted independent bilingual semantic review where available; CI is not product certification.

## Additional R3 risks — false authorization and false recovery

- **RISK-026 — Schema-as-permission confusion:** a request matching the [IPC JSON Schema](../../evidence/candidate-ipc-request-v1.schema.json) proves neither transport peer, actor, tenant scope nor Linux privilege. Block all privileged operations until reviewed Symfony/Go authorization, approved policy/plan, authenticated transport and actual negative tests exist. No generic `shell.exec`.
- **RISK-027 — False recovery/publisher trust:** a signed manifest is not verification of the exact artifact bytes; failure between SQL and Linux is not an atomic rollback. [Candidate installer lifecycle](../14-devops-releases/installer-lifecycle-r3.md) requires independent trust, signed artifacts, anti-rollback, durable steps and compensation of known reversible effects only. Missing recovery key or irreversible migration requires `RECOVERY_REQUIRED` and disclosure.

Both risks remain **OPEN**. The [24 R3 test cases](../13-tests-quality/r3-ipc-installer-gates.md) are `PLANNED`, not mitigation evidence. R1/R2 dependencies and Q132 vetoes stay in effect.

## R3 — New findings: stale fencing and IPC identity confusion

- **RISK-028 — Stale worker after lease expiry:** an old worker may resume and mutate Linux despite a newer lease owner. [Durable job contract](../09-database/durable-jobs-r3.md) requires monotonically fenced generations checked at the effect boundary, reconciliation and denial of blind retries. **OPEN**, no verified Linux protection exists.
- **RISK-029 — Socket peer vs actor authorization confusion:** a file permission or valid peer UID alone proves neither user mandate nor tenant scope. [Peer trust contract](../08-api-contracts/local-peer-trust-r3.md) requires independently checked authorization and replay resistance. **OPEN**, no authenticated service/transport is operational.

Green static JSON/Markdown checks cannot close these risks or authorize a privileged operation. [Negative QA matrix](../13-tests-quality/r3-jobs-peer-gates.md).
