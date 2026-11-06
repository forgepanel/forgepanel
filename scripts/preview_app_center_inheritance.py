#!/usr/bin/env python3
"""Pure offline Q180/Q220 App Center inheritance candidate; NEVER an authorization API.

No OS reads, files written, network, Symfony/Go operations, database, secrets or
policy APPLY. All data is synthetic and all results are UNTRUSTED/NOT EXECUTABLE.
"""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FIXTURES = ROOT / "evidence" / "app-center-fixtures"
SCOPE_ORDER = ("global", "server", "organization", "plan", "site")
SUBJECT_KEYS = ("server_id", "organization_id", "plan_id", "site_id")
RESOURCE_KEY_TYPES = {
    "app.native.allowed": "restrictive_bool",
    "app.container.allowed": "restrictive_bool",
    "app.catalog.verified_partner_allowed": "restrictive_bool",
    "app.container.max_cpu_millicores": "narrowing_ceiling",
    "app.container.max_memory_mib": "narrowing_ceiling",
    "app.container.max_pids": "narrowing_ceiling",
}
# Hard-coded invariants for demonstration. These are not overridable by any
# tenant-level setting, application catalog or publisher Hub metadata.
IMMUTABLE_INVARIANTS = {
    "app.native.premium_required": False,
    "app.native.container_runtime_required": False,
    "app.core.hub_required": False,
    "app.security.generic_shell_allowed": False,
    "app.security.tenant_isolation_required": True,
    "app.security.signed_artifacts_required": True,
    "app.container.privileged_by_default": False,
    "app.system.reserved_tcp_ports": [8446, 8447],
}
SAFE_ID = re.compile(r"[a-z][a-z0-9_-]{2,63}\Z")
MAX_FIXTURE_SCALAR = (2 ** 31) - 1


class PolicyPreviewRejected(ValueError):
    """Synthetic proposed rules or input cannot be processed safely."""


def deny(reason: str) -> None:
    raise PolicyPreviewRejected(reason)


def check_value(key: str, value: object) -> None:
    kind = RESOURCE_KEY_TYPES[key]
    if kind == "restrictive_bool":
        if type(value) is not bool:
            deny(f"INVALID_TYPE: {key} requires boolean")
    elif kind == "narrowing_ceiling":
        if type(value) is not int or not 0 < value <= MAX_FIXTURE_SCALAR:
            deny(f"INVALID_BOUND: {key} requires positive integer")
    else:
        deny("UNKNOWN_POLICY_KIND")


def resolve_synthetic_policy(candidate: object) -> dict:
    """Evaluate only synthetic values; never mark a permission as verified."""
    if not isinstance(candidate, dict) or set(candidate) != {
        "schema_version", "status", "policy_contract",
        "numeric_values_are", "subject", "layers"
    }:
        deny("INVALID_POLICY_SHAPE")
    if (type(candidate["schema_version"]) is not int or candidate["schema_version"] != 1 or
        candidate["status"] != "SYNTHETIC_UNVERIFIED" or
        candidate["policy_contract"] != "APP_CENTER_INHERITANCE_CANDIDATE_V1" or
        candidate["numeric_values_are"] != "FICTIONAL_QA_EXAMPLES_NOT_PRODUCT_DEFAULTS"):
        deny("UNTRUSTED_POLICY_STATUS")
    subject = candidate["subject"]
    if not isinstance(subject, dict) or set(subject) != set(SUBJECT_KEYS):
        deny("INVALID_SUBJECT")
    if any(type(subject[k]) is not str or not SAFE_ID.fullmatch(subject[k]) for k in SUBJECT_KEYS):
        deny("INVALID_SUBJECT_ID")

    layers = candidate["layers"]
    if not isinstance(layers, list) or len(layers) != len(SCOPE_ORDER):
        deny("INVALID_SCOPE_CHAIN")
    effective: dict[str, object] = {}
    trace: dict[str, list[dict[str, object]]] = {k: [] for k in RESOURCE_KEY_TYPES}
    for index, (expected_scope, layer) in enumerate(zip(SCOPE_ORDER, layers)):
        if not isinstance(layer, dict) or set(layer) != {"scope", "changes"}:
            deny("INVALID_SCOPE_LAYER")
        if layer["scope"] != expected_scope:
            deny("INVALID_SCOPE_CHAIN")
        changes = layer["changes"]
        if not isinstance(changes, dict) or len(changes) > len(RESOURCE_KEY_TYPES):
            deny("INVALID_SCOPE_CHANGES")
        if index == 0 and set(changes) != set(RESOURCE_KEY_TYPES):
            deny("GLOBAL_CANDIDATE_MUST_DECLARE_ALL_DEMO_KEYS")
        for key, value in changes.items():
            if key not in RESOURCE_KEY_TYPES:
                deny("IMMUTABLE_OR_UNKNOWN_KEY")
            check_value(key, value)
            if index > 0:
                parent = effective.get(key)
                if parent is None:
                    deny("INCOMPLETE_PARENT_POLICY")
                kind = RESOURCE_KEY_TYPES[key]
                if kind == "restrictive_bool" and parent is False and value is True:
                    deny(f"CHILD_WIDENS_PARENT_POLICY: {key}")
                if kind == "narrowing_ceiling" and value > parent:
                    deny(f"CHILD_EXCEEDS_PARENT_CEILING: {key}")
            effective[key] = value
            trace[key].append({"scope": expected_scope, "synthetic_value": value})
    return {
        "schema_version": 1,
        "policy_status": "SYNTHETIC_CANDIDATE_ONLY",
        "scope_order": list(SCOPE_ORDER),
        "effective": effective,
        "provenance": trace,
        "immutable_invariants": {
            key: value[:] if isinstance(value, list) else value
            for key, value in IMMUTABLE_INVARIANTS.items()
        },
        "root_numeric_values_are": "FICTIONAL_NOT_PRODUCTION_LIMITS",
        "authorization_verified": False,
        "host_capabilities_verified": False,
        "policy_signature_verified": False,
        "physical_capacity_verified": False,
        "audit_written": False,
        "resource_reservations_created": False,
        "execution_allowed": False,
        "apply_available": False,
        "next_action": "EXPLICIT_ARCHITECTURE_SECURITY_API_DB_REVIEW_REQUIRED",
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--fixture", choices=("app-center",), required=True)
    args = parser.parse_args()
    path = FIXTURES / "config-inheritance.synthetic.json"
    try:
        raw = path.read_bytes()
        if len(raw) > 64 * 1024:
            deny("FIXTURE_TOO_LARGE")
        policy = json.loads(raw)
        result = resolve_synthetic_policy(policy)
    except (OSError, ValueError, UnicodeError) as exc:
        print(f"FAIL: {exc}")
        return 1
    print(json.dumps(result, sort_keys=True, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
