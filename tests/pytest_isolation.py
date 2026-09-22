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
        scratch/  -- throw-away repositories, one directory per session
            <session-id>/   -- owned by exactly one session

The location derives from the platform temp directory (``TMPDIR``/``TEMP``/
``/tmp``) and is rejected when it resolves inside the repository working tree,
so it works in CI/Linux and on Windows without hardcoding a machine path.
``ARGENTOS_PYTEST_TMP`` overrides it, for a shell, a CI job or a sandbox that
needs to place the session temporaries somewhere else.

Session ownership of scratch (plan 145, I-1)
--------------------------------------------

The throw-away repositories are **owned by one session** and live under a
per-session directory (``scratch/<session-id>/``).  The root ``conftest.py``
declares that token once, before any test module is imported, and clears
**only** it.  Two consequences, both deliberate:

- a second pytest session can never delete the throw-away repositories of a
  session that is still running.  The previous shared root made every session
  wipe every other session's live scratch, which is what made the suite
  non-deterministic under concurrent runs — and what an operating system's own
  temp cleanup could equally do to a running session;
- the cleanup policy survives without becoming a race: a session clears its own
  (empty, freshly created) directory, and :func:`prune_stale_sessions` removes
  leftovers of sessions that are long gone, by **age**, never by presence.

The token is **declared, not guessed**: it is passed in explicitly, or read
from the environment by a child process that was handed it.  It deliberately
does **not** derive from a PID, a timestamp or any other accidental piece of
process state — a token two live sessions could collide on would reintroduce
exactly the defect this module removes.
"""

from __future__ import annotations

import os
import shutil
import tempfile
import time
from pathlib import Path

#: Repository root (``tests/`` lives directly under it).
REPO_ROOT = Path(__file__).resolve().parents[1]

#: Environment variable that overrides the isolated session temp root.
ENV_OVERRIDE = "ARGENTOS_PYTEST_TMP"

#: Environment variable carrying the session token to child processes.
ENV_SESSION_ID = "ARGENTOS_PYTEST_SESSION"

#: Directory name created under the platform temp directory by default.
DEFAULT_ROOT_NAME = "argentos-pytest"

#: Age after which a sibling session's scratch directory counts as abandoned.
#: A session that is still running keeps writing inside its own directory, so
#: age — not presence — is the discriminator.
STALE_SESSION_SECONDS = 24 * 60 * 60

#: File a session writes inside its own scratch directory to declare ownership.
#: Pruning reads **this** file's age rather than walking the tree: a single
#: ``stat`` per sibling keeps cleanup bounded (a scratch tree is a whole git
#: repository per test, so a recursive walk costs seconds), and its name keeps
#: the sweep from touching anything that is not a session directory.
SESSION_MARKER = ".session"

_root: Path | None = None
_session_id: str | None = None


def repo_root() -> Path:
    """The repository working tree that must stay free of pytest temporaries."""
    return REPO_ROOT


def is_within(path: Path | str, root: Path | str) -> bool:
    """True when ``path`` is ``root`` itself or lives inside it."""
    resolved = Path(os.path.abspath(str(path)))
    container = Path(os.path.abspath(str(root)))
    return resolved == container or container in resolved.parents


def set_session_id(token: str) -> str:
    """Declare the token that owns this session's throw-away repositories.

    The root ``conftest.py`` calls this once, before any test module is
    imported, with a value it generated itself.  Re-declaring a *different*
    token in one process is refused: two tokens in one interpreter would mean
    two "sessions" sharing a process, which is precisely the ambiguity this
    module exists to prevent.
    """
    global _session_id
    token = str(token).strip()
    if not token:
        raise ValueError("the pytest session token must not be empty")
    if _session_id is not None and _session_id != token:
        raise RuntimeError(
            f"the pytest session token is already declared as {_session_id!r} "
            f"and cannot be redeclared as {token!r} in the same process"
        )
    _session_id = token
    os.environ[ENV_SESSION_ID] = token
    return token


def session_id() -> str:
    """The declared token of this session.

    Resolution order, and nothing else:

    1. the token declared in this process (:func:`set_session_id`);
    2. the token this process was handed through the environment — the path a
       **child** process (a subprocess a suite launches, or a nested pytest)
       takes to adopt the session it belongs to;
    3. otherwise there is no session, and the caller is told so rather than
       being handed a shared directory that would silently collide with another
       session.
    """
    if _session_id is not None:
        return _session_id
    from_env = os.environ.get(ENV_SESSION_ID, "").strip()
    if from_env:
        return from_env
    raise RuntimeError(
        "no pytest session token is declared: call "
        f"pytest_isolation.set_session_id(...) (or set {ENV_SESSION_ID}) before "
        "asking for a session-owned path. A shared fallback is deliberately not "
        "provided: a shared scratch root is what let concurrent sessions destroy "
        "each other's throw-away repositories (plan 145, I-1)."
    )


def new_session_id() -> str:
    """A fresh, collision-free session token (used by ``conftest.py``)."""
    return f"s{os.getpid():x}-{time.time_ns():x}-{os.urandom(4).hex()}"


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


def sessions_root() -> Path:
    """Parent of every session-owned scratch directory."""
    return pytest_temp_root() / "scratch"


def session_scratch_root(token: str | None = None) -> Path:
    """The scratch root owned by ``token`` (default: this session).

    Creates nothing and removes nothing: it is a pure path question, so it is
    safe to ask about another session's directory — which is what the
    regression suite does to prove that ownership is respected.
    """
    return sessions_root() / (session_id() if token is None else str(token))


def scratch_root(name: str = "") -> Path:
    """A throw-away directory, outside the repository, for test-owned state.

    Used by the suites that build real git repositories (Orchestrator, Agent
    Worker): nesting those repositories inside the repository under test is
    what makes temporaries look like repository changes.

    Scoped to the **declaring session** (plan 145, I-1): the path includes the
    session token, so a directory returned here can never be shared with, or
    removed by, a different pytest session.
    """
    path = session_scratch_root()
    if name:
        path = path / name
    path.mkdir(parents=True, exist_ok=True)
    return path


def clear_own_scratch() -> Path:
    """Remove and recreate **this session's own** scratch directory.

    This is the whole cleanup contract for a running session, and it never
    touches a sibling session's directory: starting a session cannot destroy
    the live throw-away repositories of another one. The session marker written
    here is what :func:`prune_stale_sessions` later reads as this session's
    heartbeat.
    """
    own = session_scratch_root()
    if own.exists():
        shutil.rmtree(own, ignore_errors=True)
    own.mkdir(parents=True, exist_ok=True)
    marker = own / SESSION_MARKER
    marker.write_text(f"{own.name}\n", encoding="utf-8")
    return own


def _session_marker_age(entry: Path, reference: float) -> float | None:
    """Age of ``entry``'s session marker, or ``None`` when it is not a session.

    The presence of the marker is what makes a directory a session directory:
    the sweep never removes anything it does not recognise, so an unrelated
    directory dropped into the scratch parent is left alone rather than deleted
    by inference.
    """
    marker = entry / SESSION_MARKER
    try:
        return reference - marker.stat().st_mtime
    except OSError:
        return None


def prune_stale_sessions(
    *, max_age_seconds: float = STALE_SESSION_SECONDS, now: float | None = None
) -> list[str]:
    """Remove sibling session directories older than ``max_age_seconds``.

    Bounded cleanup without a race. Two rules, both deliberate:

    - a session that is still running keeps writing inside its own directory,
      so its modification time stays recent and it is never pruned. Only
      directories whose newest entry is already older than the threshold —
      sessions that are long gone — are removed;
    - the current session's own directory is never a candidate, however old it
      looks.

    Cost is one ``stat`` per sibling: the sweep reads the session marker
    instead of walking a tree that, for the Orchestrator and Agent Worker
    suites, contains a whole git repository per test.

    Returns the tokens removed, so the decision is observable, not silent.
    """
    root = sessions_root()
    if not root.is_dir():
        return []
    current = _session_id
    reference = time.time() if now is None else now
    removed: list[str] = []
    for entry in sorted(root.iterdir()):
        if not entry.is_dir():
            continue
        if current is not None and entry.name == current:
            continue
        age = _session_marker_age(entry, reference)
        if age is None or age <= max_age_seconds:
            continue
        shutil.rmtree(entry, ignore_errors=True)
        removed.append(entry.name)
    return removed
