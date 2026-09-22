"""Tests for tools/determine_execution_state.py (dev-only, no payload dependency)."""

from __future__ import annotations

import json
import os
import shutil
import subprocess
import tempfile
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[1]

import determine_execution_state as des  # noqa: E402
import scoped_content_identity as sci  # noqa: E402


_GIT_ENV = {
    "GIT_AUTHOR_NAME": "t",
    "GIT_AUTHOR_EMAIL": "t@t",
    "GIT_COMMITTER_NAME": "t",
    "GIT_COMMITTER_EMAIL": "t@t",
    "PATH": os.environ.get("PATH", ""),
    "HOME": os.environ.get("HOME", ""),
    "SYSTEMROOT": os.environ.get("SYSTEMROOT", ""),
}


def _git(repo: Path, *args: str) -> str:
    """Run git in ``repo`` and return trimmed stdout; raises on failure."""
    result = subprocess.run(
        ["git", "-C", str(repo), *args],
        check=True,
        capture_output=True,
        text=True,
        env=_GIT_ENV,
    )
    return result.stdout.strip()


def _init_git_root(tmp_path: Path) -> Path:
    """Turn tmp_path into a git repo with one committed baseline file."""
    _git(tmp_path, "init", "-q", "-b", "main")
    (tmp_path / "baseline.txt").write_text("baseline\n", encoding="utf-8")
    _git(tmp_path, "add", "baseline.txt")
    _git(tmp_path, "commit", "-q", "-m", "initial")
    return tmp_path


def _write_state(session: Path, iteration: str, status: str, gates: dict) -> None:
    """Write a state.json for an iteration of a fixture session."""
    iter_dir = session / iteration
    iter_dir.mkdir(parents=True, exist_ok=True)
    state = {
        "session": session.name,
        "iteration": iteration,
        "task_profile": "standard",
        "gates": gates,
        "last_gate": max(gates) if gates else None,
        "status": status,
        "updated": "2026-09-05T12:00:00Z",
    }
    (iter_dir / "state.json").write_text(json.dumps(state), encoding="utf-8")


def _write_session_log(session: Path, version: str = "11.0.0") -> None:
    """Write the minimal SESSION_LOG header declaring the protocol version."""
    session.mkdir(parents=True, exist_ok=True)
    (session / "SESSION_LOG.md").write_text(
        f"# Session Log\n\n- Session UUID: {session.name}\n"
        f"- Protocol version: {version}\n",
        encoding="utf-8",
    )


def _session_uuid(tmp_path: Path, name: str = "uuid-session") -> Path:
    session = tmp_path / ".project" / name
    _write_session_log(session)
    return session


def test_no_project_dir_is_empty(tmp_path):
    report = des.determine(tmp_path)
    assert report["executions"] == []
    assert report["summary"] == {"total": 0, "determined": 0, "undetermined": 0}


def test_completed_terminal_state_is_determined(tmp_path):
    session = _session_uuid(tmp_path)
    gates = {
        trigger: {"result": "PASS", "timestamp": "2026-09-05T12:00:00Z"}
        for trigger in ("H00", "H01", "H02", "H03", "H04", "H05", "H06", "H07")
    }
    _write_state(session, "00", "COMPLETED", gates)
    report = des.determine(tmp_path)
    entry = report["executions"][0]
    assert entry["session"] == session.name
    assert entry["iteration"] == "00"
    assert entry["state_json"] == "present"
    assert entry["determined"] is True
    assert entry["terminal_task_state"] == "COMPLETED"
    assert entry["reason"] is None
    assert report["summary"] == {"total": 1, "determined": 1, "undetermined": 0}


def test_abort_terminal_state_is_determined(tmp_path):
    session = _session_uuid(tmp_path)
    gates = {"H00": {"result": "PASS", "timestamp": "2026-09-05T11:00:00Z"}}
    _write_state(session, "00", "ABORT", gates)
    entry = des.determine(tmp_path)["executions"][0]
    assert entry["determined"] is True
    assert entry["terminal_task_state"] == "ABORT"


def test_in_progress_status_is_not_determined_even_with_closure_gates(tmp_path):
    """A record without terminal status must not yield an inferred result."""
    session = _session_uuid(tmp_path)
    gates = {
        trigger: {"result": "PASS", "timestamp": "2026-09-05T12:00:00Z"}
        for trigger in ("H00", "H01", "H02", "H03", "H04", "H05", "H06", "H07")
    }
    _write_state(session, "00", "in_progress", gates)
    entry = des.determine(tmp_path)["executions"][0]
    assert entry["determined"] is False
    assert entry["terminal_task_state"] is None
    assert entry["reason"] == "status_not_terminal"


def test_no_gates_passed_status_is_not_determined(tmp_path):
    session = _session_uuid(tmp_path)
    _write_state(session, "00", "no_gates_passed", {})
    entry = des.determine(tmp_path)["executions"][0]
    assert entry["determined"] is False
    assert entry["reason"] == "status_not_terminal"


def test_missing_state_json_is_not_determined(tmp_path):
    session = _session_uuid(tmp_path)
    (session / "00").mkdir()
    entry = des.determine(tmp_path)["executions"][0]
    assert entry["state_json"] == "missing"
    assert entry["determined"] is False
    assert entry["reason"] == "state_json_missing"


def test_corrupt_state_json_is_not_determined(tmp_path):
    session = _session_uuid(tmp_path)
    iter_dir = session / "00"
    iter_dir.mkdir(parents=True)
    (iter_dir / "state.json").write_text("{not json", encoding="utf-8")
    entry = des.determine(tmp_path)["executions"][0]
    assert entry["state_json"] == "corrupt"
    assert entry["determined"] is False
    assert entry["reason"] == "state_json_corrupt"


def test_non_dict_state_json_is_not_determined(tmp_path):
    session = _session_uuid(tmp_path)
    iter_dir = session / "00"
    iter_dir.mkdir(parents=True)
    (iter_dir / "state.json").write_text('"not-an-object"', encoding="utf-8")
    entry = des.determine(tmp_path)["executions"][0]
    assert entry["state_json"] == "corrupt"
    assert entry["determined"] is False


def test_state_json_without_status_is_not_determined(tmp_path):
    session = _session_uuid(tmp_path)
    iter_dir = session / "00"
    iter_dir.mkdir(parents=True)
    (iter_dir / "state.json").write_text('{"gates": {}}', encoding="utf-8")
    entry = des.determine(tmp_path)["executions"][0]
    assert entry["state_json"] == "corrupt"
    assert entry["determined"] is False


def test_session_filter_limits_report(tmp_path):
    first = _session_uuid(tmp_path, "session-a")
    second = _session_uuid(tmp_path, "session-b")
    _write_state(first, "00", "COMPLETED", {"H00": {}})
    _write_state(second, "00", "ABORT", {})
    report = des.determine(tmp_path, session_filter="session-a")
    assert [e["session"] for e in report["executions"]] == ["session-a"]
    assert report["summary"]["total"] == 1


def test_multiple_iterations_report_in_numeric_order(tmp_path):
    session = _session_uuid(tmp_path)
    _write_state(session, "00", "COMPLETED", {"H00": {}})
    _write_state(session, "01", "ABORT", {})
    report = des.determine(tmp_path)
    assert [e["iteration"] for e in report["executions"]] == ["00", "01"]
    assert report["summary"] == {"total": 2, "determined": 2, "undetermined": 0}


def test_protocol_version_reported_from_session_log(tmp_path):
    session = tmp_path / ".project" / "uuid-version"
    _write_session_log(session, "10.3.0")
    _write_state(session, "00", "COMPLETED", {"H00": {}})
    entry = des.determine(tmp_path)["executions"][0]
    assert entry["protocol_version"] == "10.3.0"


def test_cli_prints_json_report(tmp_path, capsys):
    session = _session_uuid(tmp_path)
    _write_state(session, "00", "COMPLETED", {"H00": {}})
    assert des.main(["--root", str(tmp_path)]) == 0
    captured = capsys.readouterr()
    report = json.loads(captured.out)
    assert report["summary"] == {"total": 1, "determined": 1, "undetermined": 0}


def test_iteration_query_returns_only_the_requested_execution(tmp_path):
    session = _session_uuid(tmp_path)
    _write_state(session, "00", "COMPLETED", {"H00": {}})
    _write_state(session, "01", "ABORT", {})
    report = des.determine(
        tmp_path, session_filter=session.name, iteration_filter="00"
    )
    assert [e["iteration"] for e in report["executions"]] == ["00"]
    assert report["summary"] == {"total": 1, "determined": 1, "undetermined": 0}
    entry = report["executions"][0]
    assert entry["session"] == session.name
    assert entry["determined"] is True
    assert entry["terminal_task_state"] == "COMPLETED"


def test_iteration_query_distinguishes_same_iteration_across_sessions(tmp_path):
    first = _session_uuid(tmp_path, "session-a")
    second = _session_uuid(tmp_path, "session-b")
    _write_state(first, "00", "COMPLETED", {"H00": {}})
    _write_state(second, "00", "ABORT", {})
    report = des.determine(
        tmp_path, session_filter="session-a", iteration_filter="00"
    )
    assert [e["session"] for e in report["executions"]] == ["session-a"]
    assert report["executions"][0]["terminal_task_state"] == "COMPLETED"


def test_iteration_query_non_terminal_execution_is_not_determined(tmp_path):
    session = _session_uuid(tmp_path)
    _write_state(session, "00", "in_progress", {})
    _write_state(session, "01", "ABORT", {})
    report = des.determine(
        tmp_path, session_filter=session.name, iteration_filter="00"
    )
    assert len(report["executions"]) == 1
    entry = report["executions"][0]
    assert entry["determined"] is False
    assert entry["reason"] == "status_not_terminal"
    assert report["summary"] == {"total": 1, "determined": 0, "undetermined": 1}


def test_iteration_query_missing_state_json_is_fail_closed(tmp_path):
    session = _session_uuid(tmp_path)
    (session / "00").mkdir()
    report = des.determine(
        tmp_path, session_filter=session.name, iteration_filter="00"
    )
    assert len(report["executions"]) == 1
    entry = report["executions"][0]
    assert entry["state_json"] == "missing"
    assert entry["determined"] is False
    assert entry["reason"] == "state_json_missing"


def test_iteration_query_corrupt_state_json_is_fail_closed(tmp_path):
    session = _session_uuid(tmp_path)
    iter_dir = session / "00"
    iter_dir.mkdir(parents=True)
    (iter_dir / "state.json").write_text("{not json", encoding="utf-8")
    report = des.determine(
        tmp_path, session_filter=session.name, iteration_filter="00"
    )
    assert len(report["executions"]) == 1
    entry = report["executions"][0]
    assert entry["state_json"] == "corrupt"
    assert entry["determined"] is False
    assert entry["reason"] == "state_json_corrupt"


def test_iteration_query_nonexistent_iteration_is_empty(tmp_path):
    session = _session_uuid(tmp_path)
    _write_state(session, "00", "COMPLETED", {"H00": {}})
    report = des.determine(
        tmp_path, session_filter=session.name, iteration_filter="99"
    )
    assert report["executions"] == []
    assert report["summary"] == {"total": 0, "determined": 0, "undetermined": 0}


def test_iteration_query_unknown_session_is_empty(tmp_path):
    session = _session_uuid(tmp_path)
    _write_state(session, "00", "COMPLETED", {"H00": {}})
    report = des.determine(
        tmp_path, session_filter="unknown-session", iteration_filter="00"
    )
    assert report["executions"] == []
    assert report["summary"] == {"total": 0, "determined": 0, "undetermined": 0}


def test_iteration_without_session_fails_deterministically(tmp_path):
    with pytest.raises(SystemExit) as excinfo:
        des.main(["--root", str(tmp_path), "--iteration", "00"])
    assert excinfo.value.code == 2


def test_full_session_query_keeps_reporting_all_iterations(tmp_path):
    session = _session_uuid(tmp_path)
    _write_state(session, "00", "COMPLETED", {"H00": {}})
    _write_state(session, "01", "ABORT", {})
    report = des.determine(tmp_path, session_filter=session.name)
    assert [e["iteration"] for e in report["executions"]] == ["00", "01"]
    assert report["summary"] == {"total": 2, "determined": 2, "undetermined": 0}


# ── Plan 110: --content-identity (result ↔ Execution Record content identity)


def _write_artifact(session: Path, iteration: str, name: str, text: str) -> None:
    """Write a per-iteration session artifact of a fixture session."""
    iter_dir = session / iteration
    iter_dir.mkdir(parents=True, exist_ok=True)
    (iter_dir / name).write_text(text, encoding="utf-8")


def _git_session(tmp_path: Path, name: str = "uuid-git") -> tuple[Path, Path]:
    """Git repo root + session fixture with the session under .project/."""
    root = _init_git_root(tmp_path)
    session = _session_uuid(root, name)
    return root, session


def _record_scope(session: str, iteration: str, *names: str) -> list[str]:
    """Repo-relative record scope (sorted) of an iteration fixture."""
    return sorted(f".project/{session}/{iteration}/{name}" for name in names)


def test_content_identity_applies_for_completed_execution(tmp_path):
    root, session = _git_session(tmp_path)
    gates = {
        trigger: {"result": "PASS", "timestamp": "2026-09-05T12:00:00Z"}
        for trigger in ("H00", "H01", "H02", "H03", "H04", "H05", "H06", "H07")
    }
    _write_state(session, "00", "COMPLETED", gates)
    _write_artifact(session, "00", "EXECUTION_SUMMARY.md", "# summary\n")

    report = des.determine(
        root,
        session_filter=session.name,
        iteration_filter="00",
        content_identity=True,
    )
    entry = report["executions"][0]
    assert entry["determined"] is True
    assert entry["terminal_task_state"] == "COMPLETED"
    ci = entry["content_identity"]
    assert ci["applicable"] is True
    assert ci["scope"] == _record_scope(
        session.name, "00", "EXECUTION_SUMMARY.md", "state.json"
    )
    assert len(ci["delta_scoped_identity"]) == 64
    assert ci["state_identity"] == {
        "source": "staged",
        "ref": None,
        "tree": _git(root, "write-tree"),
    }
    direct = sci.compute(
        root,
        [
            str((session / "00" / "EXECUTION_SUMMARY.md").resolve()),
            str((session / "00" / "state.json").resolve()),
        ],
    )
    assert ci["delta_scoped_identity"] == direct["delta_scoped_identity"]
    assert ci["state_identity"] == direct["state_identity"]
    assert report["summary"] == {"total": 1, "determined": 1, "undetermined": 0}


# ── Plan 111 (Etapa 1): --session-summary


def _zero_summary(sessions: int = 0) -> dict:
    return {
        "sessions": sessions,
        "executions": 0,
        "determined": 0,
        "undetermined": 0,
        "terminal_abort": 0,
        "terminal_completed": 0,
    }


def test_session_summary_without_project_is_empty(tmp_path):
    report = des.session_summaries(tmp_path)
    assert report["sessions"] == []
    assert report["summary"] == _zero_summary()


def test_session_summary_counts_single_session(tmp_path):
    session = _session_uuid(tmp_path)
    _write_state(session, "00", "COMPLETED", {"H00": {}})
    _write_state(session, "01", "ABORT", {})
    _write_state(session, "02", "in_progress", {})
    report = des.session_summaries(tmp_path)
    assert report["sessions"] == [
        {
            "session": session.name,
            "protocol_version": "11.0.0",
            "executions": 3,
            "determined": 2,
            "undetermined": 1,
            "terminal_abort": 1,
            "terminal_completed": 1,
        }
    ]
    assert report["summary"] == {
        "sessions": 1,
        "executions": 3,
        "determined": 2,
        "undetermined": 1,
        "terminal_abort": 1,
        "terminal_completed": 1,
    }


def test_session_summary_aggregates_multiple_sessions(tmp_path):
    first = _session_uuid(tmp_path, "session-a")
    second = _session_uuid(tmp_path, "session-b")
    _write_state(first, "00", "COMPLETED", {"H00": {}})
    _write_state(second, "00", "ABORT", {})
    _write_state(second, "01", "no_gates_passed", {})
    report = des.session_summaries(tmp_path)
    assert [row["session"] for row in report["sessions"]] == [
        "session-a",
        "session-b",
    ]
    assert report["sessions"][0] == {
        "session": "session-a",
        "protocol_version": "11.0.0",
        "executions": 1,
        "determined": 1,
        "undetermined": 0,
        "terminal_abort": 0,
        "terminal_completed": 1,
    }
    assert report["summary"] == {
        "sessions": 2,
        "executions": 3,
        "determined": 2,
        "undetermined": 1,
        "terminal_abort": 1,
        "terminal_completed": 1,
    }


def test_session_summary_missing_state_json_counts_undetermined(tmp_path):
    session = _session_uuid(tmp_path)
    _write_state(session, "00", "COMPLETED", {"H00": {}})
    (session / "01").mkdir()
    row = des.session_summaries(tmp_path)["sessions"][0]
    assert row["executions"] == 2
    assert row["determined"] == 1
    assert row["undetermined"] == 1
    assert row["terminal_completed"] == 1


def test_session_summary_protocol_version_from_session_log(tmp_path):
    session = tmp_path / ".project" / "uuid-versioned"
    _write_session_log(session, "10.3.0")
    _write_state(session, "00", "ABORT", {})
    row = des.session_summaries(tmp_path)["sessions"][0]
    assert row["protocol_version"] == "10.3.0"


def test_session_summary_protocol_version_none_without_declaration(tmp_path):
    session = tmp_path / ".project" / "uuid-no-log"
    _write_state(session, "00", "COMPLETED", {"H00": {}})
    row = des.session_summaries(tmp_path)["sessions"][0]
    assert row["protocol_version"] is None


def test_session_summary_ignores_knowledge_and_skills_dirs(tmp_path):
    for name in ("knowledge", "skills"):
        _write_state(tmp_path / ".project" / name, "00", "COMPLETED", {})
    report = des.session_summaries(tmp_path)
    assert report["sessions"] == []
    assert report["summary"] == _zero_summary()


def test_session_summary_session_filter_limits_report(tmp_path):
    first = _session_uuid(tmp_path, "session-a")
    _session_uuid(tmp_path, "session-b")
    _write_state(first, "00", "COMPLETED", {"H00": {}})
    report = des.session_summaries(tmp_path, session_filter="session-a")
    assert [row["session"] for row in report["sessions"]] == ["session-a"]
    assert report["summary"]["sessions"] == 1


def test_session_summary_unknown_session_is_fail_closed_empty(tmp_path):
    session = _session_uuid(tmp_path)
    _write_state(session, "00", "COMPLETED", {"H00": {}})
    report = des.session_summaries(tmp_path, session_filter="unknown")
    assert report["sessions"] == []
    assert report["summary"] == _zero_summary()


def test_session_summary_session_without_iterations_is_zero(tmp_path):
    session = _session_uuid(tmp_path)
    row = des.session_summaries(tmp_path)["sessions"][0]
    assert row["session"] == session.name
    assert row["executions"] == 0
    assert row["determined"] == 0
    assert row["undetermined"] == 0
    assert row["terminal_abort"] == 0
    assert row["terminal_completed"] == 0


def test_session_summary_is_deterministic(tmp_path):
    session = _session_uuid(tmp_path)
    _write_state(session, "00", "COMPLETED", {"H00": {}})
    _write_state(session, "01", "in_progress", {})
    first = des.session_summaries(tmp_path)
    second = des.session_summaries(tmp_path)
    assert first == second


def test_cli_session_summary_prints_json_report(tmp_path, capsys):
    session = _session_uuid(tmp_path)
    _write_state(session, "00", "COMPLETED", {"H00": {}})
    assert des.main(["--root", str(tmp_path), "--session-summary"]) == 0
    cli = json.loads(capsys.readouterr().out)
    assert cli == des.session_summaries(tmp_path)


def test_session_summary_with_iteration_fails_deterministically(tmp_path):
    session = _session_uuid(tmp_path)
    _write_state(session, "00", "COMPLETED", {"H00": {}})
    with pytest.raises(SystemExit) as excinfo:
        des.main(
            [
                "--root",
                str(tmp_path),
                "--session",
                session.name,
                "--iteration",
                "00",
                "--session-summary",
            ]
        )
    assert excinfo.value.code == 2


def test_session_summary_with_content_identity_fails_deterministically(
    tmp_path,
):
    session = _session_uuid(tmp_path)
    _write_state(session, "00", "COMPLETED", {"H00": {}})
    with pytest.raises(SystemExit) as excinfo:
        des.main(
            [
                "--root",
                str(tmp_path),
                "--session",
                session.name,
                "--iteration",
                "00",
                "--content-identity",
                "--session-summary",
            ]
        )
    assert excinfo.value.code == 2


def test_content_identity_applies_for_abort_execution(tmp_path):
    root, session = _git_session(tmp_path)
    _write_state(session, "00", "ABORT", {"H00": {}})

    entry = des.determine(
        root,
        session_filter=session.name,
        iteration_filter="00",
        content_identity=True,
    )["executions"][0]
    assert entry["determined"] is True
    assert entry["terminal_task_state"] == "ABORT"
    ci = entry["content_identity"]
    assert ci["applicable"] is True
    assert ci["scope"] == _record_scope(session.name, "00", "state.json")


def test_content_identity_is_deterministic(tmp_path):
    root, session = _git_session(tmp_path)
    _write_state(session, "00", "COMPLETED", {"H00": {}})
    _write_artifact(session, "00", "EXECUTION_SUMMARY.md", "# s\n")

    first = des.determine(
        root,
        session_filter=session.name,
        iteration_filter="00",
        content_identity=True,
    )
    second = des.determine(
        root,
        session_filter=session.name,
        iteration_filter="00",
        content_identity=True,
    )
    assert first == second
    assert first["executions"][0]["content_identity"]["applicable"] is True


def test_content_change_in_record_scope_changes_delta(tmp_path):
    root, session = _git_session(tmp_path)
    _write_state(session, "00", "COMPLETED", {"H00": {}})

    def delta() -> str:
        return des.determine(
            root,
            session_filter=session.name,
            iteration_filter="00",
            content_identity=True,
        )["executions"][0]["content_identity"]["delta_scoped_identity"]

    before = delta()
    state_file = session / "00" / "state.json"
    state = json.loads(state_file.read_text(encoding="utf-8"))
    state["updated"] = "2026-09-06T09:00:00Z"
    state_file.write_text(json.dumps(state), encoding="utf-8")
    after = delta()

    assert before != after


def test_out_of_record_scope_change_keeps_delta(tmp_path):
    root, session = _git_session(tmp_path)
    _write_state(session, "00", "COMPLETED", {"H00": {}})

    def report() -> dict:
        return des.determine(
            root,
            session_filter=session.name,
            iteration_filter="00",
            content_identity=True,
        )["executions"][0]["content_identity"]

    before = report()
    (session / "SESSION_LOG.md").write_text(
        f"# Session Log\n\n- Session UUID: {session.name}\n"
        "- Protocol version: 11.0.1\n",
        encoding="utf-8",
    )
    _write_state(session, "01", "ABORT", {})
    after = report()

    assert before == after


def test_gitignored_record_files_identity_matches_generator(tmp_path):
    root, session = _git_session(tmp_path)
    (root / ".gitignore").write_text(".project/\n", encoding="utf-8")
    _write_state(session, "00", "COMPLETED", {"H00": {}})
    ignored = subprocess.run(
        [
            "git",
            "-C",
            str(root),
            "check-ignore",
            "--",
            f".project/{session.name}/00/state.json",
        ],
        capture_output=True,
        text=True,
        env=_GIT_ENV,
    )
    assert ignored.returncode == 0

    ci = des.determine(
        root,
        session_filter=session.name,
        iteration_filter="00",
        content_identity=True,
    )["executions"][0]["content_identity"]
    assert ci["applicable"] is True
    direct = sci.compute(root, [str((session / "00" / "state.json").resolve())])
    assert ci["delta_scoped_identity"] == direct["delta_scoped_identity"]


def test_empty_iteration_folder_content_not_applicable(tmp_path):
    root, session = _git_session(tmp_path)
    (session / "00").mkdir()

    entry = des.determine(
        root,
        session_filter=session.name,
        iteration_filter="00",
        content_identity=True,
    )["executions"][0]
    assert entry["state_json"] == "missing"
    assert entry["content_identity"] == {
        "applicable": False,
        "reason": "content_scope_empty",
    }


def test_non_git_root_content_not_applicable():
    """A root outside any git repository yields applicable: false.

    Built in the OS temp dir (not pytest tmp_path) so git discovery cannot
    escape into the real repository that hosts the test run.
    """
    root = Path(tempfile.mkdtemp(prefix="nonrepo-"))
    try:
        session = _session_uuid(root)
        _write_state(session, "00", "COMPLETED", {"H00": {}})

        entry = des.determine(
            root,
            session_filter=session.name,
            iteration_filter="00",
            content_identity=True,
        )["executions"][0]
        assert entry["determined"] is True
        assert entry["content_identity"] == {
            "applicable": False,
            "reason": "not_a_git_repository",
        }
    finally:
        shutil.rmtree(root, ignore_errors=True)


def test_content_identity_unknown_session_is_empty(tmp_path):
    root, session = _git_session(tmp_path)
    _write_state(session, "00", "COMPLETED", {"H00": {}})

    report = des.determine(
        root,
        session_filter="unknown-session",
        iteration_filter="00",
        content_identity=True,
    )
    assert report["executions"] == []
    assert report["summary"] == {"total": 0, "determined": 0, "undetermined": 0}


def test_content_identity_unknown_iteration_is_empty(tmp_path):
    root, session = _git_session(tmp_path)
    _write_state(session, "00", "COMPLETED", {"H00": {}})

    report = des.determine(
        root,
        session_filter=session.name,
        iteration_filter="99",
        content_identity=True,
    )
    assert report["executions"] == []
    assert report["summary"] == {"total": 0, "determined": 0, "undetermined": 0}


def test_content_identity_without_session_fails_deterministically(tmp_path):
    with pytest.raises(SystemExit) as excinfo:
        des.main(
            [
                "--root",
                str(tmp_path),
                "--iteration",
                "00",
                "--content-identity",
            ]
        )
    assert excinfo.value.code == 2


def test_content_identity_without_iteration_fails_deterministically(tmp_path):
    with pytest.raises(SystemExit) as excinfo:
        des.main(
            [
                "--root",
                str(tmp_path),
                "--session",
                "uuid-git",
                "--content-identity",
            ]
        )
    assert excinfo.value.code == 2


def test_specific_query_without_content_identity_is_unchanged(tmp_path):
    root, session = _git_session(tmp_path)
    _write_state(session, "00", "COMPLETED", {"H00": {}})

    report = des.determine(
        root, session_filter=session.name, iteration_filter="00"
    )
    assert len(report["executions"]) == 1
    assert "content_identity" not in report["executions"][0]


def test_full_session_query_without_content_identity_is_unchanged(tmp_path):
    root, session = _git_session(tmp_path)
    _write_state(session, "00", "COMPLETED", {"H00": {}})
    _write_state(session, "01", "ABORT", {})

    report = des.determine(root, session_filter=session.name)
    assert [e["iteration"] for e in report["executions"]] == ["00", "01"]
    assert all("content_identity" not in e for e in report["executions"])


def test_content_identity_api_requires_targeted_filters(tmp_path):
    with pytest.raises(ValueError):
        des.determine(tmp_path, content_identity=True)
    with pytest.raises(ValueError):
        des.determine(
            tmp_path, session_filter="uuid-git", content_identity=True
        )


def test_content_identity_api_matches_cli(tmp_path, capsys):
    root, session = _git_session(tmp_path)
    _write_state(session, "00", "COMPLETED", {"H00": {}})
    _write_artifact(session, "00", "EXECUTION_SUMMARY.md", "# s\n")

    api = des.determine(
        root,
        session_filter=session.name,
        iteration_filter="00",
        content_identity=True,
    )
    assert (
        des.main(
            [
                "--root",
                str(root),
                "--session",
                session.name,
                "--iteration",
                "00",
                "--content-identity",
            ]
        )
        == 0
    )
    cli = json.loads(capsys.readouterr().out)
    assert cli == api


def test_content_identity_over_missing_state_json_uses_other_files(tmp_path):
    root, session = _git_session(tmp_path)
    _write_artifact(session, "00", "EXECUTION_SUMMARY.md", "# s\n")

    entry = des.determine(
        root,
        session_filter=session.name,
        iteration_filter="00",
        content_identity=True,
    )["executions"][0]
    assert entry["state_json"] == "missing"
    assert entry["determined"] is False
    assert entry["reason"] == "state_json_missing"
    ci = entry["content_identity"]
    assert ci["applicable"] is True
    assert ci["scope"] == _record_scope(
        session.name, "00", "EXECUTION_SUMMARY.md"
    )


def test_content_identity_over_corrupt_state_json(tmp_path):
    root, session = _git_session(tmp_path)
    _write_artifact(session, "00", "EXECUTION_SUMMARY.md", "# s\n")
    (session / "00" / "state.json").write_text("{not json", encoding="utf-8")

    entry = des.determine(
        root,
        session_filter=session.name,
        iteration_filter="00",
        content_identity=True,
    )["executions"][0]
    assert entry["state_json"] == "corrupt"
    assert entry["determined"] is False
    assert entry["reason"] == "state_json_corrupt"
    ci = entry["content_identity"]
    assert ci["applicable"] is True
    assert ci["scope"] == _record_scope(
        session.name, "00", "EXECUTION_SUMMARY.md", "state.json"
    )


# ── Plan 111 (Etapa 2): --undetermined


def test_undetermined_filters_report_to_undetermined_entries(tmp_path):
    session = _session_uuid(tmp_path)
    _write_state(session, "00", "COMPLETED", {"H00": {}})
    _write_state(session, "01", "in_progress", {})
    (session / "02").mkdir()
    report = des.determine(tmp_path, undetermined_only=True)
    assert [entry["iteration"] for entry in report["executions"]] == [
        "01",
        "02",
    ]
    assert all(entry["determined"] is False for entry in report["executions"])
    assert report["summary"] == {
        "total": 2,
        "determined": 0,
        "undetermined": 2,
    }


def test_undetermined_keeps_deterministic_reasons(tmp_path):
    session = _session_uuid(tmp_path)
    _write_state(session, "00", "in_progress", {})
    (session / "01").mkdir()
    iter_dir = session / "02"
    iter_dir.mkdir()
    (iter_dir / "state.json").write_text("{not json", encoding="utf-8")
    report = des.determine(tmp_path, undetermined_only=True)
    reasons = {
        entry["iteration"]: entry["reason"] for entry in report["executions"]
    }
    assert reasons == {
        "00": "status_not_terminal",
        "01": "state_json_missing",
        "02": "state_json_corrupt",
    }


def test_undetermined_combines_with_session_filter(tmp_path):
    first = _session_uuid(tmp_path, "session-a")
    _session_uuid(tmp_path, "session-b")
    _write_state(first, "00", "COMPLETED", {"H00": {}})
    _write_state(first, "01", "in_progress", {})
    report = des.determine(
        tmp_path, session_filter="session-a", undetermined_only=True
    )
    assert [entry["iteration"] for entry in report["executions"]] == ["01"]
    assert report["summary"] == {
        "total": 1,
        "determined": 0,
        "undetermined": 1,
    }


def test_undetermined_without_undetermined_entries_is_empty(tmp_path):
    session = _session_uuid(tmp_path)
    _write_state(session, "00", "COMPLETED", {"H00": {}})
    _write_state(session, "01", "ABORT", {})
    report = des.determine(tmp_path, undetermined_only=True)
    assert report["executions"] == []
    assert report["summary"] == {"total": 0, "determined": 0, "undetermined": 0}


def test_undetermined_across_sessions_aggregates(tmp_path):
    first = _session_uuid(tmp_path, "session-a")
    second = _session_uuid(tmp_path, "session-b")
    _write_state(first, "00", "ABORT", {})
    _write_state(first, "01", "in_progress", {})
    _write_state(second, "00", "no_gates_passed", {})
    report = des.determine(tmp_path, undetermined_only=True)
    assert [entry["session"] for entry in report["executions"]] == [
        "session-a",
        "session-b",
    ]
    assert report["summary"] == {
        "total": 2,
        "determined": 0,
        "undetermined": 2,
    }


def test_default_report_unchanged_without_undetermined_flag(tmp_path):
    session = _session_uuid(tmp_path)
    _write_state(session, "00", "COMPLETED", {"H00": {}})
    _write_state(session, "01", "in_progress", {})
    assert des.determine(tmp_path) == des.determine(
        tmp_path, undetermined_only=False
    )
    assert des.determine(tmp_path)["summary"] == {
        "total": 2,
        "determined": 1,
        "undetermined": 1,
    }


def test_cli_undetermined_prints_json_report(tmp_path, capsys):
    session = _session_uuid(tmp_path)
    _write_state(session, "00", "COMPLETED", {"H00": {}})
    _write_state(session, "01", "in_progress", {})
    assert des.main(["--root", str(tmp_path), "--undetermined"]) == 0
    cli = json.loads(capsys.readouterr().out)
    assert cli == des.determine(tmp_path, undetermined_only=True)


def test_undetermined_with_iteration_fails_deterministically(tmp_path):
    session = _session_uuid(tmp_path)
    _write_state(session, "00", "COMPLETED", {"H00": {}})
    with pytest.raises(SystemExit) as excinfo:
        des.main(
            [
                "--root",
                str(tmp_path),
                "--session",
                session.name,
                "--iteration",
                "00",
                "--undetermined",
            ]
        )
    assert excinfo.value.code == 2


def test_undetermined_with_session_summary_fails_deterministically(tmp_path):
    session = _session_uuid(tmp_path)
    _write_state(session, "00", "COMPLETED", {"H00": {}})
    with pytest.raises(SystemExit) as excinfo:
        des.main(
            [
                "--root",
                str(tmp_path),
                "--session-summary",
                "--undetermined",
            ]
        )
    assert excinfo.value.code == 2


def test_undetermined_api_guard_rejects_iteration(tmp_path):
    session = _session_uuid(tmp_path)
    _write_state(session, "00", "COMPLETED", {"H00": {}})
    with pytest.raises(ValueError):
        des.determine(
            tmp_path,
            session_filter=session.name,
            iteration_filter="00",
            undetermined_only=True,
        )
