<!-- forgepanel-doc id=FP-14-APP-HOST-HINTS revision=2 status=specified -->
# App Center — read-only Go host facts, not trusted capacity

[Français](../../fr/14-devops-releases/app-center-host-observation.md) · [DevOps](README.md) · [Source](../../../tools/app-center-host-probe/README.md)

**Status: STANDALONE SOURCE PROTOTYPE; CORE INTEGRATION NOT IMPLEMENTED.** This Go 1.23 standard-library tool is source that can run **unprivileged** on a Linux system to read OS facts. It is not the Foundation v0.7 source import, a trusted Go agent, an authenticated Symfony API, an approved install planner, a configured OS service or a production release.

## Observed facts versus verified capabilities

| Observation field | Source and meaning | What it does NOT establish |
|---|---|---|
| `logical_cpu_count_hint` | Go process-visible logical CPU count | cgroup CPU quota, CPU millicores available to a tenant, reservation or enforceable limit |
| `memory_total_bytes_hint`, `memory_available_bytes_hint` | Bounded parse of exact `MemTotal`/`MemAvailable` lines in `/proc/meminfo` | tenant RAM entitlement, available container budget, atomic reservation or OOM-safe allocation |
| `cgroup_v2_controllers` | Read-only `/sys/fs/cgroup/cgroup.controllers` token listing | controllers actually delegated to a tenant, enforcement or supported rootless configuration |
| `docker_binary_candidate` / `podman_binary_candidate` | `lstat` of fixed known executable paths only; differentiates files, symlinks, absence and errors | installed/available/healthy Docker or Podman runtime, socket, Compose provider or image compatibility |

Reads are bounded; no caller can choose a path or issue a command. The tool never executes Docker/Podman, opens their sockets, runs shell, asks the network, modifies firewall/ports, reads tenant files or requires elevated privileges. Incomplete/malformed evidence is labeled `INCONCLUSIVE` or `NOT_OBSERVED`, with fixed redacted warning codes. Non-Linux returns `NOT_APPLICABLE`. This CLI does not enumerate applications or installed customer data.

All output reports `driver_qualification=NOT_EXECUTED`, `qualified_container_drivers=[]` and **false** for host identity, actor authorization, enforceable budget, cgroup limits, container runtime test, signed report, Linux execution and install apply availability. A binary symlink is only `SYMLINK_UNVERIFIED`, not permission to start a container.

### Additional cgroup-v2 visible-root tokens (still untrusted)

The observer now also reads **four fixed files in the visible cgroup mount root**: `cpu.max`, `memory.max`, `memory.current`, and `pids.max`. It parses the Linux kernel's two-field CPU quota/period tokens and `max`/numeric memory and process tokens, with bounded 128-byte reads, strict decimal syntax and redacted errors. <https://www.kernel.org/doc/html/latest/admin-guide/cgroup-v2.html>

The nested `visible_cgroup_root` object reports raw **hints**, such as `cpu_quota_state=NUMERIC_TOKEN_UNVERIFIED` or `memory_max_state=MAX_TOKEN_UNVERIFIED`, never an effective container or tenant limit. Files at a *visible mount root* may be missing or unrelated to the process/tenant under namespaces and hierarchical cgroups. **Do not calculate "free allocatable CPU/RAM/PIDs" from these values**, turn a `max` token into guaranteed available resources, or use this output to authorize installation. `cgroup_limits_enforced` remains **false** even when a numeric token is observed. Cgroup-v1 and actual tenant-scoped delegated control groups are **not qualified by this probe**.

## Code, tests and CI

[Go source and README](../../../tools/app-center-host-probe/README.md) · [Go unit test source](../../../tools/app-center-host-probe/probe/probe_test.go) · [Dedicated CI](../../../.github/workflows/app-center-host-probe.yml).

The module uses injectable filesystem readers and fixed paths; 35 offline Go tests cover malformed/oversized meminfo, integer overflow, cgroup parsing, symlink/executable/failed binary inspection, missing Linux facilities, no secret leakage, strict paths and no privilege claims. The CI additionally runs `go test -race`, `go vet`, `gofmt` checking, no-argument refusal and an actual runner's JSON **invariant check only**. A GitHub Actions runner is **not** an authorized ForgePanel customer server, OS certification or Docker/Podman qualification.

## Blocking integration decisions

- Authenticated local peer and host identity must be defined in the [typed Go IPC contract](../08-api-contracts/symfony-go-ipc-r3.md); report provenance/signatures/expiry and anti-replay remain OPEN.
- The [four-source admission contract](../08-api-contracts/app-center-admission-evidence.md) must bind **trusted** host facts to independently validated Symfony actor/tenant/site RBAC, current Core policy revision and untrusted user intent. This raw CLI report is **never directly trusted**.
- Reserve true CPU/RAM/PIDs/volumes and protected **FORGE 8447** / **PANEL 8446** ports under separately reviewed capability and transaction/locking contracts. Raw `MemAvailable` must **never** be interpreted as available allocatable customer quota.
- The native free **ONE-CLICK INSTALL** works without Docker/Podman or Hub. **CONTAINER APPS** remains a distinct qualified runtime family. Do not merge recipe types or bypass owner Q1–Q220 decisions.

**Remaining:** genuine Foundation source import #2, real Symfony/PostgreSQL #3, authenticated Go agent/IPC, versioned DB and real OS/VM/tenant tests. The existing [12 admission tests](../13-tests-quality/app-center-evidence-gates.md) remain **PLANNED, not PASS**. The standalone probe does not remove those requirements.
