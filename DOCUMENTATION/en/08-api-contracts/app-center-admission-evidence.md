<!-- forgepanel-doc id=FP-08-APP-EVIDENCE revision=2 status=specified -->
# App Center — evidence binding, revision and freshness before installation

[Français](../../fr/08-api-contracts/app-center-admission-evidence.md) · [API contracts](README.md) · [Q180/Q220 configuration rules](../02-architecture/app-center-config-inheritance.md) · [Security boundary](../10-security/app-center-admission-trust-boundary.md)

**SPECIFIED CANDIDATE / NOT IMPLEMENTED / REAL TESTS NOT EXECUTED.** The owner's approved Q180 and Q220 require inherited configuration, authorization and secure application of changes. This contract proposes strict, **separate** host/authorization/policy/request evidence for App Center. It is not a real authenticated IPC protocol, active Symfony voter, production API, Go agent, signature verifier or installation authorization.

## Four independent input authorities

| Evidence | Future authoritative producer | Candidate checks | Never sourced from |
|---|---|---|---|
| **Host observation** | Authenticated and bounded local Go agent, scoped to server | Host ID, observed version, measured free capacity, available qualified runtime drivers, protected/listening ports, observation time/freshness | User browser, Hub catalog, billing entitlement |
| **Core authorization** | Authenticated Symfony Core, effective tenant/actor/site RBAC | Actor, tenant, host, site rights, distinct native/container plan scope, authority revision and lifetime | Linux host probe, user-supplied role, Hub metadata |
| **Core effective policy** | Versioned Core Configuration Center under local authorization | Host, policy revision, allowed runtime family, qualified driver list, effective inherited ceilings and policy freshness | Hub publisher setting, plan text in a browser, unsigned recipe |
| **Client install intent** | Untrusted browser/API request, normalized by Core | References host/tenant/actor/site, chosen recipe family and driver, expected revisions, requested resources and host ports, request idempotency reference | Never evidence of an actor role or real host capacity |

A metadata envelope can match host/tenant IDs and revision numbers, **but equality alone cannot authenticate any source**. The final Core integration must independently establish the Unix peer or remote-agent identity, bind it to the target host, verify the user's current session/permissions, validate origin/signature and use a trusted monotonic policy/revision and timestamp strategy. Native One-Click remains free of Hub entitlement and Docker/Podman; Container Apps has its own resource policies and driver qualification.

## Candidate requirements and trust gates

| ID | Proposed boundary before APPLY |
|---|---|
| EVID-FP-0001 | Provenance must come from separately authenticated host observation, Symfony authorization and Core effective policy, not client-submitted JSON |
| EVID-FP-0002 | Every actor, tenant, site and host reference must match trusted sources and resource ownership must be checked server-side |
| EVID-FP-0003 | Host snapshot, RBAC context and policy version/expected revision must be independently compared and protected against replays |
| EVID-FP-0004 | Observation/policy lifetimes and clock skew policy are bounded, but **exact TTL and trusted clock strategy remain OPEN** |
| EVID-FP-0005 | A stale, missing, future-dated, conflicting or unverified source fails closed; do not infer success from its JSON format |
| EVID-FP-0006 | Native and container permissions are distinct, with no fallback or cross-engine resource interpretation |
| EVID-FP-0007 | Docker/Podman drivers and capacity measurements must be qualified on the actual server; a Docker-only package never proves Podman support |
| EVID-FP-0008 | FORGE HTTPS port **8447** and PANEL HTTPS port **8446** cannot be allocated to applications, even when a client omits them |
| EVID-FP-0009 | Host port exposure and resource reservation require separate signed/reviewed local policy and atomic host-side checks |
| EVID-FP-0010 | A preview response is **never** an APPLY grant, Linux job, capability token, signed approval or evidence of completed installation |
| EVID-FP-0011 | APPLY must re-check current identity/policy/capacity, acquire DB/resource fences and record idempotent durable jobs; this is **not yet implemented** |
| EVID-FP-0012 | Core keeps the customer data and Linux authority; publisher Hub cannot replace host observations, Core RBAC or the no-premium native policy |

**No generic `shell.exec` API** or unreviewed remote command is permitted. Neither a syntactically valid SHA-256 nor a plausible localhost snapshot proves signature/trust. A future idempotency key must be stored atomically with the canonical request digest; this candidate merely validates key syntax.

## Standalone synthetic reference code

The [strict synthetic-only JSON Schema](../../../evidence/app-center-admission.synthetic-v1.schema.json) describes the four source envelopes with explicit allowlists and no unknown fields. It is an illustrative *schema for fake test data*, **not an approved IPC wire schema or signature verifier**. The [offline reviewer](../../../scripts/check_app_center_candidate_evidence.py) reads two **bundled fictional** [native](../../../evidence/app-center-fixtures/admission-native.synthetic.json) and [container](../../../evidence/app-center-fixtures/admission-container.synthetic.json) JSON records. Each uses a fixed **fictional clock**, explicitly `SYNTHETIC_UNVERIFIED` host/AuthZ/config evidence and `UNTRUSTED_CLIENT_FIXTURE` intent. Their dates, revisions, CPU/RAM values and identity strings are **QA examples, not product defaults or real evidence**.

```sh
python3 scripts/check_app_center_candidate_evidence.py --fixture native
python3 scripts/check_app_center_candidate_evidence.py --fixture container
python3 tests/documentation/test_app_center_evidence_binding.py -v
```

The pure reviewer verifies strict field/types, illustrative timestamp windows, same host/tenant/actor/site references, expected revisions, candidate plan scopes, native/container capacity separation and reserved ports. It emits only `MATCHES_SYNTHETIC_CONTEXT_ONLY` or `BLOCKED_SYNTHETIC`. Every result retains `actor_authenticated=false`, `host_identity_verified=false`, `policy_signature_verified=false`, `authorization_approved=false`, `resource_reservations_created=false`, `execution_allowed=false`, `apply_available=false`. A matching result **is not an authorization**. No network, OS probe, disk write, SQL, Docker, Podman, TLS or privileged action occurs.

Tests of forged sources, outdated snapshots, replayed revisions, other-tenant targets, unknown fields, privileged commands and port collisions are **offline unit checks only**. The separate [real-runtime qualification matrix](../13-tests-quality/app-center-evidence-gates.md) remains **PLANNED / NOT EXECUTED**.

## Hand-off and unresolved technical decisions

- **Security:** real peer authentication and anti-replay, signed provenance/trust roots, clock/TTL/nonce threat model, tenant isolation and privilege separation.
- **API/IPC:** versioned typed `observeCapabilities`, `readEffectivePolicy`, `planInstall` and eventual separately approved `applyInstall`; no unconstrained shell, no direct Hub instructions to Go.
- **Database:** immutable approved policy revisions, signed snapshot references (if selected), durable idempotency, resource ownership, locks and fencing; **no tables or migrations are approved here**.
- **QA/DevOps:** live PHP/site, SQL, Docker/Podman driver, port/snapshot consistency, firewall and backup/recovery tests on named OS/VM; the genuine Foundation source R1 and Symfony/PostgreSQL R2 must first be integrated.
- **Hub:** optional signed/versioned catalog metadata only, not host-resource or tenant-role evidence. Core remains usable without it.

Exact TTL, signing algorithm, transport, resource thresholds, registered roles, OS/driver versions, cost, public API names and response error codes remain **OPEN** pending specialist review. Q1–Q220 owner decisions stay intact; Q221+ are unanswered.
