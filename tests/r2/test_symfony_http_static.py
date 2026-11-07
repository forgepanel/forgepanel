"""Candidate static checks, NOT a substitute for a real booted Symfony kernel."""
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[2]


class R2HttpCandidateTests(unittest.TestCase):
    def test_test_file_guards_env(self):
        s = (ROOT / 'apps/panel/tests/http_r2.php').read_text()
        self.assertIn('APP_ENV', s)
        self.assertIn('PANEL_ORIGIN', s)
        self.assertIn('Symfony\\Component\\HttpFoundation\\Request', s)

    def test_negative_boundaries_in_smoke(self):
        s = (ROOT / 'apps/panel/tests/http_r2.php').read_text()
        for token in ('insecure', 'wrongHost', 'wrongPort', 'wrongOrigin', 'tooLarge', 'missingCsrf', 'no-store'):
            with self.subTest(token=token):
                self.assertIn(token, s)

    def test_workflow_no_release_or_prod(self):
        s = (ROOT / '.github/workflows/r2-symfony-http-candidate.yml').read_text()
        self.assertIn('composer update', s)
        self.assertIn('composer audit', s)
        self.assertIn('forgepanel_test', s)
        self.assertNotIn('install apply', s)

    def test_bootstrap_requires_real_secret_without_env_file(self):
        src = (ROOT / 'apps/panel/config/bootstrap.php').read_text()
        self.assertIn('is_file($localEnv)', src)
        self.assertIn("is_file('/etc/forgepanel/panel.env')", src)
        self.assertIn('strlen($secret) < 32', src)
        self.assertNotIn('.env.example', src.split('if (is_file($localEnv))')[1])

    def test_pair_metadata(self):
        en = (ROOT / 'DOCUMENTATION/en/13-tests-quality/r2-symfony-http-smoke.md').read_text()
        fr = (ROOT / 'DOCUMENTATION/fr/13-tests-quality/r2-symfony-http-smoke.md').read_text()
        prefix = '<!-- forgepanel-doc id=FP-13-R2-HTTP-SMOKE revision=2 status=specified -->'
        self.assertTrue(en.startswith(prefix) and fr.startswith(prefix))


if __name__ == '__main__':
    unittest.main()