"""Tests for the reference runtime materializations.

These tests validate the runtime implementations in `dev/runtime/toolcalls/`,
including the conformance criteria declared in `dev/runtime/README.md`. They are
independent of `.agents/harness/tests/`, which validates the protocol.
"""

from __future__ import annotations

import math
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(REPO_ROOT / "dev"))

from runtime.toolcalls import prompt_rendering, toolcalls_rendering  # noqa: E402
from runtime.toolcalls.budget import MaterializationCost, estimate_tokens  # noqa: E402
from runtime.toolcalls.context import ExecutionContext, SkillSource, resolve_skills  # noqa: E402

SKILLS_ROOT = REPO_ROOT / "protocol" / ".agents" / "skills"
SAMPLE_SKILLS = ["planner", "extractor", "summarizer"]


@pytest.fixture()
def context() -> ExecutionContext:
    """A realistic Execution Context built from real protocol skills."""
    return ExecutionContext(
        session_uuid="00000000-0000-0000-0000-000000000000",
        current_state="EXECUTING",
        target_phase="05-plan",
        role_to_adopt="planner",
        task_summary="Produce EXECUTION_PLAN.md from the task specification.",
        skills=resolve_skills(SAMPLE_SKILLS, SKILLS_ROOT),
        knowledge_entries=(),
        context_budget=100_000,
    )


# --- Budget -----------------------------------------------------------------


def test_estimate_tokens_ceil_rule():
    assert estimate_tokens("") == 0
    assert estimate_tokens("abcd") == 1
    assert estimate_tokens("abcde") == 2
    assert estimate_tokens("x" * 7) == math.ceil(7 / 4)


def test_cost_totals():
    cost = MaterializationCost(initial_tokens=10, deferred_tokens=5, tool_declarations=2)
    assert cost.total_tokens_if_fully_loaded == 15


# --- Context resolution ------------------------------------------------------


def test_resolve_skills_resolves_real_skills():
    skills = resolve_skills(SAMPLE_SKILLS, SKILLS_ROOT)
    assert [s.name for s in skills] == SAMPLE_SKILLS
    for skill in skills:
        assert skill.skill_md.is_file()
        assert skill.description()  # non-empty front matter description


def test_resolve_skills_rejects_unknown_name():
    with pytest.raises(FileNotFoundError):
        resolve_skills(["no-such-skill"], SKILLS_ROOT)


# --- Prompt materialization ---------------------------------------------------


def test_prompt_materialization_lists_names_without_content(context):
    prompt, cost = prompt_rendering.materialize(context)
    for name in SAMPLE_SKILLS:
        assert f"- {name}" in prompt
        # The representation carries no skill content.
        assert "# Mission" not in prompt
    assert cost.tool_declarations == 0
    assert cost.initial_tokens == estimate_tokens(prompt)
    # Deferred cost: the Worker must read every listed SKILL.md up front.
    assert cost.deferred_tokens == sum(
        estimate_tokens(s.content()) for s in context.skills
    )


# --- Tool-call materialization ------------------------------------------------


def test_declarations_come_from_front_matter(context):
    declarations = toolcalls_rendering.declare_tools(context)
    assert len(declarations) == len(SAMPLE_SKILLS)
    for declaration, skill in zip(declarations, context.skills):
        assert declaration.name == skill.name
        assert declaration.description == skill.description()


def test_toolcalls_prompt_has_declarations_without_content(context):
    prompt, cost = toolcalls_rendering.materialize(context)
    for skill in context.skills:
        assert f"tool {skill.name}: {skill.description()}" in prompt
    assert "# Mission" not in prompt
    assert cost.tool_declarations == len(SAMPLE_SKILLS)
    assert cost.initial_tokens == estimate_tokens(prompt)


def test_invoke_tool_loads_content_on_demand(context):
    skill = context.skills[0]
    assert toolcalls_rendering.invoke_tool(context, skill.name) == skill.content()


def test_invoke_tool_rejects_undeclared_name(context):
    with pytest.raises(KeyError):
        toolcalls_rendering.invoke_tool(context, "no-such-skill")


# --- Conformance criteria (runtime/README.md) ---------------------------------


def test_effective_capability_is_identical_across_materializations(context):
    """Same activated capability, byte-identical content in both."""
    up_front = prompt_rendering.load_skill_contents(context)
    on_demand = {
        skill.name: toolcalls_rendering.invoke_tool(context, skill.name)
        for skill in context.skills
    }
    assert up_front == on_demand


def test_toolcalls_defers_real_cost(context):
    """Declarations cost less up front than reading every SKILL.md."""
    _, prompt_cost = prompt_rendering.materialize(context)
    _, tool_cost = toolcalls_rendering.materialize(context)
    # Deferred (full content) is identical; the difference is the up-front
    # cost of the skills portion.
    assert tool_cost.deferred_tokens == prompt_cost.deferred_tokens
    assert tool_cost.initial_tokens < prompt_cost.initial_tokens + prompt_cost.deferred_tokens


def test_both_materializations_coexist_on_same_context(context):
    """Coexistence Rule: two representations of the same Execution Context."""
    prompt_repr, _ = prompt_rendering.materialize(context)
    tool_repr, _ = toolcalls_rendering.materialize(context)
    assert prompt_repr != tool_repr  # different representations...
    for line in (
        f"session: {context.session_uuid}",
        f"task: {context.task_summary}",
        f"context_budget: {context.context_budget}",
    ):
        assert line in prompt_repr and line in tool_repr  # ...same context
