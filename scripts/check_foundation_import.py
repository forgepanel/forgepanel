#!/usr/bin/env python3
"""Verify pinned Foundation v0.7 source import bytes (read-only).

Not a publisher signature, security review, source license or runtime approval.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import re
import stat
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "DOCUMENTATION/evidence/foundation-v07-import-candidate.json"
SOURCE_SHA = "19479d5be9da9bb0ff9180f9b8819ea48baff785ccc3fef59deb2bb0894faf1a"
SHA256 = re.compile(r"[a-f0-9]{64}\Z")
IMPORT_COUNT = 66

class ImportRejected(Exception):
    """No untrusted source bytes are included in error messages."""


def safe_path(name: str) -> bool:
    if not isinstance(name, str) or not name or "\\" in name or len(name) > 1024:
        return False
    parts = name.split("/")
    return all(part not in ("", ".", "..") and part.casefold() != ".git"
               and ":" not in part
               and all(32 <= ord(c) != 127 for c in part) for part in parts)


def validate(root: Path, manifest: dict, count: int = IMPORT_COUNT) -> dict:
    if (manifest.get("schema_version") != "forgepanel.foundation-import/v1"
            or manifest.get("source_id") != "SRC-03"
            or manifest.get("original_sha256") != SOURCE_SHA
            or manifest.get("original_regular_files") != 92):
        raise ImportRejected("source_provenance_mismatch")
    if (manifest.get("review_status") != "DRAFT_IMPORT_CANDIDATE"
            or manifest.get("runtime_certified") is not False
            or manifest.get("installer_apply_allowed") is not False
            or manifest.get("public_release_approved") is not False
            or manifest.get("independent_security_review_complete") is not False):
        raise ImportRejected("false_qualification_or_release_claim")
    entries = manifest.get("imported_files")
    if not isinstance(entries, list) or len(entries) != count:
        raise ImportRejected("unexpected_import_file_count")
    paths: set[str] = set()
    for entry in entries:
        if not isinstance(entry, dict) or set(entry) != {"path", "bytes", "sha256", "provenance"}:
            raise ImportRejected("invalid_file_record")
        name = entry["path"]
        if not safe_path(name) or name in paths:
            raise ImportRejected("unsafe_or_duplicate_file_path")
        if name in ("apps/panel/.env", "LICENSE", "composer.lock"):
            raise ImportRejected("disallowed_file_path")
        paths.add(name)
        digest = entry["sha256"]
        size = entry["bytes"]
        if (not isinstance(digest, str) or not SHA256.fullmatch(digest)
                or not isinstance(size, int) or isinstance(size, bool) or size < 0
                or entry["provenance"] not in ("exact_src03", "adapted_template")):
            raise ImportRejected("invalid_file_identity")
        dest = root.joinpath(*name.split("/"))
        try:
            # Reject symlinked path components, not only the final file.
            cursor = root
            for part in name.split("/"):
                cursor /= part
                meta = cursor.lstat()
                if stat.S_ISLNK(meta.st_mode):
                    raise ImportRejected("symlink_in_import_path")
            if not stat.S_ISREG(meta.st_mode) or meta.st_nlink != 1:
                raise ImportRejected("import_file_type_or_hardlink")
            if meta.st_size != size:
                raise ImportRejected("import_file_size_changed")
            h = hashlib.sha256()
            with dest.open("rb") as stream:
                for block in iter(lambda: stream.read(65536), b""):
                    h.update(block)
            if h.hexdigest() != digest:
                raise ImportRejected("import_file_bytes_changed")
        except (FileNotFoundError, NotADirectoryError, OSError) as exc:
            raise ImportRejected("import_file_missing_or_unreadable") from exc
    for forbidden in ("apps/panel/.env", "apps/panel/.env.local",
                      "apps/panel/.env.prod", "apps/panel/.env.production"):
        if (root / forbidden).exists() or (root / forbidden).is_symlink():
            raise ImportRejected("live_environment_file_present")
    if "apps/panel/.env.example" not in paths or ".gitignore" not in paths:
        raise ImportRejected("required_template_or_gitignore_absent")
    return {"status": "VERIFIED_SOURCE_BYTES_ONLY", "files_checked": len(paths),
            "source_import_sha256": manifest["original_sha256"],
            "production_apply_allowed": False, "runtime_certified": False,
            "source_license_cleared": False, "release_published": False}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=ROOT)
    parser.add_argument("--manifest", type=Path, default=MANIFEST)
    opt = parser.parse_args()
    try:
        result = validate(opt.root, json.loads(opt.manifest.read_text(encoding="utf-8")))
        code = 0
    except (ImportRejected, ValueError, OSError, TypeError) as exc:
        result = {"status": "BLOCKED", "reason": str(exc) if isinstance(exc, ImportRejected)
                  else "invalid_manifest_or_io", "production_apply_allowed": False,
                  "runtime_certified": False}
        code = 2
    print(json.dumps(result, indent=2, sort_keys=True))
    return code


if __name__ == "__main__":
    raise SystemExit(main())