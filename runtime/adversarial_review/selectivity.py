"""Advisory selectivity rule of the Minimal Adversarial Review (MAR) prototype.

DEV-only reference runtime, **experimental**: this module belongs to the isolated
``runtime/adversarial_review/`` package, a read-only instrument for a validation
experiment. It is **advisory-only**, **not integrated** in any workflow, host or
payload, and it holds **no authority**: the rule recommends a review depth and
never invokes, routes, blocks or chooses anything. The caller declares the
invocation decision and records the motive in the frame.

The rule below is an **EXPERIMENTAL heuristic**, not architecture and not a
classifier. It is deterministic and is applied in this order:

1. any declared signal ``UNKNOWN`` -> ``INSUFFICIENT_SIGNALS`` (no trigger is
   invented);
2. ``materiality_potential == LOW`` -> ``NO_REVIEW``;
3. materiality ``MEDIUM|HIGH`` and any of ``ambiguity``, ``irreversibility``,
   ``error_cost``, ``risk`` is ``HIGH`` -> ``REVIEW_TWO_PASS``;
4. materiality ``MEDIUM|HIGH`` and any of ``ambiguity``, ``risk``, ``impact``,
   ``uncertainty``, ``irreversibility``, ``error_cost`` is ``MEDIUM`` ->
   ``REVIEW_SINGLE_PASS``;
5. otherwise -> ``NO_REVIEW``.

The signals must be declared by the invoker (never inferred); ``recommend_review``
raises ``ValueError`` on a malformed signal set, because that is a programmer
error, not a review result.

Provenance: ``docs/working/research/MINIMAL_ADVERSARIAL_REVIEW_DESIGN_2026-10-25.md``
(Working / Research; non-normative).
"""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any

from .model import SIGNAL_KEYS, SIGNAL_LEVELS

#: Constant note attached to every recommendation: the rule advises, the caller
#: decides. Wording is part of the prototype's declared boundary.
ADVISORY_NOTE = (
    "advisory recommendation only; the caller declares the invocation decision "
    "and records the motive (no automatic trigger/classifier)"
)

#: Signals whose ``HIGH`` level can justify the two-pass depth.
_TWO_PASS_SIGNALS = ("ambiguity", "irreversibility", "error_cost", "risk")

#: Signals whose ``MEDIUM`` level can justify the single-pass depth.
_SINGLE_PASS_SIGNALS = (
    "ambiguity",
    "risk",
    "impact",
    "uncertainty",
    "irreversibility",
    "error_cost",
)


def _result(recommendation: str, basis: list[str]) -> dict[str, Any]:
    return {
        "recommendation": recommendation,
        "basis": basis,
        "advisory": True,
        "note": ADVISORY_NOTE,
    }


def _validate_signals(signals: Mapping[str, Any]) -> dict[str, str]:
    """Check the signal set is exactly the contracted one, or raise ValueError."""
    if not isinstance(signals, Mapping):
        raise ValueError(
            "signals must be a mapping with exactly the contracted signal keys"
        )
    given_keys = set(signals)
    expected_keys = set(SIGNAL_KEYS)
    if given_keys != expected_keys:
        missing = sorted(expected_keys - given_keys)
        unexpected = sorted(given_keys - expected_keys)
        raise ValueError(
            "signals must contain exactly the contracted signal keys "
            f"(missing: {missing}; unexpected: {unexpected})"
        )
    levels: dict[str, str] = {}
    for key in SIGNAL_KEYS:
        level = signals[key]
        if level not in SIGNAL_LEVELS:
            raise ValueError(
                f"signal {key!r} must be one of {sorted(SIGNAL_LEVELS)}, "
                f"got {level!r}"
            )
        levels[key] = level
    return levels


def recommend_review(signals: Mapping[str, Any]) -> dict[str, Any]:
    """Recommend a review depth from the declared signals. Pure and deterministic.

    The result is advisory by construction: ``advisory`` is always ``True`` and
    the recommendation never acts. A malformed signal set raises ``ValueError``
    (programmer error) rather than inventing a recommendation.
    """
    levels = _validate_signals(signals)

    unknown = [key for key in SIGNAL_KEYS if levels[key] == "UNKNOWN"]
    if unknown:
        return _result(
            "INSUFFICIENT_SIGNALS",
            [f"signal {key!r} is UNKNOWN; the review depth cannot be recommended"
             for key in unknown],
        )

    materiality = levels["materiality_potential"]
    if materiality == "LOW":
        return _result(
            "NO_REVIEW",
            [
                "materiality_potential is LOW: the expected material consequence "
                "does not justify the cost of a review"
            ],
        )

    high = [key for key in _TWO_PASS_SIGNALS if levels[key] == "HIGH"]
    if materiality in {"MEDIUM", "HIGH"} and high:
        return _result(
            "REVIEW_TWO_PASS",
            [
                f"materiality_potential is {materiality}",
                "HIGH signal(s) that justify a second, adversarial pass: "
                + ", ".join(high),
            ],
        )

    medium = [key for key in _SINGLE_PASS_SIGNALS if levels[key] == "MEDIUM"]
    if materiality in {"MEDIUM", "HIGH"} and medium:
        return _result(
            "REVIEW_SINGLE_PASS",
            [
                f"materiality_potential is {materiality}",
                "no HIGH signal justifies a second pass; MEDIUM signal(s): "
                + ", ".join(medium),
            ],
        )

    return _result(
        "NO_REVIEW",
        [
            f"materiality_potential is {materiality} and no declared signal reaches "
            "the review thresholds of the experimental rule"
        ],
    )
