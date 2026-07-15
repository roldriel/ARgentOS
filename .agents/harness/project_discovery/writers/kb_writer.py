"""Write project discovery results as knowledge-base entries."""

from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from ..models import DiscoveryResult

# Map discovery categories to KB entry file names and human titles.
ENTRY_CATALOG: dict[str, tuple[str, str]] = {
    "stack": ("stack.md", "Stack"),
    "dependencies": ("dependencies.md", "Dependencies"),
    "configuration": ("configuration.md", "Configuration"),
    "database": ("database.md", "Database"),
    "containers": ("containers.md", "Containers"),
    "architecture": ("architecture.md", "Architecture"),
    "business_rules": ("business_rules.md", "Business Rules"),
    "technical_debt": ("technical_debt.md", "Technical Debt"),
    "known_errors": ("known_errors.md", "Known Errors"),
    "project_flow": ("project_flow.md", "Project Flow"),
    "project_unknown": ("project_unknown.md", "Project Unknown"),
}

# Categories that require LLM synthesis in Phase 2.
SYNTHESIZED_CATEGORIES = {
    "architecture",
    "business_rules",
    "technical_debt",
    "known_errors",
    "project_flow",
}


def _format_value(value: Any) -> str:
    if isinstance(value, str):
        return value
    return repr(value)


def _build_front_matter(
    title: str,
    source_files: list[str],
    tags: list[str],
    generated_at: str,
) -> str:
    files_list = "\n".join(f'  - "{f}"' for f in sorted(set(source_files)))
    tags_list = "\n".join(f'  - "{t}"' for t in sorted(set(tags)))
    return f"""+++
artifact = "KB_DISCOVERY_ENTRY.md"
title = "{title}"
generated_at = "{generated_at}"
tags =
{tags_list}
source_files =
{files_list}
+++
"""


def write_kb_entries(
    result: DiscoveryResult,
    output_dir: Path,
    generated_at: str | None = None,
) -> list[Path]:
    """Write discovery facts as themed KB entries under ``output_dir``."""
    output_dir.mkdir(parents=True, exist_ok=True)
    generated_at = generated_at or datetime.now(timezone.utc).isoformat()

    facts_by_category: dict[str, list] = {}
    for fact in result.facts:
        facts_by_category.setdefault(fact.category, []).append(fact)

    written: list[Path] = []

    deterministic_facts = [f for f in result.facts if f.confidence == "deterministic"]

    for category, (filename, title) in ENTRY_CATALOG.items():
        if category == "project_unknown":
            continue

        facts = facts_by_category.get(category, [])
        source_files = [f.source_file for f in facts]
        tags = [f"discovery", category]

        lines: list[str] = []
        lines.append(_build_front_matter(title, source_files, tags, generated_at))
        lines.append(f"# {title}")
        lines.append("")

        if category in SYNTHESIZED_CATEGORIES:
            lines.append("## Summary")
            lines.append(
                "_This entry is reserved for LLM synthesis. "
                "Run the discovery synthesis step to populate qualitative content._"
            )
            lines.append("")

        if facts:
            lines.append("## Discovered Facts")
            lines.append("")
            for fact in facts:
                value = _format_value(fact.value)
                lines.append(f"- **{fact.key}**: {value}")
            lines.append("")
        else:
            lines.append("## Discovered Facts")
            lines.append("_No deterministic facts found for this category._")
            lines.append("")

        entry_path = output_dir / filename
        entry_path.write_text("\n".join(lines), encoding="utf-8")
        written.append(entry_path)

    # If no deterministic facts were found, add a project_unknown entry.
    if not deterministic_facts:
        unknown_filename, unknown_title = ENTRY_CATALOG["project_unknown"]
        lines = [
            _build_front_matter(
                unknown_title, [], ["discovery", "project_unknown"], generated_at
            ),
            f"# {unknown_title}",
            "",
            "## Summary",
            "_The project type could not be determined from recognizable configuration files._",
            "",
            "## Discovered Facts",
            "_No deterministic facts found. Recognized files: pyproject.toml, requirements.txt, "
            "setup.py, setup.cfg, package.json, Dockerfile, docker-compose.yml, README.md, .gitignore._",
            "",
        ]
        entry_path = output_dir / unknown_filename
        entry_path.write_text("\n".join(lines), encoding="utf-8")
        written.append(entry_path)

    return written
