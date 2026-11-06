"""Static R3 job and peer contract checks; no PostgreSQL, socket or Linux execution."""
import json
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DOC = ROOT / "DOCUMENTATION"
EV = DOC / "evidence"
FILES = {
    "09-database/durable-jobs-r3.md": ("FP-09-R3-DURABLE-JOBS", "DB-FP-"),
    "08-api-contracts/local-peer-trust-r3.md": ("FP-08-R3-PEER-TRUST", "PEER-FP-"),
    "13-tests-quality/r3-jobs-peer-gates.md": ("FP-13-R3-JOBS-PEER-QA", None),
}
STATES = {"QUEUED", "RUNNING", "VERIFYING", "SUCCEEDED", "FAILED", "COMPENSATION_REQUIRED", "BLOCKED"}
TERMINAL = {"SUCCEEDED", "FAILED", "COMPENSATION_REQUIRED", "BLOCKED"}
TEST_IDS = {f"R3-JOB-TEST-{n:03d}" for n in range(1, 13)}
TEST_IDS |= {f"R3-PEER-TEST-{n:03d}" for n in range(1, 13)}
FORBIDDEN = {"command", "argv", "shell", "script_path", "qemu_args", "raw_args"}


def load(name):
    return json.loads((EV / name).read_text(encoding="utf-8"))


class R3JobsPeerDocumentationTests(unittest.TestCase):
    def test_document_metadata_and_scope(self):
        for name, (doc_id, _) in FILES.items():
            for lang in ("fr", "en"):
                with self.subTest(name=name, lang=lang):
                    raw = (DOC / lang / name).read_text(encoding="utf-8")
                    revision = 2 if name.startswith("09-database/") else 1
                    self.assertIn(f"id={doc_id} revision={revision} status=specified", raw)
                    self.assertIn("R3", raw)
                    if name.startswith("08-api-contracts/"):
                        self.assertIn("Q1–Q170", raw)
                    else:
                        self.assertIn("Q171+", raw)
                    self.assertIn("PLANNED" if name.startswith("13-") else "CANDIDATE", raw)

    def test_requirement_ids_in_both_languages(self):
        for name, (_, prefix) in FILES.items():
            if prefix is None:
                continue
            expected = {f"{prefix}{n:04d}" for n in range(1, 13)}
            for lang in ("fr", "en"):
                raw = (DOC / lang / name).read_text(encoding="utf-8")
                actual = set(re.findall(rf"\b{re.escape(prefix)}\d{{4}}\b", raw))
                self.assertEqual(actual, expected, f"{lang} {name}")

    def test_24_mirrored_planned_test_rows(self):
        orders = []
        for lang in ("fr", "en"):
            raw = (DOC / lang / "13-tests-quality/r3-jobs-peer-gates.md").read_text()
            rows = [row for row in raw.splitlines() if row.startswith("| " + chr(96) + "R3-")]
            extracted = [re.match(r"^\| .(R3-(?:JOB|PEER)-TEST-\d{3}).", row).group(1) for row in rows]
            self.assertEqual(len(rows), 24)
            self.assertEqual(set(extracted), TEST_IDS)
            self.assertTrue(all(row.endswith("| **PLANNED** |") for row in rows))
            orders.append(extracted)
        self.assertEqual(orders[0], orders[1])

    def test_job_record_is_strict_and_no_execution_permission(self):
        schema = load("candidate-job-record-v1.schema.json")
        self.assertEqual(schema["$schema"], "https://json-schema.org/draft/2020-12/schema")
        self.assertEqual(schema["x-contract-status"], "CANDIDATE_NOT_IMPLEMENTED")
        self.assertIs(schema["additionalProperties"], False)
        self.assertEqual(set(schema["required"]), set(schema["properties"]))
        self.assertEqual(set(schema["properties"]["state"]["enum"]), STATES)
        self.assertEqual(schema["properties"]["admission"]["const"], "ACCEPTED")
        self.assertIs(schema["properties"]["admitted_after_commit"]["const"], True)
        conditions = {
            part["if"]["properties"]["state"]["const"]: part["then"]["properties"]
            for part in schema["allOf"] if "state" in part["if"].get("properties", {})
        }
        self.assertEqual(conditions["QUEUED"]["lease"]["type"], "null")
        self.assertEqual(conditions["RUNNING"]["lease"]["type"], "object")
        self.assertEqual(conditions["QUEUED"]["observed_effect_status"]["const"], "UNVERIFIED")
        ops = load("typed-agent-operations-v1.json")["operations"]
        self.assertEqual(set(schema["properties"]["operation_id"]["enum"]), {o["name"] for o in ops})
        self.assertFalse(FORBIDDEN & set(schema["properties"]))
        self.assertTrue(any(
            part.get("if", {}).get("properties", {}).get("state", {}).get("const") == "SUCCEEDED"
            and part.get("then", {}).get("properties", {}).get("observed_effect_status", {}).get("const") == "VERIFIED"
            for part in schema["allOf"]
        ))

    def test_transitions_require_fencing_and_observed_success(self):
        data = load("candidate-job-transitions-v1.json")
        self.assertEqual(data["status"], "SPECIFIED_NOT_IMPLEMENTED")
        self.assertEqual(set(data["states"]), STATES)
        checks = data["requirements"]
        self.assertTrue(checks["durable_commit_before_ack"])
        self.assertFalse(checks["exactly_once_linux_side_effect_claimed"])
        self.assertFalse(checks["lease_expiry_authorizes_reexecution"])
        self.assertFalse(checks["old_fencing_generation_is_valid"])
        self.assertFalse(checks["blind_replay_after_uncertain_effect"])
        self.assertTrue(checks["success_requires_observed_effect"])
        self.assertEqual(checks["same_idempotency_key_different_digest"], "IDEMPOTENCY_CONFLICT")
        actual = {(x["from"], x["to"]) for x in data["transitions"]}
        self.assertEqual(len(actual), len(data["transitions"]))
        self.assertTrue(all(x["from"] in STATES and x["to"] in STATES and x["guard"]
                            and x["from"] not in TERMINAL for x in data["transitions"]))
        self.assertIn(("VERIFYING", "SUCCEEDED"), actual)
        self.assertNotIn(("RUNNING", "SUCCEEDED"), actual)
        self.assertTrue({"lease_duration", "timeouts", "retries", "retention", "table_names"}
                        .issubset(set(data["unratified_settings"])))

    def test_peer_binding_never_grants_privilege(self):
        schema = load("candidate-peer-binding-v1.schema.json")
        self.assertEqual(schema["x-contract-status"], "CANDIDATE_NOT_IMPLEMENTED")
        self.assertIs(schema["additionalProperties"], False)
        self.assertEqual(set(schema["required"]), set(schema["properties"]))
        self.assertEqual(schema["properties"]["record_origin"]["const"],
                         "SERVER_SIDE_KERNEL_OBSERVATION_ONLY")
        self.assertEqual(schema["properties"]["transport_kind"]["const"],
                         "FILESYSTEM_UNIX_SOCKET_CANDIDATE")
        for key in ("privileged_action_authorized", "privileged_executor_implemented",
                    "hub_can_authorize_core_linux"):
            self.assertIs(schema["properties"][key]["const"], False)
        self.assertFalse(FORBIDDEN & set(schema["properties"]))

    def test_current_product_authority_unchanged(self):
        for lang in ("fr", "en"):
            db = (DOC / lang / "09-database/durable-jobs-r3.md").read_text(encoding="utf-8")
            peer = (DOC / lang / "08-api-contracts/local-peer-trust-r3.md").read_text(encoding="utf-8")
            tests = (DOC / lang / "13-tests-quality/r3-jobs-peer-gates.md").read_text(encoding="utf-8")
            for mark in ("DOC-GAP-004", "DOC-GAP-006", "Q1–Q170", "Q171+"):
                self.assertIn(mark, db)
            self.assertIn("DOC-GAP-006", peer)
            self.assertIn("BLOCKED_UNTIL_QUALIFIED", peer)
            self.assertIn("Q1–Q170", peer)
            self.assertIn("PLANNED", tests)


if __name__ == "__main__":
    unittest.main()
