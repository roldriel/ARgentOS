"""Deterministic value, retention, cost and efficiency metrics of a MAR record.

DEV-only reference runtime, **experimental**: this module belongs to the isolated
``runtime/adversarial_review/`` package, a read-only instrument for a validation
experiment. It is **advisory-only**, **not integrated** in any workflow, host or
payload, and it holds **no authority**: it counts and divides declared data; it
never scores an outcome as a decision, never accepts or rejects anything and
never persists a measurement. All functions are pure and deterministic over
JSON-shaped dicts/lists; none performs I/O.

Retention is computed from an **evaluator-declared** mapping (full finding id ->
minimal finding id), never from text matching. Bundles are declared by mapping
several full ids to one minimal id; invalid mapping entries are reported, not
silently repaired (design doc §9.6).

Provenance: ``docs/working/research/MINIMAL_ADVERSARIAL_REVIEW_DESIGN_2026-10-25.md``
(Working / Research; non-normative).
"""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from typing import Any

from .budget import assess_budget
from .record import _budget_inputs

#: Deterministic key order of the metric sub-dicts (never iterate the frozensets,
#: whose order is not stable across processes).
_NOVELTY_ORDER = ("NEW", "DERIVED", "DUPLICATE")
_MATERIALITY_ORDER = ("MATERIAL", "NON_MATERIAL", "SPURIOUS")
_IMPACT_ORDER = (
    "DECISIONAL_IMPACT",
    "PLAN_IMPACT",
    "EVIDENCE_IMPACT",
    "NONE",
)


def _is_number(value: Any) -> bool:
    return isinstance(value, (int, float)) and not isinstance(value, bool)


def _mapping(value: Any) -> Mapping[str, Any]:
    return value if isinstance(value, Mapping) else {}


def _items(value: Any) -> tuple[Any, ...]:
    return tuple(value) if isinstance(value, (list, tuple)) else ()


def _findings(findings: Sequence[Mapping[str, Any]]) -> list[Mapping[str, Any]]:
    return [finding for finding in _items(findings) if isinstance(finding, Mapping)]


def _unique_ids(values: Sequence[str]) -> list[str]:
    """Declared id sequence, strings only, duplicates removed preserving order."""
    identifiers: list[str] = []
    for value in _items(values):
        if isinstance(value, str) and value not in identifiers:
            identifiers.append(value)
    return identifiers


def value_metrics(findings: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    """Count findings by novelty, materiality and impact, and their shares.

    ``duplicate_share`` and ``spurious_share`` divide by the total number of
    findings (``0.0`` when there are none). ``distinct_material_new`` counts
    ``(NEW|DERIVED) + MATERIAL`` findings — the numerator of the retention
    experiment.
    """
    items = _findings(findings)
    total = len(items)
    by_novelty = {name: 0 for name in _NOVELTY_ORDER}
    by_materiality = {name: 0 for name in _MATERIALITY_ORDER}
    impact_counts = {name: 0 for name in _IMPACT_ORDER}

    for finding in items:
        novelty = finding.get("novelty")
        if novelty in by_novelty:
            by_novelty[novelty] += 1
        materiality = finding.get("materiality")
        if materiality in by_materiality:
            by_materiality[materiality] += 1
        impact = finding.get("impact")
        if impact in impact_counts:
            impact_counts[impact] += 1

    distinct_material_new = sum(
        1
        for finding in items
        if finding.get("novelty") in {"NEW", "DERIVED"}
        and finding.get("materiality") == "MATERIAL"
    )
    duplicate_material = sum(
        1
        for finding in items
        if finding.get("novelty") == "DUPLICATE"
        and finding.get("materiality") == "MATERIAL"
    )
    material_without_impact = sum(
        1
        for finding in items
        if finding.get("materiality") == "MATERIAL"
        and finding.get("impact") == "NONE"
    )

    duplicate_count = by_novelty["DUPLICATE"]
    spurious_count = by_materiality["SPURIOUS"]
    return {
        "total": total,
        "by_novelty": by_novelty,
        "by_materiality": by_materiality,
        "distinct_material_new": distinct_material_new,
        "duplicate_material": duplicate_material,
        "duplicate_share": (duplicate_count / total) if total else 0.0,
        "spurious_share": (spurious_count / total) if total else 0.0,
        "impact_counts": impact_counts,
        "material_without_impact": material_without_impact,
    }


def retention_metrics(
    full_dmn_ids: Sequence[str],
    minimal_dmn_ids: Sequence[str],
    mapping: Mapping[str, str],
    impactful_full_ids: Sequence[str] = (),
) -> dict[str, Any]:
    """Compute value and impact retention from an evaluator-declared mapping.

    ``mapping`` is ``FULL_ID -> MINIMAL_ID``. A mapping entry is *retained* when
    its full id is in ``full_dmn_ids`` and its minimal id is in
    ``minimal_dmn_ids``; several full ids may map to one minimal id (a declared
    bundle), and each valid entry counts once. ``None`` means the ratio is not
    defined (empty denominator), never a fabricated ``0.0``.
    """
    full = _unique_ids(full_dmn_ids)
    minimal = _unique_ids(minimal_dmn_ids)
    full_set = set(full)
    minimal_set = set(minimal)

    mapping_entries: list[tuple[Any, Any]] = []
    if isinstance(mapping, Mapping):
        mapping_entries = list(mapping.items())

    retained = 0
    retained_pairs: dict[str, str] = {}
    invalid_mapping: list[dict[str, Any]] = []
    for full_id, minimal_id in mapping_entries:
        valid_full = isinstance(full_id, str) and full_id in full_set
        valid_minimal = isinstance(minimal_id, str) and minimal_id in minimal_set
        if valid_full and valid_minimal:
            retained += 1
            retained_pairs[full_id] = minimal_id
            continue
        reasons: list[str] = []
        if not valid_full:
            reasons.append("FULL_ID_NOT_IN_FULL_SET")
        if not valid_minimal:
            reasons.append("MINIMAL_ID_NOT_IN_MINIMAL_SET")
        invalid_mapping.append(
            {"full_id": full_id, "minimal_id": minimal_id, "reasons": reasons}
        )

    matched_full_ids = {full_id for full_id, _ in mapping_entries if isinstance(full_id, str)}
    unmatched_full = [full_id for full_id in full if full_id not in matched_full_ids]

    impactful = [full_id for full_id in _unique_ids(impactful_full_ids) if full_id in full_set]
    impacted_retained = sum(1 for full_id in impactful if full_id in retained_pairs)

    return {
        "full_count": len(full),
        "minimal_count": len(minimal),
        "retained_count": retained,
        "value_retention": (retained / len(full)) if full else None,
        "impacted_full_count": len(impactful),
        "impacted_retained_count": impacted_retained,
        "impact_retention": (impacted_retained / len(impactful)) if impactful else None,
        "unmatched_full": unmatched_full,
        "invalid_mapping": invalid_mapping,
    }


def cost_metrics(budget: Mapping[str, Any]) -> dict[str, Any]:
    """Pass through the budget's status and key numbers (a view, not a judgement)."""
    budget_map = _mapping(budget)
    return {
        "status": budget_map.get("status"),
        "evaluation_passes": budget_map.get("evaluation_passes"),
        "treatment_agent_seconds": budget_map.get("treatment_agent_seconds"),
        "treatment_words": budget_map.get("treatment_words"),
        "treatment_calls": budget_map.get("treatment_calls"),
        "cost_multiplier": budget_map.get("cost_multiplier"),
        "words_multiplier": budget_map.get("words_multiplier"),
    }


def _per_1000_agent_seconds(count: Any, agent_seconds: Any) -> float | None:
    if not _is_number(count) or not _is_number(agent_seconds) or agent_seconds <= 0:
        return None
    return count / agent_seconds * 1000.0


def efficiency_metrics(
    value: Mapping[str, Any], budget: Mapping[str, Any]
) -> dict[str, Any]:
    """Value produced per 1 000 agent-seconds; ``None`` when undefined."""
    value_map = _mapping(value)
    budget_map = _mapping(budget)
    agent_seconds = budget_map.get("treatment_agent_seconds")
    impact_counts = _mapping(value_map.get("impact_counts"))
    by_materiality = _mapping(value_map.get("by_materiality"))
    return {
        "distinct_material_new_per_1000_agent_seconds": _per_1000_agent_seconds(
            value_map.get("distinct_material_new"), agent_seconds
        ),
        "decisive_impacts_per_1000_agent_seconds": _per_1000_agent_seconds(
            impact_counts.get("DECISIONAL_IMPACT"), agent_seconds
        ),
        "spurious_per_1000_agent_seconds": _per_1000_agent_seconds(
            by_materiality.get("SPURIOUS"), agent_seconds
        ),
    }


def review_metrics(record: Mapping[str, Any]) -> dict[str, Any]:
    """Compute value, budget, cost and efficiency metrics of one review record.

    Findings are collected from every pass; the budget is recomputed from the
    record's declared costs with the same inputs ``validate_record`` uses. No
    I/O: the record is the caller's data.
    """
    record_map = _mapping(record)
    findings: list[Mapping[str, Any]] = []
    for raw_pass in _items(record_map.get("passes")):
        pass_map = _mapping(raw_pass)
        findings.extend(
            finding
            for finding in _items(pass_map.get("findings"))
            if isinstance(finding, Mapping)
        )

    value = value_metrics(findings)
    entries, cost = _budget_inputs(record_map)
    assessment = assess_budget(entries, cost)
    return {
        "finding_count": len(findings),
        "findings": findings,
        "value": value,
        "budget": assessment,
        "cost": cost_metrics(assessment),
        "efficiency": efficiency_metrics(value, assessment),
    }
