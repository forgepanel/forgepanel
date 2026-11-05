<!-- forgepanel-doc id=FP-14-KVM-HOST-PROBE revision=1 status=specified -->
# Local QEMU/KVM host observation — R3 preparation tool

[Français](../../fr/14-devops-releases/kvm-host-probe.md) · [Installation and releases](README.md) · [Roadmap](../00-project-control/implementation-roadmap.md) · [Tests](../13-tests-quality/README.md)

## Purpose and gate separation

ForgePanel Core includes a **standalone read-only Go tool**, under `tools/kvm-host-probe/`, preparing owner choices **Q151 A and Q161 C**: qualify local QEMU/KVM systems first, with later ephemeral isolated runners, pinned images, quotas and cleanup. **This tool neither boots a VM nor implements a runner.** It is not part of the historical Foundation v0.7 archive, whose source import remains blocked pending genuine ZIP bytes (R1, issue #2). Decisions Q1–Q170 and Hub separation remain intact.

## Unprivileged usage

```bash
cd tools/kvm-host-probe
GOTOOLCHAIN=local GOPROXY=off go test ./...
GOTOOLCHAIN=local GOPROXY=off go test -race ./...
GOTOOLCHAIN=local GOPROXY=off go vet ./...
GOTOOLCHAIN=local GOPROXY=off go run ./cmd/forgepanel-kvm-probe
```

The tool only inspects **fixed local inputs**: `/etc/os-release` (ID/version), `/dev/kvm` through `lstat` (character device, reject symlinks), `/proc/cpuinfo` (exact VMX/SVM flags on x86), and `/sys/module/kvm` (directory presence). Bounded file reads; no shell, `ioctl`, opening `/dev/kvm`, package installation, writes, network, secret, IP or hostname collection. The output distinguishes unknown facts instead of inventing PASS.

## JSON v1 response contract

Fields `schema_version`, `runtime_os`, `runtime_arch`, `os_id`, `os_version`, `kvm_device`, `cpu_virtualization`, `kvm_kernel_module`, `host_assessment`, `qualification`, `warnings` and explicit booleans represent **observations, not VM certification**. `host_assessment=CANDIDATE_FOR_ISOLATED_VM_TESTS` only means a KVM character device and compatible CPU flags were observed on x86. Other architectures or missing data: `INCONCLUSIVE`; absent or untrusted device: `NO_TRUSTED_KVM_DEVICE`; non-Linux: `NOT_APPLICABLE`.

**Hardcoded truthfulness:** `qualification=NOT_EXECUTED`, `vm_executed=false`, `vm_image_pinned=false`, `snapshot_tested=false`, `resource_quotas_verified=false`, `failure_recovery_tested=false`, `report_signed=false`. Actual permissions to open the device are **not** tested. This output is **unsigned** and is not Q152/Q162 private immutable evidence.

## Verification and missing milestones

**Available now:** 14 synthetic Go unit tests, `go test -race`, `go vet`, symlink/fake-device/flag/read-failure/no-false-certification cases and PR CI. **Not performed:** QEMU/KVM boot, isolated runner, pinned images, CPU/RAM/I/O budgets, cleanup, snapshots, failure injection, signed reports, immutable storage, load/benchmarks, real backup and restore. All remain **future R3/R4 gates** including Q132/Q152/Q161–Q166.

The tool **selects no default first OS** under Q121, proves no supported distribution and permits no exception to Q132 critical vetoes. No privileged Linux operation or Hub dependency. [Q161–Q170 decisions](../00-project-control/decisions-q161-q170.md).
