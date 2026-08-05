"""Tool-call materialization (second materialization).

A materialization of the Execution Context distinct from prompt text
injection: each activated skill is represented as an invocable tool
declaration (name + description, taken from the SKILL.md front matter), and
the skill's content is obtained on demand by invoking the tool, never up
front. This is the "Tool Calls" rendering variant
(`plans/rfc/14-prompt-rendering-model.md`, §Rendering Variants: "¿Qué parte
del Execution Context se representa como capacidades invocables en lugar de
texto leído?") and the future-runtime direction already anticipated by
RFC-00YM (`plans/rfc/15-skill-materialization-model.md`, §Conceptual Model:
invocable tools).

Conformance with the conceptual model:

- Represents without altering: the declarations carry only the skill's own
  name and description; invocation returns the SKILL.md content verbatim.
- Effective capability: every skill in the Execution Context is invocable
  during execution; the activated capability's content is byte-identical to
  what the prompt materialization makes the Worker read.
- No pipeline feedback: this module consumes an already-built
  ExecutionContext and changes nothing about its construction.
- Budget respected: the cost is reported in the runtime's declared dual
  unit (estimated tokens + tool declaration count; see `.budget`).
"""

from __future__ import annotations

from dataclasses import dataclass

from .budget import MaterializationCost, estimate_tokens
from .context import ExecutionContext


@dataclass(frozen=True)
class ToolDeclaration:
    """An invocable representation of a skill: name plus description.

    Equivalent to the declaration a tool-capable runtime would register for
    the model; it carries the capability's identity and purpose, not its
    content.
    """

    name: str
    description: str

    def render(self) -> str:
        """Render the declaration as it would appear to the runtime."""
        return f"tool {self.name}: {self.description}"


def declare_tools(context: ExecutionContext) -> tuple[ToolDeclaration, ...]:
    """Represent every activated skill as a tool declaration.

    The declaration text comes from the skill's own SKILL.md front matter:
    the runtime represents the capability, it does not paraphrase it.
    """
    return tuple(
        ToolDeclaration(name=skill.name, description=skill.description())
        for skill in context.skills
    )


def invoke_tool(context: ExecutionContext, name: str) -> str:
    """Invoke a tool: load the skill's content on demand.

    This is the deferred act of the materialization: the content is paid
    only when invoked. A name not present in the Execution Context raises —
    the runtime cannot materialize a capability the protocol did not
    deliver.
    """
    for skill in context.skills:
        if skill.name == name:
            return skill.content()
    raise KeyError(f"Tool not declared by the Execution Context: {name}")


def render_prompt(context: ExecutionContext) -> str:
    """Render the Execution Context as prompt text with tool declarations.

    Same delivered fields as the prompt materialization; the skills portion
    is represented as invocable declarations instead of read-up-front names.
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
    declarations = declare_tools(context)
    if declarations:
        lines.append("tools:")
        for declaration in declarations:
            lines.append(f"  - {declaration.render()}")
        lines.append(
            "instruction: invoke a tool to obtain the skill's content, "
            "only when the execution requires that capability."
        )
    return "\n".join(lines) + "\n"


def materialize(context: ExecutionContext) -> tuple[str, MaterializationCost]:
    """Materialize the Execution Context as tool calls and report its cost.

    Initial cost: the prompt text, which includes one declaration per skill
    (name + description) and no skill content. Deferred cost: the full
    content of every skill, paid only if its tool is invoked.
    """
    prompt = render_prompt(context)
    deferred = sum(estimate_tokens(skill.content()) for skill in context.skills)
    return prompt, MaterializationCost(
        initial_tokens=estimate_tokens(prompt),
        deferred_tokens=deferred,
        tool_declarations=len(declare_tools(context)),
    )
