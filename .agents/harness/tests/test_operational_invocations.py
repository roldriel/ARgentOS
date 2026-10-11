"""GATE 2 remediation F2: the documented invocations must work in the adopted layout.

The payload documents how the Orchestrator/System Agent run the harness. This
suite runs those documented commands from ``PROJECT_ROOT`` in a scratch adopted
project (``.argentos/.agents/harness/``) and guards that no payload document
reintroduces the old command form or omits the project root.
"""

from __future__ import annotations

import json
import re
import shutil
import subprocess
import sys
import uuid
from pathlib import Path

import pytest

HARNESS = Path(__file__).resolve().parents[1]
PAYLOAD = HARNESS.parent
SCRIPTS = (
    "runner_state.py",
    "hook_gate.py",
    "gate_validator.py",
    "health_check.py",
    "roots.py",
)

H01_WITH_CITATIONS = """# Artifact

## Objective
Build X.

## Expected Outcome
X works.

## Scope
X.

## Constraints
None.

## Acceptance Criteria
- The API shall return HTTP 200.

## Assumptions
- none

## Unknowns
- none

## Validation
```toml
[refs]
specification = ".agents/standards/X.md"
artifact = "src/app.py"
```
"""


@pytest.fixture()
def adopted(tmp_path: Path) -> Path:
    """A scratch adopted project with the harness installed in the payload root."""
    harness = tmp_path / ".argentos" / ".agents" / "harness"
    harness.mkdir(parents=True)
    for name in SCRIPTS:
        shutil.copy(HARNESS / name, harness / name)
    (tmp_path / ".argentos" / ".project").mkdir(parents=True)
    return tmp_path


def run_script(project: Path, script: str, *args: str) -> subprocess.CompletedProcess:
    """Run a harness script through the documented relative path, from the root."""
    return subprocess.run(
        [
            sys.executable,
            str(project / ".argentos/.agents/harness" / script),
            *args,
        ],
        capture_output=True,
        text=True,
        cwd=project,
    )


def run_hook(project: Path, event: dict) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, str(project / ".argentos/.agents/harness/hook_gate.py")],
        input=json.dumps(event),
        capture_output=True,
        text=True,
        cwd=project,
    )


def test_health_check_documented_invocation(adopted: Path):
    result = run_script(
        adopted, "health_check.py", "--project-root", str(adopted)
    )

    assert result.returncode == 0, result.stdout + result.stderr
    assert json.loads(result.stdout)["result"] == "PASS"


def test_runner_state_documented_invocation(adopted: Path):
    session = str(uuid.uuid4())
    (adopted / ".argentos" / ".project" / session / "00").mkdir(parents=True)

    result = run_script(
        adopted,
        "runner_state.py",
        "--project-root",
        str(adopted),
        "--session",
        session,
        "--trigger",
        "H04",
        "pass",
    )

    assert result.returncode == 0, result.stdout + result.stderr
    state = adopted / ".argentos" / ".project" / session / "00" / "state.json"
    assert state.is_file()


def test_gate_validator_documented_invocation_resolves_citations(adopted: Path):
    iteration = (
        adopted / ".argentos" / ".project" / str(uuid.uuid4()) / "00"
    )
    iteration.mkdir(parents=True)
    standard = adopted / ".argentos" / ".agents" / "standards" / "X.md"
    standard.parent.mkdir(parents=True)
    standard.write_text("# Section\n\ncontent\n", encoding="utf-8")
    (adopted / "src").mkdir()
    (adopted / "src" / "app.py").write_text("x = 1\n", encoding="utf-8")
    artifact = iteration / "TASK_SPECIFICATION.md"
    artifact.write_text(H01_WITH_CITATIONS, encoding="utf-8")

    result = run_script(
        adopted,
        "gate_validator.py",
        "--project-root",
        str(adopted),
        "--trigger",
        "H01",
        "--artifact",
        str(artifact),
    )

    assert result.returncode == 0, result.stdout + result.stderr
    checks = json.loads(result.stdout)["checks"]
    assert any(
        check["id"] == "citations" and check["result"] == "PASS"
        for check in checks
    )


def test_hook_documented_command_uses_the_event_context(adopted: Path):
    event = {
        "session_id": "cli-session",
        "cwd": str(adopted),
        "hook_event_name": "PreToolUse",
        "tool_name": "Write",
        "tool_input": {"file_path": str(adopted / "src" / "app.py")},
    }
    assert run_hook(adopted, event).returncode == 2

    event["tool_input"]["file_path"] = str(
        adopted / ".argentos" / "features.toml"
    )
    assert run_hook(adopted, event).returncode == 0


def test_no_payload_document_uses_the_old_command_form():
    """F2 guard — commands must use `.argentos/.agents/harness/...`."""
    offenders = []
    for path in sorted(PAYLOAD.rglob("*.md")):
        text = path.read_text(encoding="utf-8")
        if re.search(r"python\s+\.agents/harness/", text):
            offenders.append(str(path.relative_to(PAYLOAD)))
    assert offenders == []


def test_documented_harness_cli_calls_pass_project_root():
    """F2 guard — the documented CLI commands must declare the project root."""
    offenders = []
    for path in sorted(PAYLOAD.rglob("*.md")):
        for number, line in enumerate(
            path.read_text(encoding="utf-8").splitlines(), 1
        ):
            for script in (
                "health_check.py",
                "runner_state.py",
                "gate_validator.py",
            ):
                marker = f"python .argentos/.agents/harness/{script}"
                if marker not in line or "--project-root" in line:
                    continue
                # The H15 schema-support actions do not need a project root.
                if "validate-delegation" in line or "validate-return" in line:
                    continue
                offenders.append(f"{path.relative_to(PAYLOAD)}:{number}")
    assert offenders == []
