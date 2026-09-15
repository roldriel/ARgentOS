"""Behaviour tests of the DEV Agent Worker (plan 123).

These tests exercise the **Agent Worker over a real repository**: a throw-away git
repository is built per test, the host really observes it, the Agent Worker really
reconstructs the delivered Execution Context, an injected ``AgentInvoker`` really
performs work, the repository really changes, the declared verification really
runs and the Worker Result is really persisted and re-read.

They deliberately do **not** use pytest's ``tmp_path``: the throw-away git
repositories built here must not be nested in the repository under test, so a
scratch directory is created explicitly **outside** the repository (see
``tests/pytest_isolation.py``) and is overridable through
``ARGENTOS_ORCHESTRATOR_SCRATCH``. The tests are deterministic and independent of
``protocol/``.
"""

from __future__ import annotations

import json
import os
import subprocess
import sys
import uuid
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT))
sys.path.insert(0, str(REPO_ROOT / "tests"))

import pytest_isolation  # noqa: E402

from runtime.orchestrator.agent_worker import (  # noqa: E402
    INVOCATION_COMPLETED,
    INVOCATION_INCOMPLETE,
    INVOCATION_NOT_EXECUTED,
    AgentInvocationRequest,
    AgentInvocationResult,
    AgentWorker,
    AgentWorkerError,
    NullAgentInvoker,
)
from runtime.orchestrator.authority import (  # noqa: E402
    AuthorityBoundary,
    recommended_action_is_authority,
)
from runtime.orchestrator.contracts import (  # noqa: E402
    ANOMALY,
    AUTHORIZED_EXISTING,
    FORBIDDEN,
    GAP,
    NOT_APPLICABLE,
    REQUIRES_HUMAN,
    RUN_IMPLEMENTATION_TASK,
    STOP_FORBIDDEN_ACTION,
    VALID,
    WORKER_RESULT_FIELDS,
    AuthorityDecision,
    ContractError,
    Delegation,
    WorkerResult,
    validate_worker_result,
)
from runtime.orchestrator.derivation import (  # noqa: E402
    derive_next_action,
    forbidden_scope_action,
)
from runtime.orchestrator.governance import (  # noqa: E402
    build_finding_record,
    write_finding,
)
from runtime.orchestrator.host import ExecutionHost  # noqa: E402
from runtime.orchestrator.observation import (  # noqa: E402
    parse_agent_task,
    observe,
)
from runtime.orchestrator.store import OrchestratorStore  # noqa: E402
from runtime.orchestrator.worker import CommandWorker, NullWorker  # noqa: E402

SCRATCH_ROOT = Path(
    os.environ.get(
        "ARGENTOS_ORCHESTRATOR_SCRATCH",
        str(pytest_isolation.scratch_root("agent-worker")),
    )
)

PLAN_NUMBER = 201
PLAN_NAME = f"{PLAN_NUMBER}-fake-agent-change.md"

#: A plan that declares authorized semantic work over two paths.
AGENT_TASK_BLOCK = """
## Delegación agentiva

- **Task:** Make the target module report the marker.
- **Scope:** `src/target.py`, `tests/test_target.py`
"""

GATE_SCRIPT = '''"""Synthetic lifecycle gate used only by the agent worker test suite."""
import json
import pathlib
import sys

NAME_TO_GATE = {
    "check_lifecycle_anchor": "C-1",
    "check_lifecycle_checkpoint": "C-2",
    "check_lifecycle_lineage": "C-3",
}
name = pathlib.Path(__file__).stem
gate = NAME_TO_GATE[name]
config = json.loads(pathlib.Path(".gate_signals.json").read_text(encoding="utf-8"))
signal = config.get(gate, "VALID")
print(f"Lifecycle gate check ({gate}, synthetic):")
print(f"- docs/plans/{config.get('plan', '201-fake-agent-change.md')}: {signal} - synthetic gate")
sys.exit(1 if signal in ("ANOMALY", "BOUNDARY") else 0)
'''

CHECK_OK = """import sys
print("ok")
sys.exit(0)
"""


# --------------------------------------------------------------------------- #
# Fixtures (fake repository, no tmp_path)
# --------------------------------------------------------------------------- #


def _scratch(name: str) -> Path:
    path = SCRATCH_ROOT / f"{name}-{uuid.uuid4().hex[:8]}"
    path.mkdir(parents=True, exist_ok=True)
    return path


def _git(root: Path, *args: str) -> None:
    subprocess.run(["git", "-C", str(root), *args], check=True,
                   capture_output=True, text=True)


def make_repo(name: str, *, agent_task: bool = True, extra_scope: str = "") -> Path:
    """A throw-away git repository with a plan, a target module and gates."""
    root = _scratch(name)
    _git(root, "init", "-q", ".")
    _git(root, "config", "user.email", "test@example.invalid")
    _git(root, "config", "user.name", "Agent Worker Test")

    (root / "docs" / "plans").mkdir(parents=True, exist_ok=True)
    (root / "src").mkdir(parents=True, exist_ok=True)
    (root / "tests").mkdir(parents=True, exist_ok=True)
    (root / "tools").mkdir(parents=True, exist_ok=True)

    (root / "src" / "target.py").write_text(
        '"""Target module."""\n\nmarker = "before"\n', encoding="utf-8"
    )
    (root / "tests" / "test_target.py").write_text(
        "from src.target import marker\n\n\ndef test_placeholder():\n    assert marker\n",
        encoding="utf-8",
    )
    for name_, gate in (
        ("check_lifecycle_anchor.py", "C-1"),
        ("check_lifecycle_checkpoint.py", "C-2"),
        ("check_lifecycle_lineage.py", "C-3"),
    ):
        (root / "tools" / name_).write_text(GATE_SCRIPT, encoding="utf-8")
    (root / ".gate_signals.json").write_text(
        json.dumps({"plan": PLAN_NAME, "C-1": "VALID", "C-2": "VALID", "C-3": "N/A"}),
        encoding="utf-8",
    )
    (root / "src" / "check_ok.py").write_text(CHECK_OK, encoding="utf-8")
    (root / ".gitignore").write_text(".project/\n__pycache__/\n", encoding="utf-8")

    task_block = AGENT_TASK_BLOCK if agent_task else ""
    plan = f"""# Plan {PLAN_NUMBER} — fake agent change

**Status:** Aprobado para ejecución
**Fecha:** 2026-09-15
**RFC:** —
**Clase:** —
**Change Level:** L1
**Depende de:** —
**Origen:** synthetic fixture

## Objetivo

Exercise the Agent Worker end to end.

## Criterio de entrada

- [x] synthetic

## Entregables

1. `src/target.py`
2. `tests/test_target.py`

## Pasos

1. Do the work.
{task_block}
## Criterios de salida

- [ ] synthetic

## Verificación

```bash
python src/check_ok.py
{extra_scope}```

## Validation anchor

<!-- container the host records into; empty by design -->

## Checkpoint / cierre

<!-- container the host records into; empty by design -->

## Findings / Correcciones / Pending

### Findings

No findings detected / N/A

## Riesgos

None.
"""
    (root / "docs" / "plans" / PLAN_NAME).write_text(plan, encoding="utf-8")
    (root / "docs" / "plans" / "INDEX.md").write_text(
        f"# Plans\n\n- {PLAN_NAME}\n", encoding="utf-8"
    )
    _git(root, "add", "-A")
    _git(root, "commit", "-qm", "fixture")
    return root


def make_delegation(root: Path, **overrides) -> Delegation:
    defaults = dict(
        delegation_id="plan201-it0001-run_implementation_task",
        plan=PLAN_NUMBER,
        iteration=1,
        action=RUN_IMPLEMENTATION_TASK,
        created_at="2026-09-15T00:00:00Z",
        authority_basis="the authorized plan's own declaration of the work",
        declared_scope=("src/target.py", "tests/test_target.py"),
        command_set=(("python", "src/check_ok.py"),),
        expected_evidence=("the agent invocation transcript",),
        worker_kind="agent",
        worker_command=(),
        task="Make the target module report the marker.",
        input_artifacts=("src/target.py",),
    )
    defaults.update(overrides)
    return Delegation(**defaults)


class RecordingInvoker:
    """An injected invoker that really edits the repository.

    It is the execution environment's stand-in: it receives the materialized
    request, performs a real modification inside the scope it was given and
    reports what it did. It is deliberately *not* part of the shipped package —
    this repository ships no provider and no model.
    """

    kind = "recording"

    def __init__(self, *, status: str = INVOCATION_COMPLETED, write: bool = True,
                 outside_scope: bool = False, reported_commands=(),
                 reported_problems=()):
        self.status = status
        self.write = write
        self.outside_scope = outside_scope
        self.reported_commands = tuple(reported_commands)
        self.reported_problems = tuple(reported_problems)
        self.requests: list[AgentInvocationRequest] = []

    def invoke(self, request: AgentInvocationRequest) -> AgentInvocationResult:
        self.requests.append(request)
        root = Path(request.root)
        if self.write:
            target = root / "src" / "target.py"
            target.write_text(
                '"""Target module."""\n\nmarker = "after"\n', encoding="utf-8"
            )
        if self.outside_scope:
            (root / "src" / "unrelated.py").write_text("x = 1\n", encoding="utf-8")
        return AgentInvocationResult(
            status=self.status,
            summary="edited the target module",
            transcript="observe: read src/target.py\nact: rewrote marker\n",
            steps=3,
            reported_commands=self.reported_commands,
            reported_problems=self.reported_problems,
        )


# --------------------------------------------------------------------------- #
# 1-2. Delegation compatibility and the new fields
# --------------------------------------------------------------------------- #


def test_delegation_without_task_keeps_compatibility():
    """A delegation persisted before plan 123 is still read, with no task."""
    legacy = {
        "schema_version": "1",
        "delegation_id": "plan122-it0001-run_validation",
        "plan": 122,
        "iteration": 1,
        "action": "RUN_VALIDATION",
        "created_at": "2026-09-14T00:00:00Z",
        "authority_basis": "the plan's declared validation command-set",
        "declared_scope": ["runtime/README.md"],
        "command_set": [["python", "tools/check_plan_structure.py"]],
        "expected_evidence": ["stdout/stderr capture per command"],
        "worker": {"kind": "command", "command": []},
    }
    delegation = Delegation.from_dict(legacy)
    assert delegation.task is None
    assert delegation.input_artifacts == ()
    assert delegation.declared_scope == ("runtime/README.md",)
    # And it still round-trips through the persisted form.
    assert Delegation.from_dict(delegation.to_dict()).task is None


def test_delegation_carries_task_and_input_artifacts():
    delegation = make_delegation(Path("."))
    payload = delegation.to_dict()
    assert payload["task"] == "Make the target module report the marker."
    assert payload["input_artifacts"] == ["src/target.py"]
    restored = Delegation.from_dict(payload)
    assert restored.task == delegation.task
    assert restored.input_artifacts == delegation.input_artifacts
    assert restored == delegation


def test_agent_task_declaration_is_parsed_and_absent_is_declared():
    declared = parse_agent_task(
        "## Delegación agentiva\n\n- **Task:** do the thing\n"
        "- **Scope:** `a/b.py`\n"
    )
    assert declared.declared is True
    assert declared.task == "do the thing"
    assert declared.scope == ("a/b.py",)
    assert declared.scope_declared is True

    absent = parse_agent_task("## Objetivo\n\nNothing declared.\n")
    assert absent.declared is False
    assert absent.section_present is False

    empty = parse_agent_task("## Delegación agentiva\n\n<!-- placeholder -->\n")
    assert empty.declared is False
    assert empty.section_present is True


# --------------------------------------------------------------------------- #
# 3-4. The invocation boundary
# --------------------------------------------------------------------------- #


def test_agent_invoker_protocol_shape():
    """The boundary is exactly one method plus a kind, like WorkerAdapter."""
    invoker = NullAgentInvoker()
    assert hasattr(invoker, "kind")
    assert callable(invoker.invoke)
    request = AgentInvocationRequest(
        task="t", prompt="p", root=".", scope=(), input_artifacts=(),
        verification_commands=(), max_steps=1, delegation_id="d",
    )
    assert isinstance(invoker.invoke(request), AgentInvocationResult)


def test_null_agent_invoker_reports_not_executed_honestly():
    result = NullAgentInvoker().invoke(
        AgentInvocationRequest(
            task="t", prompt="p", root=".", scope=(), input_artifacts=(),
            verification_commands=(), max_steps=1, delegation_id="d",
        )
    )
    assert result.status == INVOCATION_NOT_EXECUTED
    assert result.steps == 0
    assert result.reported_commands == ()
    assert any(
        problem.get("signal") == NOT_APPLICABLE
        for problem in result.reported_problems
    )
    assert result.reported_pending  # it says what remained pending
    # It never fabricates work.
    assert "not executed" in result.summary


def test_invocation_status_vocabulary_is_closed():
    with pytest.raises(AgentWorkerError):
        AgentInvocationResult(status="whatever")


# --------------------------------------------------------------------------- #
# 5-6. The worker really works and really produces a WorkerResult
# --------------------------------------------------------------------------- #


def test_agent_worker_executes_through_injected_invoker_and_persists_result():
    root = make_repo("agent-work")
    store = OrchestratorStore(root)
    invoker = RecordingInvoker()
    worker = AgentWorker(invoker=invoker)

    result = worker.execute(
        make_delegation(root), store=store, run_id="run-01",
        plan_rel=f"docs/plans/{PLAN_NAME}",
    )

    # The invoker really received the materialized request.
    assert len(invoker.requests) == 1
    request = invoker.requests[0]
    assert request.task == "Make the target module report the marker."
    assert request.scope == ("src/target.py", "tests/test_target.py")
    assert "task: Make the target module report the marker." in request.prompt
    assert request.verification_commands == (("python", "src/check_ok.py"),)

    # The work really happened in the repository.
    assert (root / "src" / "target.py").read_text(encoding="utf-8").endswith(
        'marker = "after"\n'
    )
    assert "src/target.py" in result.artifacts_modified

    # Verification really ran and was classified.
    assert [entry["signal"] for entry in result.results] == [VALID]
    assert result.commands_executed[0]["exit_code"] == 0

    # The result is persisted, contract-valid, and re-readable.
    assert validate_worker_result(result.to_dict()) == ()
    stored = store.read_worker_result(PLAN_NUMBER, result.delegation_id)
    assert stored is not None
    assert stored.result_id == result.result_id
    assert stored.worker_kind == "agent"

    # The transcript and the request are persisted as evidence.
    kinds = {entry["kind"] for entry in result.evidence}
    assert "agent-transcript" in kinds
    assert "agent-request" in kinds
    transcript = store.read_run_artifact(
        PLAN_NUMBER, "run-01/it0001/agent-transcript.txt"
    )
    assert transcript and "observe: read src/target.py" in transcript


def test_agent_worker_result_id_is_deterministic_per_delegation():
    root = make_repo("agent-idempotent")
    store = OrchestratorStore(root)
    delegation = make_delegation(root)
    first = AgentWorker(invoker=RecordingInvoker()).execute(
        delegation, store=store, run_id="run-01"
    )
    second = AgentWorker(invoker=RecordingInvoker()).execute(
        delegation, store=store, run_id="run-02"
    )
    assert first.result_id == second.result_id == f"{delegation.delegation_id}-result"


# --------------------------------------------------------------------------- #
# 7-9. What the worker may never declare
# --------------------------------------------------------------------------- #


def test_agent_worker_never_claims_completion():
    root = make_repo("agent-claims")
    result = AgentWorker(invoker=RecordingInvoker()).execute(
        make_delegation(root), store=OrchestratorStore(root), run_id="run-01"
    )
    assert result.claims["self_reported_completion"] is False
    assert result.recommended_next_action["advisory"] is True
    assert result.recommended_next_action["action"] is None


def test_agent_worker_cannot_declare_closed():
    """No field of the result can express a derived lifecycle condition."""
    root = make_repo("agent-closed")
    result = AgentWorker(invoker=RecordingInvoker()).execute(
        make_delegation(root), store=OrchestratorStore(root), run_id="run-01"
    )
    payload = result.to_dict()
    # The closed vocabulary of derived conditions cannot appear as a result field.
    for condition in ("Closed", "Executed", "Verified", "Released"):
        assert condition not in payload
    assert set(payload) - {"schema_version", "result_id", "delegation_id",
                           "plan", "iteration", "created_at", "status",
                           "worker", "claims", "limitations"} == set(
        WORKER_RESULT_FIELDS
    )


def test_agent_worker_cannot_resolve_human_authority():
    boundary = AuthorityBoundary(plan_authorized=True)
    for action in (
        "RESOLVE_FINDING",
        "RESOLVE_PENDING_DECISION",
        "APPROVE_PLAN",
        "ACCEPT_RFC",
        "CHANGE_SCOPE",
        "DECIDE_ADR_WORTHINESS",
    ):
        assert boundary.evaluate(action).verdict == FORBIDDEN
    for action in ("RELEASE", "TAG", "PROMOTE", "PUBLISH"):
        assert boundary.evaluate(action).verdict == FORBIDDEN


def test_recommendation_is_never_an_authorization():
    # A recommendation naming a real derived action is still not an authority:
    # the host derives from evidence, it never consumes the recommendation.
    assert recommended_action_is_authority(
        RUN_IMPLEMENTATION_TASK, RUN_IMPLEMENTATION_TASK
    ) is False
    assert recommended_action_is_authority("RUN_VALIDATION", "RUN_VALIDATION") is False
    # An action only a recommendation could name is not authority either.
    assert recommended_action_is_authority(
        "STOP_AND_ESCALATE", "STOP_AND_ESCALATE"
    ) is True
    # No recommendation is not authority by definition.
    assert recommended_action_is_authority(RUN_IMPLEMENTATION_TASK, None) is False

    # And the derivation does not read any recommendation at all.
    root = make_repo("agent-recommendation")
    host = ExecutionHost(root, PLAN_NUMBER, worker=AgentWorker(invoker=RecordingInvoker()))
    host.run(max_iterations=1)
    journal = host.store.read_journal(PLAN_NUMBER)
    assert journal
    # The recorded action came from the derivation, not from a recommendation.
    assert journal[0]["action"] in (RUN_IMPLEMENTATION_TASK,)


# --------------------------------------------------------------------------- #
# 10-11. Scope: authorized vs forbidden
# --------------------------------------------------------------------------- #


def test_scope_valid_is_accepted_and_recorded():
    root = make_repo("agent-scope-valid")
    store = OrchestratorStore(root)
    delegation = make_delegation(root)
    result = AgentWorker(invoker=RecordingInvoker(outside_scope=False)).execute(
        delegation, store=store, run_id="run-01"
    )
    authorized = set(delegation.declared_scope)
    assert set(result.artifacts_modified) <= authorized


def test_scope_invalid_stops_with_forbidden_action_and_requires_human():
    root = make_repo("agent-scope-invalid", extra_scope="")
    store = OrchestratorStore(root)
    host = ExecutionHost(
        root, PLAN_NUMBER,
        worker=AgentWorker(invoker=RecordingInvoker(outside_scope=True)),
    )
    run = host.run()

    assert run.terminal_action == STOP_FORBIDDEN_ACTION
    terminal = run.records[-1]
    assert terminal["authority"]["verdict"] == REQUIRES_HUMAN
    assert "src/unrelated.py" in terminal["rationale"]
    # The host detected it from the repository, not from the worker's claim.
    assert any(
        "scope violation detected by the host" in note
        for note in terminal.get("notes") or ()
    )


def test_forbidden_scope_action_names_the_violation_and_the_authorized_scope():
    decision = AuthorityBoundary(plan_authorized=True)
    action = forbidden_scope_action(
        decision, "d-1", ["src/out.py"], ["src/in.py"]
    )
    assert action.kind == STOP_FORBIDDEN_ACTION
    assert action.terminal is True
    assert "src/out.py" in action.rationale
    assert "src/in.py" in action.rationale
    assert action.evidence_refs == ("src/out.py",)
    assert action.authority is not None
    assert action.authority.verdict == REQUIRES_HUMAN


# --------------------------------------------------------------------------- #
# 12-13. Ingestion and derivation on the post-ingestion state
# --------------------------------------------------------------------------- #


def test_host_ingests_and_records_the_result_ids():
    root = make_repo("agent-ingest")
    host = ExecutionHost(root, PLAN_NUMBER, worker=AgentWorker(invoker=RecordingInvoker()))
    run = host.run(max_iterations=1)
    record = run.records[0]
    assert record["delegation_id"] is not None
    assert record["result_id"] is not None
    stored = host.store.read_worker_result(PLAN_NUMBER, record["delegation_id"])
    assert stored is not None
    assert stored.result_id == record["result_id"]


def test_derivation_runs_the_implementation_task_before_validation():
    """The work comes first: validating before it would evidence the wrong state."""
    root = make_repo("agent-order")
    observation = observe(root, PLAN_NUMBER, OrchestratorStore(root))
    assert observation.agent_task.declared is True
    assert observation.implementation_done_for_current_state is False
    action = derive_next_action(
        observation, AuthorityBoundary(plan_authorized=True)
    )
    assert action.kind == RUN_IMPLEMENTATION_TASK
    assert action.authority is not None
    assert action.authority.verdict == AUTHORIZED_EXISTING


def test_derivation_uses_post_ingestion_state_and_does_not_repeat_the_task():
    root = make_repo("agent-post-ingestion")
    store = OrchestratorStore(root)
    host = ExecutionHost(
        root, PLAN_NUMBER, store=store,
        worker=AgentWorker(invoker=RecordingInvoker()), max_iterations=2,
    )
    run = host.run()

    actions = [record["action"] for record in run.records]
    assert actions[0] == RUN_IMPLEMENTATION_TASK
    # Once the result exists for the current content state, the implementation
    # task is not derived again: the derivation reads the post-ingestion state.
    assert actions.count(RUN_IMPLEMENTATION_TASK) == 1
    observation = observe(root, PLAN_NUMBER, store)
    assert observation.implementation_done_for_current_state is True


def test_plan_without_agent_task_delegates_no_semantic_work():
    root = make_repo("agent-no-task", agent_task=False)
    observation = observe(root, PLAN_NUMBER, OrchestratorStore(root))
    assert observation.agent_task.declared is False
    action = derive_next_action(
        observation, AuthorityBoundary(plan_authorized=True)
    )
    assert action.kind != RUN_IMPLEMENTATION_TASK


def test_implementation_task_requires_an_authorized_plan():
    root = make_repo("agent-unauthorized")
    plan_path = root / "docs" / "plans" / PLAN_NAME
    plan_path.write_text(
        plan_path.read_text(encoding="utf-8").replace(
            "**Status:** Aprobado para ejecución", "**Status:** Aprobado para redacción"
        ),
        encoding="utf-8",
    )
    _git(root, "add", "-A")
    _git(root, "commit", "-qm", "unauthorized")
    observation = observe(root, PLAN_NUMBER, OrchestratorStore(root))
    action = derive_next_action(
        observation, AuthorityBoundary(plan_authorized=False)
    )
    assert action.kind != RUN_IMPLEMENTATION_TASK


# --------------------------------------------------------------------------- #
# 14-15. Incomplete work and the human boundary
# --------------------------------------------------------------------------- #


def test_incomplete_invocation_produces_a_declared_gap_not_a_success():
    root = make_repo("agent-incomplete")
    result = AgentWorker(
        invoker=RecordingInvoker(status=INVOCATION_INCOMPLETE)
    ).execute(make_delegation(root), store=OrchestratorStore(root), run_id="run-01")
    assert result.status == INVOCATION_INCOMPLETE
    signals = [problem["signal"] for problem in result.problems]
    assert GAP in signals
    assert result.claims["self_reported_completion"] is False


def test_verification_failure_makes_the_result_incomplete_even_if_agent_finished():
    """The repository contradicting the agent is not a success."""
    root = make_repo("agent-verify-fail", extra_scope="python src/check_fail.py\n")
    (root / "src" / "check_fail.py").write_text(
        "import sys\nprint('boom')\nsys.exit(1)\n", encoding="utf-8"
    )
    _git(root, "add", "-A")
    _git(root, "commit", "-qm", "failing verification")
    store = OrchestratorStore(root)
    # The delegated command-set is the plan's declared verification, as observed.
    observed = observe(root, PLAN_NUMBER, store)
    result = AgentWorker(invoker=RecordingInvoker()).execute(
        make_delegation(root, command_set=observed.command_set),
        store=store, run_id="run-01",
    )
    assert result.status == INVOCATION_INCOMPLETE
    assert any(problem["signal"] == "FAIL" for problem in result.problems)
    assert result.claims["self_reported_completion"] is False


def test_invocation_claiming_an_unobserved_command_is_a_declared_gap():
    """A claim without a trace is not evidence — and it is not an ANOMALY either.

    The invocation reports truthfully; the delegation's declared command-set is
    read from the plan and may change between attempts, so a truthful report can
    name a command the current attempt did not run. It is recorded as a declared
    GAP and left for the host's own validation to settle.
    """
    root = make_repo("agent-claim-gap")
    result = AgentWorker(
        invoker=RecordingInvoker(
            reported_commands=(("python", "never-ran.py"),)
        )
    ).execute(make_delegation(root), store=OrchestratorStore(root), run_id="run-01")
    signals = [problem["signal"] for problem in result.problems]
    assert GAP in signals
    assert ANOMALY not in signals


def test_reported_command_matching_the_delegation_is_not_a_problem():
    root = make_repo("agent-claim-declared")
    delegation = make_delegation(root)
    result = AgentWorker(
        invoker=RecordingInvoker(reported_commands=delegation.command_set)
    ).execute(delegation, store=OrchestratorStore(root), run_id="run-01")
    assert not result.problems
    assert result.status == INVOCATION_COMPLETED


def test_human_boundary_stops_with_requires_human_on_open_finding():
    root = make_repo("agent-human-boundary")
    plan_path = root / "docs" / "plans" / PLAN_NAME
    record = build_finding_record(
        plan=PLAN_NUMBER, index=1,
        observation="the agent found a defect requiring a human decision",
        evidence="synthetic", git_state="synthetic", provenance="agent worker test",
    )
    decision = AuthorityDecision(
        action="RECORD_FINDING", verdict=AUTHORIZED_EXISTING,
        basis="synthetic", reason="synthetic",
    )
    plan_path.write_text(
        plan_path.read_text(encoding="utf-8")
        + "\n## Findings / Correcciones / Pending\n\n### Findings\n\n",
        encoding="utf-8",
    )
    assert write_finding(
        decision=decision, plan_path=plan_path, record=record
    ) is True
    _git(root, "add", "-A")
    _git(root, "commit", "-qm", "finding")

    host = ExecutionHost(root, PLAN_NUMBER, worker=AgentWorker(invoker=RecordingInvoker()))
    run = host.run()
    assert run.terminal_action in (
        "STOP_OPEN_FINDINGS", "STOP_FINDING_REQUIRES_HUMAN"
    )
    terminal = run.records[-1]
    assert terminal["authority"]["verdict"] == REQUIRES_HUMAN
    assert "F-01" in terminal["rationale"]


# --------------------------------------------------------------------------- #
# 16. Restart / recovery without process memory
# --------------------------------------------------------------------------- #


def test_recovery_after_restart_from_persisted_evidence_only():
    root = make_repo("agent-recovery")
    store = OrchestratorStore(root)
    first_host = ExecutionHost(
        root, PLAN_NUMBER, store=store,
        worker=AgentWorker(invoker=RecordingInvoker()), max_iterations=1,
        run_id="run-01",
    )
    first = first_host.run()
    assert first.records[0]["action"] == RUN_IMPLEMENTATION_TASK

    # A brand-new host instance, with no state carried over, reconstructs from
    # the repository and the persisted evidence.
    second_host = ExecutionHost(
        root, PLAN_NUMBER, store=OrchestratorStore(root),
        worker=AgentWorker(invoker=RecordingInvoker()), run_id="run-02",
    )
    report = second_host.reconstruct("run-01")
    assert "RUN_IMPLEMENTATION_TASK" in report
    assert "agent-transcript" not in report  # the report cites evidence, not content

    observation = second_host.observe()
    assert observation.implementation_done_for_current_state is True
    # The reconstructed position is not "do the implementation again".
    action = derive_next_action(
        observation, AuthorityBoundary(plan_authorized=observation.authorized_for_execution)
    )
    assert action.kind != RUN_IMPLEMENTATION_TASK


def test_agent_transcript_is_readable_after_restart():
    root = make_repo("agent-transcript-restart")
    store = OrchestratorStore(root)
    result = AgentWorker(invoker=RecordingInvoker()).execute(
        make_delegation(root), store=store, run_id="run-01"
    )
    fresh_store = OrchestratorStore(root)
    stored = fresh_store.read_worker_result(PLAN_NUMBER, result.delegation_id)
    assert stored is not None
    for entry in stored.evidence:
        if entry["kind"] == "agent-transcript":
            text = fresh_store.read_run_artifact(PLAN_NUMBER, entry["path"])
            assert text is not None and text.strip()


# --------------------------------------------------------------------------- #
# 17-19. Findings, revalidation and the exit-code rule
# --------------------------------------------------------------------------- #


def test_finding_blocks_closure_until_resolved_and_revalidation_is_derivable():
    root = make_repo("agent-revalidation")
    store = OrchestratorStore(root)

    # The agent performs the work; the host ingests it.
    host = ExecutionHost(
        root, PLAN_NUMBER, store=store,
        worker=AgentWorker(invoker=RecordingInvoker()), max_iterations=1,
    )
    host.run()

    # A finding registered on the plan stops the loop.
    plan_path = root / "docs" / "plans" / PLAN_NAME
    plan_path.write_text(
        plan_path.read_text(encoding="utf-8")
        + "\n## Findings / Correcciones / Pending\n\n### Findings\n\n",
        encoding="utf-8",
    )
    write_finding(
        decision=AuthorityDecision(
            action="RECORD_FINDING", verdict=AUTHORIZED_EXISTING,
            basis="synthetic", reason="synthetic",
        ),
        plan_path=plan_path,
        record=build_finding_record(
            plan=PLAN_NUMBER, index=1, observation="real defect found during work",
            evidence="synthetic", git_state="synthetic", provenance="agent worker",
        ),
    )
    observation = observe(root, PLAN_NUMBER, store)
    action = derive_next_action(
        observation, AuthorityBoundary(plan_authorized=True)
    )
    assert action.kind in ("STOP_OPEN_FINDINGS", "STOP_FINDING_REQUIRES_HUMAN")

    # Once the finding is resolved by the human, the loop can proceed to
    # validation again (revalidation is derived from evidence, not declared).
    text = plan_path.read_text(encoding="utf-8").replace(
        "estado: open", "estado: resolved"
    )
    plan_path.write_text(text, encoding="utf-8")
    observation = observe(root, PLAN_NUMBER, store)
    action = derive_next_action(
        observation, AuthorityBoundary(plan_authorized=True)
    )
    assert action.kind in ("RUN_VALIDATION", "RECORD_VALIDATION_ANCHOR")


def test_stale_validation_does_not_allow_closed():
    """Changing scoped content after a validation makes the anchor stale."""
    root = make_repo("agent-stale")
    store = OrchestratorStore(root)
    host = ExecutionHost(root, PLAN_NUMBER, store=store,
                         worker=AgentWorker(invoker=RecordingInvoker()))
    # A full run that cannot reach Closed: nothing was validated yet.
    run = host.run(max_iterations=3)
    assert run.derived_conditions["Closed"] is False


def test_exit_code_zero_is_not_completion():
    root = make_repo("agent-exit-code")
    result = AgentWorker(invoker=RecordingInvoker()).execute(
        make_delegation(root), store=OrchestratorStore(root), run_id="run-01"
    )
    assert result.results[0]["exit_code"] == 0
    assert result.results[0]["signal"] == VALID
    # ... and the worker still refuses to claim the change is complete.
    assert result.claims["self_reported_completion"] is False
    assert result.limitations


# --------------------------------------------------------------------------- #
# 20. Dependency injection of an external invoker
# --------------------------------------------------------------------------- #


def test_external_agent_invoker_can_replace_the_null_one():
    root = make_repo("agent-injection")
    store = OrchestratorStore(root)

    null_result = AgentWorker().execute(
        make_delegation(root, delegation_id="null-run"),
        store=store, run_id="run-null",
    )
    assert null_result.status == INVOCATION_NOT_EXECUTED
    assert null_result.artifacts_modified == ()

    injected = AgentWorker(invoker=RecordingInvoker())
    injected_result = injected.execute(
        make_delegation(root, delegation_id="injected-run"),
        store=store, run_id="run-injected",
    )
    assert injected_result.status == INVOCATION_COMPLETED
    assert "src/target.py" in injected_result.artifacts_modified
    assert injected_result.authority_used["invoker"] == "recording"


def test_agent_worker_is_a_worker_adapter_like_the_others():
    """The three workers share one boundary and one result contract."""
    for worker in (CommandWorker(), NullWorker(), AgentWorker()):
        assert isinstance(getattr(worker, "kind"), str)
        assert callable(worker.execute)
    root = make_repo("agent-boundary")
    store = OrchestratorStore(root)
    delegation = make_delegation(root)
    for worker in (NullWorker(), AgentWorker(invoker=RecordingInvoker())):
        result = worker.execute(delegation, store=store, run_id="run-x")
        assert isinstance(result, WorkerResult)
        assert validate_worker_result(result.to_dict()) == ()


def test_result_contract_is_unchanged():
    """Plan 123 adds no field to the M4 contract."""
    assert WORKER_RESULT_FIELDS == (
        "delegation_received",
        "intended_actions",
        "performed_actions",
        "artifacts_modified",
        "commands_executed",
        "results",
        "evidence",
        "problems",
        "pending",
        "recommended_next_action",
        "authority_used",
        "effects_executed",
    )


def test_invalid_agent_result_fails_the_m4_contract():
    payload = {
        "schema_version": "1",
        "result_id": "x",
        "delegation_id": "d",
        "plan": 1,
        "iteration": 0,
        "created_at": "t",
        "status": "completed",
        "worker": {"kind": "agent"},
    }
    problems = validate_worker_result(payload)
    assert problems  # missing contract fields
    with pytest.raises(ContractError):
        WorkerResult.from_dict({"schema_version": "1"})


# --------------------------------------------------------------------------- #
# 21. The journal read declares the evidence it could not read
# --------------------------------------------------------------------------- #


def test_journal_read_reports_the_lines_it_could_not_read():
    root = make_repo("agent-journal-gaps")
    store = OrchestratorStore(root)
    store.append_iteration(PLAN_NUMBER, {"iteration": 1, "action": "RUN_VALIDATION"})
    journal_path = store.journal_path(PLAN_NUMBER)
    with journal_path.open("a", encoding="utf-8", newline="\n") as handle:
        handle.write("{ this is not json }\n")
    store.append_iteration(PLAN_NUMBER, {"iteration": 2, "action": "RECORD_CHECKPOINT"})

    read = store.read_journal_with_gaps(PLAN_NUMBER)
    assert len(read.records) == 2
    assert read.malformed_lines == (2,)
    notes = read.gap_notes()
    assert len(notes) == 1
    assert "line 2" in notes[0]
    assert "GAP" in notes[0]
    # The convenience view still yields the readable records only.
    assert len(store.read_journal(PLAN_NUMBER)) == 2


def test_observation_declares_unreadable_journal_lines_as_gap():
    root = make_repo("agent-observation-gap")
    store = OrchestratorStore(root)
    store.append_iteration(PLAN_NUMBER, {"iteration": 1, "action": "RUN_VALIDATION"})
    with store.journal_path(PLAN_NUMBER).open("a", encoding="utf-8", newline="\n") as handle:
        handle.write("not-json\n")

    observation = observe(root, PLAN_NUMBER, store)
    assert observation.journal_gaps
    assert any("line 2" in note for note in observation.journal_gaps)
    # The absence is declared in the observation's gaps, not silently dropped.
    assert any("line 2" in gap for gap in observation.gaps)
    assert observation.journal_gaps == store.read_journal_with_gaps(
        PLAN_NUMBER
    ).gap_notes()


def test_well_formed_journal_declares_no_gap():
    root = make_repo("agent-journal-clean")
    store = OrchestratorStore(root)
    store.append_iteration(PLAN_NUMBER, {"iteration": 1, "action": "RUN_VALIDATION"})
    read = store.read_journal_with_gaps(PLAN_NUMBER)
    assert read.malformed_lines == ()
    assert read.gap_notes() == ()
    assert observe(root, PLAN_NUMBER, store).journal_gaps == ()


# --------------------------------------------------------------------------- #
# 22. A delegation's own change is observable on an already-dirty tree
# --------------------------------------------------------------------------- #


def test_artifacts_modified_is_observed_even_when_the_path_was_already_dirty():
    """`git status` alone cannot attribute a change to a delegation.

    A scoped path that is already modified when the delegation starts yields the
    same dirty answer before and after, so a dirty-path comparison would report
    no change at all. The content snapshot reports the real one.
    """
    root = make_repo("agent-dirty-scope")
    store = OrchestratorStore(root)
    # The target path is modified *before* the delegation, and never committed.
    (root / "src" / "target.py").write_text(
        '"""Target module."""\n\nmarker = "dirty-before"\n', encoding="utf-8"
    )
    delegation = make_delegation(root, delegation_id="dirty-run")
    result = AgentWorker(invoker=RecordingInvoker()).execute(
        delegation, store=store, run_id="run-01"
    )
    assert "src/target.py" in result.artifacts_modified
    assert result.status == INVOCATION_COMPLETED
    scope_evidence = [
        entry for entry in result.evidence if entry["kind"] == "scope-observation"
    ]
    assert scope_evidence and "src/target.py" in scope_evidence[0]["note"]


def test_scope_violation_is_detected_even_when_the_scope_path_was_already_dirty():
    root = make_repo("agent-dirty-violation")
    (root / "src" / "unrelated.py").write_text("x = 0\n", encoding="utf-8")
    _git(root, "add", "-A")
    _git(root, "commit", "-qm", "seed unrelated")
    # Dirty the scoped path first, then have the worker write outside the scope.
    (root / "src" / "target.py").write_text(
        '"""Target module."""\n\nmarker = "dirty-before"\n', encoding="utf-8"
    )
    host = ExecutionHost(
        root, PLAN_NUMBER,
        worker=AgentWorker(invoker=RecordingInvoker(outside_scope=True)),
    )
    run = host.run()
    assert run.terminal_action == STOP_FORBIDDEN_ACTION
    assert run.records[-1]["authority"]["verdict"] == REQUIRES_HUMAN


def test_repository_snapshot_and_changed_paths_are_content_based():
    from runtime.orchestrator.worker import changed_paths, repository_snapshot

    root = make_repo("agent-snapshot")
    before = repository_snapshot(root)
    (root / "src" / "target.py").write_text("changed\n", encoding="utf-8")
    (root / "src" / "brand_new.py").write_text("new\n", encoding="utf-8")
    after = repository_snapshot(root)
    changed = changed_paths(before, after)
    assert "src/target.py" in changed
    assert "src/brand_new.py" in changed
    (root / ".project" / "orchestrator").mkdir(parents=True, exist_ok=True)
    (root / ".project" / "orchestrator" / "x.json").write_text("{}", encoding="utf-8")
    assert ".project/orchestrator/x.json" not in repository_snapshot(root)


def test_empty_implementation_result_does_not_re_delegate_forever():
    """A finished implementation that changed nothing here is already satisfied."""
    root = make_repo("agent-no-repeat")
    store = OrchestratorStore(root)
    delegation = make_delegation(root)
    AgentWorker(invoker=RecordingInvoker()).execute(
        delegation, store=store, run_id="run-01"
    )
    host = ExecutionHost(root, PLAN_NUMBER, store=store,
                         worker=AgentWorker(invoker=RecordingInvoker()))
    run = host.run(max_iterations=2)
    assert RUN_IMPLEMENTATION_TASK in [record["action"] for record in run.records]
    observation = host.observe()
    assert observation.implementation_done_for_current_state is True
    action = derive_next_action(
        observation,
        AuthorityBoundary(plan_authorized=observation.authorized_for_execution),
    )
    assert action.kind != RUN_IMPLEMENTATION_TASK
