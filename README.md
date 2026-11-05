# ForgePanel

**The Modern Linux Server Control Panel**  
Modern • Secure • Modular • Scalable

[Français](README.fr.md) · [Documentation](DOCUMENTATION/README.md) · [Project status](DOCUMENTATION/en/00-project-control/status.md) · [Changelog](CHANGELOG/CHANGELOG.md)

## What this repository contains

The documentation and governance foundation for ForgePanel. The repository was empty when inspected on 2026-11-05. Foundation v0.6/v0.7 source archives supplied in the project conversation were inspected separately; they have **not been imported as application source** in this documentation change. Their archive names are not GitHub releases.

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

Run documentation checks with `python3 scripts/check_documentation.py`. Application tests documented for the supplied archives require those sources; they are not runnable from this documentation-only repository.

Workflow: `features/*` → `develop` → `stable` → `main` → `production`. A branch name is not evidence of deployment. License selection remains an owner decision; this change grants no new software license.
