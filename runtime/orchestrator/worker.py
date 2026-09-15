"""Worker boundary and the MVP worker (plan 122 §6 and §15).

The host delegates; a **Worker** executes and reports. The MVP ships one real
worker and one null worker:

``CommandWorker``
    Really runs the delegated command-set as subprocesses (no shell), captures
    stdout/stderr to persistent files, observes which artifacts changed, and
    writes the persistent Worker Result. It is a real executor, not a simulator:
    every field of its result is derived from something that happened.
``NullWorker``
    Executes nothing and reports exactly that. It exists as the test boundary and
    as the honest default when no worker is configured — it never fabricates a
    result.

Two rules are structural:

1. ``exit_code == 0`` means *the command ran and reported success*. It never
   means the workflow is complete, and this module never returns such a claim.
2. A command whose failure is covered by an environmental class **declared in the
   authorized plan** yields ``GAP`` (declared absence of obtainable evidence),
   never ``PASS``. Absence of evidence is never converted into positive evidence.
"""

from __future__ import annotations

import hashlib
import re
import subprocess
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable, Mapping, Protocol, Sequence

from .contracts import (
    ANOMALY,
    BOUNDARY,
    EXCLUDED,
    FAIL,
    GAP,
    NOT_APPLICABLE,
    SIGNALS,
    VALID,
    Delegation,
    WorkerResult,
)
from .store import OrchestratorStore

DEFAULT_TIMEOUT_SECONDS = 1800
CAPTURE_TAIL_LINES = 40

_LIFECYCLE_GATE_LABELS = {
    "check_lifecycle_anchor.py": "C-1",
    "check_lifecycle_checkpoint.py": "C-2",
    "check_lifecycle_lineage.py": "C-3",
}

_SIGNAL_TEXT = "|".join(re.escape(signal) for signal in SIGNALS)


class WorkerError(RuntimeError):
    """The worker could not produce a result at all (fail-closed)."""


class WorkerAdapter(Protocol):
    """The boundary the host delegates through. Implementations execute nothing
    else and never decide anything."""

    kind: str

    def execute(
        self, delegation: Delegation, *, store: OrchestratorStore, run_id: str
    ) -> WorkerResult:  # pragma: no cover - protocol declaration
        ...


def _sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8", errors="replace")).hexdigest()


def _tail(text: str, lines: int = CAPTURE_TAIL_LINES) -> str:
    rows = text.splitlines()
    return "\n".join(rows[-lines:])


def _gate_label(argv: Sequence[str]) -> str | None:
    for token in argv:
        name = Path(token).name
        if name in _LIFECYCLE_GATE_LABELS:
            return _LIFECYCLE_GATE_LABELS[name]
    return None


def _is_checker(argv: Sequence[str]) -> bool:
    return any(Path(token).name.startswith("check_") and token.endswith(".py") for token in argv)


def _is_pytest(argv: Sequence[str]) -> bool:
    return "pytest" in Path(argv[0]).name or "-m" in argv and "pytest" in argv


def environmental_class_for(
    argv: Sequence[str], environmental: Sequence[tuple[str, str]]
) -> str | None:
    """The declared environmental class covering this command, if declared.

    Matching is by whole command prefix, not by raw substring: the declared
    prefix must be the command itself or a token-boundary prefix of it, so a
    declaration for one command never silently covers a different one.
    """
    joined = " ".join(argv)
    for prefix, declaration in environmental:
        if joined == prefix or joined.startswith(prefix + " "):
            return declaration
    return None


def _gate_signal_for_plan(text: str, plan_rel: str) -> str | None:
    """The signal the gate reported for this artifact, read from its own output."""
    pattern = re.compile(
        r"^\s*-\s*" + re.escape(plan_rel) + r":\s*(" + _SIGNAL_TEXT + r")\b",
        re.MULTILINE,
    )
    match = pattern.search(text)
    return match.group(1) if match else None


def classify(
    argv: Sequence[str],
    *,
    exit_code: int | None,
    timed_out: bool,
    stdout_text: str,
    plan_rel: str | None,
    environmental: Sequence[tuple[str, str]],
) -> tuple[str, str, str | None]:
    """Classify one command's real outcome.

    Returns ``(signal, basis, label)``. The class of a command is derived from
    the checker's own classification when it publishes one; otherwise from its
    exit status and its declared environmental class. A time-out is a declared
    absence of evidence (``GAP``).
    """
    label = _gate_label(argv)
    if timed_out:
        return GAP, "command exceeded its declared timeout: no evidence obtained", label

    declared = environmental_class_for(argv, environmental)

    if label is not None and plan_rel is not None:
        signal = _gate_signal_for_plan(stdout_text, plan_rel)
        if signal is not None:
            return signal, f"{label} reported its own classification for {plan_rel}", label
        if exit_code == 0:
            return (
                GAP,
                f"{label} published no classification for {plan_rel}: absence of evidence",
                label,
            )
        return FAIL, f"{label} exited {exit_code} without a classification", label

    if exit_code is None:
        return GAP, "the command did not produce an exit status", label

    if exit_code == 0:
        if _is_checker(argv):
            return VALID, "the checker reported no violation (exit 0)", label
        return VALID, "the command completed with exit 0", label

    if declared is not None:
        return (
            GAP,
            (
                "declared environmental class in the authorized plan: "
                f"{declared} (non-zero exit is a declared absence of obtainable "
                "evidence, never PASS)"
            ),
            label,
        )
    if _is_pytest(argv):
        return FAIL, f"the test suite exited {exit_code}", label
    if _is_checker(argv):
        return FAIL, f"the checker exited {exit_code}: mechanical violation", label
    return FAIL, f"the command exited {exit_code}", label


def repository_paths(root: Path) -> set[str]:
    """Every path git reports as changed in the working tree (read-only).

    Includes untracked paths (``??``), so a *new* file that was never added to
    the index counts as a change — which is what makes ``host._committed``
    correct for a path whose content is in no commit. A non-repository root or an
    unavailable git yields an empty set: a declared absence of observation, never
    a fabricated one.

    The orchestrator's own evidence area is excluded. It is the repository's
    ephemeral, never-committed session area (gitignored in this repository), and
    the evidence the worker persists there is not a change to the project: letting
    it through would make the worker look as if it had modified content outside
    its authorized scope.
    """
    try:
        proc = subprocess.run(
            ["git", "-C", str(root), "status", "--porcelain"],
            check=False,
            capture_output=True,
            text=True,
        )
    except OSError:
        return set()
    if proc.returncode != 0:
        return set()
    paths: set[str] = set()
    for line in proc.stdout.splitlines():
        if len(line) > 3:
            path = line[3:].strip().strip('"')
            if path == ".project" or path.startswith(".project/"):
                continue
            paths.add(path)
    return paths


#: Digest recorded for a path that does not exist. Distinct from any real digest,
#: so "created" and "deleted" are both observable as a change.
ABSENT_DIGEST = "absent"


def content_digests(root: Path, paths: Sequence[str]) -> dict[str, str]:
    """SHA-256 of every path's content, or a declared marker when it is absent."""
    digests: dict[str, str] = {}
    for rel in paths:
        try:
            digests[rel] = hashlib.sha256((root / rel).read_bytes()).hexdigest()
        except OSError:
            digests[rel] = ABSENT_DIGEST
    return digests


def repository_snapshot(root: Path) -> dict[str, str]:
    """A content snapshot of the whole working tree (read-only, git-based).

    Every tracked file plus every untracked file that is not ignored. The
    orchestrator's ephemeral evidence area is excluded: it is never committed, and
    the evidence a worker persists there is not a change to the project.

    Comparing two snapshots yields the paths whose content really changed between
    them, whatever the repository's starting state was. That is what makes both
    the worker's ``artifacts_modified`` and the host's scope verification honest on
    a working tree that was already dirty — a dirty-path comparison cannot see a
    change to a path that was already dirty, and therefore cannot see a scope
    violation either.
    """
    try:
        proc = subprocess.run(
            [
                "git", "-C", str(root), "ls-files", "-z",
                "--cached", "--others", "--exclude-standard",
            ],
            check=False,
            capture_output=True,
        )
    except OSError:
        return {}
    if proc.returncode != 0:
        return {}
    snapshot: dict[str, str] = {}
    for entry in proc.stdout.split(b"\x00"):
        if not entry:
            continue
        rel = entry.decode("utf-8", errors="replace")
        if rel == ".project" or rel.startswith(".project/"):
            continue
        try:
            snapshot[rel] = hashlib.sha256((root / rel).read_bytes()).hexdigest()
        except OSError:
            snapshot[rel] = ABSENT_DIGEST
    return snapshot


def changed_paths(
    before: Mapping[str, str], after: Mapping[str, str]
) -> list[str]:
    """Paths whose content (or existence) differs between two snapshots."""
    return sorted(
        rel
        for rel in set(before) | set(after)
        if before.get(rel) != after.get(rel)
    )


@dataclass
class CommandWorker:
    """Runs the delegated command-set and persists a real Worker Result."""

    timeout_seconds: int = DEFAULT_TIMEOUT_SECONDS
    kind: str = "command"

    def execute(
        self,
        delegation: Delegation,
        *,
        store: OrchestratorStore,
        run_id: str,
        plan_rel: str | None = None,
        environmental: Sequence[tuple[str, str]] = (),
        now: str | None = None,
    ) -> WorkerResult:
        root = store.root
        before = repository_paths(root)
        commands: list[dict[str, Any]] = []
        results: list[dict[str, Any]] = []
        problems: list[dict[str, Any]] = []
        evidence: list[dict[str, Any]] = []
        pending: list[str] = []

        for index, argv in enumerate(delegation.command_set, start=1):
            label = _gate_label(argv) or f"command-{index:02d}"
            # Captures are unique per iteration: two iterations of the same run
            # must never overwrite each other's evidence.
            capture_dir = f"{run_id}/it{delegation.iteration:04d}"
            stdout_rel = f"{capture_dir}/cmd-{index:02d}-stdout.txt"
            stderr_rel = f"{capture_dir}/cmd-{index:02d}-stderr.txt"
            stdout_path = store.runs_dir(delegation.plan) / stdout_rel
            stderr_path = store.runs_dir(delegation.plan) / stderr_rel
            stdout_path.parent.mkdir(parents=True, exist_ok=True)

            started = time.monotonic()
            timed_out = False
            exit_code: int | None = None
            with stdout_path.open("wb") as out, stderr_path.open("wb") as err:
                try:
                    proc = subprocess.run(
                        list(argv),
                        cwd=str(root),
                        stdout=out,
                        stderr=err,
                        timeout=self.timeout_seconds,
                        check=False,
                    )
                    exit_code = proc.returncode
                except subprocess.TimeoutExpired:
                    timed_out = True
                except OSError as exc:
                    exit_code = None
                    pending.append(f"{' '.join(argv)}: could not be executed ({exc})")
            duration_ms = int((time.monotonic() - started) * 1000)

            stdout_text = stdout_path.read_text(encoding="utf-8", errors="replace")
            stderr_text = stderr_path.read_text(encoding="utf-8", errors="replace")
            signal, basis, gate_label = classify(
                argv,
                exit_code=exit_code,
                timed_out=timed_out,
                stdout_text=stdout_text,
                plan_rel=plan_rel,
                environmental=environmental,
            )

            commands.append(
                {
                    "argv": list(argv),
                    "exit_code": exit_code,
                    "timed_out": timed_out,
                    "duration_ms": duration_ms,
                    "stdout_path": stdout_rel,
                    "stdout_sha256": _sha256_text(stdout_text),
                    "stdout_bytes": len(stdout_text.encode("utf-8", errors="replace")),
                    "stdout_tail": _tail(stdout_text),
                    "stderr_path": stderr_rel,
                    "stderr_sha256": _sha256_text(stderr_text),
                    "stderr_bytes": len(stderr_text.encode("utf-8", errors="replace")),
                    "stderr_tail": _tail(stderr_text),
                }
            )
            results.append(
                {
                    "label": gate_label or label,
                    "command_index": index,
                    "argv": list(argv),
                    "signal": signal,
                    "classification_basis": basis,
                    "exit_code": exit_code,
                }
            )
            for rel in (stdout_rel, stderr_rel):
                evidence.append(
                    {
                        "kind": "command-capture",
                        "path": (store.runs_dir(delegation.plan) / rel)
                        .relative_to(root)
                        .as_posix(),
                        "sha256": _sha256_text(
                            stdout_text if rel.endswith("stdout.txt") else stderr_text
                        ),
                    }
                )
            if signal != VALID:
                problems.append(
                    {
                        "signal": signal,
                        "description": f"{' '.join(argv)}: {basis}",
                        "evidence_ref": stdout_rel,
                    }
                )

        after = repository_paths(root)
        modified = sorted(after - before)

        result = WorkerResult(
            result_id=f"{delegation.delegation_id}-result",
            delegation_id=delegation.delegation_id,
            plan=delegation.plan,
            iteration=delegation.iteration,
            created_at=now or _utc_now(),
            status=("incomplete" if any(c["timed_out"] for c in commands) else "completed"),
            worker_kind=self.kind,
            delegation_received=delegation.to_dict(),
            intended_actions=tuple(
                " ".join(argv) for argv in delegation.command_set
            ),
            performed_actions=tuple(
                f"{' '.join(command['argv'])} -> exit {command['exit_code']}"
                for command in commands
            ),
            artifacts_modified=tuple(modified),
            commands_executed=tuple(commands),
            results=tuple(results),
            evidence=tuple(evidence),
            problems=tuple(problems),
            pending=tuple(pending),
            recommended_next_action=_recommendation(results),
            authority_used={
                "basis": delegation.authority_basis,
                "scope": list(delegation.declared_scope),
                "claim": (
                    "the worker claims it acted only within the delegated "
                    "command-set; this claim is evidence, not authority"
                ),
            },
            effects_executed=tuple(
                [
                    f"wrote {len(commands) * 2} capture file(s) under {run_id}/",
                    f"persisted worker result for delegation {delegation.delegation_id}",
                ]
                + [f"artifact modified: {path}" for path in modified]
            ),
            claims={
                "self_reported_completion": False,
                "note": (
                    "a worker never determines workflow completion: exit 0 means "
                    "the command ran, not that the change is complete"
                ),
            },
            limitations=(
                "the worker executes commands and reports observations; it does "
                "not decide, verify or close anything",
                "classification is derived from each command's own published "
                "classification, its exit status and the plan's declared "
                "environmental classes; it is evidence, never authority",
            ),
        )
        store.write_worker_result(result)
        return result


@dataclass
class NullWorker:
    """Executes nothing and reports exactly that (honest default / test boundary)."""

    kind: str = "null"

    def execute(
        self,
        delegation: Delegation,
        *,
        store: OrchestratorStore,
        run_id: str,
        **_: Any,
    ) -> WorkerResult:
        result = WorkerResult(
            result_id=f"{delegation.delegation_id}-result",
            delegation_id=delegation.delegation_id,
            plan=delegation.plan,
            iteration=delegation.iteration,
            created_at=_utc_now(),
            status="not-executed",
            worker_kind=self.kind,
            delegation_received=delegation.to_dict(),
            intended_actions=(),
            performed_actions=(),
            artifacts_modified=(),
            commands_executed=(),
            results=(),
            evidence=(),
            problems=(
                {
                    "signal": NOT_APPLICABLE,
                    "description": "no worker was configured: nothing was executed",
                    "evidence_ref": "",
                },
            ),
            pending=("the delegated command-set was not executed",),
            recommended_next_action={
                "action": None,
                "advisory": True,
                "rationale": "no execution took place",
            },
            authority_used={"basis": delegation.authority_basis},
            effects_executed=(),
            claims={"self_reported_completion": False},
            limitations=("the null worker produces no evidence",),
        )
        store.write_worker_result(result)
        return result


def _recommendation(results: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    """An advisory recommendation. Never an authorization."""
    signals = [str(item.get("signal")) for item in results]
    if any(signal in (ANOMALY, BOUNDARY, FAIL) for signal in signals):
        action = "STOP_AND_ESCALATE"
        rationale = "at least one delegated command reported a non-advisory signal"
    elif signals and all(signal in (VALID, EXCLUDED) for signal in signals):
        action = "CONTINUE"
        rationale = "every delegated command reported a non-blocking signal"
    else:
        action = "CONTINUE_WITH_DECLARED_GAPS"
        rationale = "some evidence was unobtainable; it is declared, not fabricated"
    return {
        "action": action,
        "advisory": True,
        "rationale": rationale,
        "note": "advisory only: the host derives its own next action and never "
        "converts this recommendation into authority",
    }


def _utc_now() -> str:
    from datetime import datetime, timezone

    return datetime.now(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z")
