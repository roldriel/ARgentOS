"""Mechanical, section-scoped, idempotent records for the authorized plan (plan 122 §14).

The host records evidence; it never decides. This module is the only place where
the orchestrator writes into a governance artifact, and it is deliberately
narrow:

- it only ever writes to the **plan artifact of the authorized plan**;
- it only writes the record containers the plan template already owns
  (``**Status:**``, ``## Validation anchor``, ``## Checkpoint / cierre``,
  ``## Nota de ejecución``, ``### Findings``);
- every write requires an ``AuthorityDecision`` whose verdict is
  ``AUTHORIZED_EXISTING`` — an unauthorized write raises instead of happening;
- every write is a pure replacement (or a marker-guarded append), so applying the
  same record twice leaves the artifact identical;
- it never resolves a finding, never approves anything, never publishes, never
  touches ``protocol/.agents/``, ``dist/`` or an artifact of another plan.

The record bodies are derived from observations that really happened (command
outputs, Scoped Content Identity, Git state). Nothing here invents evidence.
"""

from __future__ import annotations

import os
import re
import tempfile
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable, Mapping, Sequence

from .contracts import AUTHORIZED_EXISTING, AuthorityDecision

_H2_RE = re.compile(r"^##\s+(.+?)\s*$", re.MULTILINE)
_H3_RE = re.compile(r"^###\s+(.+?)\s*$", re.MULTILINE)
_STATUS_LINE_RE = re.compile(r"^\*\*Status:\*\*.*$", re.MULTILINE)


class GovernanceError(RuntimeError):
    """The record could not be written under the declared authority."""


def _require_authorized(decision: AuthorityDecision, what: str) -> None:
    if decision.verdict != AUTHORIZED_EXISTING:
        raise GovernanceError(
            f"refusing to write {what}: authority verdict is {decision.verdict} "
            f"({decision.reason})"
        )


# --------------------------------------------------------------------------- #
# Section-scoped text editing (pure functions: text in, text out)
# --------------------------------------------------------------------------- #


def _find_section(
    text: str, prefix: str, pattern: re.Pattern[str]
) -> tuple[int, int] | None:
    matches = list(pattern.finditer(text))
    for index, match in enumerate(matches):
        if match.group(1).strip().casefold().startswith(prefix.casefold()):
            end = matches[index + 1].start() if index + 1 < len(matches) else len(text)
            return match.end(), end
    return None


def write_section_body(text: str, prefix: str, body: str) -> str:
    """Replace the body of a section, preserving a trailing ``---`` separator."""
    found = _find_section(text, prefix, _H2_RE) or _find_section(text, prefix, _H3_RE)
    if found is None:
        raise GovernanceError(f"section not found: {prefix}")
    start, end = found
    original = text[start:end]
    separator = "\n---\n" if original.rstrip().endswith("---") else ""
    return text[:start] + "\n" + body.strip("\n") + "\n" + separator + "\n" + text[end:]


def set_status(text: str, status: str) -> str:
    """Replace the plan's ``**Status:**`` line (idempotent)."""
    if not _STATUS_LINE_RE.search(text):
        raise GovernanceError("plan artifact has no **Status:** line")
    return _STATUS_LINE_RE.sub(f"**Status:** {status}", text, count=1)


def append_marked_block(text: str, marker: str, block: str) -> str:
    """Append a marker-guarded block; a second call is a no-op (idempotent)."""
    if marker in text:
        return text
    return text.rstrip("\n") + "\n\n" + marker + "\n" + block.strip("\n") + "\n"


def _write_atomic(path: Path, text: str) -> None:
    fd, tmp_name = tempfile.mkstemp(
        dir=str(path.parent), prefix=path.name + ".", suffix=".tmp"
    )
    try:
        with os.fdopen(fd, "w", encoding="utf-8", newline="\n") as handle:
            handle.write(text)
        os.replace(tmp_name, path)
    except BaseException:
        try:
            os.unlink(tmp_name)
        except OSError:
            pass
        raise


# --------------------------------------------------------------------------- #
# Record bodies (derived, never invented)
# --------------------------------------------------------------------------- #


def _fmt_commands(commands: Sequence[Sequence[str]]) -> str:
    return "; ".join("`" + " ".join(argv) + "`" for argv in commands)


def build_anchor_body(
    *,
    run_id: str,
    iteration: int,
    plan: int,
    change_description: str,
    scope: Sequence[str],
    commands: Sequence[Sequence[str]],
    delta_identity: str | None,
    state_identity: str | None,
    environmental: Sequence[tuple[str, str]],
    gaps: Sequence[str],
    validation_summary: str,
) -> str:
    """The v1 Validation Anchor body (fields of ``.agents/policies/validation-closure.md`` §1).

    The plan identity is a parameter, never a constant: an anchor that describes
    itself as another plan's change is a false record, and a record that names the
    wrong change cannot be the evidence it claims to be.
    """
    scope_list = ", ".join("`" + path + "`" for path in scope)
    dependencies = "`git` (identidad de contenido y estado), `python` (intérprete de los checkers y de la suite); el resto no instrumentado"
    if environmental:
        env_text = "; ".join(
            f"clase ambiental declarada para `{prefix}`: {declaration}"
            for prefix, declaration in environmental
        )
    else:
        env_text = "sin factores ambientales declarados"
    if gaps:
        env_text += " | GAP declarados: " + "; ".join(gaps)
    delta = delta_identity or "no disponible (GAP declarado, no se fabrica identidad)"
    tree = state_identity or "no disponible (GAP declarado, no se fabrica identidad)"
    return f"""*Validación A1 — registrada al ejecutar por el DEV Autonomous Orchestrator (run `{run_id}`, iteración {iteration}; VC-1, Incremento 1).*

- **Declared scope:** el cambio del Plan {plan}{change_description}: {scope_list}
- **Validation command-set:** {_fmt_commands(commands)}
- **Effective inputs (repo content):** el scope declarado ({len(scope)} paths) más el artifact del Plan y `docs/plans/INDEX.md` consumidos por los checkers.
- **Observed dependencies:** {dependencies}
- **Environmental factors:** {env_text}
- **Scoped Content Identity:**
  - **State identity (estado validado = árbol de cierre):** T1 = `{tree}`.
  - **Delta scoped identity (scope S = los {len(scope)} paths del cambio, ordenados; serialización `scoped-v1`):** `{delta}`.
  - **Scope set (repo-relative paths, ordenados; reconstruible desde este artifact):** {scope_list}
- **Validity / stale:** `vigente` (validación sobre el estado de contenido observado; el cierre se apoya en el Checkpoint).

*Resultado real de la ejecución:* {validation_summary}
"""


def build_checkpoint_body(
    *,
    run_id: str,
    iteration: int,
    anchor_label: str,
    delta_identity: str | None,
    state_identity: str | None,
    governance: Sequence[str],
    condition: str,
) -> str:
    """The GC-1 checkpoint body (fields of ``.agents/policies/validation-closure.md`` §5).

    ``anchor_label`` names the anchor whose validated state the closure
    corresponds to. It is a parameter because the applicable anchor may be a
    revalidation (A2) rather than the original A1, and a checkpoint that names the
    wrong anchor describes a relation that does not hold.
    """
    delta = delta_identity or "no disponible"
    tree = state_identity or "no disponible"
    governance_text = "; ".join(governance) if governance else "sin registros adicionales"
    return f"""*Registrado al ejecutar por el DEV Autonomous Orchestrator (run `{run_id}`, iteración {iteration}; GC-1, Incremento 3).*

- **Commits de cierre:** pendiente — el commit atómico en `dev` es la acción del mantenedor y el host no la ejecuta (`Committed` es estado del repositorio, no un status).
- **Estado validado (ref al Validation anchor):** {anchor_label}, delta `{delta}`, tree `{tree}`.
- **Estado de cierre (tree id):** `{tree}`.
- **Consistencia checkpoint↔anchor:** PASS — el estado de cierre es el estado validado por el anchor aplicable (mismo delta y mismo tree id); la consistencia se verificó con C-2.
- **Governance aplicada:** {governance_text}.
- **Condición derivada:** {condition}
"""


def build_finding_record(
    *,
    plan: int,
    index: int,
    observation: str,
    evidence: str,
    git_state: str,
    provenance: str,
) -> str:
    """One LC-1 finding record with its four immutable element labels.

    The record is registered ``open``: the host detects and records, and never
    resolves (resolution is a human decision with evidence).
    """
    ref = f"PLAN-{plan}:F-{index:02d}"
    return (
        f"- `{ref}` — estado: open; observación: {observation}; "
        f"evidencia original: {evidence}; estado Git observado: {git_state}; "
        f"provenance original: {provenance}"
    )


def write_finding(
    *,
    decision: AuthorityDecision,
    plan_path: Path,
    record: str,
) -> bool:
    """Register one open finding in ``### Findings``. Returns True when written.

    Idempotent: an identical record already present is not duplicated.
    """
    _require_authorized(decision, "a finding record")
    text = plan_path.read_text(encoding="utf-8")
    if record.strip() in text:
        return False
    found = _find_section(text, "Findings", _H3_RE)
    if found is None:
        raise GovernanceError("plan artifact has no ### Findings container")
    start, end = found
    body = text[start:end]
    body = re.sub(r"<!--.*?-->", "", body, flags=re.DOTALL).strip()
    if body.startswith("N/A") or body.startswith("No findings"):
        body = ""
    new_body = (body + "\n" + record).strip("\n")
    updated = text[:start] + "\n" + new_body + "\n\n" + text[end:]
    _write_atomic(plan_path, updated)
    return True


# --------------------------------------------------------------------------- #
# High-level record application
# --------------------------------------------------------------------------- #


def build_revalidation_pair(
    *,
    run_id: str,
    iteration: int,
    state_identity: str | None,
    delta_identity: str | None,
) -> str:
    """The A2 identity pair, appended to the anchor without mutating A1.

    A2 is its own registered validation with its own anchor on the new state; it
    references A1 as lineage origin and never replaces, mutates or reinterprets
    it (``.agents/policies/validation-closure.md`` §3).
    """
    tree = state_identity or "no disponible (GAP declarado)"
    delta = delta_identity or "no disponible (GAP declarado)"
    return (
        f"  - **State identity (A2, estado revalidado; run `{run_id}`, "
        f"iteración {iteration}):** T2 = `{tree}`.\n"
        f"  - **Delta scoped identity (A2, estado revalidado; run `{run_id}`, "
        f"iteración {iteration}):** `{delta}`.\n"
        f"  - **Revalidación (A2 de A1, run `{run_id}`, iteración {iteration}):** "
        "el mismo contrato se re-ejecutó sobre el estado nuevo; A1 permanece como "
        "registro histórico y no se muta ni se reinterpreta."
    )


_VALIDITY_FIELD_RE = re.compile(
    r"^([ \t]*-[ \t]*\*{0,2}Validity\s*/\s*stale\*{0,2}\s*:\s*).*$", re.MULTILINE
)


_SCOPE_SET_LINE_RE = re.compile(
    r"^([ \t]*-[ \t]*\*{0,2}Scope set[^\n]*?:\*{0,2}[ \t]*).*$", re.MULTILINE
)


_DELTA_ID_RE = re.compile(r"\b([0-9a-f]{64})\b")


def _applicable_delta_identity(text: str) -> str | None:
    """The last registered delta identity of the validation anchor, or None.

    The applicable identity is the most recently registered one: A1 stays as
    history and a revalidation (A2) never replaces it, so "the identity in
    effect" is the final entry.
    """
    anchor = _find_section(text, "Validation anchor", _H2_RE)
    if anchor is None:
        return None
    start, end = anchor
    deltas: list[str] = []
    for match in re.finditer(
        r"^[ \t]*-[ \t]*\*{0,2}Delta scoped identity[^\n]*$", text[start:end], re.MULTILINE
    ):
        found = _DELTA_ID_RE.search(match.group(0))
        if found:
            deltas.append(found.group(1))
    return deltas[-1] if deltas else None


def record_revalidation(
    *,
    decision: AuthorityDecision,
    plan_path: Path,
    pair: str,
    state_identity: str | None,
    delta_identity: str | None,
    scope: Sequence[str],
    run_id: str,
    iteration: int,
) -> bool:
    """Append the A2 identity pair inside ``Scoped Content Identity``.

    The ``Validity / stale`` field is updated to declare the revalidation (A2
    references A1) and the declared scope set is extended to the scope the
    revalidation really covered; A1's identity values are never mutated.
    Idempotent by state identity: re-applying the same revalidation does not
    duplicate the pair. Returns True when the artifact changed.
    """
    _require_authorized(decision, "a revalidation record")
    text = plan_path.read_text(encoding="utf-8")
    # The applicable identity is the *last* registered one (A1 is history and is
    # never mutated). The check must ask whether a revalidation for **this**
    # content state was already registered, never whether the identity appears
    # anywhere in the artifact: a vacuous containment test would suppress a
    # revalidation that is still needed and the loop would re-derive it forever.
    if delta_identity and _applicable_delta_identity(text) == delta_identity:
        return False
    anchor = _find_section(text, "Validation anchor", _H2_RE)
    if anchor is None:
        raise GovernanceError("plan artifact has no ## Validation anchor section")
    start, end = anchor
    body = text[start:end]
    deltas = list(
        re.finditer(
            r"^[ \t]*-[ \t]*\*{0,2}Delta scoped identity[^\n]*$", body, re.MULTILINE
        )
    )
    if not deltas:
        raise GovernanceError("anchor has no Delta scoped identity subfield to extend")
    insert_at = start + deltas[-1].end()
    updated = text[:insert_at] + "\n" + pair.rstrip("\n") + text[insert_at:]
    validity = (
        f"revalidada — A1 permanece como registro histórico (no se muta ni se "
        f"reinterpreta); A2 re-ejecutó el mismo contrato sobre el estado nuevo "
        f"(run `{run_id}`, iteración {iteration})"
    )
    updated = _VALIDITY_FIELD_RE.sub(
        lambda match: match.group(1) + validity, updated, count=1
    )
    if scope:
        scope_list = ", ".join("`" + path + "`" for path in scope)
        _require_authorized(decision, "the declared scope set")
        updated = _SCOPE_SET_LINE_RE.sub(
            lambda match: match.group(1) + scope_list, updated, count=1
        )
    _write_atomic(plan_path, updated)
    return True


def record_validation_anchor(
    *,
    decision: AuthorityDecision,
    plan_path: Path,
    body: str,
) -> None:
    _require_authorized(decision, "the validation anchor")
    text = plan_path.read_text(encoding="utf-8")
    _write_atomic(plan_path, write_section_body(text, "Validation anchor", body))


def record_checkpoint(
    *,
    decision: AuthorityDecision,
    plan_path: Path,
    body: str,
) -> None:
    _require_authorized(decision, "the checkpoint")
    text = plan_path.read_text(encoding="utf-8")
    _write_atomic(plan_path, write_section_body(text, "Checkpoint", body))


def record_plan_status(
    *,
    decision: AuthorityDecision,
    plan_path: Path,
    status: str,
) -> None:
    _require_authorized(decision, "the plan status")
    text = plan_path.read_text(encoding="utf-8")
    _write_atomic(plan_path, set_status(text, status))


def record_run_note(
    *,
    decision: AuthorityDecision,
    plan_path: Path,
    run_id: str,
    block: str,
) -> None:
    _require_authorized(decision, "the execution note")
    text = plan_path.read_text(encoding="utf-8")
    marker = f"<!-- orchestrator-run: {run_id} -->"
    _write_atomic(plan_path, append_marked_block(text, marker, block))
