#!/usr/bin/env python3
"""Offline synthetic preview tests; never install or verify host capabilities."""
from __future__ import annotations

import copy
import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))
from preview_app_center_install import (  # noqa: E402
    preview_install, validate_synthetic_inputs,
)
from validate_app_center_recipe import FIXTURES, RecipeContractError  # noqa: E402


class AppCenterPreviewTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.native = json.loads((FIXTURES / "native-cms.v1.json").read_text())
        cls.container = json.loads((FIXTURES / "container-worker.v1.json").read_text())
        cls.facts = json.loads((FIXTURES / "host-capabilities.synthetic.json").read_text())
        cls.request = json.loads((FIXTURES / "install-request.synthetic.json").read_text())

    def context(self):
        return copy.deepcopy(self.facts), copy.deepcopy(self.request)

    def test_native_preview_is_free_and_never_executable(self):
        facts, request = self.context()
        request["hub_available"] = False
        r = preview_install(self.native, facts, request)
        self.assertEqual(r["recipe_kind"], "native_script")
        self.assertEqual(r["compatibility"], "MATCHES_SYNTHETIC_FACTS_ONLY")
        self.assertEqual(r["blocking_reasons"], [])
        self.assertFalse(r["hub_entitlement_required"])
        self.assertFalse(r["execution_allowed"])
        self.assertFalse(r["apply_available"])
        self.assertFalse(r["tenant_authorization_verified"])

    def test_container_preview_is_separate_and_never_executable(self):
        facts, request = self.context()
        r = preview_install(self.container, facts, request)
        self.assertEqual(r["recipe_kind"], "container_stack")
        self.assertEqual(r["compatibility"], "MATCHES_SYNTHETIC_FACTS_ONLY")
        self.assertTrue(all(step.startswith("CONTAINER_") for step in r["preview_steps"]))
        self.assertFalse(r["execution_allowed"])
        self.assertFalse(r["resource_reservations_created"])

    def test_native_preview_never_requests_container_resources(self):
        facts, request = self.context()
        r = preview_install(self.native, facts, request)
        self.assertTrue(all(step.startswith("NATIVE_") for step in r["preview_steps"]))

    def test_native_without_docker_or_hub_still_matches_synthetic_facts(self):
        facts, request = self.context()
        facts["available_container_drivers"] = []
        request["hub_available"] = False
        self.assertEqual(
            preview_install(self.native, facts, request)["compatibility"],
            "MATCHES_SYNTHETIC_FACTS_ONLY",
        )

    def test_missing_native_php_blocks_only_native(self):
        facts, request = self.context()
        facts["php_fpm_available"] = False
        a = preview_install(self.native, facts, request)
        b = preview_install(self.container, facts, request)
        self.assertIn("NATIVE_PHP_FPM_UNAVAILABLE", a["blocking_reasons"])
        self.assertEqual(b["blocking_reasons"], [])

    def test_missing_native_database_denies_native(self):
        facts, request = self.context()
        facts["native_db_engines"] = []
        self.assertIn("NATIVE_DATABASE_UNAVAILABLE",
                      preview_install(self.native, facts, request)["blocking_reasons"])

    def test_no_container_driver_denies_only_container(self):
        facts, request = self.context()
        facts["available_container_drivers"] = []
        a = preview_install(self.native, facts, request)
        b = preview_install(self.container, facts, request)
        self.assertEqual(a["blocking_reasons"], [])
        self.assertIn("CONTAINER_DRIVER_NOT_AVAILABLE", b["blocking_reasons"])

    def test_qualified_driver_names_are_not_interchangeable(self):
        facts, request = self.context()
        facts["available_container_drivers"] = ["PODMAN"]
        r = preview_install(self.container, facts, request)
        self.assertIn("CONTAINER_DRIVER_NOT_AVAILABLE", r["blocking_reasons"])

    def test_container_cpu_memory_pids_are_independent(self):
        facts, request = self.context()
        facts["free_cpu_millicores"] = 1
        facts["free_memory_mib"] = 1
        facts["free_pids"] = 1
        reasons = preview_install(self.container, facts, request)["blocking_reasons"]
        self.assertIn("CONTAINER_CPU_MILLICORES_BUDGET_UNAVAILABLE", reasons)
        self.assertIn("CONTAINER_MEMORY_MIB_BUDGET_UNAVAILABLE", reasons)
        self.assertIn("CONTAINER_PIDS_LIMIT_BUDGET_UNAVAILABLE", reasons)

    def test_site_not_owned_blocks_both_engines(self):
        facts, request = self.context()
        request["target_site_id"] = "foreign-site"
        for recipe in (self.native, self.container):
            self.assertIn("SITE_OWNERSHIP_UNVERIFIED",
                          preview_install(recipe, facts, request)["blocking_reasons"])

    def test_container_scope_missing_blocks_container(self):
        facts, request = self.context()
        facts["container_scope_claimed"] = False
        self.assertIn("CONTAINER_SCOPE_UNVERIFIED",
                      preview_install(self.container, facts, request)["blocking_reasons"])

    def test_forgepanel_reserved_ports_are_never_available(self):
        for port in (8446, 8447):
            with self.subTest(port=port):
                facts, request = self.context()
                facts["reserved_host_tcp_ports"] = []
                request["host_tcp_ports"] = [port]
                self.assertIn(
                    "FORGEPANEL_OR_OTHER_RESERVED_PORT",
                    preview_install(self.container, facts, request)["blocking_reasons"],
                )

    def test_observed_bound_port_cannot_be_reused(self):
        facts, request = self.context()
        request["host_tcp_ports"] = [443]
        self.assertIn("HOST_PORT_ALREADY_CLAIMED",
                      preview_install(self.container, facts, request)["blocking_reasons"])

    def test_free_host_port_is_still_unapproved_for_publication(self):
        facts, request = self.context()
        request["host_tcp_ports"] = [9000]
        self.assertIn("HOST_PORT_PUBLICATION_NOT_APPROVED",
                      preview_install(self.container, facts, request)["blocking_reasons"])

    def test_native_host_port_request_is_not_implicitly_authorized(self):
        facts, request = self.context()
        request["host_tcp_ports"] = [9000]
        self.assertIn("HOST_PORT_PUBLICATION_NOT_APPROVED",
                      preview_install(self.native, facts, request)["blocking_reasons"])

    def test_invalid_port_boolean_rejected(self):
        facts, request = self.context()
        request["host_tcp_ports"] = [True]
        with self.assertRaises(RecipeContractError):
            preview_install(self.native, facts, request)

    def test_duplicate_ports_rejected(self):
        facts, request = self.context()
        request["host_tcp_ports"] = [9000, 9000]
        with self.assertRaises(RecipeContractError):
            preview_install(self.container, facts, request)

    def test_huge_or_negative_capacity_rejected(self):
        for val in (True, -1, 2**31, "1024"):
            with self.subTest(value=val):
                facts, request = self.context()
                facts["free_memory_mib"] = val
                with self.assertRaises(RecipeContractError):
                    preview_install(self.container, facts, request)

    def test_unknown_host_fields_rejected_including_secrets(self):
        facts, request = self.context()
        facts["sql_password"] = "never-in-preview"
        with self.assertRaises(RecipeContractError):
            preview_install(self.native, facts, request)

    def test_unknown_request_fields_rejected_including_commands(self):
        facts, request = self.context()
        request["shell_command"] = "sudo any-command"
        with self.assertRaises(RecipeContractError):
            preview_install(self.container, facts, request)

    def test_client_cannot_claim_verified_context(self):
        facts, request = self.context()
        facts["fixture_status"] = "VERIFIED"
        with self.assertRaises(RecipeContractError):
            preview_install(self.native, facts, request)

    def test_unverified_ownership_never_turns_into_real_authorization(self):
        facts, request = self.context()
        r = preview_install(self.native, facts, request)
        for key in ("tenant_authorization_verified", "artifact_signature_verified",
                    "runtime_capabilities_verified", "port_probe_executed",
                    "external_reachability_verified", "resource_reservations_created"):
            self.assertIs(r[key], False, key)

    def test_recipe_with_untrusted_exec_field_rejected(self):
        facts, request = self.context()
        recipe = copy.deepcopy(self.native)
        recipe["shell"] = "echo unexpected"
        with self.assertRaises(RecipeContractError):
            preview_install(recipe, facts, request)

    def test_preview_is_deterministic_and_does_not_mutate_inputs(self):
        facts, request = self.context()
        inputs = copy.deepcopy((self.native, facts, request))
        a = preview_install(self.native, facts, request)
        b = preview_install(self.native, facts, request)
        self.assertEqual(a, b)
        self.assertEqual(inputs, (self.native, facts, request))

    def test_synthetic_context_has_strict_version(self):
        facts, request = self.context()
        request["schema_version"] = True
        with self.assertRaises(RecipeContractError):
            validate_synthetic_inputs(facts, request)

    def test_host_without_owned_sites_is_not_implicitly_authorized(self):
        facts, request = self.context()
        facts["site_ids"] = []
        self.assertIn("SITE_OWNERSHIP_UNVERIFIED",
                      preview_install(self.native, facts, request)["blocking_reasons"])


if __name__ == "__main__":
    unittest.main()
