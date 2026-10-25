"""Behaviour of the Minimal Adversarial Review (MAR) prototype.

DEV-only, experimental, advisory-only, not integrated, and with no authority:
these tests protect a validation instrument, not a mechanism of the protocol.
They are fully isolated — a synthetic review record is built in memory, a JSON
copy is written only under ``tmp_path``, and nothing is read from ``protocol/``.

The runtime package is imported through the repository-root bootstrap shared by
the runtime suites (``tests/AGENTS.md``): a suite that imports ``runtime.*``
inserts the root itself.
"""

from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from runtime.adversarial_review import (  # noqa: E402
    AUTHORITY_ADVISORY,
    DIRECTIONS,
    DISAGREEMENT_STATES,
    IMPACTS,
    MATERIALITY,
    MAX_PASS_WORDS,
    MAX_PASSES,
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
    assess_budget,
    cost_metrics,
    efficiency_metrics,
    recommend_review,
    retention_metrics,
    review_metrics,
    validate_record,
    value_metrics,
)


# --- Fixtures ---------------------------------------------------------------


def _finding(
    finding_id: str,
    *,
    source: str,
    criterion: str = "criterion-1",
    direction: str = "NEUTRAL",
    novelty: str = "NEW",
    materiality: str = "NON_MATERIAL",
    impact: str = "NONE",
    consequence: str = "consequence",
    evidence_refs: list[str] | None = None,
) -> dict:
    return {
        "finding_id": finding_id,
        "source": source,
        "claim": f"claim of {finding_id}",
        "criterion": criterion,
        "direction": direction,
        "evidence_refs": ["evidence-1"] if evidence_refs is None else evidence_refs,
        "novelty": novelty,
        "materiality": materiality,
        "impact": impact,
        "consequence": consequence,
    }


def make_record(*, commit_before_reveal: bool | None = None) -> dict:
    """A structurally valid TWO_PASS review record (one WARNING by default)."""
    frame = {
        "question_ref": "Q-001",
        "candidate": "candidate A",
        "criteria": ["criterion-1", "criterion-2"],
        "evidence_refs": ["evidence-1"],
        "mode": "viability",
        "declared_invocation_reason": "material uncertainty on candidate A",
        "declared_by": "maintainer",
        "trigger_recommendation": "REVIEW_TWO_PASS",
    }
    if commit_before_reveal is not None:
        frame["commit_before_reveal"] = commit_before_reveal
    return {
        "schema_version": "1",
        "frame": frame,
        "passes": [
            {
                "pass_id": "P1",
                "posture": "TARGETED_FALSIFICATION",
                "executor": "executor-1",
                "commitment_hash": "a" * 64,
                "material_received": ["material-1"],
                "withheld_material": [],
                "evaluation_ref": "EVAL-1",
                "cost": {"agent_seconds": 100.0, "words": 400, "calls": 3},
                "findings": [
                    _finding(
                        "F-1",
                        source="PASS_FALSIFICATION",
                        criterion="criterion-1",
                        direction="OPPOSES",
                        novelty="NEW",
                        materiality="MATERIAL",
                        impact="DECISIONAL_IMPACT",
                        consequence="would flip the decision",
                    ),
                    _finding(
                        "F-2",
                        source="PASS_FALSIFICATION",
                        criterion="criterion-2",
                        direction="NEUTRAL",
                        novelty="DERIVED",
                        materiality="NON_MATERIAL",
                        impact="NONE",
                        consequence="",
                    ),
                ],
            },
            {
                "pass_id": "P2",
                "posture": "STRONGEST_CASE_FOR",
                "executor": "executor-2",
                "commitment_hash": "b" * 64,
                "material_received": ["material-1"],
                "withheld_material": ["material-2"],
                "evaluation_ref": "EVAL-2",
                "cost": {"agent_seconds": 120.0, "words": 350, "calls": 2},
                "findings": [
                    _finding(
                        "F-3",
                        source="PASS_ADVOCACY",
                        criterion="criterion-1",
                        direction="SUPPORTS",
                        novelty="NEW",
                        materiality="MATERIAL",
                        impact="PLAN_IMPACT",
                        consequence="keeps the plan sound",
                    )
                ],
            },
        ],
        "synthesis": {
            "method": "CRITERION_MAPPED_SHORT",
            "evaluation_ref": "EVAL-SYNTHESIS",
            "findings_kept": ["F-1", "F-2", "F-3"],
            "new_material_findings": [],
            "disagreements": [
                {
                    "criterion": "criterion-1",
                    "state": "UNRESOLVED_DISAGREEMENT",
                    "position_a": "the candidate fails",
                    "position_b": "the candidate holds",
                }
            ],
            "cost": {"agent_seconds": 150.0, "words": 300, "calls": 2},
        },
        "advisory_result": {
            "recommendation": "ADVISE_REVISE",
            "basis": ["F-1", "F-3"],
            "authority": "ADVISORY_ONLY",
        },
        "cost": {
            "baseline_agent_seconds": 200.0,
            "baseline_words": 1000,
            "target_multiplier": 2.0,
        },
    }


def _codes(issues) -> list[str]:
    return [issue.code for issue in issues]


def _error_codes(issues) -> list[str]:
    return [issue.code for issue in issues if issue.severity == "ERROR"]


def _warning_codes(issues) -> list[str]:
    return [issue.code for issue in issues if issue.severity == "WARNING"]


def _signals(**overrides: str) -> dict:
    signals = {key: "LOW" for key in SIGNAL_KEYS}
    signals["materiality_potential"] = "MEDIUM"
    signals.update(overrides)
    return signals


def _budget_passes() -> list[dict]:
    return [
        {"pass_id": "P1", "cost": {"agent_seconds": 100.0, "words": 400, "calls": 3}},
        {"pass_id": "P2", "cost": {"agent_seconds": 120.0, "words": 350, "calls": 2}},
        {
            "pass_id": "SYNTHESIS",
            "cost": {"agent_seconds": 150.0, "words": 300, "calls": 2},
        },
    ]


def _budget_cost(**overrides) -> dict:
    cost = {
        "baseline_agent_seconds": 200.0,
        "baseline_words": 1000,
        "target_multiplier": 2.0,
    }
    cost.update(overrides)
    return cost


def run_cli(*args: str, cwd: Path) -> subprocess.CompletedProcess[str]:
    env = os.environ.copy()
    env["PYTHONPATH"] = str(REPO_ROOT) + os.pathsep + env.get("PYTHONPATH", "")
    return subprocess.run(
        [sys.executable, "-B", "-m", "runtime.adversarial_review", *args],
        cwd=cwd,
        capture_output=True,
        text=True,
        encoding="utf-8",
        env=env,
        check=False,
    )


# --- Constants and closed vocabularies --------------------------------------


def test_constants_and_closed_vocabularies() -> None:
    assert SCHEMA_VERSION == "1"
    assert MAX_PASSES == 2
    assert TARGET_COST_MULTIPLIER == 2.0
    assert MAX_PASS_WORDS == 700
    assert MAX_SYNTHESIS_WORDS == 500
    vocabularies = {
        "POSTURES": (POSTURES, {"TARGETED_FALSIFICATION", "STRONGEST_CASE_FOR"}),
        "SOURCES": (SOURCES, {"PASS_FALSIFICATION", "PASS_ADVOCACY"}),
        "NOVELTY": (NOVELTY, {"NEW", "DERIVED", "DUPLICATE"}),
        "MATERIALITY": (MATERIALITY, {"MATERIAL", "NON_MATERIAL", "SPURIOUS"}),
        "IMPACTS": (
            IMPACTS,
            {"DECISIONAL_IMPACT", "PLAN_IMPACT", "EVIDENCE_IMPACT", "NONE"},
        ),
        "DIRECTIONS": (DIRECTIONS, {"SUPPORTS", "OPPOSES", "NEUTRAL"}),
        "DISAGREEMENT_STATES": (
            DISAGREEMENT_STATES,
            {"AGREEMENT", "PARTIAL_AGREEMENT", "UNRESOLVED_DISAGREEMENT"},
        ),
        "RECOMMENDATIONS": (
            RECOMMENDATIONS,
            {
                "ADVISE_PROCEED",
                "ADVISE_REVISE",
                "ADVISE_GATHER_EVIDENCE",
                "ADVISE_STOP",
                "NO_RECOMMENDATION",
            },
        ),
        "TRIGGER_RECOMMENDATIONS": (
            TRIGGER_RECOMMENDATIONS,
            {"REVIEW_TWO_PASS", "REVIEW_SINGLE_PASS", "NO_REVIEW", "INSUFFICIENT_SIGNALS"},
        ),
        "SIGNAL_LEVELS": (SIGNAL_LEVELS, {"LOW", "MEDIUM", "HIGH", "UNKNOWN"}),
    }
    for name, (vocabulary, expected) in vocabularies.items():
        assert isinstance(vocabulary, frozenset), name
        assert vocabulary == expected, name
    assert SIGNAL_KEYS == (
        "materiality_potential",
        "ambiguity",
        "risk",
        "impact",
        "uncertainty",
        "irreversibility",
        "error_cost",
    )
    assert AUTHORITY_ADVISORY == "ADVISORY_ONLY"
    assert SYNTHESIS_METHOD == "CRITERION_MAPPED_SHORT"


# --- Record validation -------------------------------------------------------


def test_a_valid_record_has_no_errors() -> None:
    issues = validate_record(make_record())
    assert _error_codes(issues) == []
    assert _warning_codes(issues) == ["COMMIT_ORDER_UNVERIFIED"]


def test_a_valid_record_declaring_commit_order_is_issue_free() -> None:
    assert validate_record(make_record(commit_before_reveal=True)) == []


def test_commit_order_unverified_warning() -> None:
    issues = validate_record(make_record())
    warnings = [issue for issue in issues if issue.severity == "WARNING"]
    assert [issue.code for issue in warnings] == ["COMMIT_ORDER_UNVERIFIED"]
    assert "not technically enforced" in warnings[0].message
    assert validate_record(make_record(commit_before_reveal=True)) == []


def test_envelope_errors() -> None:
    schema_record = make_record()
    schema_record["schema_version"] = "2"
    assert "SCHEMA_VERSION" in _error_codes(validate_record(schema_record))

    frame_mutations = (
        lambda record: record["frame"].update({"question_ref": ""}),
        lambda record: record["frame"].update({"candidate": "   "}),
        lambda record: record["frame"].update({"criteria": []}),
        lambda record: record["frame"].update({"criteria": ["criterion-1", ""]}),
        lambda record: record["frame"].update({"evidence_refs": []}),
        lambda record: record["frame"].update({"mode": "review"}),
        lambda record: record["frame"].update({"declared_invocation_reason": ""}),
        lambda record: record["frame"].update({"declared_by": ""}),
        lambda record: record["frame"].update({"trigger_recommendation": "REVIEW_ALWAYS"}),
        lambda record: record.pop("frame"),
    )
    for mutate in frame_mutations:
        record = make_record()
        mutate(record)
        assert "FRAME_INCOMPLETE" in _error_codes(validate_record(record))


def test_pass_structure_errors() -> None:
    count_mutations = (
        lambda record: record.update({"passes": []}),
        lambda record: record.update({"passes": record["passes"] * 2}),
        lambda record: record.update({"passes": "not-a-list"}),
    )
    for mutate in count_mutations:
        record = make_record()
        mutate(record)
        assert "PASS_COUNT" in _error_codes(validate_record(record))

    posture_mutations = (
        lambda record: record["passes"][0].update({"posture": "STRONGEST_CASE_FOR"}),
        lambda record: record["passes"][0].update({"posture": "UNKNOWN_POSTURE"}),
        lambda record: record["passes"][1].update({"pass_id": "P1"}),
        lambda record: record["passes"][1].update({"posture": "TARGETED_FALSIFICATION"}),
    )
    for mutate in posture_mutations:
        record = make_record()
        mutate(record)
        assert "PASS_POSTURE" in _error_codes(validate_record(record))

    commitment_mutations = (
        lambda record: record["passes"][0].update({"commitment_hash": "A" * 64}),
        lambda record: record["passes"][0].update({"commitment_hash": "a" * 63}),
        lambda record: record["passes"][0].update({"material_received": []}),
        lambda record: record["passes"][0].update({"withheld_material": "material-2"}),
        lambda record: record["passes"][0].update({"evaluation_ref": ""}),
    )
    for mutate in commitment_mutations:
        record = make_record()
        mutate(record)
        assert "COMMITMENT_MISSING" in _error_codes(validate_record(record))


def test_finding_errors() -> None:
    mutations = {
        "FINDING_ID_DUPLICATE": lambda record: record["passes"][1]["findings"][0].update(
            {"finding_id": "F-1"}
        ),
        "FINDING_NO_EVIDENCE": lambda record: record["passes"][0]["findings"][0].update(
            {"evidence_refs": []}
        ),
        "FINDING_NO_CRITERION": lambda record: record["passes"][0]["findings"][0].update(
            {"criterion": ""}
        ),
        "FINDING_SOURCE_MISMATCH": lambda record: record["passes"][0]["findings"][
            0
        ].update({"source": "PASS_ADVOCACY"}),
        "MATERIAL_WITHOUT_CONSEQUENCE": lambda record: record["passes"][0]["findings"][
            0
        ].update({"consequence": ""}),
    }
    for expected_code, mutate in mutations.items():
        record = make_record()
        mutate(record)
        assert expected_code in _error_codes(validate_record(record)), expected_code

    vocabulary_mutations = (
        lambda record: record["passes"][0]["findings"][0].update({"novelty": "MAYBE"}),
        lambda record: record["passes"][0]["findings"][0].update({"materiality": "MAYBE"}),
        lambda record: record["passes"][0]["findings"][0].update({"impact": "MAYBE"}),
        lambda record: record["passes"][0]["findings"][0].update({"direction": "MAYBE"}),
    )
    for mutate in vocabulary_mutations:
        record = make_record()
        mutate(record)
        assert "FINDING_VOCAB" in _error_codes(validate_record(record))


def test_synthesis_errors() -> None:
    unknown_finding = make_record()
    unknown_finding["synthesis"]["findings_kept"] = ["F-1", "F-99"]
    assert "SYNTHESIS_UNKNOWN_FINDING" in _error_codes(
        validate_record(unknown_finding)
    )

    new_material = make_record()
    new_material["synthesis"]["new_material_findings"] = ["F-1"]
    assert "SYNTHESIS_NEW_MATERIAL" in _error_codes(validate_record(new_material))

    bad_method = make_record()
    bad_method["synthesis"]["method"] = "FULL_DELIBERATION"
    assert "SYNTHESIS_METHOD" in _error_codes(validate_record(bad_method))

    empty_ref = make_record()
    empty_ref["synthesis"]["evaluation_ref"] = ""
    assert "SYNTHESIS_METHOD" in _error_codes(validate_record(empty_ref))

    no_synthesis = make_record()
    no_synthesis.pop("synthesis")
    assert "SYNTHESIS_METHOD" in _error_codes(validate_record(no_synthesis))


def test_disagreement_errors() -> None:
    lost = make_record()
    lost["synthesis"]["disagreements"] = []
    assert "DISAGREEMENT_NOT_PRESERVED" in _error_codes(validate_record(lost))

    preserved_elsewhere = make_record()
    preserved_elsewhere["synthesis"]["disagreements"] = [
        {"criterion": "criterion-2", "state": "UNRESOLVED_DISAGREEMENT"}
    ]
    assert "DISAGREEMENT_NOT_PRESERVED" in _error_codes(
        validate_record(preserved_elsewhere)
    )

    bad_state = make_record()
    bad_state["synthesis"]["disagreements"] = [
        {"criterion": "criterion-1", "state": "MAYBE"}
    ]
    assert "DISAGREEMENT_STATE" in _error_codes(validate_record(bad_state))

    empty_criterion = make_record()
    empty_criterion["synthesis"]["disagreements"] = [
        {"criterion": "", "state": "AGREEMENT"}
    ]
    assert "DISAGREEMENT_STATE" in _error_codes(validate_record(empty_criterion))


def test_advisory_and_forbidden_fields() -> None:
    advisory_mutations = (
        lambda record: record["advisory_result"].update({"authority": "AUTHORITY"}),
        lambda record: record["advisory_result"].update({"recommendation": "DECIDE"}),
        lambda record: record["advisory_result"].update({"basis": []}),
        lambda record: record["advisory_result"].update({"basis": ["F-99"]}),
        lambda record: record.pop("advisory_result"),
    )
    for mutate in advisory_mutations:
        record = make_record()
        mutate(record)
        assert "ADVISORY_AUTHORITY" in _error_codes(validate_record(record))

    forbidden_mutations = (
        lambda record: record.update({"verdict": "ADOPT"}),
        lambda record: record["frame"].update({"judge": "someone"}),
        lambda record: record["passes"][0]["findings"][0].update(
            {"authorization": "granted"}
        ),
        lambda record: record["synthesis"].update({"votes": {"F-1": 1}}),
    )
    for mutate in forbidden_mutations:
        record = make_record()
        mutate(record)
        assert "FORBIDDEN_AUTHORITY_FIELD" in _error_codes(validate_record(record))


def test_cost_record_errors() -> None:
    missing_baseline = make_record()
    missing_baseline["cost"]["baseline_agent_seconds"] = 0
    assert "MISSING_COST" in _error_codes(validate_record(missing_baseline))

    missing_pass_cost = make_record()
    missing_pass_cost["passes"][0].pop("cost")
    assert "MISSING_COST" in _error_codes(validate_record(missing_pass_cost))

    over_cap = make_record()
    over_cap["passes"][0]["cost"]["words"] = MAX_PASS_WORDS + 1
    assert "PASS_CAP_EXCEEDED" in _error_codes(validate_record(over_cap))

    synthesis_over_cap = make_record()
    synthesis_over_cap["synthesis"]["cost"]["words"] = MAX_SYNTHESIS_WORDS + 1
    assert "PASS_CAP_EXCEEDED" in _error_codes(validate_record(synthesis_over_cap))

    over_target = make_record()
    over_target["cost"]["target_multiplier"] = 0.5
    issues = validate_record(over_target)
    warnings = [issue for issue in issues if issue.severity == "WARNING"]
    assert "COST_OVER_TARGET" in _codes(warnings)
    assert "COST_OVER_TARGET" not in _error_codes(issues)


def test_issues_are_sorted_deterministically() -> None:
    record = make_record()
    record["schema_version"] = "2"
    record["frame"]["criteria"] = []
    record["cost"]["baseline_agent_seconds"] = 0
    first = validate_record(record)
    second = validate_record(record)
    assert [issue.to_dict() for issue in first] == [issue.to_dict() for issue in second]
    sort_keys = [(issue.severity, issue.code, issue.message) for issue in first]
    assert sort_keys == sorted(sort_keys)
    assert len(first) == len({(issue.severity, issue.code, issue.message) for issue in first})


# --- Advisory selectivity ----------------------------------------------------


@pytest.mark.parametrize(
    ("signals", "expected"),
    [
        (_signals(materiality_potential="LOW", ambiguity="UNKNOWN"), "INSUFFICIENT_SIGNALS"),
        (_signals(materiality_potential="LOW"), "NO_REVIEW"),
        (_signals(materiality_potential="MEDIUM", ambiguity="HIGH"), "REVIEW_TWO_PASS"),
        (
            _signals(materiality_potential="HIGH", irreversibility="HIGH"),
            "REVIEW_TWO_PASS",
        ),
        (_signals(materiality_potential="HIGH", impact="MEDIUM"), "REVIEW_SINGLE_PASS"),
        (_signals(materiality_potential="HIGH", error_cost="MEDIUM"), "REVIEW_SINGLE_PASS"),
        (_signals(materiality_potential="HIGH"), "NO_REVIEW"),
    ],
)
def test_selectivity_rule_table(signals: dict, expected: str) -> None:
    result = recommend_review(signals)
    assert result["recommendation"] == expected
    assert result["advisory"] is True
    assert result["note"] == (
        "advisory recommendation only; the caller declares the invocation decision "
        "and records the motive (no automatic trigger/classifier)"
    )
    assert result["basis"]


@pytest.mark.parametrize(
    "signals",
    [
        {key: level for key, level in _signals().items() if key != "risk"},
        {**_signals(), "unexpected_signal": "LOW"},
        _signals(ambiguity="MAYBE"),
        {**_signals(), "risk": None},
    ],
)
def test_selectivity_rejects_malformed_signals(signals: dict) -> None:
    with pytest.raises(ValueError):
        recommend_review(signals)


def test_selectivity_is_always_advisory_only() -> None:
    for signals in (
        _signals(),
        _signals(materiality_potential="LOW"),
        _signals(ambiguity="HIGH"),
        _signals(impact="MEDIUM"),
        _signals(materiality_potential="HIGH"),
    ):
        result = recommend_review(signals)
        assert result["advisory"] is True
        assert result["recommendation"] in TRIGGER_RECOMMENDATIONS


# --- Budget ------------------------------------------------------------------


@pytest.mark.parametrize(
    ("passes", "cost", "expected_status", "expected_issue"),
    [
        (_budget_passes(), _budget_cost(), "WITHIN_TARGET", None),
        (_budget_passes(), _budget_cost(baseline_agent_seconds=100.0), "EXCEEDED_TARGET", "EXCEEDED_TARGET"),
        (_budget_passes(), _budget_cost(baseline_agent_seconds=0), "MISSING_COST", "MISSING_COST"),
        (
            [
                {"pass_id": "P1", "cost": {"agent_seconds": 1.0, "words": MAX_PASS_WORDS + 1, "calls": 1}}
            ],
            _budget_cost(),
            "PASS_CAP_EXCEEDED",
            "PASS_CAP_EXCEEDED",
        ),
    ],
)
def test_budget_statuses(
    passes: list[dict], cost: dict, expected_status: str, expected_issue: str | None
) -> None:
    assessment = assess_budget(passes, cost)
    assert assessment["status"] == expected_status
    if expected_issue is None:
        assert assessment["issues"] == []
    else:
        assert expected_issue in assessment["issues"]


def test_budget_precedence() -> None:
    missing_and_capped = assess_budget(
        [
            {
                "pass_id": "P1",
                "cost": {"agent_seconds": 1.0, "words": MAX_PASS_WORDS + 1, "calls": 1},
            }
        ],
        _budget_cost(baseline_agent_seconds=0),
    )
    assert missing_and_capped["status"] == "MISSING_COST"
    assert missing_and_capped["issues"] == ["MISSING_COST", "PASS_CAP_EXCEEDED"]

    capped_and_exceeded = assess_budget(
        [
            {
                "pass_id": "P1",
                "cost": {"agent_seconds": 400.0, "words": MAX_PASS_WORDS + 1, "calls": 1},
            }
        ],
        _budget_cost(baseline_agent_seconds=100.0),
    )
    assert capped_and_exceeded["status"] == "PASS_CAP_EXCEEDED"
    assert capped_and_exceeded["issues"] == ["PASS_CAP_EXCEEDED", "EXCEEDED_TARGET"]


def test_budget_word_caps_totals_and_per_pass() -> None:
    assessment = assess_budget(_budget_passes(), _budget_cost())
    assert assessment["evaluation_passes"] == 2
    assert assessment["treatment_agent_seconds"] == pytest.approx(370.0)
    assert assessment["treatment_words"] == 1050
    assert assessment["treatment_calls"] == 7
    assert assessment["cost_multiplier"] == pytest.approx(1.85)
    assert assessment["words_multiplier"] == pytest.approx(1.05)
    assert [row["pass_id"] for row in assessment["per_pass"]] == [
        "P1",
        "P2",
        "SYNTHESIS",
    ]
    assert all(row["within_word_cap"] for row in assessment["per_pass"])
    assert set(assessment["per_pass"][0]) == {
        "pass_id",
        "words",
        "within_word_cap",
        "agent_seconds",
    }

    synthesis_over_cap = assess_budget(
        [
            {"pass_id": "P1", "cost": {"agent_seconds": 1.0, "words": 1, "calls": 1}},
            {
                "pass_id": "SYNTHESIS",
                "cost": {
                    "agent_seconds": 1.0,
                    "words": MAX_SYNTHESIS_WORDS + 1,
                    "calls": 1,
                },
            },
        ],
        _budget_cost(),
    )
    assert synthesis_over_cap["status"] == "PASS_CAP_EXCEEDED"
    assert synthesis_over_cap["per_pass"][-1]["within_word_cap"] is False

    empty = assess_budget([], _budget_cost())
    assert empty["status"] == "WITHIN_TARGET"
    assert empty["evaluation_passes"] == 0
    assert empty["treatment_agent_seconds"] == 0.0
    assert empty["per_pass"] == []


# --- Metrics -----------------------------------------------------------------


def test_value_metrics() -> None:
    findings = [
        _finding("F-1", source="PASS_FALSIFICATION", novelty="NEW", materiality="MATERIAL", impact="DECISIONAL_IMPACT"),
        _finding("F-2", source="PASS_ADVOCACY", novelty="DERIVED", materiality="MATERIAL", impact="PLAN_IMPACT"),
        _finding("F-3", source="PASS_FALSIFICATION", novelty="DUPLICATE", materiality="MATERIAL", impact="EVIDENCE_IMPACT"),
        _finding("F-4", source="PASS_ADVOCACY", novelty="DERIVED", materiality="SPURIOUS", impact="NONE"),
        _finding("F-5", source="PASS_FALSIFICATION", novelty="NEW", materiality="MATERIAL", impact="NONE"),
    ]
    metrics = value_metrics(findings)
    assert metrics["total"] == 5
    assert metrics["by_novelty"] == {"NEW": 2, "DERIVED": 2, "DUPLICATE": 1}
    assert metrics["by_materiality"] == {"MATERIAL": 4, "NON_MATERIAL": 0, "SPURIOUS": 1}
    assert metrics["distinct_material_new"] == 3
    assert metrics["duplicate_material"] == 1
    assert metrics["duplicate_share"] == pytest.approx(0.2)
    assert metrics["spurious_share"] == pytest.approx(0.2)
    assert metrics["impact_counts"] == {
        "DECISIONAL_IMPACT": 1,
        "PLAN_IMPACT": 1,
        "EVIDENCE_IMPACT": 1,
        "NONE": 2,
    }
    assert metrics["material_without_impact"] == 1

    empty = value_metrics([])
    assert empty["total"] == 0
    assert empty["distinct_material_new"] == 0
    assert empty["duplicate_share"] == 0.0
    assert empty["spurious_share"] == 0.0
    assert empty["by_novelty"] == {"NEW": 0, "DERIVED": 0, "DUPLICATE": 0}


def test_retention_metrics() -> None:
    metrics = retention_metrics(
        ["F-1", "F-2", "F-3"],
        ["M-1", "M-2"],
        {"F-1": "M-1", "F-2": "M-2"},
        ["F-1", "F-3"],
    )
    assert metrics["full_count"] == 3
    assert metrics["minimal_count"] == 2
    assert metrics["retained_count"] == 2
    assert metrics["value_retention"] == pytest.approx(2 / 3)
    assert metrics["impacted_full_count"] == 2
    assert metrics["impacted_retained_count"] == 1
    assert metrics["impact_retention"] == pytest.approx(0.5)
    assert metrics["unmatched_full"] == ["F-3"]
    assert metrics["invalid_mapping"] == []

    bundle = retention_metrics(
        ["F-1", "F-2", "F-3"],
        ["M-1"],
        {"F-1": "M-1", "F-2": "M-1"},
    )
    assert bundle["retained_count"] == 2
    assert bundle["value_retention"] == pytest.approx(2 / 3)
    assert bundle["impact_retention"] is None


def test_retention_edges() -> None:
    invalid = retention_metrics(
        ["F-1", "F-2", "F-3"],
        ["M-1"],
        {"F-1": "M-9", "F-9": "M-1"},
    )
    assert invalid["retained_count"] == 0
    assert invalid["value_retention"] == 0.0
    assert [entry["reasons"] for entry in invalid["invalid_mapping"]] == [
        ["MINIMAL_ID_NOT_IN_MINIMAL_SET"],
        ["FULL_ID_NOT_IN_FULL_SET"],
    ]
    assert invalid["unmatched_full"] == ["F-2", "F-3"]

    undefined = retention_metrics([], ["M-1"], {})
    assert undefined["value_retention"] is None
    assert undefined["impact_retention"] is None
    assert undefined["full_count"] == 0


def test_cost_and_efficiency_metrics() -> None:
    assessment = assess_budget(_budget_passes(), _budget_cost())
    cost = cost_metrics(assessment)
    assert cost["status"] == "WITHIN_TARGET"
    assert cost["evaluation_passes"] == 2
    assert cost["treatment_agent_seconds"] == pytest.approx(370.0)
    assert cost["cost_multiplier"] == pytest.approx(1.85)

    value = {
        "distinct_material_new": 3,
        "impact_counts": {"DECISIONAL_IMPACT": 1},
        "by_materiality": {"SPURIOUS": 1},
    }
    efficiency = efficiency_metrics(value, {"treatment_agent_seconds": 500.0})
    assert efficiency["distinct_material_new_per_1000_agent_seconds"] == pytest.approx(6.0)
    assert efficiency["decisive_impacts_per_1000_agent_seconds"] == pytest.approx(2.0)
    assert efficiency["spurious_per_1000_agent_seconds"] == pytest.approx(2.0)

    guarded = efficiency_metrics(value, {"treatment_agent_seconds": 0})
    assert guarded["distinct_material_new_per_1000_agent_seconds"] is None
    assert guarded["decisive_impacts_per_1000_agent_seconds"] is None
    assert guarded["spurious_per_1000_agent_seconds"] is None


def test_review_metrics() -> None:
    record = make_record()
    metrics = review_metrics(record)
    assert metrics["finding_count"] == 3
    assert metrics["value"]["total"] == 3
    assert metrics["value"]["distinct_material_new"] == 2
    assert metrics["budget"]["status"] == "WITHIN_TARGET"
    assert metrics["cost"]["status"] == "WITHIN_TARGET"
    assert metrics["efficiency"]["distinct_material_new_per_1000_agent_seconds"] == pytest.approx(
        2 / 370.0 * 1000.0
    )

    empty = review_metrics({})
    assert empty["finding_count"] == 0
    assert empty["budget"]["status"] == "MISSING_COST"
    assert empty["efficiency"]["distinct_material_new_per_1000_agent_seconds"] is None


# --- CLI ---------------------------------------------------------------------


def test_cli_help(tmp_path: Path) -> None:
    proc = run_cli("--help", cwd=tmp_path)
    assert proc.returncode == 0, proc.stderr
    assert "validate" in proc.stdout
    assert "selectivity" in proc.stdout
    assert "metrics" in proc.stdout


def test_cli_validate_exit_codes(tmp_path: Path) -> None:
    valid_path = tmp_path / "valid.json"
    valid_path.write_text(json.dumps(make_record(commit_before_reveal=True)), encoding="utf-8")
    proc = run_cli("validate", str(valid_path), cwd=tmp_path)
    assert proc.returncode == 0, proc.stderr
    payload = json.loads(proc.stdout)
    assert payload["ok"] is True
    assert payload["issues"] == []

    invalid = make_record()
    invalid["frame"]["criteria"] = []
    invalid_path = tmp_path / "invalid.json"
    invalid_path.write_text(json.dumps(invalid), encoding="utf-8")
    proc = run_cli("validate", str(invalid_path), cwd=tmp_path)
    assert proc.returncode == 1, proc.stderr
    payload = json.loads(proc.stdout)
    assert payload["ok"] is False
    assert "FRAME_INCOMPLETE" in [issue["code"] for issue in payload["issues"]]

    malformed_path = tmp_path / "malformed.json"
    malformed_path.write_text("{not json", encoding="utf-8")
    proc = run_cli("validate", str(malformed_path), cwd=tmp_path)
    assert proc.returncode == 2
    assert proc.stderr.strip()

    proc = run_cli("validate", str(tmp_path / "missing.json"), cwd=tmp_path)
    assert proc.returncode == 2
    assert proc.stderr.strip()


def test_cli_selectivity_output(tmp_path: Path) -> None:
    signals_path = tmp_path / "signals.json"
    signals_path.write_text(
        json.dumps(_signals(materiality_potential="HIGH", ambiguity="HIGH")),
        encoding="utf-8",
    )
    proc = run_cli("selectivity", str(signals_path), cwd=tmp_path)
    assert proc.returncode == 0, proc.stderr
    payload = json.loads(proc.stdout)
    assert payload["recommendation"] == "REVIEW_TWO_PASS"
    assert payload["advisory"] is True

    malformed_path = tmp_path / "bad_signals.json"
    malformed_path.write_text(json.dumps({"materiality_potential": "HIGH"}), encoding="utf-8")
    proc = run_cli("selectivity", str(malformed_path), cwd=tmp_path)
    assert proc.returncode == 2
    assert proc.stderr.strip()


def test_cli_metrics_output(tmp_path: Path) -> None:
    findings_path = tmp_path / "findings.json"
    findings_path.write_text(
        json.dumps(
            {
                "findings": [
                    _finding(
                        "F-1",
                        source="PASS_FALSIFICATION",
                        novelty="NEW",
                        materiality="MATERIAL",
                        impact="DECISIONAL_IMPACT",
                    )
                ]
            }
        ),
        encoding="utf-8",
    )
    proc = run_cli("metrics", str(findings_path), cwd=tmp_path)
    assert proc.returncode == 0, proc.stderr
    payload = json.loads(proc.stdout)
    assert payload["mode"] == "value"
    assert payload["metrics"]["total"] == 1
    assert payload["metrics"]["distinct_material_new"] == 1

    retention_path = tmp_path / "retention.json"
    retention_path.write_text(
        json.dumps(
            {
                "full_dmn_ids": ["F-1", "F-2"],
                "minimal_dmn_ids": ["M-1"],
                "mapping": {"F-1": "M-1", "F-2": "M-1"},
            }
        ),
        encoding="utf-8",
    )
    proc = run_cli("metrics", str(retention_path), cwd=tmp_path)
    assert proc.returncode == 0, proc.stderr
    payload = json.loads(proc.stdout)
    assert payload["mode"] == "retention"
    assert payload["metrics"]["retained_count"] == 2
    assert payload["metrics"]["value_retention"] == pytest.approx(1.0)

    unsupported_path = tmp_path / "unsupported.json"
    unsupported_path.write_text(json.dumps({"other": 1}), encoding="utf-8")
    proc = run_cli("metrics", str(unsupported_path), cwd=tmp_path)
    assert proc.returncode == 2
    assert proc.stderr.strip()


def test_cli_writes_nothing(tmp_path: Path) -> None:
    record_path = tmp_path / "record.json"
    record_path.write_text(json.dumps(make_record()), encoding="utf-8")
    before = {
        path.relative_to(tmp_path).as_posix(): path.read_bytes()
        for path in tmp_path.rglob("*")
        if path.is_file()
    }
    proc = run_cli("validate", str(record_path), cwd=tmp_path)
    assert proc.returncode == 0, proc.stderr
    after = {
        path.relative_to(tmp_path).as_posix(): path.read_bytes()
        for path in tmp_path.rglob("*")
        if path.is_file()
    }
    assert after == before
