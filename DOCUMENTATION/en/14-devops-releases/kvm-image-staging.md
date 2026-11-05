<!-- forgepanel-doc id=FP-14-KVM-IMAGE-STAGING revision=1 status=specified -->
# R3 — Private verified copying of local test images

[Français](../../fr/14-devops-releases/kvm-image-staging.md) · [QCOW2 admission](kvm-image-admission.md) · [KVM host observation](kvm-host-probe.md) · [Roadmap](../00-project-control/implementation-roadmap.md)

## Scope and readiness

The standalone `tools/kvm-host-probe/staging/` library and `forgepanel-kvm-image-stage` CLI prepare **one private copy** of an already SHA-256-admitted QCOW2 image (Q151 A, Q161 C). They do not boot any guest or implement an isolated runner, installer, or plugin. Historical Foundation v0.7 source import remains blocked (issue #2), and the tool is separate from Core runtime and ForgePanel-Hub.

A positive `STAGED_FOR_MANUAL_REVIEW` means **only** that the staged bytes matched the pinned digest at inspection time. The result always states `qualification=NOT_EXECUTED`, `manual_review_required=true`, `execution_authorized=false`, `immutable_storage_verified=false`, `resource_quotas_enforced=false`, `vm_executed=false`, and `report_signed=false`.

## Processing contract

1. CLI requires **three absolute paths**: private policy JSON, private request JSON, and a private staging-parent directory. Policy and request retain existing [R3 policy](../../../tools/kvm-host-probe/schemas/policy.v1.schema.json) and [request](../../../tools/kvm-host-probe/schemas/request.v1.schema.json) contracts. No CPU/RAM/duration defaults are invented.
2. Existing admission checks request syntax, explicit policy bounds, image SHA-256 and denial of network/host shares/privilege requests. Staging requires a **nonroot** Linux amd64 account, separate nonnested canonical source and destination directories, both private (0700), owned by that account.
3. Copy uses Linux descriptor-relative `openat`/`O_NOFOLLOW`, exclusively creates a **new** `<parent>/<run_id>` directory (0700), and makes `image.qcow2` read-only (0400) after write/sync. The source must be private, owned, regular, not executable, no symlink and no extra hardlink. No existing file or run is overwritten.
4. Source bytes are **re-copied and SHA-256 checked** against the request; source inode/size/change metadata is rechecked, then the staged copy is **reopened and SHA-256 verified** independently. Any drift fails closed.
5. Private `stage-receipt.json` (0400) records image, policy and request digests, run identity, policy revision, requested CPU/RAM/duration, image size and all nonexecution flags. [Versioned result schema](../../../tools/kvm-host-probe/schemas/stage-result.v1.schema.json). It is **unsigned** and does not establish durable immutability.

## Run only as an unprivileged lab user

```bash
cd tools/kvm-host-probe
GOTOOLCHAIN=local GOPROXY=off GOSUMDB=off go run ./cmd/forgepanel-kvm-image-stage \
  /private/policy.json /private/request.json /private/staging-root
```

The `staging-root` parent must **already exist with 0700 permissions** under the lab user's ownership; both input JSON files must be private (0600), and the source image in its own private directory. CLI rejects root, shared/symlinked directories, relative paths, unsafe options, modified images, invalid limits, existing `run_id` and nested source/staging roots.

## Failure and truthfulness

Failures **before directory creation** return `BLOCKED` without copied files. Failures **after creation** return `PARTIAL_STAGE_REQUIRES_MANUAL_CLEANUP`: a private partial directory is preserved for inspection and **never automatically recursively deleted** (avoids deleting a substituted unrelated directory). An isolated receipt must not authorize a VM; recheck exact bytes at the future launch boundary. Mode 0400 **is not immutable storage**: the same Unix UID can later change modes and bytes.

## Tests and remaining gates

**21 new synthetic Go test functions** cover correct copies, overwrite/unsafe path denial, source mutation, partial failures, private CLI inputs, JSON contract parity and false-certification prevention, bringing the standalone module to **62 Go test functions**. Use `go test ./...`, `go test -race ./...`, `go vet ./...`, `gofmt -l .`; GitHub CI establishes evidence for a specific commit.

**Not implemented**: QEMU/KVM runner or guest boot, full QCOW2 structural verification, publisher signing trust, operator authorization, sandbox/real cgroups and enforced quotas, snapshots, faults/recovery, ephemeral guest cleanup, signed Q152 qualification reports, immutable Q162 private store, OS certification, or Q166 backup restoration. These remain tracked in [issue #42](https://github.com/yyogas/forgepanel/issues/42) under Q132 hard vetoes. No licensing policy, open Q171+ settings, or unknown numeric value is implicitly approved.
