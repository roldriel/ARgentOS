"""Prompt materialization (reference, existing de facto).

The current runtime materializes the Execution Context as prompt text: the
skill names travel in the Delegation Payload and the Worker reads each
`SKILL.md` before executing the phase
(`protocol/.agents/delegation/WORKER_DELEGATION_CONTRACT.md`, `skills` field: "the
Worker MUST read each skill's SKILL.md before executing the phase").

This module formalizes that practice as a materialization function so it can
coexist with — and be compared against — the tool-call materialization.
"""

from __future__ import annotations

from .budget import MaterializationCost, estimate_tokens
from .context import ExecutionContext


def render_prompt(context: ExecutionContext) -> str:
    """Render the Execution Context as the Worker's prompt text.

    The representation lists the activated skills by name with the standing
    instruction to read each `SKILL.md` before executing. It contains no
    skill content: reading is a separate, later act of the Worker.
    """
    lines = [
        f"session: {context.session_uuid}",
        f"state: {context.current_state}",
        f"phase: {context.target_phase}",
        f"role: {context.role_to_adopt}",
        f"task: {context.task_summary}",
        f"context_budget: {context.context_budget}",
    ]
    if context.knowledge_entries:
        lines.append("knowledge_entries:")
        lines.extend(f"  - {entry}" for entry in context.knowledge_entries)
    if context.skills:
        lines.append("skills:")
        for skill in context.skills:
            lines.append(f"  - {skill.name}")
        lines.append(
            "instruction: read each skill's SKILL.md before executing the phase; "
            "load references/ lazily, only when the procedure requires them."
        )
    return "\n".join(lines) + "\n"


def render_dynamic_suffix(context: ExecutionContext) -> str:
    """Render the dynamic suffix of the canonical payload (ordering v2).

    RFC-78 section 5 defines the v2 field order as stable content first and the
    dynamic suffix last. This function produces only the parameterized portion:
    the task-specific fields and the execution/session metadata. The stable
    prefix is resolved separately from the payload
    (`runtime/toolcalls/segment_resolution.py`) and is not part of the suffix.
    """
    lines = [
        "suffix: task",
        f"task: {context.task_summary}",
        "suffix: knowledge_entries",
    ]
    lines.extend(f"  - {entry}" for entry in context.knowledge_entries)
    lines.append("suffix: artifacts")
    lines.extend(f"  - {ref}" for ref in context.input_artifacts)
    lines.append("suffix: execution_metadata")
    lines.append(f"session_uuid: {context.session_uuid}")
    lines.append(f"current_state: {context.current_state}")
    lines.append("target_phase: " + ", ".join(context.phases()))
    lines.append(f"context_budget: {context.context_budget}")
    return "\n".join(lines) + "\n"


def load_skill_contents(context: ExecutionContext) -> dict[str, str]:
    """What the Worker reads up front under this materialization.

    The contract requires reading every listed skill's SKILL.md before
    executing the phase, so the deferred cost is the full content of all
    activated skills.
    """
    return {skill.name: skill.content() for skill in context.skills}


def materialize(context: ExecutionContext) -> tuple[str, MaterializationCost]:
    """Materialize the Execution Context as a prompt and report its cost.

    Initial cost: the prompt text. Deferred cost: every activated skill's
    full content, which the Worker must read before executing.
    """
    prompt = render_prompt(context)
    deferred = sum(estimate_tokens(c) for c in load_skill_contents(context).values())
    return prompt, MaterializationCost(
        initial_tokens=estimate_tokens(prompt),
        deferred_tokens=deferred,
        tool_declarations=0,
    )
