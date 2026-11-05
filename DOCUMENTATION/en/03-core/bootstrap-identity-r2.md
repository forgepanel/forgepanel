<!-- forgepanel-doc id=FP-03-IDENTITY-R2 revision=1 status=specified -->
# R2 — Candidate bootstrap, identity and session contract

[Français](../../fr/03-core/bootstrap-identity-r2.md) · [Core](README.md) · [R2 transactions](../09-database/setup-transaction-r2.md) · [R2 matrix](../13-tests-quality/r2-integration-gates.md)

**Owner:** Core / Security with Database and API/IPC review. **State: SPECIFIED — CANDIDATE, not implementation-APPROVED.** This refines existing requirements **without changing Q1–Q170**. No functioning Symfony HTTP integration is evidenced; original SRC-03 source is still missing (R1, [issue #2](https://github.com/yyogas/forgepanel/issues/2)). IDs R2-ID-001–R2-ID-012 are documentation requirements, not executed code.

## Boundaries and actors

| Actor | Target capability | Explicit denial |
|---|---|---|
| Unauthenticated visitor | Local bootstrap entry only while server is eligible | Post-activation configuration and other users' state/secrets |
| Bootstrap-token holder | Exchange ephemeral proof for bounded grant | Multiple initial super-admins, endless renewal, Linux operations |
| Initial administrator | Establish durable identity after validations | Linux root impersonation or other-tenant privilege |
| Application Super Administrator | Authenticated panel use and recent authentication for sensitive changes | Generic root shell and bypass of resource scopes |
| Website manager | Only the authorized owned websites after R4 | Global server changes, role grants or cross-tenant SFTP/backup |
| Hub administrator | **No privileged Core rights** merely from licensing | Core sessions, private keys, OS recovery or customer content |

**R2-ID-001 — Separation:** Linux root, privileged service operator and Symfony application admin are distinct; publisher Hub identity grants no Core operation.

## Observed bootstrap states and required evolution

SRC-03 uses `NEW → TOKEN_ISSUED → MFA_PENDING → CONFIGURING → REVIEWED`. These are historical state names, **not** proof of permanent account activation. The v0.7 mandatory-TOTP path is **superseded** by the owner decision: administrator **MFA optional**, skip cannot block the wizard.

- **R2-ID-002 — Bootstrap entry:** restricted to trusted local exposure with defense against publicly exposed listeners; validate origin, trusted host and proxy boundaries. Never pass Linux root credentials to browsers.
- **R2-ID-003 — Token/grant:** cryptographically generated, verifier-only storage, expiry and attempt limits matching prototype subject to actual tests; redact raw tokens from logs, URLs, exceptions and reports. Prefer nonenumerating errors for unknown/expired inputs.
- **R2-ID-004 — Atomic exchange:** one locked SQL transaction checks proof, attempt counters and grant issuance; refuse reused tokens and concurrent activation. Database commit precedes acknowledging an achieved transition.
- **R2-ID-005 — Durable initial account:** exactly one initial administrator, normalized unique email, Argon2id password and explicit account activation state; DB constraints enforce singleton during concurrency.
- **R2-ID-006 — Explicit MFA choice:** present “Enable MFA” and “Continue without MFA.” On enable, TOTP enrollment with possession proof and protected recovery. On skip, do not create a fake TOTP secret or block configuration. Later enrollment is authenticated and audited.
- **R2-ID-007 — Resume:** reboot/retry preserves only committed state; new resume grant revokes old grant. Out-of-order/stale revision requests must not erase an active administrator.
- **R2-ID-008 — Session isolation:** bootstrap grant is distinct from permanent login session. Rotate session identifier on authentication/privilege changes; Secure/HttpOnly/SameSite cookies appropriate to flows, CSRF/fixation protections, logout and server-side expiration. Numeric lifetime remains open.
- **R2-ID-009 — Server-side authorization:** RBAC + organization/site scope + resource ownership for **every API/action**; hiding UI controls does not enforce access. Use nonenumerating responses where appropriate.
- **R2-ID-010 — Sensitive actions:** recent authentication and policy/risk-based independent approval when applicable; MFA does **not** become required by default for admin without a new explicit owner choice. Core RBAC does not derive from commercial entitlements.
- **R2-ID-011 — Audit:** correlate bootstrap, denials, success, grant renewal, MFA enrollment/skip, recovery, login/logout; timestamp, resource scope and actor where relevant; never log tokens, cookies or secrets.
- **R2-ID-012 — Recovery:** specify and test a local administrator access-recovery flow without public/root endpoints, deletion of the active account, or Hub dependency. Lost-access proof and exact recovery policy remain an **open technical review** for Security.

## Candidate logical exchange contracts (no new public routes)

| Logical operation | Preconditions | Business result | Errors and recovery |
|---|---|---|---|
| `bootstrap.exchange` | Local trust, bounded token, authorized origin | Ephemeral grant bound to committed state | `DENIED`, `EXPIRED`, `LOCKED`, `CONFLICT`, `UNAVAILABLE` |
| `bootstrap.admin.create` | Valid grant, singleton rule, current revision | Durable configuring account | `CONFLICT`, `INVALID`, SQL rollback |
| `bootstrap.mfa.choose` | Current grant, explicit `enable` or `skip` | Committed transition, TOTP only if chosen | `STALE_REVISION`, invalid proof, rollback |
| `bootstrap.resume` | Local proof and authorized resume policy | Revoke previous grant, issue new | `DENIED`, `CONFLICT`, unavailable DB |
| `identity.login/logout` | Permanent identity and hardened session | Create/revoke local session | `DENIED`, `RATE_LIMITED`, `EXPIRED` |

**Exact request/response schemas, endpoints, TTL, thresholds and HTTP codes remain subject to API/IPC, Security and Database ratification** against the imported original source. Candidate contracts do not create working endpoints.

## Verification and exit gates

[R2 matrix](../13-tests-quality/r2-integration-gates.md) tracks `R2-AUTH-001` to `R2-AUTH-010`: MFA enable/skip, invalid TOTP, replay, expiry, CSRF, origin/proxy, concurrency, lost response after commit, restart, sessions and cross-tenant denial. **Every integration test remains PLANNED**; no genuine Symfony/PDO PostgreSQL process ran in this documentation work.

**Dependencies and HANDOFF:** R1 source import issue #2 → Core/Identity [#6](https://github.com/yyogas/forgepanel/issues/6) → Symfony/PG [#3](https://github.com/yyogas/forgepanel/issues/3). Database owns any schema change, API/IPC owns any endpoint/transport, Security owns recovery/secrets. No code, migration or numerical configuration value is invented.
