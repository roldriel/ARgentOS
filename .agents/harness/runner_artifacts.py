"""Artifact path resolution for the harness runner."""

from __future__ import annotations

import sys
from pathlib import Path

_HARNESS_DIR = Path(__file__).resolve().parent
if str(_HARNESS_DIR) not in sys.path:
    sys.path.insert(0, str(_HARNESS_DIR))

import re

import runner_paths


def iteration_dirs(session_uuid: str) -> list[Path]:
    """Return sorted list of numeric iteration directories for a session."""
    session_dir = runner_paths.ARTIFACTS_DIR / session_uuid
    if not session_dir.exists():
        return []
    dirs = [
        p for p in session_dir.iterdir() if p.is_dir() and re.fullmatch(r"\d+", p.name)
    ]
    return sorted(dirs, key=lambda p: int(p.name))


def _find_artifact_in_iter(iter_dir: Path, artifact_name: str) -> Path | None:
    """Look for an artifact by its base name inside an iteration folder.

    Accepts files named either `<artifact_name>` or `<prefix>-<artifact_name>`.
    Returns the first match found, or None.
    """
    if not iter_dir.exists():
        return None
    candidates = sorted(p for p in iter_dir.iterdir() if p.is_file())
    # Prefer an exact name match over an `<order>-` prefixed one for determinism.
    for candidate in candidates:
        if candidate.name == artifact_name:
            return candidate
    for candidate in candidates:
        if candidate.name.endswith(f"-{artifact_name}"):
            return candidate
    return None


def artifact_path(
    session_uuid: str, artifact_name: str, iteration: str | None = None
) -> Path:
    """Resolve the path to an artifact inside a numbered iteration folder.

    Artifacts are expected to be named either `<artifact_name>` or
    `<order>-<artifact_name>` (e.g. `01-TASK_ANALYSIS.md`). The order prefix
    reflects the generation/reading order within the iteration and is not
    derived from the iteration folder name.

    If iteration is provided, look in that folder. Otherwise scan iterations in
    descending order and return the latest match. If no match is found, return
    the path where the artifact is expected to be created (latest iteration, or
    iteration 00 if none exist).
    """
    session_dir = runner_paths.ARTIFACTS_DIR / session_uuid

    if iteration is not None:
        iter_dir = session_dir / iteration
        found = _find_artifact_in_iter(iter_dir, artifact_name)
        return found if found else iter_dir / artifact_name

    dirs = iteration_dirs(session_uuid)
    for iter_dir in reversed(dirs):
        found = _find_artifact_in_iter(iter_dir, artifact_name)
        if found:
            return found

    # Default target for creation: latest iteration or 00
    target_iter = dirs[-1].name if dirs else "00"
    return session_dir / target_iter / artifact_name


def report_path(session_uuid: str) -> Path:
    """Return the session-level HARNESS_REPORT.md path."""
    return runner_paths.ARTIFACTS_DIR / session_uuid / "HARNESS_REPORT.md"


# Registry of semantic validators a policy can declare via the
# `semantic_checks` front matter key. Each validator receives
