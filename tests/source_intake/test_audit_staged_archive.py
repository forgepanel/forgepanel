"""Read-only staged-file integrity tests using synthetic archives only."""
import hashlib
import importlib.util
import json
import os
import stat
import sys
import tempfile
import unittest
import zipfile
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))
spec = importlib.util.spec_from_file_location("audit_staged_archive", ROOT / "scripts/audit_staged_archive.py")
auditor = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = auditor
spec.loader.exec_module(auditor)
from stage_source_archive import RECEIPT, stage


class QuarantineAuditTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.private = self.root / "private"
        self.private.mkdir(mode=0o700)
        self.archive = self.root / "fixture.zip"
        self.evidence = self.root / "evidence.json"
        self.destination = self.private / "quarantine"
        self.make_zip({"src/main.go": b"package main\n", "README.md": b"hello\n"})
        self.stage_fixture()

    def make_zip(self, members):
        with zipfile.ZipFile(self.archive, "w", compression=zipfile.ZIP_DEFLATED) as zipped:
            for name, contents in members.items():
                zipped.writestr(name, contents)
        digest = hashlib.sha256(self.archive.read_bytes()).hexdigest()
        self.evidence.write_text(json.dumps({"inputs": [
            {"id": "SRC-03", "sha256": digest, "file_count": len(members)}
        ]}))
        return digest

    def stage_fixture(self):
        with patch.object(os, "geteuid", return_value=self.private.stat().st_uid):
            report = stage(self.archive, self.destination, self.evidence, commit=True)
        self.assertEqual(report["status"], "STAGED_FOR_MANUAL_REVIEW", report)

    def audit(self):
        return auditor.verify(self.archive, self.destination, self.evidence)

    def assert_block(self, expected):
        result = self.audit()
        self.assertEqual(result["status"], "BLOCKED", result)
        self.assertTrue(any(expected in x for x in result["blockers"]), result)

    def test_valid_source_is_consistent_but_not_approved(self):
        result = self.audit()
        self.assertEqual(result["status"], "CONSISTENT_FOR_MANUAL_REVIEW", result)
        self.assertEqual(result["files_verified"], 2)
        self.assertFalse(result["import_approved"])
        self.assertFalse(result["imported_into_core"])
        self.assertFalse(result["executed"])

    def test_modified_staged_file_detected(self):
        (self.destination / "README.md").write_text("world\n")
        self.assert_block("staged_file_digest_mismatch")

    def test_modified_staged_file_size_detected(self):
        (self.destination / "README.md").write_text("altered-longer\n")
        self.assert_block("staged_file_size_mismatch")

    def test_missing_staged_file_detected(self):
        (self.destination / "README.md").unlink()
        self.assert_block("staged_inventory_incomplete")

    def test_unexpected_staged_file_detected(self):
        (self.destination / "secret.txt").write_text("hidden")
        self.assert_block("unexpected_staged_file")

    def test_unexpected_staged_directory_detected(self):
        (self.destination / "another").mkdir()
        self.assert_block("unexpected_staged_directory")

    def test_staged_symlink_refused(self):
        (self.destination / "src" / "main.go").unlink()
        (self.destination / "src" / "main.go").symlink_to(self.destination / "README.md")
        self.assert_block("staged_special_file_or_symlink")

    def test_staged_symlink_directory_refused(self):
        (self.destination / "src" / "main.go").unlink()
        (self.destination / "src").rmdir()
        (self.destination / "src").symlink_to(self.private, target_is_directory=True)
        self.assert_block("staged_special_file_or_symlink")

    def test_staged_hardlink_detected(self):
        (self.destination / "src" / "main.go").unlink()
        os.link(self.destination / "README.md", self.destination / "src" / "main.go")
        self.assert_block("staged_hardlink_detected")

    def test_executable_mode_detected(self):
        (self.destination / "README.md").chmod(0o700)
        self.assert_block("staged_file_has_executable_or_shared_mode")

    def test_world_or_group_access_to_root_is_rejected(self):
        self.destination.chmod(0o750)
        self.assert_block("staged_directory_not_private_or_owned")

    def test_group_access_to_nested_directory_is_rejected(self):
        (self.destination / "src").chmod(0o750)
        self.assert_block("staged_directory_shared_mode")

    def test_receipt_tampering_detected(self):
        receipt = self.destination / RECEIPT
        data = json.loads(receipt.read_text())
        data["files"][0]["sha256"] = "a" * 64
        receipt.write_text(json.dumps(data))
        self.assert_block("receipt_differs_from_verified_zip")

    def test_receipt_symlink_detected(self):
        (self.destination / RECEIPT).unlink()
        (self.destination / RECEIPT).symlink_to(self.evidence)
        self.assert_block("missing_or_unsafe_receipt")

    def test_missing_receipt_detected(self):
        (self.destination / RECEIPT).unlink()
        self.assert_block("missing_or_unsafe_receipt")

    def test_modified_original_zip_detected(self):
        self.archive.write_bytes(b"not the original ZIP")
        self.assert_block("archive_sha256_mismatch")

    def test_missing_source_zip_detected(self):
        self.archive.unlink()
        self.assert_block("archive_unavailable")

    def test_noncanonical_directory_is_rejected(self):
        alias = self.private / "alias"
        alias.symlink_to(self.destination, target_is_directory=True)
        result = auditor.verify(self.archive, alias, self.evidence)
        self.assertEqual(result["status"], "BLOCKED")

    def test_quarantine_under_repository_is_rejected(self):
        result = auditor.verify(self.archive, ROOT, self.evidence)
        self.assertEqual(result["status"], "BLOCKED")
        self.assertIn("staged_directory_inside_repository_forbidden", result["blockers"])

    def test_receipt_marked_import_approved_is_rejected(self):
        receipt = self.destination / RECEIPT
        data = json.loads(receipt.read_text())
        data["import_approved"] = True
        receipt.write_text(json.dumps(data))
        self.assert_block("receipt_provenance_or_state_mismatch")

    def test_receipt_mode_shared_is_rejected(self):
        (self.destination / RECEIPT).chmod(0o644)
        self.assert_block("receipt_not_private_regular_file")

    def test_staged_special_fifo_is_rejected(self):
        os.mkfifo(self.destination / "fifo")
        self.assert_block("staged_special_file_or_symlink")


if __name__ == "__main__":
    unittest.main()
