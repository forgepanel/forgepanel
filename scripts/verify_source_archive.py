#!/usr/bin/env python3
"""Read-only preflight for a provenance-pinned ForgePanel source ZIP.

This scanner neither extracts nor executes archive members. SHA-256 validates
identity relative to repository evidence, not publisher authenticity.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import stat
import unicodedata
import zipfile
import zlib
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_EVIDENCE = ROOT / "DOCUMENTATION" / "evidence" / "sources.json"
ALLOWED_METHODS = {zipfile.ZIP_STORED, zipfile.ZIP_DEFLATED}
SECRET_RULES = (
    ("private_key", re.compile(rb"-----BEGIN (?:[A-Z0-9 ]+ )?PRIVATE KEY-----")),
    ("github_token", re.compile(rb"\bgh[pousr]_[A-Za-z0-9]{36,}\b")),
    ("aws_access_key", re.compile(rb"\bAKIA[A-Z0-9]{16}\b")),
)


@dataclass(frozen=True)
class Limits:
    archive_bytes: int = 64 * 1024 * 1024
    members: int = 2048
    member_bytes: int = 32 * 1024 * 1024
    expanded_bytes: int = 160 * 1024 * 1024
    compression_ratio: int = 500


@dataclass
class Report:
    source_id: str
    archive_sha256: str = ""
    expected_sha256: str = ""
    expected_files: int = 0
    file_count: int = 0
    expanded_bytes: int = 0
    entries: list[dict[str, Any]] = field(default_factory=list)
    blockers: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)

    def as_dict(self) -> dict[str, Any]:
        return {
            "source_id": self.source_id,
            "state": "PASS" if not self.blockers else "BLOCKED",
            "archive_sha256": self.archive_sha256,
            "expected_sha256": self.expected_sha256,
            "expected_files": self.expected_files,
            "file_count": self.file_count,
            "expanded_bytes": self.expanded_bytes,
            "entries": self.entries,
            "blockers": self.blockers,
            "warnings": self.warnings,
            "archive_extracted": False,
            "archive_executed": False,
            "runtime_certified": False,
        }


def evidence_record(evidence: Path, source_id: str = "SRC-03") -> tuple[str, int]:
    data = json.loads(evidence.read_text(encoding="utf-8"))
    matching = [row for row in data.get("inputs", []) if row.get("id") == source_id]
    if len(matching) != 1:
        raise ValueError("Exactly one matching source identity is required")
    row = matching[0]
    sha = row.get("sha256", "")
    files = row.get("file_count")
    if not isinstance(sha, str) or not re.fullmatch(r"[0-9a-f]{64}", sha):
        raise ValueError("Source evidence must contain a 64-character lowercase SHA-256")
    if not isinstance(files, int) or isinstance(files, bool) or files <= 0:
        raise ValueError("Source evidence must have a positive integer file_count")
    return sha, files


def sha256_file(path: Path, chunk_size: int = 128 * 1024) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(chunk_size), b""):
            digest.update(chunk)
    return digest.hexdigest()


def unsafe_name(name: str, is_dir: bool) -> str | None:
    if not name or len(name) > 1024 or any(ord(char) < 32 or ord(char) == 127 for char in name):
        return "invalid_name"
    if name.startswith("/") or re.match(r"^[A-Za-z]:", name) or "\\" in name:
        return "absolute_or_non_posix_path"
    if unicodedata.normalize("NFC", name) != name:
        return "unicode_noncanonical_path"
    if any(unicodedata.category(char) in ("Cf", "Cs") for char in name):
        return "unicode_format_or_surrogate_path"
    pieces = name[:-1].split("/") if is_dir and name.endswith("/") else name.split("/")
    if any(piece in ("", ".", "..") for piece in pieces):
        return "unsafe_path_component"
    if any(":" in piece or piece.rstrip(" .") != piece for piece in pieces):
        return "nonportable_path_component"
    if any(piece.casefold() == ".git" for piece in pieces):
        return "embedded_git_metadata"
    return None


def entry_kind(info: zipfile.ZipInfo) -> str:
    if info.create_system == 3:
        mode = (info.external_attr >> 16) & 0xFFFF
        if mode & (stat.S_ISUID | stat.S_ISGID):
            return "privileged_mode_bits"
        unix_type = stat.S_IFMT(mode)
        if unix_type and unix_type not in (stat.S_IFREG, stat.S_IFDIR):
            return "special_file_or_symlink"
        if unix_type == stat.S_IFREG and info.is_dir():
            return "file_directory_conflict"
        if unix_type == stat.S_IFDIR and not info.is_dir():
            return "file_directory_conflict"
    return "directory" if info.is_dir() else "regular"


def scan_archive(
    archive: Path, expected_sha256: str, expected_files: int,
    source_id: str = "SRC-03", limits: Limits = Limits(),
) -> Report:
    report = Report(source_id=source_id, expected_sha256=expected_sha256, expected_files=expected_files)
    if not archive.is_file():
        report.blockers.append("archive_unavailable")
        return report
    if archive.stat().st_size > limits.archive_bytes:
        report.blockers.append("archive_size_limit_exceeded")
        return report
    report.archive_sha256 = sha256_file(archive)
    if report.archive_sha256 != expected_sha256:
        report.blockers.append("archive_sha256_mismatch")
        # Do not parse or trust source whose identity differs from recorded evidence.
        return report

    seen: set[str] = set()
    regular_files: set[str] = set()
    try:
        with zipfile.ZipFile(archive) as zf:
            infos = zf.infolist()
            if len(infos) > limits.members:
                report.blockers.append("entry_count_limit_exceeded")
                return report
            for info in infos:
                kind = entry_kind(info)
                normalized = info.filename.rstrip("/")
                error = unsafe_name(info.filename, info.is_dir())
                if error:
                    report.blockers.append(f"{error}:{info.filename!r}")
                    continue
                if kind in ("special_file_or_symlink", "file_directory_conflict", "privileged_mode_bits"):
                    report.blockers.append(f"{kind}:{info.filename!r}")
                    continue
                folded = normalized.casefold()
                if folded in seen:
                    report.blockers.append(f"duplicate_or_casefold_collision:{info.filename!r}")
                    continue
                seen.add(folded)
                if kind == "regular":
                    regular_files.add(folded)
                if info.flag_bits & 1:
                    report.blockers.append(f"encrypted_member:{info.filename!r}")
                    continue
                if info.compress_type not in ALLOWED_METHODS:
                    report.blockers.append(f"unsupported_compression:{info.filename!r}")
                    continue
                if kind == "directory":
                    continue
                report.file_count += 1
                if info.file_size > limits.member_bytes or report.expanded_bytes + info.file_size > limits.expanded_bytes:
                    report.blockers.append(f"uncompressed_size_limit_exceeded:{info.filename!r}")
                    continue
                if info.file_size > limits.compression_ratio * max(info.compress_size, 1):
                    report.blockers.append(f"compression_ratio_limit_exceeded:{info.filename!r}")
                    continue
                digest = hashlib.sha256()
                scanned = 0
                overlap = b""
                matches: set[str] = set()
                with zf.open(info, "r") as stream:
                    while chunk := stream.read(128 * 1024):
                        scanned += len(chunk)
                        if scanned > limits.member_bytes or report.expanded_bytes + scanned > limits.expanded_bytes:
                            raise ValueError("uncompressed_size_limit_exceeded")
                        digest.update(chunk)
                        sample = overlap + chunk
                        for rule_name, pattern in SECRET_RULES:
                            if pattern.search(sample):
                                matches.add(rule_name)
                        overlap = sample[-128:]
                if scanned != info.file_size:
                    report.blockers.append(f"member_size_mismatch:{info.filename!r}")
                report.expanded_bytes += scanned
                report.entries.append({"path": normalized, "bytes": scanned, "sha256": digest.hexdigest()})
                for match in sorted(matches):
                    # Never echo secret values into reports or CI logs.
                    report.blockers.append(f"sensitive_material_{match}:{info.filename!r}")
                base_name = normalized.split("/")[-1].casefold()
                safe_env_templates = {".env.example", ".env.sample", ".env.dist", ".env.template"}
                if base_name == ".env" or (base_name.startswith(".env.") and base_name not in safe_env_templates):
                    report.blockers.append(f"potential_live_environment_file:{info.filename!r}")
                elif normalized.endswith((".key", ".pem", ".p12", ".pfx")):
                    report.warnings.append(f"manual_key_material_review_required:{info.filename!r}")
            for path in regular_files:
                parts = path.split("/")
                if any("/".join(parts[:i]) in regular_files for i in range(1, len(parts))):
                    report.blockers.append(f"file_directory_collision:{path!r}")
            if report.file_count != expected_files:
                report.blockers.append("unexpected_regular_file_count")
    except (zipfile.BadZipFile, zlib.error, EOFError, OSError, RuntimeError, ValueError) as exc:
        # Never include untrusted extracted bytes or exception payload from member in output.
        report.blockers.append(f"archive_read_or_integrity_error:{type(exc).__name__}")
    return report


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--archive", required=True, type=Path, help="Local owner-supplied source ZIP; read-only")
    parser.add_argument("--evidence", type=Path, default=DEFAULT_EVIDENCE)
    parser.add_argument("--source-id", default="SRC-03")
    options = parser.parse_args(argv)
    try:
        expected_sha, expected_count = evidence_record(options.evidence, options.source_id)
        report = scan_archive(options.archive, expected_sha, expected_count, options.source_id)
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(json.dumps({"state": "BLOCKED", "source_id": options.source_id, "blockers": [f"invalid_evidence_or_input:{type(exc).__name__}"]}))
        return 2
    print(json.dumps(report.as_dict(), sort_keys=True, ensure_ascii=True, indent=2))
    return 0 if not report.blockers else 2


if __name__ == "__main__":
    raise SystemExit(main())
