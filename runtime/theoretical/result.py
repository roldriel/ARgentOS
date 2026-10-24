"""The ``TE_RESULT`` contract, validator, status derivation and comparison.

The result is a value, never a write.  The engine validates form and declared
honesty only: it cannot decide whether a semantic claim is true.  The ``status``
is *derived* here from the result's record; a producer cannot declare
``CONVERGED`` by editing a field.
"""

from __future__ import annotations

import importlib
import json
import sys
from pathlib import Path
from typing import Any, Mapping, Sequence

from .checks import (
    ANOMALY,
    BOUNDARY,
    GAP,
    NOT_APPLICABLE,
    VALID,
    CheckResult,
    check_ids,
)
from .identity import (
    TOOL_VERSION,
    canonical_json,
    input_identity,
    run_identity,
)
from .overlay import GitRepository
from .proposal import Proposal, ProposalError, load_proposal_at

SCHEMA_VERSION = "1"
TOOL = "runtime.theoretical"

STATUSES = (
    "CONVERGED",
    "OPEN_FINDINGS",
    "REQUIRES_HUMAN",
    "GAP",
    "NO_PROGRESS",
    "RESOURCE_LIMIT",
)

CLAIM_KINDS = ("OBSERVATION", "INFERENCE", "PREDICTION")
CLAIM_SUPPORTS = ("CHECKED", "NOT_EVALUABLE", "NOT_APPLICABLE", "UNCHECKED")
EVIDENCE_CLASSES = ("FACTUAL", "NORMATIVE", "DECISION", "RELEASE", "DESCRIPTIVE", "NONE")
FINDING_SIGNALS = (ANOMALY, BOUNDARY, GAP)
DISPOSITIONS = ("OPEN", "ESCALATED", "RESIDUAL")
EXECUTORS = ("engine", "producer", "engine+producer")
DIMENSION_STATUSES = ("PERFORMED", "PENDING", "NOT_APPLICABLE")
OBLIGATION_CANDIDATES = (
    "structural_checker",
    "unit_test",
    "integration_test",
    "dogfood_test",
    "runtime_check",
    "manual_review",
    "git_evidence",
    "declared_environmental_gap",
)
OBLIGATION_STATUSES = ("OPEN",)
ASSUMPTION_SOURCES = ("PREMISE_REF", "ANALYSIS")
DIMENSIONS = ("completeness", "consistency", "adversarial", "authority", "verification")

_TOP_KEYS = {
    "schema_version",
    "te_id",
    "status",
    "reason",
    "provenance",
    "input",
    "identity",
    "model",
    "coverage",
    "claims",
    "assumptions",
    "findings",
    "corrections",
    "verification_obligations",
    "escalations",
    "residual_risks",
    "limits",
    "no_progress",
}
_PROVENANCE_KEYS = {
    "kind",
    "method",
    "tool",
    "tool_version",
    "created_at",
    "producer",
    "authority_basis",
}
_INPUT_KEYS = {"factual", "proposal", "check_set", "previous_te_id", "revision"}
_IDENTITY_KEYS = {"factual", "projected", "inputs", "run"}
_RUN_KEYS = {"te_id", "input_identity", "producer", "created_at", "nonce"}
_MODEL_KEYS = {"paths", "effects", "scope", "content"}
_COVERAGE_KEYS = {
    "required_items",
    "claims",
    "checked",
    "not_evaluable",
    "not_applicable",
    "dimensions",
}
_CLAIM_KEYS = {
    "id",
    "item",
    "statement",
    "kind",
    "support",
    "evidence_class",
    "evidence_refs",
    "rule_ref",
    "obligation_ref",
    "reason",
}
_ASSUMPTION_KEYS = {"id", "statement", "source", "invalidated_by", "affects"}
_FINDING_KEYS = {
    "id",
    "signal",
    "statement",
    "location",
    "evidence_refs",
    "disposition",
    "escalation_ref",
    "accepted_by",
}
_CORRECTION_KEYS = {
    "id",
    "finding_ref",
    "target",
    "statement",
    "authority_required",
    "applied",
}
_OBLIGATION_KEYS = {
    "id",
    "for_claim",
    "finding_ref",
    "statement",
    "falsified_if",
    "depends_on",
    "candidate",
    "status",
}
_ESCALATION_KEYS = {
    "id",
    "decision",
    "alternatives",
    "why_not_derivable",
    "consequences",
    "recommendation",
    "reversibility",
    "affected_contracts",
}
_RESIDUAL_KEYS = {"id", "description", "why_not_resolvable", "owner"}
_LIMITS_KEYS = {"unevaluated_areas", "declared_limits"}
_PROGRESS_KEYS = {"fingerprint", "previous_fingerprint", "previous_te_id"}
_DIMENSION_KEYS = {
    "executor",
    "status",
    "computed",
    "capability",
    "probed",
    "claim_refs",
    "finding_refs",
    "escalation_refs",
    "evidence_refs",
}


def _load_tool(name: str):
    tools = Path(__file__).resolve().parents[2] / "tools"
    if str(tools) not in sys.path:
        sys.path.insert(0, str(tools))
    return importlib.import_module(name)


def _check_list(value: Any) -> bool:
    return isinstance(value, (list, tuple))


def _is_int(value: Any) -> bool:
    return isinstance(value, int) and not isinstance(value, bool)


def _missing_keys(obj: Any, keys: set[str], label: str, problems: list[str]) -> None:
    if not isinstance(obj, Mapping):
        problems.append(f"{label} is not an object")
        return
    for key in sorted(keys):
        if key not in obj:
            problems.append(f"{label} is missing field: {key}")


def _unknown_keys(obj: Any, keys: set[str], label: str, problems: list[str]) -> None:
    if isinstance(obj, Mapping):
        for key in sorted(set(obj) - keys):
            problems.append(f"{label} has unknown field: {key}")


def _finding_key(finding: Mapping[str, Any]) -> tuple[str, str, str]:
    return (
        str(finding.get("signal", "")),
        str(finding.get("statement", "")),
        str(finding.get("location", "")),
    )


def fingerprint(payload: Mapping[str, Any]) -> str:
    """The no-progress fingerprint: items + material findings + status.

    Deliberately *not* the plan blob: a cosmetic edit is not progress while the
    same material findings remain.  A previous result may carry this value.
    """
    items = sorted(
        str(claim.get("item"))
        for claim in payload.get("claims") or ()
        if isinstance(claim, Mapping) and claim.get("item")
    )
    findings = sorted(
        _finding_key(finding)
        for finding in payload.get("findings") or ()
        if isinstance(finding, Mapping)
        and finding.get("disposition") != "RESIDUAL"
    )
    return canonical_json(
        {
            "items": items,
            "findings": findings,
            "status": payload.get("status"),
        }
    ).strip()


def _dimensions_performed(payload: Mapping[str, Any]) -> bool:
    coverage = payload.get("coverage") or {}
    dimensions = coverage.get("dimensions") if isinstance(coverage, Mapping) else None
    if not isinstance(dimensions, Mapping):
        return False
    for name in DIMENSIONS:
        record = dimensions.get(name)
        if not isinstance(record, Mapping) or record.get("status") != "PERFORMED":
            return False
    return True


def _has_gap_condition(payload: Mapping[str, Any]) -> bool:
    coverage = payload.get("coverage") or {}
    claims = payload.get("claims") or ()
    findings = payload.get("findings") or ()
    if not isinstance(coverage, Mapping):
        return True
    if not _dimensions_performed(payload):
        return True
    if coverage.get("required_items") != coverage.get("claims"):
        return True
    if coverage.get("claims") != len(claims):
        return True
    counts = {"CHECKED": 0, "NOT_EVALUABLE": 0, "NOT_APPLICABLE": 0, "UNCHECKED": 0}
    for claim in claims:
        if not isinstance(claim, Mapping):
            return True
        support = claim.get("support")
        counts[str(support)] = counts.get(str(support), 0) + 1
        if support == "UNCHECKED":
            return True
        if support == "NOT_EVALUABLE" and not claim.get("obligation_ref"):
            return True
        if support == "NOT_APPLICABLE" and not str(claim.get("reason") or "").strip():
            return True
    if coverage.get("checked") != counts["CHECKED"]:
        return True
    if coverage.get("not_evaluable") != counts["NOT_EVALUABLE"]:
        return True
    if coverage.get("not_applicable") != counts["NOT_APPLICABLE"]:
        return True
    producer = (payload.get("provenance") or {}).get("producer")
    if not str(producer or "").strip() or str(producer).strip() == "pending":
        return True
    for finding in findings:
        if not isinstance(finding, Mapping):
            return True
        signal = finding.get("signal")
        disposition = finding.get("disposition")
        if signal == GAP and disposition != "RESIDUAL":
            return True
        if disposition == "RESIDUAL" and not str(finding.get("accepted_by") or "").strip():
            return True
        if disposition == "ESCALATED" and not str(finding.get("escalation_ref") or "").strip():
            return True
    if not isinstance(payload.get("limits"), Mapping):
        return True
    return False


def _has_open(payload: Mapping[str, Any]) -> bool:
    return any(
        isinstance(finding, Mapping) and finding.get("disposition") == "OPEN"
        for finding in payload.get("findings") or ()
    )


def _has_escalated(payload: Mapping[str, Any]) -> bool:
    findings = payload.get("findings") or ()
    if any(
        isinstance(finding, Mapping) and finding.get("disposition") == "ESCALATED"
        for finding in findings
    ):
        return True
    return bool(payload.get("escalations"))


def _revision_limit_reached(payload: Mapping[str, Any]) -> bool:
    revision = (payload.get("input") or {}).get("revision") or {}
    if not isinstance(revision, Mapping):
        return False
    index = revision.get("index")
    ceiling = revision.get("ceiling")
    return _is_int(index) and _is_int(ceiling) and ceiling > 0 and index >= ceiling


def _no_progress(payload: Mapping[str, Any]) -> bool:
    progress = payload.get("no_progress") or {}
    if not isinstance(progress, Mapping):
        return False
    previous = progress.get("previous_fingerprint")
    if not str(previous or "").strip():
        return False
    return str(previous) == fingerprint(payload)


def _is_converged(payload: Mapping[str, Any]) -> bool:
    if _has_gap_condition(payload):
        return False
    if _has_open(payload) or _has_escalated(payload):
        return False
    return True


def derive_status(payload: Mapping[str, Any]) -> str | None:
    """Derive the one status from the record, in the closed precedence order.

    ``CONVERGED > RESOURCE_LIMIT > NO_PROGRESS > GAP > REQUIRES_HUMAN >
    OPEN_FINDINGS``.  ``None`` means no condition applies: the result is invalid.
    """
    if _is_converged(payload):
        return "CONVERGED"
    if _revision_limit_reached(payload):
        return "RESOURCE_LIMIT"
    if _no_progress(payload):
        return "NO_PROGRESS"
    if _has_gap_condition(payload):
        return "GAP"
    if _has_escalated(payload):
        return "REQUIRES_HUMAN"
    if _has_open(payload):
        return "OPEN_FINDINGS"
    return None


def _dimension(
    executor: str,
    *,
    status: str = "PENDING",
    computed: bool = False,
    capability: str = "",
    probed: Sequence[str] = (),
    claim_refs: Sequence[str] = (),
    finding_refs: Sequence[str] = (),
    escalation_refs: Sequence[str] = (),
    evidence_refs: Sequence[str] = (),
) -> dict[str, Any]:
    return {
        "executor": executor,
        "status": status,
        "computed": computed,
        "capability": capability,
        "probed": list(probed),
        "claim_refs": list(claim_refs),
        "finding_refs": list(finding_refs),
        "escalation_refs": list(escalation_refs),
        "evidence_refs": list(evidence_refs),
    }


def build_skeleton(proposal: Proposal, checks: Sequence[CheckResult]) -> dict[str, Any]:
    """Build the producer-facing skeleton from deterministic facts only.

    Producer dimensions are ``PENDING`` with empty ``probed``; the engine's
    dimensions are marked ``computed`` but not ``PERFORMED`` until the producer
    reviews them.  The status is ``GAP`` because the attestation is pending.
    """
    inputs = input_identity(proposal.base, proposal.overlay)
    run = run_identity(inputs, plan=proposal.plan, producer="pending")
    claims = [
        {
            "id": f"TC-{index:02d}",
            "item": item.id,
            "statement": item.text,
            "kind": "OBSERVATION",
            "support": "UNCHECKED",
            "evidence_class": "FACTUAL",
            "evidence_refs": [],
            "rule_ref": None,
            "obligation_ref": None,
            "reason": "producer attestation pending",
        }
        for index, item in enumerate(proposal.items, start=1)
    ]

    findings: list[dict[str, Any]] = []
    obligations: list[dict[str, Any]] = []
    for result in checks:
        if result.signal in (VALID, NOT_APPLICABLE):
            continue
        finding_id = f"TF-{len(findings) + 1:02d}"
        findings.append(
            {
                "id": finding_id,
                "signal": result.signal,
                "statement": result.statement,
                "location": result.check,
                "evidence_refs": list(result.evidence_refs),
                "disposition": "OPEN",
                "escalation_ref": None,
                "accepted_by": None,
            }
        )
        if result.obligation is not None:
            obligation_id = f"TV-{len(obligations) + 1:02d}"
            obligations.append(
                {
                    "id": obligation_id,
                    "for_claim": None,
                    "finding_ref": finding_id,
                    "statement": result.obligation["statement"],
                    "falsified_if": result.obligation["falsified_if"],
                    "depends_on": list(result.obligation.get("depends_on") or ()),
                    "candidate": result.obligation["candidate"],
                    "status": "OPEN",
                }
            )
    for gap_text in proposal.gaps:
        finding_id = f"TF-{len(findings) + 1:02d}"
        findings.append(
            {
                "id": finding_id,
                "signal": GAP,
                "statement": gap_text,
                "location": "proposal",
                "evidence_refs": [proposal.path],
                "disposition": "OPEN",
                "escalation_ref": None,
                "accepted_by": None,
            }
        )
        obligation_id = f"TV-{len(obligations) + 1:02d}"
        obligations.append(
            {
                "id": obligation_id,
                "for_claim": None,
                "finding_ref": finding_id,
                "statement": f"provide or explicitly disposition: {gap_text}",
                "falsified_if": "the declared section is present and readable",
                "depends_on": [],
                "candidate": "manual_review",
                "status": "OPEN",
            }
        )

    coverage = {
        "required_items": len(proposal.items),
        "claims": len(claims),
        "checked": 0,
        "not_evaluable": 0,
        "not_applicable": 0,
        "dimensions": {
            "completeness": _dimension("producer"),
            "consistency": _dimension("producer"),
            "adversarial": _dimension("producer"),
            "authority": _dimension(
                "engine+producer", computed=True, evidence_refs=list(check_ids())
            ),
            "verification": _dimension("engine", computed=True),
        },
    }

    return {
        "schema_version": SCHEMA_VERSION,
        "te_id": run["te_id"],
        "status": "GAP",
        "reason": "producer dimensions and attestation are pending",
        "provenance": {
            "kind": "theoretical",
            "method": "theoretical-execution",
            "tool": TOOL,
            "tool_version": TOOL_VERSION,
            "created_at": run["created_at"],
            "producer": "pending",
            "authority_basis": "READ_ONLY_ANALYSIS",
        },
        "input": {
            "factual": proposal.base.to_dict(),
            "proposal": {
                "path": proposal.path,
                "blob": proposal.blob,
                "status": proposal.status,
            },
            "check_set": list(inputs["check_set"]),
            "previous_te_id": None,
            "revision": {"index": 1, "ceiling": None},
        },
        "identity": {
            "factual": inputs["factual"],
            "projected": inputs["projected"],
            "inputs": inputs,
            "run": run,
        },
        "model": {
            "paths": list(proposal.deliverables),
            "effects": list(proposal.effects),
            "scope": list(proposal.scope),
            "content": "unknown",
        },
        "coverage": coverage,
        "claims": claims,
        "assumptions": [],
        "findings": findings,
        "corrections": [],
        "verification_obligations": obligations,
        "escalations": [],
        "residual_risks": [],
        "limits": {
            "unevaluated_areas": list(proposal.gaps),
            "declared_limits": [
                "semantic dimensions are producer-attested",
                "no runtime execution is performed by TE",
            ],
        },
        "no_progress": {
            "fingerprint": None,
            "previous_fingerprint": None,
            "previous_te_id": None,
        },
    }


def _resolve_reference(root: Path, base_commit: str, reference: str) -> bool:
    if not reference or ":" not in reference:
        return False
    path, section = reference.rsplit(":", 1)
    path = path.strip()
    section = section.strip()
    if not path or not section:
        return False
    repo = GitRepository(root)
    text = repo.read_text(base_commit, path)
    if text is None:
        return False
    try:
        tool = _load_tool("check_plan_citations")
        return bool(tool.section_exists(section, text))
    except Exception:  # noqa: BLE001 - fail closed
        return False


def _validate_dimension(
    name: str,
    record: Any,
    problems: list[str],
    *,
    coverage: Mapping[str, Any],
) -> None:
    if not isinstance(record, Mapping):
        problems.append(f"coverage.dimensions.{name} is not an object")
        return
    _missing_keys(record, _DIMENSION_KEYS, f"coverage.dimensions.{name}", problems)
    executor = record.get("executor")
    status = record.get("status")
    if executor not in EXECUTORS:
        problems.append(f"coverage.dimensions.{name}.executor is unknown: {executor!r}")
    if status not in DIMENSION_STATUSES:
        problems.append(f"coverage.dimensions.{name}.status is unknown: {status!r}")
    expected = {
        "completeness": "producer",
        "consistency": "producer",
        "adversarial": "producer",
        "authority": "engine+producer",
        "verification": "engine",
    }[name]
    if executor != expected:
        problems.append(
            f"coverage.dimensions.{name}.executor must be {expected!r}, got {executor!r}"
        )
    if status == "PERFORMED":
        if "producer" in str(executor):
            if not str(record.get("capability") or "").strip():
                problems.append(
                    f"coverage.dimensions.{name} is PERFORMED without a capability"
                )
            if not list(record.get("probed") or ()):
                problems.append(
                    f"coverage.dimensions.{name} is PERFORMED without a non-empty probed list"
                )
        if "engine" in str(executor):
            if record.get("computed") is not True:
                problems.append(
                    f"coverage.dimensions.{name} is PERFORMED without computed=true"
                )
            refs = list(record.get("evidence_refs") or ())
            if not refs and not (name == "verification" and coverage.get("not_evaluable") == 0):
                problems.append(
                    f"coverage.dimensions.{name} is PERFORMED without evidence_refs"
                )


def _validate_claim(
    claim: Any,
    *,
    item_ids: set[str],
    obligations: Mapping[str, Mapping[str, Any]],
    problems: list[str],
) -> None:
    if not isinstance(claim, Mapping):
        problems.append("claim is not an object")
        return
    _missing_keys(claim, _CLAIM_KEYS, "claim", problems)
    claim_id = str(claim.get("id", ""))
    kind = claim.get("kind")
    support = claim.get("support")
    evidence_class = claim.get("evidence_class")
    if kind not in CLAIM_KINDS:
        problems.append(f"claim {claim_id}: unknown kind {kind!r}")
    if support not in CLAIM_SUPPORTS:
        problems.append(f"claim {claim_id}: unknown support {support!r}")
    if evidence_class not in EVIDENCE_CLASSES:
        problems.append(f"claim {claim_id}: unknown evidence_class {evidence_class!r}")
    if claim.get("item") not in item_ids:
        problems.append(f"claim {claim_id}: item is not an enumerated item")
    if not str(claim.get("statement") or "").strip():
        problems.append(f"claim {claim_id}: empty statement")
    refs = claim.get("evidence_refs")
    if not _check_list(refs):
        problems.append(f"claim {claim_id}: evidence_refs is not a list")
    if kind == "OBSERVATION" and evidence_class != "FACTUAL":
        problems.append(f"claim {claim_id}: OBSERVATION must use evidence_class FACTUAL")
    if kind == "INFERENCE" and evidence_class not in ("NORMATIVE", "DESCRIPTIVE"):
        problems.append(
            f"claim {claim_id}: INFERENCE must use NORMATIVE or DESCRIPTIVE"
        )
    if kind == "PREDICTION":
        if evidence_class != "NONE":
            problems.append(f"claim {claim_id}: PREDICTION must use evidence_class NONE")
        if support != "NOT_EVALUABLE":
            problems.append(f"claim {claim_id}: PREDICTION must be NOT_EVALUABLE")
        if not str(claim.get("obligation_ref") or "").strip():
            problems.append(f"claim {claim_id}: PREDICTION requires an obligation_ref")
    if support == "CHECKED":
        if kind == "PREDICTION":
            problems.append(f"claim {claim_id}: PREDICTION cannot be CHECKED")
        if not refs:
            problems.append(f"claim {claim_id}: CHECKED requires evidence_refs")
        if kind == "INFERENCE" and not str(claim.get("rule_ref") or "").strip():
            problems.append(f"claim {claim_id}: CHECKED INFERENCE requires rule_ref")
    if support == "NOT_EVALUABLE":
        obligation_ref = claim.get("obligation_ref")
        if not str(obligation_ref or "").strip():
            problems.append(f"claim {claim_id}: NOT_EVALUABLE requires an obligation_ref")
        elif str(obligation_ref) not in obligations:
            problems.append(
                f"claim {claim_id}: obligation_ref {obligation_ref!r} does not exist"
            )
    if support == "NOT_APPLICABLE" and not str(claim.get("reason") or "").strip():
        problems.append(f"claim {claim_id}: NOT_APPLICABLE requires a reason")


def _validate_finding(
    finding: Any,
    *,
    root: Path | None,
    base_commit: str,
    escalation_ids: set[str],
    problems: list[str],
) -> None:
    if not isinstance(finding, Mapping):
        problems.append("finding is not an object")
        return
    _missing_keys(finding, _FINDING_KEYS, "finding", problems)
    finding_id = str(finding.get("id", ""))
    signal = finding.get("signal")
    disposition = finding.get("disposition")
    if signal not in FINDING_SIGNALS:
        problems.append(f"finding {finding_id}: unknown signal {signal!r}")
    if disposition not in DISPOSITIONS:
        problems.append(f"finding {finding_id}: unknown disposition {disposition!r}")
    if not str(finding.get("statement") or "").strip():
        problems.append(f"finding {finding_id}: empty statement")
    if not str(finding.get("location") or "").strip():
        problems.append(f"finding {finding_id}: empty location")
    if not _check_list(finding.get("evidence_refs")):
        problems.append(f"finding {finding_id}: evidence_refs is not a list")
    if disposition == "ESCALATED":
        ref = finding.get("escalation_ref")
        if not str(ref or "").strip():
            problems.append(f"finding {finding_id}: ESCALATED requires escalation_ref")
        elif str(ref) not in escalation_ids:
            problems.append(f"finding {finding_id}: escalation_ref {ref!r} does not exist")
    if disposition == "RESIDUAL":
        accepted = finding.get("accepted_by")
        if not str(accepted or "").strip():
            problems.append(f"finding {finding_id}: RESIDUAL requires accepted_by")
        elif root is not None and not _resolve_reference(root, base_commit, str(accepted)):
            problems.append(
                f"finding {finding_id}: accepted_by does not resolve to a committed "
                "path:section"
            )


def validate_result(
    payload: Mapping[str, Any],
    root: str | Path | None = None,
) -> tuple[list[str], str | None]:
    """Validate structural form and declared honesty; return problems + derived status."""
    problems: list[str] = []
    if not isinstance(payload, Mapping):
        return (["result is not an object"], None)
    _unknown_keys(payload, _TOP_KEYS, "result", problems)
    _missing_keys(payload, _TOP_KEYS, "result", problems)
    if problems:
        return (problems, None)
    if payload.get("schema_version") != SCHEMA_VERSION:
        problems.append(f"unsupported schema_version: {payload.get('schema_version')!r}")
    if payload.get("status") not in STATUSES:
        problems.append(f"unknown status: {payload.get('status')!r}")
    if not str(payload.get("reason") or "").strip():
        problems.append("reason is empty")

    provenance = payload.get("provenance")
    _missing_keys(provenance, _PROVENANCE_KEYS, "provenance", problems)
    if isinstance(provenance, Mapping):
        if provenance.get("kind") != "theoretical":
            problems.append("provenance.kind must be 'theoretical'")
        if provenance.get("method") != "theoretical-execution":
            problems.append("provenance.method must be 'theoretical-execution'")
        if provenance.get("tool") != TOOL:
            problems.append(f"provenance.tool must be {TOOL!r}")
        for key in ("created_at", "producer", "authority_basis"):
            if not str(provenance.get(key) or "").strip():
                problems.append(f"provenance.{key} is empty")

    data = payload.get("input")
    _missing_keys(data, _INPUT_KEYS, "input", problems)
    if isinstance(data, Mapping):
        _missing_keys(data.get("factual"), {"commit", "tree"}, "input.factual", problems)
        proposal_input = data.get("proposal")
        _missing_keys(
            proposal_input, {"path", "blob", "status"}, "input.proposal", problems
        )
        _missing_keys(data.get("revision"), {"index", "ceiling"}, "input.revision", problems)
        if not _check_list(data.get("check_set")):
            problems.append("input.check_set is not a list")
        revision = data.get("revision")
        if isinstance(revision, Mapping):
            if not _is_int(revision.get("index")) or int(revision.get("index")) < 1:
                problems.append("input.revision.index is not a positive integer")
            ceiling = revision.get("ceiling")
            if ceiling is not None and (not _is_int(ceiling) or int(ceiling) < 1):
                problems.append("input.revision.ceiling is not a positive integer or null")
        previous = data.get("previous_te_id")
        if previous is not None and not str(previous).strip():
            problems.append("input.previous_te_id is empty")

    identity = payload.get("identity")
    _missing_keys(identity, _IDENTITY_KEYS, "identity", problems)
    if isinstance(identity, Mapping):
        _missing_keys(identity.get("run"), _RUN_KEYS, "identity.run", problems)
        for key in ("factual", "projected", "inputs"):
            if not isinstance(identity.get(key), Mapping):
                problems.append(f"identity.{key} is not an object")
        run = identity.get("run")
        if isinstance(run, Mapping):
            for key in ("te_id", "producer", "created_at", "nonce"):
                if not str(run.get(key) or "").strip():
                    problems.append(f"identity.run.{key} is empty")
            if isinstance(provenance, Mapping) and run.get("producer") != provenance.get(
                "producer"
            ):
                problems.append("identity.run.producer != provenance.producer")
            if run.get("input_identity") != identity.get("inputs"):
                problems.append("identity.run.input_identity != identity.inputs")
        if isinstance(data, Mapping):
            if identity.get("factual") != data.get("factual"):
                problems.append("identity.factual != input.factual")
        if isinstance(provenance, Mapping):
            inputs = identity.get("inputs")
            if isinstance(inputs, Mapping) and provenance.get("tool_version") != inputs.get(
                "tool_version"
            ):
                problems.append("provenance.tool_version != identity.inputs.tool_version")

    model = payload.get("model")
    _missing_keys(model, _MODEL_KEYS, "model", problems)
    if isinstance(model, Mapping):
        if model.get("content") != "unknown":
            problems.append("model.content must be 'unknown'")
        for key in ("paths", "effects", "scope"):
            if not _check_list(model.get(key)):
                problems.append(f"model.{key} is not a list")

    coverage = payload.get("coverage")
    _missing_keys(coverage, _COVERAGE_KEYS, "coverage", problems)
    if isinstance(coverage, Mapping):
        for key in ("required_items", "claims", "checked", "not_evaluable", "not_applicable"):
            if not _is_int(coverage.get(key)) or int(coverage.get(key)) < 0:
                problems.append(f"coverage.{key} is not a non-negative integer")
        dimensions = coverage.get("dimensions")
        if not isinstance(dimensions, Mapping):
            problems.append("coverage.dimensions is not an object")
        else:
            for name in DIMENSIONS:
                _validate_dimension(name, dimensions.get(name), problems, coverage=coverage)

    claims = payload.get("claims")
    if not _check_list(claims):
        problems.append("claims is not a list")
        claims = []
    obligations_list = payload.get("verification_obligations")
    if not _check_list(obligations_list):
        problems.append("verification_obligations is not a list")
        obligations_list = []
    obligations: dict[str, Mapping[str, Any]] = {}
    for obligation in obligations_list:
        if isinstance(obligation, Mapping) and str(obligation.get("id") or "").strip():
            obligations[str(obligation["id"])] = obligation

    escalations = payload.get("escalations")
    if not _check_list(escalations):
        problems.append("escalations is not a list")
        escalations = []
    escalation_ids = {
        str(escalation.get("id"))
        for escalation in escalations
        if isinstance(escalation, Mapping) and escalation.get("id")
    }

    item_ids: set[str] = set()
    if root is not None and isinstance(data, Mapping):
        proposal_input = data.get("proposal")
        if isinstance(proposal_input, Mapping):
            try:
                proposal = load_proposal_at(
                    root,
                    str(proposal_input.get("path") or ""),
                    base_ref=str((data.get("factual") or {}).get("commit") or ""),
                )
            except ProposalError as exc:
                problems.append(f"proposal cannot be recomposed: {exc}")
                proposal = None
            if proposal is not None:
                item_ids = {item.id for item in proposal.items}
                if proposal.blob != proposal_input.get("blob"):
                    problems.append("input.proposal.blob does not match the base blob")
                if proposal.status != proposal_input.get("status"):
                    problems.append("input.proposal.status does not match the base Plan")
                if proposal.base.to_dict() != data.get("factual"):
                    problems.append("input.factual does not match the base commit/tree")
                if list(proposal.deliverables) != list((model or {}).get("paths") or ()):
                    problems.append("model.paths does not match the base deliverables")
                if list(proposal.effects) != list((model or {}).get("effects") or ()):
                    problems.append("model.effects does not match the base effects")
                if list(proposal.scope) != list((model or {}).get("scope") or ()):
                    problems.append("model.scope does not match the base Scope")
                if coverage.get("required_items") != len(proposal.items):
                    problems.append(
                        "coverage.required_items does not match the enumerated items"
                    )
                expected_inputs = input_identity(proposal.base, proposal.overlay)
                if identity.get("inputs") != expected_inputs:
                    problems.append("identity.inputs does not match the recomputed inputs")
                if identity.get("projected") != proposal.overlay.identity():
                    problems.append("identity.projected does not match the overlay")
                if isinstance(data, Mapping) and data.get("check_set") != expected_inputs.get(
                    "check_set"
                ):
                    problems.append("input.check_set does not match the recomputed check-set")
    elif root is None:
        item_ids = {
            str(claim.get("item"))
            for claim in claims
            if isinstance(claim, Mapping) and claim.get("item")
        }

    claim_ids: set[str] = set()
    item_claims: dict[str, int] = {}
    counts = {"CHECKED": 0, "NOT_EVALUABLE": 0, "NOT_APPLICABLE": 0, "UNCHECKED": 0}
    for claim in claims:
        _validate_claim(
            claim,
            item_ids=item_ids or {
                str(c.get("item")) for c in claims if isinstance(c, Mapping) and c.get("item")
            },
            obligations=obligations,
            problems=problems,
        )
        if not isinstance(claim, Mapping):
            continue
        claim_id = str(claim.get("id") or "")
        if not claim_id:
            problems.append("claim has an empty id")
        elif claim_id in claim_ids:
            problems.append(f"duplicate claim id: {claim_id}")
        claim_ids.add(claim_id)
        item = claim.get("item")
        if item:
            item_claims[str(item)] = item_claims.get(str(item), 0) + 1
        support = str(claim.get("support"))
        counts[support] = counts.get(support, 0) + 1
    if isinstance(coverage, Mapping):
        if coverage.get("claims") != len(claims):
            problems.append("coverage.claims does not match the claim count")
        if coverage.get("checked") != counts["CHECKED"]:
            problems.append("coverage.checked does not match CHECKED claims")
        if coverage.get("not_evaluable") != counts["NOT_EVALUABLE"]:
            problems.append("coverage.not_evaluable does not match NOT_EVALUABLE claims")
        if coverage.get("not_applicable") != counts["NOT_APPLICABLE"]:
            problems.append("coverage.not_applicable does not match NOT_APPLICABLE claims")
    if item_ids:
        missing = sorted(item_ids - set(item_claims))
        if missing:
            problems.append("claims missing for enumerated items: " + ", ".join(missing))
        unknown = sorted(set(item_claims) - item_ids)
        if unknown:
            problems.append("claims reference unknown items: " + ", ".join(unknown))
        duplicated = sorted(item for item, count in item_claims.items() if count > 1)
        if duplicated:
            problems.append("multiple claims for item(s): " + ", ".join(duplicated))

    assumptions = payload.get("assumptions")
    if not _check_list(assumptions):
        problems.append("assumptions is not a list")
        assumptions = []
    assumption_ids: set[str] = set()
    for assumption in assumptions:
        if not isinstance(assumption, Mapping):
            problems.append("assumption is not an object")
            continue
        _missing_keys(assumption, _ASSUMPTION_KEYS, "assumption", problems)
        assumption_id = str(assumption.get("id") or "")
        if not assumption_id:
            problems.append("assumption has an empty id")
        elif assumption_id in assumption_ids:
            problems.append(f"duplicate assumption id: {assumption_id}")
        assumption_ids.add(assumption_id)
        if assumption.get("source") not in ASSUMPTION_SOURCES:
            problems.append(
                f"assumption {assumption_id}: unknown source {assumption.get('source')!r}"
            )
        if not str(assumption.get("invalidated_by") or "").strip():
            problems.append(f"assumption {assumption_id}: empty invalidated_by")
        if not _check_list(assumption.get("affects")):
            problems.append(f"assumption {assumption_id}: affects is not a list")

    findings = payload.get("findings")
    if not _check_list(findings):
        problems.append("findings is not a list")
        findings = []
    finding_ids: set[str] = set()
    for finding in findings:
        _validate_finding(
            finding,
            root=Path(root) if root is not None else None,
            base_commit=str(((data or {}).get("factual") or {}).get("commit") or ""),
            escalation_ids=escalation_ids,
            problems=problems,
        )
        if isinstance(finding, Mapping):
            finding_id = str(finding.get("id") or "")
            if not finding_id:
                problems.append("finding has an empty id")
            elif finding_id in finding_ids:
                problems.append(f"duplicate finding id: {finding_id}")
            finding_ids.add(finding_id)

    corrections = payload.get("corrections")
    if not _check_list(corrections):
        problems.append("corrections is not a list")
        corrections = []
    for correction in corrections:
        if not isinstance(correction, Mapping):
            problems.append("correction is not an object")
            continue
        _missing_keys(correction, _CORRECTION_KEYS, "correction", problems)
        if correction.get("applied") is not False:
            problems.append(
                f"correction {correction.get('id')}: applied must be false"
            )
        if str(correction.get("finding_ref") or "") not in finding_ids:
            problems.append(
                f"correction {correction.get('id')}: finding_ref does not exist"
            )
        if not str(correction.get("statement") or "").strip():
            problems.append(f"correction {correction.get('id')}: empty statement")

    for obligation in obligations_list:
        if not isinstance(obligation, Mapping):
            problems.append("verification obligation is not an object")
            continue
        _missing_keys(obligation, _OBLIGATION_KEYS, "verification_obligation", problems)
        obligation_id = str(obligation.get("id") or "")
        if not str(obligation.get("statement") or "").strip():
            problems.append(f"obligation {obligation_id}: empty statement")
        if not str(obligation.get("falsified_if") or "").strip():
            problems.append(f"obligation {obligation_id}: empty falsified_if")
        if obligation.get("candidate") not in OBLIGATION_CANDIDATES:
            problems.append(
                f"obligation {obligation_id}: unknown candidate "
                f"{obligation.get('candidate')!r}"
            )
        if obligation.get("status") not in OBLIGATION_STATUSES:
            problems.append(f"obligation {obligation_id}: status must be OPEN")
        has_claim = str(obligation.get("for_claim") or "").strip()
        has_finding = str(obligation.get("finding_ref") or "").strip()
        if bool(has_claim) == bool(has_finding):
            problems.append(
                f"obligation {obligation_id}: exactly one of for_claim/finding_ref is required"
            )
        if has_claim and has_claim not in claim_ids:
            problems.append(f"obligation {obligation_id}: for_claim does not exist")
        if has_finding and has_finding not in finding_ids:
            problems.append(f"obligation {obligation_id}: finding_ref does not exist")
        depends_on = obligation.get("depends_on")
        if not _check_list(depends_on):
            problems.append(f"obligation {obligation_id}: depends_on is not a list")
        else:
            for assumption_id in depends_on:
                if str(assumption_id) not in assumption_ids:
                    problems.append(
                        f"obligation {obligation_id}: depends_on {assumption_id!r} "
                        "does not exist"
                    )

    for escalation in escalations:
        if not isinstance(escalation, Mapping):
            problems.append("escalation is not an object")
            continue
        _missing_keys(escalation, _ESCALATION_KEYS, "escalation", problems)
        escalation_id = str(escalation.get("id") or "")
        for key in ("decision", "why_not_derivable", "consequences", "recommendation",
                    "reversibility"):
            if not str(escalation.get(key) or "").strip():
                problems.append(f"escalation {escalation_id}: empty {key}")
        if not list(escalation.get("alternatives") or ()):
            problems.append(f"escalation {escalation_id}: alternatives is empty")
        if not _check_list(escalation.get("affected_contracts")):
            problems.append(f"escalation {escalation_id}: affected_contracts is not a list")

    residual_risks = payload.get("residual_risks")
    if not _check_list(residual_risks):
        problems.append("residual_risks is not a list")
        residual_risks = []
    for risk in residual_risks:
        if not isinstance(risk, Mapping):
            problems.append("residual risk is not an object")
            continue
        _missing_keys(risk, _RESIDUAL_KEYS, "residual_risk", problems)
        for key in ("description", "why_not_resolvable", "owner"):
            if not str(risk.get(key) or "").strip():
                problems.append(f"residual risk {risk.get('id')}: empty {key}")

    limits = payload.get("limits")
    _missing_keys(limits, _LIMITS_KEYS, "limits", problems)
    if isinstance(limits, Mapping):
        for key in ("unevaluated_areas", "declared_limits"):
            if not _check_list(limits.get(key)):
                problems.append(f"limits.{key} is not a list")

    progress = payload.get("no_progress")
    _missing_keys(progress, _PROGRESS_KEYS, "no_progress", problems)
    if isinstance(progress, Mapping):
        previous = progress.get("previous_fingerprint")
        if previous is not None and not isinstance(previous, str):
            problems.append("no_progress.previous_fingerprint is not a string or null")

    derived = derive_status(payload) if not problems else None
    if derived is not None and payload.get("status") != derived:
        problems.append(
            f"declared status {payload.get('status')!r} != derived status {derived!r}"
        )
    if derived is None and not problems:
        problems.append("no status condition applies to this result")
    return (problems, derived)


def stale_state(payload: Mapping[str, Any], root: str | Path) -> dict[str, Any]:
    """Return ``fresh``/``stale``/``incomparable``/``gap`` for one result."""
    repo = GitRepository(root)
    data = payload.get("input") or {}
    factual = data.get("factual") or {}
    proposal_input = data.get("proposal") or {}
    commit = str(factual.get("commit") or "")
    path = str(proposal_input.get("path") or "")
    if not commit or not path or not repo.verify_ref(commit):
        return {
            "state": "gap",
            "reason": "the result's base commit is not resolvable",
            "current_head": repo.commit("HEAD"),
            "result_base": commit or None,
        }
    head = repo.commit("HEAD")
    if head is None:
        return {
            "state": "gap",
            "reason": "the current HEAD is not resolvable",
            "current_head": None,
            "result_base": commit,
        }
    if head != commit:
        return {
            "state": "stale",
            "reason": "the result was evaluated at a different commit than HEAD",
            "current_head": head,
            "result_base": commit,
        }
    try:
        proposal = load_proposal_at(root, path, base_ref=commit)
    except ProposalError as exc:
        return {
            "state": "gap",
            "reason": str(exc),
            "current_head": head,
            "result_base": commit,
        }
    identity = payload.get("identity") or {}
    inputs = identity.get("inputs") or {}
    expected = input_identity(proposal.base, proposal.overlay)
    if inputs.get("tool_version") != TOOL_VERSION or inputs.get("check_set") != expected.get(
        "check_set"
    ):
        return {
            "state": "incomparable",
            "reason": "tool version or check-set differs",
            "current_head": head,
            "result_base": commit,
        }
    if inputs != expected:
        return {
            "state": "stale",
            "reason": "the recomputed InputIdentity differs from the result",
            "current_head": head,
            "result_base": commit,
        }
    return {
        "state": "fresh",
        "reason": "the result's InputIdentity recomposes at HEAD",
        "current_head": head,
        "result_base": commit,
    }


def compare_results(previous: Mapping[str, Any], current: Mapping[str, Any]) -> dict[str, Any]:
    """Compare two results structurally; never claim resolved/reopened."""
    prev_inputs = (previous.get("identity") or {}).get("inputs")
    cur_inputs = (current.get("identity") or {}).get("inputs")
    if prev_inputs != cur_inputs:
        return {
            "comparison": "INPUT_CHANGED",
            "semantic": "NOT_COMPARABLE",
            "reason": "the two results were evaluated over different InputIdentity values",
        }
    prev_findings = {
        _finding_key(finding)
        for finding in previous.get("findings") or ()
        if isinstance(finding, Mapping) and finding.get("disposition") != "RESIDUAL"
    }
    cur_findings = {
        _finding_key(finding)
        for finding in current.get("findings") or ()
        if isinstance(finding, Mapping) and finding.get("disposition") != "RESIDUAL"
    }
    prev_claims = {
        str(claim.get("id")): claim.get("support")
        for claim in previous.get("claims") or ()
        if isinstance(claim, Mapping)
    }
    cur_claims = {
        str(claim.get("id")): claim.get("support")
        for claim in current.get("claims") or ()
        if isinstance(claim, Mapping)
    }
    support_changes = [
        {"id": claim_id, "previous": prev_claims.get(claim_id), "current": cur_claims.get(claim_id)}
        for claim_id in sorted(set(prev_claims) & set(cur_claims))
        if prev_claims.get(claim_id) != cur_claims.get(claim_id)
    ]
    only_prev = sorted(prev_findings - cur_findings)
    only_cur = sorted(cur_findings - prev_findings)
    divergence = bool(only_prev or only_cur or support_changes)
    return {
        "comparison": "SAME_INPUT",
        "semantic": "DIVERGENT" if divergence else "OBSERVED_EQUAL",
        "semantic_divergence": divergence,
        "only_in_prev": only_prev,
        "only_in_cur": only_cur,
        "claim_support_changes": support_changes,
        "note": "observed differences only; resolved/reopened are human interpretations",
    }


def load_result(path: str | Path) -> Mapping[str, Any]:
    """Read a result JSON fail-closed."""
    try:
        payload = json.loads(Path(path).read_text(encoding="utf-8"))
    except OSError as exc:
        raise ValueError(f"cannot read result: {exc}") from exc
    except json.JSONDecodeError as exc:
        raise ValueError(f"result is not valid JSON: {exc}") from exc
    if not isinstance(payload, Mapping):
        raise ValueError("result is not a JSON object")
    return payload
