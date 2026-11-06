#!/usr/bin/env python3
"""Validate candidate ForgePanel portal discovery/access registry; no network or runtime effects."""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "evidence" / "portal-access-registry-v1.json"

EXPECTED = {
    "FORGE": ("/forge", 8447, "server-administration"),
    "PANEL": ("/panel", 8446, "customer-hosting"),
}
SURFACE_FIELDS = frozenset({
    "route_prefix", "direct_https_port", "address_source", "domain_policy", "purpose",
})
REQUIRED_DISCOVERY = {
    "address_enumeration": "OS_INTERFACES_AND_ROUTING",
    "include_ipv4": True,
    "include_ipv6": True,
    "exclude_loopback": True,
    "verify_address_is_host_assigned_or_explicitly_reachable": True,
    "do_not_assume_public_ip_from_private_interface": True,
    "fqdn_candidate_source": "OS_HOSTNAME_AND_RESOLVER",
    "fqdn_optional": True,
    "fqdn_requires_forward_dns_validation": True,
    "require_dns_ip_consistency": True,
    "ipv6_url_uses_square_brackets": True,
    "no_manually_entered_custom_domain": True,
    "no_automatic_subdomain_creation": True,
    "no_automatic_port_443_virtual_host": True,
    "url_advertisement_requires_valid_tls": True,
    "discovery_result_states": ["VERIFIED", "UNVERIFIED", "UNAVAILABLE"],
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


def validate_registry(data: Any) -> None:
    """Fail closed on changed policies or invented deployable defaults."""
    if not isinstance(data, dict):
        raise ValueError("Registry must be a JSON object")
    if type(data.get("schema_version")) is not int or data["schema_version"] != 1:
        raise ValueError("Expected integer schema_version 1")
    if type(data.get("draft_revision")) is not int or data["draft_revision"] != 2:
        raise ValueError("Expected corrected candidate draft revision 2")
    if data.get("status") != "SPECIFIED_NOT_IMPLEMENTED":
        raise ValueError("Registry cannot claim a running panel")

    surfaces = data.get("surfaces")
    if not isinstance(surfaces, dict) or set(surfaces) != set(EXPECTED):
        raise ValueError("Exactly FORGE and PANEL are required")
    seen_ports: set[int] = set()
    for role, (prefix, port, purpose) in EXPECTED.items():
        spec = surfaces[role]
        if not isinstance(spec, dict) or set(spec) != SURFACE_FIELDS:
            raise ValueError(f"{role} has missing/extra fields, including forbidden custom-domain settings")
        if spec["route_prefix"] != prefix or spec["purpose"] != purpose:
            raise ValueError(f"Wrong path/purpose for {role}")
        current_port = spec["direct_https_port"]
        if type(current_port) is not int or current_port != port or current_port in seen_ports:
            raise ValueError(f"Wrong/duplicate port for {role}")
        seen_ports.add(current_port)
        if spec["address_source"] != "SYSTEM_DETECTED":
            raise ValueError(f"{role} IP must be autodetected")
        if spec["domain_policy"] != "DISCOVER_EXISTING_FQDN_IF_VERIFIED":
            raise ValueError(f"{role} domain must be discovered, not user-customized")

    discovery = data.get("discovery")
    if not isinstance(discovery, dict) or set(discovery) != set(REQUIRED_DISCOVERY):
        raise ValueError("Discovery contract has missing/extra controls")
    if any(type(discovery[name]) is not type(expected) or discovery[name] != expected
           for name, expected in REQUIRED_DISCOVERY.items()):
        raise ValueError("Discovery contract altered: no custom domains, guessing, or automatic 443")
    security = data.get("required_security")
    if not isinstance(security, dict) or set(security) != set(REQUIRED_SECURITY):
        raise ValueError("Required security policy keys differ")
    if any(security[key] is not True for key in REQUIRED_SECURITY):
        raise ValueError("Cannot weaken security prerequisites")
    expected = [f"PORTAL-FP-{i:04d}" for i in range(1, 13)]
    if data.get("requirements") != expected:
        raise ValueError("The twelve portal requirements must remain traceable")
    unresolved = data.get("deployment_decisions_not_set")
    if not isinstance(unresolved, list) or not unresolved:
        raise ValueError("Unresolved deployment details must remain visible")
    if any(not isinstance(value, str) or not value.strip() for value in unresolved):
        raise ValueError("Unresolved details must be non-empty strings")


def main() -> int:
    try:
        validate_registry(json.loads(REGISTRY.read_text(encoding="utf-8")))
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"FAIL: offline portal discovery/access registry: {exc}")
        return 1
    print("PASS: candidate discovery/access contract only; no real IP/DNS/TLS probe or runtime qualification.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
