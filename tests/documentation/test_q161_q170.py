"""Q161-Q170 documentation invariant tests, not product verification."""
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
OPTIONS = {161: "C", 162: "B", 163: "C", 164: "B", 165: "C", 166: "C", 167: "C", 168: "C", 169: "C", 170: "B"}

class DocumentationGateTests(unittest.TestCase):
    def test_options_and_preserved_decisions(self):
        for lang in ("fr", "en"):
            doc = (ROOT / f"DOCUMENTATION/{lang}/00-project-control/decisions-q161-q170.md").read_text()
            actual = {int(q): o for q,o in re.findall(r"^\| Q(16[1-9]|170) \| ([BC]) \|",doc,re.M)}
            self.assertEqual(actual, OPTIONS)
            for key in ("Q1–Q160","Q132","Q153","Q156","Q159","Q160","SPECIFIED"):
                self.assertIn(key,doc)
            reg = (ROOT / f"DOCUMENTATION/{lang}/00-project-control/decisions.md").read_text()
            self.assertTrue({f"ADR-{n}" for n in range(130,140)}.issubset(set(re.findall(r"ADR-\d{3}",reg))))

    def test_matrix_has_every_case_and_planned_status(self):
        expected={f"MVP-Q{q}-01" for q in OPTIONS}
        for lang in ("fr", "en"):
            doc=(ROOT / f"DOCUMENTATION/{lang}/13-tests-quality/mvp-gates-q161-q170.md").read_text()
            self.assertEqual(set(re.findall(r"MVP-Q(?:16[1-9]|170)-01",doc)),expected)
            self.assertIn("PLANNED",doc)
            self.assertIn("HTTP-01",doc)

if __name__ == "__main__":
    unittest.main()
