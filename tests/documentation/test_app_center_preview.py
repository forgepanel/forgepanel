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
        cls.authorization = json.loads((FIXTURES / "authorization.synthetic.json").read_text())
        cls.request = json.loads((FIXTURES / "install-request.synthetic.json").read_text())

    def context(self):
        return (copy.deepcopy(self.facts), copy.deepcopy(self.authorization),
                copy.deepcopy(self.request))

    def test_native_preview_is_free_and_never_executable(self):
        facts, auth, request = self.context()
        request["hub_available"] = False
        r = preview_install(self.native, facts, auth, request)
        self.assertEqual(r["recipe_kind"], "native_script")
        self.assertEqual(r["compatibility"], "MATCHES_SYNTHETIC_FACTS_ONLY")
        self.assertEqual(r["blocking_reasons"], [])
        self.assertFalse(r["hub_entitlement_required"])
        self.assertFalse(r["execution_allowed"])
        self.assertFalse(r["apply_available"])
        self.assertFalse(r["tenant_authorization_verified"])

    def test_container_preview_is_separate_and_never_executable(self):
        facts, auth, request = self.context()
        r = preview_install(self.container, facts, auth, request)
        self.assertEqual(r["recipe_kind"], "container_stack")
        self.assertEqual(r["compatibility"], "MATCHES_SYNTHETIC_FACTS_ONLY")
        self.assertTrue(all(step.startswith("CONTAINER_") for step in r["preview_steps"]))
        self.assertFalse(r["execution_allowed"])
        self.assertFalse(r["resource_reservations_created"])

    def test_native_preview_never_requests_container_resources(self):
        facts, auth, request = self.context()
        r = preview_install(self.native, facts, auth, request)
        self.assertTrue(all(step.startswith("NATIVE_") for step in r["preview_steps"]))

    def test_native_without_docker_or_hub_still_matches_synthetic_facts(self):
        facts, auth, request = self.context()
        facts["available_container_drivers"] = []
        request["hub_available"] = False
        self.assertEqual(
            preview_install(self.native, facts, auth, request)["compatibility"],
            "MATCHES_SYNTHETIC_FACTS_ONLY",
        )

    def test_missing_native_php_blocks_only_native(self):
        facts, auth, request = self.context()
        facts["php_fpm_available"] = False
        a = preview_install(self.native, facts, auth, request)
        b = preview_install(self.container, facts, auth, request)
        self.assertIn("NATIVE_PHP_FPM_UNAVAILABLE", a["blocking_reasons"])
        self.assertEqual(b["blocking_reasons"], [])

    def test_missing_native_database_denies_native(self):
        facts, auth, request = self.context()
        facts["native_db_engines"] = []
        self.assertIn("NATIVE_DATABASE_UNAVAILABLE",
                      preview_install(self.native, facts, auth, request)["blocking_reasons"])

    def test_no_container_driver_denies_only_container(self):
        facts, auth, request = self.context()
        facts["available_container_drivers"] = []
        a = preview_install(self.native, facts, auth, request)
        b = preview_install(self.container, facts, auth, request)
        self.assertEqual(a["blocking_reasons"], [])
        self.assertIn("CONTAINER_DRIVER_NOT_AVAILABLE", b["blocking_reasons"])

    def test_qualified_driver_names_are_not_interchangeable(self):
        facts, auth, request = self.context()
        facts["available_container_drivers"] = ["PODMAN"]
        r = preview_install(self.container, facts, auth, request)
        self.assertIn("CONTAINER_DRIVER_NOT_AVAILABLE", r["blocking_reasons"])

    def test_container_cpu_memory_pids_are_independent(self):
        facts, auth, request = self.context()
        facts["free_cpu_millicores"] = 1
        facts["free_memory_mib"] = 1
        facts["free_pids"] = 1
        reasons = preview_install(self.container, facts, auth, request)["blocking_reasons"]
        self.assertIn("CONTAINER_CPU_MILLICORES_BUDGET_UNAVAILABLE", reasons)
        self.assertIn("CONTAINER_MEMORY_MIB_BUDGET_UNAVAILABLE", reasons)
        self.assertIn("CONTAINER_PIDS_LIMIT_BUDGET_UNAVAILABLE", reasons)

    def test_site_not_owned_blocks_both_engines(self):
        facts, auth, request = self.context()
        request["target_site_id"] = "foreign-site"
        for recipe in (self.native, self.container):
            self.assertIn("SITE_OWNERSHIP_UNVERIFIED",
                          preview_install(recipe, facts, auth, request)["blocking_reasons"])

    def test_container_scope_missing_blocks_container(self):
        facts, auth, request = self.context()
        auth["container_permission_claimed"] = False
        self.assertIn("CONTAINER_SCOPE_UNVERIFIED",
                      preview_install(self.container, facts, auth, request)["blocking_reasons"])

    def test_forgepanel_reserved_ports_are_never_available(self):
        for port in (8446, 8447):
            with self.subTest(port=port):
                facts, auth, request = self.context()
                facts["reserved_host_tcp_ports"] = []
                request["host_tcp_ports"] = [port]
                self.assertIn(
                    "FORGEPANEL_OR_OTHER_RESERVED_PORT",
                    preview_install(self.container, facts, auth, request)["blocking_reasons"],
                )

    def test_observed_bound_port_cannot_be_reused(self):
        facts, auth, request = self.context()
        request["host_tcp_ports"] = [443]
        self.assertIn("HOST_PORT_ALREADY_CLAIMED",
                      preview_install(self.container, facts, auth, request)["blocking_reasons"])

    def test_free_host_port_is_still_unapproved_for_publication(self):
        facts, auth, request = self.context()
        request["host_tcp_ports"] = [9000]
        self.assertIn("HOST_PORT_PUBLICATION_NOT_APPROVED",
                      preview_install(self.container, facts, auth, request)["blocking_reasons"])

    def test_native_host_port_request_is_not_implicitly_authorized(self):
        facts, auth, request = self.context()
        request["host_tcp_ports"] = [9000]
        self.assertIn("HOST_PORT_PUBLICATION_NOT_APPROVED",
                      preview_install(self.native, facts, auth, request)["blocking_reasons"])

    def test_invalid_port_boolean_rejected(self):
        facts, auth, request = self.context()
        request["host_tcp_ports"] = [True]
        with self.assertRaises(RecipeContractError):
            preview_install(self.native, facts, auth, request)

    def test_duplicate_ports_rejected(self):
        facts, auth, request = self.context()
        request["host_tcp_ports"] = [9000, 9000]
        with self.assertRaises(RecipeContractError):
            preview_install(self.container, facts, auth, request)

    def test_huge_or_negative_capacity_rejected(self):
        for val in (True, -1, 2**31, "1024"):
            with self.subTest(value=val):
                facts, auth, request = self.context()
                facts["free_memory_mib"] = val
                with self.assertRaises(RecipeContractError):
                    preview_install(self.container, facts, auth, request)

    def test_unknown_host_fields_rejected_including_secrets(self):
        facts, auth, request = self.context()
        facts["sql_password"] = "never-in-preview"
        with self.assertRaises(RecipeContractError):
            preview_install(self.native, facts, auth, request)

    def test_unknown_request_fields_rejected_including_commands(self):
        facts, auth, request = self.context()
        request["shell_command"] = "sudo any-command"
        with self.assertRaises(RecipeContractError):
            preview_install(self.container, facts, auth, request)

    def test_client_cannot_claim_verified_context(self):
        facts, auth, request = self.context()
        facts["fixture_status"] = "VERIFIED"
        with self.assertRaises(RecipeContractError):
            preview_install(self.native, facts, auth, request)

    def test_unverified_ownership_never_turns_into_real_authorization(self):
        facts, auth, request = self.context()
        r = preview_install(self.native, facts, auth, request)
        for key in ("tenant_authorization_verified", "artifact_signature_verified",
                    "runtime_capabilities_verified", "port_probe_executed",
                    "external_reachability_verified", "resource_reservations_created"):
            self.assertIs(r[key], False, key)

    def test_recipe_with_untrusted_exec_field_rejected(self):
        facts, auth, request = self.context()
        recipe = copy.deepcopy(self.native)
        recipe["shell"] = "echo unexpected"
        with self.assertRaises(RecipeContractError):
            preview_install(recipe, facts, auth, request)

    def test_preview_is_deterministic_and_does_not_mutate_inputs(self):
        facts, auth, request = self.context()
        inputs = copy.deepcopy((self.native, facts, auth, request))
        a = preview_install(self.native, facts, auth, request)
        b = preview_install(self.native, facts, auth, request)
        self.assertEqual(a, b)
        self.assertEqual(inputs, (self.native, facts, auth, request))

    def test_synthetic_context_has_strict_version(self):
        facts, auth, request = self.context()
        request["schema_version"] = True
        with self.assertRaises(RecipeContractError):
            validate_synthetic_inputs(facts, auth, request)

    def test_host_without_owned_sites_is_not_implicitly_authorized(self):
        facts, auth, request = self.context()
        auth["authorized_site_ids"] = []
        self.assertIn("SITE_OWNERSHIP_UNVERIFIED",
                      preview_install(self.native, facts, auth, request)["blocking_reasons"])


    def test_host_facts_cannot_contain_site_permissions(self):
        facts, auth, request = self.context()
        facts["authorized_site_ids"] = ["owned-site"]
        with self.assertRaises(RecipeContractError):
            preview_install(self.native, facts, auth, request)

    def test_host_facts_cannot_assert_container_grants(self):
        facts, auth, request = self.context()
        facts["container_permission_claimed"] = True
        with self.assertRaises(RecipeContractError):
            preview_install(self.container, facts, auth, request)

    def test_client_request_cannot_supply_host_resources(self):
        facts, auth, request = self.context()
        request["free_memory_mib"] = 2000000
        with self.assertRaises(RecipeContractError):
            preview_install(self.container, facts, auth, request)

    def test_client_request_cannot_claim_authorization(self):
        facts, auth, request = self.context()
        request["authorized_site_ids"] = ["foreign-site"]
        with self.assertRaises(RecipeContractError):
            preview_install(self.native, facts, auth, request)

    def test_host_reference_mismatch_blocks_both_engines(self):
        facts, auth, request = self.context()
        auth["host_id"] = "different-host"
        for recipe in (self.native, self.container):
            result = preview_install(recipe, facts, auth, request)
            self.assertIn("HOST_SCOPE_MISMATCH", result["blocking_reasons"])
            self.assertFalse(result["execution_allowed"])

    def test_client_host_reference_mismatch_blocks(self):
        facts, auth, request = self.context()
        request["host_id"] = "other-host"
        self.assertIn("HOST_SCOPE_MISMATCH",
                      preview_install(self.native, facts, auth, request)["blocking_reasons"])

    def test_tenant_reference_mismatch_blocks_both_engines(self):
        facts, auth, request = self.context()
        request["tenant_id"] = "other-tenant"
        for recipe in (self.native, self.container):
            result = preview_install(recipe, facts, auth, request)
            self.assertIn("TENANT_SCOPE_MISMATCH", result["blocking_reasons"])

    def test_missing_authorization_scope_denies_both_engines(self):
        facts, auth, request = self.context()
        auth["authorized_site_ids"] = []
        for recipe in (self.native, self.container):
            self.assertIn("SITE_OWNERSHIP_UNVERIFIED",
                          preview_install(recipe, facts, auth, request)["blocking_reasons"])

    def test_client_cannot_pass_verified_authorization(self):
        facts, auth, request = self.context()
        auth["fixture_status"] = "VERIFIED"
        with self.assertRaises(RecipeContractError):
            preview_install(self.native, facts, auth, request)

    def test_authorization_context_cannot_embed_root_command(self):
        facts, auth, request = self.context()
        auth["root_command"] = "sudo bash"
        with self.assertRaises(RecipeContractError):
            preview_install(self.native, facts, auth, request)

    def test_identity_fields_need_strict_syntax(self):
        for field in ("actor_id", "tenant_id", "host_id"):
            with self.subTest(field=field):
                facts, auth, request = self.context()
                auth[field] = "bad\\ncontrol"
                with self.assertRaises(RecipeContractError):
                    preview_install(self.native, facts, auth, request)

    def test_input_provenance_is_explicitly_unverified(self):
        facts, auth, request = self.context()
        result = preview_install(self.native, facts, auth, request)
        self.assertEqual(result["input_trust"], {
            "host_capabilities": "SYNTHETIC_UNVERIFIED",
            "authorization_context": "SYNTHETIC_UNVERIFIED",
            "client_request": "UNTRUSTED_CANDIDATE",
        })
        self.assertIs(result["tenant_authorization_verified"], False)

    def test_no_hub_dependency_even_if_other_inputs_missing(self):
        facts, auth, request = self.context()
        request["hub_available"] = False
        facts["available_container_drivers"] = []
        self.assertNotIn("CONTAINER_DRIVER_NOT_AVAILABLE",
                         preview_install(self.native, facts, auth, request)["blocking_reasons"])


if __name__ == "__main__":
    unittest.main()
