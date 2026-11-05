<!-- forgepanel-doc id=FP-04-COMPONENTS revision=1 status=documented -->
# Component records

[Français](../../fr/04-modules/components.md) · [Module index](README.md)

All prototype paths below are inside SRC-03, not tracked application paths in this repository. Their state is `IMPLEMENTED IN ARCHIVE`; native tests were rerun, but they are not published or deployed. Shared lifecycle: source compilation/testing in a laboratory; no automated production installation, upgrade or uninstall. Removal of prototype code never authorizes deletion of accounts, keys or databases. These common rules apply to every record unless stated otherwise.

## CMP-CLI — Local CLI and preflight

| Field | Record |
|---|---|
| Goal / users | Operator/engineer entry point; `cmd/forgepanel`, `internal/doctor` |
| Functions / acceptance | Version, read-only host preflight and JSON diagnosis; errors have defined exit codes; unsupported operations must not mutate the host |
| Dependencies / consumers | Go/Linux and host facts; used by operators and future installer, not a live web service |
| Data / migration | No application schema; diagnostic output; no migration |
| Contracts / jobs | CLI arguments and exit codes; no broker or event stream |
| Permissions / security | Inspection only for doctor; no arbitrary shell API; redact sensitive diagnostics before sharing |
| Failure / lifecycle | Return preflight/usage/internal failure; compile locally; no installer or automatic repair |
| Tests / observability / limit | Go tests and CLI build pass; structured report; full platform `status` and repair remain absent |

## CMP-PLAN — Install-intent planner

| Field | Record |
|---|---|
| Goal / users | Convert administrator configuration into an inspectable plan; `internal/installer` |
| Functions / acceptance | Strict configuration and target/profile selection; always reports `executable=false` until a separate execution engine exists |
| Dependencies / consumers | OS facts and config schema; consumed by CLI and exported wizard intent |
| Data / migration | Version-1 JSON intent; no durable execution journal or migration |
| Contracts / jobs | Five profile IDs, six fixture targets, symbolic steps and blockers; no actual installation jobs |
| Permissions / security | Planning requires no privileged changes; reject unknown/duplicate/oversized or conflicting input |
| Failure / lifecycle | Invalid input fails before action; no packages/services/ports modified; schema changes need compatibility tests |
| Tests / observability / limit | Go validators and 30 fixture combinations tested; no package availability or VM qualification |

## CMP-SETUP — Bootstrap domain and MFA enrollment

| Field | Record |
|---|---|
| Goal / users | Establish the first panel administrator without Linux credentials; `apps/panel/src/Setup` |
| Functions / acceptance | Token issuance/consumption, one initial account, TOTP enrollment, local resume and revisioned draft; no configuration before MFA |
| Dependencies / consumers | Clock, repository transaction, secret encryption, TOTP; consumed by HTTP controllers and local console commands |
| Data / migration | Setup verifiers/counters, account and audit through the three-table schema |
| Contracts / jobs | Named phase transitions and grant-bound methods; audit events; no system provisioning jobs |
| Permissions / security | Short-lived grants, hash verifiers, Argon2id password hashes, encrypted MFA data; local issuance restricted |
| Failure / lifecycle | Persist invalid attempts, roll back infrastructure errors, reject replay/stale revision; v0.6 tokens not migrated or accepted |
| Tests / observability / limit | 28 native PHP tests/184 assertions pass; metadata audit excludes secrets; permanent login and recovery-code consumption absent |

## CMP-WIZARD — Symfony setup interface

| Field | Record |
|---|---|
| Goal / users | Guided initial setup for server owner; controller, Http boundary and Twig templates |
| Functions / acceptance | Registration, MFA, recovery-code display, configuration and JSON export; reviewed draft must not say installed |
| Dependencies / consumers | Symfony/Twig, sessions, CSRF, rate limiter and CMP-SETUP; browser and CLI plan consume outputs |
| Data / migration | Session capability and transient recovery display; database writes delegated to setup domain |
| Contracts / jobs | Declared `/setup` routes; GET views/exports and CSRF-protected POST mutations; no remote agent job |
| Permissions / security | HTTPS/origin boundary and grant checks; USER portal closed; cookies not isolated by port |
| Failure / lifecycle | Resume expired setup locally; return safe errors; dependency resolution and HTTPS gateway are prerequisites |
| Tests / observability / limit | PHP syntax checked, framework/HTTP/browser execution pending; source guards are not integration proof |

## CMP-STORE — PostgreSQL setup repository

| Field | Record |
|---|---|
| Goal / users | One transaction authority for bootstrap; infrastructure repository/transaction classes |
| Functions / acceptance | Lock singleton, create account, persist state/audit; failed transaction must leave no consumed token without account |
| Dependencies / consumers | PDO PostgreSQL, migrated dedicated database; consumed by setup domain |
| Data / migration | `fp_setup`, `fp_admins`, `fp_setup_audit`, partial unique initial-admin index; `001_setup.sql` |
| Contracts / jobs | SetupRepository/SetupTransaction; no message queue or hosting schema |
| Permissions / security | Dedicated runtime SQL role planned; production role must not perform DDL; encryption key outside database |
| Failure / lifecycle | SQL rollback on infrastructure failure; migration runner, backup and upgrade orchestration absent |
| Tests / observability / limit | Supplied SQL test exits 77 here; no database concurrency/restore certification; audit rows are not a complete tamper-proof audit service |

## CMP-BRIDGE — Fixed local console bridge

| Field | Record |
|---|---|
| Goal / users | Privileged local operator invokes only setup status/token/resume; `internal/panelbridge` |
| Functions / acceptance | Verify trusted paths; drop to `forgepanel` identity; execute fixed PHP console action; never run application PHP as root |
| Dependencies / consumers | Linux credentials, root-owned `/usr/share/forgepanel/panel/bin/console`, trusted PHP, service account and healthy PHP/SQL; consumed by CLI |
| Data / migration | No own schema; console accesses setup state; no own migration |
| Contracts / jobs | Three allowlisted actions, sanitized environment, bounded execution; no generic command executor |
| Permissions / security | Local sudo/root required; token output needs controlling TTY; caller environment not inherited |
| Failure / lifecycle | Missing/untrusted installation fails closed; no fallback to legacy tokens; installed package lifecycle not supplied |
| Tests / observability / limit | Go guard tests pass; installed credential drop/end-to-end flow unverified; cannot recover SQL-backed accounts with SQL down |

## CMP-RELEASE — Publication verification prototype

| Field | Record |
|---|---|
| Goal / users | Validate signed publication metadata; `internal/releases`, CLI `release verify` |
| Functions / acceptance | Verify Ed25519 signature, expiry, sequence and library artifact hashes; altered inputs must fail |
| Dependencies / consumers | Caller-provisioned public key, clock and manifest; future installer/updater consumer |
| Data / migration | No persistent trust/sequence store, no schema migration |
| Contracts / jobs | Manifest and detached signature; CLI checks manifest only, not artifact bytes; no download/install job |
| Permissions / security | Read-only verification; trust depends on independent key provisioning; no production private key supplied |
| Failure / lifecycle | Invalid, expired or insufficient-sequence manifest rejected; key lifecycle/update/install/removal not implemented |
| Tests / observability / limit | Go adversarial unit cases pass; no official channel, key rotation/revocation or persistent rollback protection |

## CMP-LEGACY — Historical file token store

| Field | Record |
|---|---|
| Goal / users | Preserve the v0.6 prototype/test history; `internal/bootstrap` |
| Functions / acceptance | File-based token expiry/single use and locking protections; not accepted by the v0.7 web flow |
| Dependencies / consumers | Local filesystem/Go; tests only in the current integration |
| Data / migration | Local token state; no automatic migration into SQL |
| Contracts / jobs | Historical package API; no active web or agent contract |
| Permissions / security | Private files and lock checks; never use as silent SQL fallback |
| Failure / lifecycle | Reject unsafe locks/replay; deprecation/removal needs explicit decision, not production state deletion |
| Tests / observability / limit | Go tests pass; historical artifact, not current bootstrap authority |

## CMP-AGENT-TARGET — Future system agent

State: `SPECIFIED`, not implemented. Operators and Symfony will consume a private typed API; OS/service adapters, durable jobs, resource locks and audit are dependencies. Job journal schema and IPC contract are not finalized. It must enforce authorized resource scope independently, isolate a minimal privileged executor and recover interrupted operations without arbitrary shell commands. Installation/update/removal need signed packages, systemd policies and per-OS tests. Acceptance requires peer authentication, denied operations, safe paths, concurrency, crash recovery and service-health evidence. No runnable daemon or monitoring endpoint is supplied.

New component records must retain all fields above, including absent migrations/contracts, consumers, failure behavior, lifecycle and test limits. Missing detail is recorded explicitly rather than filled with invented functionality.
