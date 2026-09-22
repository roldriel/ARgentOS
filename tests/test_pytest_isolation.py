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

Section 6 adds the plan-145 (I-1) regressions: the throw-away repositories are
owned by **one** session, so a second session cannot destroy the live scratch
of the first — which is what made the suite non-deterministic under concurrent
runs.
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


def _now() -> float:
    """The current wall clock, read once so a threshold is asserted stably."""
    import time

    return time.time()


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


# --------------------------------------------------------------------------- #
# 6. Scratch is owned by one session: a second session cannot destroy it
#    (plan 145, I-1)
# --------------------------------------------------------------------------- #


def test_scratch_root_is_scoped_to_the_declared_session() -> None:
    """The scratch root carries the session token, so it is not a shared path."""
    token = pytest_isolation.session_id()
    own = pytest_isolation.scratch_root()
    assert own == pytest_isolation.sessions_root() / token
    assert own.name == token
    assert pytest_isolation.session_scratch_root(own.name) == own


def test_two_sessions_do_not_share_a_scratch_root() -> None:
    """Two tokens resolve to two disjoint directories under the same parent."""
    first = pytest_isolation.session_scratch_root("session-one")
    second = pytest_isolation.session_scratch_root("session-two")

    assert first != second
    assert pytest_isolation.sessions_root() in first.parents
    assert pytest_isolation.sessions_root() in second.parents
    assert not pytest_isolation.is_within(first, second)
    assert not pytest_isolation.is_within(second, first)


def _declare_session(token: str, *, age_seconds: float | None = None) -> Path:
    """Create a sibling session scratch directory, optionally backdated.

    Mirrors what a real session start does (a directory plus its ownership
    marker); ``age_seconds`` moves the marker into the past so the age-based
    sweep can be exercised deterministically, without sleeping.
    """
    root = pytest_isolation.session_scratch_root(token)
    root.mkdir(parents=True, exist_ok=True)
    marker = root / pytest_isolation.SESSION_MARKER
    marker.write_text(f"{token}\n", encoding="utf-8")
    if age_seconds is not None:
        when = _now() - age_seconds
        os.utime(marker, (when, when))
    return root


def test_a_session_directory_is_marked_with_its_own_ownership() -> None:
    """The marker is the ownership declaration the sweep reads."""
    own = pytest_isolation.clear_own_scratch()
    marker = own / pytest_isolation.SESSION_MARKER
    assert marker.is_file()
    assert marker.read_text(encoding="utf-8").strip() == own.name


def test_starting_a_second_session_leaves_the_first_session_scratch_alive() -> None:
    """A session's cleanup touches only its own directory.

    This is the direct regression for I-1. Under the previous *shared* root,
    every session start removed the whole scratch parent, so a concurrent
    session lost the throw-away repositories it was still using. The surviving
    file below is exactly what the old implementation destroyed.
    """
    own = pytest_isolation.clear_own_scratch()
    live = own / "in-flight-repository"
    live.mkdir(parents=True, exist_ok=True)
    (live / "plan.md").write_text("in flight\n", encoding="utf-8")

    # A *second* session starting, aged past the threshold so it is a real
    # pruning candidate: it must still not touch the first session's directory.
    second = _declare_session("second-session", age_seconds=10 * 24 * 60 * 60)
    assert not pytest_isolation.is_within(own, second)
    assert not pytest_isolation.is_within(second, own)

    # What the second session does on start: clear only its own, then sweep the
    # abandoned leftovers.
    removed = pytest_isolation.prune_stale_sessions(now=_now())

    assert (live / "plan.md").read_text(encoding="utf-8") == "in flight\n"
    assert own.exists()
    # The aged sibling was collected — the sweep really ran — and the deciding
    # session survived it.
    assert "second-session" in removed
    assert pytest_isolation.session_scratch_root().name not in removed


def test_cleanup_of_an_abandoned_session_does_not_touch_a_live_one() -> None:
    """Age, not presence, decides. A fresh sibling session is never pruned."""
    own = pytest_isolation.session_scratch_root()
    live_sibling = _declare_session("live-sibling")
    marker = live_sibling / "still-working.txt"
    marker.write_text("live\n", encoding="utf-8")

    removed = pytest_isolation.prune_stale_sessions(now=_now())

    assert "live-sibling" not in removed
    assert marker.exists()
    assert live_sibling.exists()
    assert own.exists()


def test_cleanup_removes_an_abandoned_session_and_reports_it() -> None:
    """A session whose marker is older than the threshold is removed."""
    abandoned = _declare_session(
        "abandoned-session", age_seconds=10 * 24 * 60 * 60
    )
    (abandoned / "old-repository").mkdir(parents=True, exist_ok=True)

    removed = pytest_isolation.prune_stale_sessions(now=_now())

    assert "abandoned-session" in removed
    assert not abandoned.exists()
    # The deciding session is never a candidate, however old it looks.
    assert pytest_isolation.session_scratch_root().name not in removed


def test_pruning_leaves_directories_it_does_not_recognise_alone() -> None:
    """No ownership marker, no ownership claim: the sweep does not infer one."""
    foreign = pytest_isolation.sessions_root() / "not-a-session"
    foreign.mkdir(parents=True, exist_ok=True)
    payload = foreign / "someone-elses-data.txt"
    payload.write_text("keep\n", encoding="utf-8")
    ancient = _now() - 30 * 24 * 60 * 60
    os.utime(payload, (ancient, ancient))
    os.utime(foreign, (ancient, ancient))

    removed = pytest_isolation.prune_stale_sessions(now=_now())

    assert "not-a-session" not in removed
    assert payload.exists()
    shutil.rmtree(foreign, ignore_errors=True)


def test_pruning_never_removes_the_current_session_even_when_it_looks_ancient() -> None:
    """The deciding session is excluded by ownership, not by freshness."""
    own = pytest_isolation.clear_own_scratch()
    marker = own / pytest_isolation.SESSION_MARKER
    ancient = _now() - 10 * 24 * 60 * 60
    os.utime(marker, (ancient, ancient))
    os.utime(own, (ancient, ancient))

    removed = pytest_isolation.prune_stale_sessions(now=_now())

    assert removed == []
    assert marker.exists()


def test_an_undeclared_session_is_refused_instead_of_shared(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """No token, no session-owned path: a shared fallback is not provided.

    A silent shared fallback is precisely how one session would end up with
    another's directory, so the absence is reported instead.
    """
    monkeypatch.setattr(pytest_isolation, "_session_id", None)
    monkeypatch.delenv(pytest_isolation.ENV_SESSION_ID, raising=False)

    with pytest.raises(RuntimeError, match="no pytest session token is declared"):
        pytest_isolation.session_id()
    with pytest.raises(RuntimeError, match="no pytest session token is declared"):
        pytest_isolation.session_scratch_root()


def test_a_session_token_cannot_be_redeclared_in_one_process() -> None:
    """One process is one session; a second token is a programming error."""
    declared = pytest_isolation.session_id()
    assert pytest_isolation.set_session_id(declared) == declared
    with pytest.raises(RuntimeError, match="cannot be redeclared"):
        pytest_isolation.set_session_id(f"{declared}-other")


def test_the_session_token_is_exported_to_child_processes() -> None:
    """A child adopts the session it belongs to instead of inventing one."""
    token = pytest_isolation.session_id()
    assert os.environ.get(pytest_isolation.ENV_SESSION_ID) == token

    code = (
        "import sys; sys.path.insert(0, r'%s'); import pytest_isolation as p; "
        "print(p.session_id())" % (REPO_ROOT / "tests")
    )
    child = subprocess.run(
        [sys.executable, "-c", code], capture_output=True, text=True, check=True
    )
    assert child.stdout.strip() == token


def test_pruning_has_a_documented_default_threshold() -> None:
    """The bound is declared, not incidental."""
    assert pytest_isolation.STALE_SESSION_SECONDS == 24 * 60 * 60
