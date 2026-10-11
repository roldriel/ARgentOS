"""Root resolution contract for the adopted ARgentOS layout (GATE 1).

The adopted layout fixes three roots and their relationship::

    PROJECT_ROOT     the real project root (provided by the entry point/host)
    ARGENTOS_ROOT    PROJECT_ROOT/.argentos        (fixed, never configurable)
    PAYLOAD_ROOT     ARGENTOS_ROOT/.agents         (the protocol payload)

``PROJECT_ROOT`` is an **input**. This module never discovers it: not by fixed
parent depth (``parents[n]``), not by scanning for ``.project`` / ``.agents``
markers, and not from the process working directory. A caller that does not
have a project root must obtain one from its entry point — the ``--project-root``
CLI flag or the ``ARGENTOS_PROJECT_ROOT`` environment variable — before using
the protocol.

Declared path anchors (GATE 1)::

    .agents/<path>    -> PAYLOAD_ROOT/<path>
    .project/<path>   -> ARGENTOS_ROOT/.project/<path>
    .argentos/<path>  -> ARGENTOS_ROOT/<path>
    features.toml     -> ARGENTOS_ROOT/features.toml
    <other>           -> PROJECT_ROOT/<other>    (project files)

This module is the single implementation of the contract: the harness scripts
(``runner_state``, ``hook_gate``, ``gate_validator``, ``health_check``) import
it instead of each deriving a root for itself. Standard library only.
"""

from __future__ import annotations

import os
import re
from dataclasses import dataclass
from pathlib import Path, PurePosixPath

#: Fixed directory names of the adopted layout.
ARGENTOS_DIRNAME = ".argentos"
AGENTS_DIRNAME = ".agents"
PROJECT_DIRNAME = ".project"
BACKUP_DIRNAME = ".backup"
FEATURES_FILENAME = "features.toml"

#: Environment variable carrying the project root to a protocol component.
ENV_PROJECT_ROOT = "ARGENTOS_PROJECT_ROOT"

#: A drive-absolute reference (``C:/x`` or ``C:\\x``) is an explicit absolute path.
_DRIVE_ABSOLUTE_RE = re.compile(r"^[A-Za-z]:[\\/]")
#: A drive-relative reference (``C:x``) is ambiguous and never admissible.
_DRIVE_RELATIVE_RE = re.compile(r"^[A-Za-z]:")


class RootResolutionError(ValueError):
    """The root contract could not be satisfied (fail closed, never guess)."""


def is_within(path: Path | str, root: Path | str) -> bool:
    """True when ``path`` is ``root`` itself or lives inside it."""
    resolved = Path(os.path.abspath(str(path)))
    container = Path(os.path.abspath(str(root)))
    return resolved == container or container in resolved.parents


@dataclass(frozen=True)
class Roots:
    """The three roots of the adopted layout, derived from ``PROJECT_ROOT``."""

    project_root: Path
    argentos_root: Path
    payload_root: Path

    @property
    def project_dir(self) -> Path:
        """``ARGENTOS_ROOT/.project`` — the protocol's session/state area."""
        return self.argentos_root / PROJECT_DIRNAME

    @property
    def features_file(self) -> Path:
        """``ARGENTOS_ROOT/features.toml`` — the only active adopter config."""
        return self.argentos_root / FEATURES_FILENAME

    def contains_argentos_space(self, path: Path | str) -> bool:
        """True when ``path`` lives inside the ARgentOS space (``.argentos/``)."""
        return is_within(path, self.argentos_root)

    def resolve_reference(self, raw: str | Path) -> Path:
        """Anchor a declared path reference per the contract above.

        Relative references are anchored exactly as documented in the module
        docstring and must stay inside their anchor: a reference containing
        ``..`` is rejected (it could escape the anchor), as is a drive-relative
        reference such as ``C:x``. An absolute path (POSIX, ``C:/x`` or UNC) is
        returned as given; the caller decides whether it is inside the project.
        """
        text = str(raw).strip()
        if not text:
            raise RootResolutionError("empty path reference")
        normalized = text.replace("\\", "/")
        posix = PurePosixPath(normalized)
        if posix.is_absolute() or _DRIVE_ABSOLUTE_RE.match(normalized):
            return Path(normalized)
        if _DRIVE_RELATIVE_RE.match(normalized):
            raise RootResolutionError(
                f"drive-relative path reference is not admissible: {raw!r}"
            )
        parts = posix.parts
        if not parts:
            raise RootResolutionError(f"unresolvable path reference: {raw!r}")
        if ".." in parts:
            raise RootResolutionError(
                f"path reference escapes its anchor: {raw!r} "
                "('..' is not allowed)"
            )
        head = parts[0]
        if head == AGENTS_DIRNAME:
            return self.payload_root.joinpath(*parts[1:])
        if head == ARGENTOS_DIRNAME:
            return self.argentos_root.joinpath(*parts[1:])
        if head == PROJECT_DIRNAME:
            return self.project_dir.joinpath(*parts[1:])
        if len(parts) == 1 and head == FEATURES_FILENAME:
            return self.features_file
        return self.project_root.joinpath(*parts)


def resolve(project_root: str | os.PathLike[str] | None) -> Roots:
    """Build the three roots from a project root provided by the entry point.

    Raises :class:`RootResolutionError` when no project root is provided: the
    contract forbids inventing one.
    """
    if project_root is None or not str(project_root).strip():
        raise RootResolutionError(
            "PROJECT_ROOT must be provided by the entry point "
            f"(--project-root or {ENV_PROJECT_ROOT})"
        )
    project = Path(os.path.expanduser(str(project_root))).resolve()
    argentos = project / ARGENTOS_DIRNAME
    return Roots(
        project_root=project,
        argentos_root=argentos,
        payload_root=argentos / AGENTS_DIRNAME,
    )


def from_env(env: dict[str, str] | None = None) -> Roots | None:
    """Resolve the roots from ``ARGENTOS_PROJECT_ROOT``; ``None`` when unset."""
    source = os.environ if env is None else env
    value = source.get(ENV_PROJECT_ROOT)
    if value is None or not str(value).strip():
        return None
    return resolve(value)
