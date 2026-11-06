#!/usr/bin/env python3
"""Offline candidate portal-contract tests; no live host/IP/DNS/TLS detection."""
from __future__ import annotations

import copy
import json
import re
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))
from validate_portal_access_registry import REGISTRY, validate_registry  # noqa: E402

IDS = {f"PORTAL-FP-{i:04d}" for i in range(1, 13)}
TEST_IDS = {f"TEST-PORTAL-{i:04d}" for i in range(1, 23)}


class PortalAccessContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.base = json.loads(REGISTRY.read_text(encoding="utf-8"))

    def altered(self) -> dict:
        return copy.deepcopy(self.base)

    def rejects(self, mutated: dict) -> None:
        with self.assertRaises(ValueError):
            validate_registry(mutated)

    def test_corrected_candidate_contract_is_valid(self) -> None:
        validate_registry(self.base)

    def test_status_and_revision_are_not_live_claims(self) -> None:
        self.assertEqual(self.base["status"], "SPECIFIED_NOT_IMPLEMENTED")
        self.assertEqual(self.base["draft_revision"], 2)
        self.assertTrue(self.base["deployment_decisions_not_set"])

    def test_fixed_ip_and_path_contract(self) -> None:
        self.assertEqual(self.base["surfaces"]["FORGE"]["direct_https_port"], 8447)
        self.assertEqual(self.base["surfaces"]["PANEL"]["direct_https_port"], 8446)
        self.assertEqual(self.base["surfaces"]["FORGE"]["route_prefix"], "/forge")
        self.assertEqual(self.base["surfaces"]["PANEL"]["route_prefix"], "/panel")

    def test_discovery_is_system_only_without_domain_input(self) -> None:
        self.assertTrue(self.base["discovery"]["no_manually_entered_custom_domain"])
        self.assertTrue(self.base["discovery"]["fqdn_optional"])
        for spec in self.base["surfaces"].values():
            self.assertEqual(spec["address_source"], "SYSTEM_DETECTED")
            self.assertEqual(spec["domain_policy"], "DISCOVER_EXISTING_FQDN_IF_VERIFIED")
            self.assertNotIn("example_hostname", spec)
            self.assertNotIn("virtual_host_https_port", spec)

    def test_documented_requirements_match_registry_both_languages(self) -> None:
        self.assertEqual(set(self.base["requirements"]), IDS)
        for lang in ("en", "fr"):
            path = ROOT / "DOCUMENTATION" / lang / "07-interfaces-roles" / "portal-access-routing.md"
            text = path.read_text(encoding="utf-8")
            self.assertEqual(set(re.findall(r"PORTAL-FP-\d{4}", text)), IDS)

    def test_planned_http_vm_matrix_is_bilingual(self) -> None:
        for lang in ("en", "fr"):
            path = ROOT / "DOCUMENTATION" / lang / "13-tests-quality" / "portal-access-gates.md"
            text = path.read_text(encoding="utf-8")
            self.assertEqual(set(re.findall(r"TEST-PORTAL-\d{4}", text)), TEST_IDS)
            self.assertIn("PLANNED", text)

    def test_reject_wrong_admin_port(self) -> None:
        x = self.altered()
        x["surfaces"]["FORGE"]["direct_https_port"] = 8446
        self.rejects(x)

    def test_reject_wrong_panel_prefix(self) -> None:
        x = self.altered()
        x["surfaces"]["PANEL"]["route_prefix"] = "/forge"
        self.rejects(x)

    def test_reject_port_with_boolean_type(self) -> None:
        x = self.altered()
        x["surfaces"]["PANEL"]["direct_https_port"] = True
        self.rejects(x)

    def test_reject_custom_domain_policy(self) -> None:
        x = self.altered()
        x["surfaces"]["FORGE"]["domain_policy"] = "CONFIGURABLE_PER_INSTALLATION"
        self.rejects(x)

    def test_reject_manually_supplied_domain_field(self) -> None:
        x = self.altered()
        x["surfaces"]["FORGE"]["custom_domain"] = "forge.example.test"
        self.rejects(x)

    def test_reject_hardcoded_example_host(self) -> None:
        x = self.altered()
        x["surfaces"]["PANEL"]["example_hostname"] = "panel.example.test"
        self.rejects(x)

    def test_reject_extra_virtual_host_port(self) -> None:
        x = self.altered()
        x["surfaces"]["PANEL"]["virtual_host_https_port"] = 443
        self.rejects(x)

    def test_reject_explicit_custom_domain_input(self) -> None:
        x = self.altered()
        x["discovery"]["no_manually_entered_custom_domain"] = False
        self.rejects(x)

    def test_reject_auto_subdomain(self) -> None:
        x = self.altered()
        x["discovery"]["no_automatic_subdomain_creation"] = False
        self.rejects(x)

    def test_reject_auto_port_443_virtual_host(self) -> None:
        x = self.altered()
        x["discovery"]["no_automatic_port_443_virtual_host"] = False
        self.rejects(x)

    def test_reject_required_fqdn(self) -> None:
        x = self.altered()
        x["discovery"]["fqdn_optional"] = False
        self.rejects(x)

    def test_reject_dns_without_forward_validation(self) -> None:
        x = self.altered()
        x["discovery"]["fqdn_requires_forward_dns_validation"] = False
        self.rejects(x)

    def test_reject_unverified_dns_ip_mapping(self) -> None:
        x = self.altered()
        x["discovery"]["require_dns_ip_consistency"] = False
        self.rejects(x)

    def test_reject_public_ip_assumption(self) -> None:
        x = self.altered()
        x["discovery"]["do_not_assume_public_ip_from_private_interface"] = False
        self.rejects(x)

    def test_reject_loopback_ip(self) -> None:
        x = self.altered()
        x["discovery"]["exclude_loopback"] = False
        self.rejects(x)

    def test_reject_ipv6_suppression(self) -> None:
        x = self.altered()
        x["discovery"]["include_ipv6"] = False
        self.rejects(x)

    def test_reject_ipv6_literal_without_brackets(self) -> None:
        x = self.altered()
        x["discovery"]["ipv6_url_uses_square_brackets"] = False
        self.rejects(x)

    def test_reject_unverified_tls_links(self) -> None:
        x = self.altered()
        x["discovery"]["url_advertisement_requires_valid_tls"] = False
        self.rejects(x)

    def test_reject_non_system_ip_source(self) -> None:
        x = self.altered()
        x["surfaces"]["PANEL"]["address_source"] = "USER_INPUT"
        self.rejects(x)

    def test_reject_cookie_isolation_weakening(self) -> None:
        x = self.altered()
        x["required_security"]["distinct_sessions_and_cookie_names"] = False
        self.rejects(x)

    def test_reject_proxy_spoofing_policy_weakening(self) -> None:
        x = self.altered()
        x["required_security"]["trust_forwarded_headers_from_allowlisted_proxies_only"] = False
        self.rejects(x)

    def test_reject_hub_dependency(self) -> None:
        x = self.altered()
        x["required_security"]["core_operates_without_hub"] = False
        self.rejects(x)

    def test_reject_generic_root_shell(self) -> None:
        x = self.altered()
        x["required_security"]["no_generic_root_shell_endpoint"] = False
        self.rejects(x)

    def test_reject_changed_runtime_status(self) -> None:
        x = self.altered()
        x["status"] = "DEPLOYED"
        self.rejects(x)

    def test_reject_old_revision(self) -> None:
        x = self.altered()
        x["draft_revision"] = 1
        self.rejects(x)

    def test_reject_missing_requirement(self) -> None:
        x = self.altered()
        x["requirements"].pop()
        self.rejects(x)

    def test_reject_unknown_discovery_field(self) -> None:
        x = self.altered()
        x["discovery"]["allow_unverified_domains"] = True
        self.rejects(x)


if __name__ == "__main__":
    unittest.main()
