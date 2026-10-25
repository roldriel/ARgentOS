#!/usr/bin/env python3
"""Generate the Scoped Content Identity v1 of a declared scope (DEV-only).

Implements the v1 Scoped Content Identity algorithm of the Change Lifecycle
regime: `docs/plans/96-change-lifecycle-unit-b-increments-1-3.md` §13 and
`docs/CONVENTIONS.md:Change Lifecycle — Validation anchors y Scoped Content
Identity (regla operacional; VC-1, Incremento 1)`. The identity is the
deterministic content identity recorded by every Validation Anchor (VC-1) and
verified by the Checkpoint / closure record (GC-1; C-2).

Given a scope set S of repository-relative file paths, the tool computes:

- **Delta scoped identity**: for each ``p`` in ``S`` (lexicographic order),
  the blob id ``b(p)`` = ``git ls-files -s`` (content of the index, i.e. the
  staged state after ``git add``) or, when the path has no index entry,
  ``git hash-object --path=<p> <p>`` (working-tree content "as it would be
  staged", for new/untracked files); then the sha256 of the canonical
  serialization ``scoped-v1`` plus the pairs ``path <0x00> blob <0x00>``.
  With ``--content-ref REF`` (equivalently ``compute(..., content_ref=REF)``)
  the blob of every path is read from ``REF`` instead, so the Delta identity
  depends only on that commit and never on the index or the working tree; the
  serialization is **identical** in both modes. This is the base-relative mode
  used by the DEV theoretical evaluation, which must be a function of its
  declared base.
- **State identity**: the tree id of the staged index (``git write-tree``) by
  default, or the tree of a git ref (``git rev-parse <ref>^{tree}``) when
  ``--ref`` is given. The staged tree is the identity of the full repo state
  that a battery-style validation consumes; the ref tree is the committed
  state identity used to verify a closure state after commit (e.g.
  ``C1^{tree}``).

Boundary with the lifecycle checkers (no authority, no duplication): this
tool **generates** the value that C-1
(``tools/check_lifecycle_anchor.py``) format-validates and that C-2
(``tools/check_lifecycle_checkpoint.py``) resolves against git; it neither
replaces nor modifies those checkers, and nothing here is normative (ADR-16).
The tool is DEV-only and read-only: it never writes the working tree or the
index, never creates artifacts or registries, and adds no field, state or
semantic category.

Fail-closed semantics: a path that is not repository-relative, a path with no
index entry that does not exist on disk, a directory in the scope, a
non-git ``--root`` or an unresolvable ``--ref`` produce a deterministic error
on stderr and exit 1, with no partial output on stdout. Reproducibility
precondition (plan 96 §13.2): run after ``git add`` of the plan's intentional
changes so the index represents the state to validate.

Usage:
  python tools/scoped_content_identity.py [--root REPO_ROOT] [--ref REF]
      [--expected-root PROJECT_ROOT] PATH...

Prints a deterministic JSON report on stdout and exits 0. Standard library
only plus local read-only git invocations. No network.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import sys
from pathlib import Path


_SERIALIZATION_PREFIX = b"scoped-v1"


class ToolError(Exception):
    """Deterministic, user-facing tool error (fail-closed)."""


def _run_git(cwd: Path, *args: str) -> str:
    """Run a local git command and return stdout on success."""
    proc = subprocess.run(
        ["git", "-C", str(cwd), *args],
        check=False,
        capture_output=True,
        text=True,
    )
    if proc.returncode != 0:
        raise ToolError(
            f"git {' '.join(args)} failed: {proc.stderr.strip() or 'unknown error'}"
        )
    return proc.stdout


def _repository_toplevel(root: Path) -> Path:
    """Resolve the git toplevel of ``root`` (fail-closed outside a repo)."""
    try:
        out = _run_git(root, "rev-parse", "--show-toplevel")
    except ToolError as exc:
        raise ToolError(f"not a git repository (or any parent): {root}") from exc
    return Path(out.strip()).resolve()


def _repo_relative(toplevel: Path, arg: str) -> str:
    """Normalize a path argument to a repo-relative POSIX path."""
    raw = Path(arg)
    candidate = toplevel / raw if not raw.is_absolute() else raw
    try:
        rel = candidate.resolve().relative_to(toplevel)
    except ValueError as exc:
        raise ToolError(f"path outside repository: {arg}") from exc
    return rel.as_posix()


def _index_blob(toplevel: Path, rel: str) -> str | None:
    """Blob id of the index entry for ``rel``, or None when not tracked."""
    out = _run_git(toplevel, "ls-files", "-s", "--", rel)
    lines = [line for line in out.splitlines() if line.strip()]
    if len(lines) > 1:
        raise ToolError(
            f"path is a directory (scope paths must be files): {rel}"
        )
    if len(lines) == 1:
        fields = lines[0].split("\t", 1)[0].split()
        if len(fields) == 3 and len(fields[1]) == 40:
            return fields[1]
    return None


def _worktree_blob(toplevel: Path, rel: str) -> str:
    """Blob id of the working-tree file as it would be staged."""
    file = toplevel / rel
    if file.is_dir():
        raise ToolError(f"path is a directory (scope paths must be files): {rel}")
    if not file.is_file():
        raise ToolError(f"path not found (untracked and missing): {rel}")
    return _run_git(toplevel, "hash-object", f"--path={rel}", str(file)).strip()


def _try_git(cwd: Path, *args: str) -> tuple[int, str]:
    """Run a local git command without raising; return (exit code, stdout)."""
    proc = subprocess.run(
        ["git", "-C", str(cwd), *args],
        check=False,
        capture_output=True,
        text=True,
    )
    return proc.returncode, proc.stdout.strip()


def _ref_blob(toplevel: Path, ref: str, rel: str) -> str:
    """Blob id of ``rel`` at ``ref`` (fail-closed when absent or not a file)."""
    code, oid = _try_git(toplevel, "rev-parse", "--verify", "--quiet", f"{ref}:{rel}")
    if code != 0 or not oid:
        raise ToolError(f"path not found at {ref}: {rel}")
    code, kind = _try_git(toplevel, "cat-file", "-t", oid)
    if code != 0 or kind != "blob":
        raise ToolError(f"path is a directory (scope paths must be files): {rel}")
    return oid


def _delta_identity(
    toplevel: Path, rels: list[str], content_ref: str | None = None
) -> str:
    """Delta scoped identity: sha256 of ``scoped-v1`` + path NUL blob NUL.

    By default the blob of a path is read from the index (or the working tree
    for an untracked path).  With ``content_ref`` the blobs are read from that
    commit instead, which is the base-relative mode used by a theoretical
    evaluation: the identity then depends only on the declared base, never on
    the index or the working tree.
    """
    payload = bytearray(_SERIALIZATION_PREFIX)
    for rel in rels:
        if content_ref is None:
            if (toplevel / rel).is_dir():
                raise ToolError(
                    f"path is a directory (scope paths must be files): {rel}"
                )
            blob = _index_blob(toplevel, rel)
            if blob is None:
                blob = _worktree_blob(toplevel, rel)
        else:
            blob = _ref_blob(toplevel, content_ref, rel)
        payload += rel.encode("utf-8") + b"\x00" + blob.encode("ascii") + b"\x00"
    return hashlib.sha256(bytes(payload)).hexdigest()


def _state_identity(toplevel: Path, ref: str | None) -> dict:
    """State identity: staged tree id (default) or ``<ref>^{tree}``."""
    if ref is None:
        return {"source": "staged", "ref": None, "tree": _run_git(toplevel, "write-tree").strip()}
    try:
        tree = _run_git(toplevel, "rev-parse", "--verify", f"{ref}^{{tree}}").strip()
    except ToolError as exc:
        raise ToolError(f"unresolved ref: {ref}") from exc
    return {"source": "ref", "ref": ref, "tree": tree}


def compute(
    root: Path,
    paths: list[str],
    ref: str | None = None,
    *,
    content_ref: str | None = None,
    expected_toplevel: Path | str | None = None,
) -> dict:
    """Compute the v1 Scoped Content Identity of a declared scope.

    Returns a deterministic report with the sorted scope, the Delta scoped
    identity and the State identity. Raises ToolError (fail-closed) on any
    invalid input; never writes the working tree or the index.

    ``content_ref`` reads the per-path blobs from that commit instead of the
    index/working tree. It is the base-relative mode: the Delta scoped identity
    then depends only on the commit, so a theoretical evaluation is a function
    of its declared base and never of the staged or working state. The
    serialization is the same ``scoped-v1`` in both modes; nothing about the
    default (index) mode changes.

    ``expected_toplevel`` declares the repository root the scope belongs to.
    When it is given, the git toplevel resolved from ``root`` must equal it;
    otherwise the computation fails closed. This is the guard that keeps a
    call rooted at the payload from silently identifying the payload's own
    repository instead of the adopting project (e.g. when PAYLOAD_ROOT is a
    git submodule).
    """
    toplevel = _repository_toplevel(root)
    if expected_toplevel is not None:
        expected = Path(str(expected_toplevel)).expanduser().resolve()
        if toplevel != expected:
            raise ToolError(
                f"repository root mismatch: --root {root} resolves to git "
                f"toplevel {toplevel}, but the declared project root is "
                f"{expected}"
            )
    unique: dict[str, None] = {}
    for arg in paths:
        unique.setdefault(_repo_relative(toplevel, arg), None)
    rels = sorted(unique)
    return {
        "scope": rels,
        "delta_scoped_identity": _delta_identity(toplevel, rels, content_ref),
        "state_identity": _state_identity(toplevel, ref),
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Generate the v1 Scoped Content Identity (delta + state) of a "
            "declared scope of repository-relative paths (DEV-only, read-only)."
        )
    )
    parser.add_argument(
        "--root",
        default=".",
        help="directory containing the git repository (default: current dir)",
    )
    parser.add_argument(
        "--ref",
        default=None,
        help=(
            "resolve the State identity from <ref>^{tree} instead of the "
            "staged index (git write-tree)"
        ),
    )
    parser.add_argument(
        "--content-ref",
        default=None,
        help=(
            "read the per-path blobs of the Delta scoped identity from <ref> "
            "instead of the index/working tree (base-relative mode; the "
            "serialization is unchanged)"
        ),
    )
    parser.add_argument(
        "--expected-root",
        default=None,
        help=(
            "declared repository root the scope belongs to; the git toplevel "
            "resolved from --root must equal it (fail-closed guard for a "
            "payload that is a submodule)"
        ),
    )
    parser.add_argument("paths", nargs="+", help="repository-relative scope paths")
    args = parser.parse_args(argv)
    try:
        report = compute(
            Path(args.root),
            args.paths,
            ref=args.ref,
            content_ref=args.content_ref,
            expected_toplevel=args.expected_root,
        )
    except ToolError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    sys.exit(main())
