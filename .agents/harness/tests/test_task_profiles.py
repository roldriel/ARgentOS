"""Tests for the task profile model (trivial/standard/complex).

The profile assigned in TASK_ANALYSIS.md determines which harness gates are
mandatory. Gates a profile does not require are recorded in HARNESS_REPORT.md
as `skipped: profile`; escalation is upward-only, so reclassifying a session
to `standard` restores every gate.
"""

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


TASK_ANALYSIS_TEMPLATE = """# Task Analysis

## Metadata

```toml
id = "TA-001"
created_at = "2026-08-06T00:00:00Z"
status = "draft"
```

## User Request

```toml
original_request = "Rename a variable."
```

## Interpreted Objective

```toml
[objective]
description = "Rename a variable."
```

## Expected Outcome

```toml
[expected_outcome]
description = "The variable has the new name."
```

## Explicit Requirements

```toml
requirements = ["Rename the variable."]
```

## Explicit Restrictions

```toml
restrictions = ["Do not change behavior."]
```

## Detected Ambiguities

None.

## Intent Confidence Assessment

```toml
[intent_confidence]
level = "HIGH"
score = 8
applied_criteria = []
explanation = "Unambiguous request."
```

## Sufficiency Assessment

```toml
[sufficiency]
ready_for_specification = true
reasoning = "All information is available."
```

## Recommended Next State

```toml
recommended_next_state = "BUILDING_TASK_SPECIFICATION"
```

## Confidence

```toml
[confidence]
level = "HIGH"
explanation = "Straightforward analysis."
```

{profile_section}
"""

TRIVIAL_PROFILE_SECTION = """## Task Profile

```toml
[task_profile]
value = "trivial"
justification = "1 file estimated, no ambiguity, no design decisions, no interface impact."
```
"""

STANDARD_PROFILE_SECTION = """## Task Profile

```toml
[task_profile]
value = "standard"
justification = "More than 3 files estimated; the default cycle applies."
```
"""

INVALID_PROFILE_SECTION = """## Task Profile

```toml
[task_profile]
value = "whatever"
justification = "Not a valid profile value."
```
"""


def write_task_analysis(
    artifacts_dir: Path,
    session_uuid: str,
    profile_section: str,
    iteration: str = "00",
) -> Path:
    iter_dir = artifacts_dir / session_uuid / iteration
    iter_dir.mkdir(parents=True, exist_ok=True)
    path = iter_dir / "01-TASK_ANALYSIS.md"
    path.write_text(
        TASK_ANALYSIS_TEMPLATE.format(profile_section=profile_section),
        encoding="utf-8",
    )
    return path


def run_runner(
    artifacts_dir: Path,
    session_uuid: str,
    trigger: str,
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
    result = subprocess.run(
        cmd,
        cwd=PROJECT_ROOT,
        capture_output=True,
        text=True,
        env=os.environ.copy(),
    )
    try:
        output = json.loads(result.stdout) if result.stdout else {}
    except json.JSONDecodeError:
        output = {"error": "invalid JSON", "stdout": result.stdout, "stderr": result.stderr}
    return result.returncode, output


def read_report(artifacts_dir: Path, session_uuid: str) -> str:
    return (artifacts_dir / session_uuid / "HARNESS_REPORT.md").read_text(
        encoding="utf-8"
    )


def test_h00_passes_with_valid_task_profile(session):
    session_uuid, artifacts_dir = session
    write_task_analysis(artifacts_dir, session_uuid, TRIVIAL_PROFILE_SECTION)

    code, output = run_runner(artifacts_dir, session_uuid, "H00")

    assert code == 0
    assert output["result"] == "PASS"


def test_h00_fails_without_task_profile_section(session):
    session_uuid, artifacts_dir = session
    write_task_analysis(artifacts_dir, session_uuid, "")

    code, output = run_runner(artifacts_dir, session_uuid, "H00")

    assert code == 1
    assert output["result"] == "FAIL"
    profile_check = next(
        c for c in output["checks"] if c["id"] == "has_section_task_profile"
    )
    assert profile_check["result"] == "FAIL"


def test_trivial_profile_skips_non_mandatory_gate(session):
    session_uuid, artifacts_dir = session
    write_task_analysis(artifacts_dir, session_uuid, TRIVIAL_PROFILE_SECTION)

    # H01 (task specification) is not mandatory for the trivial profile; the
    # artifact is absent, yet the gate must not fail.
    code, output = run_runner(artifacts_dir, session_uuid, "H01")

    assert code == 0
    assert output["result"] == "SKIP"
    assert output["checks"] == [
        {
            "id": "gate_required_for_profile",
            "result": "SKIP",
            "evidence": (
                "skipped: profile — gate 'H01' is not required for task "
                "profile 'trivial'"
            ),
        }
    ]

    report = read_report(artifacts_dir, session_uuid)
    assert "skipped: profile" in report
    assert "| H01 |" in report and "| SKIP |" in report


def test_trivial_profile_still_enforces_mandatory_gates(session):
    session_uuid, artifacts_dir = session
    write_task_analysis(artifacts_dir, session_uuid, TRIVIAL_PROFILE_SECTION)

    # H04 (execution plan) is mandatory for every profile; without
    # EXECUTION_PLAN.md it fails.
    code, output = run_runner(artifacts_dir, session_uuid, "H04")

    assert code == 1
    assert output["result"] == "FAIL"
    assert output["checks"][0]["id"] == "artifact_exists"
    assert output["checks"][0]["result"] == "FAIL"


def test_standard_profile_requires_full_cycle(session):
    session_uuid, artifacts_dir = session
    write_task_analysis(artifacts_dir, session_uuid, STANDARD_PROFILE_SECTION)

    code, output = run_runner(artifacts_dir, session_uuid, "H01")

    assert code == 1
    assert output["result"] == "FAIL"
    assert output["checks"][0]["id"] == "artifact_exists"


def test_missing_profile_defaults_to_standard(session):
    session_uuid, artifacts_dir = session
    write_task_analysis(artifacts_dir, session_uuid, "")

    code, output = run_runner(artifacts_dir, session_uuid, "H01")

    assert code == 1
    assert output["result"] == "FAIL"


def test_invalid_profile_value_defaults_to_standard(session):
    session_uuid, artifacts_dir = session
    write_task_analysis(artifacts_dir, session_uuid, INVALID_PROFILE_SECTION)

    code, output = run_runner(artifacts_dir, session_uuid, "H01")

    assert code == 1
    assert output["result"] == "FAIL"


def test_upward_reclassification_restores_skipped_gates(session):
    session_uuid, artifacts_dir = session
    write_task_analysis(artifacts_dir, session_uuid, TRIVIAL_PROFILE_SECTION)

    code, output = run_runner(artifacts_dir, session_uuid, "H01")
    assert code == 0
    assert output["result"] == "SKIP"

    # Escalation is upward-only: once the Orchestrator reclassifies the task
    # as standard, the previously skipped gate validates again and forces the
    # missing artifact.
    write_task_analysis(artifacts_dir, session_uuid, STANDARD_PROFILE_SECTION)

    code, output = run_runner(artifacts_dir, session_uuid, "H01")
    assert code == 1
    assert output["result"] == "FAIL"
    assert output["checks"][0]["id"] == "artifact_exists"


def test_skipped_gates_are_not_counted_as_failures_in_metrics(session):
    session_uuid, artifacts_dir = session
    write_task_analysis(artifacts_dir, session_uuid, TRIVIAL_PROFILE_SECTION)

    run_runner(artifacts_dir, session_uuid, "H01")

    report = read_report(artifacts_dir, session_uuid)
    metrics_section = report.split("## Metrics", 1)[1]
    h01_row = next(
        line for line in metrics_section.splitlines() if line.startswith("| H01 |")
    )
    # Invocations=1, PASS=0, FAIL=0: a skipped gate is not a failure.
    assert h01_row.split("|")[2].strip() == "1"
    assert h01_row.split("|")[3].strip() == "0"
    assert h01_row.split("|")[4].strip() == "0"
