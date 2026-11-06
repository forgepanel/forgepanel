#!/usr/bin/env python3
"""Candidate-only evidence binding preflight. Does not authenticate or authorize.

No network, OS probes, filesystem mutation, SQL, Go IPC, Docker/Podman, privileged
execution, real signatures, clock provenance or resource reservation. CLI accepts
only two bundled synthetic fixture names; timestamps and resource values are fake.
"""
from __future__ import annotations

import argparse
import json
import re
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FIXTURES = ROOT / "evidence" / "app-center-fixtures"
IDENT = re.compile(r"[a-z][a-z0-9_-]{2,63}\Z")
TOKEN = re.compile(r"[a-z][a-z0-9_-]{2,79}\Z")
UTC_TIME = re.compile(r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z\Z")
TOP_KEYS = frozenset({
    "schema_version", "fixture_status", "synthetic_clock_utc",
    "host_observation", "core_authorization", "core_policy", "user_intent",
})
HOST_KEYS = frozenset({
    "source", "host_id", "snapshot_revision", "observed_at_utc",
    "expires_at_utc", "engines_present", "free_cpu_millicores",
    "free_memory_mib", "protected_host_tcp_ports",
})
AUTHZ_KEYS = frozenset({
    "source", "host_id", "tenant_id", "actor_id",
    "authorized_site_ids", "allowed_plan_scopes", "context_revision",
    "observed_at_utc", "expires_at_utc",
})
POLICY_KEYS = frozenset({
    "source", "host_id", "policy_revision", "native_enabled",
    "container_enabled", "qualified_container_drivers",
    "observed_at_utc", "expires_at_utc",
})
INTENT_KEYS = frozenset({
    "source", "host_id", "tenant_id", "actor_id", "site_id",
    "recipe_kind", "expected_host_snapshot_revision",
    "expected_authorization_revision", "expected_policy_revision",
    "requested_driver", "requested_cpu_millicores",
    "requested_memory_mib", "requested_host_tcp_ports",
    "idempotency_key",
})
DRIVERS = frozenset({"DOCKER", "PODMAN"})
ENGINES = frozenset({"NATIVE_SITE", "DOCKER", "PODMAN"})
PLAN_SCOPES = frozenset({"app.native.plan", "app.container.plan"})
PROTECTED_PORTS = frozenset({8446, 8447})
MAX_INT = 2**31 - 1
MAX_DOCUMENT_BYTES = 64 * 1024


class ContextRejected(ValueError):
    """Rejected shape: no evidence of actual host trust or system permission."""


def refuse(reason: str) -> None:
    raise ContextRejected(reason)


def strict_dict(value: object, keys: frozenset[str], label: str) -> dict:
    if not isinstance(value, dict) or set(value) != keys:
        refuse(f"INVALID_SHAPE_{label}")
    return value


def identifier(value: object, label: str) -> str:
    if type(value) is not str or not IDENT.fullmatch(value):
        refuse(f"INVALID_IDENTIFIER_{label}")
    return value


def integer(value: object, label: str, *, zero: bool = False) -> int:
    if type(value) is not int or not ((0 if zero else 1) <= value <= MAX_INT):
        refuse(f"INVALID_INTEGER_{label}")
    return value


def bounded_set(value: object, allowed: frozenset[str], label: str) -> list[str]:
    if (not isinstance(value, list) or len(value) > 16 or
        any(type(x) is not str or x not in allowed for x in value) or
        len(value) != len(set(value))):
        refuse(f"INVALID_LIST_{label}")
    return value


def ids(value: object, label: str) -> list[str]:
    if (not isinstance(value, list) or len(value) > 32 or
        any(type(x) is not str or not IDENT.fullmatch(x) for x in value) or
        len(set(value)) != len(value)):
        refuse(f"INVALID_IDS_{label}")
    return value


def ports(value: object, label: str) -> list[int]:
    if (not isinstance(value, list) or len(value) > 32 or
        any(type(x) is not int or not (1 <= x <= 65535) for x in value) or
        len(set(value)) != len(value)):
        refuse(f"INVALID_PORTS_{label}")
    return value


def utc(value: object) -> datetime:
    if type(value) is not str or not UTC_TIME.fullmatch(value):
        refuse("INVALID_TIMESTAMP")
    try:
        return datetime.strptime(value, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)
    except ValueError:
        refuse("INVALID_TIMESTAMP")


def review_candidate_context(value: object) -> dict:
    """Pure synthetic comparison. A matching result is never an APPLY grant."""
    item = strict_dict(value, TOP_KEYS, "TOP")
    if (type(item["schema_version"]) is not int or item["schema_version"] != 1 or
        item["fixture_status"] != "SYNTHETIC_UNVERIFIED"):
        refuse("UNTRUSTED_CONTEXT_STATUS")
    now = utc(item["synthetic_clock_utc"])
    host = strict_dict(item["host_observation"], HOST_KEYS, "HOST")
    auth = strict_dict(item["core_authorization"], AUTHZ_KEYS, "AUTHORIZATION")
    policy = strict_dict(item["core_policy"], POLICY_KEYS, "POLICY")
    intent = strict_dict(item["user_intent"], INTENT_KEYS, "INTENT")

    for record, source in (
        (host, "UNVERIFIED_OS_PROBE_FIXTURE"),
        (auth, "UNVERIFIED_SYMFONY_FIXTURE"),
        (policy, "UNVERIFIED_CONFIG_FIXTURE"),
        (intent, "UNTRUSTED_CLIENT_FIXTURE"),
    ):
        if record["source"] != source:
            refuse("UNTRUSTED_SOURCE_CLAIM")

    for obj, name in ((host, "HOST"), (auth, "AUTHZ"), (policy, "POLICY"),
                      (intent, "REQUEST")):
        identifier(obj["host_id"], name)
    for obj, name in ((auth, "AUTHZ"), (intent, "REQUEST")):
        identifier(obj["tenant_id"], name)
        identifier(obj["actor_id"], name)
    identifier(intent["site_id"], "SITE")
    identifier(intent["idempotency_key"], "IDEMPOTENCY_KEY")
    ids(auth["authorized_site_ids"], "AUTHORIZED_SITES")
    bounded_set(auth["allowed_plan_scopes"], PLAN_SCOPES, "AUTHORIZED_PLAN_SCOPES")
    bounded_set(host["engines_present"], ENGINES, "HOST_ENGINES")
    bounded_set(policy["qualified_container_drivers"], DRIVERS, "QUALIFIED_DRIVERS")
    ports(host["protected_host_tcp_ports"], "PROTECTED")
    ports(intent["requested_host_tcp_ports"], "REQUESTED")
    for obj, field in (
        (host, "snapshot_revision"), (auth, "context_revision"),
        (policy, "policy_revision"), (intent, "expected_host_snapshot_revision"),
        (intent, "expected_authorization_revision"),
        (intent, "expected_policy_revision"),
    ):
        integer(obj[field], field)
    for obj, field in ((host, "free_cpu_millicores"),
                       (host, "free_memory_mib"),
                       (intent, "requested_cpu_millicores"),
                       (intent, "requested_memory_mib")):
        integer(obj[field], field, zero=True)
    for field in ("native_enabled", "container_enabled"):
        if type(policy[field]) is not bool:
            refuse(f"INVALID_BOOLEAN_{field}")

    kind = intent["recipe_kind"]
    if kind not in ("native_script", "container_stack"):
        refuse("INVALID_RECIPE_KIND")
    driver = intent["requested_driver"]
    if type(driver) is not str or driver not in (DRIVERS | {"NONE"}):
        refuse("INVALID_DRIVER")

    blockers: list[str] = []
    def block(label: str) -> None:
        if label not in blockers:
            blockers.append(label)

    # Dates are synthetic; caller-provided fixture time is NOT trusted time.
    for record, label in ((host, "HOST"), (auth, "AUTHORIZATION"), (policy, "POLICY")):
        observed = utc(record["observed_at_utc"])
        expiry = utc(record["expires_at_utc"])
        if expiry <= observed or observed > now:
            block(f"{label}_EVIDENCE_FUTURE_OR_INVALID")
        elif now >= expiry:
            block(f"{label}_EVIDENCE_STALE")

    if not (host["host_id"] == auth["host_id"] == policy["host_id"] == intent["host_id"]):
        block("HOST_CONTEXT_MISMATCH")
    if auth["tenant_id"] != intent["tenant_id"]:
        block("TENANT_CONTEXT_MISMATCH")
    if auth["actor_id"] != intent["actor_id"]:
        block("ACTOR_CONTEXT_MISMATCH")
    if intent["site_id"] not in auth["authorized_site_ids"]:
        block("SITE_OWNERSHIP_UNVERIFIED")
    for left, right in (
        (host["snapshot_revision"], intent["expected_host_snapshot_revision"]),
        (auth["context_revision"], intent["expected_authorization_revision"]),
        (policy["policy_revision"], intent["expected_policy_revision"]),
    ):
        if left != right:
            block("EXPECTED_REVISION_STALE")
    if not PROTECTED_PORTS.issubset(set(host["protected_host_tcp_ports"])):
        block("CONTROL_PLANE_PORT_INVENTORY_INCOMPLETE")
    for port in intent["requested_host_tcp_ports"]:
        if port in PROTECTED_PORTS or port in host["protected_host_tcp_ports"]:
            block("CONTROL_PLANE_OR_RESERVED_PORT_COLLISION")
        else:
            block("HOST_PORT_EXPOSURE_POLICY_UNAPPROVED")

    if kind == "native_script":
        if "app.native.plan" not in auth["allowed_plan_scopes"]:
            block("NATIVE_PLAN_SCOPE_MISSING")
        if not policy["native_enabled"] or "NATIVE_SITE" not in host["engines_present"]:
            block("NATIVE_CAPABILITY_OR_POLICY_UNAVAILABLE")
        if driver != "NONE" or intent["requested_cpu_millicores"] != 0 or intent["requested_memory_mib"] != 0:
            block("NATIVE_REQUEST_MIXES_CONTAINER_RESOURCES")
    else:
        if "app.container.plan" not in auth["allowed_plan_scopes"]:
            block("CONTAINER_PLAN_SCOPE_MISSING")
        if not policy["container_enabled"]:
            block("CONTAINER_DISABLED_BY_POLICY")
        if driver not in DRIVERS or driver not in host["engines_present"] or driver not in policy["qualified_container_drivers"]:
            block("CONTAINER_DRIVER_NOT_QUALIFIED")
        if (intent["requested_cpu_millicores"] <= 0 or
            intent["requested_memory_mib"] <= 0):
            block("CONTAINER_RESOURCE_REQUEST_MISSING")
        elif (intent["requested_cpu_millicores"] > host["free_cpu_millicores"] or
              intent["requested_memory_mib"] > host["free_memory_mib"]):
            block("CONTAINER_SYNTHETIC_BUDGET_INSUFFICIENT")

    return {
        "schema_version": 1,
        "review_status": "BLOCKED_SYNTHETIC" if blockers else "MATCHES_SYNTHETIC_CONTEXT_ONLY",
        "blocking_reasons": blockers,
        "recipe_kind": kind,
        "host_id": intent["host_id"],
        "tenant_id": intent["tenant_id"],
        "site_id": intent["site_id"],
        "expected_policy_revision": intent["expected_policy_revision"],
        "source_trust": {
            "host": "UNVERIFIED",
            "core_authorization": "UNVERIFIED",
            "core_policy": "UNVERIFIED",
            "client_intent": "UNTRUSTED",
            "clock": "SYNTHETIC_UNVERIFIED",
        },
        "actor_authenticated": False,
        "host_identity_verified": False,
        "policy_signature_verified": False,
        "resource_reservations_created": False,
        "authorization_approved": False,
        "execution_allowed": False,
        "apply_available": False,
        "next_action": "AUTHORITATIVE_SYMFONY_AND_GO_IPC_REVIEW_REQUIRED",
    }


def load_synthetic(path: Path) -> object:
    if path.parent.resolve() != FIXTURES.resolve() or path.name not in {
        "admission-native.synthetic.json", "admission-container.synthetic.json",
    }:
        refuse("ONLY_BUNDLED_FIXTURES_ALLOWED")
    raw = path.read_bytes()
    if len(raw) > MAX_DOCUMENT_BYTES:
        refuse("FIXTURE_TOO_LARGE")
    try:
        return json.loads(raw)
    except (UnicodeError, ValueError):
        refuse("INVALID_JSON_FIXTURE")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--fixture", choices=("native", "container"), required=True)
    args = parser.parse_args()
    name = "admission-native.synthetic.json" if args.fixture == "native" else "admission-container.synthetic.json"
    try:
        report = review_candidate_context(load_synthetic(FIXTURES / name))
    except (ContextRejected, OSError) as exc:
        print(f"FAIL: offline evidence candidate: {exc}")
        return 1
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
