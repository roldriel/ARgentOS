"""Read-only observation of one DEV Change (plan 122, step M1-1/M1-2/M1-3).

The host does not hold state: every iteration re-observes the repository and
derives from what is really there. This module is the observation half of that
loop and it is deliberately **read-only and inference-free**:

- what exists is reported as existing, with its literal value;
- what is absent is reported as absent (a ``GAP``), never as a positive fact;
- nothing is repaired, normalised, guessed or completed here.

Sources of the observation are exactly the ones the Change Lifecycle already
declares as repository state: Git, the plan artifact, the governance INDEX and
the persisted Worker Results. No new representation of the change is created.
"""

from __future__ import annotations

import importlib
import re
import subprocess
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Mapping, Sequence

from .store import OrchestratorStore

PLANS_DIR = "docs/plans"
PLANS_INDEX = "docs/plans/INDEX.md"

_H2_RE = re.compile(r"^##\s+(.+?)\s*$", re.MULTILINE)
_H3_RE = re.compile(r"^###\s+(.+?)\s*$", re.MULTILINE)
_STATUS_RE = re.compile(r"^\*\*Status:\*\*\s*(.+?)\s*$", re.MULTILINE)
_LEVEL_RE = re.compile(r"^\*\*Change Level:\*\*\s*([A-Za-z0-9]+)", re.MULTILINE)
_RFC_RE = re.compile(r"^\*\*RFC:\*\*\s*(.+?)\s*$", re.MULTILINE)
_CHECKBOX_RE = re.compile(r"^\s*[-*]\s+\[( |x|X)\]\s*(.*)$", re.MULTILINE)
_FENCE_RE = re.compile(r"```[a-zA-Z]*\n(.*?)```", re.DOTALL)
_BACKTICK_RE = re.compile(r"`([^`]+)`")
_STATE_ID_RE = re.compile(r"\b([0-9a-f]{40})\b")
_DELTA_ID_RE = re.compile(r"\b([0-9a-f]{64})\b")
_FINDING_REF_RE = re.compile(r"^\s*[-*]\s*`([^`]*:F-\d+)`")
_PENDING_REF_RE = re.compile(r"^\s*[-*]\s*`([^`]*)`")
_ESTADO_RE = re.compile(r"estado:\s*[`*_\s]*([a-zA-Z-]+)")
_BLOCKING_RE = re.compile(r"blocking:\s*\**\s*(s[ií]|no)\b", re.IGNORECASE)
_RESOLUTION_RE = re.compile(r"resoluci[oó]n:\s*(.{0,40})", re.DOTALL)

#: Anchors declare their validated scope set in a machine-readable bullet so the
#: staleness of the anchor can be re-derived from the artifact alone.
_SCOPE_SET_RE = re.compile(r"^\s*[-*]\s*\**Scope set[^\n]*$", re.MULTILINE)

_PATH_TOKEN_RE = re.compile(r"^[A-Za-z0-9._-]+(?:/[A-Za-z0-9._-]+)+$")


class ObservationError(RuntimeError):
    """Unrecoverable read error while observing the repository."""


# --------------------------------------------------------------------------- #
# Git
# --------------------------------------------------------------------------- #


@dataclass(frozen=True)
class GitState:
    is_repository: bool
    head: str | None
    branch: str | None
    dirty_paths: tuple[str, ...]

    def to_dict(self) -> dict[str, Any]:
        return {
            "is_repository": self.is_repository,
            "head": self.head,
            "branch": self.branch,
            "dirty_paths": list(self.dirty_paths),
        }


def _run_git(root: Path, *args: str) -> str | None:
    """Run a local read-only git command; ``None`` when it cannot be resolved."""
    try:
        proc = subprocess.run(
            ["git", "-C", str(root), *args],
            check=False,
            capture_output=True,
            text=True,
        )
    except OSError:
        return None
    if proc.returncode != 0:
        return None
    return proc.stdout


def git_state(root: Path) -> GitState:
    """Head, branch and modified tracked paths; ``is_repository=False`` if not git."""
    head = _run_git(root, "rev-parse", "HEAD")
    branch = _run_git(root, "rev-parse", "--abbrev-ref", "HEAD")
    status = _run_git(root, "status", "--porcelain")
    if head is None or branch is None or status is None:
        return GitState(False, None, None, ())
    dirty = tuple(
        sorted(
            line[3:].strip()
            for line in status.splitlines()
            if line.strip() and not line.startswith("??")
        )
    )
    return GitState(True, head.strip(), branch.strip(), dirty)


def scoped_content_identity(
    root: Path, paths: Sequence[str]
) -> dict[str, Any] | None:
    """Reuse the existing v1 generator (plan 109); never duplicate the algorithm.

    Fail-closed: an unavailable generator, a non-git root or an unresolvable
    path yields ``None`` (declared absence), never a fabricated identity.
    """
    if not paths:
        return None
    tools_dir = Path(__file__).resolve().parents[2] / "tools"
    if str(tools_dir) not in sys.path:
        sys.path.insert(0, str(tools_dir))
    try:
        module = importlib.import_module("scoped_content_identity")
    except ImportError:
        return None
    try:
        return module.compute(root, list(paths))
    except Exception:  # noqa: BLE001 - the generator fails closed by contract
        return None


# --------------------------------------------------------------------------- #
# Plan artifact parsing
# --------------------------------------------------------------------------- #


def find_plan_path(root: Path, plan_number: int) -> Path | None:
    """The numbered plan artifact ``docs/plans/<NNN>-*.md``, if it exists."""
    plans_dir = root / PLANS_DIR
    if not plans_dir.is_dir():
        return None
    matches = sorted(plans_dir.glob(f"{plan_number:03d}-*.md"))
    if not matches:
        matches = sorted(plans_dir.glob(f"{plan_number}-*.md"))
    return matches[0] if matches else None


def split_sections(text: str, pattern: re.Pattern[str]) -> dict[str, str]:
    """Map heading -> body for every heading matching ``pattern``."""
    matches = list(pattern.finditer(text))
    out: dict[str, str] = {}
    for index, match in enumerate(matches):
        end = matches[index + 1].start() if index + 1 < len(matches) else len(text)
        out.setdefault(match.group(1).strip(), text[match.end() : end])
    return out


def _section(text: str, prefix: str, pattern: re.Pattern[str]) -> str | None:
    for heading, body in split_sections(text, pattern).items():
        if heading.casefold().startswith(prefix.casefold()):
            return body
    return None


def visible(text: str) -> str:
    """Text without HTML comments or horizontal rules.

    An empty record container (a comment placeholder and nothing else) is an
    **empty record**: it declares no registration, which is a ``GAP``/``N/A``,
    never a positive fact.
    """
    stripped = re.sub(r"<!--.*?-->", "", text, flags=re.DOTALL)
    lines = [
        line for line in stripped.splitlines() if line.strip() and line.strip() != "---"
    ]
    return "\n".join(lines).strip()


@dataclass(frozen=True)
class EntryCriteria:
    total: int
    checked: int
    unchecked: tuple[str, ...]

    @property
    def satisfied(self) -> bool:
        return self.total > 0 and self.checked == self.total

    def to_dict(self) -> dict[str, Any]:
        return {
            "total": self.total,
            "checked": self.checked,
            "unchecked": list(self.unchecked),
            "satisfied": self.satisfied,
        }


def parse_entry_criteria(text: str) -> EntryCriteria:
    body = _section(text, "Criterio de entrada", _H2_RE) or ""
    total = 0
    checked = 0
    unchecked: list[str] = []
    for mark, label in _CHECKBOX_RE.findall(body):
        total += 1
        if mark.casefold() == "x":
            checked += 1
        else:
            unchecked.append(label.strip()[:120])
    return EntryCriteria(total, checked, tuple(unchecked))


def parse_command_set(text: str) -> tuple[tuple[str, ...], ...]:
    """The declared validation command-set: the fenced blocks of ``## Verificación``.

    Only real command lines are taken (a line whose first token is a program
    name); prose, comments and blank lines are not commands. Nothing is
    invented: a missing section yields an empty command-set (a ``GAP``).
    """
    body = _section(text, "Verificaci", _H2_RE)
    if body is None:
        return ()
    commands: list[tuple[str, ...]] = []
    for block in _FENCE_RE.findall(body):
        for raw in block.splitlines():
            line = raw.strip()
            if not line or line.startswith("#"):
                continue
            tokens = tuple(line.split())
            if tokens and re.match(r"^[A-Za-z0-9._/-]+$", tokens[0]):
                commands.append(tokens)
    return tuple(commands)


#: Declared environmental class, machine-readable, inside the verification fence:
#: ``# environmental-class: <command prefix> -> <declaration>``
_ENVIRONMENTAL_RE = re.compile(
    r"^\s*#\s*environmental-class:\s*(?P<prefix>.+?)\s*->\s*(?P<declaration>.+?)\s*$",
    re.MULTILINE,
)


#: The plan's **agent-task declaration** (plan 123): the authorized instruction a
#: semantic worker is delegated, and the paths it is authorized to modify.
#: Additive-optional: a plan without it delegates no semantic work (declared
#: absence), which is why it is read without being required.
_AGENT_TASK_SECTION_PREFIX = "Delegación agentiva"
_AGENT_TASK_FIELD_RE = re.compile(
    r"^\s*[-*]\s*\**Task\**\s*:\s*(?P<task>.*?)\s*$", re.MULTILINE | re.IGNORECASE
)
_AGENT_SCOPE_FIELD_RE = re.compile(
    r"^\s*[-*]\s*\**Scope\**\s*:\s*(?P<scope>.*?)\s*$", re.MULTILINE | re.IGNORECASE
)


@dataclass(frozen=True)
class AgentTask:
    """The authorized semantic-work declaration of a plan (additive-optional).

    ``declared`` is True only when the plan really carries the declaration
    container with a non-empty task. A container whose task is absent is a
    declared absence, never an inferred task: the host does not invent work.
    ``scope`` is the set of repository-relative paths the worker is authorized
    to modify; when the declaration names none, the plan's declared deliverables
    are used and ``scope_declared`` records that the scope was not explicit.
    """

    declared: bool
    task: str
    scope: tuple[str, ...]
    section_present: bool
    scope_declared: bool

    def to_dict(self) -> dict[str, Any]:
        return {
            "declared": self.declared,
            "task": self.task,
            "scope": list(self.scope),
            "section_present": self.section_present,
            "scope_declared": self.scope_declared,
        }


def _unbold(value: str) -> str:
    """Remove the Markdown emphasis markers a plan field may wrap its value in."""
    return value.strip().strip("*_").strip()


def parse_agent_task(text: str) -> AgentTask:
    """Read the plan's agent-task declaration, if it carries one.

    Read-only and inference-free: a missing container, a container without a
    task, and a container without an explicit scope are three distinct declared
    facts, and none of them is completed here.
    """
    body = _section(text, _AGENT_TASK_SECTION_PREFIX, _H2_RE)
    if body is None:
        return AgentTask(False, "", (), False, False)
    content = visible(body)
    task_match = _AGENT_TASK_FIELD_RE.search(content)
    task = _unbold(task_match.group("task")) if task_match else ""
    scope: list[str] = []
    scope_match = _AGENT_SCOPE_FIELD_RE.search(content)
    if scope_match:
        for token in _BACKTICK_RE.findall(scope_match.group("scope")):
            candidate = token.strip()
            if _PATH_TOKEN_RE.match(candidate) and candidate not in scope:
                scope.append(candidate)
    return AgentTask(
        declared=bool(task),
        task=task,
        scope=tuple(sorted(scope)),
        section_present=True,
        scope_declared=bool(scope),
    )


def parse_environmental_classes(
    text: str,
) -> tuple[tuple[str, str], ...]:
    """Declared environmental classes of the validation command-set.

    The declaration is a **human declaration in the authorized plan**, not a
    judgement of the host: it states that for a named command the environment
    (not the change) prevents the evidence from being obtained, and that the
    resulting signal is ``GAP`` (declared absence), never ``PASS``. Materiality
    of the declaration remains the maintainer's decision.
    """
    body = _section(text, "Verificaci", _H2_RE)
    if body is None:
        return ()
    found: list[tuple[str, str]] = []
    for match in _ENVIRONMENTAL_RE.finditer(body):
        found.append((match.group("prefix").strip(), match.group("declaration").strip()))
    return tuple(found)


def declared_artifacts(text: str) -> tuple[str, ...]:
    """Repository-relative file paths declared in ``## Entregables``.

    Only backticked tokens that look like file paths are taken (a slash and a
    file extension, no citation separator). Absence is not an error: the list is
    advisory and is used to declare the validated scope set.
    """
    body = _section(text, "Entregables", _H2_RE) or ""
    found: list[str] = []
    for token in _BACKTICK_RE.findall(body):
        candidate = token.strip()
        if ":" in candidate or " " in candidate:
            continue
        if not _PATH_TOKEN_RE.match(candidate):
            continue
        if "." not in candidate.rsplit("/", 1)[-1]:
            continue
        if candidate not in found:
            found.append(candidate)
    return tuple(found)


@dataclass(frozen=True)
class FindingRecord:
    ref: str
    state: str
    line: str

    def to_dict(self) -> dict[str, Any]:
        return {"ref": self.ref, "state": self.state}


@dataclass(frozen=True)
class PendingRecord:
    ref: str
    blocking: bool
    resolution: str
    line: str

    @property
    def unresolved(self) -> bool:
        return "pendiente" in self.resolution.casefold()

    def to_dict(self) -> dict[str, Any]:
        return {
            "ref": self.ref,
            "blocking": self.blocking,
            "resolution": self.resolution,
            "unresolved": self.unresolved,
        }


def parse_findings(text: str) -> tuple[FindingRecord, ...]:
    body = _section(text, "Findings", _H3_RE) or ""
    records: list[FindingRecord] = []
    for line in body.splitlines():
        match = _FINDING_REF_RE.match(line)
        if not match:
            continue
        estado = _ESTADO_RE.search(line)
        records.append(
            FindingRecord(
                ref=match.group(1),
                state=(estado.group(1).casefold() if estado else "open"),
                line=line.strip(),
            )
        )
    return tuple(records)


def parse_pending(text: str) -> tuple[PendingRecord, ...]:
    body = _section(text, "Pending decisions", _H3_RE)
    if body is None:
        return ()
    records: list[PendingRecord] = []
    for line in body.splitlines():
        if line.strip().startswith("<!--"):
            continue
        match = _PENDING_REF_RE.match(line)
        if not match or ":" in match.group(1) and "F-" in match.group(1):
            continue
        blocking_match = _BLOCKING_RE.search(line)
        if blocking_match is None:
            continue
        resolution_match = _RESOLUTION_RE.search(line)
        resolution = (
            resolution_match.group(1).replace("*", "").strip()
            if resolution_match
            else ""
        )
        records.append(
            PendingRecord(
                ref=match.group(1),
                blocking=blocking_match.group(1).casefold().startswith("s"),
                resolution=resolution,
                line=line.strip(),
            )
        )
    return tuple(records)


@dataclass(frozen=True)
class AnchorObservation:
    present: bool
    state_identity: str | None
    delta_identity: str | None
    validity: str | None
    scope_set: tuple[str, ...]
    revalidated: bool = False
    state_identities: tuple[str, ...] = ()
    delta_identities: tuple[str, ...] = ()

    def to_dict(self) -> dict[str, Any]:
        return {
            "present": self.present,
            "state_identity": self.state_identity,
            "delta_identity": self.delta_identity,
            "validity": self.validity,
            "scope_set": list(self.scope_set),
            "revalidated": self.revalidated,
            "state_identities": list(self.state_identities),
            "delta_identities": list(self.delta_identities),
        }


_STATE_BULLET_RE = re.compile(
    r"^\s*[-*]\s*\*{0,2}State identity[^\n]*$", re.MULTILINE
)
_DELTA_BULLET_RE = re.compile(
    r"^\s*[-*]\s*\*{0,2}Delta scoped identity[^\n]*$", re.MULTILINE
)


def parse_anchor(text: str) -> AnchorObservation:
    """Read a Validation Anchor (v1) as an observation.

    A1 is the historical record and A2 never replaces it, so a revalidated
    anchor carries more than one identity pair: the **applicable** identity is
    the last registered one, and the earlier ones stay as history.
    """
    body = _section(text, "Validation anchor", _H2_RE) or ""
    content = visible(body)
    if not content:
        return AnchorObservation(False, None, None, None, ())

    state_ids = tuple(
        match.group(1)
        for bullet in _STATE_BULLET_RE.findall(content)
        for match in [_STATE_ID_RE.search(bullet)]
        if match
    )
    delta_ids: list[str] = []
    for bullet in _DELTA_BULLET_RE.findall(content):
        for match in _DELTA_ID_RE.finditer(bullet):
            delta_ids.append(match.group(1))
    delta_ids_tuple = tuple(delta_ids)

    validity_match = re.search(r"Validity\s*/\s*stale[^\n]*", content)
    validity = validity_match.group(0).strip() if validity_match else None
    revalidated = bool(
        validity and re.search(r"\brevalidada\b", validity, re.IGNORECASE)
    )
    scope: list[str] = []
    scope_match = _SCOPE_SET_RE.search(content)
    if scope_match:
        for token in _BACKTICK_RE.findall(scope_match.group(0)):
            candidate = token.strip()
            if _PATH_TOKEN_RE.match(candidate) and candidate not in scope:
                scope.append(candidate)
    return AnchorObservation(
        present=True,
        state_identity=state_ids[-1] if state_ids else None,
        delta_identity=delta_ids_tuple[-1] if delta_ids_tuple else None,
        validity=validity,
        scope_set=tuple(sorted(scope)),
        revalidated=revalidated,
        state_identities=state_ids,
        delta_identities=delta_ids_tuple,
    )


@dataclass(frozen=True)
class CheckpointObservation:
    present: bool
    closure_tree: str | None
    condition: str | None
    consistency_pass: bool

    def to_dict(self) -> dict[str, Any]:
        return {
            "present": self.present,
            "closure_tree": self.closure_tree,
            "condition": self.condition,
            "consistency_pass": self.consistency_pass,
        }


def parse_checkpoint(text: str) -> CheckpointObservation:
    body = _section(text, "Checkpoint", _H2_RE) or ""
    content = visible(body)
    if not content:
        return CheckpointObservation(False, None, None, False)
    closure_block = ""
    closure_match = re.search(r"Estado de cierre[^\n]*", content)
    if closure_match:
        closure_block = closure_match.group(0)
    tree_match = _STATE_ID_RE.search(closure_block)
    condition_match = re.search(r"Condici[oó]n derivada[^\n]*", content)
    consistency_match = re.search(r"Consistencia checkpoint[^\n]*", content)
    return CheckpointObservation(
        present=True,
        closure_tree=tree_match.group(1) if tree_match else None,
        condition=condition_match.group(0).strip() if condition_match else None,
        consistency_pass=bool(
            consistency_match and "PASS" in consistency_match.group(0)
        ),
    )


# --------------------------------------------------------------------------- #
# The observation
# --------------------------------------------------------------------------- #


@dataclass(frozen=True)
class ChangeObservation:
    """Everything the derivation is allowed to look at. Nothing else is consulted."""

    root: str
    plan: int
    plan_path: str | None
    plan_present: bool
    status: str | None
    change_level: str | None
    rfc: str | None
    entry_criteria: EntryCriteria
    command_set: tuple[tuple[str, ...], ...]
    environmental_classes: tuple[tuple[str, str], ...]
    verification_section_present: bool
    declared_artifacts: tuple[str, ...]
    agent_task: AgentTask
    anchor: AnchorObservation
    checkpoint: CheckpointObservation
    findings: tuple[FindingRecord, ...]
    pending: tuple[PendingRecord, ...]
    index_registered: bool
    git: GitState
    worker_results: tuple[Mapping[str, Any], ...]
    journal_length: int
    journal_gaps: tuple[str, ...]
    gates_run_after_anchor: bool
    gates_run_after_checkpoint: bool
    gates_run_for_current_state: bool
    gates_run_for_current_closure: bool
    validation_done_for_current_state: bool
    revalidation_done_for_current_state: bool
    implementation_done_for_current_state: bool
    #: The plan's authorized work was performed and reported finished. Unlike
    #: ``implementation_done_for_current_state`` this survives a later content
    #: change: the evidence that the work happened does not expire when the
    #: content moves on, and re-running the agent would only repeat itself. A
    #: genuine regression is caught by the plan's own validation, not by
    #: re-delegating blindly.
    implementation_already_satisfied: bool
    last_gate_signals: tuple[str, ...]
    validation_signals: tuple[str, ...]
    gate_signals: Mapping[str, str]
    scope_set: tuple[str, ...]
    current_delta_identity: str | None
    current_state_identity: str | None
    #: ``scope_set`` without the plan artifact — the content whose identity the
    #: validated anchor covers. The plan is the governance *record* of the change
    #: and the host writes into it, so including it would make every recorded
    #: validation change the identity it recorded.
    content_scope_set: tuple[str, ...]
    gaps: tuple[str, ...] = field(default_factory=tuple)

    # -- derived reading helpers ------------------------------------------- #

    @property
    def authorized_for_execution(self) -> bool:
        return self.status in ("Aprobado para ejecución", "Executed") or (
            self.status is not None and self.status.startswith("Executed")
        )

    @property
    def anchor_stale(self) -> bool:
        """A recorded anchor whose validated scope no longer matches the content.

        Unknown current identity is *not* staleness: it is a declared absence
        (``GAP``) and is reported as such, never silently treated as fresh.
        """
        if not self.anchor.present or self.anchor.delta_identity is None:
            return False
        if self.current_delta_identity is None:
            return False
        return self.current_delta_identity != self.anchor.delta_identity

    @property
    def scope_identity_unknown(self) -> bool:
        return self.anchor.present and self.current_delta_identity is None

    @property
    def blocking_pending(self) -> tuple[PendingRecord, ...]:
        return tuple(
            record for record in self.pending if record.blocking and record.unresolved
        )

    @property
    def open_findings(self) -> tuple[FindingRecord, ...]:
        return tuple(
            record
            for record in self.findings
            if record.state in ("open", "partially-resolved")
        )

    def governance_fingerprint(self) -> str:
        """Identity of the *governance-observable* facts (no-progress detection).

        Deliberately excludes the journal itself and timestamps: if an
        executable action produces no change in any of these facts, the loop is
        not progressing and must stop instead of spinning.
        """
        return "|".join(
            (
                str(self.status),
                f"entry={self.entry_criteria.checked}/{self.entry_criteria.total}",
                f"anchor={self.anchor.delta_identity}",
                f"anchor_stale={self.anchor_stale}",
                f"checkpoint={self.checkpoint.closure_tree}",
                f"findings={','.join(sorted(r.ref for r in self.open_findings))}",
                f"pending={','.join(sorted(r.ref for r in self.blocking_pending))}",
                f"gates_current_state={self.gates_run_for_current_state}",
                f"gates_current_closure={self.gates_run_for_current_closure}",
                f"validation_done={self.validation_done_for_current_state}",
                f"git={self.git.head}",
            )
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "root": self.root,
            "plan": self.plan,
            "plan_path": self.plan_path,
            "plan_present": self.plan_present,
            "status": self.status,
            "change_level": self.change_level,
            "rfc": self.rfc,
            "entry_criteria": self.entry_criteria.to_dict(),
            "command_set": [list(argv) for argv in self.command_set],
            "environmental_classes": [list(item) for item in self.environmental_classes],
            "verification_section_present": self.verification_section_present,
            "declared_artifacts": list(self.declared_artifacts),
            "agent_task": self.agent_task.to_dict(),
            "anchor": self.anchor.to_dict(),
            "checkpoint": self.checkpoint.to_dict(),
            "findings": [record.to_dict() for record in self.findings],
            "pending": [record.to_dict() for record in self.pending],
            "index_registered": self.index_registered,
            "git": self.git.to_dict(),
            "worker_results": [dict(item) for item in self.worker_results],
            "journal_length": self.journal_length,
            "journal_gaps": list(self.journal_gaps),
            "gates_run_after_anchor": self.gates_run_after_anchor,
            "gates_run_after_checkpoint": self.gates_run_after_checkpoint,
            "gates_run_for_current_state": self.gates_run_for_current_state,
            "gates_run_for_current_closure": self.gates_run_for_current_closure,
            "validation_done_for_current_state": self.validation_done_for_current_state,
            "revalidation_done_for_current_state": self.revalidation_done_for_current_state,
            "implementation_done_for_current_state": self.implementation_done_for_current_state,
            "implementation_already_satisfied": self.implementation_already_satisfied,
            "last_gate_signals": list(self.last_gate_signals),
            "validation_signals": list(self.validation_signals),
            "gate_signals": dict(self.gate_signals),
            "scope_set": list(self.scope_set),
            "content_scope_set": list(self.content_scope_set),
            "current_delta_identity": self.current_delta_identity,
            "current_state_identity": self.current_state_identity,
            "gaps": list(self.gaps),
        }


def observe(
    root: str | Path,
    plan: int,
    store: OrchestratorStore | None = None,
) -> ChangeObservation:
    """Observe the change and the repository state. Read-only, no inference."""
    root_path = Path(root).resolve()
    store = store or OrchestratorStore(root_path)
    git = git_state(root_path)

    plan_path = find_plan_path(root_path, plan)
    text = ""
    if plan_path is not None:
        try:
            text = plan_path.read_text(encoding="utf-8", errors="replace")
        except OSError as exc:  # pragma: no cover - defensive
            raise ObservationError(f"cannot read plan artifact: {exc}") from exc

    status_match = _STATUS_RE.search(text)
    level_match = _LEVEL_RE.search(text)
    rfc_match = _RFC_RE.search(text)
    entry = parse_entry_criteria(text)
    commands = parse_command_set(text)
    environmental = parse_environmental_classes(text)
    artifacts = declared_artifacts(text)
    agent_task = parse_agent_task(text)
    anchor = parse_anchor(text)
    checkpoint = parse_checkpoint(text)
    findings = parse_findings(text)
    pending = parse_pending(text)

    index_registered = False
    if plan_path is not None:
        try:
            index_registered = plan_path.name in (
                (root_path / PLANS_INDEX).read_text(encoding="utf-8", errors="replace")
            )
        except OSError:
            index_registered = False

    scope_set = tuple(anchor.scope_set) or artifacts
    if plan_path is not None:
        plan_rel = plan_path.relative_to(root_path).as_posix()
        if plan_rel not in scope_set:
            scope_set = scope_set + (plan_rel,)
    # The observed scope is the recorded scope plus every declared deliverable
    # that exists: a deliverable outside the validated scope is a content change
    # the recorded validation does not cover, and it must be observable as such.
    for path in artifacts:
        if path not in scope_set:
            scope_set = scope_set + (path,)
    # The identity covers content that exists at observation time; a declared
    # but absent path is reported as a gap above and never fabricated here.
    scope_set = tuple(
        sorted(path for path in scope_set if (root_path / path).is_file())
    )
    # The plan artifact is the *governance record* of the change, and the host
    # itself writes into it while conducting (anchor, checkpoint, execution note).
    # Letting it participate in the content identity would be self-referential:
    # recording a validation would change the very identity that validation just
    # recorded, the anchor would read as stale for ever and the loop would
    # re-derive a revalidation it had already registered. Plan 122 hit this class
    # of defect (`<PLAN-122>:F-1`); here it is closed at the source by excluding
    # the governance artifact from the validated content identity. It stays in
    # `scope_set`, so it still counts for `Committed` and for the scope of a
    # delegation.
    content_scope_set = tuple(
        path
        for path in scope_set
        if plan_path is None
        or path != plan_path.relative_to(root_path).as_posix()
    )
    identity = (
        scoped_content_identity(root_path, content_scope_set)
        if content_scope_set
        else None
    )
    current_delta = None
    current_tree = None
    if identity is not None:
        current_delta = identity.get("delta_scoped_identity")
        state = identity.get("state_identity") or {}
        current_tree = state.get("tree")

    journal_read = store.read_journal_with_gaps(plan)
    journal = list(journal_read.records)
    results = [result.to_dict() for result in store.list_worker_results(plan)]

    # Real signals of the last executed validation and of the last gate run.
    # Computed from the persisted worker results, never from an exit code.
    validation_signals: tuple[str, ...] = ()
    gate_signals: dict[str, str] = {}
    for item in results:
        delegation = item.get("delegation_received") or {}
        action = delegation.get("action")
        signals = tuple(
            str(command_result.get("signal"))
            for command_result in (item.get("results") or ())
        )
        if action in ("RUN_VALIDATION", "RUN_REVALIDATION"):
            validation_signals = signals
        elif action == "RUN_LIFECYCLE_GATES":
            for command_result in item.get("results") or ():
                label = str(command_result.get("label") or "")
                if label in ("C-1", "C-2", "C-3"):
                    gate_signals[label] = str(command_result.get("signal"))

    gates_after_anchor = False
    gates_after_checkpoint = False
    gates_for_current_state = False
    gates_for_current_closure = False
    last_gate_signals: tuple[str, ...] = ()
    validation_done = False
    revalidation_done = False
    implementation_done = False
    implementation_satisfied = False
    for record in journal:
        if record.get("action") == "RUN_LIFECYCLE_GATES":
            observed = record.get("observed") or {}
            if observed.get("anchor_present"):
                gates_after_anchor = True
            if observed.get("checkpoint_present"):
                gates_after_checkpoint = True
            # ``journal`` comes from disk, so a value is only known to be JSON
            # until it is checked. The declared type of ``last_gate_signals`` is
            # kept honest by narrowing into a separate local, never by trusting
            # whatever the last readable journal line happened to hold.
            recorded_signals = record.get("gate_signals")
            if isinstance(recorded_signals, list):
                last_gate_signals = tuple(str(item) for item in recorded_signals)
            same_state = observed.get("current_delta_identity") == current_delta
            if same_state and observed.get("anchor_present"):
                gates_for_current_state = True
            if (
                same_state
                and observed.get("checkpoint_present")
                and observed.get("checkpoint_tree") is not None
                and observed.get("checkpoint_tree") == current_tree
            ):
                gates_for_current_closure = True
        elif record.get("action") in ("RUN_VALIDATION", "RUN_REVALIDATION"):
            observed = record.get("observed") or {}
            if observed.get("current_delta_identity") == current_delta:
                validation_done = True
                if record.get("action") == "RUN_REVALIDATION":
                    revalidation_done = True
        elif record.get("action") == "RUN_IMPLEMENTATION_TASK":
            observed = record.get("observed") or {}
            result_status = record.get("result_status")
            # Same rule as the validation pair: a reading of another state is
            # not evidence about this one.
            if observed.get("current_delta_identity") == current_delta:
                implementation_done = True
                # A finished implementation that changed nothing at this content
                # state changed nothing *because the work is already there*.
                if (
                    result_status == "completed"
                    and not record.get("result_artifacts_modified")
                ):
                    implementation_satisfied = True
            # The evidence is carried forward across content changes: once the
            # plan's authorized work has been performed and reported finished, it
            # is not re-delegated merely because the content moved on. If the work
            # were really missing, the plan's own validation would fail and the
            # loop would stop on evidence instead of re-running the agent.
            if result_status == "completed":
                implementation_satisfied = True

    gaps: list[str] = []
    if plan_path is None:
        gaps.append("plan artifact not found")
    if plan_path is not None and not commands:
        gaps.append("plan declares no validation command-set (## Verificación)")
    if plan_path is not None and not index_registered:
        gaps.append("plan is not registered in docs/plans/INDEX.md")
    if not git.is_repository:
        gaps.append("root is not a git repository")
    missing_artifacts = [
        path for path in artifacts if not (root_path / path).is_file()
    ]
    if missing_artifacts:
        gaps.append(
            "declared deliverable(s) absent: " + ", ".join(sorted(missing_artifacts))
        )
    gaps.extend(journal_read.gap_notes())

    return ChangeObservation(
        root=str(root_path),
        plan=plan,
        plan_path=None if plan_path is None else plan_path.relative_to(root_path).as_posix(),
        plan_present=plan_path is not None,
        status=(status_match.group(1).strip() if status_match else None),
        change_level=(level_match.group(1) if level_match else None),
        rfc=(rfc_match.group(1).strip() if rfc_match else None),
        entry_criteria=entry,
        command_set=commands,
        environmental_classes=environmental,
        verification_section_present=_section(text, "Verificaci", _H2_RE) is not None,
        declared_artifacts=artifacts,
        agent_task=agent_task,
        anchor=anchor,
        checkpoint=checkpoint,
        findings=findings,
        pending=pending,
        index_registered=index_registered,
        git=git,
        worker_results=tuple(results),
        journal_length=len(journal),
        journal_gaps=journal_read.gap_notes(),
        gates_run_after_anchor=gates_after_anchor,
        gates_run_after_checkpoint=gates_after_checkpoint,
        gates_run_for_current_state=gates_for_current_state,
        gates_run_for_current_closure=gates_for_current_closure,
        validation_done_for_current_state=validation_done,
        revalidation_done_for_current_state=revalidation_done,
        implementation_done_for_current_state=implementation_done,
        implementation_already_satisfied=implementation_satisfied,
        last_gate_signals=last_gate_signals,
        validation_signals=validation_signals,
        gate_signals=dict(gate_signals),
        scope_set=tuple(sorted(scope_set)),
        content_scope_set=content_scope_set,
        current_delta_identity=current_delta,
        current_state_identity=current_tree,
        gaps=tuple(gaps),
    )
