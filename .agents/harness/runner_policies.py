"""Policy loading for the harness runner."""

from __future__ import annotations

import re
import sys
from functools import lru_cache
from pathlib import Path

_HARNESS_DIR = Path(__file__).resolve().parent
if str(_HARNESS_DIR) not in sys.path:
    sys.path.insert(0, str(_HARNESS_DIR))

from typing import Any

import runner_markdown
import runner_paths

_H1_RE = re.compile(r"^#\s+\S", re.MULTILINE)
_H2_RE = re.compile(r"^##\s+(.+?)\s*$", re.MULTILINE)
_BACKTICK_H2_RE = re.compile(r"`##\s+([^`]+?)`")

# Contract headings that never denote artifact sections: the contract's
# self-description, sections the contract prose marks as optional, and
# documentation of machinery nested inside other sections. Compared against
# every policy's pre-migration required_sections (plan 24) so that resolving
# by reference reproduces the lists the policies used to declare.
NON_NORMATIVE_SECTIONS = {
    "Purpose",  # contract self-description
    "Technical Approach",  # declared optional in the contract prose
    "Machine-readable TOML blocks",  # documents TOML blocks nested in sections
    "Rubric Evaluation",  # rubric usage documentation
    "Completion Criteria",  # contract checklist, not an artifact section
    "Relationship to project artifacts",  # contract cross-references
}


def _contract_dirs() -> list[Path]:
    """Return every directory that holds artifact contracts."""
    dirs = [runner_paths.AGENTS_DIR / "contracts"]
    dirs += sorted((runner_paths.AGENTS_DIR / "orchestrators").glob("*/contracts"))
    return [d for d in dirs if d.is_dir()]


@lru_cache(maxsize=1)
def _contract_map() -> dict[str, Path]:
    """Map artifact file name -> contract path, from contract front matter."""
    mapping: dict[str, Path] = {}
    for directory in _contract_dirs():
        for path in sorted(directory.glob("*.md")):
            try:
                meta = runner_markdown.parse_front_matter(
                    path.read_text(encoding="utf-8")
                )
            except ValueError:
                continue
            if meta.get("artifact"):
                mapping[meta["artifact"]] = path
    return mapping


def _contract_sections(contract_path: Path) -> list[str]:
    """Return the section names an artifact may have, per its contract.

    Two contract styles are supported:
    - Template style: the contract describes itself under the first H1 and the
      artifact template under a second H1; the template's ## headings are the
      candidate sections.
    - List style: a '## Required sections' section enumerates the sections as
      backticked `## Name` entries.
    """
    content = contract_path.read_text(encoding="utf-8")
    h1_matches = list(_H1_RE.finditer(content))

    if len(h1_matches) >= 2:
        template = content[h1_matches[1].start() :]
        return _H2_RE.findall(template)

    required_match = re.search(
        r"^##\s+Required sections\s*\n(.*?)(?=^##\s|\Z)",
        content,
        re.MULTILINE | re.DOTALL,
    )
    if required_match:
        return [s.strip() for s in _BACKTICK_H2_RE.findall(required_match.group(1))]

    return []


def resolve_required_sections(policy: dict[str, Any]) -> list[str]:
    """Resolve the effective required_sections for a policy.

    A policy that declares `required_sections` explicitly keeps its list
    (deliberate subset of, or opt-out from, the contract sections). Otherwise
    the list is derived by reference from the contract cited by the policy's
    `artifact` key, excluding NON_NORMATIVE_SECTIONS. Resolution fails
    closed: a missing contract or one without normative sections is a
    malformed policy.
    """
    if "required_sections" in policy:
        return policy["required_sections"] or []
    artifact = policy.get("artifact")
    if not artifact:
        return []
    contract = _contract_map().get(artifact)
    if contract is None:
        raise ValueError(
            f"Policy '{policy.get('trigger', policy.get('_source', '?'))}' cites "
            f"artifact '{artifact}' but no contract declares it"
        )
    sections = [
        s for s in _contract_sections(contract) if s not in NON_NORMATIVE_SECTIONS
    ]
    if not sections:
        raise ValueError(
            f"Contract '{contract}' for artifact '{artifact}' defines no "
            "normative sections"
        )
    return sections


def load_policy(trigger: str) -> dict[str, Any]:
    # Policies are named like H01-task-specification.md, H02-context-artifact.md, etc.
    # Require an exact prefix match "<trigger>-" to avoid ambiguous globs.
    # Policies are searched in every domain: core (H*), discovery (D*),
    # system (S*) and cross-cutting (.agents/harness/policies, e.g. H13).
    candidates = []
    for policies_dir in runner_paths.POLICIES_DIRS:
        candidates = list(policies_dir.glob(f"{trigger}-*.md"))
        if not candidates:
            candidates = list(policies_dir.glob(f"{trigger.lower()}-*.md"))
        if candidates:
            break
    if not candidates:
        raise FileNotFoundError(f"Policy not found for trigger {trigger}")
    if len(candidates) > 1:
        raise FileNotFoundError(
            f"Multiple policies found for trigger {trigger}: {', '.join(str(c) for c in candidates)}"
        )

    policy_path = candidates[0]
    content = policy_path.read_text(encoding="utf-8")
    meta = runner_markdown.parse_front_matter(content)
    meta["_source"] = str(policy_path)
    meta["required_sections"] = resolve_required_sections(meta)
    return meta
