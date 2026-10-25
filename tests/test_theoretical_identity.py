"""Identity and staleness semantics of Theoretical Execution."""

from __future__ import annotations

from pathlib import Path

from test_theoretical_overlay import build_repo

from runtime.theoretical import (
    CHECK_SET,
    TOOL_VERSION,
    build_skeleton,
    input_identity,
    load_proposal,
    run_checks,
    run_identity,
    stale_state,
)


def _proposal(repo: Path):
    return load_proposal(repo, 175, "HEAD")


def test_input_identity_is_deterministic_and_producer_independent() -> None:
    repo = build_repo("identity")
    proposal = _proposal(repo)
    first = input_identity(proposal.base, proposal.overlay)
    second = input_identity(proposal.base, proposal.overlay)
    assert first == second
    assert first["factual"] == second["factual"]
    assert first["projected"] == second["projected"]
    assert first["tool_version"] == TOOL_VERSION == "2"
    assert [entry["id"] for entry in first["check_set"]] == [
        f"CH-{index}" for index in range(1, 10)
    ]
    assert len(first["check_set"]) == len(CHECK_SET) == 9

    run_a = run_identity(
        first,
        plan=175,
        producer="agent-a",
        created_at="2026-10-24T00:00:00Z",
        nonce="a",
    )
    run_b = run_identity(
        first,
        plan=175,
        producer="agent-b",
        created_at="2026-10-24T00:00:00Z",
        nonce="b",
    )
    assert run_a["input_identity"] == run_b["input_identity"] == first
    assert run_a["te_id"] != run_b["te_id"]
    assert run_a["producer"] != run_b["producer"]


def test_run_identity_label_is_stable_with_same_created_at_and_nonce() -> None:
    repo = build_repo("identity-stable")
    proposal = _proposal(repo)
    inputs = input_identity(proposal.base, proposal.overlay)
    first = run_identity(
        inputs, plan=175, producer="agent", created_at="2026-10-24T00:00:00Z", nonce="n"
    )
    second = run_identity(
        inputs, plan=175, producer="agent", created_at="2026-10-24T00:00:00Z", nonce="n"
    )
    assert first == second


def test_run_identity_label_is_recomputable_without_a_memory_address() -> None:
    """The nonce is derived from content, so an interrupted skeleton is stable."""
    repo = build_repo("identity-nonce")
    proposal = _proposal(repo)
    inputs = input_identity(proposal.base, proposal.overlay)
    first = run_identity(inputs, plan=175, producer="agent", created_at="2026-10-24T00:00:00Z")
    second = run_identity(
        inputs, plan=175, producer="agent", created_at="2026-10-24T00:00:00Z"
    )
    assert first == second
    assert first["nonce"] == second["nonce"]
    assert first["te_id"] == second["te_id"]
    # The label is still a label: a different producer or timestamp changes it.
    other = run_identity(
        inputs, plan=175, producer="other", created_at="2026-10-24T00:00:00Z"
    )
    assert other["te_id"] != first["te_id"]
    later = run_identity(
        inputs, plan=175, producer="agent", created_at="2026-10-24T00:00:01Z"
    )
    assert later["te_id"] != first["te_id"]


def test_staleness_uses_input_identity_not_the_run_label() -> None:
    repo = build_repo("stale")
    proposal = _proposal(repo)
    skeleton = build_skeleton(proposal, run_checks(proposal))
    assert stale_state(skeleton, repo)["state"] == "fresh"

    # The semantic run label is not a staleness input.
    skeleton["identity"]["run"]["te_id"] = "te-other-run"
    assert stale_state(skeleton, repo)["state"] == "fresh"


def test_staleness_detects_a_new_head() -> None:
    repo = build_repo("stale-head")
    proposal = _proposal(repo)
    skeleton = build_skeleton(proposal, run_checks(proposal))
    plan = repo / "docs" / "plans" / "175-minimal.md"
    plan.write_text(
        plan.read_text(encoding="utf-8") + "\n<!-- changed -->\n", encoding="utf-8"
    )
    import subprocess

    subprocess.run(
        ["git", "-C", str(repo), "add", "docs/plans/175-minimal.md"],
        check=True,
        capture_output=True,
    )
    subprocess.run(
        ["git", "-C", str(repo), "commit", "-q", "-m", "change plan"],
        check=True,
        capture_output=True,
    )
    assert stale_state(skeleton, repo)["state"] == "stale"


def test_staleness_reports_incomparable_for_a_different_check_set() -> None:
    repo = build_repo("incomparable")
    proposal = _proposal(repo)
    skeleton = build_skeleton(proposal, run_checks(proposal))
    skeleton["identity"]["inputs"]["tool_version"] = "999"
    assert stale_state(skeleton, repo)["state"] == "incomparable"


def test_a_schema_one_result_is_incomparable_for_the_same_inputs() -> None:
    """A v1 result (tool_version 1, eight checks) cannot be compared to v2."""
    repo = build_repo("incomparable-v1")
    proposal = _proposal(repo)
    skeleton = build_skeleton(proposal, run_checks(proposal))
    skeleton["identity"]["inputs"]["tool_version"] = "1"
    skeleton["identity"]["inputs"]["check_set"] = [
        {"id": f"CH-{index}", "version": "1"} for index in range(1, 9)
    ]
    assert stale_state(skeleton, repo)["state"] == "incomparable"
