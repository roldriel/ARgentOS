"""Declared overlay: the v1 representation of the hypothetical world of TE.

Theoretical Execution never fabricates the content a proposal has not produced
yet.  A declared path is therefore *unknown* by construction; every other path
is answered from the factual base commit (never from the working tree).  This
module is read-only and depends only on local Git objects.
"""

from __future__ import annotations

import subprocess
from dataclasses import dataclass
from pathlib import Path, PurePosixPath

DECLARED_UNKNOWN = "DECLARED_UNKNOWN"
PRESENT = "PRESENT"
ABSENT = "ABSENT"
CONTENT_POLICY = "DECLARED_UNKNOWN"


class GitError(RuntimeError):
    """A local, read-only Git operation could not produce a usable answer."""


def normalize_path(path: str) -> str:
    """Normalize a repository-relative POSIX path, rejecting escapes.

    Representation-only normalization: separators, a leading ``./`` and a
    trailing slash.  It never invents a path and never widens the scope.
    """
    candidate = str(path or "").strip().replace("\\", "/")
    if candidate.startswith("./"):
        candidate = candidate[2:]
    candidate = candidate.rstrip("/")
    if not candidate:
        raise ValueError("empty path")
    if candidate.startswith("/") or candidate.startswith("-"):
        raise ValueError(f"not a repository-relative path: {path!r}")
    parts = PurePosixPath(candidate).parts
    if not parts or any(part == ".." for part in parts):
        raise ValueError(f"path escapes the repository: {path!r}")
    return candidate


@dataclass(frozen=True)
class BaseState:
    """The factual state a TE run reads: a commit and its tree."""

    commit: str
    tree: str

    def to_dict(self) -> dict[str, str]:
        return {"commit": self.commit, "tree": self.tree}


class GitRepository:
    """Read-only access to one local repository through Git objects.

    Only the commands needed by TE are exposed: ref resolution, tree/blob
    lookups and blob content.  There is no checkout, no index write and no
    working-tree read.
    """

    def __init__(self, root: str | Path):
        self.root = Path(root).resolve()

    def _run(self, *args: str) -> tuple[int, bytes, bytes]:
        try:
            proc = subprocess.run(
                ["git", "-C", str(self.root), *args],
                check=False,
                capture_output=True,
            )
        except OSError as exc:  # pragma: no cover - depends on the environment
            raise GitError(f"git could not be executed: {exc}") from exc
        return proc.returncode, proc.stdout, proc.stderr

    def verify_ref(self, ref: str) -> bool:
        """True when ``ref`` resolves to a commit (read-only, fail-closed)."""
        if not ref or ref.startswith("-"):
            return False
        code, _, _ = self._run("rev-parse", "--verify", "--quiet", f"{ref}^{{commit}}")
        return code == 0

    def commit(self, ref: str) -> str | None:
        if not ref or ref.startswith("-"):
            return None
        code, out, _ = self._run("rev-parse", "--verify", "--quiet", f"{ref}^{{commit}}")
        if code != 0:
            return None
        return out.decode("ascii", errors="replace").strip() or None

    def tree(self, ref: str) -> str | None:
        if not ref or ref.startswith("-"):
            return None
        code, out, _ = self._run("rev-parse", "--verify", "--quiet", f"{ref}^{{tree}}")
        if code != 0:
            return None
        return out.decode("ascii", errors="replace").strip() or None

    def base_state(self, ref: str) -> BaseState:
        commit = self.commit(ref)
        if commit is None:
            raise GitError(f"ref does not resolve to a commit: {ref!r}")
        tree = self.tree(commit)
        if tree is None:
            raise GitError(f"commit has no tree: {commit}")
        return BaseState(commit=commit, tree=tree)

    def exists(self, ref: str, path: str) -> bool:
        rel = normalize_path(path)
        code, _, _ = self._run("cat-file", "-e", f"{ref}:{rel}")
        return code == 0

    def blob(self, ref: str, path: str) -> str | None:
        rel = normalize_path(path)
        code, out, _ = self._run("rev-parse", "--verify", "--quiet", f"{ref}:{rel}")
        if code != 0:
            return None
        return out.decode("ascii", errors="replace").strip() or None

    def object_type(self, oid: str) -> str | None:
        """The Git object type of ``oid`` (tree/blob/commit), or ``None``."""
        if not oid or oid.startswith("-"):
            return None
        code, out, _ = self._run("cat-file", "-t", oid)
        if code != 0:
            return None
        return out.decode("ascii", errors="replace").strip() or None

    def read(self, ref: str, path: str) -> bytes | None:
        rel = normalize_path(path)
        code, out, _ = self._run("cat-file", "blob", f"{ref}:{rel}")
        if code != 0:
            return None
        return out

    def read_text(self, ref: str, path: str) -> str | None:
        raw = self.read(ref, path)
        if raw is None:
            return None
        return raw.decode("utf-8", errors="replace")

    def list_paths(self, ref: str, prefix: str = "") -> tuple[str, ...]:
        args = ["ls-tree", "-r", "--name-only", ref]
        if prefix:
            args.extend(["--", normalize_path(prefix)])
        code, out, _ = self._run(*args)
        if code != 0:
            raise GitError(f"git ls-tree failed for {ref!r} {prefix!r}")
        return tuple(
            sorted(line for line in out.decode("utf-8", errors="replace").splitlines() if line)
        )


@dataclass(frozen=True)
class DeclaredOverlay:
    """An immutable, three-valued view of ``base + declared change``.

    ``declared_paths`` is the set of files the proposal may change.  Its
    content is unknown; its existence is unknown too (the proposal may create,
    modify or delete it).  Every other path is answered from ``base``.
    """

    base: BaseState
    declared_paths: frozenset[str]
    effects: frozenset[str]
    repository: GitRepository
    content_policy: str = CONTENT_POLICY

    @classmethod
    def build(
        cls,
        repository: GitRepository,
        base: BaseState,
        declared_paths: Iterable[str],
        effects: Iterable[str] = (),
    ) -> "DeclaredOverlay":
        paths = frozenset(normalize_path(path) for path in declared_paths)
        effect_set = frozenset(str(effect).strip() for effect in effects if str(effect).strip())
        return cls(base=base, declared_paths=paths, effects=effect_set, repository=repository)

    def touched(self, path: str) -> bool:
        return normalize_path(path) in self.declared_paths

    def existence(self, path: str) -> str:
        rel = normalize_path(path)
        if rel in self.declared_paths:
            return DECLARED_UNKNOWN
        return PRESENT if self.repository.exists(self.base.commit, rel) else ABSENT

    def content(self, path: str) -> bytes | None:
        """Blob content for an untouched path; ``None`` for an unknown one."""
        rel = normalize_path(path)
        if rel in self.declared_paths:
            return None
        return self.repository.read(self.base.commit, rel)

    def paths(self) -> tuple[str, ...]:
        return tuple(sorted(self.declared_paths))

    def identity(self) -> dict[str, object]:
        return {
            "kind": "declared_overlay",
            "base": self.base.to_dict(),
            "paths": list(self.paths()),
            "effects": sorted(self.effects),
            "content": "unknown",
        }

    def to_dict(self) -> dict[str, object]:
        return {
            "base": self.base.to_dict(),
            "declared_paths": list(self.paths()),
            "effects": sorted(self.effects),
            "content_policy": self.content_policy,
        }
