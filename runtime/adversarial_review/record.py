"""Deterministic validation of a Minimal Adversarial Review (MAR) record.

DEV-only reference runtime, **experimental**: this module belongs to the isolated
``runtime/adversarial_review/`` package, a read-only instrument for a validation
experiment. It is **advisory-only**, **not integrated** in any workflow, host or
payload, and it holds **no authority**: validation reports structural problems in
a review record; it never accepts, rejects, gates or authorizes anything. It
performs no I/O and never mutates its input.

The record is a JSON-shaped dict (design doc §4.4). Every rule is a mechanical
property of that dict:

- the frozen frame and the 1..``MAX_PASSES`` deliberation passes;
- commit-before-reveal declared by hash — the ordering is **recorded, not
  technically enforced**, so the absence of the declaration is a WARNING, never
  a claim of observation;
- finding provenance, vocabulary and materiality consequences;
- a short synthesis that may not introduce material findings and must preserve
  material disagreements;
- an advisory result with no authority, and the structural refusal of
  adjudication fields anywhere in the record;
- the cost budget, delegated to :func:`runtime.adversarial_review.budget.assess_budget`.

Issues are returned sorted by ``(severity, code, message)`` so the same record
always yields byte-identical output.

Provenance: ``docs/working/research/MINIMAL_ADVERSARIAL_REVIEW_DESIGN_2026-10-25.md``
(Working / Research; non-normative).
"""

from __future__ import annotations

import re
from collections.abc import Mapping
from dataclasses import dataclass
from typing import Any, Literal

from .budget import SYNTHESIS_PASS_ID, assess_budget
from .model import (
    AUTHORITY_ADVISORY,
    DIRECTIONS,
    DISAGREEMENT_STATES,
    IMPACTS,
    MATERIALITY,
    MAX_PASSES,
    MAX_PASS_WORDS,
    MAX_SYNTHESIS_WORDS,
    NOVELTY,
    POSTURES,
    RECOMMENDATIONS,
    SCHEMA_VERSION,
    SYNTHESIS_METHOD,
    TRIGGER_RECOMMENDATIONS,
)

#: Sixteen hexadecimal bytes, lowercase: the declared commitment hash.
_COMMITMENT_HASH = re.compile(r"^[0-9a-f]{64}$")

#: Posture -> the only admitted source of its findings.
_POSTURE_SOURCE = {
    "TARGETED_FALSIFICATION": "PASS_FALSIFICATION",
    "STRONGEST_CASE_FOR": "PASS_ADVOCACY",
}

#: Fields the record may never carry: they would express adjudication, which the
#: review does not have. Keys are checked at any depth; values are not.
_FORBIDDEN_AUTHORITY_FIELDS = frozenset(
    {
        "verdict",
        "vote",
        "votes",
        "voting",
        "judge",
        "jury",
        "court",
        "majority",
        "authorization",
        "decision_authority",
    }
)

#: The issue codes this validator can emit (not exhaustive of order; issues are
#: sorted by severity/code/message before being returned).
CODE_SCHEMA_VERSION = "SCHEMA_VERSION"
CODE_FRAME_INCOMPLETE = "FRAME_INCOMPLETE"
CODE_PASS_COUNT = "PASS_COUNT"
CODE_PASS_POSTURE = "PASS_POSTURE"
CODE_COMMITMENT_MISSING = "COMMITMENT_MISSING"
CODE_COMMIT_ORDER_UNVERIFIED = "COMMIT_ORDER_UNVERIFIED"
CODE_FINDING_ID_DUPLICATE = "FINDING_ID_DUPLICATE"
CODE_FINDING_NO_EVIDENCE = "FINDING_NO_EVIDENCE"
CODE_FINDING_SOURCE_MISMATCH = "FINDING_SOURCE_MISMATCH"
CODE_FINDING_VOCAB = "FINDING_VOCAB"
CODE_FINDING_NO_CRITERION = "FINDING_NO_CRITERION"
CODE_MATERIAL_WITHOUT_CONSEQUENCE = "MATERIAL_WITHOUT_CONSEQUENCE"
CODE_SYNTHESIS_UNKNOWN_FINDING = "SYNTHESIS_UNKNOWN_FINDING"
CODE_SYNTHESIS_NEW_MATERIAL = "SYNTHESIS_NEW_MATERIAL"
CODE_SYNTHESIS_METHOD = "SYNTHESIS_METHOD"
CODE_DISAGREEMENT_NOT_PRESERVED = "DISAGREEMENT_NOT_PRESERVED"
CODE_DISAGREEMENT_STATE = "DISAGREEMENT_STATE"
CODE_ADVISORY_AUTHORITY = "ADVISORY_AUTHORITY"
CODE_FORBIDDEN_AUTHORITY_FIELD = "FORBIDDEN_AUTHORITY_FIELD"
CODE_MISSING_COST = "MISSING_COST"
CODE_PASS_CAP_EXCEEDED = "PASS_CAP_EXCEEDED"
CODE_COST_OVER_TARGET = "COST_OVER_TARGET"

Severity = Literal["ERROR", "WARNING"]


@dataclass(frozen=True)
class Issue:
    """One structural problem of a review record."""

    severity: Severity
    code: str
    message: str

    def to_dict(self) -> dict[str, str]:
        """JSON-shaped representation, used by the read-only CLI."""
        return {"severity": self.severity, "code": self.code, "message": self.message}


def _mapping(value: Any) -> Mapping[str, Any]:
    return value if isinstance(value, Mapping) else {}


def _items(value: Any) -> tuple[Any, ...]:
    return tuple(value) if isinstance(value, (list, tuple)) else ()


def _non_empty_text(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def _non_empty_text_list(value: Any) -> bool:
    return (
        isinstance(value, (list, tuple))
        and bool(value)
        and all(_non_empty_text(item) for item in value)
    )


def _non_empty_list(value: Any) -> bool:
    return isinstance(value, (list, tuple)) and bool(value)


def _pass_label(pass_map: Mapping[str, Any], index: int) -> str:
    pass_id = pass_map.get("pass_id")
    return repr(pass_id) if _non_empty_text(pass_id) else f"#{index + 1}"


def _finding_label(finding: Mapping[str, Any]) -> str:
    finding_id = finding.get("finding_id")
    return repr(finding_id) if _non_empty_text(finding_id) else "an unnamed finding"


def _budget_inputs(
    record: Mapping[str, Any],
) -> tuple[list[dict[str, Any]], Mapping[str, Any]]:
    """Build the budget entries a record declares.

    One entry per deliberation pass plus the synthetic synthesis entry when the
    record has a synthesis. Shared with ``metrics.review_metrics`` so both always
    assess the same declared cost.
    """
    entries: list[dict[str, Any]] = []
    for raw_pass in _items(record.get("passes")):
        pass_map = _mapping(raw_pass)
        entries.append({"pass_id": pass_map.get("pass_id"), "cost": pass_map.get("cost", {})})
    synthesis = record.get("synthesis")
    if isinstance(synthesis, Mapping):
        entries.append({"pass_id": SYNTHESIS_PASS_ID, "cost": synthesis.get("cost", {})})
    return entries, _mapping(record.get("cost"))


def _issue(severity: Severity, code: str, message: str) -> Issue:
    return Issue(severity=severity, code=code, message=message)


def _validate_frame(record: Mapping[str, Any]) -> list[Issue]:
    frame = record.get("frame")
    frame_map = _mapping(frame)
    problems: list[str] = []
    if not isinstance(frame, Mapping):
        problems.append("frame must be a JSON object")
    if not _non_empty_text(frame_map.get("question_ref")):
        problems.append("question_ref must be a non-empty string")
    if not _non_empty_text(frame_map.get("candidate")):
        problems.append("candidate must be a non-empty string")
    if not _non_empty_text_list(frame_map.get("criteria")):
        problems.append("criteria must be a non-empty list of non-empty strings")
    if not _non_empty_list(frame_map.get("evidence_refs")):
        problems.append("evidence_refs must be a non-empty list")
    if frame_map.get("mode") != "viability":
        problems.append('mode must be "viability"')
    if not _non_empty_text(frame_map.get("declared_invocation_reason")):
        problems.append("declared_invocation_reason must be a non-empty string")
    if not _non_empty_text(frame_map.get("declared_by")):
        problems.append("declared_by must be a non-empty string")
    if frame_map.get("trigger_recommendation") not in TRIGGER_RECOMMENDATIONS:
        problems.append(
            "trigger_recommendation must be one of "
            + ", ".join(sorted(TRIGGER_RECOMMENDATIONS))
        )
    if not problems:
        return []
    return [
        _issue(
            "ERROR",
            CODE_FRAME_INCOMPLETE,
            "the frozen frame is incomplete: " + "; ".join(problems),
        )
    ]


def _validate_pass_count(record: Mapping[str, Any]) -> tuple[list[Issue], tuple[Any, ...]]:
    raw_passes = record.get("passes")
    if not isinstance(raw_passes, (list, tuple)):
        return (
            [
                _issue(
                    "ERROR",
                    CODE_PASS_COUNT,
                    "passes must be a list of pass objects",
                )
            ],
            (),
        )
    if not 0 < len(raw_passes) <= MAX_PASSES:
        return (
            [
                _issue(
                    "ERROR",
                    CODE_PASS_COUNT,
                    f"passes must contain between 1 and {MAX_PASSES} deliberation "
                    f"passes (found {len(raw_passes)})",
                )
            ],
            tuple(raw_passes),
        )
    return [], tuple(raw_passes)


def _validate_pass_postures(
    passes: tuple[Mapping[str, Any], ...],
) -> list[Issue]:
    issues: list[Issue] = []
    postures = [pass_map.get("posture") for pass_map in passes]
    if postures.count("TARGETED_FALSIFICATION") != 1:
        issues.append(
            _issue(
                "ERROR",
                CODE_PASS_POSTURE,
                "exactly one pass must carry the TARGETED_FALSIFICATION posture "
                f"(found {postures.count('TARGETED_FALSIFICATION')})",
            )
        )
    unknown = [
        _pass_label(pass_map, index)
        for index, pass_map in enumerate(passes)
        if pass_map.get("posture") not in POSTURES
    ]
    if unknown:
        issues.append(
            _issue(
                "ERROR",
                CODE_PASS_POSTURE,
                "every pass posture must be one of "
                + ", ".join(sorted(POSTURES))
                + "; invalid pass(es): "
                + ", ".join(unknown),
            )
        )
    identifiers = [
        pass_map.get("pass_id")
        for pass_map in passes
        if _non_empty_text(pass_map.get("pass_id"))
    ]
    duplicates = sorted(
        {identifier for identifier in identifiers if identifiers.count(identifier) > 1}
    )
    if duplicates:
        issues.append(
            _issue(
                "ERROR",
                CODE_PASS_POSTURE,
                "pass_id must be unique; duplicated: " + ", ".join(map(repr, duplicates)),
            )
        )
    known_postures = [posture for posture in postures if posture in POSTURES]
    repeated = sorted(
        {posture for posture in known_postures if known_postures.count(posture) > 1}
    )
    if repeated:
        issues.append(
            _issue(
                "ERROR",
                CODE_PASS_POSTURE,
                "each posture may be used by at most one pass; repeated: "
                + ", ".join(repeated),
            )
        )
    return issues


def _validate_commitments(passes: tuple[Mapping[str, Any], ...]) -> list[Issue]:
    issues: list[Issue] = []
    for index, pass_map in enumerate(passes):
        problems: list[str] = []
        commitment_hash = pass_map.get("commitment_hash")
        if not (
            isinstance(commitment_hash, str)
            and _COMMITMENT_HASH.fullmatch(commitment_hash)
        ):
            problems.append("commitment_hash must be 64 lowercase hex characters")
        if not _non_empty_list(pass_map.get("material_received")):
            problems.append("material_received must be a non-empty list")
        if not isinstance(pass_map.get("withheld_material"), (list, tuple)):
            problems.append("withheld_material must be a list")
        if not _non_empty_text(pass_map.get("evaluation_ref")):
            problems.append("evaluation_ref must be a non-empty string")
        if problems:
            issues.append(
                _issue(
                    "ERROR",
                    CODE_COMMITMENT_MISSING,
                    f"pass {_pass_label(pass_map, index)}: " + "; ".join(problems),
                )
            )
    return issues


def _findings(
    passes: tuple[Mapping[str, Any], ...],
) -> list[tuple[int, Mapping[str, Any], Mapping[str, Any]]]:
    """One ``(pass_index, pass, finding)`` tuple per finding, in record order."""
    collected: list[tuple[int, Mapping[str, Any], Mapping[str, Any]]] = []
    for index, pass_map in enumerate(passes):
        for raw_finding in _items(pass_map.get("findings")):
            if isinstance(raw_finding, Mapping):
                collected.append((index, pass_map, raw_finding))
    return collected


def _finding_identifiers(
    findings: list[tuple[int, Mapping[str, Any], Mapping[str, Any]]],
) -> list[str]:
    identifiers: list[str] = []
    for _, _, finding in findings:
        finding_id = finding.get("finding_id")
        if _non_empty_text(finding_id):
            identifiers.append(finding_id)
    return identifiers


def _validate_findings(
    findings: list[tuple[int, Mapping[str, Any], Mapping[str, Any]]],
) -> list[Issue]:
    issues: list[Issue] = []

    identifiers = _finding_identifiers(findings)
    duplicates = sorted(
        {identifier for identifier in identifiers if identifiers.count(identifier) > 1}
    )
    if duplicates:
        issues.append(
            _issue(
                "ERROR",
                CODE_FINDING_ID_DUPLICATE,
                "finding_id must be unique across all passes; duplicated: "
                + ", ".join(map(repr, duplicates)),
            )
        )

    for _, _, finding in findings:
        label = _finding_label(finding)
        if not _non_empty_list(finding.get("evidence_refs")):
            issues.append(
                _issue(
                    "ERROR",
                    CODE_FINDING_NO_EVIDENCE,
                    f"finding {label} must carry a non-empty evidence_refs list",
                )
            )
        if not _non_empty_text(finding.get("criterion")):
            issues.append(
                _issue(
                    "ERROR",
                    CODE_FINDING_NO_CRITERION,
                    f"finding {label} must carry a non-empty criterion",
                )
            )
        invalid_vocabulary: list[str] = []
        if finding.get("novelty") not in NOVELTY:
            invalid_vocabulary.append("novelty")
        if finding.get("materiality") not in MATERIALITY:
            invalid_vocabulary.append("materiality")
        if finding.get("impact") not in IMPACTS:
            invalid_vocabulary.append("impact")
        if finding.get("direction") not in DIRECTIONS:
            invalid_vocabulary.append("direction")
        if invalid_vocabulary:
            issues.append(
                _issue(
                    "ERROR",
                    CODE_FINDING_VOCAB,
                    f"finding {label} uses an invalid closed vocabulary: "
                    + ", ".join(invalid_vocabulary),
                )
            )
        if finding.get("materiality") == "MATERIAL" and not _non_empty_text(
            finding.get("consequence")
        ):
            issues.append(
                _issue(
                    "ERROR",
                    CODE_MATERIAL_WITHOUT_CONSEQUENCE,
                    f"material finding {label} must declare a non-empty consequence",
                )
            )

    for index, pass_map, finding in findings:
        posture = pass_map.get("posture")
        expected_source = _POSTURE_SOURCE.get(posture)
        if expected_source is None:
            continue
        if finding.get("source") != expected_source:
            issues.append(
                _issue(
                    "ERROR",
                    CODE_FINDING_SOURCE_MISMATCH,
                    f"finding {_finding_label(finding)} in pass "
                    f"{_pass_label(pass_map, index)} must use source "
                    f"{expected_source} for posture {posture}",
                )
            )
    return issues


def _material_disagreement_criteria(
    findings: list[tuple[int, Mapping[str, Any], Mapping[str, Any]]],
) -> list[str]:
    """Criteria with material findings in opposite directions in different passes."""
    directions_by_pass: dict[str, dict[int, set[str]]] = {}
    for index, _, finding in findings:
        if finding.get("materiality") != "MATERIAL":
            continue
        criterion = finding.get("criterion")
        if not _non_empty_text(criterion):
            continue
        direction = finding.get("direction")
        if direction not in DIRECTIONS:
            continue
        directions_by_pass.setdefault(criterion, {}).setdefault(index, set()).add(direction)
    conflicting: list[str] = []
    for criterion, per_pass in directions_by_pass.items():
        supporting = [index for index, dirs in per_pass.items() if "SUPPORTS" in dirs]
        opposing = [index for index, dirs in per_pass.items() if "OPPOSES" in dirs]
        if any(a != b for a in supporting for b in opposing):
            conflicting.append(criterion)
    return sorted(conflicting)


def _validate_synthesis(
    record: Mapping[str, Any],
    existing_finding_ids: set[str],
    conflict_criteria: list[str],
) -> list[Issue]:
    raw_synthesis = record.get("synthesis")
    if not isinstance(raw_synthesis, Mapping):
        return [
            _issue(
                "ERROR",
                CODE_SYNTHESIS_METHOD,
                "synthesis must be a JSON object with method and evaluation_ref",
            )
        ]
    synthesis = raw_synthesis
    issues: list[Issue] = []

    problems: list[str] = []
    if synthesis.get("method") != SYNTHESIS_METHOD:
        problems.append(f"method must be {SYNTHESIS_METHOD}")
    if not _non_empty_text(synthesis.get("evaluation_ref")):
        problems.append("evaluation_ref must be a non-empty string")
    if problems:
        issues.append(
            _issue(
                "ERROR",
                CODE_SYNTHESIS_METHOD,
                "the short synthesis is invalid: " + "; ".join(problems),
            )
        )

    raw_kept = synthesis.get("findings_kept", [])
    if not isinstance(raw_kept, (list, tuple)):
        issues.append(
            _issue(
                "ERROR",
                CODE_SYNTHESIS_UNKNOWN_FINDING,
                "synthesis.findings_kept must be a list of existing finding ids",
            )
        )
    else:
        unknown = sorted(
            {
                kept
                for kept in raw_kept
                if not (isinstance(kept, str) and kept in existing_finding_ids)
            }
        )
        if unknown:
            issues.append(
                _issue(
                    "ERROR",
                    CODE_SYNTHESIS_UNKNOWN_FINDING,
                    "synthesis.findings_kept references findings that do not exist: "
                    + ", ".join(map(repr, unknown)),
                )
            )

    raw_new_material = synthesis.get("new_material_findings", None)
    if not (isinstance(raw_new_material, (list, tuple)) and not raw_new_material):
        issues.append(
            _issue(
                "ERROR",
                CODE_SYNTHESIS_NEW_MATERIAL,
                "synthesis.new_material_findings must be an empty list: the "
                "synthesis may not introduce material findings",
            )
        )

    raw_disagreements = synthesis.get("disagreements", [])
    if not isinstance(raw_disagreements, (list, tuple)):
        issues.append(
            _issue(
                "ERROR",
                CODE_DISAGREEMENT_STATE,
                "synthesis.disagreements must be a list",
            )
        )
        raw_disagreements = ()

    preserved: set[str] = set()
    for position, raw_disagreement in enumerate(_items(raw_disagreements)):
        disagreement = _mapping(raw_disagreement)
        state = disagreement.get("state")
        problems = []
        if state not in DISAGREEMENT_STATES:
            problems.append(
                "state must be one of " + ", ".join(sorted(DISAGREEMENT_STATES))
            )
        if not _non_empty_text(disagreement.get("criterion")):
            problems.append("criterion must be a non-empty string")
        if problems:
            issues.append(
                _issue(
                    "ERROR",
                    CODE_DISAGREEMENT_STATE,
                    f"synthesis disagreement #{position + 1}: " + "; ".join(problems),
                )
            )
        if state in {"PARTIAL_AGREEMENT", "UNRESOLVED_DISAGREEMENT"} and _non_empty_text(
            disagreement.get("criterion")
        ):
            preserved.add(disagreement["criterion"])

    missing = [criterion for criterion in conflict_criteria if criterion not in preserved]
    if missing:
        issues.append(
            _issue(
                "ERROR",
                CODE_DISAGREEMENT_NOT_PRESERVED,
                "material findings of different passes disagree on criterion/criteria "
                + ", ".join(map(repr, missing))
                + "; the synthesis must preserve each as PARTIAL_AGREEMENT or "
                "UNRESOLVED_DISAGREEMENT",
            )
        )
    return issues


def _validate_advisory_result(
    record: Mapping[str, Any], existing_finding_ids: set[str]
) -> list[Issue]:
    raw_advisory = record.get("advisory_result")
    advisory = _mapping(raw_advisory)
    problems: list[str] = []
    if not isinstance(raw_advisory, Mapping):
        problems.append("advisory_result must be a JSON object")
    if advisory.get("authority") != AUTHORITY_ADVISORY:
        problems.append(f"authority must be {AUTHORITY_ADVISORY} (advisory only)")
    if advisory.get("recommendation") not in RECOMMENDATIONS:
        problems.append(
            "recommendation must be one of " + ", ".join(sorted(RECOMMENDATIONS))
        )
    raw_basis = advisory.get("basis")
    if not (isinstance(raw_basis, (list, tuple)) and raw_basis):
        problems.append("basis must be a non-empty list of finding ids")
    else:
        unknown = sorted(
            {
                basis
                for basis in raw_basis
                if not (isinstance(basis, str) and basis in existing_finding_ids)
            }
        )
        if unknown:
            problems.append(
                "basis must reference existing finding ids; unknown: "
                + ", ".join(map(repr, unknown))
            )
    if not problems:
        return []
    return [
        _issue(
            "ERROR",
            CODE_ADVISORY_AUTHORITY,
            "the advisory result is invalid: " + "; ".join(problems),
        )
    ]


def _forbidden_field_paths(value: Any, path: str = "") -> list[str]:
    found: list[str] = []
    if isinstance(value, Mapping):
        for key, child in value.items():
            child_path = f"{path}.{key}" if path else str(key)
            if isinstance(key, str) and key in _FORBIDDEN_AUTHORITY_FIELDS:
                found.append(child_path)
            found.extend(_forbidden_field_paths(child, child_path))
    elif isinstance(value, (list, tuple)):
        for index, child in enumerate(value):
            found.extend(_forbidden_field_paths(child, f"{path}[{index}]"))
    return found


def _validate_cost(record: Mapping[str, Any]) -> list[Issue]:
    entries, cost = _budget_inputs(record)
    assessment = assess_budget(entries, cost)
    issues: list[Issue] = []
    for code in assessment["issues"]:
        if code == "MISSING_COST":
            issues.append(
                _issue(
                    "ERROR",
                    CODE_MISSING_COST,
                    "declared cost is missing or invalid: baseline_agent_seconds "
                    "and baseline_words must be positive and every pass (and the "
                    "synthesis) must declare non-negative agent_seconds, words and "
                    "calls",
                )
            )
        elif code == "PASS_CAP_EXCEEDED":
            issues.append(
                _issue(
                    "ERROR",
                    CODE_PASS_CAP_EXCEEDED,
                    "the declared review exceeds the experimental caps: at most "
                    f"{MAX_PASSES} deliberation passes, {MAX_PASS_WORDS} words per "
                    f"pass and {MAX_SYNTHESIS_WORDS} words of synthesis",
                )
            )
        elif code == "EXCEEDED_TARGET":
            multiplier = assessment.get("cost_multiplier")
            issues.append(
                _issue(
                    "WARNING",
                    CODE_COST_OVER_TARGET,
                    f"treatment cost multiplier {multiplier:.3f} exceeds the "
                    "declared target_multiplier"
                    if isinstance(multiplier, (int, float))
                    else "treatment cost exceeds the declared target_multiplier",
                )
            )
    return issues


def validate_record(record: Mapping[str, Any]) -> list[Issue]:
    """Validate a review record. Pure, deterministic, no I/O.

    Accepts any JSON-shaped dict and reports every structural problem it finds;
    it never raises for missing or malformed fields. ``ERROR`` issues make the
    record invalid; ``WARNING`` issues are recorded limitations (the absence of a
    declared commit-before-reveal order, or a cost above the experimental
    target).
    """
    if not isinstance(record, Mapping):
        return [
            _issue(
                "ERROR",
                CODE_SCHEMA_VERSION,
                "a review record must be a JSON object with schema_version '1'",
            )
        ]

    issues: list[Issue] = []

    if record.get("schema_version") != SCHEMA_VERSION:
        issues.append(
            _issue(
                "ERROR",
                CODE_SCHEMA_VERSION,
                f'schema_version must be {SCHEMA_VERSION!r}',
            )
        )

    issues.extend(_validate_frame(record))

    frame = _mapping(record.get("frame"))
    if frame.get("commit_before_reveal") is not True:
        issues.append(
            _issue(
                "WARNING",
                CODE_COMMIT_ORDER_UNVERIFIED,
                "commit-before-reveal is declared by hash, not technically "
                "enforced; the frame does not declare commit_before_reveal: true, "
                "so the ordering is at best recorded by hash",
            )
        )

    count_issues, raw_passes = _validate_pass_count(record)
    issues.extend(count_issues)
    passes = tuple(_mapping(raw_pass) for raw_pass in raw_passes)
    issues.extend(_validate_pass_postures(passes))
    issues.extend(_validate_commitments(passes))

    findings = _findings(passes)
    issues.extend(_validate_findings(findings))
    existing_finding_ids = set(_finding_identifiers(findings))

    conflict_criteria = _material_disagreement_criteria(findings)
    issues.extend(_validate_synthesis(record, existing_finding_ids, conflict_criteria))
    issues.extend(_validate_advisory_result(record, existing_finding_ids))

    for path in sorted(set(_forbidden_field_paths(record))):
        issues.append(
            _issue(
                "ERROR",
                CODE_FORBIDDEN_AUTHORITY_FIELD,
                f"the review record may not carry adjudication fields; found "
                f"forbidden field {path.split('.')[-1].split('[')[0]!r} at {path!r}",
            )
        )

    issues.extend(_validate_cost(record))

    return sorted(issues, key=lambda issue: (issue.severity, issue.code, issue.message))
