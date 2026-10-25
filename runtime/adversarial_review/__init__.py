"""Minimal Adversarial Review (MAR) — isolated DEV reference prototype.

DEV-only, **experimental**, **advisory-only**, **not integrated** anywhere, and
holding **no authority**. This package is a read-only validation instrument for
one experiment: it models and validates an adversarial review record, recomputes
an advisory selectivity recommendation, assesses a declared cost budget, and
computes value / retention / cost / efficiency metrics. It has no gate, no
state, no registry, no persistence, no consumer and no effect on any authority:
the existing human or Change authority always decides, and a review result is
evidence only.

Boundaries that do not weaken:

- **No consumer.** Nothing in this repository imports this package; it is
  invoked manually (library or the read-only CLI).
- **No I/O beyond reading a JSON file in the CLI.** Every function is a
  deterministic pure function over JSON-shaped dicts.
- **No adjudication.** There is no verdict, vote, judge, jury, court, majority
  or authorization anywhere in the record model; the validator refuses records
  that carry such fields.
- **No protocol dependency.** The package imports the standard library only and
  never reads ``protocol/``; it does not touch the Orchestrator, the payload or
  the canonical battery.

Public surface:

- constants and closed vocabularies — :mod:`runtime.adversarial_review.model`;
- :func:`validate_record` / :class:`Issue` — record validation;
- :func:`recommend_review` — advisory selectivity heuristic;
- :func:`assess_budget` — deterministic budget assessment;
- :func:`value_metrics`, :func:`retention_metrics`, :func:`cost_metrics`,
  :func:`efficiency_metrics`, :func:`review_metrics` — metrics.

CLI: ``python -m runtime.adversarial_review {validate,selectivity,metrics} FILE``.

Provenance: ``docs/working/research/MINIMAL_ADVERSARIAL_REVIEW_DESIGN_2026-10-25.md``
(Working / Research; non-normative). The precedent of a read-only, unconsumed DEV
reference library is ``runtime/placement/`` (``docs/placement-contract.md:PC-72.1``).
"""

from __future__ import annotations

from .budget import assess_budget
from .metrics import (
    cost_metrics,
    efficiency_metrics,
    retention_metrics,
    review_metrics,
    value_metrics,
)
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
    SIGNAL_KEYS,
    SIGNAL_LEVELS,
    SOURCES,
    SYNTHESIS_METHOD,
    TARGET_COST_MULTIPLIER,
    TRIGGER_RECOMMENDATIONS,
)
from .record import CODE_COMMIT_ORDER_UNVERIFIED, Issue, validate_record
from .selectivity import recommend_review

__all__ = [
    "AUTHORITY_ADVISORY",
    "CODE_COMMIT_ORDER_UNVERIFIED",
    "DIRECTIONS",
    "DISAGREEMENT_STATES",
    "IMPACTS",
    "Issue",
    "MATERIALITY",
    "MAX_PASSES",
    "MAX_PASS_WORDS",
    "MAX_SYNTHESIS_WORDS",
    "NOVELTY",
    "POSTURES",
    "RECOMMENDATIONS",
    "SCHEMA_VERSION",
    "SIGNAL_KEYS",
    "SIGNAL_LEVELS",
    "SOURCES",
    "SYNTHESIS_METHOD",
    "TARGET_COST_MULTIPLIER",
    "TRIGGER_RECOMMENDATIONS",
    "assess_budget",
    "cost_metrics",
    "efficiency_metrics",
    "recommend_review",
    "retention_metrics",
    "review_metrics",
    "validate_record",
    "value_metrics",
]
