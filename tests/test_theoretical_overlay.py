"""Declared-overlay semantics of Theoretical Execution (plan 175, S1).

The tests build throw-away Git repositories outside the working tree and read
them through the same read-only Git boundary the product uses.
"""

from __future__ import annotations

import subprocess
import sys
import uuid
from dataclasses import FrozenInstanceError
from pathlib import Path

import pytest

import pytest_isolation

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from runtime.theoretical.overlay import (  # noqa: E402
    ABSENT,
    DECLARED_UNKNOWN,
    PRESENT,
    BaseState,
    DeclaredOverlay,
    GitRepository,
    normalize_path,
)

SCRATCH = pytest_isolation.scratch_root("theoretical")

MINIMAL_PLAN = """# Plan 175 — minimal TE fixture

**Status:** Aprobado para ejecución
**Fecha:** 2026-10-24
**RFC:** —
**RFC-56 Class:** N/A
**Change Level:** L2

## Objetivo

A minimal committed proposal.

## Derivación y premisas

| Clase | Contenido | Dueño | Fuente |
|---|---|---|---|
| `P-1` | intención | humano | este Plan |

## Entregables

1. `runtime/foo.py`

## Pasos

1. Escribir foo.py.

## Delegación agentiva

- **Task:** escribir foo.py.
- **Scope:** `runtime/foo.py`

## Efectos declarados

| Efecto | Qué produce | Autorización | Estado |
|---|---|---|---|
| — | ninguno | — | authorized |

## Criterios de salida

- [ ] foo.py existe.

## Verificación

```bash
python -c "print(1)"
```
"""


def git(repo: Path, *args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["git", "-C", str(repo), *args],
        check=True,
        capture_output=True,
        text=True,
        encoding="utf-8",
    )


def build_repo(
    name: str = "repo",
    *,
    plan: str = MINIMAL_PLAN,
    extra_files: dict[str, str] | None = None,
) -> Path:
    """Create a committed throw-away repository with a plan at docs/plans/175-*.md."""
    repo = SCRATCH / f"{name}-{uuid.uuid4().hex[:8]}"
    repo.mkdir(parents=True, exist_ok=True)
    git(repo, "init", "-q")
    git(repo, "config", "user.email", "te@example.invalid")
    git(repo, "config", "user.name", "TE Tests")
    for rel, content in (extra_files or {}).items():
        target = repo / rel
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(content, encoding="utf-8")
    plan_path = repo / "docs" / "plans" / "175-minimal.md"
    plan_path.parent.mkdir(parents=True, exist_ok=True)
    plan_path.write_text(plan, encoding="utf-8")
    git(repo, "add", ".")
    git(repo, "commit", "-q", "-m", "fixture")
    return repo


def overlay_for(
    repo: Path,
    declared: list[str],
    effects: list[str] | None = None,
) -> DeclaredOverlay:
    repository = GitRepository(repo)
    base = repository.base_state("HEAD")
    return DeclaredOverlay.build(repository, base, declared, effects or [])


def test_declared_path_is_unknown_even_when_it_exists_in_base() -> None:
    repo = build_repo(extra_files={"docs/base.md": "base\n"})
    overlay = overlay_for(repo, ["docs/base.md"])
    assert overlay.touched("docs/base.md")
    assert overlay.existence("docs/base.md") == DECLARED_UNKNOWN
    assert overlay.content("docs/base.md") is None
    assert overlay.paths() == ("docs/base.md",)


def test_untouched_path_comes_from_the_base_commit() -> None:
    repo = build_repo(extra_files={"docs/base.md": "base\n"})
    overlay = overlay_for(repo, ["runtime/foo.py"])
    assert overlay.existence("docs/base.md") == PRESENT
    assert overlay.content("docs/base.md") == b"base\n"
    assert overlay.existence("docs/missing.md") == ABSENT
    assert overlay.content("docs/missing.md") is None


def test_working_tree_is_never_the_projected_state() -> None:
    repo = build_repo(extra_files={"docs/base.md": "base\n"})
    (repo / "docs/base.md").write_text("dirty working tree\n", encoding="utf-8")
    overlay = overlay_for(repo, ["runtime/foo.py"])
    assert overlay.content("docs/base.md") == b"base\n"


def test_overlay_identity_is_structural_and_stable() -> None:
    repo = build_repo(extra_files={"docs/base.md": "base\n"})
    first = overlay_for(repo, ["runtime/foo.py"], ["network"])
    second = overlay_for(repo, ["runtime/foo.py"], ["network"])
    assert first.identity() == second.identity()
    assert first.identity()["content"] == "unknown"
    assert first.identity()["kind"] == "declared_overlay"


def test_overlay_is_immutable() -> None:
    repo = build_repo()
    overlay = overlay_for(repo, ["runtime/foo.py"])
    with pytest.raises(FrozenInstanceError):
        overlay.declared_paths = frozenset()  # type: ignore[misc]


def test_path_normalization_rejects_escapes() -> None:
    assert normalize_path("./runtime/foo.py") == "runtime/foo.py"
    with pytest.raises(ValueError):
        normalize_path("../outside")
    with pytest.raises(ValueError):
        normalize_path("-option")
