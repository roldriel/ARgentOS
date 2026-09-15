"""The single, repository-external temporary root of a test session.

Both canonical test legs (``python -m pytest tests/`` and
``python -m pytest protocol/.agents/harness/tests/``) resolve their ``rootdir``
to this repository's root, so pytest's own defaults write into the working
tree:

- ``cache_dir`` defaults to ``<rootdir>/.pytest_cache``, and the cacheprovider
  materializes that directory through a transient ``pytest-cache-files-*``
  sibling created in *its parent* — that is, in the repository root (pytest
  ``cacheprovider._ensure_cache_dir_and_supporting_files``).  The sibling is
  removed on exit, but an interrupted or permission-denied cleanup leaves an
  empty ``pytest-cache-files-*`` directory behind in the working tree.
- ``tmp_path``/``tmpdir`` base their ``pytest-of-<user>/pytest-<N>`` tree on
  ``tempfile.gettempdir()``, which is outside the repository only for as long
  as ``TMPDIR``/``TEMP`` does not point back into it.
- the Orchestrator and Agent Worker suites build throw-away git repositories;
  a scratch root inside the repository nests repositories in the working tree.

:func:`pytest_temp_root` returns the one directory outside the repository where
every temporary of a session lives::

    <platform temp>/argentos-pytest/
        tmp/      -- tempfile.gettempdir() of the session (the tmp_path tree)
        cache/    -- pytest cache_dir (.pytest_cache and its transient siblings)
        scratch/  -- throw-away repositories owned by the test suites

The location derives from the platform temp directory (``TMPDIR``/``TEMP``/
``/tmp``) and is rejected when it resolves inside the repository working tree,
so it works in CI/Linux and on Windows without hardcoding a machine path.
``ARGENTOS_PYTEST_TMP`` overrides it, for a shell, a CI job or a sandbox that
needs to place the session temporaries somewhere else.
"""

from __future__ import annotations

import os
import tempfile
from pathlib import Path

#: Repository root (``tests/`` lives directly under it).
REPO_ROOT = Path(__file__).resolve().parents[1]

#: Environment variable that overrides the isolated session temp root.
ENV_OVERRIDE = "ARGENTOS_PYTEST_TMP"

#: Directory name created under the platform temp directory by default.
DEFAULT_ROOT_NAME = "argentos-pytest"

_root: Path | None = None


def repo_root() -> Path:
    """The repository working tree that must stay free of pytest temporaries."""
    return REPO_ROOT


def is_within(path: Path | str, root: Path | str) -> bool:
    """True when ``path`` is ``root`` itself or lives inside it."""
    resolved = Path(os.path.abspath(str(path)))
    container = Path(os.path.abspath(str(root)))
    return resolved == container or container in resolved.parents


def _resolve_temp_root() -> Path:
    override = os.environ.get(ENV_OVERRIDE, "").strip()
    if override:
        root = Path(override).expanduser()
    else:
        root = Path(tempfile.gettempdir()) / DEFAULT_ROOT_NAME
    root = Path(os.path.abspath(str(root)))
    if is_within(root, REPO_ROOT):
        raise RuntimeError(
            f"the isolated pytest temporary root {root} is inside the repository "
            f"working tree {REPO_ROOT}: point {ENV_OVERRIDE} at a directory "
            f"outside the repository"
        )
    return root


def pytest_temp_root() -> Path:
    """The one directory outside the repository that holds session temporaries.

    Resolved once per process, before any caller re-points
    ``tempfile.tempdir``, so the location never depends on the order in which
    the session temporaries are created.
    """
    global _root
    if _root is None:
        _root = _resolve_temp_root()
    return _root


def tmp_root() -> Path:
    """Base of the session temp directory used by ``tmp_path``/``tmpdir``."""
    return pytest_temp_root() / "tmp"


def cache_root() -> Path:
    """Parent of the session pytest cache directory.

    ``pytest-cache-files-*`` siblings are created here, never in the repository.
    """
    return pytest_temp_root() / "cache"


def scratch_root(name: str = "") -> Path:
    """A throw-away directory, outside the repository, for test-owned state.

    Used by the suites that build real git repositories (Orchestrator, Agent
    Worker): nesting those repositories inside the repository under test is
    what makes temporaries look like repository changes.
    """
    path = pytest_temp_root() / "scratch"
    if name:
        path = path / name
    path.mkdir(parents=True, exist_ok=True)
    return path
