# ForgePanel

**The Modern Linux Server Control Panel**  
Modern • Secure • Modular • Scalable

[Français](README.fr.md) · [Documentation](DOCUMENTATION/README.md) · [Project status](DOCUMENTATION/en/00-project-control/status.md) · [Changelog](CHANGELOG/CHANGELOG.md)

## What this repository contains

ForgePanel began with a documentation and governance foundation (initially empty on 2026-11-05). **On the dedicated draft R1 source-import branch**, a 66-file Foundation v0.7 source candidate is present with per-file SHA-256 and offline Go/PHP tests; it is **not yet merged, reviewed for final licensing, qualified, released or deployed**. The original historical archives are not GitHub releases. [R1 source import and evidence](DOCUMENTATION/en/12-development/foundation-v07-source-import.md).

**There is no production installer or deployable hosting panel in this repository yet.** Do not run an invented installation URL or mistake a passing documentation check for product certification.

## Product direction

A modular Symfony/PHP control plane with Twig/Symfony UX, a Go system agent, PostgreSQL and least-privilege Linux operations. Multi-distribution design targets Debian 12/13, Ubuntu 24.04/26.04 and AlmaLinux 9/10; Nginx, Apache, Caddy, PHP-FPM and FrankenPHP are planned web-stack components, not certified installations.

## Start here

| Reader | Entry point |
|---|---|
| Project owner | [Scope, decisions and priorities](DOCUMENTATION/en/00-project-control/README.md) |
| AI agent | [Repository instructions](AGENTS.md) |
| Contributor | [Contribution guide](CONTRIBUTING.md) |
| Security reviewer | [Security policy](SECURITY.md) |
| Next implementation task | [Handover and blockers](DOCUMENTATION/en/18-contributing/handover.md) |

Run documentation checks with `python3 scripts/check_documentation.py`. On the source-import branch, additionally run `python3 scripts/check_foundation_import.py`, then `bash scripts/check.sh` for isolated Go/PHP checks. They do not test real Symfony/PostgreSQL or a Linux installer.

Workflow: `features/*` → `develop` → `stable` → `main` → `production`. A branch name is not evidence of deployment. License selection remains an owner decision; this change grants no new software license.
