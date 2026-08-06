"""Gate-level tests for the mechanical semantic checks (citation resolution
and test evidence) and unit tests for the extraction logic."""

from __future__ import annotations

import sys
import uuid
from pathlib import Path

import pytest

_harness_dir = Path(__file__).resolve().parents[1]
if str(_harness_dir) not in sys.path:
    sys.path.insert(0, str(_harness_dir))

import runner_citations
from test_harness_runner import run_runner, write_artifact


@pytest.fixture
def session(tmp_path):
    """Create a temporary agent session directory outside the real .project/."""
    session_uuid = f"test-{uuid.uuid4()}"
    artifacts_dir = tmp_path / ".project"
    session_dir = artifacts_dir / session_uuid
    session_dir.mkdir(parents=True, exist_ok=True)
    yield session_uuid, artifacts_dir


RUBRIC_SECTION = """
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


def verification_report(test_results: str, extra_prose: str = "") -> str:
    """A VERIFICATION_REPORT that passes H06 except for the given variations."""
    return f"""# Verification Report

## Metadata

```toml
id = "test"
created_at = "2024-01-01T00:00:00Z"
status = "DONE"
```

## Task Reference

Reference.

## Execution Plan Reference

Reference.

## Verification Objective

Verify the fix.

## Acceptance Criteria Evaluation

```toml
[[acceptance_criteria]]
criterion = "The API shall reject empty names."
result = "PASS"
evidence = "Tested."
```

## Test Results

{test_results}

## Issues Found

None.

## Final Decision

```toml
[decision]
result = "COMPLETED"
reasoning = "All criteria met."
```

## Confidence

High.

## State Transition

```toml
[transition]
current_state = "VERIFYING"
next_state = "COMPLETED"
```
{extra_prose}{RUBRIC_SECTION}"""


COMMAND = "python -m pytest tools/tests/ -q"

NO_EVIDENCE_RESULTS = f"""```toml
[[test_results]]
test = "{COMMAND}"
result = "PASS"
details = "19 passed."
```"""

EVIDENCE_FILE_RESULTS = f"""```toml
[[test_results]]
test = "{COMMAND}"
result = "PASS"
details = "19 passed."
evidence = "pytest-results.txt"
```"""


def test_h06_fails_when_test_command_has_no_evidence(session):
    session_uuid, artifacts_dir = session
    write_artifact(
        artifacts_dir, session_uuid, "VERIFICATION_REPORT.md",
        verification_report(NO_EVIDENCE_RESULTS),
    )
    returncode, output = run_runner(artifacts_dir, session_uuid, "H06")

    assert returncode == 1
    assert output["result"] == "FAIL"
    failing = [c for c in output["checks"] if c["id"] == "test_evidence_present"]
    assert failing and failing[0]["result"] == "FAIL"
    assert COMMAND in failing[0]["evidence"]


def test_h06_passes_with_test_evidence_in_session_log(session):
    session_uuid, artifacts_dir = session
    log = artifacts_dir / session_uuid / "SESSION_LOG.md"
    log.write_text(
        f"# Session Log\n\n## 2024-01-01T00:00:00Z\n\n- Ran `{COMMAND}`: 19 passed.\n",
        encoding="utf-8",
    )
    write_artifact(
        artifacts_dir, session_uuid, "VERIFICATION_REPORT.md",
        verification_report(NO_EVIDENCE_RESULTS),
    )
    returncode, output = run_runner(artifacts_dir, session_uuid, "H06")

    assert returncode == 0
    assert output["result"] == "PASS"
    assert any(
        c["id"] == "test_evidence_1_present" and c["result"] == "PASS"
        for c in output["checks"]
    )


def test_h06_passes_with_test_evidence_file(session):
    session_uuid, artifacts_dir = session
    (artifacts_dir / session_uuid / "pytest-results.txt").write_text(
        "19 passed in 0.35s\n", encoding="utf-8"
    )
    write_artifact(
        artifacts_dir, session_uuid, "VERIFICATION_REPORT.md",
        verification_report(EVIDENCE_FILE_RESULTS),
    )
    returncode, output = run_runner(artifacts_dir, session_uuid, "H06")

    assert returncode == 0
    assert output["result"] == "PASS"


def test_h06_fails_with_phantom_citation_path(session):
    session_uuid, artifacts_dir = session
    prose = "\nVerified against `plans/definitely-not-a-real-file.md:Objetivo`.\n"
    write_artifact(
        artifacts_dir, session_uuid, "VERIFICATION_REPORT.md",
        verification_report("All tests pass.", extra_prose=prose),
    )
    returncode, output = run_runner(artifacts_dir, session_uuid, "H06")

    assert returncode == 1
    assert output["result"] == "FAIL"
    citation_checks = [c for c in output["checks"] if c["id"] == "citations_resolve"]
    assert citation_checks and citation_checks[0]["result"] == "FAIL"
    assert "plans/definitely-not-a-real-file.md" in citation_checks[0]["evidence"]


def test_h06_passes_with_resolvable_citation(session):
    session_uuid, artifacts_dir = session
    prose = "\nVerified against `plans/27-harness-coverage-closure.md:Objetivo`.\n"
    write_artifact(
        artifacts_dir, session_uuid, "VERIFICATION_REPORT.md",
        verification_report("All tests pass.", extra_prose=prose),
    )
    returncode, output = run_runner(artifacts_dir, session_uuid, "H06")

    assert returncode == 0
    assert output["result"] == "PASS"
    assert any(
        c["id"] == "citations_resolve" and c["result"] == "PASS"
        for c in output["checks"]
    )


def test_h02_fails_with_phantom_citation_path(session):
    session_uuid, artifacts_dir = session
    content = """# Context Artifact

## Relevant Files

See `src/phantom-module.py:handle_request` for the handler.
"""
    write_artifact(artifacts_dir, session_uuid, "CONTEXT_ARTIFACT.md", content)
    returncode, output = run_runner(artifacts_dir, session_uuid, "H02")

    assert returncode == 1
    assert output["result"] == "FAIL"
    citation_checks = [c for c in output["checks"] if c["id"] == "citations_resolve"]
    assert citation_checks and citation_checks[0]["result"] == "FAIL"
    assert "src/phantom-module.py" in citation_checks[0]["evidence"]


# --- Unit tests for the extraction/verification logic -----------------------


def test_extract_skips_placeholder_paths():
    text = "See `.project/<session-uuid>/00/04-TASK_SPECIFICATION.md:Metadata`."
    assert runner_citations.extract_citations(text) == []


def test_extract_toml_citation_fields():
    text = """```toml
[task_reference]
specification = ".project/abc/00/04-TASK_SPECIFICATION.md"

[plan_reference]
execution_plan = ""
```
"""
    citations = runner_citations.extract_citations(text)
    assert [c.path for c in citations] == [
        ".project/abc/00/04-TASK_SPECIFICATION.md"
    ]
    assert citations[0].section == ""


def test_numeric_anchor_requires_file_existence_only(tmp_path):
    citation = runner_citations.Citation(1, "foo.py", "102")
    target = tmp_path / "foo.py"
    target.write_text("def handle():\n    pass\n", encoding="utf-8")
    assert runner_citations.verify_citation(citation, [tmp_path]) is None
    broken = runner_citations.verify_citation(
        runner_citations.Citation(1, "nope.py", "102"), [tmp_path]
    )
    assert broken is not None and broken.reason == "file not found"


def test_section_anchor_verified_for_markdown(tmp_path):
    target = tmp_path / "doc.md"
    target.write_text("# Title\n\n## Objetivo\n\nText.\n", encoding="utf-8")
    assert (
        runner_citations.verify_citation(
            runner_citations.Citation(1, "doc.md", "Objetivo"), [tmp_path]
        )
        is None
    )
    broken = runner_citations.verify_citation(
        runner_citations.Citation(1, "doc.md", "Missing"), [tmp_path]
    )
    assert broken is not None and broken.reason == "section not found"
