"""Execution Context model for the reference runtime.

The Execution Context is produced and delivered by the protocol (the
Delegation Payload is its current transport). This module mirrors the
payload's fields as an in-memory structure on the runtime side of the
boundary. It introduces no new concepts: every field corresponds to a field
of the invocation payload defined in
`protocol/.agents/delegation/WORKER_DELEGATION_CONTRACT.md` (Required Invocation
Payload).
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from pathlib import Path


@dataclass(frozen=True)
class SkillSource:
    """A skill as discovered by the protocol: name plus its source file.

    The skill's capability is defined by its `SKILL.md`; the front matter
    provides `name` and `description`. The runtime reads the file only when
    a materialization requires it.
    """

    name: str
    skill_md: Path

    def description(self) -> str:
        """Extract the `description` field from the SKILL.md front matter."""
        text = self.skill_md.read_text(encoding="utf-8")
        match = re.match(r"^---\s*\n(.*?)\n---\s*\n", text, re.DOTALL)
        if not match:
            raise ValueError(f"{self.skill_md}: no front matter found")
        for line in match.group(1).splitlines():
            if line.startswith("description:"):
                return line.split(":", 1)[1].strip()
        raise ValueError(f"{self.skill_md}: no description in front matter")

    def content(self) -> str:
        """Return the full SKILL.md content (the capability definition)."""
        return self.skill_md.read_text(encoding="utf-8")


@dataclass(frozen=True)
class ExecutionContext:
    """The Execution Context as delivered to the runtime.

    Fields mirror the Delegation Payload: the task, the role and phase, the
    activated skills, the knowledge entries, and the materialized Context
    Budget for this delegation.
    """

    session_uuid: str
    current_state: str
    target_phase: str
    role_to_adopt: str
    task_summary: str
    skills: tuple[SkillSource, ...] = field(default_factory=tuple)
    knowledge_entries: tuple[str, ...] = field(default_factory=tuple)
    context_budget: int = 1000  # estimated tokens, prompt runtime convention


def resolve_skills(names: list[str], skills_root: Path) -> tuple[SkillSource, ...]:
    """Resolve skill names to their sources under a skills root.

    Mirrors the contract rule: each entry is a skill name resolvable under
    the skills directory (`protocol/.agents/delegation/WORKER_DELEGATION_CONTRACT.md`,
    `skills` field). A name that does not resolve raises, as a materialization
    must not invent a skill's content.
    """
    resolved = []
    for name in names:
        skill_md = skills_root / name / "SKILL.md"
        if not skill_md.is_file():
            raise FileNotFoundError(f"Skill not resolvable: {name} under {skills_root}")
        resolved.append(SkillSource(name=name, skill_md=skill_md))
    return tuple(resolved)
