"""Deterministic checks CH-1…CH-8 (plan 175, S3)."""

from __future__ import annotations

from pathlib import Path

from test_theoretical_overlay import MINIMAL_PLAN, build_repo

from runtime.theoretical import load_proposal, run_checks
from runtime.theoretical.checks import ANOMALY, BOUNDARY, GAP, VALID


def _checks(repo: Path):
    return run_checks(load_proposal(repo, 175, "HEAD"))


def _signals(repo: Path, check: str) -> list[str]:
    return [result.signal for result in _checks(repo) if result.check == check]


def test_ch1_class_and_payload_paths() -> None:
    payload = MINIMAL_PLAN.replace(
        "1. `runtime/foo.py`", "1. `protocol/.agents/contracts/X.md`"
    ).replace(
        "- **Scope:** `runtime/foo.py`",
        "- **Scope:** `protocol/.agents/contracts/X.md`",
    )
    assert ANOMALY in _signals(build_repo("ch1-n/a", plan=payload), "CH-1")

    class_a_payload = payload.replace("**RFC-56 Class:** N/A", "**RFC-56 Class:** A")
    assert VALID in _signals(build_repo("ch1-a", plan=class_a_payload), "CH-1")

    class_a_no_payload = MINIMAL_PLAN.replace(
        "**RFC-56 Class:** N/A", "**RFC-56 Class:** A"
    )
    assert ANOMALY in _signals(build_repo("ch1-a-empty", plan=class_a_no_payload), "CH-1")


def test_ch2_deliverable_outside_scope_and_missing_scope() -> None:
    outside = MINIMAL_PLAN.replace(
        "- **Scope:** `runtime/foo.py`", "- **Scope:** `runtime/other.py`"
    )
    assert ANOMALY in _signals(build_repo("ch2-outside", plan=outside), "CH-2")

    no_scope = MINIMAL_PLAN.replace("- **Scope:** `runtime/foo.py`\n", "")
    assert GAP in _signals(build_repo("ch2-missing", plan=no_scope), "CH-2")


def test_ch3_broken_touched_and_superseded_citations() -> None:
    broken = MINIMAL_PLAN.replace(
        "A minimal committed proposal.",
        "A minimal committed proposal citing `docs/missing.md:Section`.",
    )
    assert ANOMALY in _signals(build_repo("ch3-broken", plan=broken), "CH-3")

    touched = MINIMAL_PLAN.replace(
        "A minimal committed proposal.",
        "A minimal committed proposal citing `docs/foo.md:Section`.",
    ).replace("1. `runtime/foo.py`", "1. `docs/foo.md`").replace(
        "- **Scope:** `runtime/foo.py`", "- **Scope:** `docs/foo.md`"
    )
    assert GAP in _signals(build_repo("ch3-touched", plan=touched), "CH-3")

    superseded_file = """# RFC 99 — old

**Status:** Superseded

## Decision

Old decision.
"""
    superseded = MINIMAL_PLAN.replace(
        "A minimal committed proposal.",
        "A minimal committed proposal citing `docs/rfc/99-old.md:Decision`.",
    )
    repo = build_repo(
        "ch3-superseded",
        plan=superseded,
        extra_files={"docs/rfc/99-old.md": superseded_file},
    )
    assert BOUNDARY in _signals(repo, "CH-3")


def _closed_plan(closed: bool) -> str:
    body = """# Plan 174 — closed fixture

**Status:** Executed
**Fecha:** 2026-01-01
**RFC:** —
**RFC-56 Class:** N/A
**Change Level:** L1

## Objetivo

Closed fixture.
"""
    if closed:
        body += """
## Validation anchor

- **Scope set:** `docs/base.md`
- **State identity:** 0000000000000000000000000000000000000000
- **Delta scoped identity:** 1111111111111111111111111111111111111111111111111111111111111111
- **Validity / stale:** vigente

## Checkpoint / cierre

- **Condición derivada:** Closed
- **Consistencia checkpoint↔anchor:** PASS
"""
    return body


def test_ch4_closed_and_executed_artifacts() -> None:
    delivered = MINIMAL_PLAN.replace(
        "1. `runtime/foo.py`", "1. `docs/plans/174-closed.md`"
    ).replace(
        "- **Scope:** `runtime/foo.py`",
        "- **Scope:** `docs/plans/174-closed.md`",
    )
    closed_repo = build_repo(
        "ch4-closed",
        plan=delivered,
        extra_files={
            "docs/plans/174-closed.md": _closed_plan(True),
            "docs/base.md": "base\n",
        },
    )
    assert ANOMALY in _signals(closed_repo, "CH-4")

    executed_repo = build_repo(
        "ch4-executed",
        plan=delivered,
        extra_files={"docs/plans/174-closed.md": _closed_plan(False)},
    )
    assert BOUNDARY in _signals(executed_repo, "CH-4")


def test_ch5_payload_obligation_is_declared_or_boundary() -> None:
    payload = MINIMAL_PLAN.replace(
        "**RFC-56 Class:** N/A", "**RFC-56 Class:** A"
    ).replace(
        "1. `runtime/foo.py`", "1. `protocol/.agents/contracts/X.md`"
    ).replace(
        "- **Scope:** `runtime/foo.py`",
        "- **Scope:** `protocol/.agents/contracts/X.md`",
    )
    assert BOUNDARY in _signals(build_repo("ch5-payload", plan=payload), "CH-5")


def test_ch6_criteria_without_verification_are_boundary() -> None:
    no_verification = MINIMAL_PLAN.split("## Verificación")[0]
    assert BOUNDARY in _signals(
        build_repo("ch6-no-verification", plan=no_verification), "CH-6"
    )
    assert VALID in _signals(build_repo("ch6-ok"), "CH-6")


def test_ch7_anchor_identity_is_recomposed_or_anomaly() -> None:
    anchor = """
## Validation anchor

- **Scope set:** `docs/base.md`
- **State identity:** 0000000000000000000000000000000000000000
- **Delta scoped identity:** 1111111111111111111111111111111111111111111111111111111111111111
- **Validity / stale:** vigente
"""
    plan = MINIMAL_PLAN + anchor
    repo = build_repo(
        "ch7-anchor",
        plan=plan,
        extra_files={"docs/base.md": "base\n"},
    )
    assert ANOMALY in _signals(repo, "CH-7")
    assert "N/A" in _signals(build_repo("ch7-none"), "CH-7")


def test_ch8_resolves_the_committed_proposal() -> None:
    assert VALID in _signals(build_repo("ch8"), "CH-8")
