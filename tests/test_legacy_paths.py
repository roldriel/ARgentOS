"""Tests for tools/legacy_paths.py (RFC-69 legacy mapping infrastructure)."""

from __future__ import annotations

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]

import legacy_paths as lp  # noqa: E402


def test_more_specific_prefix_resolves_first() -> None:
    assert lp.resolve_legacy("plans/rfc/68-architecture-evolution-workflow.md") == (
        "docs/rfc/68-architecture-evolution-workflow.md"
    )
    assert lp.resolve_legacy("plans/82-architecture-evolution-workflow.md") == (
        "docs/plans/82-architecture-evolution-workflow.md"
    )


def test_plans_index_maps_to_plans_index() -> None:
    assert lp.resolve_legacy("plans/INDEX.md") == "docs/plans/INDEX.md"


def test_bare_root_models_map_to_architecture() -> None:
    assert lp.resolve_legacy("ARCHITECTURAL_PROBLEM_MODEL.md") == (
        "docs/architecture/ARCHITECTURAL_PROBLEM_MODEL.md"
    )
    assert lp.resolve_legacy("ARCHITECTURAL_DECISION_MODEL.md") == (
        "docs/architecture/ARCHITECTURAL_DECISION_MODEL.md"
    )


def test_bare_working_docs_map_to_working() -> None:
    assert lp.resolve_legacy("WORKFLOW_PROPOSAL.md") == (
        "docs/working/proposals/WORKFLOW_PROPOSAL.md"
    )
    assert lp.resolve_legacy(
        "INVESTIGACION_COSTO_RECOMPUTACION_2026-08-25.md"
    ) == "docs/working/research/INVESTIGACION_COSTO_RECOMPUTACION_2026-08-25.md"
    assert lp.resolve_legacy("AUDITORIA_SISTEMA.md") == (
        "docs/working/audits/AUDITORIA_SISTEMA.md"
    )
    assert lp.resolve_legacy("AUDITORIA_SISTEMA_2026-08-16.md") == (
        "docs/working/audits/AUDITORIA_SISTEMA_2026-08-16.md"
    )
    assert lp.resolve_legacy("AUDITORIA_REUTILIZACION_2026-08-25.md") == (
        "docs/working/audits/AUDITORIA_REUTILIZACION_2026-08-25.md"
    )


def test_feature_md_maps_to_new_vision_location() -> None:
    assert lp.resolve_legacy("feature.md") == (
        "docs/plans/ec-pipeline-vision.md"
    )


def test_legacy_payload_mappings_preserved() -> None:
    assert lp.resolve_legacy("AGENTS.md") == "protocol/_AGENTS.md"
    assert lp.resolve_legacy(".agents/INDEX.md") == "protocol/.agents/INDEX.md"
    assert lp.resolve_legacy("VERSIONING.md") == "docs/VERSIONING.md"
    assert lp.resolve_legacy("ORCHESTRATION_GUIDE.md") == (
        "protocol/.agents/standards/orchestration/ORCHESTRATION_GUIDE.md"
    )


def test_unmapped_path_returns_none() -> None:
    assert lp.resolve_legacy("other/file.md") is None
    assert lp.resolve_legacy("protocol/.agents/INDEX.md") is None


def test_unique_resolution_for_every_legacy_prefix() -> None:
    """Each legacy path resolves to exactly one target (first match wins)."""
    for legacy, _ in lp.LEGACY_PATHS:
        probe = legacy + ("x" if legacy.endswith("/") else "")
        resolved = lp.resolve_legacy(probe)
        assert resolved is not None
        assert resolved != probe


def test_matches_legacy_detects_legacy_and_only_legacy() -> None:
    assert lp.matches_legacy("plans/42-h13-planned-cleanup.md")
    assert lp.matches_legacy("plans/rfc/62-guarantee-model-and-enforcement-boundaries.md")
    assert lp.matches_legacy("ARCHITECTURAL_DECISION_MODEL.md")
    assert not lp.matches_legacy("docs/plans/42-h13-planned-cleanup.md")
    assert not lp.matches_legacy("tools/check_plan_citations.py")
