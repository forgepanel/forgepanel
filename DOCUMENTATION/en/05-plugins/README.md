<!-- forgepanel-doc id=FP-05 revision=1 status=documented -->
# Plugins and trust boundaries

[Français](../../fr/05-plugins/README.md) · [Index](../README.md)

No plugin loader, marketplace, signed catalog or third-party plugin is implemented in SRC-03. Wizard module checkboxes do not install plugins. This chapter specifies requirements; it does not describe an available extension API.

## Proposed contract

A future manifest must declare publisher identity, plugin ID/version, compatible core/API versions, dependencies, entry points, requested capabilities, migrations, resource limits, update origin and data-retention/uninstall behavior. A signature establishes the publisher/artifact relationship, not the safety of its code. The exact schema remains to be designed and versioned.

Trusted in-process Symfony extensions share the application's trust boundary; a manifest cannot prevent arbitrary PHP from accessing that process's privileges. Untrusted code requires a separately designed isolation boundary and narrow authenticated APIs. Neither model receives root access automatically. User-provided templates, scripts and hooks are executable inputs, not harmless configuration.

## Lifecycle and acceptance

Installation stages and verifies the artifact without activating it. Activation requires dependency and permission review. Upgrades require migration and recovery plans; deactivation stops new work while preserving data. Removal explicitly distinguishes code removal from customer data deletion. Dependency failures or malicious requests must not prevent the core from starting or recovering.

Acceptance requires capability-denial tests, signature/integrity failures, version incompatibility, dependency-cycle detection, interrupted migration and safe removal tests. Audit records include actor, plugin identity, approved permissions, artifact identity and outcome; secrets are excluded.

ForgePanel-Hub is now specified in the private `yyogas/forgepanel-hub` repository as an optional detached publisher extension. **No compatible plugin loader or activated Hub plugin exists yet.** Private catalog, license or billing services are not yet approved components. If introduced, their credentials, signing authority and operational data stay outside the public repository; only versioned integration contracts belong here. No marketplace purchase, service account or plugin publication is authorized by this documentation.

[Native modules](../04-modules/README.md) · [Security](../10-security/README.md) · [Release gates](../14-devops-releases/README.md)
