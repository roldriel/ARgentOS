"""Offline tests for the experimental DEV Memory agent executor (tools/).

The executor is experimental infrastructure for the controlled DEV Memory test:
it adapts a local DeepSeek Harness ``headless`` run to the JSONL interface that
``tools/dev_memory_controlled_runner.py`` expects. These tests never invoke the
model, the network or the ``dsh`` CLI -- process execution is replaced with
synthetic run events -- so they are deterministic and portable.
"""

from __future__ import annotations

import io
import json
import os
import subprocess
import sys
import time
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[1]

import dev_memory_agent_executor as executor  # noqa: E402
import testsupport  # noqa: E402


def _write(path: Path, text: str) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")
    return path


def _valid_key() -> dict:
    return {
        "meta": {"method": "test"},
        "questions": {
            f"Q{i:02d}": {
                "question": f"question {i}",
                "expected_conclusion": f"conclusion {i}",
                "expected_scope": f"scope {i}",
                "supporting_sources": ["REFACTOR_CREWAI.md"],
            }
            for i in range(1, 13)
        },
    }


# ---------------------------------------------------------------------------
# Packaging / CLI contract
# ---------------------------------------------------------------------------


def test_executor_imports_only_stdlib() -> None:
    testsupport.assert_tool_imports_only_stdlib(REPO_ROOT / "tools" / "dev_memory_agent_executor.py")


def test_self_check_cli_reports_missing_configuration(tmp_path: Path) -> None:
    env = os.environ.copy()
    for variable in (
        "DEEPSEEK_API_KEY",
        "ARGENTOS_DSH_CLI",
        "DSH_CLI_PATH",
        "ARGENTOS_EXPECTED_KEY",
        "ARGENTOS_EVIDENCE_DIR",
    ):
        env.pop(variable, None)
    proc = subprocess.run(
        [sys.executable, str(REPO_ROOT / "tools" / "dev_memory_agent_executor.py"), "--self-check"],
        capture_output=True,
        text=True,
        env=env,
        cwd=str(tmp_path),
        timeout=120,
    )
    assert proc.returncode == 2
    payload = json.loads(proc.stdout)
    assert payload["executor"] == "tools/dev_memory_agent_executor.py"
    problems = " ".join(payload["problems"])
    assert "DEEPSEEK_API_KEY" in problems
    assert "expected key" in problems
    assert "ARGENTOS_EVIDENCE_DIR" in problems


def test_self_check_cli_rejects_unknown_arguments(tmp_path: Path) -> None:
    proc = subprocess.run(
        [sys.executable, str(REPO_ROOT / "tools" / "dev_memory_agent_executor.py"), "--bogus"],
        capture_output=True,
        text=True,
        cwd=str(tmp_path),
        timeout=120,
    )
    assert proc.returncode == 2
    assert "usage" in proc.stderr.lower()


# ---------------------------------------------------------------------------
# Event parsing and instrumentation mapping
# ---------------------------------------------------------------------------


def test_parse_ndjson_ignores_noise() -> None:
    text = "\n".join(
        [
            '{"type": "session", "sessionId": "s1"}',
            "not json",
            "",
            "[1, 2, 3]",
            '{"type": "final", "text": "done"}',
        ]
    )
    events = executor.parse_ndjson(text)
    assert [event["type"] for event in events] == ["session", "final"]


def test_summarize_usage_sums_step_end_events() -> None:
    events = [
        {"type": "status", "phase": "step_end", "usage": {"inputTokens": 10, "outputTokens": 2}},
        {"type": "status", "phase": "step_start"},
        {"type": "status", "phase": "step_end", "usage": {"inputTokens": 5, "outputTokens": 3}},
    ]
    assert executor.summarize_usage(events) == {"inputTokens": 15, "outputTokens": 5}


def test_map_instrumentation_read_search_and_rehydration(tmp_path: Path) -> None:
    workspace = tmp_path / "repo"
    _write(workspace / "REFACTOR_CREWAI.md", "# study\n")
    _write(workspace / "docs" / "note.md", "# note\n")
    _write(workspace / "DEV_MEMORY_PILOT.md", "# memory\n")
    events = [
        {"type": "tool_call", "tool": "read", "input": {"file_path": "REFACTOR_CREWAI.md"}},
        {"type": "tool_call", "tool": "grep", "input": {"pattern": "checkpoint", "path": "."}},
        {"type": "tool_call", "tool": "glob", "input": {"pattern": "**/*.md"}},
        {"type": "tool_call", "tool": "read", "input": {"file_path": "DEV_MEMORY_PILOT.md"}},
        {"type": "tool_call", "tool": "read", "input": {"file_path": str(workspace / "docs" / "note.md")}},
    ]
    inst = executor.map_instrumentation(events, workspace)

    assert inst.file_open_events == ["REFACTOR_CREWAI.md", "DEV_MEMORY_PILOT.md", "docs/note.md"]
    assert inst.search_events == ["checkpoint", "**/*.md"]
    assert inst.rehydration_events == ["REFACTOR_CREWAI.md"]
    assert inst.opened == ["REFACTOR_CREWAI.md", "DEV_MEMORY_PILOT.md", "docs/note.md"]
    assert inst.observed_tools == {"read", "grep", "glob"}


def test_map_instrumentation_records_shell_calls_as_observed(tmp_path: Path) -> None:
    workspace = tmp_path / "repo"
    _write(workspace / "REFACTOR_LETTA.md", "# study\n")
    events = [
        {"type": "tool_call", "tool": "pwsh", "input": {"command": 'Get-Content "REFACTOR_LETTA.md"'}},
        {
            "type": "tool_call",
            "tool": "pwsh",
            "input": {"command": "Get-ChildItem -Recurse | Select-String -Pattern 'memory'"},
        },
    ]
    inst = executor.map_instrumentation(events, workspace)

    assert inst.observed_tools == {"pwsh"}
    assert len(inst.file_open_events) == 1
    assert len(inst.search_events) == 1
    assert "REFACTOR_LETTA.md" in inst.opened


def test_map_instrumentation_ignores_failed_reads_and_maps_read_image(tmp_path: Path) -> None:
    workspace = tmp_path / "repo"
    _write(workspace / "REFACTOR_CREWAI.md", "# study\n")
    events = [
        {
            "type": "tool_call",
            "callId": "c1",
            "tool": "read",
            "input": {"file_path": "missing.md"},
        },
        {"type": "tool_result", "callId": "c1", "status": "error", "result": "not found"},
        {
            "type": "tool_call",
            "callId": "c2",
            "tool": "read_image",
            "input": {"file_path": "REFACTOR_CREWAI.md"},
        },
        {"type": "tool_result", "callId": "c2", "status": "completed", "result": "..."},
    ]
    inst = executor.map_instrumentation(events, workspace)
    assert inst.file_open_events == ["REFACTOR_CREWAI.md"]
    assert inst.failed_reads == ["missing.md"]
    assert inst.opened == ["REFACTOR_CREWAI.md"]


def test_map_instrumentation_ignores_failed_shell_attempts(tmp_path: Path) -> None:
    workspace = tmp_path / "repo"
    _write(workspace / "REFACTOR_LETTA.md", "# study\n")
    events = [
        {"type": "tool_call", "callId": "c0", "tool": "bash", "input": {"command": "ls"}},
        {"type": "tool_result", "callId": "c0", "status": "error", "result": 'Error: unknown tool "bash"'},
    ]
    inst = executor.map_instrumentation(events, workspace)
    assert inst.shell_commands == ["ls"]
    assert inst.search_events == []
    assert inst.file_open_events == []


def test_summarize_tool_calls_keeps_status_and_relative_paths(tmp_path: Path) -> None:
    workspace = tmp_path / "repo"
    _write(workspace / "REFACTOR_OPENHANDS.md", "# study\n")
    events = [
        {
            "type": "tool_call",
            "callId": "c1",
            "tool": "read",
            "input": {"file_path": str(workspace / "REFACTOR_OPENHANDS.md")},
        },
        {"type": "tool_result", "callId": "c1", "status": "completed", "result": "..."},
    ]
    calls = executor.summarize_tool_calls(events, workspace)
    assert calls == [{"tool": "read", "path": "REFACTOR_OPENHANDS.md", "status": "completed"}]


# ---------------------------------------------------------------------------
# Deterministic provenance
# ---------------------------------------------------------------------------


def test_extract_citations_resolves_root_and_nested_paths(tmp_path: Path) -> None:
    workspace = tmp_path / "repo"
    _write(workspace / "REFACTOR_CREWAI.md", "# study\n")
    _write(workspace / "docs" / "plans" / "180-study.md", "# plan\n")
    answer = (
        "CONCLUSION: yes.\nEVIDENCE: `REFACTOR_CREWAI.md` and "
        "docs/plans/180-study.md support this; also mention REFACTOR_MATRIX.md."
    )
    cited = executor.extract_citations(
        answer, workspace, ["REFACTOR_CREWAI.md", "docs/plans/180-study.md"]
    )
    assert "REFACTOR_CREWAI.md" in cited
    assert "docs/plans/180-study.md" in cited
    assert "REFACTOR_MATRIX.md" not in cited


def test_provenance_requires_cited_source_actually_opened(tmp_path: Path) -> None:
    workspace = tmp_path / "repo"
    _write(workspace / "REFACTOR_ADK.md", "# study\n")
    answer = "CONCLUSION: x.\nEVIDENCE: REFACTOR_ADK.md"

    present, cited, supported = executor.compute_provenance(answer, workspace, ["REFACTOR_ADK.md"])
    assert present is True
    assert cited == ["REFACTOR_ADK.md"]
    assert supported == ["REFACTOR_ADK.md"]

    present_not_opened, _, supported_not_opened = executor.compute_provenance(answer, workspace, [])
    assert present_not_opened is False
    assert supported_not_opened == []


def test_provenance_rejects_the_derived_memory_surface(tmp_path: Path) -> None:
    workspace = tmp_path / "repo"
    _write(workspace / "DEV_MEMORY_PILOT.md", "# memory\n")
    answer = "EVIDENCE: DEV_MEMORY_PILOT.md (DEV-MEM-001)"
    present, cited, supported = executor.compute_provenance(
        answer, workspace, ["DEV_MEMORY_PILOT.md"]
    )
    assert present is False
    assert "DEV_MEMORY_PILOT.md" in cited and supported == []


def test_provenance_unknown_without_answer(tmp_path: Path) -> None:
    present, cited, supported = executor.compute_provenance(None, tmp_path, [])
    assert present is None and cited == [] and supported == []


# ---------------------------------------------------------------------------
# Expected-answer key and fixed evidence pack
# ---------------------------------------------------------------------------


def test_validate_expected_key_accepts_a_complete_key() -> None:
    assert executor.validate_expected_key(_valid_key()) == []


def test_validate_expected_key_reports_missing_entries_and_fields() -> None:
    key = _valid_key()
    del key["questions"]["Q07"]
    key["questions"]["Q08"]["expected_scope"] = ""
    problems = executor.validate_expected_key(key)
    assert any("Q07: missing" in problem for problem in problems)
    assert any("Q08: expected_scope" in problem for problem in problems)


def test_build_fixed_evidence_unions_family_key_and_governance(tmp_path: Path) -> None:
    evidence_dir = tmp_path / "groundtruth"
    for rel in (
        "REFACTOR_CREWAI.md",
        "REFACTOR_SYNTHESIS.md",
        "REFACTOR_MATRIX.md",
        "REFACTOR_OPENHANDS.md",
        "REFACTOR_LETTA.md",
        "DEV_MEMORY_PILOT.md",
        "docs/plans/INDEX.md",
        "docs/plans/180-comparative-architecture-refactor-study.md",
        "docs/rfc/75-change-lifecycle.md",
        "docs/adr/15-change-lifecycle-continuity.md",
        "docs/adr/16-change-lifecycle-authority.md",
        "protocol/.agents/standards/context/MEMORY_SYSTEM.md",
    ):
        _write(evidence_dir / rel, f"# {rel}\nbody of {rel}\n")
    entry = {"supporting_sources": ["REFACTOR_CREWAI.md", "REFACTOR_MISSING.md"]}
    text, included, missing = executor.build_fixed_evidence(entry, evidence_dir, "Q11")

    # Q11's frozen evidence family contributes the synthesis and the matrix.
    assert "REFACTOR_CREWAI.md" in included
    assert "REFACTOR_SYNTHESIS.md" in included
    assert "REFACTOR_MATRIX.md" in included
    assert "docs/plans/180-comparative-architecture-refactor-study.md" in included
    # Derived indexes, entry points and the memory surface are never evidence.
    assert "DEV_MEMORY_PILOT.md" not in included
    assert "docs/plans/INDEX.md" not in included
    assert "REFACTOR_MISSING.md" in missing
    assert "body of REFACTOR_SYNTHESIS.md" in text


# ---------------------------------------------------------------------------
# Grader parsing, prompts and calibration
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    "text",
    [
        '{"correct_conclusion": true, "correct_scope": false, '
        '"authority_boundary_preserved": true, "unsupported_claim": false, "rationale": "r"}',
        '```json\n{"correct_conclusion": true}\n```',
        'Here is the result:\n{"correct_conclusion": true}\nThanks.',
    ],
)
def test_parse_grader_json_accepts_plain_fenced_and_embedded_objects(text: str) -> None:
    parsed = executor.parse_grader_json(text)
    assert parsed is not None
    assert parsed["correct_conclusion"] is True


def test_parse_grader_json_rejects_non_json() -> None:
    assert executor.parse_grader_json("I cannot grade this.") is None
    assert executor.parse_grader_json("") is None


def test_coerce_bool_only_accepts_real_booleans() -> None:
    assert executor.coerce_bool(True) is True
    assert executor.coerce_bool(False) is False
    assert executor.coerce_bool("true") is None
    assert executor.coerce_bool(1) is None
    assert executor.coerce_bool(None) is None


def test_gradable_fields_leave_unknown_values_unknown() -> None:
    fields = executor.gradable_fields({"correct_conclusion": True, "correct_scope": "yes"})
    assert fields == {
        "correct_conclusion": True,
        "correct_scope": None,
        "authority_boundary_preserved": None,
        "unsupported_claim": None,
    }
    assert all(value is None for value in executor.gradable_fields(None).values())


def test_task_prompt_is_condition_blind() -> None:
    prompt = executor.build_task_prompt("Is two-tier retrieval plausible?")
    lowered = prompt.lower()
    assert "two-tier retrieval" in prompt
    for forbidden in ("control", "treatment", "dev_memory_pilot", "memory surface", "experiment"):
        assert forbidden not in lowered


def test_grader_prompt_is_condition_blind_and_has_fixed_evidence() -> None:
    key = {"expected_conclusion": "k", "expected_scope": "s"}
    prompt = executor.build_grader_prompt(
        "Q?", key, "CONCLUSION: answer", "--- REFACTOR_CREWAI.md ---\ncontent"
    )
    assert json.dumps(key, ensure_ascii=False, indent=2) in prompt
    assert "CONCLUSION: answer" in prompt
    assert "FIXED EVIDENCE PACK" in prompt
    assert "--- REFACTOR_CREWAI.md ---" in prompt
    for forbidden in ("control", "treatment", "DEV_MEMORY_PILOT.md"):
        assert forbidden.lower() not in prompt.lower()


def test_calibration_verdict_flags_a_broken_grader() -> None:
    broken = {
        "key_consistent": {"parsed": {"correct_conclusion": False, "correct_scope": False}},
        "overgeneralized": {"parsed": {"correct_scope": True, "unsupported_claim": False}},
        "memory_as_authority": {"parsed": {"authority_boundary_preserved": True}},
        "uncited": {"parsed": {"unsupported_claim": False, "correct_conclusion": True}},
    }
    flags = executor.calibration_verdict(broken)
    assert "grader did not accept the key-consistent answer" in flags
    assert "grader did not penalize the over-generalized answer" in flags
    assert "grader did not penalize memory-as-authority" in flags
    assert "grader did not penalize the uncited answer" in flags

    good = {
        "key_consistent": {"parsed": {"correct_conclusion": True, "correct_scope": True}},
        "overgeneralized": {"parsed": {"correct_scope": False, "unsupported_claim": True}},
        "memory_as_authority": {"parsed": {"authority_boundary_preserved": False}},
        "uncited": {"parsed": {"unsupported_claim": True}},
        "synthesis_cited": {"parsed": {"correct_conclusion": True, "unsupported_claim": False}},
    }
    assert executor.calibration_verdict(good) == []

    broken_synthesis = dict(good)
    broken_synthesis["synthesis_cited"] = {"parsed": {"correct_conclusion": True, "unsupported_claim": True}}
    flags = executor.calibration_verdict(broken_synthesis)
    assert "grader marked a correct summary-backed answer as unsupported" in flags


# ---------------------------------------------------------------------------
# Environment scrubbing, neutral workspace and bounded process execution
# ---------------------------------------------------------------------------


def test_build_child_env_scrubs_runner_and_harness_variables(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setenv("ARGENTOS_MEMORY_MODE", "TREATMENT")
    monkeypatch.setenv("ARGENTOS_WORKSPACE", str(tmp_path))
    monkeypatch.setenv("DSH_SESSION_ID", "session-secret")
    monkeypatch.setenv("DEEPSEEK_API_KEY", "sk-test")
    env = executor.build_child_env(tmp_path / "home")
    assert env["DSH_HOME"] == str(tmp_path / "home")
    assert env["DSH_PERMISSION_MODE"] == "read-only"
    assert env.get("DEEPSEEK_API_KEY") == "sk-test"
    assert all(
        not key.startswith(("ARGENTOS_", "DSH_"))
        for key in env
        if key not in {"DSH_HOME", "DSH_PERMISSION_MODE"}
    )


def test_prepare_agent_workspace_uses_a_neutral_path(tmp_path: Path) -> None:
    runner_workspace = tmp_path / "argentos-memory-treatment-abc123" / "repo"
    _write(runner_workspace / "FOO.md", "content\n")
    agent_workspace, copy_root = executor.prepare_agent_workspace(runner_workspace)
    try:
        assert (agent_workspace / "FOO.md").read_text(encoding="utf-8") == "content\n"
        assert "treatment" not in agent_workspace.name.lower()
        assert "control" not in str(agent_workspace).lower()
    finally:
        import shutil

        shutil.rmtree(copy_root, ignore_errors=True)


def test_tool_policy_disables_shell_and_delegation() -> None:
    for tool in ("tool-pwsh", "tool-bash", "tool-web", "tool-subagent", "tool-workflow"):
        assert tool in executor.DISABLED_TOOLS
        assert f"- id: {tool}" in executor.TOOL_POLICY_PATCH


def test_run_process_enforces_a_timeout_and_terminates_the_tree(tmp_path: Path) -> None:
    started = time.perf_counter()
    stdout, stderr, returncode, timed_out = executor.run_process(
        [sys.executable, "-c", "import time; time.sleep(30)"],
        "",
        cwd=tmp_path,
        env=os.environ.copy(),
        timeout=1.0,
    )
    assert timed_out is True
    assert time.perf_counter() - started < 20
    assert stdout == "" and stderr == ""


# ---------------------------------------------------------------------------
# End-to-end main() with synthetic agent and grader (no model, no network)
# ---------------------------------------------------------------------------


def _synthetic_agent_run(*args, **kwargs) -> executor.HeadlessRun:
    answer = "CONCLUSION: yes.\nEVIDENCE: REFACTOR_CREWAI.md"
    events = [
        {"type": "tool_call", "callId": "c1", "tool": "read", "input": {"file_path": "REFACTOR_CREWAI.md"}},
        {"type": "tool_result", "callId": "c1", "status": "completed", "result": "..."},
        {"type": "status", "phase": "step_end", "usage": {"inputTokens": 100, "outputTokens": 10}},
        {"type": "final", "text": answer},
    ]
    return executor.HeadlessRun(
        events=events,
        final_text=answer,
        returncode=0,
        elapsed=1.5,
        usage={"inputTokens": 100, "outputTokens": 10},
        raw_stdout='{"type":"final","text":"CONCLUSION: yes."}\n',
    )


def _synthetic_grader_run(*args, **kwargs) -> executor.HeadlessRun:
    text = json.dumps(
        {
            "correct_conclusion": True,
            "correct_scope": True,
            "authority_boundary_preserved": True,
            "unsupported_claim": False,
            "rationale": "synthetic",
        }
    )
    return executor.HeadlessRun(
        events=[{"type": "final", "text": text}], final_text=text, returncode=0, elapsed=0.5
    )


def _populate_evidence(evidence_dir: Path, question_id: str) -> None:
    key = _valid_key()
    candidates = (
        list(executor.FIXTURE_EVIDENCE_FAMILIES.get(question_id, ()))
        + list(key["questions"][question_id]["supporting_sources"])
        + list(executor.GOVERNANCE_EVIDENCE)
    )
    for rel in dict.fromkeys(candidates):
        _write(evidence_dir / rel, f"# {rel}\n")


def _run_main(
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
    tmp_path: Path,
    *,
    condition: str = "TREATMENT",
    pilot: bool = True,
    question_id: str = "Q04",
    question: str = "Is two-tier retrieval a plausible DEV Memory pattern?",
) -> tuple[int, list[dict], str, Path]:
    workspace = tmp_path / "repo"
    _write(workspace / "REFACTOR_CREWAI.md", "# study\n")
    if pilot:
        _write(workspace / "DEV_MEMORY_PILOT.md", "# memory\n")
    evidence_dir = tmp_path / "groundtruth"
    _populate_evidence(evidence_dir, question_id)
    key_path = _write(tmp_path / "expected-key.json", json.dumps(_valid_key()))
    trace_dir = tmp_path / "traces"

    monkeypatch.setattr(executor, "run_headless", _synthetic_agent_run)
    monkeypatch.setattr(executor, "run_grader", _synthetic_grader_run)
    monkeypatch.setattr(sys, "stdin", io.StringIO(question + "\n"))
    monkeypatch.setenv("ARGENTOS_WORKSPACE", str(workspace))
    monkeypatch.setenv("ARGENTOS_MEMORY_MODE", condition)
    monkeypatch.setenv("ARGENTOS_QUESTION_ID", question_id)
    monkeypatch.setenv("ARGENTOS_TRACE_DIR", str(trace_dir))
    monkeypatch.setenv("ARGENTOS_DSH_CLI", str(_write(tmp_path / "dsh.cmd", "@echo off\n")))
    monkeypatch.setenv("ARGENTOS_BASE_COMMIT", "deadbeef")
    monkeypatch.setenv("ARGENTOS_EXPECTED_KEY", str(key_path))
    monkeypatch.setenv("ARGENTOS_EVIDENCE_DIR", str(evidence_dir))
    monkeypatch.setenv("DEEPSEEK_API_KEY", "sk-test")
    capsys.readouterr()

    returncode = executor.main([])
    captured = capsys.readouterr()
    events = [json.loads(line) for line in captured.out.splitlines() if line.strip()]
    trace = trace_dir / condition.lower() / f"{question_id}.json"
    return returncode, events, captured.err, trace


def test_main_emits_runner_events_and_writes_trace(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str], tmp_path: Path
) -> None:
    returncode, events, stderr, trace = _run_main(monkeypatch, capsys, tmp_path)

    assert returncode == 0
    kinds = [event["event"] for event in events]
    assert kinds[0] == "file_open"
    assert "source_rehydrated" in kinds
    answer = next(event for event in events if event["event"] == "answer")
    assert answer["correct_conclusion"] is True
    assert answer["correct_scope"] is True
    assert answer["authority_boundary_preserved"] is True
    assert answer["unsupported_claim"] is False
    assert answer["provenance_present"] is True
    assert "INTEGRITY" not in stderr

    data = json.loads(trace.read_text(encoding="utf-8"))
    assert data["schema"] == executor.TRACE_SCHEMA
    assert data["condition"] == "TREATMENT"
    assert data["question_id"] == "Q04"
    assert data["workspace"]["neutral_copy"] is True
    assert "treatment" not in data["workspace"]["agent"].lower()
    assert data["integrity"]["pilot_present"] is True
    assert data["integrity"]["condition_labels_in_child_env"] == []
    assert data["integrity"]["condition_token_in_agent_cwd"] is False
    assert data["integrity"]["workspace_stable"] is True
    assert "REFACTOR_CREWAI.md" in data["grader"]["evidence_included"]
    assert data["agent"]["final_answer"].startswith("CONCLUSION:")
    assert data["agent"]["usage"] == {"inputTokens": 100, "outputTokens": 10}
    assert data["run"]["prompt_sha256"]
    assert data["run"]["adapter_sha256"]
    assert data["raw_ndjson"]["agent"]["sha256"]
    assert Path(data["raw_ndjson"]["agent"]["path"]).is_file()
    assert data["integrity"]["out_of_workspace_calls"] == []


def test_main_rejects_control_workspace_that_still_has_the_pilot(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str], tmp_path: Path
) -> None:
    returncode, events, stderr, trace = _run_main(
        monkeypatch, capsys, tmp_path, condition="CONTROL", pilot=True
    )
    assert returncode == 2
    assert "INTEGRITY FAILURE" in stderr
    assert "present in CONTROL" in stderr
    assert events == []
    failure = json.loads(trace.read_text(encoding="utf-8"))
    assert "present in CONTROL" in failure["integrity_failure"]


def _prepare_integrity_test(monkeypatch: pytest.MonkeyPatch, tmp_path: Path, *, agent_run) -> Path:
    workspace = tmp_path / "repo"
    _write(workspace / "REFACTOR_CREWAI.md", "# study\n")
    _write(workspace / "DEV_MEMORY_PILOT.md", "# memory\n")
    evidence_dir = tmp_path / "groundtruth"
    _populate_evidence(evidence_dir, "Q04")
    key_path = _write(tmp_path / "expected-key.json", json.dumps(_valid_key()))
    monkeypatch.setattr(executor, "run_headless", agent_run)
    monkeypatch.setattr(executor, "run_grader", _synthetic_grader_run)
    monkeypatch.setattr(sys, "stdin", io.StringIO("Is two-tier retrieval plausible?\n"))
    monkeypatch.setenv("ARGENTOS_WORKSPACE", str(workspace))
    monkeypatch.setenv("ARGENTOS_MEMORY_MODE", "TREATMENT")
    monkeypatch.setenv("ARGENTOS_QUESTION_ID", "Q04")
    monkeypatch.setenv("ARGENTOS_TRACE_DIR", str(tmp_path / "traces"))
    monkeypatch.setenv("ARGENTOS_DSH_CLI", str(_write(tmp_path / "dsh.cmd", "@echo off\n")))
    monkeypatch.setenv("ARGENTOS_EXPECTED_KEY", str(key_path))
    monkeypatch.setenv("ARGENTOS_EVIDENCE_DIR", str(evidence_dir))
    monkeypatch.setenv("DEEPSEEK_API_KEY", "sk-test")
    return workspace


def test_main_rejects_out_of_workspace_read(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str], tmp_path: Path
) -> None:
    outside = _write(tmp_path / "outside.md", "secret\n")

    def outside_agent(task, cwd, **kwargs):
        events = [
            {"type": "tool_call", "callId": "c1", "tool": "read", "input": {"file_path": str(outside)}},
            {"type": "tool_result", "callId": "c1", "status": "completed", "result": "secret"},
            {"type": "final", "text": "CONCLUSION: x"},
        ]
        return executor.HeadlessRun(events=events, final_text="CONCLUSION: x", returncode=0, elapsed=0.1)

    _prepare_integrity_test(monkeypatch, tmp_path, agent_run=outside_agent)
    capsys.readouterr()
    returncode = executor.main([])
    captured = capsys.readouterr()
    assert returncode == 2
    assert "out-of-workspace" in captured.err
    assert captured.out == ""


def test_main_rejects_workspace_mutation(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str], tmp_path: Path
) -> None:
    def mutating_agent(task, cwd, **kwargs):
        (Path(cwd) / "AGENT_WROTE_THIS.md").write_text("x", encoding="utf-8")
        events = [
            {"type": "tool_call", "callId": "c1", "tool": "read", "input": {"file_path": "REFACTOR_CREWAI.md"}},
            {"type": "tool_result", "callId": "c1", "status": "completed", "result": "x"},
            {"type": "final", "text": "CONCLUSION: x"},
        ]
        return executor.HeadlessRun(events=events, final_text="CONCLUSION: x", returncode=0, elapsed=0.1)

    _prepare_integrity_test(monkeypatch, tmp_path, agent_run=mutating_agent)
    capsys.readouterr()
    returncode = executor.main([])
    captured = capsys.readouterr()
    assert returncode == 2
    assert "workspace changed" in captured.err
    assert captured.out == ""


def test_main_rejects_completed_use_of_a_frozen_out_tool(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str], tmp_path: Path
) -> None:
    def pwsh_agent(task, cwd, **kwargs):
        events = [
            {"type": "tool_call", "callId": "c1", "tool": "pwsh", "input": {"command": "Get-Location"}},
            {"type": "tool_result", "callId": "c1", "status": "completed", "result": "..."},
            {"type": "final", "text": "CONCLUSION: x"},
        ]
        return executor.HeadlessRun(events=events, final_text="CONCLUSION: x", returncode=0, elapsed=0.1)

    _prepare_integrity_test(monkeypatch, tmp_path, agent_run=pwsh_agent)
    capsys.readouterr()
    returncode = executor.main([])
    captured = capsys.readouterr()
    assert returncode == 2
    assert "observed in use" in captured.err
    assert captured.out == ""
    failure = json.loads((tmp_path / "traces" / "treatment" / "Q04.json").read_text(encoding="utf-8"))
    assert "pwsh" in failure["integrity_failure"]


def test_main_treats_a_failed_frozen_out_tool_attempt_as_a_note(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str], tmp_path: Path
) -> None:
    """A model trying a non-existent tool must not invalidate the measurement."""

    def bash_attempt_agent(task, cwd, **kwargs):
        events = [
            {"type": "tool_call", "callId": "c0", "tool": "bash", "input": {"command": "ls"}},
            {"type": "tool_result", "callId": "c0", "status": "error", "result": 'Error: unknown tool "bash"'},
            {"type": "tool_call", "callId": "c1", "tool": "read", "input": {"file_path": "REFACTOR_CREWAI.md"}},
            {"type": "tool_result", "callId": "c1", "status": "completed", "result": "..."},
            {"type": "final", "text": "CONCLUSION: yes.\nEVIDENCE: REFACTOR_CREWAI.md"},
        ]
        return executor.HeadlessRun(
            events=events,
            final_text="CONCLUSION: yes.\nEVIDENCE: REFACTOR_CREWAI.md",
            returncode=0,
            elapsed=0.1,
            raw_stdout='{"type":"final","text":"CONCLUSION: yes."}\n',
        )

    _prepare_integrity_test(monkeypatch, tmp_path, agent_run=bash_attempt_agent)
    capsys.readouterr()
    returncode = executor.main([])
    captured = capsys.readouterr()
    assert returncode == 0
    answer = next(json.loads(line) for line in captured.out.splitlines() if '"answer"' in line)
    assert answer["correct_conclusion"] is True
    data = json.loads((tmp_path / "traces" / "treatment" / "Q04.json").read_text(encoding="utf-8"))
    assert data["integrity"]["observed_disallowed_tools"] == []
    assert data["integrity"]["observed_disallowed_tool_attempts"] == ["bash"]
    assert any("failed attempts" in note for note in data["notes"])


def test_main_rejects_treatment_workspace_without_the_pilot(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str], tmp_path: Path
) -> None:
    returncode, events, stderr, _ = _run_main(
        monkeypatch, capsys, tmp_path, condition="TREATMENT", pilot=False
    )
    assert returncode == 2
    assert "missing in TREATMENT" in stderr
    assert events == []


def test_main_rejects_incomplete_expected_key(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str], tmp_path: Path
) -> None:
    key = _valid_key()
    del key["questions"]["Q12"]
    key_path = _write(tmp_path / "expected-key.json", json.dumps(key))
    evidence_dir = tmp_path / "groundtruth"
    evidence_dir.mkdir()
    monkeypatch.setattr(sys, "stdin", io.StringIO("question\n"))
    monkeypatch.setenv("ARGENTOS_EXPECTED_KEY", str(key_path))
    monkeypatch.setenv("ARGENTOS_EVIDENCE_DIR", str(evidence_dir))
    monkeypatch.setenv("ARGENTOS_DSH_CLI", str(_write(tmp_path / "dsh.cmd", "@echo off\n")))
    monkeypatch.setenv("DEEPSEEK_API_KEY", "sk-test")
    returncode = executor.main([])
    assert returncode == 2
    assert "Q12: missing" in capsys.readouterr().err


def test_main_rejects_empty_question(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str], tmp_path: Path
) -> None:
    monkeypatch.setattr(sys, "stdin", io.StringIO("   \n"))
    returncode = executor.main([])
    assert returncode == 2
    assert "empty question" in capsys.readouterr().err


def test_main_reports_missing_dsh_cli(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str], tmp_path: Path
) -> None:
    monkeypatch.setattr(sys, "stdin", io.StringIO("question\n"))
    monkeypatch.setenv("ARGENTOS_DSH_CLI", str(tmp_path / "does-not-exist.cmd"))
    monkeypatch.setenv("ARGENTOS_EXPECTED_KEY", str(_write(tmp_path / "key.json", json.dumps(_valid_key()))))
    evidence_dir = tmp_path / "groundtruth"
    evidence_dir.mkdir()
    monkeypatch.setenv("ARGENTOS_EVIDENCE_DIR", str(evidence_dir))
    monkeypatch.setattr(executor.shutil, "which", lambda name: None)
    monkeypatch.setattr(executor, "DEFAULT_DSH_CLI", str(tmp_path / "also-missing.cmd"))
    returncode = executor.main([])
    assert returncode == 2
    assert "dsh CLI not found" in capsys.readouterr().err
