"""Static R3 IPC/installer contract checks. Never execute Linux or agent operations."""
import json
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DOC = ROOT / "DOCUMENTATION"
EVIDENCE = DOC / "evidence"
FILES = {
    "08-api-contracts/symfony-go-ipc-r3.md": ("FP-08-R3-IPC", "IPC-FP-", 12),
    "14-devops-releases/installer-lifecycle-r3.md": ("FP-14-R3-INSTALLER", "INST-FP-", 12),
    "13-tests-quality/r3-ipc-installer-gates.md": ("FP-13-R3-IPC-INSTALL-QA", None, 24),
}
FORBIDDEN_FIELDS = {
    "command", "argv", "script_path", "shell", "raw_args", "interpreter", "eval", "qemu_args",
}
EXPECTED_OPS = {f"ACT-FP-{i:04d}" for i in range(1, 8)}
EXPECTED_TESTS = (
    {f"R3-IPC-TEST-{i:03d}" for i in range(1, 13)}
    | {f"R3-INSTALL-TEST-{i:03d}" for i in range(1, 13)}
)

def evidence(name):
    return json.loads((EVIDENCE / name).read_text(encoding="utf-8"))

class R3CandidateContractsTests(unittest.TestCase):
    def test_bilingual_document_ids_and_scope(self):
        for relative, (identity, _, _) in FILES.items():
            for lang in ("fr", "en"):
                with self.subTest(path=relative, lang=lang):
                    value = (DOC / lang / relative).read_text(encoding="utf-8")
                    self.assertRegex(value, rf"id={re.escape(identity)} revision=[1-9]\d* status=specified")
                    if relative.startswith("14-devops-releases/"):
                        self.assertIn("Foundation", value)
                    else:
                        self.assertIn("R1", value)
                    self.assertIn("R2", value)
                    self.assertIn("R3", value)
                    self.assertIn("Q171+", value)
                    self.assertIn("PLANNED" if "tests-quality" in relative else "CANDIDATE", value)

    def test_exact_requirement_ids(self):
        for relative, (_, prefix, total) in FILES.items():
            if prefix is None:
                continue
            expected = {f"{prefix}{i:04d}" for i in range(1, total + 1)}
            for lang in ("fr", "en"):
                raw = (DOC / lang / relative).read_text(encoding="utf-8")
                actual = set(re.findall(rf"\b{re.escape(prefix)}\d{{4}}\b", raw))
                self.assertEqual(actual, expected, f"{lang}/{relative}")

    def test_24_planned_qa_rows_and_parity(self):
        orders = []
        for lang in ("fr", "en"):
            value = (DOC / lang / "13-tests-quality/r3-ipc-installer-gates.md").read_text()
            rows = [line for line in value.splitlines() if line.startswith("| " + chr(96) + "R3-")]
            ids = [re.match(r"^\| \x60(R3-(?:IPC|INSTALL)-TEST-\d{3})\x60", line).group(1) for line in rows]
            self.assertEqual(len(ids), 24)
            self.assertEqual(set(ids), EXPECTED_TESTS)
            self.assertTrue(all(row.rstrip().endswith("| **PLANNED** |") for row in rows))
            self.assertTrue(all(len(row.split("|")) >= 7 for row in rows))
            orders.append(ids)
        self.assertEqual(orders[0], orders[1])

    def test_closed_operation_registry_and_privileged_blocks(self):
        registry = evidence("typed-agent-operations-v1.json")
        self.assertEqual(registry["schema_version"], "candidate-1")
        self.assertEqual(registry["registry_status"], "SPECIFIED_NOT_APPROVED")
        self.assertIs(registry["core_source_imported"], False)
        self.assertIs(registry["privileged_executor_implemented"], False)
        ops = registry["operations"]
        self.assertEqual({x["id"] for x in ops}, EXPECTED_OPS)
        self.assertEqual(len(ops), 7)
        self.assertEqual(len({x["name"] for x in ops}), 7)
        self.assertTrue(FORBIDDEN_FIELDS.issubset(set(registry["forbidden_payload_fields"])))
        for operation in ops:
            with self.subTest(operation=operation["id"]):
                self.assertEqual(operation["version"], "candidate-1")
                self.assertTrue(operation["name"].startswith(("host.", "artifact.", "installer.")))
                self.assertNotIn(operation["name"], registry["prohibited_operation_families"])
                self.assertEqual(operation["transport"], "AUTHENTICATED_PRIVATE_CHANNEL_NOT_SELECTED")
                self.assertEqual(operation["authorization"], "SYMFONY_AND_AGENT_INDEPENDENT_RESOURCE_SCOPE")
                self.assertEqual(operation["audit"], "REQUIRED_REDACTED_CORRELATED")
                self.assertTrue(operation["purpose_fr"] and operation["purpose_en"])
                self.assertEqual(len(operation["tests"]), 2)
                self.assertFalse(set(operation["tests"]) - EXPECTED_TESTS)
                self.assertIn(operation["status"], {"CANDIDATE", "BLOCKED_UNTIL_QUALIFIED"})
                if operation["privilege_class"] == "BOUNDED_PRIVILEGED":
                    self.assertEqual(operation["status"], "BLOCKED_UNTIL_QUALIFIED")
                else:
                    self.assertEqual(operation["status"], "CANDIDATE")
        self.assertEqual(
            {x["id"] for x in ops if x["status"] == "BLOCKED_UNTIL_QUALIFIED"},
            {"ACT-FP-0005", "ACT-FP-0007"},
        )

    def test_request_schema_has_no_arbitrary_command_fields(self):
        registry = evidence("typed-agent-operations-v1.json")
        request = evidence("candidate-ipc-request-v1.schema.json")
        self.assertEqual(request["$schema"], "https://json-schema.org/draft/2020-12/schema")
        self.assertEqual(request["x-contract-status"], "CANDIDATE_NOT_IMPLEMENTED")
        self.assertIs(request["additionalProperties"], False)
        self.assertEqual(
            set(request["properties"]["operation_id"]["enum"]),
            {x["name"] for x in registry["operations"]},
        )
        required = {"contract_version", "request_id", "idempotency_key", "actor_claim",
                    "target", "policy_revision", "expected_revision", "deadline", "parameters"}
        self.assertTrue(required.issubset(set(request["required"])))
        for conditional in request["allOf"]:
            op = conditional["if"]["properties"]["operation_id"]["const"]
            self.assertIn(op, request["properties"]["operation_id"]["enum"])
            params = conditional["then"]["properties"]["parameters"]
            self.assertIs(params["additionalProperties"], False)
            self.assertTrue(set(params["required"]) <= set(params["properties"]))
            self.assertFalse(FORBIDDEN_FIELDS & set(params["properties"]))
        self.assertEqual(len(request["allOf"]), len(registry["operations"]))
        self.assertIs(request["properties"]["actor_claim"]["additionalProperties"], False)

    def test_response_schema_distinguishes_admission_from_job(self):
        response = evidence("candidate-ipc-response-v1.schema.json")
        self.assertEqual(response["x-contract-status"], "CANDIDATE_NOT_IMPLEMENTED")
        self.assertIs(response["additionalProperties"], False)
        self.assertEqual(set(response["properties"]["admission"]["enum"]), {"ACCEPTED", "DENIED", "REJECTED"})
        self.assertIn("COMPENSATION_REQUIRED", response["properties"]["job_state"]["enum"])
        self.assertIn("IDEMPOTENCY_CONFLICT", response["properties"]["error_code"]["enum"])
        self.assertTrue({"job_state", "admission", "error_code"}.issubset(set(response["required"])))
        self.assertTrue(response["allOf"])
        self.assertFalse(FORBIDDEN_FIELDS & set(response["properties"]))

if __name__ == "__main__":
    unittest.main()
