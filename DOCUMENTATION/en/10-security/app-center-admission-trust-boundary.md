<!-- forgepanel-doc id=FP-10-APP-TRUST revision=1 status=specified -->
# App Center — preflight evidence provenance and authorization boundaries

[Français](../../fr/10-security/app-center-admission-trust-boundary.md) · [Security](README.md) · [Preview contract](../08-api-contracts/app-center-preview-contract.md)

**DRAFT SECURITY MODEL / NOT VERIFIED.** ForgePanel's App Center needs *three separate trust origins*: server capabilities, authenticated Core authorization, and untrusted user intent. This document describes the architectural gate, **not a deployed trusted-agent protocol, permission voter, anti-replay implementation or security audit approval**.

## Corrected boundary from candidate-code review

The earlier synthetic preview incorrectly placed site membership and the container permission flag in its **host capacity** fixture. Linux interface/resource observations cannot prove a user's identity, tenancy or permission. The candidate prototype now separates:

| Source | Fields | Production source required | Never inferred from |
|---|---|---|---|
| Host capabilities | Host ID, PHP availability, qualified SQL/container drivers, free CPU/RAM/PIDs, reserved and bound ports | Reviewed local inventory service/agent, authenticated to Core and scoped to the addressed host | Browser form, catalog metadata, Hub billing, JWT claims alone |
| Authorization context | Authenticated actor, tenant, target website ownership, container-operation permission | Symfony server-side identity, RBAC, organization/resource checks, effective policy revision | Linux host probe, plugin widget, untrusted request |
| Installation request | Host/tenant/site references, selected recipe variant, requested host TCP ports | Client-origin *intent* normalized by Core, never permission | Unauthenticated HTTP parameters as authority |

These objects may share IDs **for cross-reference only**. String equality or a matching mock site list is **not authentication**, nor does it imply that the target site's ownership is current. Never accept the entire host snapshot or the authorization context from user-submitted JSON.

## Candidate offline implementation

The independent [host capacity fixture](../../../evidence/app-center-fixtures/host-capabilities.synthetic.json) now contains **no actor, tenant sites or container authorization**. The separate [authorization fixture](../../../evidence/app-center-fixtures/authorization.synthetic.json) contains an imaginary actor/tenant/host and site scope, explicitly tagged `SYNTHETIC_UNVERIFIED`. A third [request fixture](../../../evidence/app-center-fixtures/install-request.synthetic.json) contains user intent and host/tenant references.

The [offline preview](../../../scripts/preview_app_center_install.py) rejects any extra host/request authorization fields, invalid synthetic scopes and self-declared `VERIFIED` state; cross-host or cross-tenant mismatches add `HOST_SCOPE_MISMATCH` or `TENANT_SCOPE_MISMATCH`, and missing site membership adds `SITE_OWNERSHIP_UNVERIFIED`. The preview always emits:

```json
{
  "input_trust": {
    "host_capabilities": "SYNTHETIC_UNVERIFIED",
    "authorization_context": "SYNTHETIC_UNVERIFIED",
    "client_request": "UNTRUSTED_CANDIDATE"
  },
  "tenant_authorization_verified": false,
  "runtime_capabilities_verified": false,
  "execution_allowed": false,
  "apply_available": false
}
```

This is **illustrative partial output**, not a signed/approved result. `MATCHES_SYNTHETIC_FACTS_ONLY` is not an installation admission, even if none of the fictional numbers conflict. Preview input check success never creates reservations, keys, locks, audit records, tokens or Linux effects.

## Production admission still requires decisions and tests

1. **Host identity and evidence:** choose an authenticated kernel-peer/agent channel, versioned typed host-capability report, verified source, bounded observation time and state freshness. Host/port ownership requires actual socket/service state. This is not a request for an arbitrary root command facility.
2. **Actor identity:** Symfony must authenticate the user, resolve organization/tenant ownership and resource rights, enforce delegation/plan quotas and optionally reauthenticate sensitive operations (administrator MFA remains optional). Never let a client choose a role or assert tenant permissions in a request.
3. **Artifact policy:** independently authenticate publisher/catalog metadata and pinned package/image provenance; a SHA string in a fixture is not a verified artifact. Free native installation must not require Hub entitlement.
4. **Planning versus applying:** a preview is informational. A future apply contract must re-evaluate **current** actor, policy, job revision, host capabilities, image/manifest digest, ports and quotas under locking/fencing. Prevent TOCTOU, confused-deputy cross-host requests and retry/replay across tenants. Real DB/resource locks and typed agent operations belong to their specialist authorities.
5. **Resource isolation:** native PHP/SQL/site storage and container image/volume/network CPU/RAM/PIDs use different resource managers; no cross-engine fallback. Host control-plane ports **8447 FORGE** and **8446 PANEL** are hard-reserved even if a client-supplied fixture omits them.
6. **Privacy and diagnostics:** record only the minimal required actor/host/site IDs, redacted source and effective permissions; never log credentials, installation secrets or full tokens. Hub must not receive client files, SQL credentials or private volume data.

## Security test evidence and remaining blockers

The [39 synthetic preview regression cases](../../../tests/documentation/test_app_center_preview.py) include denial of hostile fields, mismatched host/tenant references, missing scopes and unverified status. These are **offline tests of mock structures**, not real authentication, agent verification, tenant isolation or networking tests. The [32 runtime/VM cases](../13-tests-quality/app-center-engine-gates.md) remain **PLANNED** and must gain independent security/QA approval before an installer ships.

**Required handoff:** Security → API/IPC → Database → QA/VM → Architecture Review → MASTER. Exact TTL, capability-signature scheme, ACL roles, trust anchor, driver and resource budgets are **not invented**. Core Foundation import R1, Symfony/PostgreSQL R2 and first PHP/HTTPS site R4 remain gating prerequisites.
