#!/usr/bin/env python3
"""Validate ForgePanel documentation; never claim product/security certification."""
from __future__ import annotations
import argparse
import json
import re
from pathlib import Path
from urllib.parse import unquote, urlsplit

CATEGORIES = (
    '00-project-control', '01-product', '02-architecture', '03-core',
    '04-modules', '05-plugins', '06-apps-recipes', '07-interfaces-roles',
    '08-api-contracts', '09-database', '10-security', '11-design-system',
    '12-development', '13-tests-quality', '14-devops-releases',
    '15-operations', '16-performance', '17-user-guides',
    '18-contributing', '19-audits-risks',
)
META = re.compile(r'<!-- forgepanel-doc id=([A-Z0-9-]+) revision=(\d+) status=([a-z-]+) -->')
LINK = re.compile(r'!?\[[^\]\n]*\]\(([^\s)]+)(?:\s+"[^"]*")?\)')
IDENTIFIERS = re.compile(r'\b(?:ADR-\d{3}|REQ-\d{3}|RISK-\d{3}|CMP-[A-Z0-9-]+)\b')
SECRETS = (
    re.compile(r'-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----'),
    re.compile(r'\bgh[pousr]_[A-Za-z0-9]{36,}\b'),
    re.compile(r'\bAKIA[A-Z0-9]{16}\b'),
)


def check(root: Path) -> tuple[list[str], dict[str, int]]:
    root = root.resolve()
    errors: list[str] = []
    stats = {'markdown_files': 0, 'document_pairs': 0, 'relative_links': 0}
    required = ['README.md', 'README.fr.md', 'AGENTS.md', 'CONTRIBUTING.md',
                'SECURITY.md', 'DOCUMENTATION/README.md', 'CHANGELOG/CHANGELOG.md']
    for name in required:
        if not (root / name).is_file():
            errors.append(f'Missing entry point: {name}')
    for lang in ('en', 'fr'):
        for category in CATEGORIES:
            if not (root / 'DOCUMENTATION' / lang / category / 'README.md').is_file():
                errors.append(f'Missing category: {lang}/{category}')
    maps = {lang: {p.relative_to(root / 'DOCUMENTATION' / lang): p
                  for p in (root / 'DOCUMENTATION' / lang).rglob('*.md')}
            for lang in ('en', 'fr')}
    if set(maps['en']) != set(maps['fr']):
        errors.append('Language file sets differ')
    for lang, files in maps.items():
        ids: set[str] = set()
        for relative, path in files.items():
            text = path.read_text(encoding='utf-8')
            match = META.search(text)
            if not match:
                errors.append(f'Missing metadata: {lang}/{relative}')
            else:
                if match[1] in ids:
                    errors.append(f'Duplicate document ID: {lang}/{match[1]}')
                ids.add(match[1])
            if len(text.strip()) < 180:
                errors.append(f'Insufficient document content: {lang}/{relative}')
    for relative in sorted(set(maps['en']) & set(maps['fr'])):
        a, b = maps['en'][relative], maps['fr'][relative]
        ta, tb = a.read_text(encoding='utf-8'), b.read_text(encoding='utf-8')
        ma, mb = META.search(ta), META.search(tb)
        if ma and mb and ma.groups() != mb.groups():
            errors.append(f'Metadata mismatch: {relative}')
        if set(IDENTIFIERS.findall(ta)) != set(IDENTIFIERS.findall(tb)):
            errors.append(f'Shared requirement identifiers differ: {relative}')
        for source, target, text in ((a, b, ta), (b, a, tb)):
            local_links = [urlsplit(v).path for v in LINK.findall(text)
                           if not urlsplit(v).scheme and not urlsplit(v).netloc]
            if not any((source.parent / unquote(v)).resolve() == target.resolve()
                       for v in local_links if v):
                errors.append(f'Missing language backlink: {source.relative_to(root)}')
        stats['document_pairs'] += 1
    markdown = sorted(root.rglob('*.md'))
    markdown = [p for p in markdown if '.git' not in p.relative_to(root).parts]
    stats['markdown_files'] = len(markdown)
    for path in markdown:
        text = path.read_text(encoding='utf-8')
        visible = re.sub(r'(?ms)^```[^\n]*\n.*?^```\s*$', '', text)
        for raw in LINK.findall(visible):
            url = urlsplit(raw)
            if url.scheme or url.netloc or not url.path:
                continue
            dest = (path.parent / unquote(url.path)).resolve()
            if not dest.is_relative_to(root):
                errors.append(f'Link escapes repository: {path.relative_to(root)} -> {raw}')
            elif not dest.exists():
                errors.append(f'Broken relative link: {path.relative_to(root)} -> {raw}')
            stats['relative_links'] += 1
        if any(pattern.search(text) for pattern in SECRETS):
            errors.append(f'Potential secret pattern: {path.relative_to(root)}')
    changelogs = [p.relative_to(root).as_posix() for p in markdown
                  if p.name.lower() == 'changelog.md']
    if changelogs != ['CHANGELOG/CHANGELOG.md']:
        errors.append(f'Expected one central changelog, found: {changelogs}')
    central = root / 'CHANGELOG/CHANGELOG.md'
    if central.exists() and '## Unreleased / Non publié' not in central.read_text(encoding='utf-8'):
        errors.append('Missing bilingual Unreleased section')
    for path in (root / 'DOCUMENTATION').rglob('*.json'):
        text = path.read_text(encoding='utf-8')
        try:
            json.loads(text)
        except json.JSONDecodeError as exc:
            errors.append(f'Invalid JSON: {path.relative_to(root)}: {exc}')
        if any(pattern.search(text) for pattern in SECRETS):
            errors.append(f'Potential secret pattern: {path.relative_to(root)}')
    return errors, stats


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, default=Path(__file__).resolve().parents[1])
    args = parser.parse_args()
    try:
        errors, stats = check(args.root)
    except (OSError, UnicodeError, ValueError) as exc:
        print(f'FAIL: cannot inspect documentation: {exc}')
        return 1
    for error in errors:
        print(f'FAIL: {error}')
    print(json.dumps(stats, sort_keys=True))
    print('FAIL' if errors else 'PASS: documentation checks only; no product certification.')
    return 1 if errors else 0


if __name__ == '__main__':
    raise SystemExit(main())
