# ForgePanel App Center — non-privileged Linux host hints

This independent **Go standard-library-only** tool reads narrowly allowlisted local OS facts. It is preparatory code for App Center's future authorized host-capability service, **not** an imported Foundation Core component, trusted Go agent, Symfony integration, approved Docker/Podman provider or installer.

Run from this directory with Go 1.23:

```sh
GOTOOLCHAIN=local GOPROXY=off GOSUMDB=off go test ./...
GOTOOLCHAIN=local GOPROXY=off GOSUMDB=off go test -race ./...
GOTOOLCHAIN=local GOPROXY=off GOSUMDB=off go vet ./...
GOTOOLCHAIN=local GOPROXY=off GOSUMDB=off go run ./cmd/forgepanel-app-center-observe
```

The command accepts **no arguments**. It makes bounded reads of `/proc/meminfo`, `/sys/fs/cgroup/cgroup.controllers`, and four fixed **visible cgroup-v2 mount-root files** (`cpu.max`, `memory.max`, `memory.current`, `pids.max`); it examines only fixed Docker/Podman binary paths with `lstat` and reports a process-visible CPU count hint. It never invokes those programs, touches sockets, runs a subprocess, makes HTTP/DNS calls, writes files or uses root privileges.

### Critical interpretation

- `logical_cpu_count_hint` is **not a tenant CPU budget**. `memory_available_bytes_hint` is the kernel's current `MemAvailable` metric, **not** a cgroup-adjusted, reserved or safely allocatable amount.
- A cgroup-v2 controller file **does not** prove a tenant is confined, permitted to use a controller or subject to enforceable quotas.
- `visible_cgroup_root` contains **mount-root tokens only**, parsed as `NUMERIC_TOKEN_UNVERIFIED`, `MAX_TOKEN_UNVERIFIED`, `INVALID_TOKEN` or `NOT_OBSERVED` (plus a bounded CPU quota/period value when parseable). Namespace and parent limits can change what actually applies to a process or tenant. The root mount's `max` **does not prove unbounded tenant resources** and numeric limits **do not establish allocatable CPU/RAM/PIDs**. No cgroup v1 or tenant-specific enforcement is assessed. See the [Linux kernel cgroup v2 specification](https://www.kernel.org/doc/html/latest/admin-guide/cgroup-v2.html).
- Docker/Podman binary/symlink presence **does not** prove a functioning rootless engine, compatible Compose provider or qualified application stack. `qualified_container_drivers` is always empty.
- The result is **unsigned and unauthenticated** and must not be used as direct Core host/RBAC evidence. No actor, tenant, site, trusted host identity or policy revision is claimed.
- `host_identity_verified`, `actor_authorization_verified`, `host_capacity_budget_verified`, `cgroup_limits_enforced`, `container_runtime_tested`, `report_signed`, `linux_execution_authorized` and `install_apply_available` are always `false`.

The module includes **34 offline Go unit-test functions**, including 15 additional cgroup-token parser and error-injection cases. CI checks Go formatting, race safety, vetted CLI arguments and false-claim invariants.

Reports may contain infrastructure characteristics; keep them local or share through an authorized/redacted channel. This code requires independent Security/API/IPC/Database/QA review before any authenticated Core integration.

The free native **ONE-CLICK INSTALL** remains independent of Docker, Podman and publisher Hub. **CONTAINER APPS** requires separately verified driver, resources and tenant rights. FORGE HTTPS **8447** and PANEL HTTPS **8446** remain protected.

[EN specification](../../DOCUMENTATION/en/14-devops-releases/app-center-host-observation.md) · [FR specification](../../DOCUMENTATION/fr/14-devops-releases/app-center-host-observation.md) · [Tracking issue #54](https://github.com/yyogas/forgepanel/issues/54) · [Cross-domain issue #55](https://github.com/yyogas/forgepanel/issues/55).
