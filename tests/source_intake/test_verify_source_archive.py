"""Synthetic archive-only unit checks; never execute source archive entries."""
import importlib.util
import io
import json
import stat
import tempfile
import unittest
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
spec = importlib.util.spec_from_file_location("verify_source_archive", ROOT / "scripts" / "verify_source_archive.py")
scanner = importlib.util.module_from_spec(spec)
import sys
sys.modules[spec.name] = scanner
spec.loader.exec_module(scanner)


class ArchiveIntakeTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.archive = Path(self.tmp.name) / "input.zip"

    def make_zip(self, entries, compression=zipfile.ZIP_DEFLATED):
        with zipfile.ZipFile(self.archive, "w", compression=compression) as zf:
            for name, data in entries:
                if isinstance(name, zipfile.ZipInfo):
                    zf.writestr(name, data)
                else:
                    zf.writestr(name, data)
        return scanner.sha256_file(self.archive)

    def scan(self, entries, *, limit=None, expected_count=None):
        sha = self.make_zip(entries)
        return scanner.scan_archive(self.archive, sha, len(entries) if expected_count is None else expected_count, limits=limit or scanner.Limits())

    def test_safe_archive_manifest_and_no_extraction(self):
        r = self.scan([("cmd/forgepanel/main.go", b"package main"), ("README.md", b"documentation")])
        self.assertFalse(r.blockers)
        self.assertEqual(r.file_count, 2)
        self.assertEqual([x["path"] for x in r.entries], ["cmd/forgepanel/main.go", "README.md"])
        self.assertFalse((Path(self.tmp.name) / "cmd").exists())
        self.assertEqual(r.as_dict()["state"], "PASS")
        self.assertFalse(r.as_dict()["runtime_certified"])

    def test_checksum_mismatch_blocks_before_parsing(self):
        self.make_zip([("safe.txt", b"hello")])
        r = scanner.scan_archive(self.archive, "0" * 64, 1)
        self.assertEqual(r.blockers, ["archive_sha256_mismatch"])
        self.assertFalse(r.entries)

    def test_missing_archive_blocks(self):
        r = scanner.scan_archive(self.archive, "a" * 64, 1)
        self.assertEqual(r.blockers, ["archive_unavailable"])

    def test_path_traversal_rejected(self):
        r = self.scan([("../escape.txt", b"x")])
        self.assertTrue(any("unsafe_path_component" in b for b in r.blockers))

    def test_absolute_and_windows_paths_rejected(self):
        for name in ("/etc/passwd", "C:/windows/file", r"dir\evil.txt"):
            with self.subTest(name=name):
                r = self.scan([(name, b"x")])
                self.assertTrue(any("absolute_or_non_posix_path" in b for b in r.blockers))

    def test_casefold_collision(self):
        r = self.scan([("Code/Hello.go", b"x"), ("code/hello.go", b"y")])
        self.assertTrue(any("duplicate_or_casefold_collision" in b for b in r.blockers))

    def test_file_as_parent_directory(self):
        r = self.scan([("docs", b"x"), ("docs/index.md", b"y")])
        self.assertTrue(any("file_directory_collision" in b for b in r.blockers))

    def test_symlink_detected(self):
        info = zipfile.ZipInfo("unsafe-link")
        info.create_system = 3
        info.external_attr = (stat.S_IFLNK | 0o777) << 16
        r = self.scan([(info, b"/etc/shadow")])
        self.assertTrue(any("special_file_or_symlink" in b for b in r.blockers))

    def test_compression_bomb_limit(self):
        r = self.scan([("zeros.bin", b"0" * (64 * 1024))], limit=scanner.Limits(compression_ratio=5))
        self.assertTrue(any("compression_ratio_limit_exceeded" in b for b in r.blockers))

    def test_entry_size_limit(self):
        r = self.scan([("large.bin", b"x" * 800)], limit=scanner.Limits(member_bytes=100))
        self.assertTrue(any("uncompressed_size_limit_exceeded" in b for b in r.blockers))

    def test_private_key_redacted_and_blocked(self):
        secret_marker = "SENSITIVE_FIXTURE_74f8a55e_do_not_log_content"
        private = b"prefix -----BEGIN PRIVATE KEY----- foo " + secret_marker.encode()
        r = self.scan([("config/secret.txt", private)])
        self.assertTrue(any("sensitive_material_private_key" in b for b in r.blockers))
        serialized_report = json.dumps(r.as_dict())
        self.assertNotIn(secret_marker, serialized_report)
        self.assertNotIn("-----BEGIN PRIVATE KEY-----", serialized_report)

    def test_env_file_blocked_but_example_allowed(self):
        r = self.scan([(".env", b"APP_ENV=prod")])
        self.assertTrue(any("potential_live_environment_file" in b for b in r.blockers))
        r = self.scan([(".env.example", b"APP_ENV=dev")])
        self.assertEqual(r.blockers, [])

    def test_entry_count_limit(self):
        r = self.scan([("a.txt", b"1"), ("b.txt", b"2")], limit=scanner.Limits(members=1))
        self.assertIn("entry_count_limit_exceeded", r.blockers)

    def test_expected_file_count(self):
        r = self.scan([("ok.txt", b"1")], expected_count=92)
        self.assertIn("unexpected_regular_file_count", r.blockers)

    def test_evidence_record_validates_source(self):
        data = {"inputs": [{"id": "SRC-03", "sha256": "a" * 64, "file_count": 92}]}
        p = Path(self.tmp.name) / "sources.json"
        p.write_text(json.dumps(data))
        self.assertEqual(scanner.evidence_record(p), ("a" * 64, 92))
        with self.assertRaises(ValueError):
            scanner.evidence_record(p, "SRC-99")

    def test_cli_missing_archive_is_safe_nonzero(self):
        evidence = Path(self.tmp.name) / "sources.json"
        evidence.write_text(json.dumps({"inputs": [{"id": "SRC-03", "sha256": "a" * 64, "file_count": 2}]}))
        from contextlib import redirect_stdout
        buffer = io.StringIO()
        with redirect_stdout(buffer):
            code = scanner.main(["--archive", str(self.archive), "--evidence", str(evidence)])
        self.assertEqual(code, 2)
        self.assertEqual(json.loads(buffer.getvalue())["state"], "BLOCKED")



class ArchivePathHardeningTests(unittest.TestCase):
    setUp = ArchiveIntakeTests.setUp
    make_zip = ArchiveIntakeTests.make_zip
    scan = ArchiveIntakeTests.scan

    def test_unicode_decomposed_path_rejected(self):
        result = self.scan([("cafe\u0301.txt", b"x")])
        self.assertTrue(any("unicode_noncanonical_path" in x for x in result.blockers))

    def test_unicode_format_character_rejected(self):
        result = self.scan([("name\u202e.txt", b"x")])
        self.assertTrue(any("unicode_format_or_surrogate_path" in x for x in result.blockers))

    def test_windows_trailing_dot_rejected(self):
        result = self.scan([("folder./file.txt", b"x")])
        self.assertTrue(any("nonportable_path_component" in x for x in result.blockers))

    def test_embedded_git_metadata_rejected(self):
        result = self.scan([("source/.git/config", b"unsafe")])
        self.assertTrue(any("embedded_git_metadata" in x for x in result.blockers))

    def test_env_variant_is_blocked(self):
        result = self.scan([(".env.production", b"SECRET=hidden")])
        self.assertTrue(any("potential_live_environment_file" in x for x in result.blockers))

    def test_setuid_member_mode_is_blocked(self):
        info = zipfile.ZipInfo("script")
        info.create_system = 3
        info.external_attr = (stat.S_IFREG | stat.S_ISUID | 0o755) << 16
        result = self.scan([(info, b"echo nope")])
        self.assertTrue(any("privileged_mode_bits" in x for x in result.blockers))


if __name__ == "__main__":
    unittest.main()
