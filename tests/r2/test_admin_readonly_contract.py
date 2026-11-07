"""R2 static safety policy checks; these do NOT replace live SQL/HTTP evidence."""
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[2]


class AdminReadonlyPolicy(unittest.TestCase):
    def test_no_privileged_operations(self):
        src = (ROOT / 'apps/panel/src/Controller/AdminSessionController.php').read_text()
        for forbidden in ('shell_exec(', 'system(', 'passthru(', 'proc_open(', 'Hub', 'install apply', 'docker.sock'):
            self.assertNotIn(forbidden, src)
        self.assertIn("#[Route('/admin'", src)
        self.assertIn('readonly', src)

    def test_sql_session_revalidation_and_hmac(self):
        src = (ROOT / 'apps/panel/src/Identity/AdminAuthentication.php').read_text()
        for required in ('password_verify(', 'hash_hmac(', 'hash_equals(', 'REVIEWED', 'fp_admins', 'last_totp_counter', 'FOR UPDATE', 'recovery_hashes', 'auth.login_rejected'):
            self.assertIn(required, src)
        self.assertNotIn('shell_exec(', src)

    def test_csrf_rate_limit_logout_and_rotation(self):
        src = (ROOT / 'apps/panel/src/Controller/AdminSessionController.php').read_text()
        for required in ('admin-login', 'admin-logout', 'login_ip', 'login_identity', '->migrate(true)', '->invalidate()', 'forge_admin_seal', 'MAX_SESSION_AGE_SECONDS'):
            self.assertIn(required, src)
        self.assertNotIn('setup_grant', (ROOT / 'apps/panel/templates/auth/readonly.html.twig').read_text())

    def test_no_trusted_forwarding_and_host_session_protection(self):
        cfg = (ROOT / 'apps/panel/config/packages/framework.yaml').read_text()
        for required in ('__Host-FORGE_ADMIN', 'cookie_secure: true', 'cookie_httponly: true', 'cookie_samesite: strict', 'admin_login_ip:', 'admin_login_identity:'):
            self.assertIn(required, cfg)
        security = (ROOT / 'apps/panel/config/packages/security.yaml').read_text()
        self.assertIn('default_deny:', security)
        self.assertIn('ROLE_SUPER_ADMIN', security)

    def test_mfa_replay_recovery_are_atomic(self):
        src = (ROOT / 'apps/panel/src/Identity/AdminAuthentication.php').read_text()
        self.assertIn('last_totp_counter<:previous', src)
        self.assertIn('array_values($hashes)', src)
        self.assertIn('SET LOCAL lock_timeout', src)
        self.assertIn('rollBack()', src)

    def test_ephemeral_postgres_refusal_and_consent(self):
        for path in ('apps/panel/tests/admin_identity_r2.php', 'apps/panel/tests/admin_http_r2.php'):
            src = (ROOT / path).read_text()
            for required in ('FORGE_TEST_ALLOW_SCHEMA_CREATE', "'_test'", 'DROP SCHEMA', 'APP_ENV'):
                self.assertIn(required, src)
        flow = (ROOT / '.github/workflows/r2-admin-readonly-candidate.yml').read_text()
        self.assertIn('composer install', flow)
        self.assertNotIn('composer update', flow)
        self.assertNotIn('install apply', flow)

    def test_bilingual_records_paired(self):
        for basename, tag in [
            ('03-core/admin-identity-r2.md', 'FP-03-ADMIN-IDENTITY-R2'),
            ('13-tests-quality/r2-admin-readonly-qa.md', 'FP-13-R2-ADMIN-QA'),
        ]:
            for lang in ('en', 'fr'):
                p = ROOT / 'DOCUMENTATION' / lang / basename
                self.assertTrue(p.is_file(), p)
                self.assertTrue(p.read_text().startswith(f'<!-- forgepanel-doc id={tag} revision=1 status=specified -->'))


if __name__ == '__main__':
    unittest.main()
