#!/usr/bin/env python3
"""Offline, candidate-only App Center manifest policy checks. NEVER authorize execution.

No network access, filesystem write, shell execution, Docker/Podman call, database
access, signature verification or runtime capability check takes place here.
"""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parents[1]
FIXTURES = ROOT / "evidence" / "app-center-fixtures"
BASE_FIELDS = frozenset({
    "schema_version", "contract_status", "execution_allowed", "app_id",
    "variant_id", "app_version", "publisher_id", "recipe_kind", "artifact",
})
ARTIFACT_FIELDS = frozenset({
    "source_url", "sha256", "license_id", "provenance_state",
})
NATIVE_FIELDS = frozenset({
    "site_scope", "runtime", "database_engine", "required_extensions",
    "requires_container_runtime",
})
CONTAINER_FIELDS = frozenset({
    "driver", "images", "cpu_millicores", "memory_mib", "pids_limit",
    "volumes", "network_mode", "privileged", "host_mounts",
    "engine_socket_mount", "ports",
})
IMAGE_FIELDS = frozenset({"repository", "digest"})
PORT_FIELDS = frozenset({"container_port", "protocol", "exposure"})
IDENTIFIER = re.compile(r"[a-z][a-z0-9_-]{2,63}\Z")
PUBLISHER = re.compile(r"[a-z][a-z0-9._-]{2,79}\Z")
EXTENSION = re.compile(r"[a-z][a-z0-9_]{0,63}\Z")
LICENSE_ID = re.compile(r"[A-Za-z0-9][A-Za-z0-9.-]{2,79}\Z")
VERSION = re.compile(r"[A-Za-z0-9][A-Za-z0-9._+~-]{0,63}\Z")
HOST = re.compile(r"(?:[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?\.)+[a-z][a-z0-9-]{1,62}\Z")
REPO = re.compile(r"[a-z0-9]+(?:[a-z0-9._:/-]*[a-z0-9])?\Z")
HEX = re.compile(r"[a-f0-9]{64}\Z")
MAX_DOCUMENT_BYTES = 64 * 1024


class RecipeContractError(ValueError):
    """A candidate was refused; does not represent a runtime API response."""


def reject(code: str, reason: str) -> None:
    raise RecipeContractError(f"{code}: {reason}")


def fields(value: object, wanted: frozenset[str], where: str) -> dict:
    if not isinstance(value, dict):
        reject("REJECT_UNREVIEWED_FIELD", f"{where} must be an object")
    if set(value) != wanted:
        reject("REJECT_UNREVIEWED_FIELD", f"{where} has missing or extra fields")
    return value


def matches(value: object, pattern: re.Pattern, name: str) -> str:
    if not isinstance(value, str) or not pattern.fullmatch(value):
        reject("REJECT_UNREVIEWED_FIELD", f"invalid {name}")
    return value


def positive_int(value: object, name: str) -> int:
    # Explicitly disallow bool: isinstance(True, int) is True.
    if type(value) is not int or not (0 < value < 2**31):
        reject("REJECT_UNREVIEWED_FIELD", f"invalid positive bound for {name}")
    return value


def valid_source(url: object) -> None:
    if not isinstance(url, str) or len(url) > 2048:
        reject("REJECT_UNTRUSTED_ARTIFACT", "invalid artifact origin")
    try:
        parsed = urlsplit(url)
        hostname = parsed.hostname
    except ValueError:
        reject("REJECT_UNTRUSTED_ARTIFACT", "malformed artifact origin")
    if (parsed.scheme != "https" or not hostname or
        not HOST.fullmatch(hostname) or parsed.username is not None or
        parsed.password is not None or parsed.port is not None or
        parsed.query or parsed.fragment or not parsed.path.startswith("/") or
        any(ord(char) < 32 for char in url) or "\\" in url):
        reject("REJECT_UNTRUSTED_ARTIFACT", "not a bounded HTTPS artifact URL")
    # This is only a *syntactic* check. Production must independently guard
    # DNS rebinding, redirects, SSRF, signatures and publisher provenance.


def check_artifact(data: object) -> None:
    artifact = fields(data, ARTIFACT_FIELDS, "artifact")
    valid_source(artifact["source_url"])
    matches(artifact["sha256"], HEX, "SHA-256 syntax")
    matches(artifact["license_id"], LICENSE_ID, "third-party license identifier")
    if artifact["provenance_state"] != "DECLARED_UNVERIFIED":
        reject("REJECT_UNAPPROVED_EXECUTION", "candidate cannot assert publisher verification")


def check_native(data: object) -> None:
    item = fields(data, NATIVE_FIELDS, "native")
    if item["site_scope"] != "OWNED_SITE":
        reject("REJECT_TYPE_MISMATCH", "native scope must be owned site")
    if item["runtime"] != "PHP_FPM":
        reject("BLOCKED_CAPABILITY", "only PHP_FPM is described by candidate fixture v1")
    if item["database_engine"] not in ("NONE", "MYSQL", "MARIADB", "POSTGRESQL"):
        reject("BLOCKED_CAPABILITY", "unknown declared SQL engine")
    if item["requires_container_runtime"] is not False:
        reject("REJECT_TYPE_MISMATCH", "native install cannot require containers")
    extensions = item["required_extensions"]
    if not isinstance(extensions, list) or len(extensions) > 32:
        reject("REJECT_UNREVIEWED_FIELD", "invalid native extension set")
    if len(set(map(str, extensions))) != len(extensions):
        reject("REJECT_UNREVIEWED_FIELD", "duplicate extensions")
    for extension in extensions:
        matches(extension, EXTENSION, "native extension")


def check_container(data: object) -> None:
    item = fields(data, CONTAINER_FIELDS, "container")
    if item["driver"] not in ("DOCKER", "PODMAN"):
        reject("BLOCKED_CAPABILITY", "container driver not qualified by recipe")
    if item["network_mode"] != "ISOLATED":
        reject("REJECT_UNREVIEWED_FIELD", "host networking is not allowed")
    for field in ("privileged", "host_mounts", "engine_socket_mount"):
        if item[field] is not False:
            reject("REJECT_UNREVIEWED_FIELD", f"unreviewed container privilege: {field}")
    for field in ("cpu_millicores", "memory_mib", "pids_limit"):
        positive_int(item[field], field)
    images = item["images"]
    if not isinstance(images, list) or not 1 <= len(images) <= 8:
        reject("REJECT_UNREVIEWED_FIELD", "bounded list of pinned OCI images required")
    repositories = set()
    for image in images:
        i = fields(image, IMAGE_FIELDS, "container image")
        repo = matches(i["repository"], REPO, "image repository")
        if "/" not in repo or repo in repositories:
            reject("REJECT_UNREVIEWED_FIELD", "image repository must be unique and qualified")
        repositories.add(repo)
        digest = i["digest"]
        if (not isinstance(digest, str) or not digest.startswith("sha256:") or
            not HEX.fullmatch(digest[7:])):
            reject("REJECT_UNTRUSTED_ARTIFACT", "unpinned image digest")
    volumes = item["volumes"]
    if not isinstance(volumes, list) or len(volumes) > 32:
        reject("REJECT_UNREVIEWED_FIELD", "invalid volume declarations")
    if len(set(map(str, volumes))) != len(volumes):
        reject("REJECT_UNREVIEWED_FIELD", "duplicate volumes")
    for volume in volumes:
        matches(volume, IDENTIFIER, "logical volume name")
    ports = item["ports"]
    if not isinstance(ports, list) or len(ports) > 32:
        reject("REJECT_UNREVIEWED_FIELD", "invalid container port declarations")
    seen_ports = set()
    for port in ports:
        p = fields(port, PORT_FIELDS, "container port")
        n = p["container_port"]
        if type(n) is not int or not 1 <= n <= 65535:
            reject("REJECT_UNREVIEWED_FIELD", "invalid container port")
        if p["protocol"] not in ("TCP", "UDP") or p["exposure"] != "INTERNAL":
            reject("REJECT_UNREVIEWED_FIELD", "port exposure needs separate review")
        pair = (n, p["protocol"])
        if pair in seen_ports:
            reject("REJECT_UNREVIEWED_FIELD", "duplicate port")
        seen_ports.add(pair)


def validate_recipe(candidate: object) -> str:
    """Return recipe kind after *static metadata refusal checks only*."""
    if not isinstance(candidate, dict):
        reject("REJECT_UNREVIEWED_FIELD", "candidate must be a JSON object")
    kind = candidate.get("recipe_kind")
    if kind not in ("native_script", "container_stack"):
        reject("REJECT_TYPE_MISMATCH", "unrecognized recipe kind")
    expected = BASE_FIELDS | {("native" if kind == "native_script" else "container")}
    fields(candidate, expected, "recipe")
    if type(candidate["schema_version"]) is not int or candidate["schema_version"] != 1:
        reject("REJECT_UNREVIEWED_FIELD", "unknown candidate version")
    if candidate["contract_status"] != "CANDIDATE_ONLY" or candidate["execution_allowed"] is not False:
        reject("REJECT_UNAPPROVED_EXECUTION", "candidate cannot authorize execution")
    for key in ("app_id", "variant_id"):
        matches(candidate[key], IDENTIFIER, key)
    matches(candidate["app_version"], VERSION, "app_version")
    matches(candidate["publisher_id"], PUBLISHER, "publisher_id")
    check_artifact(candidate["artifact"])
    if kind == "native_script":
        check_native(candidate["native"])
    else:
        check_container(candidate["container"])
    return kind


def load_fixture(path: Path) -> object:
    if path.parent.resolve() != FIXTURES.resolve() or path.suffix != ".json":
        reject("REJECT_UNREVIEWED_FIELD", "CLI permits bundled synthetic fixture files only")
    try:
        raw = path.read_bytes()
        if len(raw) > MAX_DOCUMENT_BYTES:
            reject("REJECT_UNREVIEWED_FIELD", "candidate exceeds size limit")
        return json.loads(raw)
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        reject("REJECT_UNREVIEWED_FIELD", f"invalid fixture: {type(exc).__name__}")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--fixture", choices=("native", "container"), required=True)
    args = parser.parse_args()
    name = ("native-cms.v1.json" if args.fixture == "native" else
            "container-worker.v1.json")
    try:
        kind = validate_recipe(load_fixture(FIXTURES / name))
    except RecipeContractError as exc:
        print(f"FAIL: {exc}")
        return 1
    print(f"PASS: candidate {kind} *metadata* only; execution ALWAYS denied, no live compatibility or installer tested.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
