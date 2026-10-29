#!/usr/bin/env python3
"""Controlled DEV Memory benchmark runner.

This runner is intentionally model-agnostic. It creates isolated Control/Treatment
workspace copies, runs the same external agent command against the same question set,
and records only declared instrumentation. It does not infer quality from prose.

The external agent must accept the question on stdin and may emit JSONL events:
  {"event":"file_open","path":"..."}
  {"event":"search","query":"..."}
  {"event":"source_rehydrated","path":"..."}
  {"event":"answer","correct":true,"scope_ok":true,"provenance":true,
   "authority_boundary":true,"unsupported_claim":false}

Any missing metric remains null/unknown; it is never estimated.
"""

from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import sys
import tempfile
import time
from dataclasses import asdict, dataclass, field
from pathlib import Path


QUESTIONS = [
    ("Q01", "Should runtime execution continuity remain separate from Change Lifecycle?"),
    ("Q02", "Does the comparative study justify a universal Unit/Relationship/State ontology?"),
    ("Q03", "Is runtime memory the same problem as DEV Memory?"),
    ("Q04", "Is two-tier retrieval a plausible DEV Memory pattern?"),
    ("Q05", "Is semantic similarity sufficient for automatic Memory deletion?"),
    ("Q06", "Is Agent-Computer Interface design an independent optimization surface?"),
    ("Q07", "Are behavioral evaluation and lifecycle verification interchangeable?"),
    ("Q08", "Do runtime traces establish authority or lifecycle closure?"),
    ("Q09", "What evidence supports explicit checkpoint/resume investigation?"),
    ("Q10", "What evidence supports two-tier DEV Memory?"),
    ("Q11", "What should ARgentOS adapt without copying external architectures?"),
    ("Q12", "What is the current architectural decision after the comparative study?"),
]


@dataclass
class Record:
    condition: str
    question_id: str
    elapsed_seconds: float
    files_opened: int = 0
    searches: int = 0
    source_rehydrations: int = 0
    correct_conclusion: bool | None = None
    correct_scope: bool | None = None
    provenance_present: bool | None = None
    authority_boundary_preserved: bool | None = None
    unsupported_claim: bool | None = None
    raw_events: int = 0
    errors: list[str] = field(default_factory=list)


def parse_events(stdout: str, record: Record) -> None:
    for line in stdout.splitlines():
        try:
            event = json.loads(line)
        except json.JSONDecodeError:
            continue
        if not isinstance(event, dict):
            continue
        record.raw_events += 1
        kind = event.get("event")
        if kind == "file_open":
            record.files_opened += 1
        elif kind == "search":
            record.searches += 1
        elif kind == "source_rehydrated":
            record.source_rehydrations += 1
        elif kind == "answer":
            for key in (
                "correct_conclusion",
                "correct_scope",
                "provenance_present",
                "authority_boundary_preserved",
                "unsupported_claim",
            ):
                if key in event:
                    setattr(record, key, bool(event[key]))


def run_question(
    command: list[str],
    workspace: Path,
    condition: str,
    qid: str,
    question: str,
) -> Record:
    env = os.environ.copy()
    env["ARGENTOS_MEMORY_MODE"] = condition
    env["ARGENTOS_WORKSPACE"] = str(workspace)
    env["ARGENTOS_QUESTION_ID"] = qid

    record = Record(condition, qid, 0.0)
    started = time.perf_counter()
    try:
        proc = subprocess.run(
            command,
            input=question + "\n",
            text=True,
            capture_output=True,
            cwd=workspace,
            env=env,
            check=False,
        )
        parse_events(proc.stdout, record)
        if proc.returncode != 0:
            record.errors.append(f"agent_exit={proc.returncode}")
        if proc.stderr.strip():
            record.errors.append("agent_stderr_present")
    except OSError as exc:
        record.errors.append(f"runner_error={exc}")
    finally:
        record.elapsed_seconds = time.perf_counter() - started
    return record


def prepare_workspace(source: Path, condition: str) -> Path:
    temp = Path(tempfile.mkdtemp(prefix=f"argentos-memory-{condition.lower()}-"))
    destination = temp / "repo"
    shutil.copytree(source, destination, ignore=shutil.ignore_patterns(".git"))
    if condition == "CONTROL":
        memory = destination / "DEV_MEMORY_PILOT.md"
        if memory.exists():
            memory.unlink()
    return destination


def run(source: Path, command: list[str], output: Path) -> int:
    records: list[Record] = []
    temp_roots: list[Path] = []
    try:
        for condition in ("CONTROL", "TREATMENT"):
            workspace = prepare_workspace(source, condition)
            temp_roots.append(workspace.parent)
            for qid, question in QUESTIONS:
                records.append(run_question(command, workspace, condition, qid, question))
    finally:
        for root in temp_roots:
            shutil.rmtree(root, ignore_errors=True)

    payload = {
        "schema": "argentos.dev-memory.controlled-test.v1",
        "conditions": ["CONTROL", "TREATMENT"],
        "question_count": len(QUESTIONS),
        "records": [asdict(r) for r in records],
        "limitations": [
            "The runner measures only what the external agent reports.",
            "Missing quality fields remain unknown; no correctness is inferred.",
            "The runner does not provide an agent/model.",
            "Control and Treatment use separate filesystem copies.",
        ],
    }
    output.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(output)
    return 0


def self_test() -> int:
    with tempfile.TemporaryDirectory(prefix="argentos-memory-selftest-") as raw:
        root = Path(raw)
        (root / "DEV_MEMORY_PILOT.md").write_text("memory", encoding="utf-8")
        (root / "REFACTOR_SYNTHESIS.md").write_text("source", encoding="utf-8")
        command = [
            sys.executable,
            "-c",
            (
                "import json,sys; "
                "print(json.dumps({'event':'file_open','path':'REFACTOR_SYNTHESIS.md'})); "
                "print(json.dumps({'event':'search','query':sys.stdin.read().strip()})); "
                "print(json.dumps({'event':'source_rehydrated','path':'REFACTOR_SYNTHESIS.md'})); "
                "print(json.dumps({'event':'answer','correct_conclusion':True,"
                "'correct_scope':True,'provenance_present':True,"
                "'authority_boundary_preserved':True,'unsupported_claim':False}))"
            ),
        ]
        out = root / "result.json"
        rc = run(root, command, out)
        data = json.loads(out.read_text(encoding="utf-8"))
        assert rc == 0
        assert len(data["records"]) == 24
        assert {r["condition"] for r in data["records"]} == {"CONTROL", "TREATMENT"}
        assert all(r["files_opened"] == 1 for r in data["records"])
        print("self-test: PASS")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", type=Path, help="Repository root to copy for the test")
    parser.add_argument("--command", nargs="+", help="External agent command; question is sent on stdin")
    parser.add_argument("--output", type=Path, default=Path("dev_memory_controlled_result.json"))
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()

    if args.self_test:
        return self_test()
    if not args.repo or not args.command:
        parser.error("--repo and --command are required unless --self-test is used")
    return run(args.repo.resolve(), args.command, args.output.resolve())


if __name__ == "__main__":
    raise SystemExit(main())
