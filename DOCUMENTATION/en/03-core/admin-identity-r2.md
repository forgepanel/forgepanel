<!-- forgepanel-doc id=FP-03-ADMIN-IDENTITY-R2 revision=1 status=specified -->
# R2 — read-only administrator identity candidate

[Français](../../fr/03-core/admin-identity-r2.md) · [QA](../13-tests-quality/r2-admin-readonly-qa.md) · [R2 existing contracts](bootstrap-identity-r2.md)

**PROPOSED CODE / NOT APPROVED FOR A PRODUCTION ADMIN PANEL.** Reuse the original Foundation v0.7.1 PostgreSQL tables for an initial administrator, password hash, optional encrypted TOTP secret, replay counter, hashed one-time recovery codes and audit. No extra tables, DDL, privileged Linux operation, new module, Hub integration, network listener or production installer is added.

## Limited authentication

`AdminAuthentication` verifies Argon2id passwords against the database; unknown principals use a non-secret dummy Argon2id verifier to reduce account enumeration. Incorrect credentials have the same generic public response. The SQL `fp_setup` singleton must be `phase=REVIEWED` with the matching initial administrator and `ROLE_SUPER_ADMIN`. This phase indicates **a plan reviewed, never a deployed server**. This candidate grants only a read-only `/admin` preview; no site, API or root operations are exposed.

When MFA is opted into by the owner, TOTP validation compares the verified counter with the last committed counter under a locked SQL transaction; old steps are rejected. Alternatively, one 24-hex recovery code may be consumed from the hashed JSONB list atomically, never stored or logged in plaintext. When MFA is opted out, password-only login is supported, without retaining a pending TOTP secret.

`AdminSessionController` uses GET/POST `/login`, GET `/admin` and POST-only `/logout`. It applies CSRF to login/logout, a pair of provisional per-IP and hashed IP+principal Symfony limiters, session identifier rotation and clearing of the setup grant at login, and revocation on logout. The session stores only the administrator ID, timestamp and HMAC of the credential/policy version; every protected read rechecks PostgreSQL and rejects expired/forged credentials, revoked passwords and changed MFA policy. DB unavailability fails closed. Audit is redacted.

The `__Host-FORGE_ADMIN` cookie configuration remains Secure/HttpOnly/SameSite=Strict, root path and host-only. The existing boundary refuses HTTP, incorrect Host, port and Origin. No proxy is trusted by default. Missing or incorrect CSRF must not mutate identity state.

## Review blockers

This is a **read-only identity preview**, not an operational Symfony Security authenticator or tenant-scoped RBAC layer. Before a real administration page can write to host resources, require independent Security/API/Database review, signed/authorized IPC, actual installer qualification, role checks, a full Symfony authenticator, session store/revocation policy, CSRF browser tests through real HTTPS, rate-limiter persistence across workers, recovery and restore tests, and the complete R2 acceptance matrix. Numeric rate limit and session expiry are candidate values, not product-owner decisions. External Hub has no role in local login; modules not yet available cannot be activated.
