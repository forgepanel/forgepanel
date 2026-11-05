"""Check owner choices and planned MVP matrix; does not prove runtime behavior."""
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CHOICES = {"151": "A", **{str(n): "C" for n in range(152, 161)}}
IDS = {f"MVP-Q{n}-01" for n in range(151, 161)}

class Q151ToQ160DocumentationTests(unittest.TestCase):
    def test_decisions_in_both_languages(self):
        for lang in ("fr", "en"):
            s = (ROOT / f"DOCUMENTATION/{lang}/00-project-control/decisions-q151-q160.md").read_text()
            self.assertEqual(dict(re.findall(r"^\\| Q(15[1-9]|160) \\| ([AC]) \\|", s, re.M)), CHOICES)
            self.assertIn("Q1–Q150", s)
            self.assertIn("Q132", s)

    def test_planned_mvp_matrix_in_both_languages(self):
        for lang in ("fr", "en"):
            s = (ROOT / f"DOCUMENTATION/{lang}/13-tests-quality/mvp-gates-q151-q160.md").read_text()
            self.assertEqual(set(re.findall(r"MVP-Q(?:15[1-9]|160)-01", s)), IDS)
            self.assertIn("PLANNED", s)

if __name__ == "__main__":
    unittest.main()
