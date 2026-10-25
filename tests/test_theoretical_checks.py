"""Deterministic checks CH-1…CH-9 and their base-relative determinism."""

from __future__ import annotations

import subprocess
from pathlib import Path

from test_theoretical_overlay import MINIMAL_PLAN, build_repo

from runtime.theoretical import load_proposal, run_checks
from runtime.theoretical.checks import ANOMALY, BOUNDARY, GAP, VALID


def _checks(repo: Path):
    return run_checks(load_proposal(repo, 175, "HEAD"))


def _signals(repo: Path, check: str) -> list[str]:
    return [result.signal for result in _checks(repo) if result.check == check]


def _signals_at(repo: Path, check: str, base: str) -> list[str]:
    return [
        result.signal
        for result in run_checks(load_proposal(repo, 175, base))
        if result.check == check
    ]


def git(repo: Path, *args: str) -> None:
    subprocess.run(
        ["git", "-C", str(repo), *args],
        check=True,
        capture_output=True,
        text=True,
        encoding="utf-8",
    )


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
    assert ANOMALY in _signals(
        build_repo("ch1-a-empty", plan=class_a_no_payload), "CH-1"
    )


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

    touched = (
        MINIMAL_PLAN.replace(
            "A minimal committed proposal.",
            "A minimal committed proposal citing `docs/foo.md:Section`.",
        )
        .replace("1. `runtime/foo.py`", "1. `docs/foo.md`")
        .replace("- **Scope:** `runtime/foo.py`", "- **Scope:** `docs/foo.md`")
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


def test_ch3_reads_the_base_not_the_working_tree() -> None:
    """A citation that resolves only uncommitted does not resolve for TE."""
    cited = "\n## Section\n\nCited.\n"
    repo = build_repo("ch3-base", extra_files={"docs/cited.md": cited})
    plan = (repo / "docs" / "plans" / "175-minimal.md").read_text(encoding="utf-8")
    plan = plan.replace(
        "A minimal committed proposal.",
        "A minimal committed proposal citing `docs/cited.md:Section`.",
    )
    (repo / "docs" / "plans" / "175-minimal.md").write_text(plan, encoding="utf-8")
    git(repo, "add", ".")
    git(repo, "commit", "-q", "-m", "cite")
    assert VALID in _signals(repo, "CH-3")

    # A staged/working change to the cited file must not change the result.
    (repo / "docs" / "cited.md").write_text("\n## Other\n\n", encoding="utf-8")
    git(repo, "add", "docs/cited.md")
    assert VALID in _signals(repo, "CH-3")
    (repo / "docs" / "cited.md").write_text("\n## Other\n\n", encoding="utf-8")
    assert VALID in _signals(repo, "CH-3")

    # The same citation against the new HEAD (committed) is broken.
    git(repo, "commit", "-q", "-m", "retire section")
    assert ANOMALY in _signals(repo, "CH-3")


def test_ch3_artifact_status_is_read_at_the_base() -> None:
    """A Superseded status that exists only in the working tree is invisible."""
    plan = MINIMAL_PLAN.replace(
        "A minimal committed proposal.",
        "A minimal committed proposal citing `docs/rfc/99-old.md:Decision`.",
    )
    repo = build_repo(
        "ch3-status-base",
        plan=plan,
        extra_files={
            "docs/rfc/99-old.md": "# RFC 99 — old\n\n**Status:** Accepted\n\n## Decision\n\nOld.\n"
        },
    )
    assert VALID in _signals(repo, "CH-3")
    (repo / "docs" / "rfc" / "99-old.md").write_text(
        "# RFC 99 — old\n\n**Status:** Superseded\n\n## Decision\n\nOld.\n",
        encoding="utf-8",
    )
    git(repo, "add", "docs/rfc/99-old.md")
    assert VALID in _signals(repo, "CH-3")


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
    payload = (
        MINIMAL_PLAN.replace("**RFC-56 Class:** N/A", "**RFC-56 Class:** A")
        .replace("1. `runtime/foo.py`", "1. `protocol/.agents/contracts/X.md`")
        .replace(
            "- **Scope:** `runtime/foo.py`",
            "- **Scope:** `protocol/.agents/contracts/X.md`",
        )
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


def test_ch7_recomposes_the_delta_from_the_base_commit() -> None:
    """The declared delta is a property of the base, not of the index."""
    import scoped_content_identity

    repo = build_repo("ch7-base", extra_files={"docs/base.md": "base\n"})
    report = scoped_content_identity.compute(
        repo,
        ["docs/base.md"],
        ref="HEAD",
        content_ref="HEAD",
    )
    anchor = f"""
## Validation anchor

- **Scope set:** `docs/base.md`
- **Delta scoped identity:** {report['delta_scoped_identity']}
"""
    plan = (repo / "docs" / "plans" / "175-minimal.md").read_text(encoding="utf-8") + anchor
    (repo / "docs" / "plans" / "175-minimal.md").write_text(plan, encoding="utf-8")
    git(repo, "add", ".")
    git(repo, "commit", "-q", "-m", "anchor")
    assert VALID in _signals(repo, "CH-7")

    # A staged change of a scoped path is invisible to the base-relative delta.
    (repo / "docs" / "base.md").write_text("staged change\n", encoding="utf-8")
    git(repo, "add", "docs/base.md")
    assert VALID in _signals(repo, "CH-7")

    # Committing it makes the declared anchor stale at the new base.
    git(repo, "commit", "-q", "-m", "change the scoped file")
    assert ANOMALY in _signals(repo, "CH-7")


def test_ch8_resolves_the_committed_proposal() -> None:
    assert VALID in _signals(build_repo("ch8"), "CH-8")


def test_ch9_reports_unresolved_and_escaping_deliverables() -> None:
    unresolved = MINIMAL_PLAN.replace(
        "1. `runtime/foo.py`",
        "1. `runtime/foo.py`\n2. el paquete nuevo, sin ruta",
    )
    assert GAP in _signals(build_repo("ch9-unresolved", plan=unresolved), "CH-9")

    escaping = MINIMAL_PLAN.replace(
        "1. `runtime/foo.py`",
        "1. `runtime/foo.py`\n2. `../outside/secret.py`",
    )
    assert ANOMALY in _signals(build_repo("ch9-escaping", plan=escaping), "CH-9")

    assert VALID in _signals(build_repo("ch9-ok"), "CH-9")


def test_ch9_rejects_an_effect_class_outside_the_closed_vocabulary() -> None:
    plan = MINIMAL_PLAN.replace(
        "| — | ninguno | — | authorized |",
        "| `teleport` | un efecto no clasificable | — | authorized |",
    )
    assert ANOMALY in _signals(build_repo("ch9-effect", plan=plan), "CH-9")
    recognised = MINIMAL_PLAN.replace(
        "| — | ninguno | — | authorized |",
        "| `network` | descarga un artefacto | este Plan | authorized |",
    )
    assert VALID in _signals(build_repo("ch9-effect-ok", plan=recognised), "CH-9")


def test_checks_are_a_function_of_the_base_commit() -> None:
    repo = build_repo("checks-deterministic")
    before = [
        (result.check, result.signal, result.statement) for result in _checks(repo)
    ]
    (repo / "docs" / "plans" / "175-minimal.md").write_text(
        (repo / "docs" / "plans" / "175-minimal.md").read_text(encoding="utf-8")
        + "\n<!-- dirty -->\n",
        encoding="utf-8",
    )
    (repo / "runtime.py").write_text("dirty\n", encoding="utf-8")
    after = [
        (result.check, result.signal, result.statement) for result in _checks(repo)
    ]
    assert after == before
