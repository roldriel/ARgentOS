"""Tests for the decision-tree evaluator and CLI."""

from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

import pytest

PROJECT_ROOT = Path(__file__).resolve().parents[3]
RUNNER_PATH = PROJECT_ROOT / ".agents" / "harness" / "runner.py"
TREES_DIR = PROJECT_ROOT / ".agents" / "harness" / "decision_trees"

import decision_tree_evaluator as dte


def run_decide(
    trigger: str, vars_value: str, env: dict[str, str] | None = None
) -> tuple[int, dict]:
    cmd = [
        sys.executable,
        str(RUNNER_PATH),
        "decide",
        "--session",
        "test-session",
        "--trigger",
        trigger,
        "--vars",
        vars_value,
    ]
    result = subprocess.run(
        cmd,
        cwd=PROJECT_ROOT,
        capture_output=True,
        text=True,
        env={**os.environ, **(env or {})},
    )
    try:
        output = json.loads(result.stdout) if result.stdout else {}
    except json.JSONDecodeError:
        output = {"raw_stdout": result.stdout, "stderr": result.stderr}
    return result.returncode, output


@pytest.fixture
def base_vars():
    return {
        "trigger": "H01",
        "artifact_exists": True,
        "retry_count": 0,
    }


def test_all_toml_files_parse():
    for path in sorted(TREES_DIR.glob("H*_FAIL.toml")):
        tree = json.loads(json.dumps({}))  # placeholder
        import tomllib

        raw = path.read_text(encoding="utf-8")
        tree = tomllib.loads(raw)
        assert "metadata" in tree
        assert "nodes" in tree
        assert "start" in tree["nodes"]


def test_simple_true_branch(base_vars):
    tree = {
        "metadata": {"trigger": "H01"},
        "nodes": {
            "start": {
                "condition": "artifact_exists == false",
                "true": {
                    "action": "RETRY_WORKER",
                    "target_phase": "x.md",
                    "role": "worker",
                },
                "false": {
                    "action": "RECOVERY_GENERIC",
                    "target_phase": "08-recovery.md",
                },
            }
        },
    }
    base_vars["artifact_exists"] = False
    result = dte.evaluate_tree(tree, base_vars)
    assert result.result == "DECISION"
    assert result.action == "RETRY_WORKER"


def test_simple_false_branch(base_vars):
    tree = {
        "metadata": {"trigger": "H01"},
        "nodes": {
            "start": {
                "condition": "artifact_exists == false",
                "true": {
                    "action": "RETRY_WORKER",
                    "target_phase": "x.md",
                    "role": "worker",
                },
                "false": {
                    "action": "RECOVERY_GENERIC",
                    "target_phase": "08-recovery.md",
                },
            }
        },
    }
    result = dte.evaluate_tree(tree, base_vars)
    assert result.result == "DECISION"
    assert result.action == "RECOVERY_GENERIC"


def test_multi_node_path(base_vars):
    tree = {
        "metadata": {"trigger": "H01"},
        "nodes": {
            "start": {
                "condition": "artifact_exists == false",
                "true": {"next": "check_retry"},
                "false": {
                    "action": "RECOVERY_GENERIC",
                    "target_phase": "08-recovery.md",
                },
            },
            "check_retry": {
                "condition": "retry_count < 2",
                "true": {
                    "action": "RETRY_WORKER",
                    "target_phase": "x.md",
                    "role": "worker",
                },
                "false": {"action": "NEEDS_CLARIFICATION"},
            },
        },
    }
    base_vars["artifact_exists"] = False
    base_vars["retry_count"] = 1
    result = dte.evaluate_tree(tree, base_vars)
    assert result.result == "DECISION"
    assert result.action == "RETRY_WORKER"
    assert result.path == ["start", "check_retry"]


def test_fallback_node(base_vars):
    tree = {
        "metadata": {"trigger": "H01"},
        "nodes": {
            "start": {
                "condition": "true",
                "true": {
                    "action": "RECOVERY_GENERIC",
                    "target_phase": "08-recovery.md",
                },
                "false": {
                    "action": "RECOVERY_GENERIC",
                    "target_phase": "08-recovery.md",
                },
            }
        },
    }
    result = dte.evaluate_tree(tree, base_vars)
    assert result.result == "DECISION"
    assert result.action == "RECOVERY_GENERIC"


def test_missing_variable():
    tree = {
        "metadata": {"trigger": "H01"},
        "nodes": {
            "start": {
                "condition": "true",
                "true": {
                    "action": "RECOVERY_GENERIC",
                    "target_phase": "08-recovery.md",
                },
                "false": {
                    "action": "RECOVERY_GENERIC",
                    "target_phase": "08-recovery.md",
                },
            }
        },
    }
    result = dte.evaluate_tree(tree, {"trigger": "H01"})
    assert result.result == "ERROR"
    assert result.error["code"] == "MISSING_VARIABLE"


def test_no_eval_arbitrary_code():
    with pytest.raises(dte.DecisionTreeError):
        dte.parse_condition("__import__('os').system('echo pwned')")


def test_cycle_detected():
    tree = {
        "metadata": {"trigger": "H01"},
        "nodes": {
            "start": {
                "condition": "true",
                "true": {"next": "b"},
                "false": {"action": "ABORT"},
            },
            "b": {
                "condition": "true",
                "true": {"next": "start"},
                "false": {"action": "ABORT"},
            },
        },
    }
    result = dte.evaluate_tree(
        tree, {"trigger": "H01", "artifact_exists": True, "retry_count": 0}
    )
    assert result.result == "ERROR"
    assert result.error["code"] == "CYCLE_DETECTED"


def test_unreachable_node():
    tree = {
        "metadata": {"trigger": "H01"},
        "nodes": {
            "start": {
                "condition": "true",
                "true": {"next": "missing"},
                "false": {"action": "ABORT"},
            }
        },
    }
    result = dte.evaluate_tree(
        tree, {"trigger": "H01", "artifact_exists": True, "retry_count": 0}
    )
    assert result.result == "ERROR"
    assert result.error["code"] == "UNREACHABLE_NODE"


def test_invalid_action():
    tree = {
        "metadata": {"trigger": "H01"},
        "nodes": {
            "start": {
                "condition": "true",
                "true": {"action": "UNKNOWN_ACTION"},
                "false": {"action": "ABORT"},
            }
        },
    }
    result = dte.evaluate_tree(
        tree, {"trigger": "H01", "artifact_exists": True, "retry_count": 0}
    )
    assert result.result == "ERROR"
    assert result.error["code"] == "INVALID_ACTION"


def test_default_recovery_on_error():
    result = dte.evaluate_tree(
        {"metadata": {"trigger": "H01"}, "nodes": {}},
        {"trigger": "H01", "artifact_exists": True, "retry_count": 0},
    )
    assert result.result == "ERROR"
    assert result.action == "RECOVERY_GENERIC"
    assert result.params["target_phase"] == "08-recovery.md"


def test_cli_vars_file(tmp_path):
    vars_file = tmp_path / "vars.json"
    vars_file.write_text(
        json.dumps({"artifact_exists": False, "retry_count": 0}),
        encoding="utf-8",
    )
    returncode, output = run_decide("H01", f"@{vars_file}")
    assert returncode == 0
    assert output["result"] == "DECISION"
    assert output["action"] == "RETRY_WORKER"


def test_cli_exit_code_decision():
    returncode, output = run_decide(
        "H01", json.dumps({"artifact_exists": False, "retry_count": 0})
    )
    assert returncode == 0
    assert output["result"] == "DECISION"


def test_cli_exit_code_error():
    returncode, output = run_decide("H01", json.dumps({"trigger": "H01"}))
    assert returncode == 1
    assert output["result"] == "ERROR"


def test_cli_tree_not_found():
    returncode, output = run_decide(
        "H99", json.dumps({"artifact_exists": True, "retry_count": 0})
    )
    assert returncode == 1
    assert output["error"]["code"] == "TREE_NOT_FOUND"
