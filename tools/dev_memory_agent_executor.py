#!/usr/bin/env python3
"""EXPERIMENTAL external-agent executor for the DEV Memory controlled test.

This module is experimental infrastructure, **not** Protocol, **not** runtime and
**not** a DEV Memory implementation. It exists only so that the frozen harness
``tools/dev_memory_controlled_runner.py`` can execute a real local DeepSeek agent
against the Control / Treatment workspace copies of plan 181.

Interface implemented (this is the interface the runner defines -- see its
module docstring and ``run_question``):

* stdin      -- exactly one benchmark question (text).
* cwd        -- the condition workspace produced by the runner.
* stdout     -- newline-delimited JSON instrumentation events:
                 {"event": "file_open", "path": "..."}
                 {"event": "search", "query": "..."}
                 {"event": "source_rehydrated", "path": "..."}
                 {"event": "answer", "<rubric field>": true|false, ...}
* env (read) -- ``ARGENTOS_QUESTION_ID``, ``ARGENTOS_WORKSPACE``,
                 ``ARGENTOS_MEMORY_MODE``. They are consumed here and are
                 deliberately NOT forwarded to the agent.

Experiment-only environment (not part of the runner contract):

* ``DEEPSEEK_API_KEY``        -- credential for the DeepSeek provider route.
* ``ARGENTOS_DSH_CLI``        -- path to the local ``dsh`` CLI.
* ``ARGENTOS_TRACE_DIR``      -- directory for per-question trace JSON files.
* ``ARGENTOS_EXPECTED_KEY``   -- JSON expected-answer key used by the grader.
* ``ARGENTOS_EVIDENCE_DIR``   -- pristine source tree used to build the grader's
                                 fixed per-question evidence pack.
* ``ARGENTOS_BASE_COMMIT``    -- corpus commit recorded in the trace.
* ``ARGENTOS_MODEL_LABEL``    -- free-text label of the model route used.
* ``ARGENTOS_AGENT_TIMEOUT``  -- seconds per agent run (same in both conditions).
* ``ARGENTOS_JUDGE_TIMEOUT``  -- seconds per grading run.

How a question is executed
--------------------------

1. The runner's condition workspace is copied to a neutral temporary path
   (``bench-<hex>/repo``). The agent runs there, because the runner's own
   temporary directory name contains the condition label and the installed
   harness reports the absolute cwd to the model. File contents are identical;
   only the path visible to the agent is neutral. The copy is deleted afterwards.
2. A fresh ``dsh --profile headless --json`` process runs the *same* task prompt
   in both conditions, with a scrubbed environment, a read-only sandbox and an
   overlaid tool policy that removes web search, subagents, workflows, jobs and
   shell tools. Shell tools are removed so that every retrieval operation is
   visible to the instrumentation (read/grep/glob) instead of being guessed
   from shell command text.
3. Its NDJSON run events are mapped to runner instrumentation:
   * ``read`` tool call                     -> ``file_open``
   * ``grep`` / ``glob`` tool call          -> ``search``
   * opening a historical source artifact   -> ``source_rehydrated``
4. A second, fresh ``dsh`` session (same model, empty scratch cwd) grades the
   answer against the frozen rubric. It is blind to the condition: it never
   receives the file list of the run and its evidence is a FIXED per-question
   pack read from the pristine evidence tree (derived summaries and memory notes
   excluded), identical for every answer of that question. ``provenance_present``
   is computed deterministically by this adapter instead of being self-reported.

Anything the adapter cannot determine stays unknown (no answer field is emitted),
never guessed.

Modes: the default mode executes one question from stdin; ``--self-check``
validates configuration; ``--calibrate`` grades synthetic answers with the fixed
grader to expose scoring failures before a benchmark run.
"""

from __future__ import annotations

import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

TRACE_SCHEMA = "argentos.dev-memory.controlled-trace.v1"
CALIBRATION_SCHEMA = "argentos.dev-memory.grader-calibration.v1"

#: Historical source artifacts of the comparative study (plan 180). Opening one
#: of these is what the pilot's retrieval contract calls source rehydration:
#: consulting the original evidence instead of a derived conclusion.
SOURCE_ARTIFACTS = frozenset(
    {
        "REFACTOR_LANGGRAPH.md",
        "REFACTOR_OPENAI_AGENTS_SDK.md",
        "REFACTOR_MICROSOFT_AGENT_FRAMEWORK.md",
        "REFACTOR_GOOGLE_ADK.md",
        "REFACTOR_CREWAI.md",
        "REFACTOR_OPENHANDS.md",
        "REFACTOR_SWE_AGENT.md",
        "REFACTOR_LETTA.md",
        "REFACTOR_SYNTHESIS.md",
        "REFACTOR_MATRIX.md",
        "protocol/.agents/standards/context/MEMORY_SYSTEM.md",
    }
)

#: Derived memory surface. It is a legitimate file to open (it is the treatment
#: intervention) but it is not a source artifact for provenance purposes.
MEMORY_SURFACE = "DEV_MEMORY_PILOT.md"

DEFAULT_DSH_CLI = r"D:\Programas\DeepseekHarness\resources\runtime\cli\bin\dsh.cmd"
DEFAULT_AGENT_TIMEOUT = 600.0
DEFAULT_JUDGE_TIMEOUT = 300.0
EVIDENCE_TOTAL_CAP = 60_000
EVIDENCE_PER_FILE_CAP = 8_000
ANSWER_TRACE_CAP = 20_000

#: Agent tool policy overlay. The experiment measures repository retrieval, so
#: the agent must not reach the network, delegate to subagents, run workflows,
#: use shell tools (an instrumentation blind spot) or leave the condition
#: workspace. This overlay is identical in both conditions.
DISABLED_TOOLS = (
    "tool-web",
    "tool-subagent",
    "tool-subagent-fork",
    "tool-workflow",
    "tool-jobs",
    "tool-working-directory",
    "tool-pwsh",
    "tool-bash",
    "tool-subagent-control",
    "tool-subagent-list-agents",
)
TOOL_POLICY_PATCH = "".join(f"- id: {tool}\n  disabled: true\n" for tool in DISABLED_TOOLS)

#: The grader needs no filesystem or delegation tools at all: its evidence is
#: supplied inside the prompt, and a tool-free grader cannot inspect either
#: condition's workspace.
GRADER_DISABLED_TOOLS = DISABLED_TOOLS + (
    "tool-fs",
    "tool-fs-search",
    "tool-skill",
    "tool-todo",
    "tool-goal",
)
GRADER_TOOL_POLICY_PATCH = "".join(
    f"- id: {tool}\n  disabled: true\n" for tool in GRADER_DISABLED_TOOLS
)

#: Run questions with tool calls outside the frozen policy count as an
#: integrity observation, never as benchmark data.
AGENT_TOOL_NAMES = frozenset({"read", "grep", "glob", "pwsh", "bash", "skill", "jobs", "job_output"})

#: Tools the frozen policy removes. A *completed* call of one of these is an
#: integrity failure; a failed attempt (e.g. the model trying `bash` on Windows,
#: where that tool does not exist) is recorded as a note, not as data loss.
DISALLOWED_AGENT_TOOLS = frozenset(
    {"pwsh", "bash", "subagent", "subagent_fork", "workflow", "jobs", "web"}
)

TASK_TEMPLATE = """\
You are performing repository research to answer one question about the ARgentOS project.

QUESTION: {question}

Work only inside the current working directory (the repository root). Use the file search and file read tools to locate evidence. Do not modify, create or delete files. Do not use network access.

Answer only from what you actually find in this repository. Do not rely on outside knowledge or assumptions; if the repository does not establish something, say so.

Return your final answer in exactly this structure:

CONCLUSION: <a direct answer to the question>
SCOPE: <where the conclusion applies and where it must not be generalized>
EVIDENCE: <repository-relative paths that support the answer, and what each one says>
AUTHORITY: <which artifacts are authoritative evidence for this answer, and whether any of them are only derived summaries or indexes; state what remains unverified>
UNSUPPORTED: <claims or parts of the question the repository does not settle, or "none">
"""

GRADER_TEMPLATE = """\
You are an independent evaluator grading ONE repository-research answer against a fixed rubric. You do not know which experimental condition produced it, and the material below does not reveal it. Judge only the answer and the material supplied here. Do not use outside knowledge.

QUESTION: {question}

EXPECTED ANSWER KEY (derived independently from the historical comparative-study artifacts; it is a reference for grading, not an authority):
{expected_key}

AGENT ANSWER:
{answer}

FIXED EVIDENCE PACK -- the historical source artifacts, their secondary synthesis/matrix summaries and the fixed governance references for this question, identical for every answer to this question. Derived indexes, entry points and memory notes are excluded:
{evidence}

RUBRIC -- four binary fields:
1. correct_conclusion -- true if the AGENT ANSWER's conclusion agrees with the expected key on the decisive point; false if it contradicts the key or misses the decisive point.
2. correct_scope -- true if the answer states applicability and limits consistent with the expected key and does not over-generalize; false otherwise.
3. authority_boundary_preserved -- true if the answer distinguishes source evidence from derived/summary/index artifacts and does not treat any summary, memory note or index as authoritative for the conclusion; false if it does.
4. unsupported_claim -- true if the answer contains at least one material claim that the FIXED EVIDENCE PACK does not state. The secondary synthesis/matrix summaries count as evidence for what the studies report, but they are not authority (treating them as authority is a separate authority-boundary failure). Repeating the expected key is NOT by itself evidence that a claim is supported; support must be visible in the evidence pack.

Be strict and skeptical. It is a valid and common outcome to mark fields false. Mark false when the answer overreaches. If a field genuinely cannot be determined from the supplied material, use null -- never guess.

Output ONLY a single JSON object (no markdown fence) with exactly these keys:
{{"correct_conclusion": true|false|null, "correct_scope": true|false|null, "authority_boundary_preserved": true|false|null, "unsupported_claim": true|false|null, "rationale": "<2-4 sentences>"}}
"""

NON_AUTHORITATIVE_EVIDENCE = frozenset(
    {
        "DEV_MEMORY_PILOT.md",
        "README.md",
        "ROADMAP.md",
        "CHANGELOG.md",
    }
)

#: Expected evidence family per question, copied from
#: ``DEV_MEMORY_CONTROLLED_FIXTURE.md`` (the frozen evaluation target). It is
#: joined with the independently derived key's ``supporting_sources`` so the
#: grader can verify the claims an agent is expected to make for that question.
FIXTURE_EVIDENCE_FAMILIES: dict[str, tuple[str, ...]] = {
    "Q01": (
        "REFACTOR_LANGGRAPH.md",
        "REFACTOR_MICROSOFT_AGENT_FRAMEWORK.md",
        "REFACTOR_CREWAI.md",
        "REFACTOR_LETTA.md",
    ),
    "Q02": (
        "REFACTOR_OPENAI_AGENTS_SDK.md",
        "REFACTOR_MICROSOFT_AGENT_FRAMEWORK.md",
        "REFACTOR_SYNTHESIS.md",
    ),
    "Q03": (
        "REFACTOR_CREWAI.md",
        "REFACTOR_OPENHANDS.md",
        "REFACTOR_LETTA.md",
        "protocol/.agents/standards/context/MEMORY_SYSTEM.md",
    ),
    "Q04": ("REFACTOR_OPENHANDS.md", "REFACTOR_LETTA.md"),
    "Q05": ("REFACTOR_CREWAI.md",),
    "Q06": ("REFACTOR_SWE_AGENT.md",),
    "Q07": ("REFACTOR_GOOGLE_ADK.md", "REFACTOR_SYNTHESIS.md"),
    "Q08": (
        "REFACTOR_OPENAI_AGENTS_SDK.md",
        "REFACTOR_OPENHANDS.md",
        "REFACTOR_GOOGLE_ADK.md",
    ),
    "Q09": (
        "REFACTOR_LANGGRAPH.md",
        "REFACTOR_MICROSOFT_AGENT_FRAMEWORK.md",
        "REFACTOR_CREWAI.md",
        "REFACTOR_LETTA.md",
    ),
    "Q10": ("REFACTOR_OPENHANDS.md", "REFACTOR_LETTA.md"),
    "Q11": ("REFACTOR_SYNTHESIS.md", "REFACTOR_MATRIX.md"),
    "Q12": ("REFACTOR_SYNTHESIS.md", "REFACTOR_MATRIX.md"),
}

#: Fixed governance references joined into every question's evidence pack, so a
#: correct answer that grounds a claim in the repository's own lifecycle /
#: authority documents is not marked unsupported for lack of that document.
GOVERNANCE_EVIDENCE = (
    "docs/rfc/75-change-lifecycle.md",
    "docs/adr/15-change-lifecycle-continuity.md",
    "docs/adr/16-change-lifecycle-authority.md",
    "docs/plans/180-comparative-architecture-refactor-study.md",
    "protocol/.agents/standards/context/MEMORY_SYSTEM.md",
)

EVIDENCE_TOTAL_CAP = 120_000
EVIDENCE_PER_FILE_CAP = 9_000


def is_excluded_evidence(rel: str) -> bool:
    """Derived indexes, entry points and the memory surface are not evidence."""
    if rel in NON_AUTHORITATIVE_EVIDENCE:
        return True
    name = Path(rel).name
    if name == "INDEX.md":
        return True
    return False


@dataclass
class HeadlessRun:
    """Result of one headless DeepSeek Harness run."""

    events: list[dict[str, Any]] = field(default_factory=list)
    final_text: str | None = None
    stderr: str = ""
    returncode: int | None = None
    timed_out: bool = False
    elapsed: float = 0.0
    session_id: str | None = None
    turn_end: dict[str, Any] | None = None
    usage: dict[str, int] = field(default_factory=dict)
    error: str | None = None
    raw_stdout: str = ""


@dataclass
class Instrumentation:
    """Runner instrumentation derived from the agent run events."""

    file_open_events: list[str] = field(default_factory=list)
    search_events: list[str] = field(default_factory=list)
    rehydration_events: list[str] = field(default_factory=list)
    opened: list[str] = field(default_factory=list)
    shell_commands: list[str] = field(default_factory=list)
    tool_calls: list[dict[str, Any]] = field(default_factory=list)
    observed_tools: set[str] = field(default_factory=set)
    tool_events: list[dict[str, Any]] = field(default_factory=list)
    failed_reads: list[str] = field(default_factory=list)
    out_of_workspace_calls: list[dict[str, Any]] = field(default_factory=list)


# ---------------------------------------------------------------------------
# Pure helpers
# ---------------------------------------------------------------------------


def parse_ndjson(text: str) -> list[dict[str, Any]]:
    """Parse newline-delimited JSON objects, ignoring anything that is not one."""
    events: list[dict[str, Any]] = []
    for line in text.splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            event = json.loads(line)
        except json.JSONDecodeError:
            continue
        if isinstance(event, dict):
            events.append(event)
    return events


def summarize_usage(events: list[dict[str, Any]]) -> dict[str, int]:
    """Sum the token usage reported by ``status/step_end`` events."""
    totals: dict[str, int] = {}
    for event in events:
        if event.get("type") != "status" or event.get("phase") != "step_end":
            continue
        usage = event.get("usage")
        if not isinstance(usage, dict):
            continue
        for key, value in usage.items():
            if isinstance(value, int):
                totals[key] = totals.get(key, 0) + value
    return totals


def extract_final_text(events: list[dict[str, Any]]) -> str | None:
    """Return the last ``final`` event text, if any."""
    for event in reversed(events):
        if event.get("type") == "final":
            text = event.get("text")
            return text if isinstance(text, str) else None
    return None


def extract_session_id(events: list[dict[str, Any]]) -> str | None:
    for event in events:
        if event.get("type") == "session":
            session_id = event.get("sessionId")
            return session_id if isinstance(session_id, str) else None
    return None


def extract_turn_end(events: list[dict[str, Any]]) -> dict[str, Any] | None:
    for event in reversed(events):
        if event.get("type") == "status" and event.get("phase") == "turn_end":
            reason = event.get("reason")
            return reason if isinstance(reason, dict) else None
    return None


def to_workspace_rel(path: str | None, workspace: Path) -> str | None:
    """Normalize a tool path to a workspace-relative POSIX path, or None."""
    if not path or not isinstance(path, str):
        return None
    raw = Path(path)
    try:
        resolved = (workspace / raw).resolve() if not raw.is_absolute() else raw.resolve()
        return resolved.relative_to(workspace.resolve()).as_posix()
    except (OSError, ValueError):
        return None


_SHELL_SEARCH = re.compile(
    r"\b(grep|rg|Select-String|findstr|Get-ChildItem|gci|dir|ls|find)\b", re.IGNORECASE
)
_SHELL_READ = re.compile(r"\b(Get-Content|gc|cat|type|more|head|tail)\b", re.IGNORECASE)
_SHELL_PATH = re.compile(
    r"[\"']([^\"'\r\n]*\.(?:md|py|json|ya?ml|txt|toml|cfg|ini))[\"']"
    r"|([A-Za-z0-9_][A-Za-z0-9_./\\-]*\.(?:md|py|json|ya?ml|txt|toml|cfg|ini))",
    re.IGNORECASE,
)


def infer_shell_paths(command: str, workspace: Path) -> list[str]:
    """Best-effort extraction of workspace files referenced by a shell command.

    Shell tools are disabled by the frozen tool policy, so this is only a
    defence-in-depth mapping if the policy ever fails. It is reported as a
    heuristic in the trace and never presented as a precise measurement.
    """
    found: list[str] = []
    seen: set[str] = set()
    for match in _SHELL_PATH.finditer(command):
        token = match.group(1) or match.group(2) or ""
        rel = to_workspace_rel(token.strip("\"'"), workspace)
        if rel is None:
            continue
        if (workspace / rel).is_file() and rel not in seen:
            seen.add(rel)
            found.append(rel)
    return found


def summarize_tool_calls(events: list[dict[str, Any]], workspace: Path) -> list[dict[str, Any]]:
    """Build a compact, JSON-safe record of every tool call the agent made."""
    statuses: dict[str, str] = {}
    for event in events:
        if event.get("type") == "tool_result":
            call_id = event.get("callId")
            if isinstance(call_id, str):
                statuses[call_id] = str(event.get("status"))
    calls: list[dict[str, Any]] = []
    for event in events:
        if event.get("type") != "tool_call":
            continue
        tool = event.get("tool")
        payload = event.get("input")
        if not isinstance(payload, dict):
            payload = {}
        summary: dict[str, Any] = {"tool": str(tool)}
        if tool == "read":
            summary["path"] = to_workspace_rel(payload.get("file_path"), workspace) or payload.get("file_path")
        elif tool in ("grep", "glob"):
            summary["query"] = payload.get("pattern")
            if payload.get("path"):
                summary["path"] = to_workspace_rel(payload.get("path"), workspace) or payload.get("path")
        elif tool in ("pwsh", "bash"):
            summary["command"] = str(payload.get("command", ""))[:300]
        elif tool == "skill":
            summary["skill"] = payload.get("name")
        else:
            summary["input"] = json.dumps(payload, ensure_ascii=False)[:200]
        call_id = event.get("callId")
        if isinstance(call_id, str):
            summary["status"] = statuses.get(call_id)
        calls.append(summary)
    return calls


def map_instrumentation(events: list[dict[str, Any]], workspace: Path) -> Instrumentation:
    """Map DeepSeek Harness run events onto the runner's instrumentation events.

    ``file_open`` counts only references the harness reports as completed reads
    (a failed read is a retrieval attempt, recorded separately as a failed read,
    not an opened file). Shell tools are disabled by the frozen policy; their
    mapping is retained only as defence-in-depth.
    """
    inst = Instrumentation()
    inst.tool_calls = summarize_tool_calls(events, workspace)
    statuses: dict[str, str] = {}
    for event in events:
        if event.get("type") == "tool_result":
            call_id = event.get("callId")
            if isinstance(call_id, str):
                statuses[call_id] = str(event.get("status"))

    def _record_outside(tool: str, raw_path: Any, status: str | None) -> None:
        if isinstance(raw_path, str) and raw_path:
            inst.out_of_workspace_calls.append(
                {"tool": tool, "path": raw_path, "status": status}
            )

    for event in events:
        if event.get("type") != "tool_call":
            continue
        tool = event.get("tool")
        payload = event.get("input")
        if not isinstance(payload, dict):
            payload = {}
        call_id = event.get("callId")
        status = statuses.get(call_id) if isinstance(call_id, str) else None
        if isinstance(tool, str):
            inst.observed_tools.add(tool)
            inst.tool_events.append({"tool": tool, "status": status})

        if tool in ("read", "read_image"):
            raw_path = payload.get("file_path")
            rel = to_workspace_rel(raw_path, workspace)
            if rel is None:
                _record_outside(str(tool), raw_path, status)
                path = str(raw_path or "")
            else:
                path = rel
            if status in (None, "completed"):
                inst.file_open_events.append(path)
                if rel:
                    inst.opened.append(rel)
                    if rel in SOURCE_ARTIFACTS:
                        inst.rehydration_events.append(rel)
            else:
                inst.failed_reads.append(path)
        elif tool in ("grep", "glob"):
            raw_query = payload.get("pattern")
            query = (
                raw_query
                if raw_query is not None
                else json.dumps(payload, ensure_ascii=False)[:200]
            )
            inst.search_events.append(str(query))
            raw_path = payload.get("path")
            rel = to_workspace_rel(raw_path, workspace)
            if raw_path and rel is None:
                _record_outside(str(tool), raw_path, status)
            if tool == "grep" and rel in SOURCE_ARTIFACTS:
                inst.rehydration_events.append(rel)
        elif tool in ("pwsh", "bash"):
            command = str(payload.get("command", ""))
            inst.shell_commands.append(command[:500])
            # Shell tools are frozen out; only a completed call could have done
            # retrieval at all, and a failed attempt to reach a non-existent
            # tool must not be counted as a search or a file open.
            if status in (None, "completed"):
                if _SHELL_SEARCH.search(command):
                    inst.search_events.append(command[:300])
                elif _SHELL_READ.search(command):
                    inst.file_open_events.append(command[:300])
                for rel in infer_shell_paths(command, workspace):
                    inst.opened.append(rel)
                    if rel in SOURCE_ARTIFACTS:
                        inst.rehydration_events.append(rel)
    return inst


def build_task_prompt(question: str) -> str:
    """The single task prompt used identically in both conditions."""
    return TASK_TEMPLATE.format(question=question.strip())


def build_grader_prompt(
    question: str,
    expected_key: dict[str, Any] | None,
    answer: str,
    evidence: str,
) -> str:
    return GRADER_TEMPLATE.format(
        question=question.strip(),
        expected_key=json.dumps(expected_key, ensure_ascii=False, indent=2)
        if expected_key
        else "(no expected key available)",
        answer=answer,
        evidence=evidence or "(no evidence pack available)",
    )


def parse_grader_json(text: str | None) -> dict[str, Any] | None:
    """Extract the single JSON object a grader was asked to return."""
    if not text:
        return None
    stripped = text.strip()
    candidates: list[str] = []
    if stripped.startswith("{"):
        candidates.append(stripped)
    fenced = re.search(r"```(?:json)?\s*(\{.*?\})\s*```", stripped, re.DOTALL)
    if fenced:
        candidates.append(fenced.group(1))
    start = stripped.find("{")
    end = stripped.rfind("}")
    if start != -1 and end > start:
        candidates.append(stripped[start : end + 1])
    for candidate in candidates:
        try:
            parsed = json.loads(candidate)
        except json.JSONDecodeError:
            continue
        if isinstance(parsed, dict):
            return parsed
    return None


def coerce_bool(value: Any) -> bool | None:
    """Only real booleans count; anything else remains unknown."""
    return value if isinstance(value, bool) else None


_CITATION_TOKEN = re.compile(
    r"[A-Za-z0-9_][A-Za-z0-9_./\\:-]*\.(?:md|py|json|ya?ml|txt|toml|cfg|ini)",
    re.IGNORECASE,
)


def extract_citations(answer: str, workspace: Path, opened: list[str]) -> list[str]:
    """Resolve repository-relative paths cited by the answer.

    A citation counts only if it resolves to an existing file in the workspace
    (relative path or the basename of a file the agent opened).
    """
    opened_basenames: dict[str, list[str]] = {}
    for rel in opened:
        opened_basenames.setdefault(Path(rel).name, []).append(rel)
    if workspace.is_dir():
        try:
            root_files = {
                path.name: path.relative_to(workspace).as_posix()
                for path in workspace.iterdir()
                if path.is_file()
            }
        except OSError:
            root_files = {}
    else:
        root_files = {}

    cited: list[str] = []
    seen: set[str] = set()
    for match in _CITATION_TOKEN.finditer(answer):
        token = match.group(0).strip("`.,;:()[]'\"<>")
        normalized = token.replace("\\", "/").lstrip("./")
        candidates: list[str] = []
        candidate_path = workspace / normalized
        try:
            if candidate_path.is_file():
                candidates.append(normalized)
        except OSError:
            pass
        basename = Path(normalized).name
        if basename in root_files:
            candidates.append(root_files[basename])
        candidates.extend(opened_basenames.get(basename, []))
        for candidate in candidates:
            if candidate not in seen:
                seen.add(candidate)
                cited.append(candidate)
    return cited


def compute_provenance(
    answer: str | None, workspace: Path, opened: list[str]
) -> tuple[bool | None, list[str], list[str]]:
    """Deterministically decide ``provenance_present``.

    Present when the answer cites at least one existing repository file that the
    agent actually opened during the run. The derived memory surface cannot
    serve as source provenance.
    """
    if not answer:
        return None, [], []
    cited = extract_citations(answer, workspace, opened)
    allowed_opened = {rel for rel in opened if rel != MEMORY_SURFACE}
    supported = [rel for rel in cited if rel in allowed_opened and rel != MEMORY_SURFACE]
    return bool(supported), cited, supported


def workspace_tree_digest(workspace: Path) -> str | None:
    """SHA-256 over sorted (relative path, content hash) pairs.

    Used as an integrity probe: the digest must not change across the 12
    questions of one condition, which shows the agent did not mutate the
    workspace between runs.
    """
    if not workspace.is_dir():
        return None
    digest = hashlib.sha256()
    try:
        paths = sorted(path for path in workspace.rglob("*") if path.is_file())
    except OSError:
        return None
    for path in paths:
        try:
            rel = path.relative_to(workspace).as_posix()
            content = path.read_bytes()
        except OSError:
            continue
        digest.update(rel.encode("utf-8"))
        digest.update(hashlib.sha256(content).hexdigest().encode("ascii"))
    return digest.hexdigest()


def gradable_fields(grader: dict[str, Any] | None) -> dict[str, bool | None]:
    """Pick the four judged fields, leaving unknown values as None."""
    if not grader:
        return {
            "correct_conclusion": None,
            "correct_scope": None,
            "authority_boundary_preserved": None,
            "unsupported_claim": None,
        }
    return {
        "correct_conclusion": coerce_bool(grader.get("correct_conclusion")),
        "correct_scope": coerce_bool(grader.get("correct_scope")),
        "authority_boundary_preserved": coerce_bool(grader.get("authority_boundary_preserved")),
        "unsupported_claim": coerce_bool(grader.get("unsupported_claim")),
    }


# ---------------------------------------------------------------------------
# Expected-answer key and fixed evidence pack
# ---------------------------------------------------------------------------

REQUIRED_KEY_FIELDS = ("question", "expected_conclusion", "expected_scope", "supporting_sources")


def validate_expected_key(key: dict[str, Any] | None) -> list[str]:
    """Return the list of problems that make the key unusable for grading."""
    problems: list[str] = []
    if not isinstance(key, dict):
        return ["expected key is not a JSON object"]
    questions = key.get("questions")
    if not isinstance(questions, dict):
        return ["expected key has no 'questions' object"]
    for qid in [f"Q{i:02d}" for i in range(1, 13)]:
        entry = questions.get(qid)
        if not isinstance(entry, dict):
            problems.append(f"{qid}: missing")
            continue
        for field in REQUIRED_KEY_FIELDS:
            value = entry.get(field)
            if field == "supporting_sources":
                if not isinstance(value, list) or not value:
                    problems.append(f"{qid}: supporting_sources missing or empty")
            elif not isinstance(value, str) or not value.strip():
                problems.append(f"{qid}: {field} missing or empty")
    return problems


def expected_key_for(key: dict[str, Any] | None, question_id: str) -> dict[str, Any] | None:
    if not key:
        return None
    questions = key.get("questions")
    if isinstance(questions, dict):
        entry = questions.get(question_id)
        if isinstance(entry, dict):
            return entry
    return None


def build_fixed_evidence(
    expected_entry: dict[str, Any] | None,
    evidence_dir: Path,
    question_id: str | None = None,
) -> tuple[str, list[str], list[str]]:
    """Read the fixed per-question evidence pack from a pristine source tree.

    The pack is the union of the question's expected evidence family (frozen in
    the fixture), the independently derived key's ``supporting_sources`` and the
    fixed governance references. It depends only on the question, never on the
    condition or on what the agent happened to open, so every answer to a
    question is graded against identical evidence. Derived indexes, entry points
    and the memory surface are excluded; secondary synthesis/matrix summaries are
    included as evidence but remain non-authoritative under the rubric.
    """
    if not expected_entry:
        return "", [], []
    candidates: list[str] = []
    if question_id:
        candidates.extend(FIXTURE_EVIDENCE_FAMILIES.get(question_id, ()))
    candidates.extend(str(source) for source in expected_entry.get("supporting_sources", []))
    candidates.extend(GOVERNANCE_EVIDENCE)
    sources: list[str] = []
    for rel in candidates:
        if is_excluded_evidence(rel):
            continue
        if rel not in sources:
            sources.append(rel)
    included: list[str] = []
    missing: list[str] = []
    chunks: list[str] = []
    total = 0
    for rel in sources:
        path = evidence_dir / rel
        try:
            if not path.is_file():
                missing.append(rel)
                continue
            text = path.read_text(encoding="utf-8", errors="replace")
        except OSError:
            missing.append(rel)
            continue
        if len(text) > EVIDENCE_PER_FILE_CAP:
            text = text[:EVIDENCE_PER_FILE_CAP] + "\n[... truncated ...]"
        chunk = f"--- {rel} ---\n{text}"
        if total + len(chunk) > EVIDENCE_TOTAL_CAP:
            missing.append(rel + " (omitted: evidence cap)")
            continue
        chunks.append(chunk)
        included.append(rel)
        total += len(chunk)
    return "\n\n".join(chunks), included, missing


# ---------------------------------------------------------------------------
# Process execution
# ---------------------------------------------------------------------------


def resolve_dsh_cli() -> Path:
    """Locate the local DeepSeek Harness CLI."""
    for key in ("ARGENTOS_DSH_CLI", "DSH_CLI_PATH"):
        value = os.environ.get(key)
        if value and Path(value).is_file():
            return Path(value)
    which = shutil.which("dsh")
    if which:
        return Path(which)
    default = Path(DEFAULT_DSH_CLI)
    if default.is_file():
        return default
    raise RuntimeError(
        "dsh CLI not found: set ARGENTOS_DSH_CLI to the local "
        "DeepSeek Harness `dsh` executable (see the install's resources/runtime/cli/bin/dsh.cmd)"
    )


def build_child_env(dsh_home: Path) -> dict[str, str]:
    """Environment for the agent/grader process.

    The runner's ``ARGENTOS_*`` variables (including the condition label) and
    the harness's own ``DSH_*`` session variables are removed so the agent has
    no explicit condition hint. Only the credential and the dedicated
    experiment home are supplied.
    """
    env = {
        key: value
        for key, value in os.environ.items()
        if not key.upper().startswith(("ARGENTOS_", "DSH_"))
    }
    env["DSH_HOME"] = str(dsh_home)
    env["DSH_PERMISSION_MODE"] = "read-only"
    return env


def kill_process_tree(proc: subprocess.Popen[str]) -> None:
    """Kill a process and all of its descendants.

    A plain ``proc.kill()`` on the ``.cmd`` launcher leaves the harness
    executable alive holding the stdout pipe, which would stall the runner (the
    frozen runner has no timeout of its own).
    """
    if os.name == "nt":
        subprocess.run(
            ["taskkill", "/F", "/T", "/PID", str(proc.pid)],
            capture_output=True,
            check=False,
        )
    else:
        try:
            proc.kill()
        except OSError:
            pass


def run_process(
    command: list[str],
    input_text: str,
    *,
    cwd: Path,
    env: dict[str, str],
    timeout: float,
) -> tuple[str, str, int | None, bool]:
    """Run a child process with a whole-tree timeout, returning captured text."""
    proc = subprocess.Popen(
        command,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        cwd=str(cwd),
        env=env,
        text=True,
        encoding="utf-8",
        errors="replace",
    )
    try:
        stdout, stderr = proc.communicate(input_text, timeout=timeout)
        return stdout or "", stderr or "", proc.returncode, False
    except subprocess.TimeoutExpired:
        kill_process_tree(proc)
        try:
            stdout, stderr = proc.communicate(timeout=30)
        except subprocess.TimeoutExpired:  # pragma: no cover - defensive
            stdout, stderr = "", ""
        return stdout or "", stderr or "", proc.returncode, True


def run_headless(
    task_text: str,
    cwd: Path,
    *,
    timeout: float,
    child_env: dict[str, str],
    dsh_cli: Path,
    tool_policy: str = TOOL_POLICY_PATCH,
) -> HeadlessRun:
    """Run one fresh ``dsh --profile headless --json`` process."""
    run = HeadlessRun()
    dsh_home = Path(child_env["DSH_HOME"])
    patch_path = dsh_home / "experiment-tool-policy.patch.yml"
    patch_path.write_text(tool_policy, encoding="utf-8")
    command = [
        str(dsh_cli),
        "--profile",
        "headless",
        "--patch",
        str(patch_path),
        "--json",
        "-",
    ]
    started = time.perf_counter()
    try:
        stdout, stderr, returncode, timed_out = run_process(
            command, task_text, cwd=cwd, env=child_env, timeout=timeout
        )
        run.returncode = returncode
        run.stderr = stderr
        run.timed_out = timed_out
        run.raw_stdout = stdout
        run.events = parse_ndjson(stdout)
    except OSError as exc:
        run.error = f"os_error={exc}"
    finally:
        run.elapsed = time.perf_counter() - started
    if run.timed_out:
        run.error = f"timeout after {timeout:.0f}s"
    elif run.error is None:
        run.final_text = extract_final_text(run.events)
        run.session_id = extract_session_id(run.events)
        run.turn_end = extract_turn_end(run.events)
        run.usage = summarize_usage(run.events)
        if run.turn_end and run.turn_end.get("kind") == "error":
            run.error = "agent_turn_end_error"
        elif run.final_text is None and run.returncode not in (0, None):
            run.error = f"agent_exit={run.returncode}"
    return run


def run_grader(
    prompt: str,
    *,
    timeout: float,
    child_env: dict[str, str],
    dsh_cli: Path,
) -> HeadlessRun:
    """Run the grader in an empty scratch directory (it cannot see a condition)."""
    scratch = Path(tempfile.mkdtemp(prefix="argentos-dev-memory-judge-"))
    try:
        return run_headless(
            prompt,
            scratch,
            timeout=timeout,
            child_env=child_env,
            dsh_cli=dsh_cli,
            tool_policy=GRADER_TOOL_POLICY_PATCH,
        )
    finally:
        shutil.rmtree(scratch, ignore_errors=True)


def make_dsh_home() -> Path:
    """A fresh, disposable DSH home per process, so sessions never leak across questions."""
    return Path(tempfile.mkdtemp(prefix="argentos-dev-memory-dsh-home-"))


def prepare_agent_workspace(runner_workspace: Path) -> tuple[Path, Path]:
    """Copy the condition workspace to a neutral path and return it.

    The frozen runner names its temporary directory ``argentos-memory-<condition>-*``
    and the harness reports the absolute cwd to the model, so running directly in
    the runner workspace leaks the condition label. The copy has identical
    contents and a neutral name; it is removed by the caller.
    """
    root = Path(tempfile.mkdtemp(prefix="bench-"))
    destination = root / "repo"
    shutil.copytree(
        runner_workspace,
        destination,
        ignore=shutil.ignore_patterns(".git", "__pycache__", ".mypy_cache"),
    )
    return destination, root


# ---------------------------------------------------------------------------
# Trace, calibration and main
# ---------------------------------------------------------------------------


def write_trace(trace_dir: Path | None, condition: str, question_id: str, payload: dict[str, Any]) -> Path | None:
    if trace_dir is None:
        return None
    target_dir = trace_dir / condition.lower()
    target_dir.mkdir(parents=True, exist_ok=True)
    target = target_dir / f"{question_id}.json"
    target.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return target


def write_raw_ndjson(
    trace_dir: Path | None, condition: str, question_id: str, suffix: str, text: str
) -> dict[str, Any] | None:
    """Persist the raw NDJSON run stream for audit; return its integrity data."""
    if trace_dir is None:
        return None
    target_dir = trace_dir / condition.lower()
    target_dir.mkdir(parents=True, exist_ok=True)
    target = target_dir / f"{question_id}.{suffix}.ndjson"
    data = text or ""
    encoded = data.encode("utf-8")
    target.write_text(data, encoding="utf-8")
    return {"path": str(target), "sha256": hashlib.sha256(encoded).hexdigest(), "bytes": len(encoded)}


def file_sha256(path: Path) -> str | None:
    try:
        return hashlib.sha256(path.read_bytes()).hexdigest()
    except OSError:
        return None


def emit(event: dict[str, Any]) -> None:
    sys.stdout.write(json.dumps(event, ensure_ascii=False) + "\n")
    sys.stdout.flush()


def read_expected_key(path: str | None) -> dict[str, Any] | None:
    if not path:
        return None
    try:
        data = json.loads(Path(path).read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return None
    return data if isinstance(data, dict) else None


def configuration_problems() -> tuple[list[str], dict[str, Any]]:
    """Validate everything the executor needs before touching a workspace."""
    problems: list[str] = []
    info: dict[str, Any] = {}
    if not os.environ.get("DEEPSEEK_API_KEY"):
        problems.append("DEEPSEEK_API_KEY is not set in the executor environment")
    try:
        info["dsh_cli"] = str(resolve_dsh_cli())
    except RuntimeError as exc:
        problems.append(str(exc))
        info["dsh_cli"] = None
    key = read_expected_key(os.environ.get("ARGENTOS_EXPECTED_KEY"))
    key_problems = validate_expected_key(key)
    problems.extend(f"expected key: {problem}" for problem in key_problems)
    info["expected_key_entries"] = len((key or {}).get("questions", {})) if isinstance(key, dict) else 0
    evidence_dir = os.environ.get("ARGENTOS_EVIDENCE_DIR")
    if not evidence_dir or not Path(evidence_dir).is_dir():
        problems.append("ARGENTOS_EVIDENCE_DIR is not set or is not a directory")
        info["evidence_dir"] = evidence_dir
    else:
        info["evidence_dir"] = evidence_dir
    return problems, info


def self_check() -> int:
    """Validate the executor's configuration without touching a workspace."""
    problems, info = configuration_problems()
    payload = {
        "executor": "tools/dev_memory_agent_executor.py",
        "problems": problems,
        "model_label": os.environ.get("ARGENTOS_MODEL_LABEL", "unknown"),
        "agent_timeout_seconds": os.environ.get("ARGENTOS_AGENT_TIMEOUT", str(DEFAULT_AGENT_TIMEOUT)),
        "judge_timeout_seconds": os.environ.get("ARGENTOS_JUDGE_TIMEOUT", str(DEFAULT_JUDGE_TIMEOUT)),
        "trace_dir": os.environ.get("ARGENTOS_TRACE_DIR"),
        "tool_policy_sha256": hashlib.sha256(TOOL_POLICY_PATCH.encode("utf-8")).hexdigest(),
        **info,
    }
    sys.stdout.write(json.dumps(payload, indent=2) + "\n")
    if problems:
        sys.stderr.write("executor self-check failed: " + "; ".join(problems) + "\n")
        return 2
    return 0


def calibration_answers(entry: dict[str, Any]) -> dict[str, str]:
    """Synthetic answers used to expose a broken grader before a benchmark run."""
    sources = ", ".join(str(source) for source in entry.get("supporting_sources", []))
    return {
        "key_consistent": (
            f"CONCLUSION: {entry.get('expected_conclusion', '')}\n"
            f"SCOPE: {entry.get('expected_scope', '')}\n"
            f"EVIDENCE: {sources}\n"
            "AUTHORITY: the historical comparative studies are the source evidence; "
            "no derived summary or memory note is treated as authority.\n"
            "UNSUPPORTED: none"
        ),
        "overgeneralized": (
            "CONCLUSION: The comparative study proves the universal Unit/Relationship/State "
            "ontology and a single runtime continuity model should be adopted across every "
            "ARgentOS layer immediately.\n"
            "SCOPE: applies to every layer and every adopter without exception.\n"
            "EVIDENCE: general convergence of the studies.\n"
            "AUTHORITY: the comparative synthesis is the definitive authority.\n"
            "UNSUPPORTED: none"
        ),
        "memory_as_authority": (
            "CONCLUSION: According to DEV_MEMORY_PILOT.md, which is the authoritative DEV "
            "Memory source, the question is settled and no other evidence is needed.\n"
            "SCOPE: all memory work.\n"
            "EVIDENCE: DEV_MEMORY_PILOT.md (DEV-MEM-004).\n"
            "AUTHORITY: DEV_MEMORY_PILOT.md is authoritative and supersedes the individual studies.\n"
            "UNSUPPORTED: none"
        ),
        "uncited": (
            "CONCLUSION: Yes, definitely. The conclusion is settled and universally applicable.\n"
            "SCOPE: everywhere, for every ARgentOS layer and every adopter.\n"
            "EVIDENCE: none.\n"
            "AUTHORITY: none needed.\n"
            "UNSUPPORTED: none"
        ),
        "synthesis_cited": (
            f"CONCLUSION: {entry.get('expected_conclusion', '')}\n"
            f"SCOPE: {entry.get('expected_scope', '')}\n"
            "EVIDENCE: REFACTOR_SYNTHESIS.md and REFACTOR_MATRIX.md (secondary summaries), "
            f"{sources}\n"
            "AUTHORITY: the individual comparative studies are the source evidence; the "
            "synthesis and matrix are secondary summaries and are not treated as authority.\n"
            "UNSUPPORTED: none"
        ),
    }


def calibration_verdict(results: dict[str, dict[str, Any]]) -> list[str]:
    """Derive the expected discrimination flags from a calibration run."""
    flags: list[str] = []
    key_result = results.get("key_consistent", {}).get("parsed") or {}
    over_result = results.get("overgeneralized", {}).get("parsed") or {}
    memory_result = results.get("memory_as_authority", {}).get("parsed") or {}
    uncited_result = results.get("uncited", {}).get("parsed") or {}
    synthesis_result = results.get("synthesis_cited", {}).get("parsed") or {}
    if key_result.get("correct_conclusion") is not True:
        flags.append("grader did not accept the key-consistent answer")
    if key_result.get("correct_scope") is not True:
        flags.append("grader did not accept the key-consistent scope")
    if over_result.get("correct_scope") is not False and over_result.get("unsupported_claim") is not True:
        flags.append("grader did not penalize the over-generalized answer")
    if memory_result.get("authority_boundary_preserved") is not False:
        flags.append("grader did not penalize memory-as-authority")
    if (
        uncited_result.get("unsupported_claim") is not True
        and uncited_result.get("correct_conclusion") is not False
    ):
        flags.append("grader did not penalize the uncited answer")
    if synthesis_result.get("correct_conclusion") is not True:
        flags.append("grader did not accept a correct answer that cites the secondary summaries")
    if synthesis_result.get("unsupported_claim") is not False:
        flags.append("grader marked a correct summary-backed answer as unsupported")
    return flags


def calibrate() -> int:
    """Grade synthetic answers with the fixed grader, without an agent run."""
    problems, info = configuration_problems()
    if problems:
        sys.stderr.write("executor calibration failed: " + "; ".join(problems) + "\n")
        return 2
    question_id = os.environ.get("ARGENTOS_CALIBRATION_QID", "Q11")
    key = read_expected_key(os.environ.get("ARGENTOS_EXPECTED_KEY"))
    entry = expected_key_for(key, question_id)
    if not entry:
        sys.stderr.write(f"executor calibration failed: no key entry for {question_id}\n")
        return 2
    evidence_dir = Path(os.environ["ARGENTOS_EVIDENCE_DIR"])
    evidence, included, missing = build_fixed_evidence(entry, evidence_dir, question_id)
    question = str(entry.get("question", ""))
    dsh_cli = Path(info["dsh_cli"])
    judge_timeout = float(os.environ.get("ARGENTOS_JUDGE_TIMEOUT", DEFAULT_JUDGE_TIMEOUT))
    results: dict[str, dict[str, Any]] = {}
    for name, answer in calibration_answers(entry).items():
        judge_home = make_dsh_home()
        try:
            run = run_grader(
                build_grader_prompt(question, entry, answer, evidence),
                timeout=judge_timeout,
                child_env=build_child_env(judge_home),
                dsh_cli=dsh_cli,
            )
        finally:
            shutil.rmtree(judge_home, ignore_errors=True)
        results[name] = {
            "answer": answer[:600],
            "parsed": parse_grader_json(run.final_text),
            "raw_final": (run.final_text or "")[:1500],
            "error": run.error,
            "elapsed_seconds": round(run.elapsed, 2),
        }
    flags = calibration_verdict(results)
    payload = {
        "schema": CALIBRATION_SCHEMA,
        "question_id": question_id,
        "evidence_included": included,
        "evidence_missing": missing,
        "results": results,
        "discrimination_flags": flags,
        "tool_policy_sha256": hashlib.sha256(TOOL_POLICY_PATCH.encode("utf-8")).hexdigest(),
    }
    trace_dir = os.environ.get("ARGENTOS_TRACE_DIR")
    if trace_dir:
        target = Path(trace_dir) / "calibration.json"
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    sys.stdout.write(json.dumps(payload, indent=2, ensure_ascii=False) + "\n")
    return 0


def main(argv: list[str] | None = None) -> int:
    argv = list(sys.argv[1:] if argv is None else argv)
    if argv == ["--self-check"]:
        return self_check()
    if argv == ["--calibrate"]:
        return calibrate()
    if argv:
        sys.stderr.write(
            "usage: dev_memory_agent_executor.py [--self-check|--calibrate]; "
            "the question is read from stdin\n"
        )
        return 2

    question = sys.stdin.read().strip()
    if not question:
        sys.stderr.write("executor: empty question on stdin\n")
        return 2

    condition = os.environ.get("ARGENTOS_MEMORY_MODE", "UNKNOWN").strip().upper()
    question_id = os.environ.get("ARGENTOS_QUESTION_ID", "UNKNOWN").strip()
    runner_workspace = Path(os.environ.get("ARGENTOS_WORKSPACE") or os.getcwd())
    try:
        runner_workspace = runner_workspace.resolve()
    except OSError:
        pass

    problems, config = configuration_problems()
    if problems:
        sys.stderr.write("executor: refusing to run: " + "; ".join(problems) + "\n")
        return 2
    dsh_cli = Path(config["dsh_cli"])
    expected_key = read_expected_key(os.environ.get("ARGENTOS_EXPECTED_KEY"))
    expected_entry = expected_key_for(expected_key, question_id)
    if expected_entry is None:
        sys.stderr.write(f"executor: no expected key entry for {question_id}\n")
        return 2
    evidence_dir = Path(os.environ["ARGENTOS_EVIDENCE_DIR"])

    trace_dir_value = os.environ.get("ARGENTOS_TRACE_DIR")
    trace_dir = Path(trace_dir_value) if trace_dir_value else None
    agent_timeout = float(os.environ.get("ARGENTOS_AGENT_TIMEOUT", DEFAULT_AGENT_TIMEOUT))
    judge_timeout = float(os.environ.get("ARGENTOS_JUDGE_TIMEOUT", DEFAULT_JUDGE_TIMEOUT))
    base_commit = os.environ.get("ARGENTOS_BASE_COMMIT", "unknown")
    model_label = os.environ.get("ARGENTOS_MODEL_LABEL", "unknown")

    agent_workspace: Path | None = None

    def fail(reason: str, extra: dict[str, Any] | None = None) -> int:
        """Record an auditable integrity-failure trace, then refuse the run."""
        payload = {
            "schema": TRACE_SCHEMA,
            "condition": condition,
            "question_id": question_id,
            "question": question,
            "integrity_failure": reason,
            "run": {"run_id": os.environ.get("ARGENTOS_RUN_ID", "unknown")},
            "workspace": {
                "runner": str(runner_workspace),
                "agent": str(agent_workspace) if agent_workspace else None,
            },
            "recorded_at": time.strftime("%Y-%m-%dT%H:%M:%S"),
            "extra": extra or {},
        }
        write_trace(trace_dir, condition, question_id, payload)
        sys.stderr.write("executor: INTEGRITY FAILURE: " + reason + "\n")
        return 2

    if condition not in {"CONTROL", "TREATMENT"}:
        return fail(f"unexpected condition label: {condition!r}")

    evidence, evidence_included, evidence_missing = build_fixed_evidence(
        expected_entry, evidence_dir, question_id
    )
    if evidence_missing:
        return fail("grader evidence pack incomplete", {"evidence_missing": evidence_missing})

    agent_workspace, copy_root = prepare_agent_workspace(runner_workspace)
    try:
        pilot_path = agent_workspace / MEMORY_SURFACE
        pilot_present = pilot_path.is_file()
        runner_pilot_present = (runner_workspace / MEMORY_SURFACE).is_file()

        # Hard integrity gates: a condition mix-up is not a caveat, it is a failed run.
        if condition == "CONTROL" and pilot_present:
            return fail("DEV_MEMORY_PILOT.md present in CONTROL workspace")
        if condition == "TREATMENT" and not pilot_present:
            return fail("DEV_MEMORY_PILOT.md missing in TREATMENT workspace")

        run_id = os.environ.get("ARGENTOS_RUN_ID", "unknown")
        source_digest = os.environ.get("ARGENTOS_SOURCE_DIGEST", "unknown")
        runner_sha256 = os.environ.get("ARGENTOS_RUNNER_SHA", "unknown")
        tool_set_sha256 = os.environ.get("ARGENTOS_TOOL_SET_SHA", "unknown")
        key_path_value = os.environ.get("ARGENTOS_EXPECTED_KEY")
        key_path = Path(key_path_value) if key_path_value else None
        task_prompt = build_task_prompt(question)

        digest_before = workspace_tree_digest(agent_workspace)
        dsh_home = make_dsh_home()
        try:
            child_env = build_child_env(dsh_home)
            forwarded_labels = sorted(key for key in child_env if key.upper().startswith("ARGENTOS_"))
            if forwarded_labels:
                return fail(
                    "runner variables forwarded to agent: " + ", ".join(forwarded_labels),
                    {"condition_labels_in_child_env": forwarded_labels},
                )
            condition_token_in_cwd = any(
                token in str(agent_workspace).lower() for token in ("control", "treatment")
            )
            if condition_token_in_cwd:
                return fail("condition token in agent cwd", {"agent_cwd": str(agent_workspace)})
            agent_run = run_headless(
                task_prompt,
                agent_workspace,
                timeout=agent_timeout,
                child_env=child_env,
                dsh_cli=dsh_cli,
            )
        finally:
            shutil.rmtree(dsh_home, ignore_errors=True)

        raw_agent = write_raw_ndjson(trace_dir, condition, question_id, "agent", agent_run.raw_stdout)

        digest_after = workspace_tree_digest(agent_workspace)
        if digest_before and digest_after and digest_before != digest_after:
            return fail(
                "workspace changed during the run",
                {"raw_agent": raw_agent, "digest_before": digest_before, "digest_after": digest_after},
            )

        instrumentation = map_instrumentation(agent_run.events, agent_workspace)
        disallowed_completed = sorted(
            {
                event["tool"]
                for event in instrumentation.tool_events
                if event.get("tool") in DISALLOWED_AGENT_TOOLS
                and event.get("status") in (None, "completed")
            }
        )
        disallowed_attempts = sorted(
            {
                event["tool"]
                for event in instrumentation.tool_events
                if event.get("tool") in DISALLOWED_AGENT_TOOLS
                and event.get("status") not in (None, "completed")
            }
        )
        if disallowed_completed:
            return fail(
                "tools outside the frozen policy were observed in use: "
                + ", ".join(disallowed_completed),
                {"raw_agent": raw_agent, "observed_disallowed_tools": disallowed_completed},
            )
        successful_outside = [
            call
            for call in instrumentation.out_of_workspace_calls
            if call.get("status") in (None, "completed")
        ]
        attempted_outside = [
            call
            for call in instrumentation.out_of_workspace_calls
            if call.get("status") not in (None, "completed")
        ]
        if successful_outside:
            return fail(
                "out-of-workspace access: " + json.dumps(successful_outside, ensure_ascii=False)[:500],
                {"raw_agent": raw_agent, "out_of_workspace_calls": successful_outside},
            )

        for path in instrumentation.file_open_events:
            emit({"event": "file_open", "path": path})
        for query in instrumentation.search_events:
            emit({"event": "search", "query": query})
        for path in instrumentation.rehydration_events:
            emit({"event": "source_rehydrated", "path": path})

        answer = agent_run.final_text
        provenance, cited, provenance_supported = compute_provenance(
            answer, agent_workspace, instrumentation.opened
        )

        grader_run: HeadlessRun | None = None
        grader_parsed: dict[str, Any] | None = None
        grader_prompt_used: str | None = None
        if answer:
            for attempt in range(2):
                grader_prompt = build_grader_prompt(question, expected_entry, answer, evidence)
                if attempt:
                    grader_prompt += "\n\nREMINDER: return ONLY the JSON object with the rubric keys.\n"
                grader_prompt_used = grader_prompt
                judge_home = make_dsh_home()
                try:
                    grader_run = run_grader(
                        grader_prompt,
                        timeout=judge_timeout,
                        child_env=build_child_env(judge_home),
                        dsh_cli=dsh_cli,
                    )
                finally:
                    shutil.rmtree(judge_home, ignore_errors=True)
                grader_parsed = parse_grader_json(grader_run.final_text)
                if grader_parsed is not None:
                    break
            if grader_parsed is None:
                sys.stderr.write("executor: grader returned no parseable JSON\n")

        raw_grader = write_raw_ndjson(
            trace_dir,
            condition,
            question_id,
            "grader",
            grader_run.raw_stdout if grader_run else "",
        )

        judged = gradable_fields(grader_parsed)
        answer_event: dict[str, Any] = {"event": "answer"}
        for key, value in judged.items():
            if value is not None:
                answer_event[key] = value
        if provenance is not None:
            answer_event["provenance_present"] = provenance
        if len(answer_event) > 1:
            emit(answer_event)

        notes: list[str] = []
        if disallowed_attempts:
            notes.append(
                "INTEGRITY: failed attempts to use frozen-out tools: "
                + ", ".join(disallowed_attempts)
            )
        if attempted_outside:
            notes.append(
                "INTEGRITY: out-of-workspace read attempts (failed): "
                + json.dumps(attempted_outside, ensure_ascii=False)[:500]
            )
        if evidence_missing:
            notes.append("grader evidence sources missing: " + ", ".join(evidence_missing))

        if agent_run.error:
            sys.stderr.write(f"executor: agent run error: {agent_run.error}\n")

        trace: dict[str, Any] = {
            "schema": TRACE_SCHEMA,
            "condition": condition,
            "question_id": question_id,
            "question": question,
            "run": {
                "run_id": run_id,
                "source_digest": source_digest,
                "runner_sha256": runner_sha256,
                "adapter_sha256": file_sha256(Path(__file__)),
                "tool_set_sha256": tool_set_sha256,
                "tool_policy_sha256": hashlib.sha256(TOOL_POLICY_PATCH.encode("utf-8")).hexdigest(),
                "prompt_sha256": hashlib.sha256(task_prompt.encode("utf-8")).hexdigest(),
                "grader_prompt_sha256": (
                    hashlib.sha256(grader_prompt_used.encode("utf-8")).hexdigest()
                    if grader_prompt_used
                    else None
                ),
                "key_sha256": file_sha256(key_path) if key_path else None,
                "evidence_sha256": hashlib.sha256(evidence.encode("utf-8")).hexdigest(),
            },
            "workspace": {
                "runner": str(runner_workspace),
                "agent": str(agent_workspace),
                "neutral_copy": True,
            },
            "base_commit": base_commit,
            "model_label": model_label,
            "dsh_cli": str(dsh_cli),
            "experimental_infrastructure": "tools/dev_memory_agent_executor.py",
            "integrity": {
                "pilot_present": pilot_present,
                "pilot_sha256": hashlib.sha256(pilot_path.read_bytes()).hexdigest() if pilot_present else None,
                "runner_pilot_present": runner_pilot_present,
                "workspace_digest_before": digest_before,
                "workspace_digest_after": digest_after,
                "workspace_stable": bool(digest_before and digest_after and digest_before == digest_after),
                "condition_labels_in_child_env": forwarded_labels,
                "condition_token_in_agent_cwd": condition_token_in_cwd,
                "tool_policy_sha256": hashlib.sha256(TOOL_POLICY_PATCH.encode("utf-8")).hexdigest(),
                "grader_tool_policy_sha256": hashlib.sha256(
                    GRADER_TOOL_POLICY_PATCH.encode("utf-8")
                ).hexdigest(),
                "disabled_tools": list(DISABLED_TOOLS),
                "grader_disabled_tools": list(GRADER_DISABLED_TOOLS),
                "observed_disallowed_tools": disallowed_completed,
                "observed_disallowed_tool_attempts": disallowed_attempts,
                "out_of_workspace_calls": instrumentation.out_of_workspace_calls,
                "failed_reads": instrumentation.failed_reads,
                "agent_sandbox": "read-only",
            },
            "instrumentation": {
                "file_open_events": instrumentation.file_open_events,
                "search_events": instrumentation.search_events,
                "source_rehydration_events": instrumentation.rehydration_events,
                "shell_commands": instrumentation.shell_commands,
                "tool_calls": instrumentation.tool_calls,
                "observed_tools": sorted(instrumentation.observed_tools),
                "distinct_files_opened": sorted(set(instrumentation.opened)),
            },
            "agent": {
                "elapsed_seconds": round(agent_run.elapsed, 3),
                "returncode": agent_run.returncode,
                "timed_out": agent_run.timed_out,
                "error": agent_run.error,
                "session_id": agent_run.session_id,
                "turn_end": agent_run.turn_end,
                "usage": agent_run.usage,
                "stderr_tail": agent_run.stderr[-2000:],
                "final_answer": (answer or "")[:ANSWER_TRACE_CAP],
            },
            "provenance": {
                "deterministic": provenance,
                "cited": cited,
                "cited_and_opened": provenance_supported,
            },
            "grader": {
                "attempted": grader_run is not None,
                "elapsed_seconds": round(grader_run.elapsed, 3) if grader_run else None,
                "returncode": grader_run.returncode if grader_run else None,
                "timed_out": grader_run.timed_out if grader_run else None,
                "usage": grader_run.usage if grader_run else None,
                "evidence_included": evidence_included,
                "evidence_missing": evidence_missing,
                "raw_final": (grader_run.final_text or "")[:4000] if grader_run else None,
                "parsed": grader_parsed,
                "fields_used": judged,
            },
            "raw_ndjson": {"agent": raw_agent, "grader": raw_grader},
            "notes": notes,
        }
        write_trace(trace_dir, condition, question_id, trace)
        return 0
    finally:
        shutil.rmtree(copy_root, ignore_errors=True)


if __name__ == "__main__":
    raise SystemExit(main())
