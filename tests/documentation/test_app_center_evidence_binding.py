#!/usr/bin/env python3
"""Offline candidate evidence checks for Q180/Q220: NOT real authentication or IPC."""
from __future__ import annotations

import copy
import json
import re
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))
from check_app_center_candidate_evidence import (  # noqa: E402
    AUTHZ_KEYS, HOST_KEYS, INTENT_KEYS, POLICY_KEYS, TOP_KEYS,
    ContextRejected, FIXTURES, review_candidate_context, load_synthetic,
)


class AppCenterCandidateEvidenceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.native = json.loads((FIXTURES / "admission-native.synthetic.json").read_text())
        cls.container = json.loads((FIXTURES / "admission-container.synthetic.json").read_text())

    def sample(self, kind="native"):
        return copy.deepcopy(self.container if kind == "container" else self.native)

    def blocked(self, record, reason):
        result = review_candidate_context(record)
        self.assertEqual(result["review_status"], "BLOCKED_SYNTHETIC")
        self.assertIn(reason, result["blocking_reasons"])
        self.assertIs(result["execution_allowed"], False)
        self.assertIs(result["apply_available"], False)

    def refused(self, record):
        with self.assertRaises(ContextRejected):
            review_candidate_context(record)

    def test_native_fixture_matches_synthetic_context_only(self):
        r = review_candidate_context(self.native)
        self.assertEqual(r["review_status"], "MATCHES_SYNTHETIC_CONTEXT_ONLY")
        self.assertEqual(r["blocking_reasons"], [])
        self.assertEqual(r["recipe_kind"], "native_script")
        self.assertEqual(r["source_trust"]["clock"], "SYNTHETIC_UNVERIFIED")

    def test_container_fixture_matches_synthetic_context_only(self):
        r = review_candidate_context(self.container)
        self.assertEqual(r["review_status"], "MATCHES_SYNTHETIC_CONTEXT_ONLY")
        self.assertEqual(r["recipe_kind"], "container_stack")
        self.assertEqual(r["blocking_reasons"], [])

    def test_both_never_become_approved(self):
        for x in (self.native, self.container):
            r = review_candidate_context(x)
            for field in ("actor_authenticated", "host_identity_verified",
                          "policy_signature_verified", "resource_reservations_created",
                          "authorization_approved", "execution_allowed",
                          "apply_available"):
                self.assertIs(r[field], False, field)

    def test_expired_host_observation_blocks(self):
        x = self.sample()
        x["host_observation"]["expires_at_utc"] = "2026-11-06T10:00:29Z"
        self.blocked(x, "HOST_EVIDENCE_STALE")

    def test_expired_core_authorization_blocks(self):
        x = self.sample()
        x["core_authorization"]["expires_at_utc"] = "2026-11-06T10:00:29Z"
        self.blocked(x, "AUTHORIZATION_EVIDENCE_STALE")

    def test_expired_policy_snapshot_blocks(self):
        x = self.sample()
        x["core_policy"]["expires_at_utc"] = "2026-11-06T10:00:29Z"
        self.blocked(x, "POLICY_EVIDENCE_STALE")

    def test_future_dated_observation_blocks(self):
        x = self.sample()
        x["host_observation"]["observed_at_utc"] = "2026-11-06T10:00:31Z"
        self.blocked(x, "HOST_EVIDENCE_FUTURE_OR_INVALID")

    def test_reversed_snapshot_window_blocks(self):
        x = self.sample()
        x["core_policy"]["expires_at_utc"] = x["core_policy"]["observed_at_utc"]
        self.blocked(x, "POLICY_EVIDENCE_FUTURE_OR_INVALID")

    def test_timestamp_bad_format_refused(self):
        x = self.sample()
        x["synthetic_clock_utc"] = "2026-11-06 10:00"
        self.refused(x)

    def test_timestamp_calendar_invalid_refused(self):
        x = self.sample()
        x["host_observation"]["observed_at_utc"] = "2026-02-30T10:00:00Z"
        self.refused(x)

    def test_wrong_host_in_authorization_blocks(self):
        x = self.sample()
        x["core_authorization"]["host_id"] = "other-host"
        self.blocked(x, "HOST_CONTEXT_MISMATCH")

    def test_wrong_host_in_policy_blocks(self):
        x = self.sample()
        x["core_policy"]["host_id"] = "other-host"
        self.blocked(x, "HOST_CONTEXT_MISMATCH")

    def test_wrong_host_in_request_blocks(self):
        x = self.sample()
        x["user_intent"]["host_id"] = "other-host"
        self.blocked(x, "HOST_CONTEXT_MISMATCH")

    def test_wrong_tenant_blocks(self):
        x = self.sample()
        x["user_intent"]["tenant_id"] = "another-tenant"
        self.blocked(x, "TENANT_CONTEXT_MISMATCH")

    def test_wrong_actor_blocks(self):
        x = self.sample()
        x["user_intent"]["actor_id"] = "another-actor"
        self.blocked(x, "ACTOR_CONTEXT_MISMATCH")

    def test_foreign_site_blocks(self):
        x = self.sample()
        x["user_intent"]["site_id"] = "other-site"
        self.blocked(x, "SITE_OWNERSHIP_UNVERIFIED")

    def test_missing_native_plan_permission_blocks(self):
        x = self.sample()
        x["core_authorization"]["allowed_plan_scopes"] = ["app.container.plan"]
        self.blocked(x, "NATIVE_PLAN_SCOPE_MISSING")

    def test_missing_container_plan_permission_blocks(self):
        x = self.sample("container")
        x["core_authorization"]["allowed_plan_scopes"] = ["app.native.plan"]
        self.blocked(x, "CONTAINER_PLAN_SCOPE_MISSING")

    def test_unverified_context_does_not_promote_permissions(self):
        x = self.sample()
        x["core_authorization"]["source"] = "VERIFIED_CORE_RBAC"
        self.refused(x)

    def test_fake_signed_policy_source_refused(self):
        x = self.sample()
        x["core_policy"]["source"] = "SIGNED_PRODUCTION_POLICY"
        self.refused(x)

    def test_request_cannot_supply_root_shell(self):
        x = self.sample()
        x["user_intent"]["shell.exec"] = "root"
        self.refused(x)

    def test_request_cannot_supply_host_capability_evidence(self):
        x = self.sample()
        x["user_intent"]["free_memory_mib"] = 900000
        self.refused(x)

    def test_request_cannot_supply_entitlement(self):
        x = self.sample()
        x["user_intent"]["premium_required"] = True
        self.refused(x)

    def test_request_stale_host_revision_blocks(self):
        x = self.sample()
        x["user_intent"]["expected_host_snapshot_revision"] = 4
        self.blocked(x, "EXPECTED_REVISION_STALE")

    def test_request_stale_authorization_revision_blocks(self):
        x = self.sample()
        x["user_intent"]["expected_authorization_revision"] = 6
        self.blocked(x, "EXPECTED_REVISION_STALE")

    def test_request_stale_policy_revision_blocks(self):
        x = self.sample()
        x["user_intent"]["expected_policy_revision"] = 10
        self.blocked(x, "EXPECTED_REVISION_STALE")

    def test_boolean_in_revision_refused(self):
        x = self.sample()
        x["user_intent"]["expected_policy_revision"] = True
        self.refused(x)

    def test_invalid_integer_capacity_refused(self):
        for value in (-1, 2**31, "512", True):
            with self.subTest(value=value):
                x = self.sample("container")
                x["host_observation"]["free_memory_mib"] = value
                self.refused(x)

    def test_missing_protected_port_in_inventory_blocks(self):
        x = self.sample()
        x["host_observation"]["protected_host_tcp_ports"] = [8447]
        self.blocked(x, "CONTROL_PLANE_PORT_INVENTORY_INCOMPLETE")

    def test_forgepanel_port_8447_always_blocked(self):
        x = self.sample("container")
        x["user_intent"]["requested_host_tcp_ports"] = [8447]
        self.blocked(x, "CONTROL_PLANE_OR_RESERVED_PORT_COLLISION")

    def test_panel_port_8446_always_blocked(self):
        x = self.sample("container")
        x["user_intent"]["requested_host_tcp_ports"] = [8446]
        self.blocked(x, "CONTROL_PLANE_OR_RESERVED_PORT_COLLISION")

    def test_other_host_port_does_not_auto_expose(self):
        x = self.sample("container")
        x["user_intent"]["requested_host_tcp_ports"] = [9000]
        self.blocked(x, "HOST_PORT_EXPOSURE_POLICY_UNAPPROVED")

    def test_duplicate_ports_refused(self):
        x = self.sample()
        x["user_intent"]["requested_host_tcp_ports"] = [9000, 9000]
        self.refused(x)

    def test_boolean_port_refused(self):
        x = self.sample()
        x["user_intent"]["requested_host_tcp_ports"] = [True]
        self.refused(x)

    def test_native_does_not_require_container_engine(self):
        x = self.sample()
        x["host_observation"]["engines_present"] = ["NATIVE_SITE"]
        x["core_policy"]["qualified_container_drivers"] = []
        self.assertEqual(review_candidate_context(x)["review_status"],
                         "MATCHES_SYNTHETIC_CONTEXT_ONLY")

    def test_native_cannot_smuggle_container_driver(self):
        x = self.sample()
        x["user_intent"]["requested_driver"] = "DOCKER"
        self.blocked(x, "NATIVE_REQUEST_MIXES_CONTAINER_RESOURCES")

    def test_native_cannot_smuggle_container_cpu(self):
        x = self.sample()
        x["user_intent"]["requested_cpu_millicores"] = 250
        self.blocked(x, "NATIVE_REQUEST_MIXES_CONTAINER_RESOURCES")

    def test_container_docker_podman_not_interchangeable(self):
        x = self.sample("container")
        x["user_intent"]["requested_driver"] = "PODMAN"
        self.blocked(x, "CONTAINER_DRIVER_NOT_QUALIFIED")

    def test_container_engine_not_present_blocks(self):
        x = self.sample("container")
        x["host_observation"]["engines_present"] = ["NATIVE_SITE"]
        self.blocked(x, "CONTAINER_DRIVER_NOT_QUALIFIED")

    def test_container_policy_denies_blocks(self):
        x = self.sample("container")
        x["core_policy"]["container_enabled"] = False
        self.blocked(x, "CONTAINER_DISABLED_BY_POLICY")

    def test_container_cpu_shortfall_blocks(self):
        x = self.sample("container")
        x["user_intent"]["requested_cpu_millicores"] = 1000
        self.blocked(x, "CONTAINER_SYNTHETIC_BUDGET_INSUFFICIENT")

    def test_container_memory_shortfall_blocks(self):
        x = self.sample("container")
        x["user_intent"]["requested_memory_mib"] = 1100
        self.blocked(x, "CONTAINER_SYNTHETIC_BUDGET_INSUFFICIENT")

    def test_container_empty_capacity_request_blocks(self):
        x = self.sample("container")
        x["user_intent"]["requested_cpu_millicores"] = 0
        self.blocked(x, "CONTAINER_RESOURCE_REQUEST_MISSING")

    def test_forged_fixture_status_refused(self):
        x = self.sample()
        x["fixture_status"] = "VERIFIED_PRODUCTION"
        self.refused(x)

    def test_bad_idempotency_key_refused(self):
        x = self.sample()
        x["user_intent"]["idempotency_key"] = "rm -rf /"
        self.refused(x)

    def test_unknown_scope_refused(self):
        x = self.sample()
        x["core_authorization"]["allowed_plan_scopes"] = ["app.admin.shell"]
        self.refused(x)

    def test_unknown_kind_refused(self):
        x = self.sample()
        x["user_intent"]["recipe_kind"] = "generic_script"
        self.refused(x)

    def test_cannot_claim_unsigned_capability_source_as_proof(self):
        x = self.sample()
        x["host_observation"]["source"] = "SIGNED_TRUSTED_AGENT"
        self.refused(x)

    def test_no_mutation_or_live_clock(self):
        x = self.sample("container")
        unchanged = copy.deepcopy(x)
        a = review_candidate_context(x)
        b = review_candidate_context(x)
        self.assertEqual(a, b)
        self.assertEqual(x, unchanged)
        self.assertEqual(a["source_trust"]["clock"], "SYNTHETIC_UNVERIFIED")

    def test_cli_is_restricted_to_bundled_examples(self):
        with self.assertRaises(ContextRejected):
            load_synthetic(Path("/etc/passwd"))

    def test_bilingual_contracts_are_mirrored(self):
        for lang in ("fr", "en"):
            text = (ROOT / "DOCUMENTATION" / lang /
                    "08-api-contracts/app-center-admission-evidence.md").read_text(encoding="utf-8")
            self.assertIn("FP-08-APP-EVIDENCE", text)
            self.assertIn("Q220", text)
            self.assertIn("SYNTHETIC_UNVERIFIED", text)
            self.assertIn("NOT EXECUTED" if lang == "en" else "NON EXÉCUTÉ", text)

    def test_candidate_json_schema_covers_the_four_distinct_sources(self):
        path = ROOT / "evidence/app-center-admission.synthetic-v1.schema.json"
        schema = json.loads(path.read_text(encoding="utf-8"))
        self.assertEqual(schema["$schema"], "https://json-schema.org/draft/2020-12/schema")
        self.assertIn("synthetic", schema["$id"])
        self.assertEqual(set(schema["required"]), TOP_KEYS)
        self.assertIs(schema["additionalProperties"], False)
        self.assertEqual(schema["properties"]["fixture_status"]["const"],
                         "SYNTHETIC_UNVERIFIED")
        for name, expected, source in (
            ("host_observation", HOST_KEYS, "UNVERIFIED_OS_PROBE_FIXTURE"),
            ("core_authorization", AUTHZ_KEYS, "UNVERIFIED_SYMFONY_FIXTURE"),
            ("core_policy", POLICY_KEYS, "UNVERIFIED_CONFIG_FIXTURE"),
            ("user_intent", INTENT_KEYS, "UNTRUSTED_CLIENT_FIXTURE"),
        ):
            field = schema["properties"][name]
            self.assertEqual(set(field["required"]), expected)
            self.assertIs(field["additionalProperties"], False)
            self.assertEqual(field["properties"]["source"]["const"], source)
        self.assertNotIn("shell.exec", schema["properties"]["user_intent"]["properties"])
        self.assertNotIn("apply", schema["properties"])

    def test_planned_real_evidence_gates_have_exact_bilingual_parity(self):
        expected = {f"TEST-EVID-FP-{n:04d}" for n in range(1, 13)}
        for lang in ("fr", "en"):
            doc = (ROOT / "DOCUMENTATION" / lang /
                   "13-tests-quality/app-center-evidence-gates.md").read_text(encoding="utf-8")
            self.assertTrue(doc.startswith(
                "<!-- forgepanel-doc id=FP-13-APP-EVIDENCE revision=1 status=specified -->"
            ))
            ids = re.findall(r"^\| (TEST-EVID-FP-\d{4}) \|", doc, re.M)
            self.assertEqual(set(ids), expected)
            self.assertEqual(len(ids), 12)
            self.assertIn("PLANNED", doc)
            self.assertNotIn("| PASS |", doc)


if __name__ == "__main__":
    unittest.main()
