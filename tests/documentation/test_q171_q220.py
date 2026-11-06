"""Q171-Q220 owner-approved product decisions: STATIC registry and FR/EN parity only."""
from __future__ import annotations

import json
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SOURCE = ROOT / "evidence/decisions-q171-q220-v1.json"
CASES = ROOT / "evidence/acceptance-q171-q220-v1.json"
EXPECTED = {i: ("C" if i in (174, 194, 200) else "D") for i in range(171, 221)}


class ApprovedQ171ToQ220Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.registry = json.loads(SOURCE.read_text(encoding="utf-8"))
        cls.acceptance = json.loads(CASES.read_text(encoding="utf-8"))

    def test_all_50_choices_explicitly_approved(self):
        d = self.registry
        self.assertEqual(d["register_status"], "OWNER_APPROVED_PRODUCT_DIRECTIONS")
        self.assertEqual(d["owner_confirmed_date"], "2026-11-06")
        self.assertEqual(d["prior_decisions_retained"], "Q1-Q170")
        self.assertIs(d["supersedes_earlier_decisions"], False)
        self.assertEqual(d["approval_scope"], "PRODUCT_DIRECTION_ONLY")
        self.assertEqual(d["implementation_status"], "NOT_APPROVED_BY_THIS_DECISION")
        self.assertEqual(d["runtime_qa_status"], "NOT_EXECUTED_BY_THIS_DECISION")
        actual = {int(q["id"][1:]): q["choice"] for q in d["questions"]}
        self.assertEqual(actual, EXPECTED)
        self.assertEqual(len(d["questions"]), len(actual))
        self.assertTrue(all(q["status"] == "OWNER_APPROVED" for q in d["questions"]))
        self.assertTrue(all(q["scope"] in ("CORE", "CORE_HUB") for q in d["questions"]))

    def test_bilingual_register_has_exact_matching_choices(self):
        for lang in ("en", "fr"):
            text = (ROOT / "DOCUMENTATION" / lang / "00-project-control/decisions-q171-q220.md").read_text()
            self.assertTrue(text.startswith("<!-- forgepanel-doc id=FP-00-Q171-220 revision=1 status=specified -->"))
            rows = re.findall(r"^\| Q(\d{3}) \| \*\*([CD])\*\* \|", text, re.M)
            self.assertEqual(len(rows), 50)
            self.assertEqual({int(n): opt for n, opt in rows}, EXPECTED)
            for name in ("Q1–Q170", "Q174", "Q194", "Q200", "Q171–Q220", "SPECIFIED"):
                self.assertIn(name, text)
            self.assertIn("reconciliation-q171-q220.md", text)

    def test_50_acceptance_cases_are_planned_not_executed(self):
        a = self.acceptance
        self.assertEqual(a["status"], "PLANNED_NOT_EXECUTED")
        self.assertEqual(len(a["cases"]), 50)
        cases = {int(c["decision_id"][1:]): c for c in a["cases"]}
        self.assertEqual(set(cases), set(EXPECTED))
        for number, record in cases.items():
            self.assertEqual(record["id"], f"ACCEPT-Q{number}-01")
            self.assertEqual(record["choice"], EXPECTED[number])
            self.assertEqual(record["status"], "PLANNED")
            self.assertEqual(record["result"], "NOT_EXECUTED")
            self.assertTrue(record["scenario_fr"] and record["scenario_en"])

    def test_bilingual_acceptance_matrix_parity(self):
        case_ids = {f"ACCEPT-Q{n}-01" for n in EXPECTED}
        for lang in ("en", "fr"):
            text = (ROOT / "DOCUMENTATION" / lang / "13-tests-quality/mvp-gates-q171-q220.md").read_text()
            self.assertTrue(text.startswith("<!-- forgepanel-doc id=FP-13-Q171-220 revision=1 status=specified -->"))
            rows = re.findall(r"^\| (ACCEPT-Q\d{3}-01) \| ([CD]) \|", text, re.M)
            self.assertEqual(len(rows), 50)
            self.assertEqual({n for n, _ in rows}, case_ids)
            for test_id, choice in rows:
                self.assertEqual(choice, EXPECTED[int(test_id.split("-")[1][1:])])
            self.assertIn("PLANNED", text)

    def test_reconciliation_records_critical_nonadoptions(self):
        for lang in ("en", "fr"):
            text = (ROOT / "DOCUMENTATION" / lang / "00-project-control/reconciliation-q171-q220.md").read_text()
            for marker in ("Q174", "Q194", "Q200", "Q175", "Q168", "Q220", "Q221", "Q1–Q170"):
                if marker == "Q221":
                    continue  # New questions are not assumed to have a final catalog.
                self.assertIn(marker, text)
            self.assertIn("R1", text)
            self.assertIn("R4", text)
            self.assertIn("Hub", text)

    def test_q171_plus_legacy_open_assertion_not_in_active_app_center_docs(self):
        for lang in ("en", "fr"):
            for path in ("06-apps-recipes/app-center-engines.md", "08-api-contracts/app-center-recipe-contracts.md"):
                content = (ROOT / "DOCUMENTATION" / lang / path).read_text()
                self.assertNotIn("Q171+ remain open", content)
                self.assertNotIn("Q171+ restent ouverts", content)
                self.assertNotIn("Q171+ remain unanswered", content)
                self.assertNotIn("Q171+ restent sans réponse", content)
                self.assertIn("decisions-q171-q220.md", content)

    def test_technical_values_are_not_invented_as_approved(self):
        self.assertGreaterEqual(len(self.registry["still_open"]), 5)
        for choice in self.registry["questions"]:
            self.assertNotIn("IMPLEMENTED", choice["status"])
            self.assertNotIn("VERIFIED", choice["status"])


if __name__ == "__main__":
    unittest.main()
