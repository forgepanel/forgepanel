<!-- forgepanel-doc id=FP-19 revision=1 status=documented -->
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
