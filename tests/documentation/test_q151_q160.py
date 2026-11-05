"""Owner-decision and planned MVP case parity, not runtime qualification."""
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CHOICES = {151: "A", **{n: "C" for n in range(152, 161)}}
CASES = {f"MVP-Q{n}-01" for n in range(151, 161)}


class DecisionMvpParityTests(unittest.TestCase):
    def test_decision_registry(self):
        for lang in ("fr", "en"):
            doc = (ROOT / f"DOCUMENTATION/{lang}/00-project-control/decisions-q151-q160.md").read_text(encoding="utf-8")
            for q, choice in CHOICES.items():
                self.assertRegex(doc, rf"(?m)^\| Q{q} {choice} \|")
            for prior in ("Q1–Q150", "Q132", "Q138", "Q141"):
                self.assertIn(prior, doc)

    def test_mvp_matrix_coverage_and_status(self):
        for lang in ("fr", "en"):
            doc = (ROOT / f"DOCUMENTATION/{lang}/13-tests-quality/mvp-gates-q151-q160.md").read_text(encoding="utf-8")
            self.assertEqual(set(re.findall(r"MVP-Q(?:15[1-9]|160)-01", doc)), CASES)
            self.assertIn("PLANNED", doc)
            self.assertIn("Q132", doc)
            self.assertIn("HTTP-01", doc)


if __name__ == "__main__":
    unittest.main()
