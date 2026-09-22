"""Behaviour tests of the DEV Autonomous Orchestrator (plan 122 §13).

These tests exercise the host's **behaviour over a real repository**: a
throw-away git repository is built per test and the host really observes it,
really delegates, really executes commands and really writes records into the
throw-away plan artifact. Nothing here checks the presence of files.

They deliberately do **not** use pytest's ``tmp_path``: the throw-away git
repositories built here must not be nested in the repository under test, so a
scratch directory is created explicitly **outside** the repository (see
``tests/pytest_isolation.py``) and is overridable through
``ARGENTOS_ORCHESTRATOR_SCRATCH``. The tests are deterministic and independent of
``protocol/``.
"""

from __future__ import annotations

import ast
import inspect
import json
import os
import shutil
import subprocess
import sys
import uuid
from pathlib import Path
from typing import Protocol

import pytest

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT))
sys.path.insert(0, str(REPO_ROOT / "tests"))

import pytest_isolation  # noqa: E402

from runtime.orchestrator.authority import AuthorityBoundary  # noqa: E402
from runtime.orchestrator.contracts import (  # noqa: E402
    ANOMALY,
    AUTHORIZED_EXISTING,
    FORBIDDEN,
    GAP,
    REQUIRES_HUMAN,
    VALID,
    WORKER_RESULT_FIELDS,
    AuthorityDecision,
    Delegation,
    WorkerResult,
    canonical_json,
    validate_worker_result,
)
from runtime.orchestrator.derivation import derive_next_action  # noqa: E402
from runtime.orchestrator.governance import (  # noqa: E402
    GovernanceError,
    record_validation_anchor,
)
from runtime.orchestrator.host import ExecutionHost  # noqa: E402
from runtime.orchestrator.observation import (  # noqa: E402
    ObservationError,
    git_state,
    observe,
)
from runtime.orchestrator.store import OrchestratorStore  # noqa: E402
from runtime.orchestrator.worker import (  # noqa: E402
    CommandWorker,
    NullWorker,
    WorkerAdapter,
)

SCRATCH_ROOT = Path(
    os.environ.get(
        "ARGENTOS_ORCHESTRATOR_SCRATCH",
        str(pytest_isolation.scratch_root("orchestrator")),
    )
)

PLAN_NUMBER = 200
PLAN_NAME = f"{PLAN_NUMBER}-fake-change.md"

GATE_SCRIPTS = {
    "check_lifecycle_anchor.py": "C-1",
    "check_lifecycle_checkpoint.py": "C-2",
    "check_lifecycle_lineage.py": "C-3",
}

GATE_SCRIPT = '''"""Synthetic lifecycle gate used only by the orchestrator test suite."""
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
print(f"- docs/plans/{config.get('plan', '200-fake-change.md')}: {signal} - synthetic gate")
sys.exit(1 if signal in ("ANOMALY", "BOUNDARY") else 0)
'''

CHECK_OK = """import sys
print("ok")
sys.exit(0)
"""

CHECK_FAIL = """import sys
print("synthetic failure")
sys.exit(1)
"""


def _scratch(name: str) -> Path:
    # The isolated scratch root lives outside the repository and is cleared by
    # the root conftest at session start, so an interrupted run cannot
    # accumulate throw-away repositories.
    path = SCRATCH_ROOT / f"{name}-{uuid.uuid4().hex[:8]}"
    path.mkdir(parents=True, exist_ok=True)
    return path


def plan_text(
    *,
    status: str = "Aprobado para ejecución",
    entry_checked: bool = True,
    pending_blocking: bool = False,
    finding_open: bool = False,
    environmental: bool = False,
    extra_command: str | None = None,
    validation_exits_zero: bool = True,
    gate_commands: bool = True,
) -> str:
    """A plan artifact exercising the containers the host reads."""
    entry = "x" if entry_checked else " "
    commands = ["python src/check_ok.py"]
    if not validation_exits_zero:
        commands = ["python src/check_fail.py"]
    if extra_command:
        commands.append(extra_command)
    declaration = ""
    if environmental:
        declaration = (
            "# environmental-class: python src/check_fail.py -> synthetic declared "
            "environmental class: the evidence is not obtainable here\n"
        )
    verification = "\n".join(commands)
    pending = (
        "- `<PLAN-200>` — decisión: synthetic; blocking: **sí**; owner: mantenedor; "
        "resolución: **pendiente**; evidencia: synthetic; ADR-worthiness: no aplica."
        if pending_blocking
        else "- `<PLAN-200>` — decisión: synthetic; blocking: **no**; owner: mantenedor; "
        "resolución: **pendiente**; evidencia: synthetic; ADR-worthiness: no aplica."
    )
    findings = (
        "- `PLAN-200:F-01` — estado: open; observación: synthetic; "
        "evidencia original: synthetic; estado Git observado: synthetic; "
        "provenance original: synthetic"
        if finding_open
        else "N/A — sin registros reales."
    )
    return f"""# Plan 200 — synthetic change for the orchestrator suite

**Status:** {status}
**Fecha:** 2026-09-14
**RFC:** — (synthetic)
**Clase:** — (synthetic)
**Change Level:** L2
**Depende de:** —
**Origen:** synthetic test fixture

## Objetivo

Synthetic change driven by the DEV Autonomous Orchestrator test suite.

## Criterio de entrada

- [{entry}] synthetic entry criterion satisfied

## Entregables

1. `src/a.txt` — synthetic deliverable.

## Pasos

1. Nothing to do.

## Criterios de salida

- [ ] synthetic

## Verificación

```bash
{verification}
{declaration}```

## Validation anchor

<!-- empty on purpose -->

---

## Checkpoint / cierre

<!-- empty on purpose -->

---

## Findings / Correcciones / Pending

### Findings

{findings}

### Correcciones

N/A

### Pending decisions

{pending}

## Nota de ejecución
"""


def build_repo(
    path: Path,
    *,
    plan: str | None = None,
    index_registered: bool = True,
    extra_files: dict[str, str] | None = None,
    gate_commands: bool = True,
) -> Path:
    """Create a real, committed git repository with a plan artifact."""
    (path / "docs" / "plans").mkdir(parents=True, exist_ok=True)
    (path / "src").mkdir(parents=True, exist_ok=True)
    (path / "src" / "a.txt").write_text("initial content\n", encoding="utf-8")
    (path / "src" / "check_ok.py").write_text(CHECK_OK, encoding="utf-8")
    (path / "src" / "check_fail.py").write_text(CHECK_FAIL, encoding="utf-8")
    (path / "docs" / "plans" / PLAN_NAME).write_text(
        plan if plan is not None else plan_text(), encoding="utf-8"
    )
    (path / "docs" / "plans" / "INDEX.md").write_text(
        f"# Plans index\n\n| Plan |\n|---|\n| `{PLAN_NAME}` |\n"
        if index_registered
        else "# Plans index\n",
        encoding="utf-8",
    )
    # The orchestration evidence area is ephemeral and never staged, exactly as
    # in the repository (``.project/`` is gitignored there).
    (path / ".gitignore").write_text(".project/\n", encoding="utf-8")
    if gate_commands:
        (path / "tools").mkdir(parents=True, exist_ok=True)
        for name in GATE_SCRIPTS:
            (path / "tools" / name).write_text(GATE_SCRIPT, encoding="utf-8")
        (path / ".gate_signals.json").write_text(
            json.dumps({"plan": PLAN_NAME}), encoding="utf-8"
        )
    for rel, content in (extra_files or {}).items():
        target = path / rel
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(content, encoding="utf-8")

    subprocess.run(["git", "init", "-q"], cwd=path, check=True)
    subprocess.run(["git", "add", "-A"], cwd=path, check=True)
    subprocess.run(
        [
            "git",
            "-c",
            "user.email=orch@example.invalid",
            "-c",
            "user.name=Orchestrator Suite",
            "commit",
            "-q",
            "-m",
            "synthetic baseline",
        ],
        cwd=path,
        check=True,
    )
    return path


def gate_commands(prefix: str = "tools") -> tuple[tuple[str, ...], ...]:
    return tuple(
        ("python", f"{prefix}/{name}") for name in GATE_SCRIPTS
    )


def stage(repo: Path) -> None:
    """Stage the intentional change, as the evidence rule requires before validating."""
    subprocess.run(["git", "add", "-A"], cwd=repo, check=True)


def set_gate_signal(repo: Path, gate: str, signal: str) -> None:
    config_path = repo / ".gate_signals.json"
    config = json.loads(config_path.read_text(encoding="utf-8"))
    config[gate] = signal
    config_path.write_text(json.dumps(config), encoding="utf-8")


def make_host(repo: Path, **kwargs) -> ExecutionHost:
    kwargs.setdefault("gate_commands", gate_commands())
    kwargs.setdefault("worker", CommandWorker(timeout_seconds=120))
    return ExecutionHost(repo, PLAN_NUMBER, **kwargs)


# --------------------------------------------------------------------------- #
# Derivation of the next action
# --------------------------------------------------------------------------- #


def test_derives_run_validation_when_no_anchor_is_recorded():
    repo = build_repo(_scratch("derive-first"))
    observation = observe(repo, PLAN_NUMBER)
    boundary = AuthorityBoundary(plan_authorized=observation.authorized_for_execution)
    action = derive_next_action(observation, boundary)
    assert action.kind == "RUN_VALIDATION"
    assert action.authority is not None
    assert action.authority.verdict == AUTHORIZED_EXISTING


def test_refuses_to_continue_without_plan_authorization():
    repo = build_repo(
        _scratch("unauthorized"), plan=plan_text(status="Aprobado para redacción")
    )
    observation = observe(repo, PLAN_NUMBER)
    boundary = AuthorityBoundary(plan_authorized=observation.authorized_for_execution)
    action = derive_next_action(observation, boundary)
    assert action.kind == "STOP_AWAIT_PLAN_AUTHORIZATION"
    assert action.terminal
    assert action.authority is not None
    assert action.authority.verdict == REQUIRES_HUMAN

    # And the boundary itself refuses every executable action without authority.
    unauthorized = AuthorityBoundary(plan_authorized=False)
    for kind in ("RUN_VALIDATION", "RUN_LIFECYCLE_GATES", "RECORD_VALIDATION_ANCHOR"):
        assert unauthorized.evaluate(kind).verdict == REQUIRES_HUMAN


def test_stops_when_entry_criteria_are_unmet():
    repo = build_repo(
        _scratch("entry"), plan=plan_text(entry_checked=False)
    )
    observation = observe(repo, PLAN_NUMBER)
    action = derive_next_action(
        observation, AuthorityBoundary(plan_authorized=True)
    )
    assert action.kind == "STOP_ENTRY_CRITERIA_UNMET"
    assert action.terminal


def test_stops_on_a_blocking_pending_decision():
    repo = build_repo(
        _scratch("pending"), plan=plan_text(pending_blocking=True)
    )
    observation = observe(repo, PLAN_NUMBER)
    assert observation.blocking_pending
    action = derive_next_action(
        observation, AuthorityBoundary(plan_authorized=True)
    )
    assert action.kind == "STOP_BLOCKING_PENDING_DECISION"


def test_stops_on_open_findings_that_need_human_resolution():
    repo = build_repo(_scratch("finding"), plan=plan_text(finding_open=True))
    observation = observe(repo, PLAN_NUMBER)
    assert observation.open_findings
    action = derive_next_action(
        observation, AuthorityBoundary(plan_authorized=True)
    )
    assert action.kind == "STOP_OPEN_FINDINGS"
    assert action.authority is not None
    assert action.authority.verdict == REQUIRES_HUMAN


def test_stale_validation_derives_revalidation_and_fresh_does_not():
    repo = build_repo(_scratch("stale"))
    host = make_host(repo, max_iterations=3)
    host.run()
    observation = observe(repo, PLAN_NUMBER)
    assert observation.anchor.present
    # The recorded anchor matches the validated content: no revalidation.
    assert not observation.anchor_stale
    assert (
        derive_next_action(
            observation, AuthorityBoundary(plan_authorized=True)
        ).kind
        != "RUN_REVALIDATION"
    )

    # Change a path inside the declared scope and stage it, as the evidence rule
    # requires: the anchor no longer describes the observed content.
    (repo / "src" / "a.txt").write_text("changed content\n", encoding="utf-8")
    stage(repo)
    stale = observe(repo, PLAN_NUMBER)
    assert stale.anchor_stale
    assert stale.anchor.delta_identity != stale.current_delta_identity
    action = derive_next_action(
        stale, AuthorityBoundary(plan_authorized=True)
    )
    assert action.kind == "RUN_REVALIDATION"
    assert action.authority is not None
    assert action.authority.verdict == AUTHORIZED_EXISTING


# --------------------------------------------------------------------------- #
# Authority boundary
# --------------------------------------------------------------------------- #


def test_release_is_forbidden_and_never_executed():
    boundary = AuthorityBoundary(plan_authorized=True)
    for kind in ("RELEASE", "TAG", "PROMOTE", "PUBLISH"):
        assert boundary.evaluate(kind).verdict == FORBIDDEN
    for kind in (
        "APPROVE_PLAN",
        "ACCEPT_RFC",
        "CHANGE_SCOPE",
        "RESOLVE_FINDING",
        "DECIDE_ADR_WORTHINESS",
    ):
        assert boundary.evaluate(kind).verdict == FORBIDDEN


def test_boundary_rejects_unknown_actions():
    decision = AuthorityBoundary(plan_authorized=True).evaluate("SOMETHING_ELSE")
    assert decision.verdict == FORBIDDEN


def test_records_cannot_be_written_without_existing_authority():
    repo = build_repo(_scratch("governance-guard"))
    plan_path = repo / "docs" / "plans" / PLAN_NAME
    before = plan_path.read_text(encoding="utf-8")
    unauthorized = AuthorityDecision(
        action="RECORD_VALIDATION_ANCHOR",
        verdict=REQUIRES_HUMAN,
        basis="none",
        reason="synthetic",
    )
    with pytest.raises(GovernanceError):
        record_validation_anchor(
            decision=unauthorized, plan_path=plan_path, body="should not land"
        )
    assert plan_path.read_text(encoding="utf-8") == before


def test_worker_recommendation_is_never_an_authorization():
    repo = build_repo(_scratch("recommendation"))
    delegation = Delegation(
        delegation_id="d1",
        plan=PLAN_NUMBER,
        iteration=1,
        action="RUN_VALIDATION",
        created_at="2026-01-01T00:00:00Z",
        authority_basis="synthetic",
        declared_scope=(),
        command_set=(("python", "src/check_ok.py"),),
        expected_evidence=(),
        worker_kind="command",
        worker_command=(),
    )
    result = CommandWorker(timeout_seconds=60).execute(
        delegation, store=OrchestratorStore(repo), run_id="r1"
    )
    assert result.recommended_next_action["advisory"] is True
    assert result.claims["self_reported_completion"] is False
    # The boundary still refuses a human-only action even though the worker
    # recommended continuing.
    assert (
        AuthorityBoundary(plan_authorized=True).evaluate("RELEASE").verdict
        == FORBIDDEN
    )


# --------------------------------------------------------------------------- #
# Signals: exit codes are not completion
# --------------------------------------------------------------------------- #


def test_exit_code_zero_is_not_workflow_completion():
    repo = build_repo(_scratch("exit-zero"))
    store = OrchestratorStore(repo)
    delegation = Delegation(
        delegation_id="d-zero",
        plan=PLAN_NUMBER,
        iteration=1,
        action="RUN_VALIDATION",
        created_at="2026-01-01T00:00:00Z",
        authority_basis="synthetic",
        declared_scope=(),
        command_set=(("python", "src/check_ok.py"),),
        expected_evidence=(),
        worker_kind="command",
        worker_command=(),
    )
    result = CommandWorker(timeout_seconds=60).execute(
        delegation, store=store, run_id="r-zero"
    )
    assert result.commands_executed[0]["exit_code"] == 0
    assert result.results[0]["signal"] == VALID
    assert result.claims["self_reported_completion"] is False
    # Exit 0 produced VALID evidence for one command, and no closure at all.
    observation = observe(repo, PLAN_NUMBER)
    assert observation.checkpoint.present is False
    assert not observation.anchor.present


def test_checker_classification_is_read_and_not_inferred_from_exit_code():
    repo = build_repo(_scratch("gate-anomaly"))
    set_gate_signal(repo, "C-1", ANOMALY)
    store = OrchestratorStore(repo)
    delegation = Delegation(
        delegation_id="d-gate",
        plan=PLAN_NUMBER,
        iteration=1,
        action="RUN_LIFECYCLE_GATES",
        created_at="2026-01-01T00:00:00Z",
        authority_basis="synthetic",
        declared_scope=(),
        command_set=gate_commands(),
        expected_evidence=(),
        worker_kind="command",
        worker_command=(),
    )
    result = CommandWorker(timeout_seconds=60).execute(
        delegation,
        store=store,
        run_id="r-gate",
        plan_rel=f"docs/plans/{PLAN_NAME}",
    )
    # C-1 published ANOMALY. Reading the *published classification* — not the
    # exit code — is what determines the signal, and the exit code is preserved
    # raw so the two are never conflated.
    by_label = {entry["label"]: entry["signal"] for entry in result.results}
    assert by_label["C-1"] == ANOMALY
    assert result.commands_executed[0]["exit_code"] == 1
    assert by_label["C-2"] == VALID and by_label["C-3"] == VALID

    # An exit code of 0 with a published ANOMALY is still an ANOMALY.
    set_gate_signal(repo, "C-2", ANOMALY)
    (repo / "tools" / "check_lifecycle_checkpoint.py").write_text(
        GATE_SCRIPT.replace(
            'sys.exit(1 if signal in ("ANOMALY", "BOUNDARY") else 0)',
            "sys.exit(0)",
        ),
        encoding="utf-8",
    )
    zero_exit = CommandWorker(timeout_seconds=60).execute(
        Delegation(
            delegation_id="d-gate-zero",
            plan=PLAN_NUMBER,
            iteration=2,
            action="RUN_LIFECYCLE_GATES",
            created_at="2026-01-01T00:00:00Z",
            authority_basis="synthetic",
            declared_scope=(),
            command_set=gate_commands(),
            expected_evidence=(),
            worker_kind="command",
            worker_command=(),
        ),
        store=store,
        run_id="r-gate-zero",
        plan_rel=f"docs/plans/{PLAN_NAME}",
    )
    zero_by_label = {entry["label"]: entry["signal"] for entry in zero_exit.results}
    assert zero_by_label["C-2"] == ANOMALY
    assert zero_exit.commands_executed[1]["exit_code"] == 0

    observation = observe(repo, PLAN_NUMBER)
    action = derive_next_action(
        observation,
        AuthorityBoundary(plan_authorized=True),
        gate_signals=observation.gate_signals,
    )
    assert action.kind == "STOP_GATE_ANOMALY"


def test_declared_environmental_class_is_gap_and_never_pass():
    repo = build_repo(
        _scratch("environmental"),
        plan=plan_text(validation_exits_zero=False, environmental=True),
    )
    store = OrchestratorStore(repo)
    observation = observe(repo, PLAN_NUMBER)
    assert observation.environmental_classes
    delegation = Delegation(
        delegation_id="d-env",
        plan=PLAN_NUMBER,
        iteration=1,
        action="RUN_VALIDATION",
        created_at="2026-01-01T00:00:00Z",
        authority_basis="synthetic",
        declared_scope=(),
        command_set=observation.command_set,
        expected_evidence=(),
        worker_kind="command",
        worker_command=(),
    )
    result = CommandWorker(timeout_seconds=60).execute(
        delegation,
        store=store,
        run_id="r-env",
        environmental=observation.environmental_classes,
    )
    assert result.commands_executed[0]["exit_code"] == 1
    assert result.results[0]["signal"] == GAP
    assert result.results[0]["signal"] != VALID

    # Without the declaration the same failure is a mechanical violation.
    undeclared = CommandWorker(timeout_seconds=60).execute(
        delegation,
        store=store,
        run_id="r-env-undeclared",
        environmental=(),
    )
    assert undeclared.results[0]["signal"] == "FAIL"


def test_gate_without_a_classification_line_is_a_gap():
    repo = build_repo(_scratch("gate-gap"))
    # Point the synthetic gate at another artifact: no line for our plan.
    (repo / ".gate_signals.json").write_text(
        json.dumps({"plan": "999-other.md"}), encoding="utf-8"
    )
    store = OrchestratorStore(repo)
    delegation = Delegation(
        delegation_id="d-gap",
        plan=PLAN_NUMBER,
        iteration=1,
        action="RUN_LIFECYCLE_GATES",
        created_at="2026-01-01T00:00:00Z",
        authority_basis="synthetic",
        declared_scope=(),
        command_set=gate_commands(),
        expected_evidence=(),
        worker_kind="command",
        worker_command=(),
    )
    result = CommandWorker(timeout_seconds=60).execute(
        delegation,
        store=store,
        run_id="r-gap",
        plan_rel=f"docs/plans/{PLAN_NAME}",
    )
    assert result.results[0]["signal"] == GAP


# --------------------------------------------------------------------------- #
# WorkerAdapter — the boundary contract the Host really calls
# --------------------------------------------------------------------------- #
# F-1: the Protocol published `execute(self, delegation, *, store, run_id)` while
# the Host really calls it with `plan_rel=` and `environmental=`. The tests below
# fix that contract structurally: they read the *real* call out of `host.py` and
# bind its arguments against the *real* Protocol signature. Neither a concrete
# worker nor a copy of the expected signature is used, so the test cannot drift
# with an implementation: it fails the moment the published contract stops
# accepting the call the Host makes.

HOST_PATH = REPO_ROOT / "runtime" / "orchestrator" / "host.py"


def _host_worker_execute_call() -> tuple[list[ast.expr], dict[str, ast.expr]]:
    """The real ``self.worker.execute(...)`` call the Host makes.

    Read from the source so the test describes the call site instead of a guess
    at it: the positional arguments and the keywords, exactly as written. Parsing
    the AST (rather than regexing the text) keeps the test independent of
    formatting.
    """
    tree = ast.parse(HOST_PATH.read_text(encoding="utf-8"))
    for node in ast.walk(tree):
        if not isinstance(node, ast.Call):
            continue
        func = node.func
        if (
            isinstance(func, ast.Attribute)
            and func.attr == "execute"
            and isinstance(func.value, ast.Attribute)
            and func.value.attr == "worker"
        ):
            keywords = {
                keyword.arg: keyword.value
                for keyword in node.keywords
                if keyword.arg is not None
            }
            return list(node.args), keywords
    raise AssertionError(
        f"no `self.worker.execute(...)` call found in {HOST_PATH}: the test can no "
        "longer observe the call the Host makes"
    )


def test_worker_adapter_declares_the_two_parameters_the_host_passes():
    """The published boundary declares every argument the Host supplies.

    Dropping either keyword is exactly F-1: a third implementation that follows
    the Protocol literally would raise ``TypeError`` on the Host's call.
    """
    parameters = inspect.signature(WorkerAdapter.execute).parameters
    _, host_keywords = _host_worker_execute_call()

    missing = {"plan_rel", "environmental"} - set(parameters)
    assert not missing, (
        f"WorkerAdapter.execute no longer declares {sorted(missing)}: the Host "
        f"calls it with {sorted(host_keywords)} (F-1)"
    )
    for name in ("plan_rel", "environmental"):
        assert name in host_keywords, (
            f"the Host no longer supplies {name!r}: the contract this test "
            "protects changed at the call site"
        )


def test_worker_adapter_signature_accepts_the_real_host_call():
    """The real Host call binds against the published Protocol signature.

    The call is reconstructed from ``host.py`` as a real Python call against a
    placeholder worker, so ``inspect.signature`` performs exactly the argument
    matching the interpreter would perform: a missing declaration, a changed kind
    (keyword-only versus positional) or a removed default all raise ``TypeError``.
    Nothing here checks that a method merely exists.
    """
    positional, keywords = _host_worker_execute_call()
    rendered = [ast.unparse(argument) for argument in positional]
    assert rendered == ["delegation"], (
        f"the Host now passes more than the delegation positionally: {rendered}"
    )
    missing = {"store", "run_id"} - set(keywords)
    assert not missing, f"the Host call no longer passes {sorted(missing)}"

    class PlaceholderWorker:
        """An empty shell: only the *shape* of the call is under test."""

        kind = "placeholder"

        def execute(self, *args, **kwargs):
            """Never called; ``Signature.bind`` is what validates the call."""

    host_call_kwargs = {name: object() for name in keywords}
    inspect.signature(WorkerAdapter.execute).bind(
        PlaceholderWorker(), *[object() for _ in positional], **host_call_kwargs
    )


def test_worker_adapter_boundary_is_incomplete_without_plan_rel_and_environmental():
    """Controlled falsification: the assertions above really detect the regression.

    The pre-F-1 declaration — three parameters, no ``plan_rel``, no
    ``environmental`` — must reject the Host's real call. That is the exact
    failure a future removal of either parameter would reintroduce.
    """

    class IncompleteBoundary(Protocol):
        """The pre-F-1 declaration, reproduced here on purpose."""

        kind: str

        def execute(self, delegation, *, store, run_id) -> object:
            ...

    positional, keywords = _host_worker_execute_call()
    arguments = {name: object() for name in keywords}

    with pytest.raises(TypeError):
        inspect.signature(IncompleteBoundary.execute).bind(
            object(), *[object() for _ in positional], **arguments
        )

    # The corrected contract accepts the very same call; without this second half
    # the falsification would pass for the wrong reason (a broken helper).
    inspect.signature(WorkerAdapter.execute).bind(
        object(), *[object() for _ in positional], **arguments
    )


# --------------------------------------------------------------------------- #
# M4 — persistent Worker Result
# --------------------------------------------------------------------------- #


def test_worker_result_satisfies_the_contract_and_persists():
    repo = build_repo(_scratch("m4"))
    store = OrchestratorStore(repo)
    delegation = Delegation(
        delegation_id="d-m4",
        plan=PLAN_NUMBER,
        iteration=1,
        action="RUN_VALIDATION",
        created_at="2026-01-01T00:00:00Z",
        authority_basis="synthetic",
        declared_scope=("src/a.txt",),
        command_set=(("python", "src/check_ok.py"),),
        expected_evidence=("captures",),
        worker_kind="command",
        worker_command=(),
    )
    store.write_delegation(delegation)
    result = CommandWorker(timeout_seconds=60).execute(
        delegation, store=store, run_id="r-m4"
    )
    payload = result.to_dict()
    for field in WORKER_RESULT_FIELDS:
        assert field in payload, field
    assert validate_worker_result(payload) == ()

    stored = store.read_worker_result(PLAN_NUMBER, "d-m4")
    assert stored is not None
    assert stored.result_id == result.result_id
    # delegation → worker result → ingestion → next action is unambiguous.
    assert stored.delegation_id == store.read_delegation(PLAN_NUMBER, "d-m4").delegation_id
    assert stored.delegation_received["action"] == "RUN_VALIDATION"
    on_disk = json.loads(
        (store.results_dir(PLAN_NUMBER) / "d-m4.json").read_text(encoding="utf-8")
    )
    assert canonical_json(on_disk) == (
        store.results_dir(PLAN_NUMBER) / "d-m4.json"
    ).read_text(encoding="utf-8")


def test_incomplete_worker_result_is_rejected_by_the_contract():
    payload = {"schema_version": "1", "result_id": "x", "plan": 1}
    problems = validate_worker_result(payload)
    assert any("missing" in problem for problem in problems)


def test_invalid_worker_result_in_the_store_stops_the_loop():
    repo = build_repo(_scratch("invalid-result"))
    store = OrchestratorStore(repo)

    class BrokenWorker:
        """A worker that returns a result which does not satisfy the M4 contract."""

        kind = "broken"

        def execute(self, delegation, *, store, run_id, **kwargs):
            payload = {
                "schema_version": "1",
                "result_id": "broken-result",
                "delegation_id": delegation.delegation_id,
                "plan": delegation.plan,
                "iteration": delegation.iteration,
                "created_at": "2026-01-01T00:00:00Z",
                "status": "completed",
                "worker": {"kind": self.kind},
                "delegation_received": delegation.to_dict(),
                "intended_actions": [],
                "performed_actions": [],
                "artifacts_modified": [],
                "commands_executed": [],
                "results": [{"label": "x", "signal": "NOT-A-SIGNAL"}],
                "evidence": [],
                "problems": [],
                "pending": [],
                "recommended_next_action": {},
                "authority_used": {},
                "effects_executed": [],
                "claims": {},
                "limitations": [],
            }
            store.results_dir(delegation.plan).mkdir(parents=True, exist_ok=True)
            (
                store.results_dir(delegation.plan) / (delegation.delegation_id + ".json")
            ).write_text(canonical_json(payload), encoding="utf-8")
            return payload

    host = ExecutionHost(
        repo,
        PLAN_NUMBER,
        store=store,
        worker=BrokenWorker(),
        gate_commands=gate_commands(),
        max_iterations=2,
    )
    run = host.run()
    assert run.terminal_action == "STOP_WORKER_RESULT_INVALID"


def test_missing_worker_result_stops_claiming_anything():
    repo = build_repo(_scratch("missing-result"))
    store = OrchestratorStore(repo)

    class ForgetfulWorker:
        kind = "forgetful"

        def execute(self, delegation, *, store, run_id, **kwargs):
            return WorkerResult(
                result_id="never-persisted",
                delegation_id=delegation.delegation_id,
                plan=delegation.plan,
                iteration=delegation.iteration,
                created_at="2026-01-01T00:00:00Z",
                status="completed",
                worker_kind=self.kind,
                delegation_received=delegation.to_dict(),
            )

    host = ExecutionHost(
        repo,
        PLAN_NUMBER,
        store=store,
        worker=ForgetfulWorker(),
        gate_commands=gate_commands(),
        max_iterations=1,
    )
    run = host.run()
    assert run.terminal_action == "STOP_WORKER_RESULT_MISSING"


# --------------------------------------------------------------------------- #
# The loop: Closed derivation, recovery, no progress
# --------------------------------------------------------------------------- #


def test_full_loop_derives_closed_from_real_evidence():
    repo = build_repo(_scratch("closed"))
    host = make_host(repo, max_iterations=12)
    run = host.run()
    assert run.terminal_action == "CLOSED_DERIVED", [
        (record["action"], record["rationale"]) for record in run.records
    ]
    conditions = run.derived_conditions
    assert conditions["Verified"] is True
    assert conditions["Executed"] is True
    assert conditions["Closed"] is True
    assert conditions["Released"] is False
    assert conditions["Promoted"] is False

    text = (repo / "docs" / "plans" / PLAN_NAME).read_text(encoding="utf-8")
    assert "**Status:** Executed" in text
    assert "Declared scope" in text
    assert "Estado de cierre" in text
    # A1 is registered and the closure state equals the validated state.
    observation = observe(repo, PLAN_NUMBER)
    assert observation.anchor.present and observation.checkpoint.present
    assert observation.checkpoint.closure_tree == observation.anchor.state_identity
    assert observation.checkpoint.consistency_pass


def test_revalidation_is_recorded_as_a2_without_mutating_a1():
    repo = build_repo(_scratch("a2"))
    make_host(repo, max_iterations=4).run()
    first = observe(repo, PLAN_NUMBER).anchor
    assert first.present and len(first.state_identities) == 1

    (repo / "src" / "a.txt").write_text("corrected content\n", encoding="utf-8")
    stage(repo)
    # A correction changes the relevant scoped content: revalidation is required.
    stale = observe(repo, PLAN_NUMBER)
    assert stale.anchor_stale
    run = make_host(repo, max_iterations=12).run()
    assert run.terminal_action == "CLOSED_DERIVED"
    after = observe(repo, PLAN_NUMBER).anchor
    assert len(after.state_identities) == 2, after.state_identities
    assert after.state_identities[0] == first.state_identities[0]
    # A2 was recorded and A1 was preserved: the original pair is still there.
    assert after.revalidated
    assert after.delta_identities[0] == first.delta_identities[0]
    # The checkpoint now corresponds to the revalidated closure state.
    final = observe(repo, PLAN_NUMBER)
    assert final.checkpoint.closure_tree == final.current_state_identity
    assert final.checkpoint.consistency_pass


def test_restart_reconstructs_and_continues_without_lost_continuity():
    repo = build_repo(_scratch("restart"))
    store = OrchestratorStore(repo)

    # First process: it validates, records the anchor and then hits its own
    # iteration limit (a bounded, explicit stop), i.e. it is interrupted before
    # reaching closure.
    first_host = make_host(repo, max_iterations=2, store=store, run_id="run-a")
    first_run = first_host.run()
    assert first_run.terminal_action == "STOP_MAX_ITERATIONS"
    journal_after_first = store.read_journal(PLAN_NUMBER)
    assert len(journal_after_first) == first_run.iterations
    assert [record["iteration"] for record in journal_after_first] == [1, 2, 3]

    # Second process: a brand new host instance, no shared memory at all.
    second_host = make_host(repo, max_iterations=12, store=store, run_id="run-b")
    second_run = second_host.run()
    journal_after_second = store.read_journal(PLAN_NUMBER)
    assert len(journal_after_second) == len(journal_after_first) + second_run.iterations
    # Iteration numbering continues: continuity is reconstructed from evidence,
    # not from an in-memory cursor.
    assert journal_after_second[len(journal_after_first)]["iteration"] == 4
    assert second_run.terminal_action == "CLOSED_DERIVED"

    report = second_host.reconstruct("run-b")
    assert "run-b" in report
    assert "Iteración" in report
    assert "CLOSED_DERIVED" in report

    # A third, fresh host over the settled repository derives the same terminal
    # condition (idempotent reconstruction, not a remembered cursor).
    third = make_host(repo, max_iterations=4, store=store, run_id="run-c")
    observation = third.observe()
    action = derive_next_action(
        observation, AuthorityBoundary(plan_authorized=True)
    )
    assert action.kind == "CLOSED_DERIVED"


def test_no_progress_guard_stops_instead_of_spinning(monkeypatch):
    repo = build_repo(_scratch("no-progress"))
    host = make_host(repo, max_iterations=6)

    import runtime.orchestrator.host as host_module
    from runtime.orchestrator.derivation import NextAction

    def frozen(observation, boundary, **kwargs):
        return NextAction(
            kind="RUN_VALIDATION",
            rationale="frozen action for the guard test",
            authority=boundary.evaluate("RUN_VALIDATION"),
        )

    monkeypatch.setattr(host_module, "derive_next_action", frozen)
    run = host.run()
    assert run.terminal_action == "STOP_NO_PROGRESS"
    # The guard fires as soon as the same derived action repeats with unchanged
    # governance facts; it never spins to the iteration limit.
    assert run.iterations <= 3
    assert run.records[-1]["action"] == "STOP_NO_PROGRESS"


def test_max_iterations_is_an_explicit_stop():
    repo = build_repo(_scratch("max-iterations"))

    import runtime.orchestrator.host as host_module
    from runtime.orchestrator.derivation import NextAction

    original = host_module.derive_next_action

    def frozen(observation, boundary, **kwargs):
        return NextAction(
            kind="RUN_VALIDATION",
            rationale="frozen",
            authority=boundary.evaluate("RUN_VALIDATION"),
        )

    host = make_host(repo, max_iterations=1)
    # Two different frozen rationales so the no-progress guard does not fire
    # first: the iteration limit is a distinct stop condition.
    counter = {"n": 0}

    def varying(observation, boundary, **kwargs):
        counter["n"] += 1
        action = frozen(observation, boundary, **kwargs)
        return NextAction(
            kind=action.kind,
            rationale=action.rationale + f" #{counter['n']}",
            authority=action.authority,
        )

    host_module.derive_next_action = varying
    try:
        run = host.run()
    finally:
        host_module.derive_next_action = original
    assert run.iterations == 2
    assert run.terminal_action == "STOP_MAX_ITERATIONS"


def test_observation_is_read_only():
    repo = build_repo(_scratch("read-only"))
    snapshot = {
        path.relative_to(repo).as_posix(): path.read_bytes()
        for path in sorted(repo.rglob("*"))
        if path.is_file() and ".git" not in path.parts
    }
    observe(repo, PLAN_NUMBER)
    after = {
        path.relative_to(repo).as_posix(): path.read_bytes()
        for path in sorted(repo.rglob("*"))
        if path.is_file() and ".git" not in path.parts
    }
    assert after == snapshot


def test_closed_derivation_never_releases_and_reports_human_authority():
    repo = build_repo(_scratch("no-release"))
    host = make_host(repo, max_iterations=12)
    run = host.run()
    assert run.terminal_action == "CLOSED_DERIVED"
    terminal = run.records[-1]
    assert "release requires human authority" in terminal["rationale"]
    assert terminal["authority"]["verdict"] == AUTHORIZED_EXISTING
    # Nothing in the plan artifact claims that a release was executed.
    text = (repo / "docs" / "plans" / PLAN_NAME).read_text(encoding="utf-8")
    assert "`Released` requiere autoridad humana" in text
    assert "Released=sí" not in text
    assert "Released: sí" not in text
    assert run.derived_conditions["Released"] is False
    assert run.derived_conditions["Promoted"] is False


# --------------------------------------------------------------------------- #
# The observation never substitutes a missing vital resource for an absent one
# (plan 145, I-1)
# --------------------------------------------------------------------------- #


def test_unreadable_repository_is_an_error_not_a_false_absent_state(
    tmp_path: Path,
) -> None:
    """A present root with a present git CLI must not read as "no repository".

    Substituting "could not read" for "does not exist" is what let a vanished
    throw-away repository surface as an ordinary state instead of a loud
    failure. The two facts are kept apart: this one raises.
    """
    (tmp_path / "docs" / "plans").mkdir(parents=True, exist_ok=True)
    (tmp_path / "docs" / "plans" / PLAN_NAME).write_text(
        plan_text(), encoding="utf-8"
    )

    assert git_state(tmp_path).is_repository is False
    assert git_state(tmp_path).git_available is True
    with pytest.raises(ObservationError, match="could not be read"):
        observe(tmp_path, PLAN_NUMBER)


def test_an_absent_git_cli_stays_a_declared_gap_not_an_error(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """A host without git is an environmental factor, reported as GAP.

    The distinction is the point: an unpinned environment is declared, while a
    broken reading of a readable root is a defect. Neither is silently turned
    into the other.
    """
    (tmp_path / "docs" / "plans").mkdir(parents=True, exist_ok=True)
    (tmp_path / "docs" / "plans" / PLAN_NAME).write_text(
        plan_text(), encoding="utf-8"
    )
    monkeypatch.setattr(
        "runtime.orchestrator.observation.git_available", lambda: False
    )

    observation = observe(tmp_path, PLAN_NUMBER)

    assert observation.git.is_repository is False
    assert observation.git.git_available is False
    assert any("git CLI is not resolvable" in gap for gap in observation.gaps)


def test_git_state_reports_the_cli_availability_explicitly() -> None:
    """The availability fact is part of the observation, not an inference."""
    state = git_state(REPO_ROOT)
    assert state.is_repository is True
    assert state.git_available is True
    assert state.to_dict()["git_available"] is True
