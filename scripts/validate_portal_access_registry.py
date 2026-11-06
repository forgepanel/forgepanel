#!/usr/bin/env python3
"""Validate the proposed ForgePanel portal access registry (NOT live routing)."""
from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "evidence" / "portal-access-registry-v1.json"
EXPECTED = {
    "FORGE": ("/forge", 8447, "server-administration"),
    "PANEL": ("/panel", 8446, "customer-hosting"),
}
REQUIRED_SECURITY = (
    "tls_validation",
    "exact_trusted_host_allowlist",
    "distinct_sessions_and_cookie_names",
    "independent_server_side_authorization",
    "do_not_use_ports_as_cookie_boundary",
    "trust_forwarded_headers_from_allowlisted_proxies_only",
    "preserve_admin_recovery_during_listener_changes",
    "no_generic_root_shell_endpoint",
    "core_operates_without_hub",
)
HOST_RE = re.compile(
    r"(?=.{1,253}$)(?=.{1,63}(?:\\.|$))(?:[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?\\.)+"
    r"[a-z](?:[a-z0-9-]{0,61}[a-z0-9])?$"
)


def validate_registry(data: Any) -> None:
    """Reject contradictions in a documentation-only candidate; no system access."""
    if not isinstance(data, dict):
        raise ValueError("Registry must be a JSON object")
    if data.get("schema_version") != 1 or type(data.get("schema_version")) is not int:
        raise ValueError("Expected integer schema_version 1")
    if data.get("status") != "SPECIFIED_NOT_IMPLEMENTED":
        raise ValueError("Only an unimplemented specification is described")

    surfaces = data.get("surfaces")
    if not isinstance(surfaces, dict) or set(surfaces) != set(EXPECTED):
        raise ValueError("Exactly FORGE and PANEL surfaces are required")
    seen_ports: set[int] = set()
    seen_hosts: set[str] = set()
    for role, (prefix, port, purpose) in EXPECTED.items():
        spec = surfaces[role]
        if not isinstance(spec, dict):
            raise ValueError(f"{role} surface must be an object")
        if spec.get("route_prefix") != prefix:
            raise ValueError(f"Incorrect route prefix for {role}")
        direct_port = spec.get("direct_https_port")
        if type(direct_port) is not int or direct_port != port or direct_port in seen_ports:
            raise ValueError(f"Incorrect or overlapping HTTPS port for {role}")
        seen_ports.add(direct_port)
        if type(spec.get("virtual_host_https_port")) is not int or spec["virtual_host_https_port"] != 443:
            raise ValueError(f"Invalid virtual-host HTTPS port for {role}")
        if spec.get("hostname_policy") != "CONFIGURABLE_PER_INSTALLATION":
            raise ValueError(f"{role} hostname must remain configurable")
        if spec.get("example_only") is not True:
            raise ValueError(f"{role} hostname example is NOT a production default")
        host = spec.get("example_hostname")
        if not isinstance(host, str) or not HOST_RE.fullmatch(host.lower()):
            raise ValueError(f"Invalid example hostname for {role}")
        if host.lower() in seen_hosts:
            raise ValueError("FORGE/PANEL example hosts must be distinct")
        seen_hosts.add(host.lower())
        if spec.get("purpose") != purpose:
            raise ValueError(f"Incorrect audience scope for {role}")

    security = data.get("required_security")
    if not isinstance(security, dict):
        raise ValueError("Missing required security invariants")
    if set(security) != set(REQUIRED_SECURITY):
        raise ValueError("Required security policy keys differ")
    if any(security[name] is not True for name in REQUIRED_SECURITY):
        raise ValueError("Cannot weaken security prerequisites")
    expected_requirements = [f"PORTAL-FP-{i:04d}" for i in range(1, 13)]
    if data.get("requirements") != expected_requirements:
        raise ValueError("The twelve documented portal requirements must remain linked")
    unresolved = data.get("deployment_decisions_not_set")
    if not isinstance(unresolved, list) or not all(isinstance(x, str) and x.strip() for x in unresolved):
        raise ValueError("Unresolved deployment details must remain visible")
    if not unresolved:
        raise ValueError("No production defaults have been decided")


def main() -> int:
    try:
        data = json.loads(REGISTRY.read_text(encoding="utf-8"))
        validate_registry(data)
    except (OSError, json.JSONDecodeError, ValueError) as exc:
        print(f"FAIL: candidate portal registry: {exc}")
        return 1
    print("PASS: offline registry checks only; no Symfony route, TLS listener or security certification.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
