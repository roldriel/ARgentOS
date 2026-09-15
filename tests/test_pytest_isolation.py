"""Regression: a test session leaves no temporary inside the repository root.

The property asserted here is repository hygiene, not test behaviour: the
working tree before ``pytest`` equals the working tree after it, except for
changes a test is explicitly designed to produce through its own isolation
mechanism.

pytest's defaults break that property in three independent ways, and this
suite exercises each one against the *real* configuration of the running
session (no mocks):

1. the cacheprovider materializes ``.pytest_cache`` through a transient
   ``pytest-cache-files-*`` sibling created in the **parent** of the cache
   directory, which defaults to the repository root;
2. ``tmp_path``/``tmpdir`` derive their basetemp from ``tempfile.gettempdir()``;
3. the Orchestrator and Agent Worker suites build throw-away git repositories,
   which used to be nested inside the repository working tree.

``tests/pytest_isolation.py`` defines the single repository-external root for
all three; the root ``conftest.py`` pins the session to it.
"""

from __future__ import annotations

import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT))
sys.path.insert(0, str(REPO_ROOT / "tests"))

import pytest_isolation  # noqa: E402
from runtime.orchestrator.worker import changed_paths, repository_snapshot  # noqa: E402

#: pytest-owned temporary names, searched for in the whole working tree.
PYTEST_TEMPORARY_PREFIXES = (
    ".pytest_basetemp",
    ".pytest-basetemp",
    "pytest-",
    "pytest-cache-files-",
    "pytest-of-",
)

#: Other well-known temporary names, searched for at the repository root only
#: (``tmp`` also matches legitimate ``.project/`` state, so the whole tree is
#: not a valid scope for it).
ROOT_TEMPORARY_PREFIXES = ("dsh-", "tmp")

#: Scratch locations the test suites used to create inside the repository.
LEGACY_IN_REPO_SCRATCH = (
    Path(".project") / "agent-worker-probe",
    Path(".project") / "agent-worker-test",
    Path(".project") / "orchestrator-test",
)


def _temporaries_in_working_tree() -> list[str]:
    found: list[str] = []
    for dirpath, dirnames, filenames in os.walk(REPO_ROOT):
        dirnames[:] = [name for name in dirnames if name != ".git"]
        for name in (*dirnames, *filenames):
            if name == ".pytest_cache" or name.startswith(PYTEST_TEMPORARY_PREFIXES):
                found.append(str(Path(dirpath, name).relative_to(REPO_ROOT)))
    return sorted(found)


def _temporaries_at_repository_root() -> list[str]:
    return sorted(
        entry.name
        for entry in REPO_ROOT.iterdir()
        if entry.name == ".pytest_cache"
        or entry.name.startswith((*PYTEST_TEMPORARY_PREFIXES, *ROOT_TEMPORARY_PREFIXES))
    )


# --------------------------------------------------------------------------- #
# 1. The repository owns no pytest temporary
# --------------------------------------------------------------------------- #


def test_working_tree_holds_no_pytest_temporaries() -> None:
    """No pytest temp/cache artefact exists anywhere in the working tree.

    This is the direct regression for the reported symptom: empty
    ``pytest-cache-files-*`` directories left in the repository root.
    """
    assert _temporaries_in_working_tree() == []


def test_repository_root_holds_no_known_temporaries() -> None:
    assert _temporaries_at_repository_root() == []


def test_test_suites_build_no_repository_inside_the_repository() -> None:
    """Scratch repositories of the suites live outside the working tree."""
    present = [
        str(rel) for rel in LEGACY_IN_REPO_SCRATCH if (REPO_ROOT / rel).exists()
    ]
    assert present == []


# --------------------------------------------------------------------------- #
# 2. ``tmp_path`` is external to the repository, in one isolated location
# --------------------------------------------------------------------------- #


def test_tmp_path_is_outside_the_repository(tmp_path: Path) -> None:
    assert not pytest_isolation.is_within(tmp_path, REPO_ROOT)


def test_tmp_path_basetemp_is_outside_the_repository(
    pytestconfig: pytest.Config, tmp_path_factory: pytest.TempPathFactory
) -> None:
    basetemp = tmp_path_factory.getbasetemp()
    assert not pytest_isolation.is_within(basetemp, REPO_ROOT), (
        f"the tmp_path basetemp {basetemp} is inside the repository working tree"
    )
    if not pytestconfig.getoption("basetemp"):
        assert pytest_isolation.is_within(basetemp, pytest_isolation.tmp_root())


def test_session_temp_directory_is_the_isolated_root() -> None:
    """Every stdlib temporary of the session lands in the isolated root."""
    assert Path(tempfile.gettempdir()) == pytest_isolation.tmp_root()


# --------------------------------------------------------------------------- #
# 3. The pytest cache is materialized outside the repository
# --------------------------------------------------------------------------- #


def test_pytest_cache_is_outside_the_repository(pytestconfig: pytest.Config) -> None:
    """The cache cacheprovider API returns paths outside the working tree.

    ``Cache.mkdir`` is what forces the cache directory to be materialized, so
    this also covers the transient ``pytest-cache-files-*`` sibling the
    cacheprovider creates in the cache directory's parent.
    """
    cache = getattr(pytestconfig, "cache", None)
    if cache is None:  # pragma: no cover - only under -p no:cacheprovider
        pytest.skip("cacheprovider disabled for this session")
    probe = cache.mkdir("argentos-isolation-probe")
    assert pytest_isolation.is_within(probe, pytest_isolation.cache_root())
    assert not pytest_isolation.is_within(probe, REPO_ROOT)


# --------------------------------------------------------------------------- #
# 4. Cleanup works when the environment permits it
# --------------------------------------------------------------------------- #


def test_isolated_temporary_area_is_writable_and_removable() -> None:
    probe = pytest_isolation.pytest_temp_root() / "removability-probe"
    (probe / "nested").mkdir(parents=True, exist_ok=True)
    (probe / "nested" / "payload.txt").write_text("temporary\n", encoding="utf-8")
    shutil.rmtree(probe)
    assert not probe.exists()


# --------------------------------------------------------------------------- #
# 5. Temporaries are never mistaken for repository changes
# --------------------------------------------------------------------------- #


def test_temporaries_are_invisible_to_the_orchestrator_snapshot() -> None:
    """The Orchestrator's repository view cannot see the isolated temp area.

    ``repository_snapshot``/``changed_paths`` are what the host uses for scope
    verification, derivation and recovery: a temporary that showed up there
    would be treated as a legitimate change of the project under orchestration.
    """
    before = repository_snapshot(REPO_ROOT)

    (pytest_isolation.scratch_root("snapshot-probe") / "throw-away.txt").write_text(
        "throw-away\n", encoding="utf-8"
    )
    (pytest_isolation.cache_root() / "pytest-cache-files-probe").mkdir(
        parents=True, exist_ok=True
    )
    (pytest_isolation.tmp_root() / "pytest-probe").mkdir(parents=True, exist_ok=True)

    after = repository_snapshot(REPO_ROOT)

    assert changed_paths(before, after) == []
    assert [rel for rel in after if "pytest-" in rel or rel.startswith(".pytest")] == []


def test_isolated_scratch_root_supports_throw_away_repositories() -> None:
    """The suites' scratch root works as a real repository root, out of the repo."""
    root = pytest_isolation.scratch_root("probe-repository")
    subprocess.run(
        ["git", "init", "-q", "."], cwd=root, check=True, capture_output=True
    )
    (root / "tracked.txt").write_text("content\n", encoding="utf-8")

    assert not pytest_isolation.is_within(root, REPO_ROOT)
    assert "tracked.txt" in repository_snapshot(root)
