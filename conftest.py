"""DEV test-session configuration: every pytest temporary stays outside the repo.

Both canonical test legs resolve their ``rootdir`` to this repository's root,
and pytest's defaults then write into the working tree:

- the cache directory defaults to ``<rootdir>/.pytest_cache``, and the
  cacheprovider materializes it through a transient ``pytest-cache-files-*``
  sibling created in that directory's *parent* — the repository root;
- ``tmp_path``/``tmpdir`` base their ``pytest-of-<user>/pytest-<N>`` tree on
  ``tempfile.gettempdir()``, which is inside the repository as soon as
  ``TMPDIR``/``TEMP`` points there;
- the Orchestrator and Agent Worker suites build throw-away git repositories.

This file pins every session temporary to one repository-external directory, so
running the suite is transparent with respect to the repository surface: the
state before ``pytest`` equals the state after it.  Location, override and
rationale live in ``tests/pytest_isolation.py``; nothing here is
machine-specific.

Behaviour of the knobs:

- ``--basetemp`` is honoured, but rejected with a clear usage error when it
  resolves inside the repository working tree.  The in-repository basetemps
  used as ad-hoc workarounds in this repository's history
  (``--basetemp=.pytest-basetemp-<plan>``) are exactly the pollution this file
  exists to prevent.
- ``cache_dir`` is always pinned to the isolated root: the session cache must
  not be materialized inside the working tree, so an external ``cache_dir``
  override (``-o cache_dir=...``) does not move it.  ``-p no:cacheprovider``
  remains a valid way to run without a cache at all.

Scope: DEV test execution only.  Nothing here is product payload; the
regressions that assert the property live in ``tests/test_pytest_isolation.py``.
"""

from __future__ import annotations

import shutil
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent / "tests"))

import pytest  # noqa: E402
import pytest_isolation as isolation  # noqa: E402


@pytest.hookimpl(tryfirst=True)
def pytest_configure(config: pytest.Config) -> None:
    """Relocate every pytest temporary of this session outside the repository."""
    repository = isolation.repo_root()
    given_basetemp = config.option.basetemp
    if given_basetemp and isolation.is_within(Path(given_basetemp), repository):
        raise pytest.UsageError(
            f"--basetemp={given_basetemp} is inside the repository working tree "
            f"({repository}). A pytest session must not write its temporary "
            f"directories into the repository: drop --basetemp to use the "
            f"isolated session temp root ({isolation.tmp_root()}), or point it "
            f"at a directory outside the repository."
        )

    # 1. Session temp directory: `tmp_path` creates `pytest-of-<user>/pytest-N`
    #    under it, and every other stdlib temporary of the session lands here.
    tmp_root = isolation.tmp_root()
    tmp_root.mkdir(parents=True, exist_ok=True)
    tempfile.tempdir = str(tmp_root)

    # 2. pytest cache directory. The cacheprovider reads `cache_dir` when it
    #    builds its Cache during `pytest_configure`; `tryfirst` on this hook
    #    (pluggy contract: tryfirst implementations run before plain ones)
    #    guarantees the value below is already in place.
    cache_dir = isolation.cache_root() / ".pytest_cache"
    cache_dir.parent.mkdir(parents=True, exist_ok=True)
    config.inicfg["cache_dir"] = str(cache_dir)

    # 3. Throw-away repositories owned by the test suites. Cleared at session
    #    start so an interrupted run cannot accumulate scratch repositories.
    scratch = isolation.scratch_root()
    if scratch.exists():
        shutil.rmtree(scratch, ignore_errors=True)
    scratch.mkdir(parents=True, exist_ok=True)


def pytest_report_header(config: pytest.Config) -> str:
    """Make the isolation visible in the session header (diagnostics)."""
    return f"argentos test temporaries: {isolation.pytest_temp_root()}"
