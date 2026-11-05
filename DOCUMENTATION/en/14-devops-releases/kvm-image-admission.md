<!-- forgepanel-doc id=FP-14-KVM-IMAGE-ADMISSION revision=2 status=specified -->
# R3 — QEMU/KVM image admission before execution

[Français](../../fr/14-devops-releases/kvm-image-admission.md) · [KVM host probe](kvm-host-probe.md) · [Roadmap](../00-project-control/implementation-roadmap.md) · [Tests](../13-tests-quality/README.md)

## Purpose and status

The standalone `tools/kvm-host-probe/admission/` package and `cmd/forgepanel-kvm-image-admit` CLI **read-only** verify the identity of a local QCOW2 disk image and proposed future test parameters. This is a **preparatory security gate**, aligning with Q151 A, Q152 C, Q161 C, Q162 B and Q132 critical vetoes. **It boots no guest, enforces no actual resource quotas, signs nothing and certifies no operating system**. A real ephemeral QEMU/KVM runner must still be implemented/tested on an authorized host. The historical Foundation v0.7 import remains blocked in R1 (issue #2); no Hub dependency.

## Versioned JSON contracts

- [Policy](../../../tools/kvm-host-probe/schemas/policy.v1.schema.json): explicit local lab ID/revision, private image directory, vCPU, memory, duration and image-size bounds. **No invented default values or commercial limits**. An unsigned local policy does not grant execution authority.
- [Request](../../../tools/kvm-host-probe/schemas/request.v1.schema.json): run ID, plain `.qcow2` filename, full lowercase SHA-256, requested CPU/RAM/duration. `network_enabled`, `host_shares_enabled` and `privileged` must all be `false`.
- [Result](../../../tools/kvm-host-probe/schemas/result.v1.schema.json): `BLOCKED` (exit 2) or `REVIEW_REQUIRED` (exit 0), **always `qualification=NOT_EXECUTED`**, and explicit false flags for VM execution, runner isolation, actual quota enforcement, complete QCOW2 parsing, signing and Q132 checks.

## Nonprivileged preparatory usage

```bash
cd tools/kvm-host-probe
# Two private JSON files (0600) conforming to the schemas;
# image inside a canonical private directory (0700) owned by the same non-root user.
GOTOOLCHAIN=local GOPROXY=off go run ./cmd/forgepanel-kvm-image-admit \
  /private/absolute/path/policy.json /private/absolute/path/request.json
```

The CLI denies root, shared/symlinked config files, unknown/oversized/multiple JSON objects, missing limits, unsafe image filenames, quota overruns and network/share/privilege requests. The image directory must be absolute and canonical; the file must be private, owned, regular and non-executable with no symlink or additional hardlink. Linux `openat`/`O_NOFOLLOW` protects the final image path; the tool checks the QCOW2 v2/v3 **header** and computes SHA-256 over **all image bytes**. It does not disclose the private local image path in JSON.

## Remaining trust boundaries

A QCOW2 header is **not full structural validation**. SHA-256 matches bytes to a supplied manifest, **not publisher authenticity, distribution rights or safety of guest content**. Resource bounds are **checked but never enforced by a VM scheduler**. A same-UID process can change files after scanning: a future executor must use an immutable validated object/FD or re-hash bytes at launch. Without a disposable isolated host, disabled network, enforced CPU/RAM/I/O quotas, snapshots, cleanup, fault checks, Q152 signed reports and Q162 immutable private storage, **R3 remains unqualified**. Synthetic QCOW2-like test fixtures are not bootable Linux images and do not select a default first OS.

No generic privileged shell, no Hub connection and no override of Q132 critical failure gates. [Decisions Q161–Q170](../00-project-control/decisions-q161-q170.md).

## Next step: verified private staging

The separate [Image Staging](kvm-image-staging.md) component reopens bytes after admission, copies them into a fresh nonroot directory and verifies the digest. A `STAGED_FOR_MANUAL_REVIEW` receipt may be produced, **never** QEMU launch authorization or proof of immutable storage. Real quotas, snapshots, OS drivers and signing remain future work.
