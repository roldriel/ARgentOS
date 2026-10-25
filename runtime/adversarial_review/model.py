"""Closed vocabularies and limits of the Minimal Adversarial Review (MAR) prototype.

DEV-only reference runtime, **experimental**: this module belongs to the isolated
``runtime/adversarial_review/`` package, a read-only instrument for a validation
experiment. It is **advisory-only**, **not integrated** in any workflow, host or
payload, and it holds **no authority**: nothing here decides, gates, routes,
persists or authorizes anything. The values below are the design constraints of
one experiment, not architecture; if the experiment fails they are discarded
with it.

Provenance: ``docs/working/research/MINIMAL_ADVERSARIAL_REVIEW_DESIGN_2026-10-25.md``
(Working / Research; non-normative).
"""

from __future__ import annotations

#: Version of the review-record schema this prototype validates and computes on.
SCHEMA_VERSION = "1"

#: Maximum number of *deliberation* passes. The short synthesis is consolidation,
#: not a third evaluation pass (design doc, ``MAX_PASSES``).
MAX_PASSES = 2

#: Experimental cost objective: treatment agent-seconds at most this multiple of
#: the declared baseline. A hypothesis of the experiment, never a repository
#: constant.
TARGET_COST_MULTIPLIER = 2.0

#: Word caps used by the budget assessment (a pass and the synthesis).
MAX_PASS_WORDS = 700
MAX_SYNTHESIS_WORDS = 500

#: The two adversarial postures of a review pass.
POSTURES = frozenset({"TARGETED_FALSIFICATION", "STRONGEST_CASE_FOR"})

#: Where a finding came from: the falsification pass or the advocacy pass.
SOURCES = frozenset({"PASS_FALSIFICATION", "PASS_ADVOCACY"})

#: Novelty of a finding relative to the frozen baseline.
NOVELTY = frozenset({"NEW", "DERIVED", "DUPLICATE"})

#: Materiality classification of a finding.
MATERIALITY = frozenset({"MATERIAL", "NON_MATERIAL", "SPURIOUS"})

#: Impact classification of a finding (``REWEIGHTING`` is deliberately absent:
#: this minimal prototype does not need it).
IMPACTS = frozenset(
    {"DECISIONAL_IMPACT", "PLAN_IMPACT", "EVIDENCE_IMPACT", "NONE"}
)

#: Direction of a finding relative to the reviewed candidate.
DIRECTIONS = frozenset({"SUPPORTS", "OPPOSES", "NEUTRAL"})

#: States of a preserved disagreement between two passes.
DISAGREEMENT_STATES = frozenset(
    {"AGREEMENT", "PARTIAL_AGREEMENT", "UNRESOLVED_DISAGREEMENT"}
)

#: The only recommendations an advisory result may carry. None of them decides
#: anything: the existing authority always decides.
RECOMMENDATIONS = frozenset(
    {
        "ADVISE_PROCEED",
        "ADVISE_REVISE",
        "ADVISE_GATHER_EVIDENCE",
        "ADVISE_STOP",
        "NO_RECOMMENDATION",
    }
)

#: Recommendations of the advisory selectivity rule (never a gate or trigger).
TRIGGER_RECOMMENDATIONS = frozenset(
    {"REVIEW_TWO_PASS", "REVIEW_SINGLE_PASS", "NO_REVIEW", "INSUFFICIENT_SIGNALS"}
)

#: Declared signal levels of the selectivity rule.
SIGNAL_LEVELS = frozenset({"LOW", "MEDIUM", "HIGH", "UNKNOWN"})

#: The exactly-seven signals the caller declares (never inferred by a classifier).
SIGNAL_KEYS = (
    "materiality_potential",
    "ambiguity",
    "risk",
    "impact",
    "uncertainty",
    "irreversibility",
    "error_cost",
)

#: The advisory result may not carry any other authority.
AUTHORITY_ADVISORY = "ADVISORY_ONLY"

#: The only synthesis method of the minimal mechanism: a short criterion-mapped
#: comparison that may not introduce new material findings.
SYNTHESIS_METHOD = "CRITERION_MAPPED_SHORT"
