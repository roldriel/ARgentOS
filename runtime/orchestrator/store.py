"""Persistent, reconstructible store of the DEV Autonomous Orchestrator (plan 122).

Physical layout (per plan, no global database, no registry)::

    <root>/.project/orchestrator/plan-<NNN>/
        delegations/<delegation_id>.json     # delegation records (M1 → Worker)
        worker-results/<delegation_id>.json  # persistent Worker Results (M4)
        journal.jsonl                        # one iteration record per line
        runs/<run_id>.md                     # reconstruction report per run

``.project/`` is the repository's existing ephemeral execution-record area
(``AGENTS.md``: session artifacts are ephemeral and are never committed) and the
precedent for derived stores is ``runtime/toolcalls/change_governance.py``
(``.project/changes/``, RFC-76 D-01). The store is therefore **durable across
process restarts but not versioned**: the governance-level record of a change
lives in the plan artifact, while the raw evidence of each iteration lives here.

Recovery does not depend on this store being intact: the host rebuilds its view
from the repository (Git + governance artifacts) and *then* re-reads the store.
A missing or corrupt store entry is an absence of evidence (``GAP``), never a
positive fact.
"""

from __future__ import annotations

import json
import os
import tempfile
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable, Mapping

from .contracts import (
    ContractError,
    Delegation,
    WorkerResult,
    canonical_json,
    validate_worker_result,
    worker_result_from_json,
)

DEFAULT_STORE_DIRNAME = "orchestrator"


@dataclass(frozen=True)
class JournalRead:
    """A journal read plus the malformed lines it had to skip.

    The journal is written by the orchestrator itself and is therefore normally
    well-formed, but it is also the artifact the host reconstructs a run from.
    Silently dropping an unreadable line would hide an absence of evidence, so
    the read reports the dropped lines and the caller declares them as ``GAP``.
    """

    records: tuple[dict[str, Any], ...] = ()
    malformed_lines: tuple[int, ...] = ()

    def gap_notes(self) -> tuple[str, ...]:
        """Deterministic declarations of the evidence that could not be read."""
        return tuple(
            f"journal line {number} is not readable as an iteration record "
            "(declared GAP: no claim is made about it)"
            for number in self.malformed_lines
        )

    def __iter__(self):
        return iter(self.records)

    def __len__(self) -> int:
        return len(self.records)


class OrchestratorStore:
    """Append-oriented store of delegations, worker results and iteration records."""

    def __init__(self, root: str | Path, base_dir: str | Path | None = None):
        self.root = Path(root).resolve()
        self.base = (
            Path(base_dir).resolve()
            if base_dir is not None
            else self.root / ".project" / DEFAULT_STORE_DIRNAME
        )

    # -- layout ------------------------------------------------------------- #

    def plan_dir(self, plan: int) -> Path:
        return self.base / f"plan-{plan:03d}"

    def delegations_dir(self, plan: int) -> Path:
        return self.plan_dir(plan) / "delegations"

    def results_dir(self, plan: int) -> Path:
        return self.plan_dir(plan) / "worker-results"

    def runs_dir(self, plan: int) -> Path:
        return self.plan_dir(plan) / "runs"

    def journal_path(self, plan: int) -> Path:
        return self.plan_dir(plan) / "journal.jsonl"

    # -- atomic write ------------------------------------------------------- #

    def _write_text(self, path: Path, text: str) -> Path:
        """Write UTF-8/LF atomically (temp file in the same directory + replace)."""
        path.parent.mkdir(parents=True, exist_ok=True)
        fd, tmp_name = tempfile.mkstemp(
            dir=str(path.parent), prefix=path.name + ".", suffix=".tmp"
        )
        try:
            with os.fdopen(fd, "w", encoding="utf-8", newline="\n") as handle:
                handle.write(text)
            os.replace(tmp_name, path)
        except BaseException:
            try:
                os.unlink(tmp_name)
            except OSError:
                pass
            raise
        return path

    # -- delegations -------------------------------------------------------- #

    def write_delegation(self, delegation: Delegation) -> Path:
        path = self.delegations_dir(delegation.plan) / (
            delegation.delegation_id + ".json"
        )
        return self._write_text(path, canonical_json(delegation.to_dict()))

    def read_delegation(self, plan: int, delegation_id: str) -> Delegation | None:
        path = self.delegations_dir(plan) / (delegation_id + ".json")
        try:
            payload = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            return None
        if not isinstance(payload, Mapping):
            return None
        try:
            return Delegation.from_dict(payload)
        except (KeyError, TypeError, ValueError):
            return None

    def list_delegations(self, plan: int) -> list[Delegation]:
        directory = self.delegations_dir(plan)
        if not directory.is_dir():
            return []
        found: list[Delegation] = []
        for path in sorted(directory.glob("*.json")):
            try:
                payload = json.loads(path.read_text(encoding="utf-8"))
            except (OSError, json.JSONDecodeError):
                continue
            try:
                found.append(Delegation.from_dict(payload))
            except (KeyError, TypeError, ValueError):
                continue
        return found

    # -- worker results (M4) ------------------------------------------------ #

    def write_worker_result(self, result: WorkerResult) -> Path:
        payload = result.to_dict()
        problems = validate_worker_result(payload)
        if problems:
            raise ContractError("; ".join(problems))
        path = self.results_dir(result.plan) / (result.delegation_id + ".json")
        return self._write_text(path, canonical_json(payload))

    def read_worker_result(self, plan: int, delegation_id: str) -> WorkerResult | None:
        path = self.results_dir(plan) / (delegation_id + ".json")
        try:
            text = path.read_text(encoding="utf-8")
        except OSError:
            return None
        try:
            return worker_result_from_json(text)
        except ContractError:
            return None

    def read_worker_result_raw(
        self, plan: int, delegation_id: str
    ) -> dict[str, Any] | None:
        """Raw payload, preserved for the reconstruction of corrupt records."""
        path = self.results_dir(plan) / (delegation_id + ".json")
        try:
            payload = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            return None
        return payload if isinstance(payload, dict) else None

    def list_worker_results(self, plan: int) -> list[WorkerResult]:
        directory = self.results_dir(plan)
        if not directory.is_dir():
            return []
        found: list[WorkerResult] = []
        for path in sorted(directory.glob("*.json")):
            try:
                found.append(worker_result_from_json(path.read_text(encoding="utf-8")))
            except (OSError, ContractError):
                continue
        return found

    # -- journal (observability, append-only) ------------------------------- #

    def append_iteration(self, plan: int, record: Mapping[str, Any]) -> Path:
        path = self.journal_path(plan)
        path.parent.mkdir(parents=True, exist_ok=True)
        line = json.dumps(dict(record), sort_keys=True, ensure_ascii=False)
        with path.open("a", encoding="utf-8", newline="\n") as handle:
            handle.write(line + "\n")
        return path

    def read_journal_with_gaps(self, plan: int) -> "JournalRead":
        """All readable iteration records plus the lines that could not be read.

        Same fail-closed semantics as :meth:`read_journal`, but the absence is
        **returned** instead of discarded: a truncated or corrupted line is a
        declared ``GAP``, never a silently missing record and never a fabricated
        one. The journal itself is not authority: the reconstruction always
        re-observes the repository.
        """
        path = self.journal_path(plan)
        if not path.is_file():
            return JournalRead()
        try:
            text = path.read_text(encoding="utf-8", errors="replace")
        except OSError:
            return JournalRead()
        records: list[dict[str, Any]] = []
        malformed: list[int] = []
        for number, line in enumerate(text.splitlines(), start=1):
            if not line.strip():
                continue
            try:
                payload = json.loads(line)
            except json.JSONDecodeError:
                malformed.append(number)
                continue
            if isinstance(payload, dict):
                records.append(payload)
            else:
                malformed.append(number)
        return JournalRead(records=tuple(records), malformed_lines=tuple(malformed))

    def read_journal(self, plan: int) -> list[dict[str, Any]]:
        """All readable iteration records, in file order.

        Kept as the convenience view over :meth:`read_journal_with_gaps` for
        callers that only need the records. A caller that must not lose the
        absence of evidence uses ``read_journal_with_gaps`` and declares the
        malformed lines as ``GAP``.
        """
        return list(self.read_journal_with_gaps(plan).records)

    # -- run reports -------------------------------------------------------- #

    def write_run_artifact(self, plan: int, relative_path: str, text: str) -> Path:
        """Persist a raw evidence artifact of a run (captures, reports)."""
        path = self.runs_dir(plan) / relative_path
        return self._write_text(path, text)

    def read_run_artifact(self, plan: int, relative_path: str) -> str | None:
        path = self.runs_dir(plan) / relative_path
        try:
            return path.read_text(encoding="utf-8", errors="replace")
        except OSError:
            return None

    def write_run_report(self, plan: int, run_id: str, text: str) -> Path:
        return self._write_text(self.runs_dir(plan) / (run_id + ".md"), text)

    def read_run_report(self, plan: int, run_id: str) -> str | None:
        path = self.runs_dir(plan) / (run_id + ".md")
        try:
            return path.read_text(encoding="utf-8")
        except OSError:
            return None

    def list_runs(self, plan: int) -> list[str]:
        directory = self.runs_dir(plan)
        if not directory.is_dir():
            return []
        return sorted(path.stem for path in directory.glob("*.md"))

    # -- store-level evidence ---------------------------------------------- #

    def observed_evidence_paths(self, plan: int) -> list[str]:
        """Repository-relative paths of every persisted orchestration artifact."""
        base = self.plan_dir(plan)
        if not base.is_dir():
            return []
        out: list[str] = []
        for path in sorted(base.rglob("*")):
            if path.is_file():
                out.append(path.relative_to(self.root).as_posix())
        return out


def result_signal_summary(results: Iterable[WorkerResult]) -> dict[str, int]:
    """Deterministic signal histogram of a sequence of worker results."""
    counts: dict[str, int] = {}
    for result in results:
        for signal in result.problem_signals():
            counts[signal] = counts.get(signal, 0) + 1
    return counts
