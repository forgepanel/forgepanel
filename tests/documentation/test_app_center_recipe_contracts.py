#!/usr/bin/env python3
"""Negative/offline candidate App Center recipe tests; no executable installer."""
from __future__ import annotations

import copy
import json
import re
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))
from validate_app_center_recipe import FIXTURES, RecipeContractError, validate_recipe  # noqa: E402


class RecipeDiscriminatorTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.native = json.loads((FIXTURES / "native-cms.v1.json").read_text())
        cls.container = json.loads((FIXTURES / "container-worker.v1.json").read_text())

    def native_copy(self):
        return copy.deepcopy(self.native)

    def container_copy(self):
        return copy.deepcopy(self.container)

    def rejected(self, doc, contains):
        with self.assertRaises(RecipeContractError) as out:
            validate_recipe(doc)
        self.assertIn(contains, str(out.exception))

    def test_native_fixture_is_metadata_only(self):
        self.assertEqual(validate_recipe(self.native), "native_script")
        self.assertIs(self.native["execution_allowed"], False)

    def test_container_fixture_is_metadata_only(self):
        self.assertEqual(validate_recipe(self.container), "container_stack")
        self.assertIs(self.container["execution_allowed"], False)

    def test_same_app_can_have_two_independent_variant_ids(self):
        other = self.container_copy()
        other["app_id"] = self.native["app_id"]
        self.assertNotEqual(other["variant_id"], self.native["variant_id"])
        self.assertEqual(validate_recipe(other), "container_stack")

    def test_unknown_kind_is_denied(self):
        item = self.native_copy()
        item["recipe_kind"] = "universal"
        self.rejected(item, "REJECT_TYPE_MISMATCH")

    def test_native_with_container_section_denied(self):
        item = self.native_copy()
        item["container"] = self.container["container"]
        self.rejected(item, "REJECT_UNREVIEWED_FIELD")

    def test_container_with_native_section_denied(self):
        item = self.container_copy()
        item["native"] = self.native["native"]
        self.rejected(item, "REJECT_UNREVIEWED_FIELD")

    def test_wrong_variant_structure_denied(self):
        item = self.native_copy()
        item["recipe_kind"] = "container_stack"
        self.rejected(item, "REJECT_UNREVIEWED_FIELD")

    def test_execution_allowed_true_denied(self):
        item = self.native_copy()
        item["execution_allowed"] = True
        self.rejected(item, "REJECT_UNAPPROVED_EXECUTION")

    def test_approved_status_denied(self):
        item = self.container_copy()
        item["contract_status"] = "APPROVED"
        self.rejected(item, "REJECT_UNAPPROVED_EXECUTION")

    def test_direct_script_or_shell_field_denied(self):
        for name in ("shell", "command", "hooks", "compose_file", "raw_compose",
                     "post_install_script", "env_file", "host_path", "privileged"):
            with self.subTest(field=name):
                item = self.native_copy()
                item[name] = "rm -rf /"
                self.rejected(item, "REJECT_UNREVIEWED_FIELD")

    def test_untrusted_or_non_https_archive_denied(self):
        for origin in ("http://example.invalid/x", "file:///etc/passwd",
                       "https://127.0.0.1/x", "https://root:pass@example.invalid/x",
                       "https://example.invalid/one?token=value",
                       "https://example.invalid:12345/x"):
            with self.subTest(origin=origin):
                item = self.native_copy()
                item["artifact"]["source_url"] = origin
                self.rejected(item, "REJECT_UNTRUSTED_ARTIFACT")

    def test_missing_or_malformed_checksum_denied(self):
        for value in ("", "a" * 63, "not-a-digest", "g" * 64):
            with self.subTest(value=value[:12]):
                item = self.native_copy()
                item["artifact"]["sha256"] = value
                self.rejected(item, "REJECT_UNREVIEWED_FIELD")

    def test_nonverified_provenance_cannot_claim_approval(self):
        item = self.container_copy()
        item["artifact"]["provenance_state"] = "SIGNED_AND_VERIFIED"
        self.rejected(item, "REJECT_UNAPPROVED_EXECUTION")

    def test_licenses_cannot_be_missing(self):
        item = self.native_copy()
        item["artifact"]["license_id"] = ""
        self.rejected(item, "REJECT_UNREVIEWED_FIELD")

    def test_native_docker_dependency_denied(self):
        item = self.native_copy()
        item["native"]["requires_container_runtime"] = True
        self.rejected(item, "REJECT_TYPE_MISMATCH")

    def test_native_foreign_site_scope_denied(self):
        item = self.native_copy()
        item["native"]["site_scope"] = "ALL_SITES"
        self.rejected(item, "REJECT_TYPE_MISMATCH")

    def test_native_runtime_unknown_denied(self):
        item = self.native_copy()
        item["native"]["runtime"] = "ROOT_SHELL"
        self.rejected(item, "BLOCKED_CAPABILITY")

    def test_native_extensions_must_be_unique_and_bounded(self):
        item = self.native_copy()
        item["native"]["required_extensions"] = ["pdo_mysql", "pdo_mysql"]
        self.rejected(item, "REJECT_UNREVIEWED_FIELD")

    def test_container_requires_pinned_digest(self):
        item = self.container_copy()
        item["container"]["images"][0]["digest"] = "latest"
        self.rejected(item, "REJECT_UNTRUSTED_ARTIFACT")

    def test_container_driver_independently_declared(self):
        item = self.container_copy()
        item["container"]["driver"] = "PODMAN"
        self.assertEqual(validate_recipe(item), "container_stack")
        item["container"]["driver"] = "COMPOSE_AUTO"
        self.rejected(item, "BLOCKED_CAPABILITY")

    def test_container_no_privileged_or_socket_mount(self):
        for field in ("privileged", "host_mounts", "engine_socket_mount"):
            with self.subTest(field=field):
                item = self.container_copy()
                item["container"][field] = True
                self.rejected(item, "REJECT_UNREVIEWED_FIELD")

    def test_host_networking_denied(self):
        item = self.container_copy()
        item["container"]["network_mode"] = "HOST"
        self.rejected(item, "REJECT_UNREVIEWED_FIELD")

    def test_container_cannot_expose_host_ports_implicitly(self):
        item = self.container_copy()
        item["container"]["ports"][0]["exposure"] = "HOST_PUBLIC"
        self.rejected(item, "REJECT_UNREVIEWED_FIELD")

    def test_container_resource_requests_must_be_positive_not_booleans(self):
        for val in (0, -1, True, "500", 2**31):
            with self.subTest(value=val):
                item = self.container_copy()
                item["container"]["cpu_millicores"] = val
                self.rejected(item, "REJECT_UNREVIEWED_FIELD")

    def test_container_rejects_arbitrary_volume_path(self):
        item = self.container_copy()
        item["container"]["volumes"] = ["/etc/ssh"]
        self.rejected(item, "REJECT_UNREVIEWED_FIELD")

    def test_no_duplicate_ports(self):
        item = self.container_copy()
        item["container"]["ports"] *= 2
        self.rejected(item, "REJECT_UNREVIEWED_FIELD")

    def test_no_unbounded_image_list(self):
        item = self.container_copy()
        item["container"]["images"] = []
        self.rejected(item, "REJECT_UNREVIEWED_FIELD")

    def test_port_number_is_integer_not_boolean(self):
        item = self.container_copy()
        item["container"]["ports"][0]["container_port"] = True
        self.rejected(item, "REJECT_UNREVIEWED_FIELD")

    def test_cannot_describe_custom_root_exec_plan(self):
        for kind in ("native_script", "container_stack"):
            item = self.native_copy() if kind == "native_script" else self.container_copy()
            item["run_as_root"] = True
            self.rejected(item, "REJECT_UNREVIEWED_FIELD")

    def test_bilingual_contract_refs_exist(self):
        for lang in ("fr", "en"):
            content=(ROOT / "DOCUMENTATION" / lang / "08-api-contracts" / "app-center-recipe-contracts.md").read_text()
            self.assertIn("FP-08-APP-RECIPE", content)
            self.assertIn("CANDIDATE_ONLY", content)
            self.assertIn("native_script", content)
            self.assertIn("container_stack", content)
            self.assertIn("Q171+", content)


if __name__ == "__main__":
    unittest.main()
