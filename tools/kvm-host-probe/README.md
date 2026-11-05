# ForgePanel KVM Host Probe — preparatory standalone tool

Nonprivileged, read-only, independent Go 1.23+ module under `tools/kvm-host-probe/`. This is **not the Foundation Core**, a KVM runner, an installer or a production certification. It is preparatory work under Q151 A and Q161 C without bypassing R1/R2.

```sh
GOTOOLCHAIN=local GOPROXY=off go test ./...
GOTOOLCHAIN=local GOPROXY=off go test -race ./...
GOTOOLCHAIN=local GOPROXY=off go vet ./...
GOTOOLCHAIN=local GOPROXY=off go run ./cmd/forgepanel-kvm-probe
```

The executable only reads fixed Linux metadata: `/etc/os-release`, `/proc/cpuinfo` and `lstat` for `/dev/kvm` and `/sys/module/kvm`. No network, shell commands, filesystem writes, kernel ioctl, device opening or host identity collection. It prints JSON to stdout.

**Always** reports `qualification=NOT_EXECUTED`, `vm_executed=false`, `vm_image_pinned=false`, `resource_quotas_verified=false`, `snapshot_tested=false`, `failure_recovery_tested=false` and `report_signed=false`. A KVM device and CPU flag observation makes a host a **candidate for later isolated VM tests**, not a certified platform. The current user's ability to open the KVM device is **not** checked. Non-x86 architecture and unreadable metadata are INCONCLUSIVE.

[French specification](../../DOCUMENTATION/fr/14-devops-releases/kvm-host-probe.md) · [English specification](../../DOCUMENTATION/en/14-devops-releases/kvm-host-probe.md)

The historical Foundation v0.7 source ZIP remains unavailable; no original application source has been imported. No coupling to private ForgePanel-Hub.

## Pinned QCOW2 image admission (pre-execution)

A second standalone command is available: `go run ./cmd/forgepanel-kvm-image-admit /private/absolute/policy.json /private/absolute/request.json`. The JSON documents must be private (0600), owned by a nonroot local lab user, strictly conform to the [policy](schemas/policy.v1.schema.json), [request](schemas/request.v1.schema.json) and [result](schemas/result.v1.schema.json) contracts. The disk image must be a private regular, non-executable, non-symlinked `.qcow2` file in a private owned directory; its full SHA-256 must match the request.

No default vCPU, memory, time or disk limits are set. The local lab's **explicit** policy numbers are only admission bounds; they do **not enforce** real VM quotas. Guest network, host shares and privilege requests are always refused. Output is `BLOCKED` or `REVIEW_REQUIRED` and always `qualification=NOT_EXECUTED`; no QEMU guest is booted and no signed evidence is produced. The QCOW2 header check is **not** full format validation and a future launcher must revalidate/pin exact bytes at run time.

[FR specification](../../DOCUMENTATION/fr/14-devops-releases/kvm-image-admission.md) · [EN specification](../../DOCUMENTATION/en/14-devops-releases/kvm-image-admission.md). The historical Foundation Core archive remains absent and the private Hub is not involved.

### Verification before accepting a lab image

From the module root, run `GOTOOLCHAIN=local GOPROXY=off GOSUMDB=off go test ./...`, `go test -race ./...` and `go vet ./...`. These tests exercise **synthetic** QCOW2-like files only. The three versioned JSON schemas are checked for parity with Go wire fields. Any positive admission is for **manual review only**, and must be followed by independent policy/provenance authorization and re-verification at the eventual execution boundary; no VM can be started from this tool.
