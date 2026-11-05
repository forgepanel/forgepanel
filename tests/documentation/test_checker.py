"""Positive and negative fixtures for the documentation checker."""
import importlib.util
import os
from pathlib import Path
import tempfile
import unittest

MODULE = Path(os.environ.get('FORGE_DOC_CHECKER', str(Path(__file__).resolve().parents[2] / 'scripts/check_documentation.py')))
spec = importlib.util.spec_from_file_location('checker', MODULE)
checker = importlib.util.module_from_spec(spec)
spec.loader.exec_module(checker)


class DocumentationChecks(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        self.addCleanup(self.tmp.cleanup)
        for name in ('README.md', 'README.fr.md', 'AGENTS.md', 'CONTRIBUTING.md', 'SECURITY.md', 'DOCUMENTATION/README.md'):
            self.write(name, '# Test entry\n')
        self.write('CHANGELOG/CHANGELOG.md', '# Changelog\n\n## Unreleased / Non publié\n')
        for i, name in enumerate(['README.md'] + [v + '/README.md' for v in checker.CATEGORIES]):
            for lang, other in (('en', 'fr'), ('fr', 'en')):
                path = self.root / 'DOCUMENTATION' / lang / name
                target = self.root / 'DOCUMENTATION' / other / name
                link = os.path.relpath(target, path.parent)
                text = f'<!-- forgepanel-doc id=FP-TEST-{i} revision=1 status=documented -->\n# Fixture\n[Translation]({link})\n' + ('This synthetic test document exercises checker behavior, not product evidence. ' * 4)
                self.write(str(path.relative_to(self.root)), text)

    def write(self, name, text):
        path = self.root / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding='utf-8')

    def assert_failure(self, fragment):
        errors, _ = checker.check(self.root)
        self.assertTrue(any(fragment in error for error in errors), errors)

    def test_valid_fixture(self):
        errors, stats = checker.check(self.root)
        self.assertEqual([], errors)
        self.assertEqual(21, stats['document_pairs'])

    def test_missing_translation(self):
        (self.root / 'DOCUMENTATION/fr/README.md').unlink()
        self.assert_failure('Language file sets differ')

    def test_revision_mismatch(self):
        p = self.root / 'DOCUMENTATION/fr/README.md'
        p.write_text(p.read_text().replace('revision=1', 'revision=2'))
        self.assert_failure('Metadata mismatch')

    def test_broken_link(self):
        self.write('README.md', '[Missing](does-not-exist.md)')
        self.assert_failure('Broken relative link')

    def test_path_escape(self):
        self.write('README.md', '[Outside](../../outside.md)')
        self.assert_failure('Link escapes repository')

    def test_duplicate_changelog(self):
        self.write('CHANGELOG.md', '# Duplicate')
        self.assert_failure('Expected one central changelog')

    def test_secret_pattern(self):
        self.write('README.md', '-----BEGIN ' + 'PRIVATE KEY-----')
        self.assert_failure('Potential secret pattern')

    def test_missing_language_backlink(self):
        p = self.root / 'DOCUMENTATION/fr/README.md'
        p.write_text(p.read_text().replace('[Translation]', '[Translation removed] ').replace('](../en/README.md)', ']'))
        self.assert_failure('Missing language backlink')

    def test_requirement_mismatch(self):
        p = self.root / 'DOCUMENTATION/en/README.md'
        p.write_text(p.read_text() + '\nREQ-099\n')
        self.assert_failure('Shared requirement identifiers differ')

    def test_invalid_json(self):
        self.write('DOCUMENTATION/evidence/broken.json', '{bad json')
        self.assert_failure('Invalid JSON')


if __name__ == '__main__':
    unittest.main()
