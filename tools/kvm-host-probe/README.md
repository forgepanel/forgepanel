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
