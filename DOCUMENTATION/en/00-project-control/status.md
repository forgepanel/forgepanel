<!-- forgepanel-doc id=FP-00-STATUS revision=1 status=documented -->
# Status and dependency-ordered roadmap

[Français](../../fr/00-project-control/status.md) · [Project control](README.md)

## Evidence levels

`PROPOSED`: option requiring assessment. `SPECIFIED`: requirements/contracts written. `IMPLEMENTED`: source exists, with its location named. `VERIFIED`: a named check ran against a named input/environment. `PUBLISHED`: identifiable release and artifacts. `DEPLOYED`: identified environment and deployed revision. `MERGED` describes Git integration only. Documentation status is separate from feature status.

## Baseline on 2026-11-05

| Scope | Real state |
|---|---|
| GitHub before this task | Private, empty; no branches, commits, issues, PRs or releases returned |
| Repository after this documentation change | Documentation, governance and documentation validation tooling; no application import |
| Foundation v0.6/v0.7 | Supplied development archives; provenance recorded in the audit |
| v0.7 native tests | Re-executed successfully in the local container; not VM certification |
| Symfony HTTP and PostgreSQL integration | Sources/test supplied; not executed in this audit |
| Installer, full agent, WebStacks, full RBAC, plugins | Not available as a working product |
| Release and production | None evidenced; license unresolved |

All six OS targets and five profiles are planning inputs. Thirty fixture combinations are not thirty installations. The `production` branch initially points to a README-only bootstrap commit and deploys nothing.

## Roadmap

| Priority | Deliverable | Dependency and exit evidence |
|---|---|---|
| P0 | Documentation baseline and reviewed PR | Link/parity checks; facts and risks recorded |
| P1 | Provenance-preserving source import | Reviewed v0.7 inventory; no secrets/generated binaries; license status explicit; tests repeated on imported commit |
| P2 | Symfony + PostgreSQL integration | Dependency resolution/lock/audit; real HTTP, transaction rollback/concurrency and browser tests |
| P3 | Permanent identity and recovery | Login/logout, optional MFA (enroll/disable/recovery), scoped authorization, session isolation tests; fix v0.7 setup gate |
| P4 | Six-OS packaging and service foundation | Trusted package sources, runtime policy, systemd and mandatory access controls verified in VMs |
| P5 | Plan execution and one-command installation | Durable steps, safe retries, TLS, rollback/compensation, signed distribution and reinstall/update tests |
| P6 | Hosting modules and additional stacks | Proven isolation, resource controls, backups/restores and per-profile VM evidence |
| P7 | Third-party ecosystem | Trust model, contracts, isolation and maintenance policy accepted before execution |

No date or version commitment is implied by these priorities. Product-owner decisions still needed: software/contribution license and authorized private security contact. Package/runtime choices require an evidence-based technical proposal, not a new architecture by assumption.
