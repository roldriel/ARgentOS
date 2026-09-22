"""Execution Context model for the reference runtime.

The Execution Context is produced and delivered by the protocol (the Delegation
Payload is its current transport). This module mirrors the payload's fields as an
in-memory structure on the runtime side of the boundary.

Field coverage (RFC-78, section 6 / HD-7). The Delegation Payload transports
thirteen fields
(`protocol/.agents/delegation/WORKER_DELEGATION_CONTRACT.md:Required Invocation Payload`).
Every one of them is accounted for here, by one of two treatments:

- **Context fields** (participate in the delivered context, the semantic
  identity derivation and the representation): `session_uuid`,
  `current_state`, `target_phase`, `role_to_adopt`, `task_summary`,
  `knowledge_entries`, `skills`, `context_budget`, `harness_policy`,
  `profile`, `input_artifacts`.
- **Execution metadata** (delivered to the runtime, not semantic context):
  `communication_style` and `technical_approach`.

`input_artifacts` participates through its **references**; the artifact content
never enters the stable prefix
(`protocol/.agents/standards/context/CONTEXT.md:2` forbids including full
previous-session artifacts, and full artifacts are not stable content). The
references are carried because two delegations that receive different artifact
sets are different contexts: omitting them would let two distinct delivered
compositions share one `SemanticContextIdentity` — a false hit, which the
governing policy forbids (RFC-78, section 6).

Execution metadata is represented because the delivered payload carries it, but
it does not participate in the semantic identity: it changes the Worker's output
format and its selected technical practices, not the meaning of the delivered
context (RFC-78, PC-004).
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

    Context fields mirror the Delegation Payload; `communication_style` and
    `technical_approach` are execution metadata carried alongside (RFC-78,
    section 6). `target_phase`, `harness_policy` and `input_artifacts` are
    tuples so the delivered sequence is represented as delivered and the
    identity derivation stays deterministic.
    """

    session_uuid: str
    current_state: str
    target_phase: tuple[str, ...] | str
    role_to_adopt: str
    task_summary: str
    skills: tuple[SkillSource, ...] = field(default_factory=tuple)
    knowledge_entries: tuple[str, ...] = field(default_factory=tuple)
    context_budget: int = 1000  # estimated tokens, prompt runtime convention
    # --- fields reconciled by RFC-78 section 6 / HD-7 ------------------------
    harness_policy: tuple[str, ...] | str = ()
    profile: str | None = None
    input_artifacts: tuple[str, ...] = field(default_factory=tuple)
    # --- execution metadata (not semantic context) --------------------------
    communication_style: str | None = None
    technical_approach: str | None = None

    def phases(self) -> tuple[str, ...]:
        """The target phase modules as a tuple, accepting a bare string."""
        if isinstance(self.target_phase, str):
            return (self.target_phase,) if self.target_phase else ()
        return tuple(self.target_phase)

    def policies(self) -> tuple[str, ...]:
        """The harness policies as a tuple, accepting a bare string."""
        if isinstance(self.harness_policy, str):
            return (self.harness_policy,) if self.harness_policy else ()
        return tuple(self.harness_policy)


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
