"""Static candidate R3 physical PG, Linux and execution checks; no runtime effects."""
import json
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DOC = ROOT / "DOCUMENTATION"
EVIDENCE = DOC / "evidence"
DOCS = {
    "09-database/physical-jobs-model-r3.md": ("FP-09-R3-PHYSICAL-JOBS", "DBPH-FP-"),
    "14-devops-releases/linux-service-identities-r3.md": ("FP-14-R3-LINUX-IDENTITY", "LINUX-FP-"),
    "08-api-contracts/typed-execution-recovery-r3.md": ("FP-08-R3-TYPED-EXECUTION", "EXEC-FP-"),
    "13-tests-quality/r3-physical-execution-gates.md": ("FP-13-R3-PHYSICAL-QA", None),
}
PREFIXES = ("R3-PHYS-TEST-", "R3-LINUX-TEST-", "R3-EXEC-TEST-")
EXPECTED_TABLES = {
    "fp_operation_intents", "fp_job_executions", "fp_resource_leases",
    "fp_job_step_events", "fp_agent_outbox", "fp_agent_inbox",
    "fp_recovery_checkpoints", "fp_job_audit_events",
}
EXPECTED_IDENTITIES = {
    "panel_http", "panel_ipc_bridge", "panel_agent", "panel_privileged_handler",
    "panel_migrator", "panel_db_runtime", "hosted_site_user", "panel_observer",
}

def load(name):
    return json.loads((EVIDENCE / name).read_text(encoding="utf-8"))

class CandidatePhysicalBoundaries(unittest.TestCase):
    def test_french_english_requirements_and_metadata(self):
        for relative, (id_, prefix) in DOCS.items():
            versions = []
            for lang in ("fr", "en"):
                raw = (DOC / lang / relative).read_text(encoding="utf-8")
                match = re.search(
                    rf"<!-- forgepanel-doc id={re.escape(id_)} revision=([1-9]\d*) status=specified -->",
                    raw,
                )
                self.assertIsNotNone(match, f"{lang}/{relative}")
                versions.append(match.group(1))
                self.assertIn("PLANNED" if prefix is None else "CANDIDATE", raw)
                self.assertIn("SRC-03" if relative.startswith("09-database/") else "R1", raw)
                self.assertIn("R2", raw)
                if prefix:
                    actual = set(re.findall(rf"\b{re.escape(prefix)}\d{{4}}\b", raw))
                    self.assertEqual(actual, {f"{prefix}{i:04d}" for i in range(1, 13)},
                                     f"{lang}/{relative}")
            self.assertEqual(versions[0], versions[1])

    def test_36_planned_qa_scenarios_in_same_order(self):
        expected = {f"{p}{n:03d}" for p in PREFIXES for n in range(1, 13)}
        orders = []
        for lang in ("fr", "en"):
            raw = (DOC / lang / "13-tests-quality/r3-physical-execution-gates.md").read_text()
            rows = [x for x in raw.splitlines() if x.startswith("| " + chr(96) + "R3-")]
            found = [re.match(r"^\| .(R3-(?:PHYS|LINUX|EXEC)-TEST-\d{3}).", r).group(1)
                     for r in rows]
            self.assertEqual(len(found), 36)
            self.assertEqual(set(found), expected)
            self.assertTrue(all(row.rstrip().endswith("| **PLANNED** |") for row in rows))
            orders.append(found)
        self.assertEqual(orders[0], orders[1])

    def test_physical_db_map_has_no_authorized_ddl(self):
        m = load("candidate-r3-physical-data-model-v1.json")
        self.assertEqual(m["status"], "SPECIFIED_NOT_APPROVED")
        self.assertIs(m["not_sql_migration"], True)
        for k in ("has_been_applied", "authorized_to_create_tables", "production_compatible",
                  "original_source_imported", "tenant_foreign_key_model_decided"):
            self.assertIs(m[k], False, k)
        self.assertEqual(set(m["existing_prototype_tables_observed_only"]),
                         {"fp_setup", "fp_admins", "fp_setup_audit"})
        tables = m["candidate_tables"]
        self.assertEqual({t["name"] for t in tables}, EXPECTED_TABLES)
        for table in tables:
            cols = {c["column"] for c in table["columns"]}
            self.assertEqual(len(cols), len(table["columns"]))
            self.assertTrue(set(table["primary_key"]) <= cols)
            self.assertTrue(all(c["approved"] is False for c in table["columns"]))
            self.assertTrue(all(set(u) <= cols for u in table["unique_constraints"]))
            for fk in table["foreign_keys_candidacy"]:
                self.assertTrue(set(fk["columns"]) <= cols)
                self.assertIn(fk["references"]["table"], EXPECTED_TABLES)
                self.assertEqual(fk["status"], "CANDIDATE")
        by_name = {t["name"]: t for t in tables}
        key = ["scope_kind", "scope_ref", "resource_kind", "resource_ref",
               "operation_id", "idempotency_fingerprint"]
        self.assertIn(key, by_name["fp_operation_intents"]["unique_constraints"])
        self.assertIn(key[:4], by_name["fp_resource_leases"]["unique_constraints"])
        self.assertIn("effect_boundary_revalidation_mandatory", by_name["fp_resource_leases"]["guards"])
        self.assertEqual(len(m["tests"]), 12)

    def test_linux_identities_not_created_or_privileged(self):
        m = load("candidate-r3-linux-service-boundaries-v1.json")
        self.assertEqual(m["status"], "SPECIFIED_NOT_APPROVED")
        for key in ("user_accounts_created", "service_units_created", "socket_created",
                    "privileged_handlers_enabled", "selected_uid_gid", "selected_socket_path",
                    "hub_can_authorize_privileged_core_action", "dynamic_user_policy_selected"):
            self.assertIs(m[key], False)
        self.assertTrue(m["authn_does_not_imply_authz"])
        identities = m["identities"]
        self.assertEqual({x["logical_identity"] for x in identities}, EXPECTED_IDENTITIES)
        for identity in identities:
            self.assertIs(identity["unix_account_selected"], False)
            self.assertIs(identity["created_in_linux"], False)
            self.assertIs(identity["activated"], False)
            self.assertTrue(identity["explicit_denials"])
        privileged = next(x for x in identities
                          if x["logical_identity"] == "panel_privileged_handler")
        self.assertEqual(privileged["role_class"], "FUTURE_PRIVILEGED_DISABLED")
        self.assertEqual(privileged["allowed_candidate_responsibilities"], [])
        self.assertIn("verified_kernel_peer_credentials", m["socket_trust_requires"])

    def test_execution_registry_cannot_authorize_linux(self):
        m = load("candidate-typed-execution-guards-v1.json")
        old = load("typed-agent-operations-v1.json")
        self.assertEqual(m["status"], "SPECIFIED_NOT_APPROVED")
        self.assertEqual(m["approved_handlers"], [])
        for flag in ("live_dispatcher_implemented", "privileged_executor_implemented",
                     "execution_authority_granted", "public_core_hub_dependency"):
            self.assertIs(m[flag], False)
        for flag in ("all_operations_require_current_actor_scope",
                     "all_mutating_operations_require_fencing_at_effect",
                     "success_requires_observed_effect", "no_generic_shell",
                     "no_qemu_raw_args", "no_exactly_once_pg_linux_claim"):
            self.assertIs(m[flag], True)
        known = {x["id"]: x for x in old["operations"]}
        self.assertEqual({x["id"] for x in m["operations"]}, set(known))
        self.assertEqual(len(m["operations"]), 7)
        for x in m["operations"]:
            self.assertEqual(x["operation_id"], known[x["id"]]["name"])
            self.assertEqual(x["operation_status"], known[x["id"]]["status"])
            for key in ("implemented", "authorized_for_linux_apply", "linux_effect_observed"):
                self.assertIs(x[key], False)
            self.assertEqual(x["retry_when_external_effect_uncertain"], "NO_BLIND_REPLAY")
            self.assertEqual(x["stale_fencing_generation"], "DENY_AT_EFFECT_BOUNDARY")
            self.assertTrue(x["required_preconditions"])
        self.assertEqual(set(m["privileged_operations_explicitly_blocked"]),
                         {"ACT-FP-0005", "ACT-FP-0007"})

    def test_open_gates_do_not_claim_qualification(self):
        for lang in ("fr", "en"):
            db = (DOC / lang / "09-database/physical-jobs-model-r3.md").read_text()
            security = (DOC / lang / "14-devops-releases/linux-service-identities-r3.md").read_text()
            execution = (DOC / lang / "08-api-contracts/typed-execution-recovery-r3.md").read_text()
            qa = (DOC / lang / "13-tests-quality/r3-physical-execution-gates.md").read_text()
            self.assertIn("DOC-GAP-004", db)
            self.assertIn("BLOCKED_UNTIL_QUALIFIED", security)
            self.assertIn("BLOCKED_UNTIL_QUALIFIED", execution)
            self.assertIn("Q1–Q170", db + security + execution)
            self.assertIn("DOC-GAP-004/005/006", qa)
            self.assertIn("PLANNED", qa)

if __name__ == "__main__":
    unittest.main()
