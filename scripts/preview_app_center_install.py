#!/usr/bin/env python3
"""Offline App Center installation PREVIEW. Never a runtime approval or executor.

Only bundled synthetic fixtures are accepted by this CLI. No API, shell, network,
database, Docker/Podman, file mutation, host inventory or resource reservation.
"""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

from validate_app_center_recipe import (
    FIXTURES, RecipeContractError, load_fixture, validate_recipe,
)

CAPABILITY_KEYS = frozenset({
    "schema_version", "fixture_status", "host_id",
    "php_fpm_available", "native_db_engines",
    "available_container_drivers", "free_cpu_millicores",
    "free_memory_mib", "free_pids",
    "reserved_host_tcp_ports", "observed_bound_host_tcp_ports",
})
AUTHORIZATION_KEYS = frozenset({
    "schema_version", "fixture_status", "host_id", "tenant_id",
    "actor_id", "authorized_site_ids", "container_permission_claimed",
})
REQUEST_KEYS = frozenset({
    "schema_version", "request_status", "host_id", "tenant_id",
    "target_site_id",
    "host_tcp_ports", "hub_available",
})
IDENT = re.compile(r"[a-z][a-z0-9_-]{2,63}\Z")
RESERVED_FORGEPANEL_PORTS = frozenset((8447, 8446))
DB_ENGINES = frozenset(("MYSQL", "MARIADB", "POSTGRESQL"))
DRIVERS = frozenset(("DOCKER", "PODMAN"))


def bounded_port_list(value: object, label: str) -> list[int]:
    if (not isinstance(value, list) or len(value) > 32 or
        any(type(v) is not int or v < 1 or v > 65535 for v in value) or
        len(value) != len(set(value))):
        raise RecipeContractError(f"REJECT_UNREVIEWED_FIELD: invalid {label}")
    return value


def bounded_identifier_list(value: object, label: str) -> list[str]:
    if (not isinstance(value, list) or len(value) > 32 or
        any(not isinstance(v, str) or not IDENT.fullmatch(v) for v in value) or
        len(value) != len(set(value))):
        raise RecipeContractError(f"REJECT_UNREVIEWED_FIELD: invalid {label}")
    return value


def bounded_names(value: object, allowed: frozenset[str], label: str) -> list[str]:
    if (not isinstance(value, list) or len(value) > 8 or
        any(type(v) is not str or v not in allowed for v in value) or
        len(set(value)) != len(value)):
        raise RecipeContractError(f"REJECT_UNREVIEWED_FIELD: invalid {label}")
    return value


def validate_synthetic_inputs(facts: object, authorization: object, request: object) -> None:
    if not isinstance(facts, dict) or set(facts) != CAPABILITY_KEYS:
        raise RecipeContractError("REJECT_UNREVIEWED_FIELD: invalid synthetic facts shape")
    if not isinstance(authorization, dict) or set(authorization) != AUTHORIZATION_KEYS:
        raise RecipeContractError("REJECT_UNREVIEWED_FIELD: invalid synthetic authorization shape")
    if not isinstance(request, dict) or set(request) != REQUEST_KEYS:
        raise RecipeContractError("REJECT_UNREVIEWED_FIELD: invalid synthetic request shape")
    if (type(facts["schema_version"]) is not int or facts["schema_version"] != 1 or
        type(authorization["schema_version"]) is not int or authorization["schema_version"] != 1 or
        type(request["schema_version"]) is not int or request["schema_version"] != 1 or
        facts["fixture_status"] != "SYNTHETIC_UNVERIFIED" or
        authorization["fixture_status"] != "SYNTHETIC_UNVERIFIED" or
        request["request_status"] != "SYNTHETIC_UNVERIFIED"):
        raise RecipeContractError("REJECT_UNAPPROVED_EXECUTION: only synthetic unverified data")
    if not isinstance(facts["host_id"], str) or not IDENT.fullmatch(facts["host_id"]):
        raise RecipeContractError("REJECT_UNREVIEWED_FIELD: invalid host ID")
    for label, value in (
        ("authorization host", authorization["host_id"]),
        ("authorization tenant", authorization["tenant_id"]),
        ("authorization actor", authorization["actor_id"]),
        ("request host", request["host_id"]),
        ("request tenant", request["tenant_id"]),
    ):
        if not isinstance(value, str) or not IDENT.fullmatch(value):
            raise RecipeContractError(f"REJECT_UNREVIEWED_FIELD: invalid {label}")
    bounded_identifier_list(authorization["authorized_site_ids"], "authorized site IDs")
    if (not isinstance(request["target_site_id"], str) or
        not IDENT.fullmatch(request["target_site_id"])):
        raise RecipeContractError("REJECT_UNREVIEWED_FIELD: invalid target site ID")
    bounded_names(facts["native_db_engines"], DB_ENGINES, "database engines")
    bounded_names(facts["available_container_drivers"], DRIVERS, "container drivers")
    for field in ("php_fpm_available",):
        if type(facts[field]) is not bool:
            raise RecipeContractError(f"REJECT_UNREVIEWED_FIELD: invalid {field}")
    if type(authorization["container_permission_claimed"]) is not bool:
        raise RecipeContractError("REJECT_UNREVIEWED_FIELD: invalid authorization scope claim")
    if type(request["hub_available"]) is not bool:
        raise RecipeContractError("REJECT_UNREVIEWED_FIELD: invalid hub flag")
    for field in ("free_cpu_millicores", "free_memory_mib", "free_pids"):
        value = facts[field]
        if type(value) is not int or not 0 <= value < 2**31:
            raise RecipeContractError(f"REJECT_UNREVIEWED_FIELD: invalid {field}")
    for field in ("reserved_host_tcp_ports", "observed_bound_host_tcp_ports"):
        bounded_port_list(facts[field], field)
    bounded_port_list(request["host_tcp_ports"], "requested host ports")


def preview_install(recipe: object, facts: object, authorization: object, request: object) -> dict:
    """Produce a synthetic compatibility preview; NEVER authorize an install."""
    kind = validate_recipe(recipe)
    validate_synthetic_inputs(facts, authorization, request)
    blockers: list[str] = []

    def block(reason: str) -> None:
        if reason not in blockers:
            blockers.append(reason)

    # These synthetic channels are intentionally separate. Equality checks
    # are only fictional consistency checks, never authentication proof.
    if authorization["host_id"] != facts["host_id"] or request["host_id"] != facts["host_id"]:
        block("HOST_SCOPE_MISMATCH")
    if request["tenant_id"] != authorization["tenant_id"]:
        block("TENANT_SCOPE_MISMATCH")
    if request["target_site_id"] not in authorization["authorized_site_ids"]:
        block("SITE_OWNERSHIP_UNVERIFIED")

    if kind == "native_script":
        native = recipe["native"]
        steps = [
            "NATIVE_PREVIEW_SITE_OWNERSHIP",
            "NATIVE_PREVIEW_RUNTIME_COMPATIBILITY",
            "NATIVE_PREVIEW_SQL_COMPATIBILITY",
            "NATIVE_PREVIEW_FILESYSTEM_QUOTAS",
            "NATIVE_PREVIEW_BACKUP_RESTORE",
        ]
        if native["runtime"] == "PHP_FPM" and not facts["php_fpm_available"]:
            block("NATIVE_PHP_FPM_UNAVAILABLE")
        if native["database_engine"] != "NONE" and native["database_engine"] not in facts["native_db_engines"]:
            block("NATIVE_DATABASE_UNAVAILABLE")
    else:
        container = recipe["container"]
        steps = [
            "CONTAINER_PREVIEW_DRIVER_COMPATIBILITY",
            "CONTAINER_PREVIEW_IMAGE_DIGEST",
            "CONTAINER_PREVIEW_RESOURCE_BUDGET",
            "CONTAINER_PREVIEW_NETWORK_AND_VOLUMES",
            "CONTAINER_PREVIEW_BACKUP_RESTORE",
        ]
        if not authorization["container_permission_claimed"]:
            block("CONTAINER_SCOPE_UNVERIFIED")
        if container["driver"] not in facts["available_container_drivers"]:
            block("CONTAINER_DRIVER_NOT_AVAILABLE")
        for field, budget in (
            ("cpu_millicores", "free_cpu_millicores"),
            ("memory_mib", "free_memory_mib"),
            ("pids_limit", "free_pids"),
        ):
            if container[field] > facts[budget]:
                block("CONTAINER_"+field.upper()+"_BUDGET_UNAVAILABLE")
    for port in request["host_tcp_ports"]:
        if port in RESERVED_FORGEPANEL_PORTS or port in facts["reserved_host_tcp_ports"]:
            block("FORGEPANEL_OR_OTHER_RESERVED_PORT")
        elif port in facts["observed_bound_host_tcp_ports"]:
            block("HOST_PORT_ALREADY_CLAIMED")
        else:
            block("HOST_PORT_PUBLICATION_NOT_APPROVED")

    # A container preview cannot silently turn into a free native installation,
    # or vice versa, even if synthetic prerequisites appear to match.
    return {
        "schema_version": 1,
        "plan_status": "CANDIDATE_PREVIEW_ONLY",
        "recipe_kind": kind,
        "app_id": recipe["app_id"],
        "variant_id": recipe["variant_id"],
        "target_site_id": request["target_site_id"],
        "compatibility": "BLOCKED_BY_SYNTHETIC_FACTS" if blockers else "MATCHES_SYNTHETIC_FACTS_ONLY",
        "blocking_reasons": blockers,
        "preview_steps": steps,
        "execution_allowed": False,
        "apply_available": False,
        "tenant_authorization_verified": False,
        "artifact_signature_verified": False,
        "runtime_capabilities_verified": False,
        "port_probe_executed": False,
        "resource_reservations_created": False,
        "input_trust": {
            "host_capabilities": "SYNTHETIC_UNVERIFIED",
            "authorization_context": "SYNTHETIC_UNVERIFIED",
            "client_request": "UNTRUSTED_CANDIDATE",
        },
        "external_reachability_verified": False,
        "hub_entitlement_required": False,
        "next_action": "SPECIALIST_REVIEW_AND_REAL_INTEGRATION_REQUIRED",
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--fixture", choices=("native", "container"), required=True)
    args = parser.parse_args()
    recipe_name = ("native-cms.v1.json" if args.fixture == "native"
                   else "container-worker.v1.json")
    try:
        recipe = load_fixture(FIXTURES / recipe_name)
        facts = load_fixture(FIXTURES / "host-capabilities.synthetic.json")
        authorization = load_fixture(FIXTURES / "authorization.synthetic.json")
        request = load_fixture(FIXTURES / "install-request.synthetic.json")
        report = preview_install(recipe, facts, authorization, request)
    except (RecipeContractError, KeyError, TypeError) as exc:
        print(f"FAIL: synthetic plan inputs rejected: {exc}")
        return 1
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
