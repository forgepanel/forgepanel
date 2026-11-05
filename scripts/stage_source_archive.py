#!/usr/bin/env python3
"""Stage a verified source ZIP into a new private quarantine, never into Core.

Default is read-only. --stage explicitly copies regular files with modes 0600
under a fresh, privately owned directory. No code is run or installed.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import shutil
import zipfile
from pathlib import Path

from verify_source_archive import (
    DEFAULT_EVIDENCE,
    entry_kind,
    evidence_record,
    scan_archive,
    sha256_file,
    unsafe_name,
)

RECEIPT = ".forgepanel-intake-receipt.json"
CHUNK_SIZE = 64 * 1024


class StageError(Exception):
    """Safe, non-secret reason to reject a staging attempt."""


def _open_owned_parent(destination: Path) -> tuple[int, str]:
    if os.geteuid() == 0:
        raise StageError("root_execution_forbidden")
    if destination.name in ("", ".", ".."):
        raise StageError("invalid_destination")
    parent = destination.parent.resolve(strict=True)
    target = parent / destination.name
    if target.is_relative_to(Path(__file__).resolve().parents[1]):
        raise StageError("staging_inside_source_repo_forbidden")
    try:
        fd = os.open(parent, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW)
    except OSError as exc:
        raise StageError("untrusted_parent_directory") from exc
    meta = os.fstat(fd)
    if meta.st_uid != os.geteuid() or meta.st_mode & 0o022:
        os.close(fd)
        raise StageError("parent_must_be_private_and_owned")
    return fd, destination.name


def _enter_dir(fd: int, name: str) -> int:
    try:
        os.mkdir(name, mode=0o700, dir_fd=fd)
    except FileExistsError:
        pass
    return os.open(name, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW, dir_fd=fd)


def _copy_entry(root_fd: int, zf: zipfile.ZipFile, entry: dict) -> None:
    name = entry["path"]
    info = zf.getinfo(name)
    if unsafe_name(info.filename, info.is_dir()) or entry_kind(info) != "regular":
        raise StageError("source_structure_changed")
    if name == RECEIPT or name.startswith(RECEIPT + "/"):
        raise StageError("reserved_receipt_path")
    pieces = name.split("/")
    cursor = os.dup(root_fd)
    try:
        for part in pieces[:-1]:
            next_fd = _enter_dir(cursor, part)
            os.close(cursor)
            cursor = next_fd
        flags = os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW
        try:
            out_fd = os.open(pieces[-1], flags, 0o600, dir_fd=cursor)
        except OSError as exc:
            raise StageError("unable_to_stage_regular_file") from exc
        digest = hashlib.sha256()
        copied = 0
        with os.fdopen(out_fd, "wb", closefd=True) as out, zf.open(info, "r") as src:
            while data := src.read(CHUNK_SIZE):
                copied += len(data)
                if copied > entry["bytes"]:
                    raise StageError("member_size_changed")
                digest.update(data)
                out.write(data)
            out.flush()
            os.fsync(out.fileno())
        if copied != entry["bytes"] or digest.hexdigest() != entry["sha256"]:
            raise StageError("member_content_changed")
    finally:
        os.close(cursor)


def stage(archive: Path, destination: Path, evidence: Path = DEFAULT_EVIDENCE,
          source_id: str = "SRC-03", commit: bool = False) -> dict:
    """Verify first, then optionally stage exact bytes in a private directory."""
    expected_sha, count = evidence_record(evidence, source_id)
    report = scan_archive(archive, expected_sha, count, source_id)
    output = {
        "status": "BLOCKED" if report.blockers else "VERIFIED_FOR_REVIEW",
        "source_id": source_id,
        "archive_sha256": report.archive_sha256,
        "file_count": report.file_count,
        "blockers": list(report.blockers),
        "warnings": list(report.warnings),
        "staged": False,
        "imported_into_core": False,
        "executed": False,
    }
    if report.blockers or not commit:
        return output
    if any(e["path"] == RECEIPT or e["path"].startswith(RECEIPT + "/") for e in report.entries):
        output["blockers"].append("reserved_receipt_path")
        output["status"] = "BLOCKED"
        return output
    try:
        parent_fd, leaf = _open_owned_parent(destination)
    except StageError as exc:
        output["status"] = "BLOCKED"
        output["blockers"].append(str(exc))
        return output
    created = False
    try:
        try:
            os.mkdir(leaf, 0o700, dir_fd=parent_fd)
            created = True
        except FileExistsError as exc:
            raise StageError("destination_already_exists") from exc
        root_fd = os.open(leaf, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW, dir_fd=parent_fd)
        try:
            with zipfile.ZipFile(archive, "r") as zf:
                for entry in report.entries:
                    _copy_entry(root_fd, zf, entry)
            if sha256_file(archive) != expected_sha:
                raise StageError("source_archive_changed_during_staging")
            receipt = {
                "schema_version": 1,
                "source_id": source_id,
                "archive_sha256": expected_sha,
                "file_count": count,
                "files": sorted(report.entries, key=lambda e: e["path"]),
                "status": "STAGED_FOR_MANUAL_REVIEW",
                "import_approved": False,
                "executed": False,
            }
            flags = os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW
            receipt_fd = os.open(RECEIPT, flags, 0o600, dir_fd=root_fd)
            with os.fdopen(receipt_fd, "w", encoding="utf-8") as handle:
                json.dump(receipt, handle, ensure_ascii=True, sort_keys=True, indent=2)
                handle.write("\n")
                handle.flush()
                os.fsync(handle.fileno())
            os.fsync(root_fd)
        finally:
            os.close(root_fd)
        os.fsync(parent_fd)
        output["staged"] = True
        output["status"] = "STAGED_FOR_MANUAL_REVIEW"
        return output
    except (StageError, OSError, zipfile.BadZipFile, RuntimeError, EOFError, ValueError) as exc:
        # Do not disclose untrusted exception payloads in logs.
        output["status"] = "BLOCKED"
        output["blockers"].append(str(exc) if isinstance(exc, StageError) else "staging_io_failure")
        if created:
            shutil.rmtree(destination)
        return output
    finally:
        os.close(parent_fd)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--archive", required=True, type=Path)
    parser.add_argument("--destination", required=True, type=Path)
    parser.add_argument("--evidence", type=Path, default=DEFAULT_EVIDENCE)
    parser.add_argument("--source-id", default="SRC-03")
    parser.add_argument("--stage", action="store_true", help="Explicitly create private staging directory (default: inspect only)")
    args = parser.parse_args(argv)
    try:
        result = stage(args.archive, args.destination, args.evidence, args.source_id, args.stage)
    except (OSError, ValueError, json.JSONDecodeError):
        result = {"status": "BLOCKED", "blockers": ["invalid_input_or_evidence"], "staged": False}
    print(json.dumps(result, sort_keys=True, ensure_ascii=True, indent=2))
    return 0 if result["status"] in ("VERIFIED_FOR_REVIEW", "STAGED_FOR_MANUAL_REVIEW") else 2


if __name__ == "__main__":
    raise SystemExit(main())
