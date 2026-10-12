"""Dogfood: the effect frontier and the resource ceiling over the real repository (plan 159).

This module is an **anchored test** in the sense of ``tests/AGENTS.md``: it reads the
live working tree on purpose, and only reads it. A synthetic repository cannot
express what it protects — that the operational policy, the canonical plan template
and the runtime enforcement of the effect and resource axes agree with each other
and with the one effect vocabulary this repository already uses.

Its stability contract is the documented one: it may name canonical paths, artifact
numbers and statuses of the real repository, so it is updated when that canonical
state legitimately changes. It is not portable and is not meant to be.

Nothing here mutates repository state.
"""

from __future__ import annotations

import re
from pathlib import Path

from runtime.orchestrator import host as host_module
from runtime.orchestrator.autonomy import (
    EFFECT_AUTHORIZED_BY,
    EFFECT_BEARING_ACTION_CLASSES,
    EFFECT_KINDS,
    EFFECT_STATUSES,
    EXECUTE_AUTHORIZED_TASK,
    AutonomyEnvelope,
)
from runtime.orchestrator.observation import (
    declared_effects_section_present,
    observe,
    parse_declared_effects,
)
from runtime.orchestrator.store import OrchestratorStore
from tools.check_session_artifacts import (
    AUTHORIZED_BY as PROTOCOL_AUTHORIZED_BY,
    EFFECT_KINDS as PROTOCOL_EFFECT_KINDS,
    EFFECT_STATUSES as PROTOCOL_EFFECT_STATUSES,
)

REPO_ROOT = Path(__file__).resolve().parents[1]

POLICY = ".agents/policies/supervised-autonomous-execution.md"
TEMPLATE = "docs/plans/_TEMPLATE.md"
CONVENTIONS = "docs/CONVENTIONS.md"
ADR = "docs/adr/19-autonomy-envelope-authority.md"

#: The Change that materialized this frontier.
PLAN = 159


def _read(relative: str) -> str:
    return (REPO_ROOT / relative).read_text(encoding="utf-8")


def _plan_path() -> Path:
    matches = sorted((REPO_ROOT / "docs" / "plans").glob(f"{PLAN:03d}-*.md"))
    assert matches, f"plan {PLAN} artifact not found"
    return matches[0]


# --------------------------------------------------------------------------- #
# One vocabulary, shared — never a second taxonomy
# --------------------------------------------------------------------------- #


def test_the_runtime_and_the_checker_share_exactly_one_effect_vocabulary():
    """The adopted DEV vocabulary is the one the repository already verified.

    The Protocol session checker and the orchestrator frontier must name the same
    classes, the same authorizers and the same statuses. A second taxonomy is the
    failure this asserts against, so the comparison is exact and not a subset.
    """
    assert tuple(sorted(EFFECT_KINDS)) == tuple(sorted(PROTOCOL_EFFECT_KINDS))
    assert tuple(sorted(EFFECT_AUTHORIZED_BY)) == tuple(sorted(PROTOCOL_AUTHORIZED_BY))
    assert tuple(sorted(EFFECT_STATUSES)) == tuple(sorted(PROTOCOL_EFFECT_STATUSES))


def test_the_policy_declares_the_adopted_vocabulary_verbatim():
    text = _read(POLICY)
    for effect_class in EFFECT_KINDS:
        assert f"`{effect_class}`" in text, effect_class
    for authorized_by in EFFECT_AUTHORIZED_BY:
        assert f"`{authorized_by}`" in text, authorized_by
    for status in EFFECT_STATUSES:
        assert f"`{status}`" in text, status


def test_the_template_declares_the_adopted_vocabulary_and_no_more():
    text = _read(TEMPLATE)
    section = text.split("## Efectos declarados", 1)[1].split("## Criterios de salida", 1)[0]
    for effect_class in EFFECT_KINDS:
        assert effect_class in section, effect_class
    # The template used to say the vocabulary was NOT adopted. That sentence cannot
    # survive the adoption: leaving it would document the opposite of the norm.
    assert "no está adoptado" not in section
    assert "no fue adoptado" not in section


# --------------------------------------------------------------------------- #
# Policy ↔ enforcement in lockstep
# --------------------------------------------------------------------------- #


def test_the_policy_states_effect_admission_and_the_resource_ceiling():
    text = _read(POLICY)
    for heading in (
        "### 1.5 Effect admission (plan 159; ADR-19 `AE-2`, `AE-3`, `AE-4`)",
        "### 3.1 The resource ceiling (plan 159; ADR-19 `AE-6`, decision `D-3`)",
    ):
        assert heading in text, heading
    # Both axes are inside the gate the policy describes, in order.
    assert "AND every declared effect is admitted" in text
    assert "AND the declared resource ceiling is not exhausted" in text
    # The two rules the falsification suite proves are stated as rules.
    assert "is never read as authorized" in text
    assert "resource ceiling      ≠   authorization" in text
    assert "produces no authority" in text


def test_every_effect_stop_the_policy_names_is_reachable_in_the_vocabulary():
    """The policy's effect frontiers are stops the frontier really produces.

    ``STOP_AUTHORITY_REQUIRED`` is the single effect stop: an unadmitted effect is
    always a human decision (unknown class, unauthorized status, unresolvable
    reference, or an unread declaration). The assertion is that the policy does not
    promise an effect stop the code cannot reach.
    """
    from runtime.orchestrator.autonomy import STOP_AUTHORITY_REQUIRED

    text = _read(POLICY)
    assert "produces `STOP` + `REQUIRES_HUMAN`" in text
    assert STOP_AUTHORITY_REQUIRED in text

def test_the_enforcement_lives_in_the_host_before_the_delegation():
    """Structural claim, read as source text: the gate precedes the effect.

    The same protection the plan 138 dogfood asserts for the scope axis, asserted
    for the effect axis: the refusal cannot move after the delegation without
    failing here.
    """
    source = (REPO_ROOT / "runtime" / "orchestrator" / "host.py").read_text(
        encoding="utf-8"
    )
    gate = source.index("def _apply_autonomy_gate")
    delegation = source.index("def _execute_delegation")
    assert gate < delegation
    # The steps a derivable before this Change introduced are present in the gate.
    assert "_autonomy_effects(action.kind, observation)" in source
    assert "resource_required=_autonomy_consumes_delegation(action.kind)" in source
    # And the two actions that may produce an effect are the frontier's own set.
    assert host_module._AUTONOMY_EFFECT_BEARING_ACTIONS == frozenset({"RUN_IMPLEMENTATION_TASK"})


def test_the_frontier_and_the_host_agree_on_which_actions_carry_effects():
    """A drift between the two would leave an effect-bearing action unadmitted."""
    from runtime.orchestrator.host import _AUTONOMY_CLASS_BY_ACTION, RUN_IMPLEMENTATION_TASK

    host_classes = {
        _AUTONOMY_CLASS_BY_ACTION[action]
        for action in host_module._AUTONOMY_EFFECT_BEARING_ACTIONS
    }
    assert host_classes == EFFECT_BEARING_ACTION_CLASSES
    assert _AUTONOMY_CLASS_BY_ACTION[RUN_IMPLEMENTATION_TASK] == EXECUTE_AUTHORIZED_TASK


# --------------------------------------------------------------------------- #
# The normative record
# --------------------------------------------------------------------------- #


def test_the_authority_act_is_recorded_without_rewriting_the_previous_one():
    """The 2026-10-07 act is preserved; the adoption is an amendment."""
    adr = _read(ADR)
    assert "### Amendment Log" in adr
    assert "2026-10-07" in adr
    assert "2026-10-11" in adr
    assert "`OPD-1`" in adr and "`OPD-2`" in adr
    # The previous act's invariants remain, and the new work is marked implemented.
    assert "AE-10" in adr
    conventions = _read(CONVENTIONS)
    assert "Modelo de autonomía — decisiones de autoridad del Plan 151" in conventions
    assert (
        "Modelo de autonomía — vocabulario de efectos y techo de recurso "
        "(adoptado 2026-10-11)" in conventions
    )
    assert "`resource ceiling ≠ authorization`" in conventions


def test_the_ceiling_is_not_a_field_of_the_autonomy_envelope():
    """`AE-6` at the type level: the operational axis is outside the authorization."""
    assert not hasattr(
        AutonomyEnvelope(task="t", scope_paths=("a",), declaration_present=True),
        "resource_ceiling",
    )
    source = (REPO_ROOT / "runtime" / "orchestrator" / "autonomy.py").read_text(
        encoding="utf-8"
    )
    envelope_block = source.split("class AutonomyEnvelope", 1)[1].split(
        "def _normalize_path", 1
    )[0]
    assert "resource_ceiling" not in envelope_block
    assert "declared_effects" in envelope_block


# --------------------------------------------------------------------------- #
# This very Change declares its own effects — and the reader is the runtime's
# --------------------------------------------------------------------------- #


def test_the_plan_of_this_change_reads_through_the_real_parser():
    text = _plan_path().read_text(encoding="utf-8")
    assert declared_effects_section_present(text) is True
    # The Change declares the absence of out-of-frontier effects with a negative
    # row, so the parser yields no effect and the frontier has nothing to admit.
    assert parse_declared_effects(text) == ()


def test_the_ceiling_of_this_change_is_declared_and_positive():
    observation = observe(REPO_ROOT, PLAN, OrchestratorStore(REPO_ROOT))
    assert observation.agent_task.ceiling_declared is True
    assert observation.agent_task.resource_ceiling is not None
    assert observation.agent_task.resource_ceiling > 0
    assert observation.agent_task.ceiling_gap == ""


def test_the_declared_effects_of_this_change_admit_cleanly():
    """The frontier over this Change's own declaration: nothing to refuse."""
    from runtime.orchestrator.host import _autonomy_envelope

    observation = observe(REPO_ROOT, PLAN, OrchestratorStore(REPO_ROOT))
    _declaration, bounded = _autonomy_envelope(observation, PLAN)
    assert bounded.declared is True, "this Change declares task and scope"
    assert bounded.declared_effects == ()
    assert observation.declared_effects_unresolved is False


# --------------------------------------------------------------------------- #
# Scope containment of the change itself
# --------------------------------------------------------------------------- #


def test_no_second_effect_checker_or_taxonomy_was_introduced():
    """The Change adds no registry, no second checker and no parallel taxonomy."""
    for forbidden in (
        "runtime/orchestrator/effects.py",
        "runtime/orchestrator/effect_store.py",
        "tools/check_effects.py",
        "tools/check_autonomy_effects.py",
        "docs/autonomy-effects.md",
        ".project/orchestrator/effects-registry.json",
    ):
        assert not (REPO_ROOT / forbidden).exists(), forbidden
    # The effect vocabulary is declared once in the runtime.
    hits = [
        path
        for path in (REPO_ROOT / "runtime").rglob("*.py")
        if re.search(r"^EFFECT_KINDS\s*[:=]", path.read_text(encoding="utf-8"), re.M)
    ]
    assert [path.name for path in hits] == ["autonomy.py"], hits
