#!/usr/bin/env python3
"""Offline App Center owner-policy and documentation traceability tests."""
from __future__ import annotations

import copy
import json
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
REGISTRY = ROOT / "evidence/app-center-separation-v1.json"
REQUIRED_FLAGS = (
    "no_generic_shell_exec", "no_cross_engine_fallback",
    "independent_execution_contracts", "independent_resource_accounting",
    "independent_backup_restore", "local_rbac_and_agent_authorization",
    "native_no_commercial_entitlement", "native_no_docker_podman_dependency",
    "reject_unreviewed_manifests", "container_no_privileged_or_host_root_mount_by_default",
    "no_automatic_conversion_between_install_kinds", "core_runs_without_publisher_hub",
)

def check(data: dict) -> None:
    if not isinstance(data, dict) or type(data.get("schema_version")) is not int or data["schema_version"] != 1:
        raise ValueError("Unsupported registry")
    if data.get("status") != "SPECIFIED_NOT_IMPLEMENTED" or data.get("prior_decisions_preserved") != "Q1-Q170":
        raise ValueError("Cannot misreport status or override earlier decisions")
    ui = data.get("ui")
    if not isinstance(ui, dict) or ui.get("umbrella") != "APP_CENTER":
        raise ValueError("App Center umbrella missing")
    sections = ui.get("sections")
    if not isinstance(sections, list) or len(sections) != 2:
        raise ValueError("Expected exactly two sections")
    native, container = sections
    if set(native) != {"key","recipe_kind","engine","free_core","hub_required","container_runtime_required"}:
        raise ValueError("Native engine fields changed")
    if (native["key"],native["recipe_kind"],native["engine"]) != ("ONE_CLICK_INSTALL","native_script","NATIVE_SITE"):
        raise ValueError("Native engine mismatch")
    if native["free_core"] is not True or native["hub_required"] is not False or native["container_runtime_required"] is not False:
        raise ValueError("Native install must stay free and independent")
    if set(container) != {"key","recipe_kind","engine","free_core_base","hub_required","drivers"}:
        raise ValueError("Container engine fields changed")
    if (container["key"],container["recipe_kind"],container["engine"]) != ("CONTAINER_APPS","container_stack","CONTAINER_STACK"):
        raise ValueError("Container engine mismatch")
    if container["free_core_base"] is not True or container["hub_required"] is not False or container["drivers"] != ["DOCKER","PODMAN"]:
        raise ValueError("Container requirements conflict with previous decisions")
    flags=data.get("security_invariants")
    if not isinstance(flags,dict) or set(flags) != set(REQUIRED_FLAGS) or any(flags[k] is not True for k in REQUIRED_FLAGS):
        raise ValueError("Security/commercial boundary weakened")
    if not isinstance(data.get("not_shipped"),list) or set(data["not_shipped"]) != {
        "native_script_installer","container_stack_executor","docker_driver","podman_driver","app_catalog_runtime"
    }:
        raise ValueError("No working app installer can be claimed")
    if not isinstance(data.get("open_technical_choices"),list) or not data["open_technical_choices"]:
        raise ValueError("Open choices must remain recorded")

class AppCenterContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = json.loads(REGISTRY.read_text(encoding="utf-8"))

    def test_registry(self):
        check(self.data)

    def test_no_runtime_claim(self):
        self.assertEqual(self.data["status"],"SPECIFIED_NOT_IMPLEMENTED")
        self.assertEqual(len(self.data["not_shipped"]),5)

    def test_two_sections_and_runtime_discriminator(self):
        n,c=self.data["ui"]["sections"]
        self.assertNotEqual(n["recipe_kind"],c["recipe_kind"])
        self.assertFalse(n["container_runtime_required"])
        self.assertEqual(c["drivers"],["DOCKER","PODMAN"])

    def test_french_english_pages_share_same_guards(self):
        for lang in ("fr","en"):
            txt=(ROOT/"DOCUMENTATION"/lang/"06-apps-recipes/app-center-engines.md").read_text(encoding="utf-8")
            self.assertIn("ONE-CLICK INSTALL",txt)
            self.assertIn("CONTAINER APPS",txt)
            self.assertIn("native_script",txt)
            self.assertIn("container_stack",txt)
            self.assertIn("decisions-q171-q220.md",txt)
            self.assertIn("Q221+",txt)

    def test_quality_matrices_match_all_identifiers(self):
        required={f"TEST-APP-NAT-{i:04d}" for i in range(1,13)}
        required|={f"TEST-APP-CTR-{i:04d}" for i in range(1,13)}
        required|={f"TEST-APP-X-{i:04d}" for i in range(1,9)}
        for lang in ("fr","en"):
            txt=(ROOT/"DOCUMENTATION"/lang/"13-tests-quality/app-center-engine-gates.md").read_text(encoding="utf-8")
            self.assertEqual(set(re.findall(r"TEST-APP-(?:NAT|CTR|X)-\d{4}",txt)),required)
            self.assertIn("PLANNED",txt)

    def test_reject_paid_native(self):
        x=copy.deepcopy(self.data)
        x["ui"]["sections"][0]["free_core"]=False
        with self.assertRaises(ValueError): check(x)

    def test_reject_native_docker_dependency(self):
        x=copy.deepcopy(self.data)
        x["ui"]["sections"][0]["container_runtime_required"]=True
        with self.assertRaises(ValueError): check(x)

    def test_reject_one_engine_for_both(self):
        x=copy.deepcopy(self.data)
        x["ui"]["sections"][1]["recipe_kind"]="native_script"
        with self.assertRaises(ValueError): check(x)

    def test_reject_single_driver(self):
        x=copy.deepcopy(self.data)
        x["ui"]["sections"][1]["drivers"]=["DOCKER"]
        with self.assertRaises(ValueError): check(x)

    def test_reject_hub_required(self):
        x=copy.deepcopy(self.data)
        x["ui"]["sections"][1]["hub_required"]=True
        with self.assertRaises(ValueError): check(x)

    def test_reject_generic_shell(self):
        x=copy.deepcopy(self.data)
        x["security_invariants"]["no_generic_shell_exec"]=False
        with self.assertRaises(ValueError): check(x)

    def test_reject_cross_engine_conversion(self):
        x=copy.deepcopy(self.data)
        x["security_invariants"]["no_automatic_conversion_between_install_kinds"]=False
        with self.assertRaises(ValueError): check(x)

    def test_reject_privileged_mount(self):
        x=copy.deepcopy(self.data)
        x["security_invariants"]["container_no_privileged_or_host_root_mount_by_default"]=False
        with self.assertRaises(ValueError): check(x)

if __name__ == "__main__":
    unittest.main()
