"""Contract, skill, orchestration, authority and negative tests for the
Protocol-native ``adversarial-deliberation`` capability (RFC-77, plan 120).

Self-contained by construction: these tests never read the ``protocol/`` payload
(see ``tests/AGENTS.md``). The deliberation record's rules and the skill's format
requirements are vendored here as minimal fixtures and encoded as an executable
validator, so the contract invariants (``DEL-001``..``DEL-012``) are checked
rather than merely documented.

Scope: the MVP only. Confrontation, comparative mode, voting, N jurors,
reputation, telemetry, multi-agent enforcement and Prompt Cache are out of scope
and are deliberately not tested.
"""

from __future__ import annotations

import re

import pytest


# ---------------------------------------------------------------------------
# Vocabulary (closed sets from the contract)
# ---------------------------------------------------------------------------

VERDICTS = {"VIABLE", "NOT_VIABLE", "UNDETERMINED"}
TERMINATIONS = {"VERDICT", "UNDETERMINED", "LIMIT", "NO_VALUE", "FAILURE"}
EXECUTORES = {"mismo", "distinto"}

FORBIDDEN_INDEPENDENCE_PHRASES = (
    "independencia epistemológica",
    "independientes por",
    "independent because",
    "independent verification",
    "verificación independiente",
    "independently verified",
    "independencia garantizada",
)

# Values may be written bare or wrapped in backticks (the skill's output
# template renders them as code spans), so both forms are accepted.
VERDICT_VALUE_RE = re.compile(r"^\|\s*value\s*\|\s*`?([A-Z_]+)`?\s*\|", re.MULTILINE)
TERMINATION_RE = re.compile(
    r"^\|\s*termination reason\s*\|\s*`?([A-Z_]+)`?\s*\|", re.MULTILINE
)
EXECUTORES_RE = re.compile(r"ejecutores:\s*`?([a-z]+)`?", re.IGNORECASE)

REQUIRED_SECTIONS = (
    "Header",
    "Context",
    "Pass 1",
    "Pass 2",
    "Revelation",
    "Comparative evaluation",
    "Synthesis",
    "Verdict",
    "Recommendation",
    "Orchestrator interpretation",
    "Limitations",
)


class DeliberationInvalid(Exception):
    """Raised when a deliberation record violates a contract invariant."""


REQUIRED_SECTION_HEADING_RE = {
    name: re.compile(rf"^##\s+{re.escape(name)}\s*$", re.MULTILINE)
    for name in (
        "Header",
        "Context",
        "Pass 1",
        "Pass 2",
        "Revelation",
        "Comparative evaluation",
        "Synthesis",
        "Verdict",
        "Recommendation",
        "Orchestrator interpretation",
        "Limitations",
    )
}


def _section(text: str, name: str) -> str:
    """Body of a ``## <name>`` section; "" when the heading is absent.

    Use ``REQUIRED_SECTION_HEADING_RE`` to distinguish an absent heading from a
    present-but-empty section (the contract allows a deliberately empty
    ``## Recommendation`` while still requiring the heading).
    """
    m = re.search(
        rf"^##\s+{re.escape(name)}\s*$(.*?)(?=^##\s|\Z)",
        text,
        re.MULTILINE | re.DOTALL,
    )
    return m.group(1) if m else ""


def _has_section_heading(text: str, name: str) -> bool:
    return bool(REQUIRED_SECTION_HEADING_RE[name].search(text))


def validate_deliberation_report(text: str) -> None:
    """Validate a deliberation record against the contract invariants.

    Raises ``DeliberationInvalid`` on the first violation found.
    """
    # DEL-001: every required heading is present. A section may be deliberately
    # empty (## Recommendation); a missing heading is the violation.
    for name in REQUIRED_SECTIONS:
        if not _has_section_heading(text, name):
            raise DeliberationInvalid(f"DEL-001: missing section '{name}'")

    # DEL-002: both passes declare ejecutores + received material + commitment.
    for pass_name in ("Pass 1", "Pass 2"):
        body = _section(text, pass_name)
        m = EXECUTORES_RE.search(body)
        if not m:
            raise DeliberationInvalid(f"DEL-002: {pass_name} does not declare ejecutores")
        if m.group(1).lower() not in EXECUTORES:
            raise DeliberationInvalid(
                f"DEL-002: {pass_name} has invalid ejecutores '{m.group(1)}'"
            )
        for field in ("material received", "commitment"):
            if field not in body.lower():
                raise DeliberationInvalid(
                    f"DEL-002: {pass_name} does not declare '{field}'"
                )

    # DEL-003: 'distinto' requires attributed executor difference.
    for pass_name in ("Pass 1", "Pass 2"):
        body = _section(text, pass_name)
        m = EXECUTORES_RE.search(body)
        if m and m.group(1).lower() == "distinto" and "executor:" not in body.lower():
            raise DeliberationInvalid(
                f"DEL-003: {pass_name} claims 'distinto' without executor attribution"
            )

    lowered = text.lower()

    # DEL-004: no claim of epistemological independence / independent verification.
    for phrase in FORBIDDEN_INDEPENDENCE_PHRASES:
        if phrase in lowered:
            raise DeliberationInvalid(
                f"DEL-004: forbidden independence claim ('{phrase}')"
            )

    # DEL-005: revelation recorded relative to commitment; a *declared* leakage
    # (not its negation: "neither conclusion was available before commitment")
    # must be reflected in Limitations.
    revelation = _section(text, "Revelation")
    revelation_lower = revelation.lower()
    if "commit" not in revelation_lower:
        raise DeliberationInvalid(
            "DEL-005: revelation does not record the commitment/revelation ordering"
        )
    leakage_declared = any(
        marker in revelation_lower
        for marker in ("leaked", "leakage", "filtra", "conocía antes", "was available before")
    )
    negated = any(
        marker in revelation_lower
        for marker in ("neither", "no conclusion", "not available", "ninguna")
    )
    if leakage_declared and not negated:
        limitations = _section(text, "Limitations").lower()
        if not any(
            marker in limitations
            for marker in ("leak", "leakage", "available before", "filtra", "conocía antes")
        ):
            raise DeliberationInvalid(
                "DEL-005: declared leakage is not recorded in Limitations"
            )

    # DEL-006: closed vocabulary; UNDETERMINED carries a reason.
    verdict = _section(text, "Verdict")
    vm = VERDICT_VALUE_RE.search(verdict)
    if not vm:
        raise DeliberationInvalid("DEL-006: verdict value missing")
    if vm.group(1) not in VERDICTS:
        raise DeliberationInvalid(f"DEL-006: invalid verdict '{vm.group(1)}'")
    tm = TERMINATION_RE.search(verdict)
    if not tm:
        raise DeliberationInvalid("DEL-006: termination reason missing")
    if tm.group(1) not in TERMINATIONS:
        raise DeliberationInvalid(f"DEL-006: invalid termination '{tm.group(1)}'")
    if vm.group(1) == "UNDETERMINED" and not re.search(
        r"^\|\s*reason\s*\|\s*\S", verdict, re.MULTILINE
    ):
        raise DeliberationInvalid("DEL-006: UNDETERMINED without a reason")

    # DEL-007: synthesis cites origins and declares no new content.
    synthesis = _section(text, "Synthesis").lower()
    if "origin" not in synthesis and "origen" not in synthesis:
        raise DeliberationInvalid("DEL-007: synthesis cites no origin for its relations")
    if "no new content" not in synthesis and "sin contenido nuevo" not in synthesis:
        raise DeliberationInvalid(
            "DEL-007: synthesis does not declare absence of new content"
        )

    # DEL-008: a recommendation, when present, is advisory; a deliberate absence
    # must be recorded (the contract allows either, but not an unclassified claim).
    recommendation = _section(text, "Recommendation")
    if recommendation.strip():
        rec_lower = recommendation.lower()
        absence_recorded = any(
            marker in rec_lower
            for marker in ("deliberate absence", "ausencia deliberada", "no recommendation", "sin recomendación")
        )
        if "advisory" not in rec_lower and not absence_recorded:
            raise DeliberationInvalid(
                "DEL-008: recommendation not classified as advisory"
            )

    # DEL-009 / DEL-010: the record enables nothing and authorizes nothing.
    for verb in (
        "authorizes the transition",
        "autoriza la transición",
        "this report decides",
        "este informe decide",
        "satisfies the gate",
        "satisface el gate",
        "resolves the finding",
        "resuelve el finding",
    ):
        if verb in lowered:
            raise DeliberationInvalid(f"DEL-010: forbidden authority act ('{verb}')")

    # DEL-011: limitations declared.
    if not _section(text, "Limitations").strip():
        raise DeliberationInvalid("DEL-011: limitations not declared")


# ---------------------------------------------------------------------------
# Fixture: a conformant deliberation record
# ---------------------------------------------------------------------------


def _report(
    *,
    verdict: str = "NOT_VIABLE",
    termination: str = "VERDICT",
    ejecutores: str = "mismo",
    p1_executor: str = "executor: agent-A (single instance)",
    p2_executor: str = "executor: agent-A (single instance)",
    recommendation: str = "**Advisory:** keep the candidate unchanged for now.",
    synthesis_origin: str = "origin: both passes' criteria evaluation",
    synthesis_no_new: str = (
        "no new content introduced: no external facts, evidence or material arguments added"
    ),
    revelation: str = (
        "Pass 1 committed, then Pass 2 committed; neither conclusion was available "
        "before the other pass's commitment."
    ),
    limitations: str = (
        "No epistemological independence is claimed. Same executor. No cost instrumentation."
    ),
    undetermined_reason: str | None = None,
) -> str:
    reason_row = (
        f"| reason | {undetermined_reason} |\n" if undetermined_reason is not None else ""
    )
    return f"""# Deliberation Report

## Header
- protocol_version: 11.4.0
- session: 00000000-0000-0000-0000-000000000000
- iteration/order: 01/09
- artifact: DELIBERATION_REPORT.md
- type: adversarial-deliberation
- invocation_motive: two material directions and genuine doubt about viability
- decision/question: reference to the recorded decision under deliberation
- scope: viability of candidate C-1

## Context
- frame: problem=<ref>; candidate=C-1; criteria=K-1..K-3; mode=viability; limits=2 passes, no confrontation, 1 synthesis
- evidence references: docs/rfc/77-protocol-native-adversarial-deliberation.md
- shared material: framing, criteria K-1..K-3, common evidence
- pass-specific material: posture only
- withheld until commitment: the other pass's conclusion

## Pass 1
- {p1_executor}
- ejecutores: {ejecutores}
- material received: contract, RFC-77, baseline
- withheld material: Pass 2 conclusion
- relation to previous conclusions: none
- analysis: K-1 satisfied; K-2 partially satisfied; K-3 not satisfied
- criteria evaluation: K-1 yes; K-2 partial; K-3 no
- commitment: conclusion recorded before knowing any other conclusion

## Pass 2
- {p2_executor}
- ejecutores: {ejecutores}
- material received: contract, RFC-77, baseline
- withheld material: Pass 1 conclusion
- relation to previous conclusions: none
- analysis: K-1 satisfied; K-2 not satisfied; K-3 not satisfied
- criteria evaluation: K-1 yes; K-2 no; K-3 no
- commitment: conclusion recorded before knowing any other conclusion

## Revelation
- {revelation}

## Comparative evaluation
| Criterion | Pass 1 | Pass 2 | Agreement | Supporting evidence | Unresolved disagreement |
|---|---|---|---|---|---|
| K-1 | satisfied | satisfied | agree | contract | none |
| K-2 | partial | not satisfied | disagree | RFC-77 | unresolved on scope |
| K-3 | not satisfied | not satisfied | agree | baseline | none |

## Synthesis
- convergences (derived; {synthesis_origin}): K-1 and K-3 coincide
- contradictions identified (not adjudicated): K-2
- preserved disagreement (explicit, not adjudicated): K-2 scope question remains open
- {synthesis_no_new}

## Verdict
| Field | Value |
|---|---|
| value | {verdict} |
{reason_row}| attack present? | yes |
| executors | {ejecutores} |
| shared material | framing, criteria, common evidence |
| criteria | K-1..K-3 |
| not done | no confrontation; no external verification |
| reasons per criterion | K-1 satisfied; K-2 disputed; K-3 not satisfied |
| disagreement | K-2 preserved, not adjudicated |
| relation to each pass | coincides with Pass 2; diverges from Pass 1 |
| limitations | relative to available evidence; same executor when declared so |
| termination reason | {termination} |

## Recommendation
{recommendation}

## Orchestrator interpretation
- interpretation: the verdict is advisory evidence; K-2 remains unresolved
- unresolved: the K-2 scope question
- escalation required: no
- human decision required: no

## Limitations
{limitations}
"""


def _clear_section(text: str, name: str) -> str:
    """Remove the section *and its heading* (used to test DEL-001)."""
    return re.sub(
        rf"^##\s+{re.escape(name)}\s*$.*?(?=^##\s|\Z)",
        "",
        text,
        flags=re.MULTILINE | re.DOTALL,
    )


def _empty_section(text: str, name: str) -> str:
    """Keep the heading, empty the body (used to test body-level invariants)."""
    return re.sub(
        rf"(^##\s+{re.escape(name)}\s*$).*?(?=^##\s|\Z)",
        r"\1\n",
        text,
        flags=re.MULTILINE | re.DOTALL,
    )


# ---------------------------------------------------------------------------
# Contract tests
# ---------------------------------------------------------------------------


def test_contract_valid_report_passes():
    validate_deliberation_report(_report())


@pytest.mark.parametrize("section", REQUIRED_SECTIONS)
def test_contract_each_required_section_is_mandatory(section):
    with pytest.raises(DeliberationInvalid, match=f"missing section '{section}'"):
        validate_deliberation_report(_clear_section(_report(), section))


@pytest.mark.parametrize("value", sorted(VERDICTS))
def test_contract_all_valid_verdicts_accepted(value):
    reason = "insufficient evidence" if value == "UNDETERMINED" else None
    validate_deliberation_report(_report(verdict=value, undetermined_reason=reason))


def test_contract_undetermined_without_reason_rejected():
    with pytest.raises(DeliberationInvalid, match="UNDETERMINED without a reason"):
        validate_deliberation_report(_report(verdict="UNDETERMINED"))


def test_contract_invalid_verdict_rejected():
    with pytest.raises(DeliberationInvalid, match="invalid verdict"):
        validate_deliberation_report(_report(verdict="MAYBE"))


def test_contract_missing_verdict_value_rejected():
    text = _report().replace("| value | NOT_VIABLE |", "| value |  |")
    with pytest.raises(DeliberationInvalid, match="verdict value missing"):
        validate_deliberation_report(text)


@pytest.mark.parametrize("value", sorted(TERMINATIONS))
def test_contract_all_valid_terminations_accepted(value):
    validate_deliberation_report(_report(termination=value))


def test_contract_invalid_termination_rejected():
    with pytest.raises(DeliberationInvalid, match="invalid termination"):
        validate_deliberation_report(_report(termination="GAVE_UP"))


@pytest.mark.parametrize("value", sorted(EXECUTORES))
def test_contract_valid_provenance_values_accepted(value):
    p1 = "executor: agent-A (separate context)"
    p2 = "executor: agent-A (separate context)" if value == "mismo" else "executor: agent-B"
    validate_deliberation_report(_report(ejecutores=value, p1_executor=p1, p2_executor=p2))


def test_contract_invalid_provenance_value_rejected():
    text = _report().replace("ejecutores: mismo", "ejecutores: mixed", 1)
    with pytest.raises(DeliberationInvalid, match="invalid ejecutores"):
        validate_deliberation_report(text)


def test_contract_missing_provenance_rejected():
    text = _report().replace("- ejecutores: mismo\n", "", 1)
    with pytest.raises(DeliberationInvalid, match="does not declare ejecutores"):
        validate_deliberation_report(text)


def test_contract_recommendation_must_be_advisory():
    with pytest.raises(DeliberationInvalid, match="not classified as advisory"):
        validate_deliberation_report(
            _report(recommendation="Do exactly this and nothing else.")
        )


def test_contract_recommendation_absence_is_recorded_not_omitted():
    """A deliberate absence MUST be recorded, so an empty body is valid but the
    heading cannot be dropped."""
    base = _report(recommendation="No recommendation emitted (deliberate absence).")
    validate_deliberation_report(base)
    # An empty body with the heading present is still valid (deliberate absence).
    validate_deliberation_report(_empty_section(base, "Recommendation"))
    # Dropping the heading entirely is a DEL-001 violation.
    with pytest.raises(DeliberationInvalid, match="missing section 'Recommendation'"):
        validate_deliberation_report(_clear_section(base, "Recommendation"))


def test_contract_synthesis_must_cite_origin():
    with pytest.raises(DeliberationInvalid, match="cites no origin"):
        validate_deliberation_report(_report(synthesis_origin="derived"))


def test_contract_synthesis_must_declare_no_new_content():
    with pytest.raises(DeliberationInvalid, match="absence of new content"):
        validate_deliberation_report(_report(synthesis_no_new="nothing further"))


def test_contract_missing_pass_commitment_rejected():
    text = _report().replace(
        "- commitment: conclusion recorded before knowing any other conclusion", "", 1
    )
    with pytest.raises(DeliberationInvalid, match="does not declare 'commitment'"):
        validate_deliberation_report(text)


def test_contract_missing_limitations_heading_rejected():
    with pytest.raises(DeliberationInvalid, match="missing section 'Limitations'"):
        validate_deliberation_report(_clear_section(_report(), "Limitations"))


def test_contract_empty_limitations_body_rejected():
    """The heading exists but the body is empty: DEL-011, not DEL-001."""
    text = _empty_section(_report(), "Limitations")
    assert _has_section_heading(text, "Limitations")
    with pytest.raises(DeliberationInvalid, match="DEL-011: limitations not declared"):
        validate_deliberation_report(text)


# ---------------------------------------------------------------------------
# Skill format tests (vendored minimal fixture: payload-independent)
# ---------------------------------------------------------------------------

# Minimal conformant skill fixture mirroring the format contract of
# `.agents/skills/README.md`, plus the adversarial-deliberation-specific rules.
SKILL_FIXTURE = """---
name: adversarial-deliberation
description: Produce one attributed adversarial evaluation pass over a candidate decision. Use when the Orchestrator invokes adversarial deliberation on a decision whose viability is genuinely in doubt.
when_to_activate: The Orchestrator has invoked adversarial deliberation with a declared frame and an assigned posture.
when_not: The task is verification, rubric review, single-proposal critique, or the decision itself.
---

# Mission
Produce one attributed evaluation pass. Product is evidence, never a decision.

# Protocol Boundary
This skill grants no authority or permissions.

# Safety Rules
* Never claim epistemic independence.
* A pass MUST NOT invoke adversarial deliberation again and MUST NOT delegate to another Worker.
* No new facts in the synthesis.

# Workflow
1. Declare frame and posture.
2. Record material received.
3. Commit the conclusion.

# Output Format
Sections of the deliberation report.
"""

SKILL_REQUIRED_FRONT_MATTER = ("name:", "description:", "when_to_activate:", "when_not:")
SKILL_REQUIRED_SECTIONS = (
    "# Mission",
    "# Protocol Boundary",
    "# Safety Rules",
    "# Workflow",
    "# Output Format",
)


def _skill_front_matter(text: str) -> str:
    return text.split("---")[1]


def test_skill_front_matter_is_complete():
    front = _skill_front_matter(SKILL_FIXTURE)
    for key in SKILL_REQUIRED_FRONT_MATTER:
        assert key in front, f"front matter missing {key}"


def test_skill_name_matches_directory_convention():
    front = _skill_front_matter(SKILL_FIXTURE)
    assert re.search(r"^name:\s*adversarial-deliberation\s*$", front, re.MULTILINE)


def test_skill_description_states_capability_and_conditions():
    front = _skill_front_matter(SKILL_FIXTURE)
    description = re.search(r"^description:\s*(.+)$", front, re.MULTILINE).group(1)
    assert len(description) > 80, "description too thin to state capability + conditions"
    assert "use when" in description.lower(), "description lacks conditions of use"


def test_skill_declares_no_authority():
    assert "grants no authority or permissions" in SKILL_FIXTURE.lower()


def test_skill_has_required_sections():
    for section in SKILL_REQUIRED_SECTIONS:
        assert section in SKILL_FIXTURE, f"skill missing section {section}"


def test_skill_prohibits_independence_claims():
    assert "never claim epistemic independence" in SKILL_FIXTURE.lower()


def test_skill_prohibits_recursion_and_delegation():
    text = SKILL_FIXTURE.lower()
    assert "must not invoke adversarial deliberation again" in text
    assert "must not delegate to another worker" in text


# ---------------------------------------------------------------------------
# Orchestration tests
# ---------------------------------------------------------------------------


def test_orchestration_two_passes_are_recorded():
    text = _report()
    assert _section(text, "Pass 1").strip()
    assert _section(text, "Pass 2").strip()


def test_orchestration_same_executor_provenance_declared():
    validate_deliberation_report(_report(ejecutores="mismo"))


def test_orchestration_distinct_executor_provenance_declared():
    validate_deliberation_report(
        _report(
            ejecutores="distinto",
            p1_executor="executor: agent-A (separate context)",
            p2_executor="executor: agent-B (separate context)",
        )
    )


def test_orchestration_commitment_precedes_revelation():
    assert "before" in _section(_report(), "Revelation").lower()


def test_orchestration_comparative_evaluation_is_per_criterion():
    body = _section(_report(), "Comparative evaluation")
    for criterion in ("K-1", "K-2", "K-3"):
        assert criterion in body
    assert "disagreement" in body.lower()


def test_orchestration_disagreement_is_preserved_not_adjudicated():
    synthesis = _section(_report(), "Synthesis").lower()
    assert "not adjudicated" in synthesis
    assert "preserved disagreement" in synthesis


def test_orchestration_verdict_and_termination_present():
    verdict = _section(_report(), "Verdict")
    assert VERDICT_VALUE_RE.search(verdict)
    assert TERMINATION_RE.search(verdict)


def test_orchestration_optional_recommendation_present():
    assert "advisory" in _section(_report(), "Recommendation").lower()


def test_orchestration_interpretation_is_separate_from_passes():
    text = _report()
    interpretation = _section(text, "Orchestrator interpretation")
    assert "advisory" in interpretation.lower()
    assert "Orchestrator interpretation" not in _section(text, "Pass 1")


# ---------------------------------------------------------------------------
# Authority tests
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    "claim",
    [
        "this report authorizes the transition",
        "este informe decide el resultado",
        "the report satisfies the gate",
        "el informe resuelve el finding",
    ],
)
def test_authority_claims_are_rejected(claim):
    with pytest.raises(DeliberationInvalid, match="forbidden authority act"):
        validate_deliberation_report(_report(limitations=claim))


def test_authority_verdict_does_not_transition_state():
    text = _report()
    assert "state.json" not in text
    validate_deliberation_report(text)


def test_authority_recommendation_is_not_a_decision():
    recommendation = _section(_report(), "Recommendation").lower()
    assert "advisory" in recommendation
    assert "decides" not in recommendation


# ---------------------------------------------------------------------------
# Context tests
# ---------------------------------------------------------------------------


def test_context_declares_shared_and_pass_specific_material():
    context = _section(_report(), "Context").lower()
    assert "shared material" in context
    assert "pass-specific material" in context
    assert "withheld until commitment" in context


def test_context_both_passes_declare_received_material():
    text = _report()
    for name in ("Pass 1", "Pass 2"):
        assert "material received" in _section(text, name).lower()


def test_context_second_pass_declares_withheld_conclusion():
    assert "conclusion" in _section(_report(), "Pass 2").lower()


# ---------------------------------------------------------------------------
# Negative tests
# ---------------------------------------------------------------------------


def test_negative_fake_distinto_without_attribution():
    text = _report(ejecutores="distinto").replace("- executor:", "- attribution:")
    with pytest.raises(DeliberationInvalid, match="without executor attribution"):
        validate_deliberation_report(text)


@pytest.mark.parametrize("phrase", FORBIDDEN_INDEPENDENCE_PHRASES)
def test_negative_independence_claim_rejected(phrase):
    with pytest.raises(DeliberationInvalid, match="forbidden independence claim"):
        validate_deliberation_report(_report(limitations=phrase))


def test_negative_leaked_first_conclusion_must_be_declared_in_limitations():
    text = _report(
        revelation="Pass 2 leaked: it had Pass 1's conclusion available before its commitment.",
        limitations="Same executor. No cost instrumentation.",
    )
    with pytest.raises(
        DeliberationInvalid, match="declared leakage is not recorded in Limitations"
    ):
        validate_deliberation_report(text)


def test_negative_leaked_conclusion_accepted_when_declared():
    text = _report(
        revelation="Pass 2 leaked: it had Pass 1's conclusion available before its commitment.",
        limitations="Declared leakage: the first conclusion was available before commitment.",
    )
    validate_deliberation_report(text)


def test_negative_unauthorized_decision_claim_rejected():
    with pytest.raises(DeliberationInvalid, match="forbidden authority act"):
        validate_deliberation_report(_report(recommendation="**Advisory:** este informe decide el resultado"))


def test_negative_recursive_invocation_prohibited_by_skill():
    assert "must not invoke adversarial deliberation again" in SKILL_FIXTURE.lower()


def test_negative_comparative_mode_values_are_not_verdicts():
    for value in ("PREFERRED_A", "PREFERRED_B", "TIE"):
        with pytest.raises(DeliberationInvalid, match="invalid verdict"):
            validate_deliberation_report(_report(verdict=value))


def test_negative_voting_is_not_implemented():
    text = _report()
    assert "majority" not in text.lower()
    assert "quorum" not in text.lower()
    validate_deliberation_report(text)


def test_negative_confrontation_is_out_of_scope():
    text = _report()
    assert "round 2" not in text.lower()
    assert "rebuttal" not in text.lower()
    validate_deliberation_report(text)
