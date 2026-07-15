"""Tests for the rubrics standard and H06 structural validation."""

from __future__ import annotations

import json
import re
import subprocess
import sys
import uuid
from pathlib import Path

import pytest

PROJECT_ROOT = Path(__file__).resolve().parents[3]
RUNNER_PATH = PROJECT_ROOT / ".agents" / "harness" / "runner.py"
RUBRICS_PATH = PROJECT_ROOT / ".agents" / "standards" / "quality" / "RUBRICS.md"


def run_runner(
    artifacts_dir: Path,
    session_uuid: str,
    trigger: str = "H06",
    iteration: str = "00",
) -> tuple[int, dict]:
    cmd = [
        sys.executable,
        str(RUNNER_PATH),
        "--session",
        session_uuid,
        "--trigger",
        trigger,
        "--iteration",
        iteration,
        "--artifacts-dir",
        str(artifacts_dir),
    ]
    result = subprocess.run(cmd, cwd=PROJECT_ROOT, capture_output=True, text=True)
    try:
        output = json.loads(result.stdout) if result.stdout else {}
    except json.JSONDecodeError:
        output = {"raw_stdout": result.stdout, "stderr": result.stderr}
    return result.returncode, output


@pytest.fixture
def session(tmp_path):
    session_uuid = f"test-{uuid.uuid4()}"
    artifacts_dir = tmp_path / ".project"
    session_dir = artifacts_dir / session_uuid / "00"
    session_dir.mkdir(parents=True, exist_ok=True)
    yield session_uuid, artifacts_dir


def write_verification_report(
    artifacts_dir: Path, session_uuid: str, rubric_section: str
) -> Path:
    path = artifacts_dir / session_uuid / "00" / "07-VERIFICATION_REPORT.md"
    base = """# Verification Report

## Metadata

## Task Reference

## Execution Plan Reference

## Verification Objective

## Acceptance Criteria Evaluation

```yaml
acceptance_criteria:
  - criterion: "The API shall reject empty names."
    result: "PASS"
    evidence: "Tested."
```

## Test Results

## Issues Found

## Final Decision

```yaml
decision:
  result: "COMPLETED"
  reasoning: "All criteria met."
```

## Confidence

## State Transition

"""
    path.write_text(base + rubric_section, encoding="utf-8")
    return path


def test_rubrics_file_exists_and_has_base_rubrics():
    assert RUBRICS_PATH.is_file()
    content = RUBRICS_PATH.read_text(encoding="utf-8")
    rubrics = set(re.findall(r"### \d+\.\s+`([A-Z_]+_RUBRIC)`", content))
    base_rubrics = {
        "TASK_SPECIFICATION_RUBRIC",
        "CONTEXT_ARTIFACT_RUBRIC",
        "CONTEXT_VALIDATION_REPORT_RUBRIC",
        "EXECUTION_PLAN_RUBRIC",
        "EXECUTION_SUMMARY_RUBRIC",
        "VERIFICATION_REPORT_RUBRIC",
    }
    assert base_rubrics.issubset(
        rubrics
    ), f"Missing base rubrics: {base_rubrics - rubrics}"


def test_each_rubric_has_critical_criterion():
    content = RUBRICS_PATH.read_text(encoding="utf-8")
    rubrics = re.findall(r"### \d+\.\s+`([A-Z_]+_RUBRIC)`", content)
    for rubric in rubrics:
        # Extract the rubric table block following the header.
        match = re.search(
            rf"### \d+\.\s+`{re.escape(rubric)}`.*?(?=### \d+\.\s+`|## |$)",
            content,
            re.DOTALL,
        )
        assert match, f"Could not extract block for {rubric}"
        assert "✅" in match.group(0), f"{rubric} has no critical criterion"


def test_reviewer_and_verifier_roles_exist():
    assert (PROJECT_ROOT / ".agents" / "roles" / "reviewer.md").is_file()
    assert (PROJECT_ROOT / ".agents" / "roles" / "verifier.md").is_file()


def test_h06_fails_missing_rubric_evaluation(session):
    session_uuid, artifacts_dir = session
    write_verification_report(artifacts_dir, session_uuid, "")
    returncode, output = run_runner(artifacts_dir, session_uuid)
    assert returncode == 1
    check_ids = {c["id"] for c in output.get("checks", [])}
    assert "rubric_evaluation_section_present" in check_ids


def test_h06_fails_missing_rubric_subsection(session):
    session_uuid, artifacts_dir = session
    section = """## Rubric Evaluation

### TASK_SPECIFICATION_RUBRIC

- ✅ Objective clarity
  - Level: MEETS
  - Evidence: ok
"""
    write_verification_report(artifacts_dir, session_uuid, section)
    returncode, output = run_runner(artifacts_dir, session_uuid)
    assert returncode == 1
    check_ids = {c["id"] for c in output.get("checks", [])}
    assert "rubric_evaluation_all_rubrics_present" in check_ids


def test_h06_passes_complete_rubric_evaluation(session):
    session_uuid, artifacts_dir = session
    section = """## Rubric Evaluation

### TASK_SPECIFICATION_RUBRIC

- ✅ Objective clarity
  - Level: MEETS
  - Evidence: objective is clear

### CONTEXT_ARTIFACT_RUBRIC

- ✅ Relevance
  - Level: MEETS
  - Evidence: relevant

### CONTEXT_VALIDATION_REPORT_RUBRIC

- ✅ Decision clarity
  - Level: MEETS
  - Evidence: clear

### EXECUTION_PLAN_RUBRIC

- ✅ Approach alignment
  - Level: MEETS
  - Evidence: aligned

### EXECUTION_SUMMARY_RUBRIC

- ✅ Plan adherence
  - Level: MEETS
  - Evidence: adheres

### VERIFICATION_REPORT_RUBRIC

- ✅ Criteria evaluation
  - Level: MEETS
  - Evidence: evaluated
"""
    write_verification_report(artifacts_dir, session_uuid, section)
    returncode, output = run_runner(artifacts_dir, session_uuid)
    assert returncode == 0
    check_ids = {c["id"] for c in output.get("checks", [])}
    assert "rubric_evaluation_all_rubrics_present" in check_ids


def test_harness_report_includes_rubric_scores(session):
    session_uuid, artifacts_dir = session
    section = """## Rubric Evaluation

### TASK_SPECIFICATION_RUBRIC

- ✅ Objective clarity
  - Level: EXCEEDS
  - Evidence: objective is clear

### CONTEXT_ARTIFACT_RUBRIC

- ✅ Relevance
  - Level: MEETS
  - Evidence: relevant

### CONTEXT_VALIDATION_REPORT_RUBRIC

- ✅ Decision clarity
  - Level: MEETS
  - Evidence: clear

### EXECUTION_PLAN_RUBRIC

- ✅ Approach alignment
  - Level: MEETS
  - Evidence: aligned

### EXECUTION_SUMMARY_RUBRIC

- ✅ Plan adherence
  - Level: MEETS
  - Evidence: adheres

### VERIFICATION_REPORT_RUBRIC

- ✅ Criteria evaluation
  - Level: MEETS
  - Evidence: evaluated
"""
    write_verification_report(artifacts_dir, session_uuid, section)
    run_runner(artifacts_dir, session_uuid)
    report_path = artifacts_dir / session_uuid / "HARNESS_REPORT.md"
    assert report_path.is_file()
    report = report_path.read_text(encoding="utf-8")
    assert "## Rubric Scores" in report
    assert "TASK_SPECIFICATION_RUBRIC: EXCEEDS" in report
