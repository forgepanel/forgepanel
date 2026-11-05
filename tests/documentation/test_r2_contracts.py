"""Check bilingual R2 contracts and planned QA only; not product runtime QA."""
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DOC = ROOT / "DOCUMENTATION"
FILES = {
    "03-core/bootstrap-identity-r2.md": "FP-03-IDENTITY-R2",
    "09-database/setup-transaction-r2.md": "FP-09-TRANSACTION-R2",
    "13-tests-quality/r2-integration-gates.md": "FP-13-R2-GATES",
}

class R2DocumentationTests(unittest.TestCase):
    def read(self, lang, path):
        return (DOC / lang / path).read_text(encoding="utf-8")

    def test_paired_files_and_metadata(self):
        for path, document_id in FILES.items():
            for lang in ("fr", "en"):
                with self.subTest(path=path, lang=lang):
                    value = self.read(lang, path)
                    self.assertIn(f"id={document_id} revision=1 status=specified", value)
                    self.assertIn("R1", value)
                    self.assertIn("PostgreSQL", value)
                    self.assertIn("SPECIFIED" if "tests-quality" not in path else "PLANNED", value)

    def test_requirement_id_coverage(self):
        for path, prefix in (
            ("03-core/bootstrap-identity-r2.md", "R2-ID-"),
            ("09-database/setup-transaction-r2.md", "R2-DB-"),
        ):
            expected = {f"{prefix}{n:03d}" for n in range(1, 13)}
            for lang in ("fr", "en"):
                text = self.read(lang, path)
                found = set(re.findall(rf"\b{re.escape(prefix)}\d{{3}}\b", text))
                self.assertEqual(found, expected, f"{lang} {path}")

    def test_qa_rows_mirrored_and_all_planned(self):
        expected = {f"R2-AUTH-{i:03d}" for i in range(1, 11)}
        expected |= {f"R2-DB-TEST-{i:03d}" for i in range(1, 11)}
        orders = []
        for lang in ("fr", "en"):
            raw = self.read(lang, "13-tests-quality/r2-integration-gates.md")
            rows = [x for x in raw.splitlines() if x.startswith("| " + chr(96) + "R2-")]
            actual = [re.match(r"^\| [^A-Z]*(R2-[A-Z-]+\d{3})", x).group(1) for x in rows]
            self.assertEqual(len(rows), 20)
            self.assertEqual(set(actual), expected)
            self.assertTrue(all(x.strip().endswith("| **PLANNED** |") for x in rows))
            orders.append(actual)
        self.assertEqual(orders[0], orders[1])

    def test_safety_invariants(self):
        for lang in ("fr", "en"):
            identity = self.read(lang, "03-core/bootstrap-identity-r2.md")
            database = self.read(lang, "09-database/setup-transaction-r2.md")
            matrix = self.read(lang, "13-tests-quality/r2-integration-gates.md")
            for marker in ("Argon2id", "TOTP", "R2-ID-006", "R2-ID-012"):
                self.assertIn(marker, identity)
            for marker in ("fp_setup", "fp_admins", "fp_setup_audit", "R2-DB-012"):
                self.assertIn(marker, database)
            for marker in ("SKIP", "PASS", "FAIL", "PLANNED"):
                self.assertIn(marker, matrix)
            self.assertNotIn("IMPLEMENTED — VERIFIED", identity + database + matrix)

if __name__ == "__main__":
    unittest.main()
