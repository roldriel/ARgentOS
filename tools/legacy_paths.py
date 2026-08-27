"""Legacy path resolution for repository migrations (RFC-69).

Maps legacy citation paths to their single canonical target after the
``docs/`` layout migration (RFC-69, Plan A). Rules:

- every legacy path resolves to exactly one canonical target;
- more specific prefixes resolve before generic ones
  (``plans/rfc/`` before ``plans/``);
- the mapping is migration-only and must be removable;
- new references must not use legacy paths (enforced by
  ``check_plan_citations.py``).

Usage: ``resolve_legacy("plans/rfc/62-x.md")`` -> ``"docs/rfc/62-x.md"``.
Standard library only.
"""

from __future__ import annotations

# Ordered entries: more specific prefixes first. Entries ending in "/" are
# prefix matches; bare names match exactly. Each legacy path maps to exactly
# one canonical target.
LEGACY_PATHS: tuple[tuple[str, str], ...] = (
    ("plans/rfc/", "docs/rfc/"),
    ("plans/", "docs/plans/"),
    ("feature.md", "docs/plans/ec-pipeline-vision.md"),
    ("AGENTS.md", "protocol/_AGENTS.md"),
    (".agents/", "protocol/.agents/"),
    ("VERSIONING.md", "docs/VERSIONING.md"),
    ("MIGRATION.md", "docs/MIGRATION.md"),
    ("ADOPTION.md", "docs/ADOPTION.md"),
    ("AUDITORIA_DOCUMENTACION.md", "docs/AUDITORIA_DOCUMENTACION.md"),
    (
        "ARCHITECTURAL_PROBLEM_MODEL.md",
        "docs/architecture/ARCHITECTURAL_PROBLEM_MODEL.md",
    ),
    (
        "ARCHITECTURAL_DECISION_MODEL.md",
        "docs/architecture/ARCHITECTURAL_DECISION_MODEL.md",
    ),
    (
        "WORKFLOW_PROPOSAL.md",
        "docs/working/proposals/WORKFLOW_PROPOSAL.md",
    ),
    (
        "INVESTIGACION_COSTO_RECOMPUTACION_2026-08-25.md",
        "docs/working/research/INVESTIGACION_COSTO_RECOMPUTACION_2026-08-25.md",
    ),
    (
        "AUDITORIA_SISTEMA.md",
        "docs/working/audits/AUDITORIA_SISTEMA.md",
    ),
    (
        "AUDITORIA_SISTEMA_2026-08-16.md",
        "docs/working/audits/AUDITORIA_SISTEMA_2026-08-16.md",
    ),
    (
        "AUDITORIA_REUTILIZACION_2026-08-25.md",
        "docs/working/audits/AUDITORIA_REUTILIZACION_2026-08-25.md",
    ),
    (
        "ORCHESTRATION_GUIDE.md",
        "protocol/.agents/standards/orchestration/ORCHESTRATION_GUIDE.md",
    ),
)


def resolve_legacy(path: str) -> str | None:
    """Return the single canonical target for a legacy citation path.

    Returns None when the path is not a legacy path.
    """
    for legacy, target in LEGACY_PATHS:
        if legacy.endswith("/"):
            if path.startswith(legacy):
                return target + path[len(legacy):]
        elif path == legacy:
            return target
    return None


def matches_legacy(path: str) -> bool:
    """True when the path matches any legacy entry (used to detect new refs)."""
    return resolve_legacy(path) is not None
