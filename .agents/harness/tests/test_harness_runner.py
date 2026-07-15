import json
import os
import subprocess
import sys
import uuid
from pathlib import Path

import pytest

PROJECT_ROOT = Path(__file__).resolve().parents[3]
RUNNER_PATH = PROJECT_ROOT / ".agents" / "harness" / "runner.py"


@pytest.fixture
def session(tmp_path):
    """Create a temporary agent session directory outside the real .project/."""
    session_uuid = f"test-{uuid.uuid4()}"
    artifacts_dir = tmp_path / ".project"
    session_dir = artifacts_dir / session_uuid
    session_dir.mkdir(parents=True, exist_ok=True)
    yield session_uuid, artifacts_dir


# Fixed ordering prefix for artifacts inside an iteration. The prefix reflects the
# generation/reading order of the artifact within the workflow.
ARTIFACT_ORDER_PREFIX = {
    "TASK_ANALYSIS.md": "01",
    "TASK_SPECIFICATION.md": "02",
    "CONTEXT_ARTIFACT.md": "03",
    "CONTEXT_VALIDATION_REPORT.md": "04",
    "EXECUTION_PLAN.md": "05",
    "EXECUTION_SUMMARY.md": "06",
    "VERIFICATION_REPORT.md": "07",
}


def write_artifact(
    artifacts_dir: Path,
    session_uuid: str,
    name: str,
    content: str,
    iteration: str = "00",
) -> Path:
    iter_dir = artifacts_dir / session_uuid / iteration
    iter_dir.mkdir(parents=True, exist_ok=True)
    prefix = ARTIFACT_ORDER_PREFIX.get(name)
    filename = f"{prefix}-{name}" if prefix else name
    path = iter_dir / filename
    path.write_text(content, encoding="utf-8")
    return path


def write_artifact_no_prefix(
    artifacts_dir: Path,
    session_uuid: str,
    name: str,
    content: str,
    iteration: str = "00",
) -> Path:
    """Write an artifact without an order prefix (backwards-compatible case)."""
    iter_dir = artifacts_dir / session_uuid / iteration
    iter_dir.mkdir(parents=True, exist_ok=True)
    path = iter_dir / name
    path.write_text(content, encoding="utf-8")
    return path


def run_runner(
    artifacts_dir: Path,
    session_uuid: str,
    trigger: str,
    iteration: str | None = None,
    env_overrides: dict[str, str] | None = None,
) -> tuple[int, dict]:
    cmd = [
        sys.executable,
        str(RUNNER_PATH),
        "--session",
        session_uuid,
        "--trigger",
        trigger,
        "--artifacts-dir",
        str(artifacts_dir),
    ]
    if iteration is not None:
        cmd.extend(["--iteration", iteration])

    env = os.environ.copy()
    if env_overrides:
        env.update(env_overrides)

    result = subprocess.run(
        cmd,
        cwd=PROJECT_ROOT,
        capture_output=True,
        text=True,
        env=env,
    )
    try:
        output = json.loads(result.stdout) if result.stdout else {}
    except json.JSONDecodeError:
        output = {"raw_stdout": result.stdout, "stderr": result.stderr}
    return result.returncode, output


def test_h01_passes_valid_task_specification(session):
    session_uuid, artifacts_dir = session
    content = """# Task Specification

## Objective

Fix user validation.

## Expected outcome

Validation errors are clear.

## Scope

Included: schema changes.

## Constraints

No breaking changes.

## Acceptance Criteria

- The API shall reject empty names.

## Assumptions

None.

## Unknowns

None.

## Validation

Complete.
"""
    write_artifact(artifacts_dir, session_uuid, "TASK_SPECIFICATION.md", content)
    returncode, output = run_runner(artifacts_dir, session_uuid, "H01")

    assert returncode == 0
    assert output["result"] == "PASS"


def test_h01_finds_artifact_without_order_prefix(session):
    session_uuid, artifacts_dir = session
    content = """# Task Specification

## Objective

Fix user validation.

## Expected outcome

Validation errors are clear.

## Scope

Included: schema changes.

## Constraints

No breaking changes.

## Acceptance Criteria

- The API shall reject empty names.

## Assumptions

None.

## Unknowns

None.

## Validation

Complete.
"""
    write_artifact_no_prefix(
        artifacts_dir, session_uuid, "TASK_SPECIFICATION.md", content
    )
    returncode, output = run_runner(artifacts_dir, session_uuid, "H01")

    assert returncode == 0
    assert output["result"] == "PASS"
    assert "TASK_SPECIFICATION.md" in output["artifact"]


def test_h01_fails_missing_section(session):
    session_uuid, artifacts_dir = session
    content = """# Task Specification

## Objective

Fix user validation.
"""
    write_artifact(artifacts_dir, session_uuid, "TASK_SPECIFICATION.md", content)
    returncode, output = run_runner(artifacts_dir, session_uuid, "H01")

    assert returncode == 1
    assert output["result"] == "FAIL"
    assert any(c["id"] == "has_section_acceptance_criteria" for c in output["checks"])


def test_h01_fails_missing_artifact(session):
    session_uuid, artifacts_dir = session
    returncode, output = run_runner(artifacts_dir, session_uuid, "H01")

    assert returncode == 1
    assert output["result"] == "FAIL"
    assert any(
        c["id"] == "artifact_exists" and c["result"] == "FAIL" for c in output["checks"]
    )


def test_unknown_trigger_returns_error(session):
    session_uuid, artifacts_dir = session
    returncode, output = run_runner(artifacts_dir, session_uuid, "H99")

    assert returncode == 1
    assert output["result"] == "FAIL"
    assert "Policy not found" in (output.get("error") or "")


def test_harness_report_is_updated(session):
    session_uuid, artifacts_dir = session
    content = """# Task Specification

## Objective

Fix user validation.

## Expected outcome

Validation errors are clear.

## Scope

Included: schema changes.

## Constraints

No breaking changes.

## Acceptance Criteria

- The API shall reject empty names.

## Assumptions

None.

## Unknowns

None.

## Validation

Complete.
"""
    write_artifact(artifacts_dir, session_uuid, "TASK_SPECIFICATION.md", content)
    run_runner(artifacts_dir, session_uuid, "H01")

    report_path = artifacts_dir / session_uuid / "HARNESS_REPORT.md"
    assert report_path.exists()
    report = report_path.read_text(encoding="utf-8")
    assert "H01" in report
    assert "PASS" in report


def test_h05_validates_execution_summary(session):
    session_uuid, artifacts_dir = session
    content = """# Execution Summary

## Metadata

```yaml
id: "test"
created_at: "2024-01-01T00:00:00Z"
status: "DONE"
```

## Task Reference

Reference.

## Execution Plan Reference

Reference.

## Summary of Changes

Summary.

## Steps Executed

```yaml
steps_executed:
  - order: 1
    action: "Update schema"
    status: "COMPLETED"
```

## Project Files Modified

None.

## Intermediate Validations

All passed.

## Issues or Deviations

None.

## Final Project State

```yaml
final_state:
  status: "VERIFIABLE"
  reasoning: "Tests pass."
```

## Confidence

High.
"""
    write_artifact(artifacts_dir, session_uuid, "EXECUTION_SUMMARY.md", content)
    returncode, output = run_runner(artifacts_dir, session_uuid, "H05")

    assert returncode == 0
    assert output["result"] == "PASS"
    assert output["trigger"] == "H05"
    assert any(
        c["id"] == "final_state_verifiable" and c["result"] == "PASS"
        for c in output["checks"]
    )
    assert any(
        c["id"] == "all_steps_completed_or_skipped" and c["result"] == "PASS"
        for c in output["checks"]
    )


def test_ears_valid_patterns(session):
    session_uuid, artifacts_dir = session
    content = """# Task Specification

## Objective

Improve API responses.

## Expected outcome

Clear status codes.

## Scope

User endpoints.

## Constraints

None.

## Acceptance Criteria

- The API shall return HTTP 201 when a user is created successfully.
- When the email is already registered, the API shall return HTTP 409.
- While the database is unavailable, the API shall return HTTP 503.
- If the user ID does not exist, then the API shall return HTTP 404.
- Where email validation is enabled, the API shall reject malformed email addresses.

## Assumptions

None.

## Unknowns

None.

## Validation

Complete.
"""
    write_artifact(artifacts_dir, session_uuid, "TASK_SPECIFICATION.md", content)
    returncode, output = run_runner(artifacts_dir, session_uuid, "H01")

    assert returncode == 0
    assert output["result"] == "PASS"
    ears_checks = [c for c in output["checks"] if c["id"].startswith("ears_pattern_")]
    assert len(ears_checks) == 5
    assert all(c["result"] == "PASS" for c in ears_checks)


def test_ears_rejects_informal_criterion(session):
    session_uuid, artifacts_dir = session
    content = """# Task Specification

## Objective

Improve API responses.

## Expected outcome

Clear status codes.

## Scope

User endpoints.

## Constraints

None.

## Acceptance Criteria

- The API should handle errors gracefully.

## Assumptions

None.

## Unknowns

None.

## Validation

Complete.
"""
    write_artifact(artifacts_dir, session_uuid, "TASK_SPECIFICATION.md", content)
    returncode, output = run_runner(artifacts_dir, session_uuid, "H01")

    assert returncode == 1
    assert output["result"] == "FAIL"
    assert any(
        c["id"].startswith("ears_pattern_") and c["result"] == "FAIL"
        for c in output["checks"]
    )


def test_ears_rejects_compound_criterion(session):
    session_uuid, artifacts_dir = session
    content = """# Task Specification

## Objective

Improve API responses.

## Expected outcome

Clear status codes.

## Scope

User endpoints.

## Constraints

None.

## Acceptance Criteria

- The API shall validate input and return errors.

## Assumptions

None.

## Unknowns

None.

## Validation

Complete.
"""
    write_artifact(artifacts_dir, session_uuid, "TASK_SPECIFICATION.md", content)
    returncode, output = run_runner(artifacts_dir, session_uuid, "H01")

    assert returncode == 1
    assert output["result"] == "FAIL"
    assert any(
        c["id"].startswith("ears_atomic_") and c["result"] == "FAIL"
        for c in output["checks"]
    )


def test_h07_passes_with_valid_scope_compliance(session):
    session_uuid, artifacts_dir = session
    content = """# Verification Report

## Scope Compliance

```yaml
scope_compliance:
  scope_respected: true
  unplanned_changes: []
  out_of_scope_issues: []
  user_authorized_extra_work: false
  notes: "Only planned work was performed."
```
"""
    write_artifact(artifacts_dir, session_uuid, "VERIFICATION_REPORT.md", content)
    returncode, output = run_runner(artifacts_dir, session_uuid, "H07")

    assert returncode == 0
    assert output["result"] == "PASS"
    assert any(
        c["id"] == "scope_respected_true" and c["result"] == "PASS"
        for c in output["checks"]
    )
    assert any(
        c["id"] == "unplanned_changes_empty" and c["result"] == "PASS"
        for c in output["checks"]
    )
    assert any(
        c["id"] == "no_unauthorized_extra_work" and c["result"] == "PASS"
        for c in output["checks"]
    )


def test_h07_fails_scope_respected_false(session):
    session_uuid, artifacts_dir = session
    content = """# Verification Report

## Scope Compliance

```yaml
scope_compliance:
  scope_respected: false
  unplanned_changes: []
  user_authorized_extra_work: false
```
"""
    write_artifact(artifacts_dir, session_uuid, "VERIFICATION_REPORT.md", content)
    returncode, output = run_runner(artifacts_dir, session_uuid, "H07")

    assert returncode == 1
    assert output["result"] == "FAIL"
    assert any(
        c["id"] == "scope_respected_true" and c["result"] == "FAIL"
        for c in output["checks"]
    )


def test_h07_fails_unplanned_changes_not_empty(session):
    session_uuid, artifacts_dir = session
    content = """# Verification Report

## Scope Compliance

```yaml
scope_compliance:
  scope_respected: true
  unplanned_changes:
    - "foo.py"
  user_authorized_extra_work: false
```
"""
    write_artifact(artifacts_dir, session_uuid, "VERIFICATION_REPORT.md", content)
    returncode, output = run_runner(artifacts_dir, session_uuid, "H07")

    assert returncode == 1
    assert output["result"] == "FAIL"
    assert any(
        c["id"] == "unplanned_changes_empty" and c["result"] == "FAIL"
        for c in output["checks"]
    )


def test_h06_fails_when_decision_is_failed(session):
    session_uuid, artifacts_dir = session
    content = """# Verification Report

## Final Decision

```yaml
decision:
  result: "FAILED"
```

## Acceptance Criteria Evaluation

```yaml
acceptance_criteria:
  - criterion: "The API shall reject empty names."
    result: "PASS"
    evidence: "Tested."
```
"""
    write_artifact(artifacts_dir, session_uuid, "VERIFICATION_REPORT.md", content)
    returncode, output = run_runner(artifacts_dir, session_uuid, "H06")

    assert returncode == 1
    assert output["result"] == "FAIL"
    assert any(
        c["id"] == "final_decision_completed" and c["result"] == "FAIL"
        for c in output["checks"]
    )


def test_h05_fails_when_final_state_blocked(session):
    session_uuid, artifacts_dir = session
    content = """# Execution Summary

## Metadata

```yaml
id: "test"
created_at: "2024-01-01T00:00:00Z"
status: "DONE"
```

## Task Reference

Reference.

## Execution Plan Reference

Reference.

## Summary of Changes

Summary.

## Steps Executed

```yaml
steps_executed:
  - order: 1
    action: "Update schema"
    status: "COMPLETED"
```

## Project Files Modified

None.

## Intermediate Validations

All passed.

## Issues or Deviations

None.

## Final Project State

```yaml
final_state:
  status: "BLOCKED"
  reasoning: "Tests fail."
```

## Confidence

High.
"""
    write_artifact(artifacts_dir, session_uuid, "EXECUTION_SUMMARY.md", content)
    returncode, output = run_runner(artifacts_dir, session_uuid, "H05")

    assert returncode == 1
    assert output["result"] == "FAIL"
    assert any(
        c["id"] == "final_state_verifiable" and c["result"] == "FAIL"
        for c in output["checks"]
    )


def test_h05_fails_when_final_state_invalid(session):
    session_uuid, artifacts_dir = session
    content = """# Execution Summary

## Metadata

```yaml
id: "test"
created_at: "2024-01-01T00:00:00Z"
status: "DONE"
```

## Task Reference

Reference.

## Execution Plan Reference

Reference.

## Summary of Changes

Summary.

## Steps Executed

```yaml
steps_executed:
  - order: 1
    action: "Update schema"
    status: "COMPLETED"
```

## Project Files Modified

None.

## Intermediate Validations

All passed.

## Issues or Deviations

None.

## Final Project State

```yaml
final_state:
  status: "UNKNOWN"
  reasoning: "Unexpected status."
```

## Confidence

High.
"""
    write_artifact(artifacts_dir, session_uuid, "EXECUTION_SUMMARY.md", content)
    returncode, output = run_runner(artifacts_dir, session_uuid, "H05")

    assert returncode == 1
    assert output["result"] == "FAIL"
    assert any(
        c["id"] == "final_state_status_valid" and c["result"] == "FAIL"
        for c in output["checks"]
    )


def test_h05_fails_when_step_blocked(session):
    session_uuid, artifacts_dir = session
    content = """# Execution Summary

## Metadata

```yaml
id: "test"
created_at: "2024-01-01T00:00:00Z"
status: "DONE"
```

## Task Reference

Reference.

## Execution Plan Reference

Reference.

## Summary of Changes

Summary.

## Steps Executed

```yaml
steps_executed:
  - order: 1
    action: "Update schema"
    status: "BLOCKED"
```

## Project Files Modified

None.

## Intermediate Validations

All passed.

## Issues or Deviations

None.

## Final Project State

```yaml
final_state:
  status: "VERIFIABLE"
  reasoning: "Tests pass."
```

## Confidence

High.
"""
    write_artifact(artifacts_dir, session_uuid, "EXECUTION_SUMMARY.md", content)
    returncode, output = run_runner(artifacts_dir, session_uuid, "H05")

    assert returncode == 1
    assert output["result"] == "FAIL"
    assert any(
        c["id"] == "step_1_completed_or_skipped" and c["result"] == "FAIL"
        for c in output["checks"]
    )


def test_h06_fails_when_acceptance_criterion_failed(session):
    session_uuid, artifacts_dir = session
    content = """# Verification Report

## Final Decision

```yaml
decision:
  result: "COMPLETED"
  reasoning: "All good."
```

## Acceptance Criteria Evaluation

```yaml
acceptance_criteria:
  - criterion: "The API shall reject empty names."
    result: "FAIL"
    evidence: "Not implemented."
```
"""
    write_artifact(artifacts_dir, session_uuid, "VERIFICATION_REPORT.md", content)
    returncode, output = run_runner(artifacts_dir, session_uuid, "H06")

    assert returncode == 1
    assert output["result"] == "FAIL"
    assert any(
        c["id"] == "acceptance_criterion_1_not_failed" and c["result"] == "FAIL"
        for c in output["checks"]
    )


def test_h09_validates_recovery_report(session):
    session_uuid, artifacts_dir = session
    content = """# Recovery Report

## Metadata

Recovery metadata.

## Failure Reference

Reference.

## Failure Summary

Summary.

## Root Cause Classification

Root cause.

## Analysis Summary

Analysis.

## Corrective Action Recommendation

Recommendation.

## Updated Artifacts

None.

## Confidence

High.
"""
    write_artifact(artifacts_dir, session_uuid, "RECOVERY_REPORT.md", content)
    returncode, output = run_runner(artifacts_dir, session_uuid, "H09")

    assert returncode == 0
    assert output["result"] == "PASS"


def test_h09_fails_missing_recovery_report_section(session):
    session_uuid, artifacts_dir = session
    content = """# Recovery Report

## Metadata

Recovery metadata.
"""
    write_artifact(artifacts_dir, session_uuid, "RECOVERY_REPORT.md", content)
    returncode, output = run_runner(artifacts_dir, session_uuid, "H09")

    assert returncode == 1
    assert output["result"] == "FAIL"


def test_h10_validates_kb_discovery_report(session):
    session_uuid, artifacts_dir = session
    content = """# KB Discovery Report

## Discovery Objective

Find relevant KB entries.

## Recommended Entries

None.

## Context Budget Recommendation

4000

## Notes

No notes.
"""
    write_artifact(artifacts_dir, session_uuid, "KB_DISCOVERY_REPORT.md", content)
    returncode, output = run_runner(artifacts_dir, session_uuid, "H10")

    assert returncode == 0
    assert output["result"] == "PASS"


def test_h10_fails_missing_kb_discovery_report_section(session):
    session_uuid, artifacts_dir = session
    content = """# KB Discovery Report

## Discovery Objective

Find relevant KB entries.
"""
    write_artifact(artifacts_dir, session_uuid, "KB_DISCOVERY_REPORT.md", content)
    returncode, output = run_runner(artifacts_dir, session_uuid, "H10")

    assert returncode == 1
    assert output["result"] == "FAIL"


def test_h01_passes_with_valid_tdd_approach(session):
    session_uuid, artifacts_dir = session
    content = """# Task Specification

## Objective

Fix user validation.

## Expected outcome

Validation errors are clear.

## Scope

Included: schema changes.

## Constraints

No breaking changes.

## Technical Approach

```yaml
technical_approach:
  enabled:
    - "tdd"
  notes:
    - "Write a failing test for empty-name validation before the fix."
```

## Acceptance Criteria

- The API shall reject empty names.

## Assumptions

None.

## Unknowns

None.

## Validation

Complete.
"""
    write_artifact(artifacts_dir, session_uuid, "TASK_SPECIFICATION.md", content)
    returncode, output = run_runner(
        artifacts_dir,
        session_uuid,
        "H01",
        env_overrides={"AGENTS_FEATURE_TDD": "true"},
    )

    assert returncode == 0
    assert output["result"] == "PASS"
    assert any(
        c["id"] == "tdd_flag_enabled" and c["result"] == "PASS"
        for c in output["checks"]
    )
    assert any(
        c["id"] == "technical_approach_has_notes" and c["result"] == "PASS"
        for c in output["checks"]
    )


def test_h01_fails_tdd_without_notes(session):
    session_uuid, artifacts_dir = session
    content = """# Task Specification

## Objective

Fix user validation.

## Expected outcome

Validation errors are clear.

## Scope

Included: schema changes.

## Constraints

No breaking changes.

## Technical Approach

```yaml
technical_approach:
  enabled:
    - "tdd"
  notes: []
```

## Acceptance Criteria

- The API shall reject empty names.

## Assumptions

None.

## Unknowns

None.

## Validation

Complete.
"""
    write_artifact(artifacts_dir, session_uuid, "TASK_SPECIFICATION.md", content)
    returncode, output = run_runner(
        artifacts_dir,
        session_uuid,
        "H01",
        env_overrides={"AGENTS_FEATURE_TDD": "true"},
    )

    assert returncode == 1
    assert output["result"] == "FAIL"
    assert any(
        c["id"] == "technical_approach_has_notes" and c["result"] == "FAIL"
        for c in output["checks"]
    )


def test_h05_passes_with_tdd_evidence(session):
    session_uuid, artifacts_dir = session
    spec = """# Task Specification

## Objective

Fix user validation.

## Expected outcome

Validation errors are clear.

## Scope

Included: schema changes.

## Constraints

No breaking changes.

## Technical Approach

```yaml
technical_approach:
  enabled:
    - "tdd"
  notes:
    - "Write a failing test before the fix."
```

## Acceptance Criteria

- The API shall reject empty names.

## Assumptions

None.

## Unknowns

None.

## Validation

Complete.
"""
    summary = """# Execution Summary

## Metadata

```yaml
id: "test"
created_at: "2024-01-01T00:00:00Z"
status: "DONE"
```

## Task Reference

Reference.

## Execution Plan Reference

Reference.

## Summary of Changes

Summary.

## Steps Executed

```yaml
steps_executed:
  - order: 1
    action: "Write failing test and fix validation"
    status: "COMPLETED"
```

## Project Files Modified

None.

## Intermediate Validations

All passed.

## Technical Practice Evidence

```yaml
technical_practice_evidence:
  tdd:
    applied: true
    failing_tests:
      - file: "tests/test_users.py"
        description: "Test that reproduces the empty-name bug"
    production_changes:
      - file: "app/schemas/user.py"
        description: "Added empty-name validation"
    final_test_result: "PASS"
    reason: ""
```

## Issues or Deviations

None.

## Final Project State

```yaml
final_state:
  status: "VERIFIABLE"
  reasoning: "Tests pass."
```

## Confidence

High.
"""
    write_artifact(artifacts_dir, session_uuid, "TASK_SPECIFICATION.md", spec)
    write_artifact(artifacts_dir, session_uuid, "EXECUTION_SUMMARY.md", summary)
    returncode, output = run_runner(
        artifacts_dir,
        session_uuid,
        "H05",
        env_overrides={"AGENTS_FEATURE_TDD": "true"},
    )

    assert returncode == 0
    assert output["result"] == "PASS"
    assert any(
        c["id"] == "tdd_evidence_present" and c["result"] == "PASS"
        for c in output["checks"]
    )
    assert any(
        c["id"] == "tdd_evidence_nonempty" and c["result"] == "PASS"
        for c in output["checks"]
    )


def test_h05_fails_missing_tdd_evidence(session):
    session_uuid, artifacts_dir = session
    spec = """# Task Specification

## Objective

Fix user validation.

## Expected outcome

Validation errors are clear.

## Scope

Included: schema changes.

## Constraints

No breaking changes.

## Technical Approach

```yaml
technical_approach:
  enabled:
    - "tdd"
  notes:
    - "Write a failing test before the fix."
```

## Acceptance Criteria

- The API shall reject empty names.

## Assumptions

None.

## Unknowns

None.

## Validation

Complete.
"""
    summary = """# Execution Summary

## Metadata

```yaml
id: "test"
created_at: "2024-01-01T00:00:00Z"
status: "DONE"
```

## Task Reference

Reference.

## Execution Plan Reference

Reference.

## Summary of Changes

Summary.

## Steps Executed

```yaml
steps_executed:
  - order: 1
    action: "Fix validation"
    status: "COMPLETED"
```

## Project Files Modified

None.

## Intermediate Validations

All passed.

## Issues or Deviations

None.

## Final Project State

```yaml
final_state:
  status: "VERIFIABLE"
  reasoning: "Tests pass."
```

## Confidence

High.
"""
    write_artifact(artifacts_dir, session_uuid, "TASK_SPECIFICATION.md", spec)
    write_artifact(artifacts_dir, session_uuid, "EXECUTION_SUMMARY.md", summary)
    returncode, output = run_runner(
        artifacts_dir,
        session_uuid,
        "H05",
        env_overrides={"AGENTS_FEATURE_TDD": "true"},
    )

    assert returncode == 1
    assert output["result"] == "FAIL"
    assert any(
        c["id"] == "tdd_evidence_present" and c["result"] == "FAIL"
        for c in output["checks"]
    )


def test_h05_skips_tdd_validation_when_not_required(session):
    session_uuid, artifacts_dir = session
    spec = """# Task Specification

## Objective

Fix user validation.

## Expected outcome

Validation errors are clear.

## Scope

Included: schema changes.

## Constraints

No breaking changes.

## Technical Approach

```yaml
technical_approach:
  enabled: []
  notes: []
```

## Acceptance Criteria

- The API shall reject empty names.

## Assumptions

None.

## Unknowns

None.

## Validation

Complete.
"""
    summary = """# Execution Summary

## Metadata

```yaml
id: "test"
created_at: "2024-01-01T00:00:00Z"
status: "DONE"
```

## Task Reference

Reference.

## Execution Plan Reference

Reference.

## Summary of Changes

Summary.

## Steps Executed

```yaml
steps_executed:
  - order: 1
    action: "Fix validation"
    status: "COMPLETED"
```

## Project Files Modified

None.

## Intermediate Validations

All passed.

## Issues or Deviations

None.

## Final Project State

```yaml
final_state:
  status: "VERIFIABLE"
  reasoning: "Tests pass."
```

## Confidence

High.
"""
    write_artifact(artifacts_dir, session_uuid, "TASK_SPECIFICATION.md", spec)
    write_artifact(artifacts_dir, session_uuid, "EXECUTION_SUMMARY.md", summary)
    returncode, output = run_runner(
        artifacts_dir,
        session_uuid,
        "H05",
        env_overrides={"AGENTS_FEATURE_TDD": "true"},
    )

    assert returncode == 0
    assert output["result"] == "PASS"
    assert any(
        c["id"] == "technical_practices_not_required" and c["result"] == "PASS"
        for c in output["checks"]
    )


def test_h01_fails_unknown_technical_practice(session):
    session_uuid, artifacts_dir = session
    content = """# Task Specification

## Objective

Fix user validation.

## Expected outcome

Validation errors are clear.

## Scope

Included: schema changes.

## Constraints

No breaking changes.

## Technical Approach

```yaml
technical_approach:
  enabled:
    - "foo"
  notes:
    - "foo is not a known practice"
```

## Acceptance Criteria

- The API shall reject empty names.

## Assumptions

None.

## Unknowns

None.

## Validation

Complete.
"""
    write_artifact(artifacts_dir, session_uuid, "TASK_SPECIFICATION.md", content)
    returncode, output = run_runner(
        artifacts_dir,
        session_uuid,
        "H01",
        env_overrides={"AGENTS_FEATURE_TDD": "true"},
    )

    assert returncode == 1
    assert output["result"] == "FAIL"
    assert any(
        c["id"] == "foo_flag_known" and c["result"] == "FAIL" for c in output["checks"]
    )


def test_h01_fails_practice_not_enabled_globally(session):
    session_uuid, artifacts_dir = session
    content = """# Task Specification

## Objective

Fix user validation.

## Expected outcome

Validation errors are clear.

## Scope

Included: schema changes.

## Constraints

No breaking changes.

## Technical Approach

```yaml
technical_approach:
  enabled:
    - "srp"
  notes:
    - "SRP should be applied."
```

## Acceptance Criteria

- The API shall reject empty names.

## Assumptions

None.

## Unknowns

None.

## Validation

Complete.
"""
    write_artifact(artifacts_dir, session_uuid, "TASK_SPECIFICATION.md", content)
    returncode, output = run_runner(
        artifacts_dir,
        session_uuid,
        "H01",
        env_overrides={"AGENTS_FEATURE_TDD": "true", "AGENTS_FEATURE_SRP": "false"},
    )

    assert returncode == 1
    assert output["result"] == "FAIL"
    assert any(
        c["id"] == "srp_flag_enabled" and c["result"] == "FAIL"
        for c in output["checks"]
    )


def test_h05_passes_with_srp_evidence(session):
    session_uuid, artifacts_dir = session
    spec = """# Task Specification

## Objective

Fix user validation.

## Expected outcome

Validation errors are clear.

## Scope

Included: schema changes.

## Constraints

No breaking changes.

## Technical Approach

```yaml
technical_approach:
  enabled:
    - "srp"
  notes:
    - "Extraer responsabilidad de validación."
```

## Acceptance Criteria

- The API shall reject empty names.

## Assumptions

None.

## Unknowns

None.

## Validation

Complete.
"""
    summary = """# Execution Summary

## Metadata

```yaml
id: "test"
created_at: "2024-01-01T00:00:00Z"
status: "DONE"
```

## Task Reference

Reference.

## Execution Plan Reference

Reference.

## Summary of Changes

Summary.

## Steps Executed

```yaml
steps_executed:
  - order: 1
    action: "Extract email validation responsibility"
    status: "COMPLETED"
```

## Project Files Modified

None.

## Intermediate Validations

All passed.

## Technical Practice Evidence

```yaml
technical_practice_evidence:
  srp:
    applied: true
    responsibilities_identified:
      - location: "app/services/user_service.py"
        responsibility: "Validación de email"
    extraction:
      - from: "app/services/user_service.py"
        to: "app/services/email_validator.py"
        reasoning: "La validación no era responsabilidad del servicio."
```

## Issues or Deviations

None.

## Final Project State

```yaml
final_state:
  status: "VERIFIABLE"
  reasoning: "Refactor completed."
```

## Confidence

High.
"""
    write_artifact(artifacts_dir, session_uuid, "TASK_SPECIFICATION.md", spec)
    write_artifact(artifacts_dir, session_uuid, "EXECUTION_SUMMARY.md", summary)
    returncode, output = run_runner(
        artifacts_dir,
        session_uuid,
        "H05",
        env_overrides={"AGENTS_FEATURE_SRP": "true"},
    )

    assert returncode == 0
    assert output["result"] == "PASS"
    assert any(
        c["id"] == "srp_evidence_present" and c["result"] == "PASS"
        for c in output["checks"]
    )
    assert any(
        c["id"] == "srp_evidence_nonempty" and c["result"] == "PASS"
        for c in output["checks"]
    )


def test_h05_fails_missing_srp_evidence(session):
    session_uuid, artifacts_dir = session
    spec = """# Task Specification

## Objective

Fix user validation.

## Expected outcome

Validation errors are clear.

## Scope

Included: schema changes.

## Constraints

No breaking changes.

## Technical Approach

```yaml
technical_approach:
  enabled:
    - "srp"
  notes:
    - "Extraer responsabilidad de validación."
```

## Acceptance Criteria

- The API shall reject empty names.

## Assumptions

None.

## Unknowns

None.

## Validation

Complete.
"""
    summary = """# Execution Summary

## Metadata

```yaml
id: "test"
created_at: "2024-01-01T00:00:00Z"
status: "DONE"
```

## Task Reference

Reference.

## Execution Plan Reference

Reference.

## Summary of Changes

Summary.

## Steps Executed

```yaml
steps_executed:
  - order: 1
    action: "Fix validation"
    status: "COMPLETED"
```

## Project Files Modified

None.

## Intermediate Validations

All passed.

## Issues or Deviations

None.

## Final Project State

```yaml
final_state:
  status: "VERIFIABLE"
  reasoning: "Tests pass."
```

## Confidence

High.
"""
    write_artifact(artifacts_dir, session_uuid, "TASK_SPECIFICATION.md", spec)
    write_artifact(artifacts_dir, session_uuid, "EXECUTION_SUMMARY.md", summary)
    returncode, output = run_runner(
        artifacts_dir,
        session_uuid,
        "H05",
        env_overrides={"AGENTS_FEATURE_SRP": "true"},
    )

    assert returncode == 1
    assert output["result"] == "FAIL"
    assert any(
        c["id"] == "srp_evidence_present" and c["result"] == "FAIL"
        for c in output["checks"]
    )


def test_h05_passes_with_dip_evidence(session):
    session_uuid, artifacts_dir = session
    spec = """# Task Specification

## Objective

Fix user validation.

## Expected outcome

Validation errors are clear.

## Scope

Included: schema changes.

## Constraints

No breaking changes.

## Technical Approach

```yaml
technical_approach:
  enabled:
    - "dip"
  notes:
    - "Invertir dependencia del servicio hacia un repositorio abstracto."
```

## Acceptance Criteria

- The API shall reject empty names.

## Assumptions

None.

## Unknowns

None.

## Validation

Complete.
"""
    summary = """# Execution Summary

## Metadata

```yaml
id: "test"
created_at: "2024-01-01T00:00:00Z"
status: "DONE"
```

## Task Reference

Reference.

## Execution Plan Reference

Reference.

## Summary of Changes

Summary.

## Steps Executed

```yaml
steps_executed:
  - order: 1
    action: "Introduce UserRepository abstraction"
    status: "COMPLETED"
```

## Project Files Modified

None.

## Intermediate Validations

All passed.

## Technical Practice Evidence

```yaml
technical_practice_evidence:
  dip:
    applied: true
    abstractions_introduced:
      - name: "UserRepository"
        location: "app/repositories/user_repository.py"
    dependencies_inverted:
      - module: "app/services/user_service.py"
        now_depends_on: "UserRepository"
        previously_depended_on: "app.db.session"
```

## Issues or Deviations

None.

## Final Project State

```yaml
final_state:
  status: "VERIFIABLE"
  reasoning: "Refactor completed."
```

## Confidence

High.
"""
    write_artifact(artifacts_dir, session_uuid, "TASK_SPECIFICATION.md", spec)
    write_artifact(artifacts_dir, session_uuid, "EXECUTION_SUMMARY.md", summary)
    returncode, output = run_runner(
        artifacts_dir,
        session_uuid,
        "H05",
        env_overrides={"AGENTS_FEATURE_DIP": "true"},
    )

    assert returncode == 0
    assert output["result"] == "PASS"
    assert any(
        c["id"] == "dip_evidence_present" and c["result"] == "PASS"
        for c in output["checks"]
    )


def test_h06_passes_with_technical_practice_rubric(session):
    session_uuid, artifacts_dir = session
    spec = """# Task Specification

## Objective

Fix user validation.

## Expected outcome

Validation errors are clear.

## Scope

Included: schema changes.

## Constraints

No breaking changes.

## Technical Approach

```yaml
technical_approach:
  enabled:
    - "tdd"
  notes:
    - "Write a failing test before the fix."
```

## Acceptance Criteria

- The API shall reject empty names.

## Assumptions

None.

## Unknowns

None.

## Validation

Complete.
"""
    report = """# Verification Report

## Metadata

```yaml
id: "test"
created_at: "2024-01-01T00:00:00Z"
status: "DONE"
```

## Task Reference

Reference.

## Execution Plan Reference

Reference.

## Verification Objective

Verify the fix.

## Acceptance Criteria Evaluation

```yaml
acceptance_criteria:
  - criterion: "The API shall reject empty names."
    result: "PASS"
    evidence: "Tested."
```

## Test Results

All tests pass.

## Issues Found

None.

## Final Decision

```yaml
decision:
  result: "COMPLETED"
  reasoning: "All criteria met."
```

## Confidence

High.

## State Transition

```yaml
transition:
  current_state: "VERIFYING"
  next_state: "COMPLETED"
```

## Rubric Evaluation

### TASK_SPECIFICATION_RUBRIC

- ✅ Objective clarity
  - Level: MEETS
  - Evidence: objective is specific

### CONTEXT_ARTIFACT_RUBRIC

- Relevance
  - Level: MEETS
  - Evidence: relevant

### CONTEXT_VALIDATION_REPORT_RUBRIC

- Decision clarity
  - Level: MEETS
  - Evidence: clear

### EXECUTION_PLAN_RUBRIC

- Approach alignment
  - Level: MEETS
  - Evidence: aligned

### EXECUTION_SUMMARY_RUBRIC

- Plan adherence
  - Level: MEETS
  - Evidence: followed

### VERIFICATION_REPORT_RUBRIC

- Criteria evaluation
  - Level: MEETS
  - Evidence: evaluated

### TDD_RUBRIC

- ✅ Failing test first
  - Level: MEETS
  - Evidence: test was written before fix
- Test result recorded
  - Level: MEETS
  - Evidence: final result PASS
"""
    write_artifact(artifacts_dir, session_uuid, "TASK_SPECIFICATION.md", spec)
    write_artifact(artifacts_dir, session_uuid, "VERIFICATION_REPORT.md", report)
    returncode, output = run_runner(
        artifacts_dir,
        session_uuid,
        "H06",
        env_overrides={"AGENTS_FEATURE_TDD": "true", "AGENTS_FEATURE_RUBRICS": "true"},
    )

    assert returncode == 0
    assert output["result"] == "PASS"
    assert any(
        c["id"] == "rubric_evaluation_all_rubrics_present" and c["result"] == "PASS"
        for c in output["checks"]
    )


def test_h06_fails_when_technical_practice_rubric_missing(session):
    session_uuid, artifacts_dir = session
    spec = """# Task Specification

## Objective

Fix user validation.

## Expected outcome

Validation errors are clear.

## Scope

Included: schema changes.

## Constraints

No breaking changes.

## Technical Approach

```yaml
technical_approach:
  enabled:
    - "tdd"
  notes:
    - "Write a failing test before the fix."
```

## Acceptance Criteria

- The API shall reject empty names.

## Assumptions

None.

## Unknowns

None.

## Validation

Complete.
"""
    report = """# Verification Report

## Metadata

```yaml
id: "test"
created_at: "2024-01-01T00:00:00Z"
status: "DONE"
```

## Task Reference

Reference.

## Execution Plan Reference

Reference.

## Verification Objective

Verify the fix.

## Acceptance Criteria Evaluation

```yaml
acceptance_criteria:
  - criterion: "The API shall reject empty names."
    result: "PASS"
    evidence: "Tested."
```

## Test Results

All tests pass.

## Issues Found

None.

## Final Decision

```yaml
decision:
  result: "COMPLETED"
  reasoning: "All criteria met."
```

## Confidence

High.

## State Transition

```yaml
transition:
  current_state: "VERIFYING"
  next_state: "COMPLETED"
```

## Rubric Evaluation

### TASK_SPECIFICATION_RUBRIC

- ✅ Objective clarity
  - Level: MEETS
  - Evidence: objective is specific

### CONTEXT_ARTIFACT_RUBRIC

- Relevance
  - Level: MEETS
  - Evidence: relevant

### CONTEXT_VALIDATION_REPORT_RUBRIC

- Decision clarity
  - Level: MEETS
  - Evidence: clear

### EXECUTION_PLAN_RUBRIC

- Approach alignment
  - Level: MEETS
  - Evidence: aligned

### EXECUTION_SUMMARY_RUBRIC

- Plan adherence
  - Level: MEETS
  - Evidence: followed

### VERIFICATION_REPORT_RUBRIC

- Criteria evaluation
  - Level: MEETS
  - Evidence: evaluated
"""
    write_artifact(artifacts_dir, session_uuid, "TASK_SPECIFICATION.md", spec)
    write_artifact(artifacts_dir, session_uuid, "VERIFICATION_REPORT.md", report)
    returncode, output = run_runner(
        artifacts_dir,
        session_uuid,
        "H06",
        env_overrides={"AGENTS_FEATURE_TDD": "true", "AGENTS_FEATURE_RUBRICS": "true"},
    )

    assert returncode == 1
    assert output["result"] == "FAIL"
    assert any(
        c["id"] == "rubric_evaluation_all_rubrics_present" and c["result"] == "FAIL"
        for c in output["checks"]
    )


def _task_spec_with_practice(practice: str, notes: str) -> str:
    return f"""# Task Specification

## Objective

Fix user validation.

## Expected outcome

Validation errors are clear.

## Scope

Included: schema changes.

## Constraints

No breaking changes.

## Technical Approach

```yaml
technical_approach:
  enabled:
    - "{practice}"
  notes:
    - "{notes}"
```

## Acceptance Criteria

- The API shall reject empty names.

## Assumptions

None.

## Unknowns

None.

## Validation

Complete.
"""


def _execution_summary_with_evidence(evidence_yaml: str) -> str:
    return f"""# Execution Summary

## Metadata

```yaml
id: "test"
created_at: "2024-01-01T00:00:00Z"
status: "DONE"
```

## Task Reference

Reference.

## Execution Plan Reference

Reference.

## Summary of Changes

Summary.

## Steps Executed

```yaml
steps_executed:
  - order: 1
    action: "Apply technical practice"
    status: "COMPLETED"
```

## Project Files Modified

None.

## Intermediate Validations

All passed.

## Technical Practice Evidence

```yaml
technical_practice_evidence:
{evidence_yaml}
```

## Issues or Deviations

None.

## Final Project State

```yaml
final_state:
  status: "VERIFIABLE"
  reasoning: "Refactor completed."
```

## Confidence

High.
"""


def test_h01_passes_with_screaming_architecture_approach(session):
    session_uuid, artifacts_dir = session
    content = _task_spec_with_practice(
        "screaming_architecture", "Group user-related code under app/users/."
    )
    write_artifact(artifacts_dir, session_uuid, "TASK_SPECIFICATION.md", content)
    returncode, output = run_runner(
        artifacts_dir,
        session_uuid,
        "H01",
        env_overrides={"AGENTS_FEATURE_SCREAMING_ARCHITECTURE": "true"},
    )

    assert returncode == 0
    assert output["result"] == "PASS"
    assert any(
        c["id"] == "screaming_architecture_flag_enabled" and c["result"] == "PASS"
        for c in output["checks"]
    )


def test_h05_passes_with_screaming_architecture_evidence(session):
    session_uuid, artifacts_dir = session
    spec = _task_spec_with_practice(
        "screaming_architecture", "Group user-related code under app/users/."
    )
    evidence = """  screaming_architecture:
    applied: true
    domain_modules:
      - name: "users"
        path: "app/users/"
        responsibility: "User registration and validation."
    framework_modules: []
    structural_changes: []
    rationale: "Domain grouping improves discoverability."
"""
    summary = _execution_summary_with_evidence(evidence)
    write_artifact(artifacts_dir, session_uuid, "TASK_SPECIFICATION.md", spec)
    write_artifact(artifacts_dir, session_uuid, "EXECUTION_SUMMARY.md", summary)
    returncode, output = run_runner(
        artifacts_dir,
        session_uuid,
        "H05",
        env_overrides={"AGENTS_FEATURE_SCREAMING_ARCHITECTURE": "true"},
    )

    assert returncode == 0
    assert output["result"] == "PASS"
    assert any(
        c["id"] == "screaming_architecture_evidence_present" and c["result"] == "PASS"
        for c in output["checks"]
    )


def test_h05_fails_missing_screaming_architecture_evidence(session):
    session_uuid, artifacts_dir = session
    spec = _task_spec_with_practice(
        "screaming_architecture", "Group user-related code under app/users/."
    )
    summary = _execution_summary_with_evidence(
        "  screaming_architecture:\n    applied: false\n    reason: " "\n"
    )
    write_artifact(artifacts_dir, session_uuid, "TASK_SPECIFICATION.md", spec)
    write_artifact(artifacts_dir, session_uuid, "EXECUTION_SUMMARY.md", summary)
    returncode, output = run_runner(
        artifacts_dir,
        session_uuid,
        "H05",
        env_overrides={"AGENTS_FEATURE_SCREAMING_ARCHITECTURE": "true"},
    )

    assert returncode == 1
    assert output["result"] == "FAIL"
    assert any(
        c["id"] == "screaming_architecture_not_applied_has_reason"
        and c["result"] == "FAIL"
        for c in output["checks"]
    )


def test_h01_passes_with_clean_architecture_approach(session):
    session_uuid, artifacts_dir = session
    content = _task_spec_with_practice(
        "clean_architecture",
        "Introduce UserRepository port and move business rules to use cases.",
    )
    write_artifact(artifacts_dir, session_uuid, "TASK_SPECIFICATION.md", content)
    returncode, output = run_runner(
        artifacts_dir,
        session_uuid,
        "H01",
        env_overrides={"AGENTS_FEATURE_CLEAN_ARCHITECTURE": "true"},
    )

    assert returncode == 0
    assert output["result"] == "PASS"
    assert any(
        c["id"] == "clean_architecture_flag_enabled" and c["result"] == "PASS"
        for c in output["checks"]
    )


def test_h05_passes_with_clean_architecture_evidence(session):
    session_uuid, artifacts_dir = session
    spec = _task_spec_with_practice(
        "clean_architecture",
        "Introduce UserRepository port and move business rules to use cases.",
    )
    evidence = """  clean_architecture:
    applied: true
    layers_touched:
      - layer: "use_cases"
        files:
          - "app/use_cases/register_user.py"
      - layer: "interface_adapters"
        files:
          - "app/adapters/user_repository.py"
      - layer: "frameworks_and_drivers"
        files:
          - "app/persistence/sqlalchemy_user_repository.py"
    dependency_rule_violations_found: []
    dependency_rule_violations_fixed: []
    abstractions_introduced:
      - name: "UserRepository"
        location: "app/adapters/user_repository.py"
        purpose: "Persistence port for user use cases."
    rationale: "Business rules no longer depend on SQLAlchemy."
"""
    summary = _execution_summary_with_evidence(evidence)
    write_artifact(artifacts_dir, session_uuid, "TASK_SPECIFICATION.md", spec)
    write_artifact(artifacts_dir, session_uuid, "EXECUTION_SUMMARY.md", summary)
    returncode, output = run_runner(
        artifacts_dir,
        session_uuid,
        "H05",
        env_overrides={"AGENTS_FEATURE_CLEAN_ARCHITECTURE": "true"},
    )

    assert returncode == 0
    assert output["result"] == "PASS"
    assert any(
        c["id"] == "clean_architecture_evidence_present" and c["result"] == "PASS"
        for c in output["checks"]
    )


def test_h05_fails_missing_clean_architecture_evidence(session):
    session_uuid, artifacts_dir = session
    spec = _task_spec_with_practice(
        "clean_architecture",
        "Introduce UserRepository port and move business rules to use cases.",
    )
    summary = _execution_summary_with_evidence(
        "  clean_architecture:\n    applied: false\n    reason: " "\n"
    )
    write_artifact(artifacts_dir, session_uuid, "TASK_SPECIFICATION.md", spec)
    write_artifact(artifacts_dir, session_uuid, "EXECUTION_SUMMARY.md", summary)
    returncode, output = run_runner(
        artifacts_dir,
        session_uuid,
        "H05",
        env_overrides={"AGENTS_FEATURE_CLEAN_ARCHITECTURE": "true"},
    )

    assert returncode == 1
    assert output["result"] == "FAIL"
    assert any(
        c["id"] == "clean_architecture_not_applied_has_reason" and c["result"] == "FAIL"
        for c in output["checks"]
    )


def test_h01_passes_with_dry_approach(session):
    session_uuid, artifacts_dir = session
    content = _task_spec_with_practice(
        "dry", "Consolidate duplicated email validation."
    )
    write_artifact(artifacts_dir, session_uuid, "TASK_SPECIFICATION.md", content)
    returncode, output = run_runner(
        artifacts_dir,
        session_uuid,
        "H01",
        env_overrides={"AGENTS_FEATURE_DRY": "true"},
    )

    assert returncode == 0
    assert output["result"] == "PASS"
    assert any(
        c["id"] == "dry_flag_enabled" and c["result"] == "PASS"
        for c in output["checks"]
    )


def test_h05_passes_with_dry_evidence(session):
    session_uuid, artifacts_dir = session
    spec = _task_spec_with_practice("dry", "Consolidate duplicated email validation.")
    evidence = """  dry:
    applied: true
    duplicates_found:
      - locations:
          - "app/services/user_service.py:42"
          - "app/services/admin_service.py:38"
        description: "Email validation regex duplicated."
        knowledge: "Valid email format"
        consolidation_strategy: "Extracted EmailValidator."
        lines_saved: 8
    duplicates_intentionally_kept: []
    rationale: "Single source of truth for email validation."
"""
    summary = _execution_summary_with_evidence(evidence)
    write_artifact(artifacts_dir, session_uuid, "TASK_SPECIFICATION.md", spec)
    write_artifact(artifacts_dir, session_uuid, "EXECUTION_SUMMARY.md", summary)
    returncode, output = run_runner(
        artifacts_dir,
        session_uuid,
        "H05",
        env_overrides={"AGENTS_FEATURE_DRY": "true"},
    )

    assert returncode == 0
    assert output["result"] == "PASS"
    assert any(
        c["id"] == "dry_evidence_present" and c["result"] == "PASS"
        for c in output["checks"]
    )


def test_h05_fails_missing_dry_evidence(session):
    session_uuid, artifacts_dir = session
    spec = _task_spec_with_practice("dry", "Consolidate duplicated email validation.")
    summary = _execution_summary_with_evidence(
        "  dry:\n    applied: false\n    reason: " "\n"
    )
    write_artifact(artifacts_dir, session_uuid, "TASK_SPECIFICATION.md", spec)
    write_artifact(artifacts_dir, session_uuid, "EXECUTION_SUMMARY.md", summary)
    returncode, output = run_runner(
        artifacts_dir,
        session_uuid,
        "H05",
        env_overrides={"AGENTS_FEATURE_DRY": "true"},
    )

    assert returncode == 1
    assert output["result"] == "FAIL"
    assert any(
        c["id"] == "dry_not_applied_has_reason" and c["result"] == "FAIL"
        for c in output["checks"]
    )


def test_h06_passes_with_dry_rubric(session):
    session_uuid, artifacts_dir = session
    spec = _task_spec_with_practice("dry", "Consolidate duplicated email validation.")
    report = """# Verification Report

## Metadata

```yaml
id: "test"
created_at: "2024-01-01T00:00:00Z"
status: "DONE"
```

## Task Reference

Reference.

## Execution Plan Reference

Reference.

## Verification Objective

Verify the fix.

## Acceptance Criteria Evaluation

```yaml
acceptance_criteria:
  - criterion: "The API shall reject empty names."
    result: "PASS"
    evidence: "Tested."
```

## Test Results

All tests pass.

## Issues Found

None.

## Final Decision

```yaml
decision:
  result: "COMPLETED"
  reasoning: "All criteria met."
```

## Confidence

High.

## State Transition

```yaml
transition:
  current_state: "VERIFYING"
  next_state: "COMPLETED"
```

## Rubric Evaluation

### TASK_SPECIFICATION_RUBRIC

- Objective clarity
  - Level: MEETS
  - Evidence: objective is specific

### CONTEXT_ARTIFACT_RUBRIC

- Relevance
  - Level: MEETS
  - Evidence: relevant

### CONTEXT_VALIDATION_REPORT_RUBRIC

- Decision clarity
  - Level: MEETS
  - Evidence: clear

### EXECUTION_PLAN_RUBRIC

- Approach alignment
  - Level: MEETS
  - Evidence: aligned

### EXECUTION_SUMMARY_RUBRIC

- Plan adherence
  - Level: MEETS
  - Evidence: followed

### VERIFICATION_REPORT_RUBRIC

- Criteria evaluation
  - Level: MEETS
  - Evidence: evaluated

### DRY_RUBRIC

- Duplication identified
  - Level: MEETS
  - Evidence: duplicated email validation found and consolidated
- Consolidation appropriate
  - Level: MEETS
  - Evidence: extracted shared validator without coupling unrelated modules
"""
    write_artifact(artifacts_dir, session_uuid, "TASK_SPECIFICATION.md", spec)
    write_artifact(artifacts_dir, session_uuid, "VERIFICATION_REPORT.md", report)
    returncode, output = run_runner(
        artifacts_dir,
        session_uuid,
        "H06",
        env_overrides={"AGENTS_FEATURE_DRY": "true", "AGENTS_FEATURE_RUBRICS": "true"},
    )

    assert returncode == 0
    assert output["result"] == "PASS"
    assert any(
        c["id"] == "rubric_evaluation_all_rubrics_present" and c["result"] == "PASS"
        for c in output["checks"]
    )


def test_h01_passes_with_layered_architecture_approach(session):
    session_uuid, artifacts_dir = session
    content = _task_spec_with_practice(
        "layered_architecture",
        "Move business rules from controllers to application services.",
    )
    write_artifact(artifacts_dir, session_uuid, "TASK_SPECIFICATION.md", content)
    returncode, output = run_runner(
        artifacts_dir,
        session_uuid,
        "H01",
        env_overrides={"AGENTS_FEATURE_LAYERED_ARCHITECTURE": "true"},
    )

    assert returncode == 0
    assert output["result"] == "PASS"
    assert any(
        c["id"] == "layered_architecture_flag_enabled" and c["result"] == "PASS"
        for c in output["checks"]
    )


def test_h05_passes_with_layered_architecture_evidence(session):
    session_uuid, artifacts_dir = session
    spec = _task_spec_with_practice(
        "layered_architecture",
        "Move business rules from controllers to application services.",
    )
    evidence = """  layered_architecture:
    applied: true
    layers:
      - name: "presentation"
        path: "app/web/"
        responsibility: "HTTP routes."
      - name: "application"
        path: "app/services/"
        responsibility: "Use cases."
      - name: "domain"
        path: "app/domain/"
        responsibility: "Business rules."
    changes:
      - description: "Moved validation from route to service."
        from_layer: "presentation"
        to_layer: "application"
        files_affected:
          - "app/web/user_routes.py"
          - "app/services/user_service.py"
    downward_dependency_violations_found: []
    downward_dependency_violations_fixed: []
    rationale: "Thinner controllers, reusable business logic."
"""
    summary = _execution_summary_with_evidence(evidence)
    write_artifact(artifacts_dir, session_uuid, "TASK_SPECIFICATION.md", spec)
    write_artifact(artifacts_dir, session_uuid, "EXECUTION_SUMMARY.md", summary)
    returncode, output = run_runner(
        artifacts_dir,
        session_uuid,
        "H05",
        env_overrides={"AGENTS_FEATURE_LAYERED_ARCHITECTURE": "true"},
    )

    assert returncode == 0
    assert output["result"] == "PASS"
    assert any(
        c["id"] == "layered_architecture_evidence_present" and c["result"] == "PASS"
        for c in output["checks"]
    )


def test_h05_fails_missing_layered_architecture_evidence(session):
    session_uuid, artifacts_dir = session
    spec = _task_spec_with_practice(
        "layered_architecture",
        "Move business rules from controllers to application services.",
    )
    summary = _execution_summary_with_evidence(
        '  layered_architecture:\n    applied: false\n    reason: ""\n'
    )
    write_artifact(artifacts_dir, session_uuid, "TASK_SPECIFICATION.md", spec)
    write_artifact(artifacts_dir, session_uuid, "EXECUTION_SUMMARY.md", summary)
    returncode, output = run_runner(
        artifacts_dir,
        session_uuid,
        "H05",
        env_overrides={"AGENTS_FEATURE_LAYERED_ARCHITECTURE": "true"},
    )

    assert returncode == 1
    assert output["result"] == "FAIL"
    assert any(
        c["id"] == "layered_architecture_not_applied_has_reason"
        and c["result"] == "FAIL"
        for c in output["checks"]
    )


def test_h01_passes_with_grasp_approach(session):
    session_uuid, artifacts_dir = session
    content = _task_spec_with_practice(
        "grasp", "Assign validation responsibility to the information expert."
    )
    write_artifact(artifacts_dir, session_uuid, "TASK_SPECIFICATION.md", content)
    returncode, output = run_runner(
        artifacts_dir,
        session_uuid,
        "H01",
        env_overrides={"AGENTS_FEATURE_GRASP": "true"},
    )

    assert returncode == 0
    assert output["result"] == "PASS"
    assert any(
        c["id"] == "grasp_flag_enabled" and c["result"] == "PASS"
        for c in output["checks"]
    )


def test_h05_passes_with_grasp_evidence(session):
    session_uuid, artifacts_dir = session
    spec = _task_spec_with_practice(
        "grasp", "Assign validation responsibility to the information expert."
    )
    evidence = """  grasp:
    applied: true
    patterns_applied:
      - pattern: "Information Expert"
        before: "UserService validated email format."
        after: "EmailValidator owns validation."
        files_affected:
          - "app/validators/email_validator.py"
          - "app/services/user_service.py"
    coupling_or_cohesion_issues_found:
      - description: "UserService mixed validation with orchestration."
        resolution: "Extracted EmailValidator."
    rationale: "Validation rule now lives with the class that owns it."
"""
    summary = _execution_summary_with_evidence(evidence)
    write_artifact(artifacts_dir, session_uuid, "TASK_SPECIFICATION.md", spec)
    write_artifact(artifacts_dir, session_uuid, "EXECUTION_SUMMARY.md", summary)
    returncode, output = run_runner(
        artifacts_dir,
        session_uuid,
        "H05",
        env_overrides={"AGENTS_FEATURE_GRASP": "true"},
    )

    assert returncode == 0
    assert output["result"] == "PASS"
    assert any(
        c["id"] == "grasp_evidence_present" and c["result"] == "PASS"
        for c in output["checks"]
    )


def test_h05_fails_missing_grasp_evidence(session):
    session_uuid, artifacts_dir = session
    spec = _task_spec_with_practice(
        "grasp", "Assign validation responsibility to the information expert."
    )
    summary = _execution_summary_with_evidence(
        '  grasp:\n    applied: false\n    reason: ""\n'
    )
    write_artifact(artifacts_dir, session_uuid, "TASK_SPECIFICATION.md", spec)
    write_artifact(artifacts_dir, session_uuid, "EXECUTION_SUMMARY.md", summary)
    returncode, output = run_runner(
        artifacts_dir,
        session_uuid,
        "H05",
        env_overrides={"AGENTS_FEATURE_GRASP": "true"},
    )

    assert returncode == 1
    assert output["result"] == "FAIL"
    assert any(
        c["id"] == "grasp_not_applied_has_reason" and c["result"] == "FAIL"
        for c in output["checks"]
    )


def test_h01_passes_with_ddd_tactical_approach(session):
    session_uuid, artifacts_dir = session
    content = _task_spec_with_practice(
        "ddd_tactical", "Model Invoice as an aggregate root with Money value object."
    )
    write_artifact(artifacts_dir, session_uuid, "TASK_SPECIFICATION.md", content)
    returncode, output = run_runner(
        artifacts_dir,
        session_uuid,
        "H01",
        env_overrides={"AGENTS_FEATURE_DDD_TACTICAL": "true"},
    )

    assert returncode == 0
    assert output["result"] == "PASS"
    assert any(
        c["id"] == "ddd_tactical_flag_enabled" and c["result"] == "PASS"
        for c in output["checks"]
    )


def test_h05_passes_with_ddd_tactical_evidence(session):
    session_uuid, artifacts_dir = session
    spec = _task_spec_with_practice(
        "ddd_tactical", "Model Invoice as an aggregate root with Money value object."
    )
    evidence = """  ddd_tactical:
    applied: true
    bounded_context: "billing"
    patterns_applied:
      - pattern: "Aggregate Root"
        name: "Invoice"
        location: "app/domain/invoice.py"
        invariant: "An invoice must have at least one line item."
      - pattern: "Value Object"
        name: "Money"
        location: "app/domain/money.py"
        invariant: "Currency is immutable."
      - pattern: "Domain Event"
        name: "InvoicePaid"
        location: "app/domain/events.py"
        purpose: "Notify other contexts."
    invariants_enforced:
      - "Invoice cannot be paid twice."
    anemic_models_refactored:
      - before: "app/models/invoice.py"
        after: "app/domain/invoice.py"
    rationale: "Replaced anemic model with rich domain aggregate."
"""
    summary = _execution_summary_with_evidence(evidence)
    write_artifact(artifacts_dir, session_uuid, "TASK_SPECIFICATION.md", spec)
    write_artifact(artifacts_dir, session_uuid, "EXECUTION_SUMMARY.md", summary)
    returncode, output = run_runner(
        artifacts_dir,
        session_uuid,
        "H05",
        env_overrides={"AGENTS_FEATURE_DDD_TACTICAL": "true"},
    )

    assert returncode == 0
    assert output["result"] == "PASS"
    assert any(
        c["id"] == "ddd_tactical_evidence_present" and c["result"] == "PASS"
        for c in output["checks"]
    )


def test_h05_fails_missing_ddd_tactical_evidence(session):
    session_uuid, artifacts_dir = session
    spec = _task_spec_with_practice(
        "ddd_tactical", "Model Invoice as an aggregate root with Money value object."
    )
    summary = _execution_summary_with_evidence(
        '  ddd_tactical:\n    applied: false\n    reason: ""\n'
    )
    write_artifact(artifacts_dir, session_uuid, "TASK_SPECIFICATION.md", spec)
    write_artifact(artifacts_dir, session_uuid, "EXECUTION_SUMMARY.md", summary)
    returncode, output = run_runner(
        artifacts_dir,
        session_uuid,
        "H05",
        env_overrides={"AGENTS_FEATURE_DDD_TACTICAL": "true"},
    )

    assert returncode == 1
    assert output["result"] == "FAIL"
    assert any(
        c["id"] == "ddd_tactical_not_applied_has_reason" and c["result"] == "FAIL"
        for c in output["checks"]
    )


def test_h01_passes_with_ddd_strategic_approach(session):
    session_uuid, artifacts_dir = session
    content = _task_spec_with_practice(
        "ddd_strategic", "Separate sales, billing, and shipping into bounded contexts."
    )
    write_artifact(artifacts_dir, session_uuid, "TASK_SPECIFICATION.md", content)
    returncode, output = run_runner(
        artifacts_dir,
        session_uuid,
        "H01",
        env_overrides={"AGENTS_FEATURE_DDD_STRATEGIC": "true"},
    )

    assert returncode == 0
    assert output["result"] == "PASS"
    assert any(
        c["id"] == "ddd_strategic_flag_enabled" and c["result"] == "PASS"
        for c in output["checks"]
    )


def test_h05_passes_with_ddd_strategic_evidence(session):
    session_uuid, artifacts_dir = session
    spec = _task_spec_with_practice(
        "ddd_strategic", "Separate sales, billing, and shipping into bounded contexts."
    )
    evidence = """  ddd_strategic:
    applied: true
    bounded_contexts:
      - name: "sales"
        responsibility: "Quotes and orders."
        files:
          - "app/sales/"
      - name: "billing"
        responsibility: "Invoices and payments."
        files:
          - "app/billing/"
    context_map_changes:
      - contexts:
          - "sales"
          - "billing"
        pattern: "Customer-Supplier"
        description: "Sales publishes OrderPlaced events."
    anti_corruption_layers_added:
      - context: "billing"
        adapter: "SalesEventAdapter"
        location: "app/billing/acl/sales_event_adapter.py"
    ubiquitous_language_terms_defined:
      - context: "sales"
        term: "Order"
        meaning: "Customer purchase request."
    rationale: "Avoided shared Order model across contexts."
"""
    summary = _execution_summary_with_evidence(evidence)
    write_artifact(artifacts_dir, session_uuid, "TASK_SPECIFICATION.md", spec)
    write_artifact(artifacts_dir, session_uuid, "EXECUTION_SUMMARY.md", summary)
    returncode, output = run_runner(
        artifacts_dir,
        session_uuid,
        "H05",
        env_overrides={"AGENTS_FEATURE_DDD_STRATEGIC": "true"},
    )

    assert returncode == 0
    assert output["result"] == "PASS"
    assert any(
        c["id"] == "ddd_strategic_evidence_present" and c["result"] == "PASS"
        for c in output["checks"]
    )


def test_h05_fails_missing_ddd_strategic_evidence(session):
    session_uuid, artifacts_dir = session
    spec = _task_spec_with_practice(
        "ddd_strategic", "Separate sales, billing, and shipping into bounded contexts."
    )
    summary = _execution_summary_with_evidence(
        '  ddd_strategic:\n    applied: false\n    reason: ""\n'
    )
    write_artifact(artifacts_dir, session_uuid, "TASK_SPECIFICATION.md", spec)
    write_artifact(artifacts_dir, session_uuid, "EXECUTION_SUMMARY.md", summary)
    returncode, output = run_runner(
        artifacts_dir,
        session_uuid,
        "H05",
        env_overrides={"AGENTS_FEATURE_DDD_STRATEGIC": "true"},
    )

    assert returncode == 1
    assert output["result"] == "FAIL"
    assert any(
        c["id"] == "ddd_strategic_not_applied_has_reason" and c["result"] == "FAIL"
        for c in output["checks"]
    )
