"""Offline negative cases for pinned R1 import bytes, not runtime security tests."""
import copy
import hashlib
import importlib.util
import os
from pathlib import Path
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[2]
spec = importlib.util.spec_from_file_location("foundation_import", ROOT / "scripts/check_foundation_import.py")
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


class R1ImportTests(unittest.TestCase):
    def setUp(self):
        self.dir = tempfile.TemporaryDirectory()
        self.addCleanup(self.dir.cleanup)
        self.root = Path(self.dir.name)
        self.root.joinpath("apps/panel").mkdir(parents=True)
        files = {
            '.gitignore': b'/apps/panel/.env\n',
            'apps/panel/.env.example': b'APP_SECRET=\n',
        }
        self.entries=[]
        for path, content in files.items():
            (self.root/path).write_bytes(content)
            self.entries.append({'path':path,'bytes':len(content),
                                 'sha256':hashlib.sha256(content).hexdigest(),
                                 'provenance':'adapted_template'})
        self.manifest={
            'schema_version':'forgepanel.foundation-import/v1',
            'source_id':'SRC-03','original_sha256':module.SOURCE_SHA,
            'original_regular_files':92,'review_status':'DRAFT_IMPORT_CANDIDATE',
            'runtime_certified':False,'installer_apply_allowed':False,
            'public_release_approved':False,'independent_security_review_complete':False,
            'imported_files':self.entries,
        }

    def validate(self):
        return module.validate(self.root, self.manifest, count=2)

    def test_synthetic_valid_metadata_is_not_release(self):
        report=self.validate()
        self.assertEqual(report['files_checked'],2)
        self.assertFalse(report['runtime_certified'])
        self.assertFalse(report['production_apply_allowed'])

    def test_wrong_archive_sha_rejected(self):
        self.manifest['original_sha256']='0'*64
        with self.assertRaises(module.ImportRejected):self.validate()

    def test_no_fake_runtime_certification(self):
        for key in ('runtime_certified','installer_apply_allowed',
                    'public_release_approved','independent_security_review_complete'):
            with self.subTest(key=key):
                self.manifest[key]=True
                with self.assertRaises(module.ImportRejected):self.validate()
                self.manifest[key]=False

    def test_mutated_bytes_rejected(self):
        (self.root/'.gitignore').write_bytes(b'/apps/panel/.env?\n')
        with self.assertRaises(module.ImportRejected):self.validate()

    def test_mutated_digest_rejected(self):
        self.entries[0]['sha256']='0'*64
        with self.assertRaises(module.ImportRejected):self.validate()

    def test_mutated_size_rejected(self):
        self.entries[0]['bytes']+=1
        with self.assertRaises(module.ImportRejected):self.validate()

    def test_duplicate_path_rejected(self):
        self.entries[1]['path']=self.entries[0]['path']
        with self.assertRaises(module.ImportRejected):self.validate()

    def test_path_traversal_rejected(self):
        self.entries[1]['path']='../outside.txt'
        with self.assertRaises(module.ImportRejected):self.validate()

    def test_absolute_path_rejected(self):
        self.entries[1]['path']='/etc/passwd'
        with self.assertRaises(module.ImportRejected):self.validate()

    def test_original_env_rejected(self):
        (self.root/'apps/panel/.env').write_text('SECRET=do-not-publish')
        with self.assertRaises(module.ImportRejected):self.validate()

    def test_symlink_rejected(self):
        (self.root/'apps/panel/.env.example').unlink()
        (self.root/'apps/panel/.env.example').symlink_to(self.root/'.gitignore')
        with self.assertRaises(module.ImportRejected):self.validate()

    def test_file_missing_rejected(self):
        (self.root/'.gitignore').unlink()
        with self.assertRaises(module.ImportRejected):self.validate()

    def test_no_unsafe_windows_paths(self):
        for path in ('C:/secret','.git/config',r'x\evil','two//parts'):
            with self.subTest(path=path):
                self.assertFalse(module.safe_path(path))

    def test_invalid_status_rejected(self):
        self.manifest['review_status']='APPROVED'
        with self.assertRaises(module.ImportRejected):self.validate()

    def test_invalid_count_rejected(self):
        with self.assertRaises(module.ImportRejected):module.validate(self.root,self.manifest,count=66)


if __name__ == '__main__':
    unittest.main()