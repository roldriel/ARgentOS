"""CLI behaviour of Theoretical Execution (plan 175, S5)."""

from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

from test_theoretical_overlay import build_repo

REPO_ROOT = Path(__file__).resolve().parents[1]


def run_cli(repo: Path, *args: str) -> subprocess.CompletedProcess[str]:
    env = os.environ.copy()
    env["PYTHONPATH"] = str(REPO_ROOT) + os.pathsep + env.get("PYTHONPATH", "")
    return subprocess.run(
        [sys.executable, "-m", "runtime.theoretical", *args],
        cwd=repo,
        capture_output=True,
        text=True,
        encoding="utf-8",
        env=env,
        check=False,
    )


def _emit(repo: Path) -> dict:
    proc = run_cli(repo, "--plan", "175", "--base", "HEAD", "--emit")
    assert proc.returncode == 0, proc.stderr
    return json.loads(proc.stdout)


def test_emit_returns_a_gap_skeleton(tmp_path: Path) -> None:
    repo = build_repo("cli-emit")
    payload = _emit(repo)
    assert payload["status"] == "GAP"
    assert payload["provenance"]["producer"] == "pending"
    assert len(payload["claims"]) == 4
    assert payload["coverage"]["dimensions"]["completeness"]["status"] == "PENDING"
    assert payload["coverage"]["dimensions"]["authority"]["computed"] is True


def test_validate_skeleton_and_forged_status(tmp_path: Path) -> None:
    repo = build_repo("cli-validate")
    payload = _emit(repo)
    result = tmp_path / "skeleton.json"
    result.write_text(json.dumps(payload), encoding="utf-8")

    proc = run_cli(repo, "--validate", str(result))
    assert proc.returncode == 0, proc.stderr
    report = json.loads(proc.stdout)
    assert report["valid"] is True
    assert report["derived_status"] == "GAP"

    payload["status"] = "CONVERGED"
    result.write_text(json.dumps(payload), encoding="utf-8")
    proc = run_cli(repo, "--validate", str(result))
    assert proc.returncode == 1
    report = json.loads(proc.stdout)
    assert report["valid"] is False
    assert report["derived_status"] == "GAP"


def test_stale_reports_fresh_at_head(tmp_path: Path) -> None:
    repo = build_repo("cli-stale")
    result = tmp_path / "skeleton.json"
    result.write_text(json.dumps(_emit(repo)), encoding="utf-8")
    proc = run_cli(repo, "--stale", str(result))
    assert proc.returncode == 0, proc.stderr
    assert json.loads(proc.stdout)["state"] == "fresh"


def test_compare_same_and_divergent(tmp_path: Path) -> None:
    repo = build_repo("cli-compare")
    payload = _emit(repo)
    first = tmp_path / "a.json"
    second = tmp_path / "b.json"
    first.write_text(json.dumps(payload), encoding="utf-8")

    proc = run_cli(repo, "--compare", str(first), str(first))
    assert proc.returncode == 0, proc.stderr
    report = json.loads(proc.stdout)
    assert report["comparison"] == "SAME_INPUT"
    assert report["semantic_divergence"] is False
    assert "resolved" not in report

    divergent = json.loads(json.dumps(payload))
    divergent["findings"] = [
        {
            "id": "TF-01",
            "signal": "ANOMALY",
            "statement": "a divergent finding",
            "location": "test",
            "evidence_refs": ["test"],
            "disposition": "OPEN",
            "escalation_ref": None,
            "accepted_by": None,
        }
    ]
    second.write_text(json.dumps(divergent), encoding="utf-8")
    proc = run_cli(repo, "--compare", str(first), str(second))
    assert proc.returncode == 1
    report = json.loads(proc.stdout)
    assert report["semantic_divergence"] is True
    assert report["only_in_cur"]
    assert "resolved" not in report


def test_missing_plan_is_a_structured_error() -> None:
    repo = build_repo("cli-missing")
    proc = run_cli(repo, "--plan", "999", "--emit")
    assert proc.returncode == 2
    error = json.loads(proc.stderr)
    assert error["error"] == "PROPOSAL_NOT_FOUND"
