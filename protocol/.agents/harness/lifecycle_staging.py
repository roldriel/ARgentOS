"""Bootstrap staging for the ARgentOS lifecycle (RFC-81 D4 / Plan 154 U3).

The installer runs from a **temporary copy** of the payload (staging) obtained
from the origin *before* the payload exists installed. Two acquisition methods
are supported, both standard-library only:

* ``git-checkout`` — ``git archive <ref> <subdir>`` extracted into a temp
  directory (a fixed ref gives reproducibility); the resolved commit is
  recorded in the manifest.
* ``local-copy`` — copy a local payload directory (offline support and
  network-free distribution).

The staging directory must never be confusable with the project: a staging
path that is the project, lives inside it, or contains it is rejected.
"""

from __future__ import annotations

import shutil
import subprocess
import tarfile
import tempfile
import uuid
from pathlib import Path

#: Files that must exist in a valid payload (bootstrap + semantic identity).
REQUIRED_PAYLOAD_FILES = ("VERSION", "INDEX.md")


class StagingError(ValueError):
    """Staging could not be obtained or is not a valid/isolated payload."""


def _is_within(path: Path, root: Path) -> bool:
    resolved = Path(path).resolve()
    container = Path(root).resolve()
    return resolved == container or container in resolved.parents


def ensure_staging_isolated(staging: str | Path, project_root: str | Path) -> None:
    """Reject any staging location that could be confused with the project."""
    staging_path = Path(staging).resolve()
    project = Path(project_root).resolve()
    if staging_path == project:
        raise StagingError("staging directory is the project root")
    if _is_within(staging_path, project):
        raise StagingError("staging directory lives inside the project root")
    if _is_within(project, staging_path):
        raise StagingError("staging directory contains the project root")


def validate_payload(payload_root: str | Path) -> list[str]:
    """Return the list of problems with a candidate payload (empty ⇒ valid)."""
    root = Path(payload_root)
    problems: list[str] = []
    if not root.is_dir():
        return [f"payload root is not a directory: {root}"]
    for name in REQUIRED_PAYLOAD_FILES:
        candidate = root / name
        if not candidate.is_file():
            problems.append(f"payload missing required file: {name}")
    version = root / "VERSION"
    if version.is_file() and not version.read_text(encoding="utf-8").strip():
        problems.append("payload VERSION is empty")
    return problems


def new_staging_root(parent: str | Path | None = None) -> Path:
    """Create a private staging root (outside the project).

    ``parent`` selects the directory that hosts the staging root; when it is
    omitted the system temporary directory is used. The staging root is always
    a fresh, uniquely named directory.
    """
    if parent is None:
        return Path(tempfile.mkdtemp(prefix="argentos-staging-"))
    base = Path(parent)
    base.mkdir(parents=True, exist_ok=True)
    candidate = base / f"argentos-staging-{uuid.uuid4().hex}"
    candidate.mkdir()
    return candidate


def acquire_local_copy(payload_dir: str | Path, staging_root: str | Path) -> Path:
    """Copy ``payload_dir`` contents into ``<staging_root>/payload``."""
    source = Path(payload_dir)
    if not source.is_dir():
        raise StagingError(f"local payload directory not found: {source}")
    dest = Path(staging_root) / "payload"
    shutil.copytree(source, dest)
    return dest


def acquire_git_archive(
    repo: str | Path,
    ref: str,
    subdir: str,
    staging_root: str | Path,
) -> tuple[Path, str]:
    """Extract ``<repo>:<subdir>`` at ``ref`` into staging; return root + commit.

    Uses ``git archive`` (no checkout, no working-tree mutation) followed by
    standard-library ``tarfile`` extraction, so no network access is required
    when the ref is already present in the local repository.
    """
    repo_path = Path(repo)
    if not (repo_path / ".git").exists() and not (repo_path / "config").exists():
        # Tolerate bare-ish layouts only when git itself can resolve the repo.
        pass
    staging = Path(staging_root)
    archive = (staging / "_payload.tar").resolve()
    repo_arg = str(Path(repo_path).resolve())
    proc = subprocess.run(
        ["git", "-C", repo_arg, "archive", "-o", str(archive), ref, subdir],
        capture_output=True,
        text=True,
    )
    if proc.returncode != 0:
        raise StagingError(
            f"git archive failed for ref {ref!r}: {proc.stderr.strip()}"
        )
    extract = staging / "extract"
    extract.mkdir(parents=True, exist_ok=True)
    with tarfile.open(archive) as tar:
        _safe_extract(tar, extract)
    payload_root = extract.joinpath(*subdir.split("/"))
    commit_proc = subprocess.run(
        ["git", "-C", repo_arg, "rev-parse", ref],
        capture_output=True,
        text=True,
    )
    commit = commit_proc.stdout.strip() if commit_proc.returncode == 0 else ""
    return payload_root, commit


def _safe_extract(tar: tarfile.TarFile, dest: Path) -> None:
    """Extract a tar archive rejecting member paths that escape ``dest``."""
    dest_resolved = dest.resolve()
    for member in tar.getmembers():
        member_path = (dest / member.name).resolve()
        if member_path != dest_resolved and dest_resolved not in member_path.parents:
            raise StagingError(f"archive member escapes staging: {member.name}")
        if member.issym() or member.islnk():
            raise StagingError(f"archive contains a link member: {member.name}")
    tar.extractall(dest)
