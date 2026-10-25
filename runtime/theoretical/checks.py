"""Deterministic checks CH-1…CH-9 of Theoretical Execution.

Every check is a read-only function of the proposal and the **factual base
commit**.  It returns an explicit signal from the repository's failure
vocabulary (``VALID``/``ANOMALY``/``BOUNDARY``/``GAP``/``N/A``) plus the
evidence it used.  A check never decides semantics and never completes missing
information.

Determinism boundary: a check does not read the working tree or the index.  A
citation, an artifact status or a scope identity is answered from the base
commit, so two runs over the same ``InputIdentity`` produce the same signals
even when the working tree is dirty or the index holds staged changes.
"""

from __future__ import annotations

import importlib
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Mapping

from .overlay import GitRepository, normalize_path
from .proposal import Proposal

VALID = "VALID"
ANOMALY = "ANOMALY"
BOUNDARY = "BOUNDARY"
GAP = "GAP"
NOT_APPLICABLE = "N/A"

_CHECK_IDS = tuple(f"CH-{index}" for index in range(1, 10))
_STATUS_RE = re.compile(r"^\*\*Status:\*\*\s*(.+?)\s*$", re.MULTILINE)
_CHECKER_PATHS = ("docs/plans/", "docs/rfc/", "docs/adr/")
_PAYLOAD_PREFIXES = ("protocol/.agents/",)
_PAYLOAD_FILES = ("protocol/_AGENTS.md",)


def _load_tool(name: str):
    tools = Path(__file__).resolve().parents[2] / "tools"
    if str(tools) not in sys.path:
        sys.path.insert(0, str(tools))
    return importlib.import_module(name)


@dataclass(frozen=True)
class CheckResult:
    """One check's outcome and the evidence behind it."""

    check: str
    signal: str
    statement: str
    evidence_refs: tuple[str, ...] = ()
    obligation: Mapping[str, Any] | None = None


def _obligation(
    statement: str,
    *,
    candidate: str,
    falsified_if: str,
    depends_on: tuple[str, ...] = (),
) -> Mapping[str, Any]:
    return {
        "statement": statement,
        "falsified_if": falsified_if,
        "candidate": candidate,
        "depends_on": list(depends_on),
    }


_ANCHOR_HEADING_RE = re.compile(r"^##\s+Validation anchor\s*$", re.MULTILINE)
_ANCHOR_SCOPE_RE = re.compile(r"^\s*[-*]\s*\**Scope set[^\n]*$", re.MULTILINE)
_BACKTICK_RE = re.compile(r"`([^`]+)`")


def _anchor_scope(proposal: Proposal) -> tuple[str, ...]:
    """The anchor's declared scope set, including root-level files.

    ``parse_anchor`` only accepts tokens with a slash, so a root file such as
    ``CHANGELOG.md`` would silently disappear from the measured scope.  TE
    reads the bullet itself and normalizes every backticked path.
    """
    heading = _ANCHOR_HEADING_RE.search(proposal.text)
    if heading is None:
        return proposal.anchor.scope_set
    rest = proposal.text[heading.end() :]
    next_heading = re.search(r"^##\s+", rest, re.MULTILINE)
    section = rest[: next_heading.start()] if next_heading else rest
    line = _ANCHOR_SCOPE_RE.search(section)
    if line is None:
        return proposal.anchor.scope_set
    found: list[str] = []
    for token in _BACKTICK_RE.findall(line.group(0)):
        try:
            path = normalize_path(token)
        except ValueError:
            continue
        if path not in found:
            found.append(path)
    return tuple(found) or proposal.anchor.scope_set


def _payload_paths(proposal: Proposal) -> tuple[str, ...]:
    return tuple(
        path
        for path in proposal.deliverables
        if path in _PAYLOAD_FILES or path.startswith(_PAYLOAD_PREFIXES)
    )


def _classes(proposal: Proposal) -> tuple[str, ...]:
    return tuple(
        token.strip()
        for token in re.split(r",", proposal.rfc56_class or "")
        if token.strip()
    )


def _base_text(proposal: Proposal, path: str) -> str | None:
    """Text of ``path`` at the base commit; never the working tree."""
    try:
        rel = normalize_path(path)
    except ValueError:
        return None
    return proposal.overlay.repository.read_text(proposal.base.commit, rel)


def _artifact_status(proposal: Proposal, path: str) -> str | None:
    """``**Status:**`` of a governed artifact read at the base commit."""
    if not path.startswith(_CHECKER_PATHS):
        return None
    text = _base_text(proposal, path)
    if text is None:
        return None
    match = _STATUS_RE.search(text)
    if not match:
        return None
    return match.group(1).strip().split("(")[0].strip()


def _citation_at_base(
    proposal: Proposal, tool, citation
) -> tuple[str | None, str | None]:
    """Resolve a citation path through the base tree.

    The legacy mapping of ``tools/legacy_paths.py`` applies exactly as in the
    repository citation checker, but every candidate is resolved against the
    base commit: a legacy path that exists only in the working tree does not
    make a citation resolve.
    """
    candidates = [citation.path]
    mapped = tool.legacy_target(citation.path, proposal.root)
    if mapped is not None:
        try:
            relative = mapped.resolve().relative_to(proposal.root.resolve()).as_posix()
        except (OSError, ValueError):
            relative = None
        if relative and relative not in candidates:
            candidates.append(relative)
    repository = proposal.overlay.repository
    for candidate in candidates:
        try:
            rel = normalize_path(candidate)
        except ValueError:
            continue
        if not repository.exists(proposal.base.commit, rel):
            continue
        text = repository.read_text(proposal.base.commit, rel)
        if text is not None:
            return rel, text
    return None, None


def _ch1(proposal: Proposal) -> list[CheckResult]:
    classes = _classes(proposal)
    payload = _payload_paths(proposal)
    evidence = (f"{proposal.path}:header",)
    if not classes:
        return [
            CheckResult(
                "CH-1",
                BOUNDARY,
                "proposal declares no RFC-56 Class; the payload path set cannot be "
                "classified",
                evidence,
            )
        ]
    if "N/A" in classes:
        if payload:
            return [
                CheckResult(
                    "CH-1",
                    ANOMALY,
                    "RFC-56 Class N/A is incompatible with declared payload paths: "
                    + ", ".join(payload),
                    evidence + payload,
                )
            ]
        return [CheckResult("CH-1", VALID, "no payload paths and Class N/A", evidence)]
    unknown = sorted(set(classes) - {"A", "B", "C"})
    if unknown:
        return [
            CheckResult(
                "CH-1",
                ANOMALY,
                "unknown RFC-56 Class value(s): " + ", ".join(unknown),
                evidence,
            )
        ]
    if not payload:
        return [
            CheckResult(
                "CH-1",
                ANOMALY,
                "a payload class is declared but no declared deliverable touches "
                "protocol/.agents/",
                evidence,
            )
        ]
    return [
        CheckResult(
            "CH-1",
            VALID,
            "payload class and payload paths are coherent",
            evidence + payload,
        )
    ]


def _ch2(proposal: Proposal) -> list[CheckResult]:
    if not proposal.scope_declared:
        return [
            CheckResult(
                "CH-2",
                GAP,
                "no editable Scope is declared; deliverables are used and the "
                "membership check is not evaluable",
                (f"{proposal.path}:Delegación agentiva",),
                _obligation(
                    "declare the editable Scope and re-evaluate containment",
                    candidate="manual_review",
                    falsified_if="the editable Scope is declared and all deliverables "
                    "are members of it",
                ),
            )
        ]
    outside = tuple(
        path for path in proposal.deliverables if path not in proposal.scope
    )
    if outside:
        return [
            CheckResult(
                "CH-2",
                ANOMALY,
                "deliverable(s) outside the declared editable Scope: "
                + ", ".join(outside),
                (
                    f"{proposal.path}:Entregables",
                    f"{proposal.path}:Delegación agentiva",
                ),
            )
        ]
    return [
        CheckResult(
            "CH-2",
            VALID,
            "all deliverables are inside the declared editable Scope",
            (f"{proposal.path}:Delegación agentiva",),
        )
    ]


def _ch3(proposal: Proposal) -> list[CheckResult]:
    tool = _load_tool("check_plan_citations")
    declared = set(proposal.deliverables)
    results: list[CheckResult] = []
    for citation in proposal.citations:
        path = citation.path
        section = citation.section
        ref = f"{path}:{section}" if section else path
        if path in declared:
            results.append(
                CheckResult(
                    "CH-3",
                    GAP,
                    f"citation {ref} points to a path this proposal declares as "
                    "changed; its content is unknown until materialization",
                    (ref,),
                    _obligation(
                        f"verify citation {ref} after materialization",
                        candidate="manual_review",
                        falsified_if="the cited section does not exist after "
                        "materialization",
                    ),
                )
            )
            continue
        status = _artifact_status(proposal, path)
        if status and status.casefold() == "superseded":
            results.append(
                CheckResult(
                    "CH-3",
                    BOUNDARY,
                    f"citation {ref} targets a Superseded artifact; confirm the "
                    "reference is historical or update it",
                    (ref,),
                    _obligation(
                        f"review the Superseded citation {ref}",
                        candidate="manual_review",
                        falsified_if="the citation is explicitly historical or "
                        "points to the current section",
                    ),
                )
            )
            continue
        _resolved, text = _citation_at_base(proposal, tool, citation)
        if text is None:
            results.append(
                CheckResult(
                    "CH-3",
                    ANOMALY,
                    f"broken citation {ref}: file not found at the base commit",
                    (ref,),
                )
            )
            continue
        if not tool.section_exists(citation.section, text):
            results.append(
                CheckResult(
                    "CH-3",
                    ANOMALY,
                    f"broken citation {ref}: section not found at the base commit",
                    (ref,),
                )
            )
            continue
        results.append(
            CheckResult("CH-3", VALID, f"citation {ref} resolves at the base", (ref,))
        )
    if not results:
        results.append(
            CheckResult("CH-3", NOT_APPLICABLE, "proposal declares no citations")
        )
    return results


def _ch4(proposal: Proposal) -> list[CheckResult]:
    tool = _load_tool("check_lifecycle_checkpoint")
    results: list[CheckResult] = []
    for path in proposal.deliverables:
        if not path.startswith(_CHECKER_PATHS):
            continue
        if not proposal.overlay.repository.exists(proposal.base.commit, path):
            continue  # a declared creation is not a write to a closed artifact
        text = _base_text(proposal, path)
        if text is None:
            results.append(
                CheckResult(
                    "CH-4",
                    GAP,
                    f"{path} is declared but unreadable at the base",
                    (path,),
                )
            )
            continue
        base_status = (tool.status_base(text) or "").strip()
        if tool.declares_closed(text):
            results.append(
                CheckResult(
                    "CH-4",
                    ANOMALY,
                    f"{path} is declared as changed but its checkpoint declares Closed",
                    (path,),
                )
            )
            continue
        if base_status in {"Executed", "Accepted"}:
            results.append(
                CheckResult(
                    "CH-4",
                    BOUNDARY,
                    f"{path} is a {base_status} artifact; only an authorized "
                    "append-only region may change",
                    (path,),
                    _obligation(
                        f"confirm that the change to {path} stays in an authorized "
                        "append-only region",
                        candidate="manual_review",
                        falsified_if="the change modifies governing content of the "
                        f"{base_status} artifact",
                    ),
                )
            )
    if not results:
        results.append(
            CheckResult(
                "CH-4",
                NOT_APPLICABLE,
                "no declared deliverable targets a governed plan/RFC/ADR",
            )
        )
    return results


def _ch5(proposal: Proposal) -> list[CheckResult]:
    payload = _payload_paths(proposal)
    if not payload:
        return [
            CheckResult(
                "CH-5",
                NOT_APPLICABLE,
                "no payload paths; payload version/changelog obligations do not apply",
            )
        ]
    declared = set(proposal.deliverables)
    text = proposal.text
    has_version = "protocol/.agents/VERSION" in declared or "VERSION" in text
    has_changelog = "CHANGELOG.md" in declared or "CHANGELOG" in text
    if has_version and has_changelog:
        return [
            CheckResult(
                "CH-5",
                VALID,
                "payload paths and payload version/changelog obligations are declared",
                tuple(payload),
            )
        ]
    return [
        CheckResult(
            "CH-5",
            BOUNDARY,
            "payload paths are declared but the version/changelog obligation is not "
            "explicit",
            tuple(payload),
            _obligation(
                "declare the payload version/changelog obligation or record it as an "
                "environmental/scope exception",
                candidate="manual_review",
                falsified_if="the payload change is released without the required "
                "version/changelog record",
            ),
        )
    ]


def _ch6(proposal: Proposal) -> list[CheckResult]:
    criteria = tuple(item for item in proposal.items if item.kind == "criterion")
    if not criteria:
        return [
            CheckResult(
                "CH-6",
                NOT_APPLICABLE,
                "proposal declares no exit criteria",
            )
        ]
    if not proposal.commands:
        return [
            CheckResult(
                "CH-6",
                BOUNDARY,
                "exit criteria are declared but no verification command-set exists",
                (
                    f"{proposal.path}:Criterios de salida",
                    f"{proposal.path}:Verificación",
                ),
                _obligation(
                    "declare commands or explicit manual verification for the exit "
                    "criteria",
                    candidate="manual_review",
                    falsified_if="every exit criterion has an observable verification "
                    "mechanism",
                ),
            )
        ]
    return [
        CheckResult(
            "CH-6",
            VALID,
            "exit criteria and a verification command-set are declared; adequacy is "
            "evaluated by the producer",
            (f"{proposal.path}:Verificación",),
        )
    ]


def _ch7(proposal: Proposal) -> list[CheckResult]:
    anchor = proposal.anchor
    if not anchor.present or not (anchor.state_identity or anchor.delta_identity):
        return [
            CheckResult(
                "CH-7",
                NOT_APPLICABLE,
                "no declared Validation Anchor identity in the proposal",
            )
        ]
    scope = _anchor_scope(proposal)
    if not scope:
        return [
            CheckResult(
                "CH-7",
                GAP,
                "a Validation Anchor identity is declared but its Scope set is absent",
                (f"{proposal.path}:Validation anchor",),
            )
        ]
    tool = _load_tool("scoped_content_identity")
    try:
        report = tool.compute(
            proposal.root,
            list(scope),
            ref=proposal.base.commit,
            content_ref=proposal.base.commit,
        )
    except Exception as exc:  # noqa: BLE001 - the generator fails closed
        return [
            CheckResult(
                "CH-7",
                GAP,
                f"declared anchor identity cannot be recomposed: {exc}",
                (f"{proposal.path}:Validation anchor",),
            )
        ]
    delta = report.get("delta_scoped_identity")
    if anchor.delta_identity and delta != anchor.delta_identity:
        return [
            CheckResult(
                "CH-7",
                ANOMALY,
                "declared delta scoped identity does not recompose at the base",
                (f"{proposal.path}:Validation anchor",),
            )
        ]
    if anchor.state_identity:
        object_type = proposal.overlay.repository.object_type(anchor.state_identity)
        if object_type != "tree":
            return [
                CheckResult(
                    "CH-7",
                    ANOMALY,
                    "declared state identity does not resolve to a Git tree",
                    (f"{proposal.path}:Validation anchor",),
                )
            ]
    return [
        CheckResult(
            "CH-7",
            VALID,
            "declared anchor identities recompose at the base",
            (f"{proposal.path}:Validation anchor",),
        )
    ]


def _ch8(proposal: Proposal) -> list[CheckResult]:
    repo = GitRepository(proposal.root)
    if not repo.verify_ref(proposal.base.commit):
        return [
            CheckResult(
                "CH-8",
                GAP,
                "the declared base commit does not resolve",
                (proposal.base.commit,),
            )
        ]
    if repo.blob(proposal.base.commit, proposal.path) is None:
        return [
            CheckResult(
                "CH-8",
                GAP,
                "the proposal is not readable at the declared base commit",
                (f"{proposal.base.commit}:{proposal.path}",),
            )
        ]
    return [
        CheckResult(
            "CH-8",
            VALID,
            "proposal and base commit resolve",
            (proposal.base.commit, proposal.path),
        )
    ]


def _ch9(proposal: Proposal) -> list[CheckResult]:
    """Declaration integrity of the enumerated change model.

    A declared deliverable that cannot be represented is not silently dropped:
    an escaping or non-relative path is present-but-contradictory (``ANOMALY``)
    and a declaration with no resolvable path is missing information (``GAP``
    plus an obligation).  An effect class outside the closed DEV vocabulary is
    ``ANOMALY``: the frontier cannot admit what it cannot classify.
    """
    results: list[CheckResult] = []
    for token in proposal.rejected_paths:
        results.append(
            CheckResult(
                "CH-9",
                ANOMALY,
                "declared deliverable path is not repository-relative and cannot be "
                f"evaluated: {token}",
                (f"{proposal.path}:Entregables",),
            )
        )
    for label in proposal.unresolved_deliverables:
        results.append(
            CheckResult(
                "CH-9",
                GAP,
                "declared deliverable does not resolve to a repository-relative "
                f"path: {label}",
                (f"{proposal.path}:Entregables",),
                _obligation(
                    "declare the deliverable as a repository-relative path",
                    candidate="manual_review",
                    falsified_if="the deliverable entry resolves to an existing or "
                    "declared repository-relative path",
                ),
            )
        )
    vocabulary = _load_tool("check_session_artifacts").EFFECT_KINDS
    unknown = tuple(effect for effect in proposal.effects if effect not in vocabulary)
    if unknown:
        results.append(
            CheckResult(
                "CH-9",
                ANOMALY,
                "declared effect class is outside the closed vocabulary: "
                + ", ".join(unknown),
                (f"{proposal.path}:Efectos declarados",),
            )
        )
    if not results:
        results.append(
            CheckResult(
                "CH-9",
                VALID,
                "every declared deliverable resolves and every effect class belongs "
                "to the closed vocabulary",
                (f"{proposal.path}:Entregables",),
            )
        )
    return results


def run_checks(proposal: Proposal) -> tuple[CheckResult, ...]:
    """Run CH-1…CH-9 in a fixed order; deterministic and read-only."""
    results: list[CheckResult] = []
    for check in (_ch1, _ch2, _ch3, _ch4, _ch5, _ch6, _ch7, _ch8, _ch9):
        results.extend(check(proposal))
    return tuple(results)


def check_ids() -> tuple[str, ...]:
    return _CHECK_IDS


def failed_checks(results: tuple[CheckResult, ...]) -> tuple[CheckResult, ...]:
    return tuple(
        result for result in results if result.signal not in (VALID, NOT_APPLICABLE)
    )
