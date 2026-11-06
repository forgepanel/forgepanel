#!/usr/bin/env python3
"""Static candidate-contract tests; these do not exercise real HTTP/HTTPS routing."""
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
TEST_IDS = {f"TEST-PORTAL-{i:04d}" for i in range(1, 19)}


class PortalAccessContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.base = json.loads(REGISTRY.read_text(encoding="utf-8"))

    def altered(self) -> dict:
        return copy.deepcopy(self.base)

    def rejects(self, mutated: dict) -> None:
        with self.assertRaises(ValueError):
            validate_registry(mutated)

    def test_current_registry_passes_offline_checker(self) -> None:
        validate_registry(self.base)

    def test_not_a_runtime_or_release_claim(self) -> None:
        self.assertEqual(self.base["status"], "SPECIFIED_NOT_IMPLEMENTED")
        self.assertTrue(all(v["example_only"] for v in self.base["surfaces"].values()))
        self.assertTrue(self.base["deployment_decisions_not_set"])

    def test_documented_requirements_match_registry_both_languages(self) -> None:
        self.assertEqual(set(self.base["requirements"]), IDS)
        for lang in ("en", "fr"):
            path = ROOT / "DOCUMENTATION" / lang / "07-interfaces-roles" / "portal-access-routing.md"
            content = path.read_text(encoding="utf-8")
            self.assertEqual(set(re.findall(r"PORTAL-FP-\\d{4}", content)), IDS)

    def test_planned_end_to_end_matrix_is_bilingual(self) -> None:
        for lang in ("en", "fr"):
            path = ROOT / "DOCUMENTATION" / lang / "13-tests-quality" / "portal-access-gates.md"
            content = path.read_text(encoding="utf-8")
            self.assertEqual(set(re.findall(r"TEST-PORTAL-\\d{4}", content)), TEST_IDS)
            self.assertIn("PLANNED", content)

    def test_reject_changed_admin_port(self) -> None:
        x = self.altered()
        x["surfaces"]["FORGE"]["direct_https_port"] = 8446
        self.rejects(x)

    def test_reject_changed_user_path(self) -> None:
        x = self.altered()
        x["surfaces"]["PANEL"]["route_prefix"] = "/forge"
        self.rejects(x)

    def test_reject_non_https_virtual_port(self) -> None:
        x = self.altered()
        x["surfaces"]["PANEL"]["virtual_host_https_port"] = 80
        self.rejects(x)

    def test_reject_same_example_host(self) -> None:
        x = self.altered()
        x["surfaces"]["PANEL"]["example_hostname"] = x["surfaces"]["FORGE"]["example_hostname"]
        self.rejects(x)

    def test_reject_invalid_example_host(self) -> None:
        x = self.altered()
        x["surfaces"]["FORGE"]["example_hostname"] = "wrong-host/redirect"
        self.rejects(x)

    def test_reject_hardcoded_hostname_policy(self) -> None:
        x = self.altered()
        x["surfaces"]["FORGE"]["hostname_policy"] = "FIXED"
        self.rejects(x)

    def test_reject_example_treated_as_production_default(self) -> None:
        x = self.altered()
        x["surfaces"]["PANEL"]["example_only"] = False
        self.rejects(x)

    def test_reject_weakened_session_isolation(self) -> None:
        x = self.altered()
        x["required_security"]["distinct_sessions_and_cookie_names"] = False
        self.rejects(x)

    def test_reject_untrusted_forwarded_header_policy(self) -> None:
        x = self.altered()
        x["required_security"]["trust_forwarded_headers_from_allowlisted_proxies_only"] = False
        self.rejects(x)

    def test_reject_hub_required_for_core(self) -> None:
        x = self.altered()
        x["required_security"]["core_operates_without_hub"] = False
        self.rejects(x)

    def test_reject_generic_root_endpoint(self) -> None:
        x = self.altered()
        x["required_security"]["no_generic_root_shell_endpoint"] = False
        self.rejects(x)

    def test_reject_missing_invariant(self) -> None:
        x = self.altered()
        del x["required_security"]["exact_trusted_host_allowlist"]
        self.rejects(x)

    def test_reject_live_claim(self) -> None:
        x = self.altered()
        x["status"] = "DEPLOYED"
        self.rejects(x)

    def test_reject_untracked_requirements(self) -> None:
        x = self.altered()
        x["requirements"].pop()
        self.rejects(x)


if __name__ == "__main__":
    unittest.main()
