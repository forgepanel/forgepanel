"""Synthetic offline negative tests for v0.7.1 source patch checks."""
import copy
import hashlib
import importlib.util
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch as mock_patch

ROOT = Path(__file__).resolve().parents[2]
spec = importlib.util.spec_from_file_location("mfa_import_check", ROOT / "scripts/check_foundation_import.py")
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)


class OptionalMfaImportTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root=Path(self.tmp.name)
        for p in (".gitignore","apps/panel/.env.example"):
            (self.root/p).parent.mkdir(parents=True,exist_ok=True)
            (self.root/p).write_text('safe')
        self.base={'schema_version':'forgepanel.foundation-import/v1','source_id':'SRC-03',
                   'original_sha256':mod.SOURCE_SHA,'original_regular_files':92,
                   'review_status':'DRAFT_IMPORT_CANDIDATE','runtime_certified':False,
                   'installer_apply_allowed':False,'public_release_approved':False,
                   'independent_security_review_complete':False,
                   'imported_files':[]}
        for p in ('.gitignore','apps/panel/.env.example'):
            content=(self.root/p).read_bytes()
            self.base['imported_files'].append({'path':p,'bytes':len(content),
                 'sha256':hashlib.sha256(content).hexdigest(),'provenance':'adapted_template'})
        self.patch={'schema_version':'forgepanel.foundation-optional-mfa/v1',
                    'source_id':'SRC-03-OPTIONAL-MFA-071','status':'DRAFT_PATCH_NOT_QUALIFIED',
                    'base_archive_sha256':mod.SOURCE_SHA,'patch_archive_sha256':mod.PATCH_SHA,
                    'changed_file_count':11,'admin_mfa_optional':True,
                    'real_postgresql_migration_tested':False,'real_symfony_http_tested':False,
                    'runtime_release_certified':False,'production_apply_authorized':False,
                    'independent_security_review_complete':False,'records':[]}
        # The actual validator requires precisely 11 real patch records;
        # use these tests to prove non-approved/fabricated manifests fail closed.

    def reject(self):
        with self.assertRaises(mod.ImportRejected):
            mod.validate_optional_patch(self.root,self.base,self.patch)

    def test_no_unsubstantiated_patch_acceptance(self):
        self.reject()

    def test_incorrect_publisher_sha_denied(self):
        self.patch['patch_archive_sha256']='0'*64
        self.reject()

    def test_runtime_promotion_denied(self):
        self.patch['runtime_release_certified']=True
        self.reject()

    def test_invented_sql_success_denied(self):
        self.patch['real_postgresql_migration_tested']=True
        self.reject()

    def test_root_apply_authority_denied(self):
        self.patch['production_apply_authorized']=True
        self.reject()

    def test_mfa_not_optional_denied(self):
        self.patch['admin_mfa_optional']=False
        self.reject()

    def test_wrong_source_id_denied(self):
        self.patch['source_id']='UNTRUSTED'
        self.reject()

    def test_wrong_patch_status_denied(self):
        self.patch['status']='PRODUCTION'
        self.reject()

    def test_wrong_changed_count_denied(self):
        self.patch['changed_file_count']=10
        self.reject()

    def test_missing_patch_records_denied(self):
        self.patch.pop('records')
        self.reject()




class OptionalMfaPatchIntegrationTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root=Path(self.tmp.name)
        self.before=[]
        self.after=[]
        for name in ['.gitignore','apps/panel/.env.example'] + [f'apps/panel/src/OptionalPatchFixture{i}.php' for i in range(8)]:
            path=self.root/name
            path.parent.mkdir(parents=True,exist_ok=True)
            base_content=b'baseline'
            new_content=b'mfa_patched'
            path.write_bytes(new_content)
            old=hashlib.sha256(base_content).hexdigest()
            digest=hashlib.sha256(new_content).hexdigest()
            self.before.append({'path':name,'bytes':len(base_content),'sha256':old,
                                'provenance':'exact_src03'})
            self.after.append({'path':name,'base_sha256':old,'new_sha256':digest,
                               'new_bytes':len(new_content)})
        sql=self.root/mod.OPTIONAL_PATCH_FILE
        sql.parent.mkdir(parents=True,exist_ok=True)
        sql_bytes=b'ALTER TABLE fp_admins ALTER COLUMN mfa_secret DROP NOT NULL;'
        sql.write_bytes(sql_bytes)
        self.after.append({'path':mod.OPTIONAL_PATCH_FILE,'base_sha256':None,
                           'new_sha256':hashlib.sha256(sql_bytes).hexdigest(),
                           'new_bytes':len(sql_bytes)})
        self.base={'schema_version':'forgepanel.foundation-import/v1',
                   'source_id':'SRC-03','original_sha256':mod.SOURCE_SHA,
                   'original_regular_files':92,'review_status':'DRAFT_IMPORT_CANDIDATE',
                   'runtime_certified':False,'installer_apply_allowed':False,
                   'public_release_approved':False,'independent_security_review_complete':False,
                   'imported_files':self.before}
        self.patch={'schema_version':'forgepanel.foundation-optional-mfa/v1',
                   'source_id':'SRC-03-OPTIONAL-MFA-071','status':'DRAFT_PATCH_NOT_QUALIFIED',
                   'base_archive_sha256':mod.SOURCE_SHA,'patch_archive_sha256':mod.PATCH_SHA,
                   'changed_file_count':11,'admin_mfa_optional':True,
                   'real_postgresql_migration_tested':False,'real_symfony_http_tested':False,
                   'runtime_release_certified':False,'production_apply_authorized':False,
                   'independent_security_review_complete':False,'records':self.after}

    def validate(self):
        original=mod.validate
        with mock_patch.object(mod,'validate',side_effect=lambda root, base, overlay:
                               original(root,base,count=10,overlay=overlay)):
            return mod.validate_optional_patch(self.root,self.base,self.patch)

    def test_approved_synthetic_bytes_are_not_runtime_verified(self):
        status=self.validate()
        self.assertEqual(status['optional_patch_files_checked'],11)
        self.assertFalse(status['runtime_certified'])

    def test_changed_patch_file_blocked(self):
        (self.root/self.after[0]['path']).write_bytes(b'not_the_patch')
        with self.assertRaises(mod.ImportRejected):self.validate()

    def test_wrong_base_digest_blocked(self):
        self.after[0]['base_sha256']='0'*64
        with self.assertRaises(mod.ImportRejected):self.validate()

    def test_duplicate_patch_target_blocked(self):
        self.after[1]['path']=self.after[0]['path']
        with self.assertRaises(mod.ImportRejected):self.validate()

    def test_missing_sql_migration_blocked(self):
        (self.root/mod.OPTIONAL_PATCH_FILE).unlink()
        with self.assertRaises(mod.ImportRejected):self.validate()

    def test_modified_sql_migration_blocked(self):
        (self.root/mod.OPTIONAL_PATCH_FILE).write_bytes(b'ALTER TABLE wrong;')
        with self.assertRaises(mod.ImportRejected):self.validate()

    def test_extra_untrusted_file_blocked(self):
        self.after[-1]['path']='../../etc/passwd'
        with self.assertRaises(mod.ImportRejected):self.validate()

    def test_wrong_patch_sha256_format_blocked(self):
        self.after[0]['new_sha256']='unsafe'
        with self.assertRaises(mod.ImportRejected):self.validate()

    def test_sensitive_environment_never_passes(self):
        path=self.root/'apps/panel/.env'
        path.write_bytes(b'private data')
        with self.assertRaises(mod.ImportRejected):self.validate()


if __name__ == '__main__':unittest.main()