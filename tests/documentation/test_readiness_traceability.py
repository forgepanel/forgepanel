"""Documentation readiness/traceability consistency only — not product QA."""
from __future__ import annotations
import json
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "DOCUMENTATION/evidence/documentation-readiness-v1.json"
EXPECTED_IDS = {f"DOC-GAP-{i:03d}" for i in range(1, 23)}
EXPECTED_TRACE = {f"FP-TRACE-{i:03d}" for i in range(1, 23)}

def get_data():
    return json.loads(DATA.read_text(encoding="utf-8"))

class ReadinessTests(unittest.TestCase):
    def test_version_ids_and_states(self):
        data = get_data()
        self.assertEqual(data["schema_version"], "1")
        self.assertEqual(len(data["gaps"]), 22)
        self.assertEqual({x["id"] for x in data["gaps"]}, EXPECTED_IDS)
        self.assertEqual(len({x["id"] for x in data["gaps"]}), len(data["gaps"]))
        self.assertEqual(data["core_develop_snapshot"], "a6a924370ef2c4b922b38d148594ed50d08f3b6e")
        self.assertEqual(data["hub_develop_snapshot"], "243d1ebb99649372ccc931deb603d172b2e17e18")
        self.assertIn("Q171+ unanswered", data["decision_scope"])
        self.assertEqual({x["state"] for x in data["gaps"]}, {"BLOCKED", "OPEN"})
        self.assertEqual([x["id"] for x in data["gaps"] if x["state"] == "BLOCKED"], ["DOC-GAP-001"])
        for gap in data["gaps"]:
            self.assertIn(gap["phase"], ("R1","R2","R3","R4","R5","R6","PRE-PUBLIC","DESIGN","POST-MVP","RELEASE","GUIDES"))
            self.assertIn(gap["priority"], ("P0", "P1"))
            self.assertRegex(gap["issue"], r"^https://github\.com/yyogas/forgepanel(?:-hub)?/issues/\d+$")
            self.assertTrue(gap["owner"].strip())
            self.assertTrue(gap["missing_en"].strip() and gap["missing_fr"].strip())
            self.assertTrue(gap["closure_en"].strip() and gap["closure_fr"].strip())
            self.assertTrue(all(re.fullmatch(r"Q\d{1,3}", q) for q in gap["decisions"]))
            self.assertFalse(set(gap["dependencies"]) - EXPECTED_IDS)

    def test_dependency_graph_is_acyclic(self):
        graph = {x["id"]: x["dependencies"] for x in get_data()["gaps"]}
        visiting, done = set(), set()

        def visit(node):
            if node in visiting:
                self.fail(f"Dependency cycle involving {node}")
            if node in done:
                return
            visiting.add(node)
            for dep in graph[node]:
                visit(dep)
            visiting.remove(node)
            done.add(node)
        for key in graph:
            visit(key)

    def test_mirrored_document_ids_and_trace_rows(self):
        for kind, token, expected, marker in (
            ("documentation-readiness.md", "DOC-GAP-", EXPECTED_IDS, "FP-00-DOC-READINESS"),
            ("requirements-traceability.md", "FP-TRACE-", EXPECTED_TRACE, "FP-00-TRACEABILITY"),
        ):
            languages = {}
            for lang in ("fr", "en"):
                path = ROOT / "DOCUMENTATION" / lang / "00-project-control" / kind
                raw = path.read_text(encoding="utf-8")
                self.assertRegex(raw, rf"id={re.escape(marker)} revision=[1-9]\\d* status=documented")
                lines = [line for line in raw.splitlines() if line.startswith("| " + token)]
                actual = [line.split("|")[1].strip() for line in lines]
                self.assertEqual(len(actual), len(expected), f"{path} invalid row count")
                self.assertEqual(set(actual), expected, f"{path} missing IDs")
                self.assertIn("Q171+", raw)
                languages[lang] = actual
            self.assertEqual(languages["fr"], languages["en"])

    def test_current_status_reconciles_merged_tools_without_product_claim(self):
        for lang in ("fr", "en"):
            text = (ROOT / "DOCUMENTATION" / lang / "00-project-control/status.md").read_text()
            for number in ("#37", "#38", "#39", "#40", "#41", "#43", "#42", "#2"):
                self.assertIn(number, text)
            self.assertIn("a6a924370ef2c4b922b38d148594ed50d08f3b6e", text)
            self.assertIn("42120185132", text)
            self.assertIn("NOT_EXECUTED", text)
            self.assertIn("documentation-readiness.md", text)
            self.assertIn("requirements-traceability.md", text)
            self.assertNotIn("IMPLEMENTATION CANDIDATE", text)

    def test_r3_candidate_links_do_not_close_open_gaps(self):
        for lang in ("fr", "en"):
            matrix = (ROOT / "DOCUMENTATION" / lang / "00-project-control/requirements-traceability.md").read_text()
            registry = (ROOT / "DOCUMENTATION" / lang / "00-project-control/documentation-readiness.md").read_text()
            for link in ("../14-devops-releases/installer-lifecycle-r3.md",
                         "../08-api-contracts/symfony-go-ipc-r3.md",
                         "../13-tests-quality/r3-ipc-installer-gates.md"):
                self.assertIn(link, matrix)
            for gap_id in ("DOC-GAP-005", "DOC-GAP-006"):
                self.assertIn(gap_id, registry)
            self.assertIn("OPEN", registry)

    def test_evidence_and_authority_boundaries(self):
        for lang in ("fr", "en"):
            text = (ROOT / "DOCUMENTATION" / lang / "00-project-control/requirements-traceability.md").read_text()
            for term in ("Q132", "Q161", "Q162", "R1", "R2", "R3", "R4", "R5", "R6", "NOT_EXECUTED"):
                self.assertIn(term, text)
            self.assertIn("42120185132", text)
            self.assertIn("42066987234", text)
            gap = (ROOT / "DOCUMENTATION" / lang / "00-project-control/documentation-readiness.md").read_text()
            self.assertIn("R1", gap)
            self.assertIn("Q171+", gap)

if __name__ == "__main__":
    unittest.main()
