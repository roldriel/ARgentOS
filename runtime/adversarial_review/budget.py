"""Deterministic cost-budget assessment of a Minimal Adversarial Review (MAR).

DEV-only reference runtime, **experimental**: this module belongs to the isolated
``runtime/adversarial_review/`` package, a read-only instrument for a validation
experiment. It is **advisory-only**, **not integrated** in any workflow, host or
payload, and it holds **no authority**: it measures declared numbers, it never
enforces, blocks or authorizes a review. It performs no I/O and is a pure
function of its arguments.

The budget is *declared*, not instrumented: the caller (an experiment runner or
the evaluator) records agent-seconds, words and calls per pass; this module only
sums them and compares the result with the frozen experimental target.

Precedence of the returned status (first match wins):

1. ``MISSING_COST`` — the baseline or a pass cost is absent, non-numeric or
   negative, so no ratio can be trusted;
2. ``PASS_CAP_EXCEEDED`` — more than ``MAX_PASSES`` evaluation passes, a pass
   over ``MAX_PASS_WORDS``, or the synthesis over ``MAX_SYNTHESIS_WORDS``;
3. ``EXCEEDED_TARGET`` — the treatment/baseline agent-seconds ratio is above
   ``target_multiplier``;
4. ``WITHIN_TARGET``.

Provenance: ``docs/working/research/MINIMAL_ADVERSARIAL_REVIEW_DESIGN_2026-10-25.md``
(Working / Research; non-normative).
"""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from typing import Any

from .model import (
    MAX_PASSES,
    MAX_PASS_WORDS,
    MAX_SYNTHESIS_WORDS,
    TARGET_COST_MULTIPLIER,
)

#: ``pass_id`` of the synthetic entry that carries the synthesis cost. The
#: synthesis is consolidation, not an evaluation pass, so it does not count
#: toward ``MAX_PASSES`` and uses the synthesis word cap.
SYNTHESIS_PASS_ID = "SYNTHESIS"

#: The issue codes ``assess_budget`` can report, in deterministic order.
ISSUE_CODES = ("MISSING_COST", "PASS_CAP_EXCEEDED", "EXCEEDED_TARGET")


def _mapping(value: Any) -> Mapping[str, Any]:
    return value if isinstance(value, Mapping) else {}


def _is_number(value: Any) -> bool:
    """A JSON number (booleans are not numbers for cost purposes)."""
    return isinstance(value, (int, float)) and not isinstance(value, bool)


def _positive_number(value: Any) -> bool:
    return _is_number(value) and value > 0


def _positive_int(value: Any) -> bool:
    return isinstance(value, int) and not isinstance(value, bool) and value > 0


def _is_non_negative_number(value: Any) -> bool:
    return _is_number(value) and value >= 0


def _is_non_negative_int(value: Any) -> bool:
    return isinstance(value, int) and not isinstance(value, bool) and value >= 0


def _entries(passes: Sequence[Mapping[str, Any]]) -> list[Any]:
    if isinstance(passes, (list, tuple)):
        return list(passes)
    return []


def assess_budget(
    passes: Sequence[Mapping[str, Any]], cost: Mapping[str, Any]
) -> dict[str, Any]:
    """Assess the declared cost of a review against the experimental caps.

    ``passes`` carries one entry per deliberation pass, plus — when the record
    has a synthesis — a synthetic ``{"pass_id": "SYNTHESIS", "cost": ...}``
    entry. The synthesis sums into the treatment cost but is not an evaluation
    pass and uses the synthesis word cap.

    Returns a deterministic JSON-shaped dict with ``status`` (the precedence
    winner), ``issues`` (every triggered code, in ``ISSUE_CODES`` order), the
    agent-seconds / words / calls totals, the ratios (``None`` when the
    corresponding baseline is unusable) and one ``per_pass`` row per entry.
    """
    entries = _entries(passes)
    cost_map = _mapping(cost)

    baseline_agent_seconds = cost_map.get("baseline_agent_seconds")
    baseline_words = cost_map.get("baseline_words")
    target_multiplier = cost_map.get("target_multiplier", TARGET_COST_MULTIPLIER)

    missing_cost = not _positive_number(
        baseline_agent_seconds
    ) or not _positive_int(baseline_words)
    if _positive_number(target_multiplier):
        target = float(target_multiplier)
    else:
        # An unusable target is itself a missing cost declaration: the budget
        # cannot be assessed without a threshold to compare against.
        missing_cost = True
        target = TARGET_COST_MULTIPLIER

    treatment_agent_seconds = 0.0
    treatment_words = 0
    treatment_calls = 0
    evaluation_passes = 0
    cap_exceeded = False
    per_pass: list[dict[str, Any]] = []

    for raw_entry in entries:
        entry = _mapping(raw_entry)
        is_synthesis = entry.get("pass_id") == SYNTHESIS_PASS_ID
        if not is_synthesis:
            evaluation_passes += 1

        pass_cost = _mapping(entry.get("cost"))
        seconds = pass_cost.get("agent_seconds")
        words = pass_cost.get("words")
        calls = pass_cost.get("calls")

        if not (
            _is_non_negative_number(seconds)
            and _is_non_negative_int(words)
            and _is_non_negative_int(calls)
        ):
            missing_cost = True

        seconds_value = float(seconds) if _is_non_negative_number(seconds) else 0.0
        words_value = int(words) if _is_non_negative_int(words) else 0
        calls_value = int(calls) if _is_non_negative_int(calls) else 0

        treatment_agent_seconds += seconds_value
        treatment_words += words_value
        treatment_calls += calls_value

        word_cap = MAX_SYNTHESIS_WORDS if is_synthesis else MAX_PASS_WORDS
        within_word_cap = words_value <= word_cap
        if not within_word_cap:
            cap_exceeded = True

        per_pass.append(
            {
                "pass_id": entry.get("pass_id"),
                "words": words_value,
                "within_word_cap": within_word_cap,
                "agent_seconds": seconds_value,
            }
        )

    if evaluation_passes > MAX_PASSES:
        cap_exceeded = True

    cost_multiplier = (
        treatment_agent_seconds / float(baseline_agent_seconds)
        if _positive_number(baseline_agent_seconds)
        else None
    )
    words_multiplier = (
        treatment_words / float(baseline_words)
        if _positive_int(baseline_words)
        else None
    )
    exceeded_target = cost_multiplier is not None and cost_multiplier > target

    issues: list[str] = []
    if missing_cost:
        issues.append("MISSING_COST")
    if cap_exceeded:
        issues.append("PASS_CAP_EXCEEDED")
    if exceeded_target:
        issues.append("EXCEEDED_TARGET")

    if missing_cost:
        status = "MISSING_COST"
    elif cap_exceeded:
        status = "PASS_CAP_EXCEEDED"
    elif exceeded_target:
        status = "EXCEEDED_TARGET"
    else:
        status = "WITHIN_TARGET"

    return {
        "status": status,
        "issues": issues,
        "evaluation_passes": evaluation_passes,
        "treatment_agent_seconds": treatment_agent_seconds,
        "treatment_words": treatment_words,
        "treatment_calls": treatment_calls,
        "cost_multiplier": cost_multiplier,
        "words_multiplier": words_multiplier,
        "per_pass": per_pass,
    }
