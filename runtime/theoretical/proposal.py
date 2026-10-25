"""Read a committed Implementation Plan and enumerate the items TE evaluates.

The module is read-only.  It finds the plan in the **base commit** (not in the
working tree), reads its blob through Git, reuses the inference-free parsers of
``runtime.orchestrator.observation`` and produces the declared change model:
deliverables, editable scope, effects, steps, criteria, premises, citations and
the three-valued overlay.

No section is completed or guessed.  A missing section is a declared gap; a
plan that is not committed at the base is a hard ``PROPOSAL_NOT_IN_BASE``.
"""

from __future__ import annotations

import importlib
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from runtime.orchestrator.observation import (
    AnchorObservation,
    declared_effects_section_present,
    parse_anchor,
    parse_command_set,
    parse_declared_effects,
    split_sections,
    visible,
)

from .overlay import BaseState, DeclaredOverlay, GitRepository, normalize_path

_H2_RE = re.compile(r"^##\s+(.+?)\s*$", re.MULTILINE)
_STATUS_RE = re.compile(r"^\*\*Status:\*\*\s*(.+?)\s*$", re.MULTILINE)
_CLASS_RE = re.compile(r"^\*\*RFC-56 Class:\*\*\s*(.+?)\s*$", re.MULTILINE)
_LEVEL_RE = re.compile(r"^\*\*Change Level:\*\*\s*([A-Za-z0-9]+)", re.MULTILINE)
_CHECKBOX_RE = re.compile(r"^\s*[-*]\s+\[( |x|X)\]\s*(.*)$", re.MULTILINE)
_NUMBERED_RE = re.compile(r"^\s*(\d+)\.\s+(.*)$")
_BACKTICK_RE = re.compile(r"`([^`]+)`")
_SCOPE_RE = re.compile(
    r"^\s*[-*]\s*\*\*Scope(?P<label>[^*]*)\*\*\s*:?\s*(?P<scope>.*)$",
    re.MULTILINE | re.IGNORECASE,
)
_PLAN_NAME_RE = re.compile(r"^docs/plans/(?P<number>\d+)-[a-z0-9-]+\.md$")


class ProposalError(RuntimeError):
    """The proposal cannot be evaluated at the requested base (fail-closed)."""

    def __init__(self, code: str, message: str):
        super().__init__(message)
        self.code = code


@dataclass(frozen=True)
class Item:
    """One declared item that requires a claim in the result."""

    id: str
    kind: str
    label: str
    text: str

    def to_dict(self) -> dict[str, str]:
        return {
            "id": self.id,
            "kind": self.kind,
            "label": self.label,
            "text": self.text,
        }


@dataclass(frozen=True)
class Proposal:
    """The declared change model TE evaluates."""

    root: Path
    plan: int
    path: str
    text: str
    blob: str
    status: str
    rfc56_class: str
    change_level: str
    deliverables: tuple[str, ...]
    scope: tuple[str, ...]
    scope_declared: bool
    effects: tuple[str, ...]
    effects_declared: bool
    effects_unreadable: bool
    commands: tuple[tuple[str, ...], ...]
    premises: tuple[str, ...]
    items: tuple[Item, ...]
    gaps: tuple[str, ...]
    unresolved_deliverables: tuple[str, ...]
    rejected_paths: tuple[str, ...]
    anchor: AnchorObservation
    base: BaseState
    overlay: DeclaredOverlay
    citations: tuple[Any, ...]

    @property
    def payload_paths(self) -> tuple[str, ...]:
        return tuple(
            path
            for path in self.deliverables
            if path == "protocol/_AGENTS.md" or path.startswith("protocol/.agents/")
        )


def _section(text: str, prefix: str) -> str | None:
    for heading, body in split_sections(text, _H2_RE).items():
        if heading.casefold().startswith(prefix.casefold()):
            return body
    return None


def _table_rows(body: str) -> list[list[str]]:
    rows: list[list[str]] = []
    seen_separator = False
    for line in body.splitlines():
        stripped = line.strip()
        if not stripped.startswith("|"):
            continue
        cells = [cell.strip() for cell in stripped.strip("|").split("|")]
        if all(set(cell) <= set("-: ") and cell for cell in cells):
            seen_separator = True
            continue
        if not seen_separator:
            continue
        rows.append(cells)
    return rows


def _looks_like_path(token: str) -> bool:
    """True when a backticked token declares a file (a slash or an extension).

    A deliverable line may carry a parenthetical annotation in backticks (for
    example ``(`[Unreleased]`)``): that token is not a second deliverable.  The
    rule is deliberately structural, never semantic: a declaration with no
    slash and no extension is reported as unresolved instead of being guessed.
    """
    return "/" in token or "." in token


def _paths_from_text(
    text: str, rejected: list[str] | None = None
) -> tuple[str, ...]:
    """Every backticked repository-relative path in ``text``, in order.

    A token that cannot be normalized is not silently dropped when ``rejected``
    is provided: it is a declared path the change model cannot represent, and
    CH-9 reports it.
    """
    found: list[str] = []
    for token in _BACKTICK_RE.findall(text):
        candidate = token.strip()
        if not candidate or " " in candidate or ":" in candidate:
            continue
        try:
            path = normalize_path(candidate)
        except ValueError:
            if rejected is not None and candidate not in rejected:
                rejected.append(candidate)
            continue
        if path not in found:
            found.append(path)
    return tuple(found)


def _deliverables(text: str) -> tuple[tuple[str, ...], tuple[str, ...], tuple[str, ...]]:
    """Deliverables of ``## Entregables``: (paths, unresolved labels, rejected tokens).

    Every file declared on a numbered line is enumerated (a line may declare
    more than one).  A numbered line with no resolvable path is returned as an
    *unresolved label*; a token that looks like a path but is not
    repository-relative is returned as a *rejected token*.  Neither is completed
    or guessed: CH-9 reports both.
    """
    body = _section(text, "Entregables") or ""
    found: list[str] = []
    unresolved: list[str] = []
    rejected: list[str] = []
    for line in body.splitlines():
        match = _NUMBERED_RE.match(line)
        if not match:
            continue
        candidates = [
            token.strip()
            for token in _BACKTICK_RE.findall(match.group(2))
            if token.strip()
            and " " not in token.strip()
            and ":" not in token.strip()
            and _looks_like_path(token.strip())
        ]
        paths: list[str] = []
        line_rejected = False
        for candidate in candidates:
            try:
                path = normalize_path(candidate)
            except ValueError:
                line_rejected = True
                if candidate not in rejected:
                    rejected.append(candidate)
                continue
            if path not in paths:
                paths.append(path)
        if not paths and not line_rejected:
            label = match.group(2).strip()
            if label and label not in unresolved:
                unresolved.append(label)
            continue
        for path in paths:
            if path not in found:
                found.append(path)
    return tuple(found), tuple(unresolved), tuple(rejected)


def _scope(text: str) -> tuple[tuple[str, ...], bool]:
    body = _section(text, "Delegación agentiva") or ""
    match = _SCOPE_RE.search(visible(body))
    if not match:
        return (), False
    return _paths_from_text(match.group("scope")), True


def _checkbox_items(text: str, section_prefix: str) -> tuple[str, ...]:
    body = _section(text, section_prefix) or ""
    return tuple(
        label.strip() for _, label in _CHECKBOX_RE.findall(body) if label.strip()
    )


def _steps(text: str) -> tuple[tuple[str, str], ...]:
    body = _section(text, "Pasos") or ""
    rows = _table_rows(visible(body))
    steps: list[tuple[str, str]] = []
    if rows:
        for cells in rows:
            if not cells:
                continue
            label = cells[0].strip().strip("*`").strip()
            if not label:
                continue
            detail = " | ".join(cell for cell in cells[1:] if cell)
            steps.append((label, detail))
        return tuple(steps)
    for line in body.splitlines():
        match = _NUMBERED_RE.match(line)
        if match:
            steps.append((f"step-{match.group(1)}", match.group(2).strip()))
    return tuple(steps)


def _premises(text: str) -> tuple[tuple[str, str], ...]:
    body = _section(text, "Derivación y premisas") or ""
    premises: list[tuple[str, str]] = []
    for cells in _table_rows(visible(body)):
        if not cells:
            continue
        label = cells[0].strip().strip("`* ").strip()
        if not label:
            continue
        detail = " | ".join(cell for cell in cells[1:] if cell)
        premises.append((label, detail))
    return tuple(premises)


def _status(text: str) -> str:
    match = _STATUS_RE.search(text)
    return match.group(1).strip() if match else ""


def _rfc56_class(text: str) -> str:
    match = _CLASS_RE.search(text)
    return match.group(1).strip() if match else ""


def _change_level(text: str) -> str:
    match = _LEVEL_RE.search(text)
    return match.group(1).strip() if match else ""


def _load_tool(name: str):
    tools = Path(__file__).resolve().parents[2] / "tools"
    if str(tools) not in sys.path:
        sys.path.insert(0, str(tools))
    return importlib.import_module(name)


def _find_plan_in_base(repo: GitRepository, base: BaseState, plan: int) -> str | None:
    try:
        names = repo.list_paths(base.commit, "docs/plans")
    except Exception as exc:  # noqa: BLE001 - always fail closed
        raise ProposalError("BASE_UNREADABLE", str(exc)) from exc
    padded = rf"^docs/plans/{plan:03d}-[a-z0-9-]+\.md$"
    plain = rf"^docs/plans/{plan}-[a-z0-9-]+\.md$"
    for name in names:
        if re.match(padded, name) or re.match(plain, name):
            return name
    return None


def _build(
    root: Path,
    plan: int,
    path: str,
    base: BaseState,
    repo: GitRepository,
) -> Proposal:
    text = repo.read_text(base.commit, path)
    if text is None:
        raise ProposalError(
            "PROPOSAL_NOT_IN_BASE",
            f"{path} is not readable at base commit {base.commit}",
        )
    blob = repo.blob(base.commit, path)
    if blob is None:
        raise ProposalError(
            "PROPOSAL_NOT_IN_BASE",
            f"{path} has no blob at base commit {base.commit}",
        )

    status = _status(text)
    if not status:
        raise ProposalError("PROPOSAL_STATUS_MISSING", f"{path} declares no **Status:**")
    if status.split("(")[0].strip().casefold().startswith("superseded"):
        raise ProposalError("PROPOSAL_SUPERSEDED", f"{path} is Superseded")

    deliverables, unresolved_deliverables, rejected_paths = _deliverables(text)
    scope, scope_declared = _scope(text)
    effects = parse_declared_effects(text)
    effects_declared = declared_effects_section_present(text)
    effects_unreadable = any(effect.unreadable for effect in effects)
    effect_classes = tuple(
        sorted(
            {
                effect.effect_class
                for effect in effects
                if not effect.negative and not effect.unreadable and effect.effect_class
            }
        )
    )
    commands = parse_command_set(text)
    premises = _premises(text)
    criteria = _checkbox_items(text, "Criterios de salida")
    steps = _steps(text)
    anchor = parse_anchor(text)
    citations = tuple(_load_tool("check_plan_citations").extract_citations(text))

    items: list[Item] = []
    for index, path_item in enumerate(deliverables, start=1):
        items.append(Item(f"D-{index:02d}", "deliverable", path_item, path_item))
    for index, (label, detail) in enumerate(steps, start=1):
        items.append(Item(f"S-{index:02d}", "step", label, detail))
    for index, criterion in enumerate(criteria, start=1):
        items.append(Item(f"C-{index:02d}", "criterion", criterion, criterion))
    for index, effect in enumerate(effect_classes, start=1):
        items.append(Item(f"E-{index:02d}", "effect", effect, effect))
    for index, (label, detail) in enumerate(premises, start=1):
        items.append(Item(f"P-{index:02d}", "premise", label, detail))

    gaps: list[str] = []
    if not deliverables:
        gaps.append("proposal declares no deliverables (## Entregables)")
    if not steps:
        gaps.append("proposal declares no steps (## Pasos)")
    if not criteria:
        gaps.append("proposal declares no exit criteria (## Criterios de salida)")
    if not effects_declared:
        gaps.append("proposal declares no effects container (## Efectos declarados)")
    if effects_unreadable:
        gaps.append("an effects row is unreadable and is not assumed authorized")
    if not premises:
        gaps.append("proposal declares no premises(D) (## Derivación y premisas)")
    if not commands:
        gaps.append("proposal declares no verification command-set (## Verificación)")

    overlay = DeclaredOverlay.build(repo, base, deliverables, effect_classes)
    return Proposal(
        root=root,
        plan=plan,
        path=path,
        text=text,
        blob=blob,
        status=status,
        rfc56_class=_rfc56_class(text),
        change_level=_change_level(text),
        deliverables=deliverables,
        scope=scope,
        scope_declared=scope_declared,
        effects=effect_classes,
        effects_declared=effects_declared,
        effects_unreadable=effects_unreadable,
        commands=commands,
        premises=tuple(label for label, _ in premises),
        items=tuple(items),
        gaps=tuple(gaps),
        unresolved_deliverables=unresolved_deliverables,
        rejected_paths=rejected_paths,
        anchor=anchor,
        base=base,
        overlay=overlay,
        citations=citations,
    )


def load_proposal(
    root: str | Path,
    plan: int,
    base_ref: str = "HEAD",
) -> Proposal:
    """Load ``docs/plans/<plan>-*.md`` from ``base_ref`` (read-only)."""
    root_path = Path(root).resolve()
    repo = GitRepository(root_path)
    if not repo.verify_ref(base_ref):
        raise ProposalError(
            "BASE_UNREADABLE",
            f"base {base_ref!r} does not resolve to a commit in {root_path}",
        )
    base = repo.base_state(base_ref)
    path = _find_plan_in_base(repo, base, plan)
    if path is None:
        raise ProposalError(
            "PROPOSAL_NOT_FOUND",
            f"plan {plan} was not found in {base.commit}:docs/plans/",
        )
    return _build(root_path, plan, path, base, repo)


def load_proposal_at(
    root: str | Path,
    path: str,
    base_ref: str = "HEAD",
) -> Proposal:
    """Load one specific plan path from ``base_ref`` (used by the validator)."""
    root_path = Path(root).resolve()
    repo = GitRepository(root_path)
    if not repo.verify_ref(base_ref):
        raise ProposalError(
            "BASE_UNREADABLE",
            f"base {base_ref!r} does not resolve to a commit in {root_path}",
        )
    base = repo.base_state(base_ref)
    rel = normalize_path(path)
    match = _PLAN_NAME_RE.match(rel)
    plan = int(match.group("number")) if match else 0
    if repo.blob(base.commit, rel) is None:
        raise ProposalError(
            "PROPOSAL_NOT_IN_BASE",
            f"{rel} is not readable at base commit {base.commit}",
        )
    return _build(root_path, plan, rel, base, repo)


def item_list(proposal: Proposal) -> tuple[Item, ...]:
    """The enumerated items in their stable order (used by callers and tests)."""
    return proposal.items
