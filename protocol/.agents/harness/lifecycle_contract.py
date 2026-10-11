"""ARgentOS lifecycle contract: manifest schema, path safety and ownership model.

This module materializes the U1/U2 contract of Plan 154 (RFC-81): the
``install.json`` schema, its path-safety rules, the deterministic ownership
model (provenance + verified state, never the fingerprint alone) and the
atomic-write/snapshot primitives the lifecycle operations rely on.

It is distributed payload data (``.agents/harness/`` family, D1) and standard
library only. The root contract lives in ``roots.py``; this module never
discovers ``PROJECT_ROOT`` — every helper receives it explicitly.

Ownership model (RFC-81, six states). A hash detects divergence; it does not
prove authorship. Ownership is decided by the recorded provenance
(``origin``) plus the verified current state:

``managed-unchanged``  origin ``installed`` and the fingerprint matches
``managed-modified``   origin ``installed`` and the fingerprint differs
``preexisting``        not managed by ARgentOS (present before adoption)
``missing``            listed in the manifest and absent on disk
``unverified-provenance``  not listed, or listed with an unusable manifest
``restored``           a backup entry re-applied to the destination
"""

from __future__ import annotations

import hashlib
import json
import os
import re
from datetime import datetime, timezone
from pathlib import Path, PurePosixPath

#: Manifest schema supported by this build. A newer/unknown schema is a STOP.
MANIFEST_SCHEMA_VERSION = "1.0.0"
SUPPORTED_MANIFEST_SCHEMAS = ("1.0.0",)

#: Journal schema version (recovery contract).
JOURNAL_SCHEMA_VERSION = "1.0.0"

#: Canonical project-relative locations (POSIX, relative to PROJECT_ROOT).
MANIFEST_REL = ".argentos/.project/install.json"
JOURNAL_REL = ".argentos/.project/.lifecycle.journal.json"
LOCK_REL = ".argentos/.project/.lifecycle.lock"
ADAPTER_REL = "AGENTS.md"
ACTIVE_CONFIG_REL = ".argentos/features.toml"
BACKUP_DIR_REL = ".argentos/.backup"
PROJECT_STATE_DIR_REL = ".argentos/.project"
PAYLOAD_ROOT_REL = ".argentos/.agents"

#: Closed vocabularies for manifest entries.
ORIGINS = ("installed", "preexisting", "substituted-authorized")
STATES = ("present", "diverged", "missing")

#: The six ownership states of RFC-81.
OWNERSHIP_MANAGED_UNCHANGED = "managed-unchanged"
OWNERSHIP_MANAGED_MODIFIED = "managed-modified"
OWNERSHIP_PREEXISTING = "preexisting"
OWNERSHIP_MISSING = "missing"
OWNERSHIP_UNVERIFIED = "unverified-provenance"
OWNERSHIP_RESTORED = "restored"
OWNERSHIP_STATES = (
    OWNERSHIP_MANAGED_UNCHANGED,
    OWNERSHIP_MANAGED_MODIFIED,
    OWNERSHIP_PREEXISTING,
    OWNERSHIP_MISSING,
    OWNERSHIP_UNVERIFIED,
    OWNERSHIP_RESTORED,
)

_DRIVE_ABSOLUTE_RE = re.compile(r"^[A-Za-z]:")
_HEX_RE = re.compile(r"^[0-9a-f]{64}$")


class ManifestError(ValueError):
    """The manifest is absent in an inadmissible way, corrupt or incompatible."""


class PathSafetyError(ManifestError):
    """A manifest or target path escapes ``PROJECT_ROOT`` (fail closed)."""


def sha256_bytes(data: bytes) -> str:
    """Hex SHA-256 of ``data``."""
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: str | os.PathLike[str]) -> str:
    """Hex SHA-256 of the file at ``path``."""
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def utc_now() -> str:
    """Canonical UTC timestamp (ISO-8601 with ``Z``)."""
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def backup_stamp() -> str:
    """A filesystem-safe UTC stamp used to name a backup batch directory."""
    return datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S%fZ")


def ensure_within_project(project_root: str | os.PathLike[str], target: str | os.PathLike[str]) -> None:
    """Reject ``target`` when its resolved location escapes ``PROJECT_ROOT``.

    Symlinks are resolved (``os.path.realpath``), so a destination reached
    through a symlink that leaves the project is rejected even if its lexical
    form looks internal.
    """
    root_real = Path(os.path.realpath(str(project_root)))
    target_real = Path(os.path.realpath(str(target)))
    if target_real != root_real and root_real not in target_real.parents:
        raise PathSafetyError(
            f"path escapes PROJECT_ROOT after symlink resolution: {target!r}"
        )


def is_safe_relpath(rel: object) -> bool:
    """True when ``rel`` is a normalized, relative, POSIX, ``..``-free path."""
    if not isinstance(rel, str) or not rel.strip():
        return False
    norm = rel.replace("\\", "/")
    if norm.startswith("/") or _DRIVE_ABSOLUTE_RE.match(norm):
        return False
    posix = PurePosixPath(norm)
    if posix.is_absolute():
        return False
    parts = posix.parts
    if not parts or ".." in parts:
        return False
    if any(part == "" for part in parts):
        return False
    return norm == posix.as_posix()


def resolve_manifest_path(
    project_root: str | os.PathLike[str], rel: str
) -> Path:
    """Resolve a manifest path (relative to ``PROJECT_ROOT``) or raise.

    The manifest stores POSIX paths relative to ``PROJECT_ROOT``; absolute
    paths, drive-relative paths, ``..`` components and destinations that
    escape the project (including via symlinks) are rejected.
    """
    if not is_safe_relpath(rel):
        raise PathSafetyError(f"unsafe manifest path: {rel!r}")
    target = Path(project_root).joinpath(*PurePosixPath(rel).parts)
    ensure_within_project(project_root, target)
    return target


def manifest_path(project_root: str | os.PathLike[str]) -> Path:
    """``<project-root>/.argentos/.project/install.json``."""
    return Path(project_root).joinpath(*PurePosixPath(MANIFEST_REL).parts)


def journal_path(project_root: str | os.PathLike[str]) -> Path:
    return Path(project_root).joinpath(*PurePosixPath(JOURNAL_REL).parts)


def lock_path(project_root: str | os.PathLike[str]) -> Path:
    return Path(project_root).joinpath(*PurePosixPath(LOCK_REL).parts)


def active_config_path(project_root: str | os.PathLike[str]) -> Path:
    return Path(project_root).joinpath(*PurePosixPath(ACTIVE_CONFIG_REL).parts)


def backup_root(project_root: str | os.PathLike[str]) -> Path:
    return Path(project_root).joinpath(*PurePosixPath(BACKUP_DIR_REL).parts)


def _entry_problems(entry: object, kind: str, project_root) -> list[str]:
    problems: list[str] = []
    if not isinstance(entry, dict):
        return [f"{kind}: entry is not an object"]
    rel = entry.get("path")
    try:
        resolve_manifest_path(project_root, rel)  # type: ignore[arg-type]
    except ManifestError as exc:
        problems.append(f"{kind}[{rel!r}]: {exc}")
    if kind == "files":
        origin = entry.get("origin")
        if origin not in ORIGINS:
            problems.append(f"files[{rel!r}]: bad origin {origin!r}")
        state = entry.get("state")
        if state not in STATES:
            problems.append(f"files[{rel!r}]: bad state {state!r}")
    if kind == "generated":
        if entry.get("origin") not in ORIGINS:
            problems.append(f"generated[{rel!r}]: bad origin {entry.get('origin')!r}")
        if entry.get("kind") != "adapter":
            problems.append(f"generated[{rel!r}]: bad kind {entry.get('kind')!r}")
    digest = entry.get("sha256")
    if digest is not None and not (isinstance(digest, str) and _HEX_RE.match(digest)):
        problems.append(f"{kind}[{rel!r}]: bad sha256 {digest!r}")
    return problems


def validate_manifest(data: object, project_root: str | os.PathLike[str]) -> list[str]:
    """Return the list of manifest problems (empty ⇒ valid).

    An unsupported ``manifest_schema_version`` is reported as a problem so the
    caller can STOP (never interpret an unknown schema "by eye").
    """
    if not isinstance(data, dict):
        return ["manifest is not a JSON object"]
    problems: list[str] = []
    schema = data.get("manifest_schema_version")
    if schema not in SUPPORTED_MANIFEST_SCHEMAS:
        problems.append(f"unsupported manifest_schema_version: {schema!r}")
    install = data.get("install")
    if not isinstance(install, dict):
        problems.append("missing install object")
        install = {}
    declared_manifest = install.get("manifest_path")
    if declared_manifest != MANIFEST_REL:
        problems.append(f"install.manifest_path must be {MANIFEST_REL!r}")
    if install.get("method") not in ("local-copy", "git-checkout"):
        problems.append(f"install.method invalid: {install.get('method')!r}")
    if not isinstance(install.get("source"), dict):
        problems.append("install.source must be an object")
    if not isinstance(install.get("installed_at"), str):
        problems.append("install.installed_at must be a string")
    config = data.get("config")
    if not isinstance(config, dict) or config.get("active_path") != ACTIVE_CONFIG_REL:
        problems.append(f"config.active_path must be {ACTIVE_CONFIG_REL!r}")
    for kind in ("files", "generated", "backups"):
        value = data.get(kind)
        if not isinstance(value, list):
            problems.append(f"{kind} must be a list")
            continue
        for entry in value:
            problems.extend(_entry_problems(entry, kind, project_root))
    return problems


def load_manifest(project_root: str | os.PathLike[str]) -> dict | None:
    """Load and validate ``install.json``.

    Returns ``None`` when the manifest is absent. Raises :class:`ManifestError`
    when it is unreadable, corrupt or invalid (fail-closed; the caller STOPs).
    """
    path = manifest_path(project_root)
    if not path.exists():
        return None
    try:
        raw = path.read_text(encoding="utf-8")
    except OSError as exc:
        raise ManifestError(f"manifest unreadable: {exc}") from exc
    try:
        data = json.loads(raw)
    except json.JSONDecodeError as exc:
        raise ManifestError(f"manifest is not valid JSON: {exc}") from exc
    problems = validate_manifest(data, project_root)
    if problems:
        raise ManifestError("; ".join(problems))
    return data


def snapshot_manifest(
    project_root: str | os.PathLike[str], *, stamp: str | None = None
) -> Path | None:
    """Copy the current manifest into ``.backup/<stamp>/install.json``.

    Returns the snapshot path, or ``None`` when there was no manifest to
    snapshot. Never overwrites an existing entry.
    """
    current = manifest_path(project_root)
    if not current.exists():
        return None
    batch = backup_root(project_root) / (stamp or backup_stamp())
    dest = batch / PurePosixPath(MANIFEST_REL).name
    if dest.exists():
        raise ManifestError(f"backup entry already exists: {dest}")
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_bytes(current.read_bytes())
    return dest


def save_manifest_atomic(
    project_root: str | os.PathLike[str],
    data: dict,
    *,
    snapshot: bool = True,
    stamp: str | None = None,
) -> Path:
    """Write ``install.json`` atomically (temp file + rename in the same dir).

    Before replacing an existing manifest, a snapshot is preserved under
    ``.backup/`` so a corrupt manifest always has a recovery path.
    """
    target = manifest_path(project_root)
    target.parent.mkdir(parents=True, exist_ok=True)
    ensure_within_project(project_root, target)
    if snapshot:
        snapshot_manifest(project_root, stamp=stamp)
    tmp = target.with_name(target.name + ".tmp")
    payload = json.dumps(data, indent=2, sort_keys=False, ensure_ascii=False) + "\n"
    with open(tmp, "w", encoding="utf-8", newline="\n") as handle:
        handle.write(payload)
        handle.flush()
        os.fsync(handle.fileno())
    os.replace(tmp, target)
    return target


def atomic_write(path: str | os.PathLike[str], data: bytes) -> None:
    """Write ``data`` to ``path`` atomically where the filesystem allows it."""
    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    tmp = target.with_name(target.name + ".tmp")
    with open(tmp, "wb") as handle:
        handle.write(data)
        handle.flush()
        os.fsync(handle.fileno())
    os.replace(tmp, target)


def _sha_or_none(path: Path) -> str | None:
    try:
        return sha256_file(path)
    except OSError:
        return None


def classify_entry(entry: dict, project_root: str | os.PathLike[str]) -> str:
    """Classify a manifest entry into one of the six ownership states."""
    target = resolve_manifest_path(project_root, entry["path"])
    if not target.exists():
        return OWNERSHIP_MISSING
    origin = entry.get("origin")
    if origin == "installed":
        digest = entry.get("sha256")
        if isinstance(digest, str) and _sha_or_none(target) == digest:
            return OWNERSHIP_MANAGED_UNCHANGED
        return OWNERSHIP_MANAGED_MODIFIED
    return OWNERSHIP_PREEXISTING


def classify_path(
    manifest: dict | None, rel: str, project_root: str | os.PathLike[str]
) -> str:
    """Classify an arbitrary path against the manifest (six-state model).

    A path absent from the manifest — or any path when the manifest is
    unusable — is ``unverified-provenance``: readable, reported, never
    destructively touched.
    """
    if not manifest:
        return OWNERSHIP_UNVERIFIED
    for entry in manifest.get("files", []):
        if entry.get("path") == rel:
            return classify_entry(entry, project_root)
    return OWNERSHIP_UNVERIFIED


def file_entry(rel: str, origin: str, project_root: str | os.PathLike[str]) -> dict:
    """Build a ``files[]`` entry for ``rel`` from its current on-disk content."""
    target = resolve_manifest_path(project_root, rel)
    if not target.exists():
        return {"path": rel, "origin": origin, "state": "missing", "sha256": None}
    return {
        "path": rel,
        "origin": origin,
        "state": "present",
        "sha256": sha256_file(target),
    }
