#!/usr/bin/env python3
"""Read-only verification of a private, quarantined ForgePanel source ZIP.

Requires the original ZIP, canonical provenance and the staging receipt.
Does not execute source, import source into Git or modify the quarantine.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import stat
import zipfile
from pathlib import Path
from typing import Any

from stage_source_archive import RECEIPT
from verify_source_archive import DEFAULT_EVIDENCE, evidence_record, scan_archive, sha256_file, unsafe_name

MAX_RECEIPT_BYTES = 2 * 1024 * 1024
MAX_STAGED_ENTRIES = 4096
MAX_STAGED_BYTES = 160 * 1024 * 1024


class AuditRejected(Exception):
    """A fail-closed, non-secret staging audit error."""


def _validate_receipt(data: Any, expected_sha: str, expected_count: int,
                      source_id: str, zip_entries: list[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    if not isinstance(data, dict) or set(data) != {
        "schema_version", "source_id", "archive_sha256", "file_count",
        "files", "status", "import_approved", "executed",
    }:
        raise AuditRejected("invalid_receipt_schema")
    if (
        data["schema_version"] != 1
        or data["source_id"] != source_id
        or data["archive_sha256"] != expected_sha
        or data["file_count"] != expected_count
        or data["status"] != "STAGED_FOR_MANUAL_REVIEW"
        or data["import_approved"] is not False
        or data["executed"] is not False
    ):
        raise AuditRejected("receipt_provenance_or_state_mismatch")
    files = data.get("files")
    if not isinstance(files, list) or len(files) != expected_count:
        raise AuditRejected("invalid_receipt_file_count")
    entries: dict[str, dict[str, Any]] = {}
    for entry in files:
        if not isinstance(entry, dict) or set(entry) != {"path", "bytes", "sha256"}:
            raise AuditRejected("invalid_receipt_file_entry")
        path, size, digest = entry["path"], entry["bytes"], entry["sha256"]
        if not isinstance(path, str) or unsafe_name(path, False) or path == RECEIPT:
            raise AuditRejected("invalid_receipt_path")
        if not isinstance(size, int) or isinstance(size, bool) or size < 0:
            raise AuditRejected("invalid_receipt_file_size")
        if not isinstance(digest, str) or len(digest) != 64 or any(c not in "0123456789abcdef" for c in digest):
            raise AuditRejected("invalid_receipt_digest")
        if path in entries:
            raise AuditRejected("duplicate_receipt_file")
        entries[path] = entry
    if sorted(files, key=lambda e: e["path"]) != sorted(zip_entries, key=lambda e: e["path"]):
        raise AuditRejected("receipt_differs_from_verified_zip")
    return entries


def _read_receipt(root_fd: int, expected_sha: str, count: int,
                  source_id: str, zip_entries: list[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    try:
        fd = os.open(RECEIPT, os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK, dir_fd=root_fd)
    except OSError as exc:
        raise AuditRejected("missing_or_unsafe_receipt") from exc
    with os.fdopen(fd, "rb") as handle:
        info = os.fstat(handle.fileno())
        if (not stat.S_ISREG(info.st_mode) or info.st_nlink != 1
                or info.st_mode & (0o177 | stat.S_ISUID | stat.S_ISGID | stat.S_ISVTX)):
            raise AuditRejected("receipt_not_private_regular_file")
        if info.st_size > MAX_RECEIPT_BYTES:
            raise AuditRejected("oversized_receipt")
        data = handle.read(MAX_RECEIPT_BYTES + 1)
    if len(data) > MAX_RECEIPT_BYTES:
        raise AuditRejected("oversized_receipt")
    try:
        decoded = json.loads(data)
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise AuditRejected("invalid_receipt_json") from exc
    return _validate_receipt(decoded, expected_sha, count, source_id, zip_entries)


def _file_digest_in_dir(directory_fd: int, name: str, expected: dict[str, Any], owner_uid: int) -> None:
    flags = os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK
    try:
        fd = os.open(name, flags, dir_fd=directory_fd)
    except OSError as exc:
        raise AuditRejected("unreadable_or_replaced_staged_file") from exc
    with os.fdopen(fd, "rb") as file_handle:
        before = os.fstat(file_handle.fileno())
        if not stat.S_ISREG(before.st_mode) or before.st_uid != owner_uid or before.st_nlink != 1:
            raise AuditRejected("staged_file_type_owner_or_link_mismatch")
        if before.st_mode & (0o177 | stat.S_ISUID | stat.S_ISGID | stat.S_ISVTX):
            raise AuditRejected("staged_file_has_executable_or_shared_mode")
        if before.st_size != expected["bytes"] or before.st_size > MAX_STAGED_BYTES:
            raise AuditRejected("staged_file_size_mismatch")
        digest = hashlib.sha256()
        bytes_seen = 0
        while chunk := file_handle.read(65536):
            bytes_seen += len(chunk)
            if bytes_seen > expected["bytes"] or bytes_seen > MAX_STAGED_BYTES:
                raise AuditRejected("staged_file_expanded_during_verification")
            digest.update(chunk)
        after = os.fstat(file_handle.fileno())
        if (
            after.st_dev != before.st_dev or after.st_ino != before.st_ino
            or after.st_size != before.st_size or after.st_mtime_ns != before.st_mtime_ns
            or after.st_ctime_ns != before.st_ctime_ns
        ):
            raise AuditRejected("staged_file_changed_during_verification")
        if bytes_seen != expected["bytes"] or digest.hexdigest() != expected["sha256"]:
            raise AuditRejected("staged_file_digest_mismatch")


def verify(archive: Path, directory: Path, evidence: Path = DEFAULT_EVIDENCE,
           source_id: str = "SRC-03") -> dict[str, Any]:
    result: dict[str, Any] = {
        "status": "BLOCKED", "source_id": source_id, "files_verified": 0,
        "blockers": [], "read_only": True, "import_approved": False,
        "imported_into_core": False, "executed": False,
    }
    try:
        expected_sha, expected_count = evidence_record(evidence, source_id)
        archive_report = scan_archive(archive, expected_sha, expected_count, source_id)
        if archive_report.blockers:
            result["blockers"].extend(archive_report.blockers)
            return result
        if not directory.is_absolute() or directory.name in ("", ".", ".."):
            raise AuditRejected("staged_directory_must_be_absolute")
        # Do not accept symlinked parent aliases or relative path tricks.
        if directory.resolve(strict=True) != directory:
            raise AuditRejected("staged_directory_must_be_canonical")
    except (OSError, ValueError, json.JSONDecodeError, AuditRejected) as exc:
        result["blockers"].append(str(exc) if isinstance(exc, AuditRejected) else "invalid_zip_or_directory")
        return result

    try:
        root_fd = os.open(directory, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW)
        try:
            root_stat = os.fstat(root_fd)
            if (root_stat.st_uid != os.geteuid()
                    or root_stat.st_mode & (0o077 | stat.S_ISUID | stat.S_ISGID | stat.S_ISVTX)):
                raise AuditRejected("staged_directory_not_private_or_owned")
            expected = _read_receipt(root_fd, expected_sha, expected_count,
                                     source_id, archive_report.entries)
            allowed_directories = set()
            for path in expected:
                parts = path.split("/")
                allowed_directories.update("/".join(parts[:i]) for i in range(1, len(parts)))
            actual_files: set[str] = set()
            actual_directories: set[str] = set()
            seen = 0
            total_bytes = 0
            receipt_seen = False
            for current, dirs, files, dirfd in os.fwalk(".", topdown=True,
                                                         follow_symlinks=False, dir_fd=root_fd):
                for item in dirs + files:
                    relative = (Path(current) / item).as_posix().removeprefix("./")
                    if unsafe_name(relative, item in dirs):
                        raise AuditRejected("unsafe_staged_member_name")
                    seen += 1
                    if seen > MAX_STAGED_ENTRIES:
                        raise AuditRejected("staged_entry_limit_exceeded")
                    try:
                        info = os.stat(item, dir_fd=dirfd, follow_symlinks=False)
                    except OSError as exc:
                        raise AuditRejected("staged_entry_changed") from exc
                    if info.st_uid != root_stat.st_uid:
                        raise AuditRejected("staged_entry_wrong_owner")
                    if stat.S_ISDIR(info.st_mode):
                        if item not in dirs or relative not in allowed_directories:
                            raise AuditRejected("unexpected_staged_directory")
                        if info.st_mode & (0o077 | stat.S_ISUID | stat.S_ISGID | stat.S_ISVTX):
                            raise AuditRejected("staged_directory_shared_mode")
                        actual_directories.add(relative)
                    elif stat.S_ISREG(info.st_mode):
                        if item not in files:
                            raise AuditRejected("staged_file_directory_conflict")
                        if relative == RECEIPT:
                            receipt_seen = True
                            if not stat.S_ISREG(info.st_mode) or info.st_nlink != 1:
                                raise AuditRejected("receipt_replaced_after_read")
                            continue
                        if relative not in expected:
                            raise AuditRejected("unexpected_staged_file")
                        if info.st_nlink != 1:
                            raise AuditRejected("staged_hardlink_detected")
                        _file_digest_in_dir(dirfd, item, expected[relative], root_stat.st_uid)
                        total_bytes += expected[relative]["bytes"]
                        if total_bytes > MAX_STAGED_BYTES:
                            raise AuditRejected("staged_total_bytes_exceeded")
                        actual_files.add(relative)
                        result["files_verified"] += 1
                    else:
                        raise AuditRejected("staged_special_file_or_symlink")
            if not receipt_seen:
                raise AuditRejected("receipt_removed_during_verification")
            if actual_files != set(expected) or actual_directories != allowed_directories:
                raise AuditRejected("staged_inventory_incomplete")
            if result["files_verified"] != expected_count:
                raise AuditRejected("staged_file_count_mismatch")
            if sha256_file(archive) != expected_sha:
                raise AuditRejected("source_archive_changed_during_audit")
            result["status"] = "CONSISTENT_FOR_MANUAL_REVIEW"
            return result
        finally:
            os.close(root_fd)
    except (AuditRejected, OSError, ValueError, RuntimeError) as exc:
        result["blockers"].append(str(exc) if isinstance(exc, AuditRejected) else "staged_integrity_verification_failed")
        return result


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--archive", type=Path, required=True)
    parser.add_argument("--directory", type=Path, required=True)
    options = parser.parse_args(argv)
    report = verify(options.archive, options.directory)
    print(json.dumps(report, ensure_ascii=True, sort_keys=True, indent=2))
    return 0 if report["status"] == "CONSISTENT_FOR_MANUAL_REVIEW" else 2


if __name__ == "__main__":
    raise SystemExit(main())
