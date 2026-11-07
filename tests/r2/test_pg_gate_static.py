"""Source/static gates only; these are NOT PostgreSQL runtime verification."""
import pathlib
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[2]


class R2PostgresPolicyTests(unittest.TestCase):
    def test_production_guard(self):
        content = (ROOT / 'apps/panel/tests/postgres_r2.php').read_text()
        for token in ('FORGE_TEST_ALLOW_SCHEMA_CREATE', "'_test'", 'pdo_pgsql', 'random_bytes', 'DROP SCHEMA'):
            with self.subTest(token=token):
                self.assertIn(token, content)

    def test_live_lock_and_unique_admin_denials(self):
        src = (ROOT / 'apps/panel/tests/postgres_r2.php').read_text()
        for token in ('FOR UPDATE', '55P03', '23505', 'mfa_secret', 'skipMfa(', 'redeemResume', 'stale revision'):
            with self.subTest(token=token):
                self.assertIn(token, src)

    def test_workflow_has_test_only_service(self):
        flow = (ROOT / '.github/workflows/r2-postgres-disposable.yml').read_text()
        for token in ('forgepanel_test', 'postgres:16', 'POSTGRES_DB', 'php8.3-pgsql',
                      'php apps/panel/tests/postgres.php', 'php apps/panel/tests/postgres_r2.php'):
            with self.subTest(token=token):
                self.assertIn(token, flow)
        self.assertNotIn('install apply', flow)

    def test_bilingual_docs_paired(self):
        fr = ROOT / 'DOCUMENTATION/fr/13-tests-quality/r2-postgres-execution.md'
        en = ROOT / 'DOCUMENTATION/en/13-tests-quality/r2-postgres-execution.md'
        self.assertTrue(fr.is_file() and en.is_file())
        tag = '<!-- forgepanel-doc id=FP-13-R2-POSTGRES revision=1 status=specified -->'
        self.assertTrue(fr.read_text().startswith(tag))
        self.assertTrue(en.read_text().startswith(tag))


if __name__ == '__main__':
    unittest.main()