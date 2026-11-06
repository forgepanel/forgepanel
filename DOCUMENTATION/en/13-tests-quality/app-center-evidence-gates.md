<!-- forgepanel-doc id=FP-13-APP-EVIDENCE revision=1 status=specified -->
# App Center evidence and APPLY boundary — real integration gates

[Français](../../fr/13-tests-quality/app-center-evidence-gates.md) · [QA](README.md) · [Admission contract](../08-api-contracts/app-center-admission-evidence.md)

**PLANNED / NOT EXECUTED.** The 12 following real Core/Symfony/Go/VM cases are not satisfied by synthetic JSON fixtures or by passing offline Python unit checks.

| ID | Gate | Required result | Status |
|---|---|---|---|
| TEST-EVID-FP-0001 | Authenticated host peer and target binding | Agent peer authenticated; host ID cannot be forged by the browser | PLANNED |
| TEST-EVID-FP-0002 | Symfony actor/tenant/site RBAC | Different tenant/actor/site forbidden under true Core session | PLANNED |
| TEST-EVID-FP-0003 | Host observation freshness | Expired, future and unavailable host observation cannot authorize planning/APPLY | PLANNED |
| TEST-EVID-FP-0004 | Policy revision and TOCTOU | Concurrent policy change invalidates stale preview; APPLY rechecks current version | PLANNED |
| TEST-EVID-FP-0005 | Authorization revision and revocation | Revoked user/site permission invalidates earlier intent before APPLY | PLANNED |
| TEST-EVID-FP-0006 | Source signature and trust roots | Forged signer/catalog metadata rejected; trusted peer and key lifecycle tested | PLANNED |
| TEST-EVID-FP-0007 | Native One-Click autonomy | Native installer does not require Hub, payment or Docker/Podman presence | PLANNED |
| TEST-EVID-FP-0008 | Container driver and measured budgets | Docker-only recipe cannot run via Podman; CPU/RAM and quota from real host | PLANNED |
| TEST-EVID-FP-0009 | Control-plane port isolation | FORGE 8447 and PANEL 8446 cannot be allocated; fallback admin preserved | PLANNED |
| TEST-EVID-FP-0010 | Idempotency and fencing | Retry with same key/digest never double-applies; stale fencing blocked | PLANNED |
| TEST-EVID-FP-0011 | Recoverable partial failure | Crash after partial Linux/SQL effect requires truthful recovery state and data retention | PLANNED |
| TEST-EVID-FP-0012 | Hub cannot grant Core Linux authority | Publisher entitlement, update or diagnostic cannot become Go operation rights | PLANNED |

## Qualification evidence

A real PASS requires exact Core, agent and DB commit, OS/VM, authenticated peer and actor/tenant test identities, trusted clock/snapshot and policy revision, signed artifact provenance, failure/denial logs redacted, genuine resource locks and verified recovery. A BLOCKED/SKIP state must never be called PASS; peer-identity, time, rollback and idempotency tests must include adversarial cases.

No feature implementation, live security check, host permission or HTTPS listener is claimed by this matrix. Q1–Q220 remain retained; Q221+ open.
