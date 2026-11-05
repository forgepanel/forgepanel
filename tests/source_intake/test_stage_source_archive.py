"""Synthetic ZIP staging tests; no production sources or privileged execution."""
import hashlib
import importlib.util
import json
import os
import sys
import tempfile
import unittest
import zipfile
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))
spec = importlib.util.spec_from_file_location("stage_source_archive", ROOT / "scripts/stage_source_archive.py")
module = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = module
spec.loader.exec_module(module)


class StageArchiveTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.private = self.root / "private"
        self.private.mkdir(mode=0o700)
        self.archive = self.root / "synthetic.zip"
        self.destination = self.private / "quarantine"
        self.evidence = self.root / "evidence.json"
        self.make_zip({"src/main.go": b"package main\n", "README.md": b"example\n"})

    def make_zip(self, members):
        with zipfile.ZipFile(self.archive, "w", compression=zipfile.ZIP_DEFLATED) as zf:
            for name, payload in members.items():
                zf.writestr(name, payload)
        digest = hashlib.sha256(self.archive.read_bytes()).hexdigest()
        self.evidence.write_text(json.dumps({"inputs": [
            {"id": "SRC-03", "sha256": digest, "file_count": len(members)}
        ]}))

    def call(self, commit=False):
        return module.stage(self.archive, self.destination, self.evidence, commit=commit)

    def stage_nonroot(self):
        with patch.object(os, "geteuid", return_value=os.stat(self.private).st_uid):
            return self.call(commit=True)

    def test_read_only_by_default(self):
        report = self.call()
        self.assertEqual(report["status"], "VERIFIED_FOR_REVIEW")
        self.assertFalse(self.destination.exists())

    def test_private_quarantine_and_receipt(self):
        report = self.stage_nonroot()
        self.assertEqual(report["status"], "STAGED_FOR_MANUAL_REVIEW")
        self.assertFalse(report["imported_into_core"])
        self.assertEqual((self.destination / "src/main.go").read_bytes(), b"package main\n")
        manifest = json.loads((self.destination / module.RECEIPT).read_text())
        self.assertFalse(manifest["import_approved"])
        self.assertEqual(len(manifest["files"]), 2)
        self.assertEqual((self.destination / "src/main.go").stat().st_mode & 0o111, 0)

    def test_root_execution_denied(self):
        with patch.object(os, "geteuid", return_value=0):
            self.assertIn("root_execution_forbidden", self.call(commit=True)["blockers"])
        self.assertFalse(self.destination.exists())

    def test_existing_directory_not_overwritten(self):
        self.destination.mkdir()
        (self.destination / "keep.txt").write_text("preserve")
        result = self.stage_nonroot()
        self.assertIn("destination_already_exists", result["blockers"])
        self.assertEqual((self.destination / "keep.txt").read_text(), "preserve")

    def test_staging_inside_repo_is_refused(self):
        path = ROOT / "never-create-quarantine"
        with patch.object(os, "geteuid", return_value=os.stat(ROOT).st_uid):
            outcome = module.stage(self.archive, path, self.evidence, commit=True)
        self.assertIn("staging_inside_source_repo_forbidden", outcome["blockers"])
        self.assertFalse(path.exists())

    def test_cli_rejects_custom_evidence_for_staging(self):
        import io
        from contextlib import redirect_stdout
        buf = io.StringIO()
        with redirect_stdout(buf):
            code = module.main(["--archive", str(self.archive), "--destination", str(self.destination),
                                "--evidence", str(self.evidence), "--stage"])
        self.assertEqual(code, 2)
        self.assertIn("custom_evidence_staging_forbidden", buf.getvalue())
        self.assertFalse(self.destination.exists())

    def test_wrong_checksum_cannot_stage(self):
        self.archive.write_bytes(b"tampered")
        result = self.stage_nonroot()
        self.assertIn("archive_sha256_mismatch", result["blockers"])
        self.assertFalse(self.destination.exists())

    def test_writable_parent_rejected(self):
        self.private.chmod(0o770)
        result = self.stage_nonroot()
        self.assertIn("parent_must_be_private_and_owned", result["blockers"])

    def test_reserved_receipt_path_rejected(self):
        self.make_zip({module.RECEIPT: b"fake"})
        result = self.stage_nonroot()
        self.assertIn("reserved_receipt_path", result["blockers"])
        self.assertFalse(self.destination.exists())

    def test_zip_slip_rejected_before_write(self):
        self.make_zip({"../escape.txt": b"unsafe"})
        result = self.stage_nonroot()
        self.assertEqual(result["status"], "BLOCKED")
        self.assertFalse(self.destination.exists())

    def test_changed_entry_is_detected_and_cleaned(self):
        original = module.scan_archive

        def swapped(*args, **kwargs):
            report = original(*args, **kwargs)
            self.make_zip({"src/main.go": b"altered", "README.md": b"example\n"})
            return report

        with patch.object(module, "scan_archive", side_effect=swapped):
            result = self.stage_nonroot()
        self.assertIn("member_content_changed", result["blockers"])
        self.assertFalse(self.destination.exists())



    def test_relative_destination_rejected(self):
        self.destination = Path("relative-quarantine")
        result = self.stage_nonroot()
        self.assertIn("destination_must_be_absolute", result["blockers"])

    def test_source_id_other_than_canonical_is_blocked_for_cli_stage(self):
        import io
        from contextlib import redirect_stdout
        buf = io.StringIO()
        with redirect_stdout(buf):
            code = module.main(["--archive", str(self.archive),
                                "--destination", str(self.destination),
                                "--source-id", "SRC-04", "--stage"])
        self.assertEqual(code, 2)
        self.assertIn("noncanonical_source_id_for_staging", buf.getvalue())
        self.assertFalse(self.destination.exists())

    def test_replaced_quarantine_is_not_deleted_during_cleanup(self):
        def swap_then_fail(*args, **kwargs):
            self.destination.rename(self.private / "original-moved")
            self.destination.mkdir(mode=0o700)
            (self.destination / "keep.txt").write_text("do not delete")
            raise module.StageError("injected_staging_failure")

        with patch.object(module, "_copy_entry", side_effect=swap_then_fail):
            result = self.stage_nonroot()
        self.assertEqual(result["status"], "BLOCKED")
        self.assertIn("cleanup_skipped_due_to_identity_change", result["blockers"])
        self.assertEqual((self.destination / "keep.txt").read_text(), "do not delete")
        self.assertTrue((self.private / "original-moved").exists())

    def test_quarantine_replaced_before_success_is_blocked(self):
        real_sha256 = module.sha256_file

        def swap_at_final_hash(path):
            original = real_sha256(path)
            self.destination.rename(self.private / "original-moved")
            self.destination.mkdir(mode=0o700)
            (self.destination / "keep.txt").write_text("do not delete")
            return original

        with patch.object(module, "sha256_file", side_effect=swap_at_final_hash):
            result = self.stage_nonroot()
        self.assertEqual(result["status"], "BLOCKED")
        self.assertIn("quarantine_identity_changed", result["blockers"])
        self.assertEqual((self.destination / "keep.txt").read_text(), "do not delete")

    def test_shared_intermediate_directory_is_denied(self):
        original_mkdir = module.os.mkdir

        def create_shared(name, mode=0o777, *args, **kwargs):
            if name == "src":
                return original_mkdir(name, 0o755, *args, **kwargs)
            return original_mkdir(name, mode, *args, **kwargs)

        with patch.object(module.os, "mkdir", side_effect=create_shared):
            result = self.stage_nonroot()
        self.assertEqual(result["status"], "BLOCKED")
        self.assertIn("staging_subdirectory_not_private_or_owned", result["blockers"])
        self.assertFalse(self.destination.exists())



if __name__ == "__main__":
    unittest.main()
