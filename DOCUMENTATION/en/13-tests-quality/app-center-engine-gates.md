<!-- forgepanel-doc id=FP-13-APP-CENTER revision=2 status=specified -->
# App Center — native versus container qualification matrix

[Français](../../fr/13-tests-quality/app-center-engine-gates.md) · [QA](README.md) · [App Center contract](../06-apps-recipes/app-center-engines.md)

**Every test below is PLANNED, not PASS.** No working native app installer or Docker/Podman app executor is included in current Core source. Documentation/schema checks cannot certify deployment.

## ONE-CLICK INSTALL — free native test gates

| Test ID | Scenario | Expected |
|---|---|---|
| TEST-APP-NAT-0001 | Install native WordPress into an authorized PHP-FPM/SQL site | Succeeds without Docker/Podman, Hub license or payment |
| TEST-APP-NAT-0002 | Hub unavailable / offline installation | Free native install still works from trusted local catalog |
| TEST-APP-NAT-0003 | Site manager targets another organization's website | Server-side denied |
| TEST-APP-NAT-0004 | Unsupported PHP/WebStack/extension or disallowed EOL | Reject before mutation with explanation |
| TEST-APP-NAT-0005 | Tampered archive, untrusted origin or unapproved version | Provenance/integrity rejection |
| TEST-APP-NAT-0006 | Traversal or symlink into another tenant | Denied by typed filesystem operations |
| TEST-APP-NAT-0007 | DB name collision, disk/inode/PHP quota exceeded | Impact plan, safe refusal |
| TEST-APP-NAT-0008 | Duplicate requests / interruption during extract, DB and config | Durable idempotency, recovery state |
| TEST-APP-NAT-0009 | Partly irreversible SQL migration during app update | Consistent backup and warning; no false rollback guarantee |
| TEST-APP-NAT-0010 | Uninstall involving files/SQL/backups | Explicit retention choice and audit |
| TEST-APP-NAT-0011 | Command/path injection in configuration and permission changes | No generic shell, only bounded typed operations |
| TEST-APP-NAT-0012 | Third-party app has commercial license | License information shown; free engine ≠ free proprietary app |

## CONTAINER APPS — container-specific gates

| Test ID | Scenario | Expected |
|---|---|---|
| TEST-APP-CTR-0001 | Neither Docker nor Podman installed | No implicit runtime install or native conversion |
| TEST-APP-CTR-0002 | Qualified Docker and compatible manifest | Deploy only with verified policy/resources |
| TEST-APP-CTR-0003 | Qualified Podman, Docker Compose not qualified | Reject; do not assume feature parity |
| TEST-APP-CTR-0004 | Unknown/mutable image or required digest/signature absent | Reject according to artifact trust policy |
| TEST-APP-CTR-0005 | Host-root/Docker socket mount, privileged/host network, unsafe `provider`, `include` or unauthorized secret file references | Denied by default, including Compose imports |
| TEST-APP-CTR-0006 | Host port collision with FORGE 8447, PANEL 8446 or website | Reject without changing listeners |
| TEST-APP-CTR-0007 | CPU/RAM/PID/image/volume quotas exceeded | Reject before apply or tested compensation |
| TEST-APP-CTR-0008 | Multi-service app with DB/volumes/network | Verify dependencies, secrets, startup order and health |
| TEST-APP-CTR-0009 | Native-site actor lacking container scope invokes container API | Server/agent denial |
| TEST-APP-CTR-0010 | Image upgrade with failed persistent data migration | Keep volumes, explicit recovery |
| TEST-APP-CTR-0011 | Uninstall containers and volumes | Separate data/volume/backup retention choices |
| TEST-APP-CTR-0012 | Network/image-space failure or partial stack start | Observed status, retries/recovery; never false SUCCEEDED |

## Cross-engine gates

| Test ID | Scenario | Expected |
|---|---|---|
| TEST-APP-X-0001 | Same app offered natively and in containers | Separate compatible recipes, identities, requirements and upgrades |
| TEST-APP-X-0002 | Native request with \`container_stack\` recipe or vice versa | Type rejection before resource allocation |
| TEST-APP-X-0003 | Local install/removal while Hub unavailable | Free Core usable; no mandatory commerce rights |
| TEST-APP-X-0004 | Unapproved partner catalog or unsigned artifact | Never executable, even if draft item is visible |
| TEST-APP-X-0005 | Automatic conversion from native hosting to containers | Reject without dedicated migration workflow |
| TEST-APP-X-0006 | Logs/events/diagnostics after failures | No secrets; correct actor/tenant/job/digest audit |
| TEST-APP-X-0007 | Copy 1Panel/Softaculous materials without license/provenance | Block publishing until legal review |
| TEST-APP-X-0008 | Empty catalog or disabled/unavailable engine | Clear UI state; other Core services unaffected |

## Required evidence

To mark \`VERIFIED\`, name exact commit, OS/version, WebStack/PHP or Docker/Podman version, manifest/digest, tenant/permissions, measured resources and recovery result. Exercise positive **and** negative multitenant cases on real VMs. Static checks do not certify runtime deployment.

All Q1–Q170 decisions remain in force. The detailed technical mechanisms and sequencing require specialist reviews without invented PASS results.
