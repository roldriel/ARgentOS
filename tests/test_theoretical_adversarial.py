"""Adversarial review of Theoretical Execution (plan 176).

Each test attacks one declared boundary.  The suite does not demonstrate that
TE is correct: it demonstrates that the specific failure modes the design
declares are actually rejected, and that the epistemic separations
(``theoretical ≠ factual``, ``recommendation ≠ authorization``) hold under
attack.
"""

from __future__ import annotations

import ast
import hashlib
import json
from copy import deepcopy
from pathlib import Path

from test_theoretical_cli import run_cli
from test_theoretical_overlay import MINIMAL_PLAN, build_repo
from test_theoretical_result import (
    _converged,
    _fill_claims,
    _finding,
    _perform_dimensions,
    _seal,
)

from runtime.theoretical import (
    STATUSES,
    build_skeleton,
    fingerprint,
    input_identity,
    load_proposal,
    run_checks,
    validate_result,
)
from runtime.theoretical.checks import failed_checks

REPO_ROOT = Path(__file__).resolve().parents[1]
THEORETICAL = REPO_ROOT / "runtime" / "theoretical"


def _proposal(repo: Path):
    return load_proposal(repo, 175, "HEAD")


def _validated(repo: Path) -> dict:
    result, _ = _converged(repo)
    problems, derived = validate_result(result, repo)
    assert problems == []
    assert derived == "CONVERGED"
    return result


# --- SCOPE_ATTACK ---------------------------------------------------------


def test_scope_attack_the_plan_is_never_executed(tmp_path: Path) -> None:
    """A command declared in ``## Verificación`` is text, not an effect."""
    marker = "planned-effect.txt"
    plan = MINIMAL_PLAN.replace(
        'python -c "print(1)"',
        f'python -c "open(\'{marker}\', \'w\').write(\'executed\')"',
    )
    repo = build_repo("adv-no-execution", plan=plan)
    proc = run_cli(repo, "--plan", "175", "--base", "HEAD", "--emit")
    assert proc.returncode == 0, proc.stderr
    assert not (repo / marker).exists()


def test_scope_attack_a_payload_path_under_class_na_is_an_anomaly() -> None:
    plan = MINIMAL_PLAN.replace(
        "1. `runtime/foo.py`", "1. `protocol/.agents/contracts/X.md`"
    ).replace(
        "- **Scope:** `runtime/foo.py`",
        "- **Scope:** `protocol/.agents/contracts/X.md`",
    )
    repo = build_repo("adv-payload", plan=plan)
    signals = [result.signal for result in run_checks(_proposal(repo)) if result.check == "CH-1"]
    assert "ANOMALY" in signals


# --- BOUNDARY_ATTACK ------------------------------------------------------


def _module_imports() -> set[str]:
    modules: set[str] = set()
    for path in sorted(THEORETICAL.glob("*.py")):
        tree = ast.parse(path.read_text(encoding="utf-8"))
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                modules.update(alias.name for alias in node.names)
            elif isinstance(node, ast.ImportFrom) and node.module:
                modules.add(node.module)
    return modules


def test_boundary_attack_no_host_no_payload_no_store_imports() -> None:
    modules = _module_imports()
    forbidden = (
        "runtime.orchestrator.host",
        "runtime.orchestrator.worker",
        "runtime.orchestrator.store",
        "runtime.orchestrator.derivation",
        "protocol",
    )
    assert not [module for module in modules if module.startswith(forbidden)]
    assert "runtime.orchestrator.observation" in modules


def test_boundary_attack_te_never_opens_a_file_for_writing() -> None:
    for path in sorted(THEORETICAL.glob("*.py")):
        tree = ast.parse(path.read_text(encoding="utf-8"))
        for node in ast.walk(tree):
            if isinstance(node, ast.Call):
                name = ""
                if isinstance(node.func, ast.Name):
                    name = node.func.id
                elif isinstance(node.func, ast.Attribute):
                    name = node.func.attr
                assert name not in {"write_text", "write_bytes", "mkdir", "unlink"}
                if name == "open":
                    modes = [
                        argument.value
                        for argument in node.args[1:2]
                        if isinstance(argument, ast.Constant)
                    ]
                    assert not any(
                        isinstance(mode, str) and set(mode) & set("wax")
                        for mode in modes
                    ), f"{path.name} opens a file for writing"
            if isinstance(node, ast.Call):
                for keyword in node.keywords:
                    assert not (
                        keyword.arg == "shell"
                        and isinstance(keyword.value, ast.Constant)
                        and keyword.value.value is True
                    ), f"{path.name} uses shell=True"


# --- STATE_ATTACK ---------------------------------------------------------


def test_state_attack_a_partial_result_is_invalid() -> None:
    repo = build_repo("adv-partial")
    result = _validated(repo)
    partial = deepcopy(result)
    partial["claims"] = partial["claims"][:-1]
    problems, _ = validate_result(partial, repo)
    assert problems


def test_state_attack_two_emits_share_the_input_identity() -> None:
    repo = build_repo("adv-state")
    proposal = _proposal(repo)
    first = build_skeleton(proposal, run_checks(proposal))
    second = build_skeleton(proposal, run_checks(proposal))
    assert first["identity"]["inputs"] == second["identity"]["inputs"]
    assert first["checks"] == second["checks"]
    # The run label is a label, never an identity of the result.
    assert first["identity"]["run"]["te_id"].startswith("te-175-")


# --- AUTHORITY_ATTACK -----------------------------------------------------


def test_authority_attack_no_result_can_authorize_itself() -> None:
    repo = build_repo("adv-authority")
    result = _validated(repo)
    result["corrections"] = [
        {
            "id": "TCOR-01",
            "finding_ref": "TF-01",
            "target": "plan",
            "statement": "apply the correction",
            "authority_required": True,
            "applied": True,
        }
    ]
    result["findings"] = [
        {
            "id": "TF-01",
            "signal": "ANOMALY",
            "statement": "a problem",
            "location": "test",
            "evidence_refs": ["test"],
            "disposition": "OPEN",
            "escalation_ref": None,
            "accepted_by": None,
        }
    ]
    _seal(result, "OPEN_FINDINGS")
    problems, _ = validate_result(result, repo)
    assert any("applied" in problem for problem in problems)


def test_authority_attack_a_residual_must_be_accepted_by_a_committed_reference() -> None:
    repo = build_repo("adv-residual")
    result = _validated(repo)
    result["findings"] = [
        {
            "id": "TF-01",
            "signal": "GAP",
            "statement": "a residual problem",
            "location": "test",
            "evidence_refs": ["test"],
            "disposition": "RESIDUAL",
            "escalation_ref": None,
            "accepted_by": "docs/does-not-exist.md:Section",
        }
    ]
    _seal(result, "CONVERGED")
    problems, _ = validate_result(result, repo)
    assert any("accepted_by" in problem for problem in problems)


def test_authority_attack_the_engine_never_marks_semantic_dimensions_performed() -> None:
    repo = build_repo("adv-dimensions")
    skeleton = build_skeleton(_proposal(repo), run_checks(_proposal(repo)))
    for name in ("completeness", "consistency", "adversarial"):
        assert skeleton["coverage"]["dimensions"][name]["status"] == "PENDING"
        assert skeleton["coverage"]["dimensions"][name]["computed"] is False


# --- EVIDENCE_ATTACK ------------------------------------------------------


def test_evidence_attack_no_status_claims_a_factual_outcome() -> None:
    assert set(STATUSES) == {
        "CONVERGED",
        "OPEN_FINDINGS",
        "REQUIRES_HUMAN",
        "GAP",
        "NO_PROGRESS",
        "RESOURCE_LIMIT",
    }
    assert not {"PASS", "VALID", "VERIFIED", "EXECUTED"} & set(STATUSES)


def test_evidence_attack_the_provenance_kind_is_forced() -> None:
    repo = build_repo("adv-provenance")
    result = _validated(repo)
    result["provenance"]["kind"] = "factual"
    problems, _ = validate_result(result, repo)
    assert any("provenance.kind" in problem for problem in problems)


def test_evidence_attack_a_prediction_is_not_evidence() -> None:
    repo = build_repo("adv-prediction")
    result = _validated(repo)
    obligation = {
        "id": "TV-01",
        "for_claim": "TC-01",
        "finding_ref": None,
        "statement": "observe it",
        "falsified_if": "the observation contradicts",
        "depends_on": [],
        "candidate": "runtime_check",
        "status": "OPEN",
    }
    result["verification_obligations"] = [obligation]
    claim = result["claims"][0]
    claim.update(
        {
            "kind": "PREDICTION",
            "support": "NOT_EVALUABLE",
            "evidence_class": "NONE",
            "evidence_refs": [],
            "obligation_ref": "TV-01",
        }
    )
    result["coverage"]["checked"] -= 1
    result["coverage"]["not_evaluable"] = 1
    result["coverage"]["dimensions"]["verification"]["evidence_refs"] = ["TV-01"]
    _seal(result, "CONVERGED")
    problems, derived = validate_result(result, repo)
    assert problems == []
    assert derived == "CONVERGED"
    # It is convergent as a *theoretical* record, and the prediction is never
    # checkable evidence.
    assert claim["support"] == "NOT_EVALUABLE"


# --- IDENTITY_ATTACK ------------------------------------------------------


def test_identity_attack_the_working_tree_does_not_change_the_evaluation() -> None:
    repo = build_repo("adv-identity")
    proposal = _proposal(repo)
    before = input_identity(proposal.base, proposal.overlay)
    checks_before = [
        (result.check, result.signal, result.statement)
        for result in run_checks(proposal)
    ]
    (repo / "docs" / "plans" / "175-minimal.md").write_text(
        "# tampered working tree\n", encoding="utf-8"
    )
    (repo / "runtime-dirty.py").write_text("dirty\n", encoding="utf-8")
    proposal_after = _proposal(repo)
    after = input_identity(proposal_after.base, proposal_after.overlay)
    checks_after = [
        (result.check, result.signal, result.statement)
        for result in run_checks(proposal_after)
    ]
    assert after == before
    assert checks_after == checks_before


# --- TEMPORAL_ATTACK ------------------------------------------------------


def test_temporal_attack_a_result_is_stale_after_head_moves(
    tmp_path: Path,
) -> None:
    repo = build_repo("adv-temporal")
    payload = build_skeleton(_proposal(repo), run_checks(_proposal(repo)))
    import subprocess

    (repo / "notes.md").write_text("new commit\n", encoding="utf-8")
    subprocess.run(["git", "-C", str(repo), "add", "notes.md"], check=True)
    subprocess.run(
        ["git", "-C", str(repo), "commit", "-q", "-m", "advance"],
        check=True,
        capture_output=True,
    )
    result = tmp_path / "temporal.json"
    result.write_text(json.dumps(payload), encoding="utf-8")
    proc = run_cli(repo, "--stale", str(result))
    assert proc.returncode == 1
    assert json.loads(proc.stdout)["state"] == "stale"


def test_temporal_attack_a_v1_result_cannot_be_reused(tmp_path: Path) -> None:
    repo = build_repo("adv-v1")
    payload = build_skeleton(_proposal(repo), run_checks(_proposal(repo)))
    payload["identity"]["inputs"]["tool_version"] = "1"
    result = tmp_path / "v1.json"
    result.write_text(json.dumps(payload), encoding="utf-8")
    proc = run_cli(repo, "--stale", str(result))
    assert proc.returncode == 1
    assert json.loads(proc.stdout)["state"] == "incomparable"


def test_temporal_attack_no_progress_needs_a_declared_previous_run() -> None:
    repo = build_repo("adv-no-progress")
    result = _validated(repo)
    result["findings"] = [_finding()]
    result["no_progress"]["previous_fingerprint"] = fingerprint(result)
    result["no_progress"]["previous_te_id"] = "te-previous"
    result["input"]["previous_te_id"] = "te-previous"
    _seal(result, "NO_PROGRESS")
    problems, derived = validate_result(result, repo)
    assert problems == []
    assert derived == "NO_PROGRESS"


def test_temporal_attack_a_converged_result_is_never_no_progress() -> None:
    """CONVERGED outranks NO_PROGRESS: an identical converged record converges."""
    repo = build_repo("adv-converged-progress")
    result = _validated(repo)
    result["no_progress"]["previous_fingerprint"] = fingerprint(result)
    result["no_progress"]["previous_te_id"] = "te-previous"
    result["input"]["previous_te_id"] = "te-previous"
    _seal(result, "CONVERGED")
    problems, derived = validate_result(result, repo)
    assert problems == []
    assert derived == "CONVERGED"


# --- DEPENDENCY_ATTACK ----------------------------------------------------


def test_dependency_attack_the_payload_is_not_a_dependency() -> None:
    modules = _module_imports()
    assert not [module for module in modules if module.split(".")[0] == "protocol"]


# --- NEGATIVE_PATH_ATTACK -------------------------------------------------


def test_negative_path_attack_malformed_json_and_unknown_fields(
    tmp_path: Path,
) -> None:
    repo = build_repo("adv-negative")
    broken = tmp_path / "broken.json"
    broken.write_text("{not json", encoding="utf-8")
    proc = run_cli(repo, "--validate", str(broken))
    assert proc.returncode == 2
    assert json.loads(proc.stderr)["error"] == "RESULT_UNREADABLE"

    payload = build_skeleton(_proposal(repo), run_checks(_proposal(repo)))
    payload["unknown"] = 1
    candidate = tmp_path / "unknown.json"
    candidate.write_text(json.dumps(payload), encoding="utf-8")
    proc = run_cli(repo, "--validate", str(candidate))
    assert proc.returncode == 1
    assert any("unknown field" in problem for problem in json.loads(proc.stdout)["problems"])


def test_negative_path_attack_an_option_shaped_base_is_refused() -> None:
    repo = build_repo("adv-base")
    proc = run_cli(repo, "--plan", "175", "--base", "-x", "--emit")
    assert proc.returncode == 2


def test_negative_path_attack_an_unknown_signal_is_rejected() -> None:
    repo = build_repo("adv-signal")
    result = _validated(repo)
    result["checks"][0]["signal"] = "PASS"
    problems, _ = validate_result(result, repo)
    assert any("unknown signal" in problem for problem in problems)


# --- HISTORICAL_INTEGRITY_ATTACK -----------------------------------------


def test_historical_integrity_attack_a_closed_plan_is_not_modified() -> None:
    plan = REPO_ROOT / "docs" / "plans" / "175-theoretical-execution-dev-v1.md"
    before = hashlib.sha256(plan.read_bytes()).hexdigest()
    repo = build_repo("adv-history")
    proc = run_cli(repo, "--plan", "175", "--base", "HEAD", "--emit")
    assert proc.returncode == 0
    assert hashlib.sha256(plan.read_bytes()).hexdigest() == before
    # A declared change to an artifact whose checkpoint is Closed is an anomaly.
    plan_with_closed_write = MINIMAL_PLAN.replace(
        "1. `runtime/foo.py`", "1. `docs/plans/175-theoretical-execution-dev-v1.md`"
    ).replace(
        "- **Scope:** `runtime/foo.py`",
        "- **Scope:** `docs/plans/175-theoretical-execution-dev-v1.md`",
    )
    target = build_repo("adv-history-target", plan=plan_with_closed_write)
    (target / "docs" / "plans" / "175-theoretical-execution-dev-v1.md").write_text(
        (REPO_ROOT / "docs" / "plans" / "175-theoretical-execution-dev-v1.md").read_text(
            encoding="utf-8"
        ),
        encoding="utf-8",
    )
    import subprocess

    subprocess.run(
        ["git", "-C", str(target), "add", "docs/plans/175-theoretical-execution-dev-v1.md"],
        check=True,
    )
    subprocess.run(
        ["git", "-C", str(target), "commit", "-q", "-m", "add closed plan"],
        check=True,
        capture_output=True,
    )
    signals = [
        result.signal
        for result in run_checks(load_proposal(target, 175, "HEAD"))
        if result.check == "CH-4"
    ]
    assert "ANOMALY" in signals
