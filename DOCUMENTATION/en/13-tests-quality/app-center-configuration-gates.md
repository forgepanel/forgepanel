<!-- forgepanel-doc id=FP-13-APP-CONFIG revision=2 status=specified -->
# App Center Configuration Center — real-runtime acceptance gates

[Français](../../fr/13-tests-quality/app-center-configuration-gates.md) · [QA](README.md) · [Inheritance specification](../02-architecture/app-center-config-inheritance.md) · [Q180/Q220](../00-project-control/decisions-q171-q220.md)

**PLANNED / NOT EXECUTED.** These are 16 additional specialist acceptance scenarios for the future Configuration Center under owner-approved Q180/Q220. They do NOT replace the 50 decision-level planned tests or mean the Python fixture has implemented any product functionality.

| ID | Family | Required observable result | Status |
|---|---|---|---|
| TEST-CONFIG-FP-0001 | Inheritance and provenance | Real global→server→organization→plan→site policy reads correctly with actor/scope audit | PLANNED |
| TEST-CONFIG-FP-0002 | No widening of parent policy | Site cannot re-enable containers blocked by parent plan | PLANNED |
| TEST-CONFIG-FP-0003 | Physical quota enforcement | Tenant/site may never exceed observed host CPU/RAM/PIDs/storage even if configured higher | PLANNED |
| TEST-CONFIG-FP-0004 | Immutable native-free Core policy | No premium entitlement, Docker/Podman, Hub connectivity or commercial billing required for native engine | PLANNED |
| TEST-CONFIG-FP-0005 | Immutable Linux security controls | RBAC, tenant isolation, typed Go operations, signatures and port controls cannot be disabled by settings | PLANNED |
| TEST-CONFIG-FP-0006 | Revision and concurrency | Competing edits with stale expected revisions are rejected and audited | PLANNED |
| TEST-CONFIG-FP-0007 | Effective policy explanation | UI shows inherited sources, override eligibility, impact and lock reasons without exposing secrets | PLANNED |
| TEST-CONFIG-FP-0008 | Tenant privilege separation | A PANEL site manager cannot alter FORGE/global, host, unrelated tenant or private Hub settings | PLANNED |
| TEST-CONFIG-FP-0009 | Trusted host capability provenance | Host facts come from authenticated bounded agent with freshness/host binding, never client request | PLANNED |
| TEST-CONFIG-FP-0010 | Plan vs apply isolation | Read-only simulation never allocates ports, runs jobs, mutates SQL/files or launches container | PLANNED |
| TEST-CONFIG-FP-0011 | Q47 guarded apply | Plan validates dependencies, snapshot, actor approval, health and recover/compensate state | PLANNED |
| TEST-CONFIG-FP-0012 | Port collision and recovery | FORGE port 8447 and PANEL port 8446 stay reserved; listener changes preserve fallback access | PLANNED |
| TEST-CONFIG-FP-0013 | Signature and catalog policy | Unknown/signed-but-unreviewed recipe cannot bypass native/container policy or partner review | PLANNED |
| TEST-CONFIG-FP-0014 | Optional consent/telemetry | Hub communication opt-ins separate and withdrawal does not block free native Core | PLANNED |
| TEST-CONFIG-FP-0015 | Scope extension contract | Optional account/user presentation overrides cannot weaken server/plan safety or cross tenant boundaries | PLANNED |
| TEST-CONFIG-FP-0016 | Rollback under partial failure | Versioned config recovery discloses irreversible operations, preserves data and records partial outcomes | PLANNED |

## Evidence required

Each PASS must cite exact Core/Go/PostgreSQL commit, owner/tenant/actor, OS and actual server capabilities, policy revisions, denial and success paths, locks, redacted audit, backup/restore or non-destructive recovery and an independent review. SKIP/BLOCKED cannot be treated as PASS. Native One-Click must stay free with no Hub dependency; real Docker/Podman engine authorization stays separate. None of these tests was run against a real app, TLS listener, tenant or VM.
