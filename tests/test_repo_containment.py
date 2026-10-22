"""Repository integrity: no citation target may depend on the working tree.

RFC-69 invariant I2 (contención): a document referenced by a versioned
artifact cannot exist only as an untracked file. This test scans the **real**
repository with ``tools/check_plan_citations.py`` and asserts that every
citation target that exists on disk is tracked by git.

Domain of the claim (made explicit; the previous docstring was broader than
the check). The containment claim applies to the canonical citation corpus
that ``check_plan_citations.py`` defines: ``docs/plans/``, ``docs/rfc/``,
``docs/adr/`` (recursively) plus the canonical documents in ``ROOT_DOCS``.
Working documents under ``docs/working/`` are **not sources** of normative or
documentary references: they are transitory/pre-canonical notes and may
mention local, unversioned inputs without turning them into repository
dependencies (``docs/AGENTS.md:References``). They **are** targets: a Working
document cited as provenance by a canonical document must be versioned, and
that case is enforced. See the boundary tests at the end of this module.

It deliberately distinguishes:

- an untracked document; and
- an untracked document that is also the target of a canonical reference.

Only the second case violates the invariant.
"""

from __future__ import annotations

import subprocess
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]

import check_plan_citations as cpc  # noqa: E402


def tracked_files(root: Path = REPO_ROOT) -> set[Path]:
    """Return the absolute paths of every file tracked by git."""
    res = subprocess.run(
        ["git", "-C", str(root), "ls-files"],
        capture_output=True,
        text=True,
    )
    assert res.returncode == 0, res.stderr
    return {(root / line).resolve() for line in res.stdout.splitlines()}


def citation_targets(sources: list[cpc.Citation], root: Path) -> set[Path]:
    """Return every resolvable citation target emitted by ``sources``."""
    targets: set[Path] = set()
    for citation in sources:
        if citation.path.startswith(".project/"):
            continue  # ephemeral session artifacts are exempt
        target = root / citation.path
        if not target.is_file():
            mapped = cpc.legacy_target(citation.path, root)
            if mapped is None or not mapped.is_file():
                continue  # broken citations are check_plan_citations' job
            target = mapped
        targets.add(target.resolve())
    return targets


def sources(root: Path = REPO_ROOT) -> list[cpc.Citation]:
    """The canonical citation corpus (the declared domain of containment)."""
    return cpc.scan_documents(root)


def untracked_targets(
    sources: list[cpc.Citation], root: Path, tracked: set[Path]
) -> list[str]:
    return sorted(
        p.relative_to(root).as_posix()
        for p in citation_targets(sources, root) - tracked
    )


def test_no_citation_target_depends_on_working_tree() -> None:
    root = REPO_ROOT
    untracked = untracked_targets(sources(root), root, tracked_files(root))
    assert untracked == [], f"untracked citation targets: {untracked}"


def test_canonical_source_with_untracked_target_is_detected(tmp_path: Path) -> None:
    """A canonical document citing an untracked file violates containment."""
    (tmp_path / "docs" / "plans").mkdir(parents=True)
    (tmp_path / "docs" / "plans" / "a.md").write_text(
        "`docs/notes/input.md:Data`\n", encoding="utf-8"
    )
    (tmp_path / "docs" / "notes").mkdir(parents=True)
    (tmp_path / "docs" / "notes" / "input.md").write_text(
        "# Data\n", encoding="utf-8"
    )
    assert untracked_targets(sources(tmp_path), tmp_path, set()) == [
        "docs/notes/input.md"
    ]


def test_working_source_is_outside_the_declared_domain(tmp_path: Path) -> None:
    """Working notes may cite local inputs without becoming repository deps."""
    (tmp_path / "docs" / "working" / "audits").mkdir(parents=True)
    (tmp_path / "docs" / "working" / "audits" / "a.md").write_text(
        "`NOTES.md:Data`\n", encoding="utf-8"
    )
    (tmp_path / "NOTES.md").write_text("# Data\n", encoding="utf-8")
    assert sources(tmp_path) == []
    assert untracked_targets(sources(tmp_path), tmp_path, set()) == []


def test_working_target_cited_by_canonical_doc_is_enforced(tmp_path: Path) -> None:
    """When Working is provenance, the target must still be versioned."""
    (tmp_path / "docs" / "plans").mkdir(parents=True)
    (tmp_path / "docs" / "plans" / "a.md").write_text(
        "`docs/working/audits/evidence.md:Data`\n", encoding="utf-8"
    )
    (tmp_path / "docs" / "working" / "audits").mkdir(parents=True)
    (tmp_path / "docs" / "working" / "audits" / "evidence.md").write_text(
        "# Data\n", encoding="utf-8"
    )
    assert untracked_targets(sources(tmp_path), tmp_path, set()) == [
        "docs/working/audits/evidence.md"
    ]


def test_canonical_domain_matches_the_declared_source_trees() -> None:
    """The scanned source trees are the declared domain, not an accident."""
    assert cpc.SOURCE_TREES == ("docs/plans", "docs/rfc", "docs/adr")
