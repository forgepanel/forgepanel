"""Q180/Q220 synthetic App Center inherited-policy preview tests. Not runtime authorization."""
from __future__ import annotations

import copy
import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))
from preview_app_center_inheritance import (  # noqa: E402
    IMMUTABLE_INVARIANTS, PolicyPreviewRejected, SCOPE_ORDER,
    resolve_synthetic_policy,
)

FIXTURE = ROOT / "evidence/app-center-fixtures/config-inheritance.synthetic.json"


class AppCenterPolicyInheritanceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.policy = json.loads(FIXTURE.read_text(encoding="utf-8"))

    def fresh(self):
        return copy.deepcopy(self.policy)

    def rejected(self, policy):
        with self.assertRaises(PolicyPreviewRejected):
            resolve_synthetic_policy(policy)

    def test_resolve_offline_fixture_without_apply(self):
        r = resolve_synthetic_policy(self.policy)
        self.assertEqual(r["policy_status"], "SYNTHETIC_CANDIDATE_ONLY")
        self.assertEqual(r["scope_order"], list(SCOPE_ORDER))
        self.assertEqual(r["effective"]["app.container.max_cpu_millicores"], 500)
        self.assertEqual(r["effective"]["app.container.max_memory_mib"], 2048)
        self.assertFalse(r["effective"]["app.container.allowed"])
        self.assertTrue(r["effective"]["app.native.allowed"])
        for key in ("authorization_verified", "host_capabilities_verified",
                    "physical_capacity_verified", "policy_signature_verified",
                    "audit_written", "resource_reservations_created",
                    "execution_allowed", "apply_available"):
            self.assertIs(r[key], False, key)

    def test_provenance_is_readable_without_secrets(self):
        r = resolve_synthetic_policy(self.policy)
        chain = r["provenance"]["app.container.max_cpu_millicores"]
        self.assertEqual([x["scope"] for x in chain],
                         ["global", "server", "organization", "plan", "site"])
        self.assertEqual([x["synthetic_value"] for x in chain],
                         [4000, 2400, 1800, 1000, 500])
        self.assertEqual(r["root_numeric_values_are"],
                         "FICTIONAL_NOT_PRODUCTION_LIMITS")

    def test_immutable_security_invariants_cannot_be_changed(self):
        for key in IMMUTABLE_INVARIANTS:
            with self.subTest(key=key):
                p = self.fresh()
                p["layers"][4]["changes"][key] = True
                self.rejected(p)

    def test_hub_cannot_become_mandatory(self):
        self.assertIs(resolve_synthetic_policy(self.policy)["immutable_invariants"]
                      ["app.core.hub_required"], False)
        self.assertIs(resolve_synthetic_policy(self.policy)["immutable_invariants"]
                      ["app.native.premium_required"], False)

    def test_ports_8446_and_8447_are_hard_reservations(self):
        v = resolve_synthetic_policy(self.policy)["immutable_invariants"]
        self.assertEqual(v["app.system.reserved_tcp_ports"], [8446, 8447])

    def test_reject_child_reenabling_disabled_containers(self):
        p = self.fresh()
        p["layers"][4]["changes"]["app.container.allowed"] = True
        self.rejected(p)

    def test_reject_child_increasing_cpu_above_plan(self):
        p = self.fresh()
        p["layers"][4]["changes"]["app.container.max_cpu_millicores"] = 2000
        self.rejected(p)

    def test_reject_child_increasing_memory(self):
        p = self.fresh()
        p["layers"][4]["changes"]["app.container.max_memory_mib"] = 8192
        self.rejected(p)

    def test_bool_is_not_integer_limit(self):
        p = self.fresh()
        p["layers"][0]["changes"]["app.container.max_pids"] = True
        self.rejected(p)

    def test_limit_must_be_positive_and_bounded(self):
        for value in (0, -1, 2**31, "1000", 3.5):
            with self.subTest(value=value):
                p = self.fresh()
                p["layers"][1]["changes"]["app.container.max_pids"] = value
                self.rejected(p)

    def test_enabled_flags_are_strict_bool(self):
        p = self.fresh()
        p["layers"][0]["changes"]["app.native.allowed"] = "true"
        self.rejected(p)

    def test_global_must_define_all_demo_keys(self):
        p = self.fresh()
        del p["layers"][0]["changes"]["app.native.allowed"]
        self.rejected(p)

    def test_unknown_config_key_denied(self):
        p = self.fresh()
        p["layers"][2]["changes"]["app.security.disable_rbac"] = True
        self.rejected(p)

    def test_unrecognized_scope_denied(self):
        p = self.fresh()
        p["layers"][4]["scope"] = "root-user"
        self.rejected(p)

    def test_scope_reorder_denied(self):
        p = self.fresh()
        p["layers"][2], p["layers"][3] = p["layers"][3], p["layers"][2]
        self.rejected(p)

    def test_partial_chain_not_claimed_authorized(self):
        p = self.fresh()
        p["layers"].pop()
        self.rejected(p)

    def test_missing_tenant_site_identity_denied(self):
        p = self.fresh()
        del p["subject"]["site_id"]
        self.rejected(p)

    def test_injection_in_subject_denied(self):
        p = self.fresh()
        p["subject"]["server_id"] = "fixture-server;sudo"
        self.rejected(p)

    def test_unrecognized_root_field_denied(self):
        p = self.fresh()
        p["root_command"] = "bash -c echo"
        self.rejected(p)

    def test_client_claim_of_verified_policy_denied(self):
        p = self.fresh()
        p["status"] = "VERIFIED"
        self.rejected(p)

    def test_client_claim_of_product_default_denied(self):
        p = self.fresh()
        p["numeric_values_are"] = "PRODUCTION_DEFAULTS"
        self.rejected(p)

    def test_nested_mutation_does_not_change_source(self):
        before = copy.deepcopy(self.policy)
        out = resolve_synthetic_policy(self.policy)
        out["immutable_invariants"]["app.system.reserved_tcp_ports"].append(22)
        self.assertEqual(self.policy, before)
        self.assertEqual(IMMUTABLE_INVARIANTS["app.system.reserved_tcp_ports"],
                         [8446, 8447])

    def test_repeatable_preview(self):
        self.assertEqual(resolve_synthetic_policy(self.policy),
                         resolve_synthetic_policy(self.policy))

    def test_explicit_q180_hierarchy_and_overridden_false(self):
        r = resolve_synthetic_policy(self.policy)
        self.assertEqual(r["scope_order"],
                         ["global", "server", "organization", "plan", "site"])
        self.assertEqual(r["provenance"]["app.container.allowed"][-1],
                         {"scope": "plan", "synthetic_value": False})

    def test_cannot_add_account_or_user_scope_implicitly(self):
        p = self.fresh()
        p["layers"].append({"scope": "user", "changes": {"app.native.allowed": True}})
        self.rejected(p)

    def test_documentation_pair_present(self):
        for lang in ("en", "fr"):
            text = (ROOT / "DOCUMENTATION" / lang /
                    "02-architecture/app-center-config-inheritance.md").read_text(encoding="utf-8")
            self.assertIn("FP-02-APP-CONFIG", text)
            self.assertIn("Q180", text)
            self.assertIn("Q220", text)
            self.assertIn("PLANNED", text)
            self.assertIn("preview_app_center_inheritance.py", text)


if __name__ == "__main__":
    unittest.main()
