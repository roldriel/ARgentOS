"""Repository integrity: no citation target may depend on the working tree.

RFC-69 invariant I2 (contención): a document referenced by a versioned
artifact cannot exist only as an untracked file. This test scans the real
repository with ``tools/check_plan_citations.py`` and asserts that every
citation target that exists on disk is tracked by git.

It deliberately distinguishes:

- an untracked document; and
- an untracked document that is also the target of a versioned reference.

Only the second case violates the invariant.
"""

from __future__ import annotations

import subprocess
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]

import check_plan_citations as cpc  # noqa: E402


def tracked_files() -> set[Path]:
    """Return the absolute paths of every file tracked by git."""
    res = subprocess.run(
        ["git", "-C", str(REPO_ROOT), "ls-files"],
        capture_output=True,
        text=True,
    )
    assert res.returncode == 0, res.stderr
    return {REPO_ROOT / line for line in res.stdout.splitlines()}


def citation_targets() -> set[Path]:
    """Return every resolvable citation target found by the citation checker."""
    targets: set[Path] = set()
    for citation in cpc.scan_documents(REPO_ROOT):
        if citation.path.startswith(".project/"):
            continue  # ephemeral session artifacts are exempt
        target = REPO_ROOT / citation.path
        if not target.is_file():
            mapped = cpc.legacy_target(citation.path, REPO_ROOT)
            if mapped is None or not mapped.is_file():
                continue  # broken citations are check_plan_citations' job
            target = mapped
        targets.add(target.resolve())
    return targets


def test_no_citation_target_depends_on_working_tree() -> None:
    tracked = {p.resolve() for p in tracked_files()}
    untracked = sorted(
        str(p.relative_to(REPO_ROOT))
        for p in citation_targets() - tracked
    )
    assert untracked == [], f"untracked citation targets: {untracked}"
