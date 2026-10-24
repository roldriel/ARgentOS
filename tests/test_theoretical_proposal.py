"""Committed-plan loading and item enumeration (plan 175, S2)."""

from __future__ import annotations

from pathlib import Path

import pytest

from test_theoretical_overlay import MINIMAL_PLAN, build_repo

from runtime.theoretical import ProposalError, load_proposal, load_proposal_at


def test_minimal_plan_is_enumerated_without_gaps() -> None:
    repo = build_repo("proposal")
    proposal = load_proposal(repo, 175, "HEAD")
    assert proposal.path == "docs/plans/175-minimal.md"
    assert proposal.status == "Aprobado para ejecución"
    assert proposal.rfc56_class == "N/A"
    assert proposal.deliverables == ("runtime/foo.py",)
    assert proposal.scope == ("runtime/foo.py",)
    assert proposal.scope_declared is True
    assert proposal.effects == ()
    assert proposal.effects_declared is True
    assert proposal.gaps == ()
    kinds = {item.kind for item in proposal.items}
    assert kinds == {"deliverable", "step", "criterion", "premise"}
    assert len(proposal.items) == 4


def test_deliverables_and_editable_scope_are_distinct() -> None:
    plan = MINIMAL_PLAN.replace(
        "- **Scope:** `runtime/foo.py`",
        "- **Scope:** `runtime/foo.py`, `docs/extra.md`",
    )
    repo = build_repo("scope", plan=plan)
    proposal = load_proposal(repo, 175, "HEAD")
    assert proposal.deliverables == ("runtime/foo.py",)
    assert proposal.scope == ("runtime/foo.py", "docs/extra.md")
    assert proposal.overlay.paths() == ("runtime/foo.py",)


def test_missing_sections_are_declared_gaps_not_invented() -> None:
    plan = """# Plan 175 — sparse

**Status:** Aprobado para ejecución
**RFC-56 Class:** N/A
**Change Level:** L2

## Objetivo

Sparse.

## Entregables

1. `runtime/foo.py`
"""
    repo = build_repo("sparse", plan=plan)
    proposal = load_proposal(repo, 175, "HEAD")
    assert proposal.items
    joined = " ".join(proposal.gaps)
    assert "no steps" in joined
    assert "no exit criteria" in joined
    assert "no effects container" in joined
    assert "no premises" in joined
    assert "no verification command-set" in joined


def test_superseded_and_missing_status_are_rejected() -> None:
    superseded = MINIMAL_PLAN.replace(
        "**Status:** Aprobado para ejecución", "**Status:** Superseded"
    )
    repo = build_repo("superseded", plan=superseded)
    with pytest.raises(ProposalError) as error:
        load_proposal(repo, 175, "HEAD")
    assert error.value.code == "PROPOSAL_SUPERSEDED"

    missing = MINIMAL_PLAN.replace("**Status:** Aprobado para ejecución\n", "")
    repo = build_repo("missing-status", plan=missing)
    with pytest.raises(ProposalError) as error:
        load_proposal(repo, 175, "HEAD")
    assert error.value.code == "PROPOSAL_STATUS_MISSING"


def test_plan_outside_the_base_is_not_in_base() -> None:
    repo = build_repo("not-in-base")
    with pytest.raises(ProposalError) as error:
        load_proposal_at(repo, "docs/plans/176-not-there.md", "HEAD")
    assert error.value.code == "PROPOSAL_NOT_IN_BASE"
    with pytest.raises(ProposalError) as error:
        load_proposal(repo, 176, "HEAD")
    assert error.value.code == "PROPOSAL_NOT_FOUND"


def test_table_steps_are_enumerated() -> None:
    plan = MINIMAL_PLAN.replace(
        "## Pasos\n\n1. Escribir foo.py.",
        "## Pasos\n\n| Fase | Contenido | Gate |\n|---|---|---|\n| **S1** | Escribir foo.py | verde |",
    )
    repo = build_repo("table-steps", plan=plan)
    proposal = load_proposal(repo, 175, "HEAD")
    steps = [item for item in proposal.items if item.kind == "step"]
    assert [item.label for item in steps] == ["S1"]
