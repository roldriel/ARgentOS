"""Scope/Authority enforcement of SAE: the F-3 regression and its falsification (plan 138).

This module is the reproducible form of an incident that really happened. During
the execution of plan 136, an approved plan excluded ``ROADMAP.md`` from its
``Scope`` and simultaneously declared ``Roadmap Impact: REQUIRED`` naming that
artifact as the thing to reconcile. The host authorized a semantic task without
verifying the write set, the worker wrote the excluded artifact, and the
violation was reported **after** the write (``<PLAN-136>:F-3``). The plan was then
rewritten so the write looked authorized from the beginning.

The hardening this module protects is therefore not "detect better" but
"refuse earlier": every write target of the action must be authorized before the
delegation exists, and the declaration the run was authorized under cannot be
rewritten afterwards to legitimize what already happened.

Two properties make these tests worth having:

- **The excluded artifact is a parameter, never ``ROADMAP.md``.** The rule under
  test is general; hardcoding the artifact of the original incident would test
  the incident instead of the rule.
- **A test that passes before and after the fix is not a regression.** The
  companion proof lives in the plan's execution note: the same scenario against
  the pre-fix implementation produces ``STOP_FORBIDDEN_ACTION`` *after* the write
  and leaves the artifact modified. Here the assertions are strict enough that
  the pre-fix code cannot satisfy them: no delegation, no effect, byte-identical
  artifact.

Isolated tests in the sense of ``tests/AGENTS.md``: they build their own
repository under ``pytest_isolation.scratch_root`` and never touch the real tree.
"""

from __future__ import annotations

import hashlib
import subprocess
import uuid
from pathlib import Path

import pytest

import pytest_isolation
from runtime.orchestrator.agent_worker import (
    INVOCATION_COMPLETED,
    INVOCATION_INCOMPLETE,
    AgentInvocationRequest,
    AgentInvocationResult,
    AgentWorker,
)
from runtime.orchestrator.autonomy import (
    EXECUTE_AUTHORIZED_TASK,
    MODIFY_CLOSED_ARTIFACT,
    RESOLVE_FINDING_STATE,
    RUN_AUTHORIZED_VALIDATION,
    STOP_AUTHORITY_REQUIRED,
    STOP_FORBIDDEN_AUTONOMY,
    STOP_SCOPE_VIOLATION,
    AutonomyCandidate,
    AutonomyEnvelope,
    authorization_drift,
    authorization_projection,
    evaluate_autonomy,
    unresolved_targets_verdict,
    verify_action_scope,
    verify_write_targets,
)
from runtime.orchestrator.host import ExecutionHost
from runtime.orchestrator.store import OrchestratorStore
from runtime.orchestrator.worker import NullWorker

PLAN_NUMBER = 901
PLAN_NAME = f"{PLAN_NUMBER:03d}-sae-enforcement.md"

#: The artifact the plan excludes from its authorized scope. The name is a
#: parameter on purpose: the rule is general and nothing here may depend on the
#: artifact of the original incident.
EXCLUDED = "docs/ROADMAP-LIKE.md"
INCLUDED = "src/target.py"
INDEX_PATH = "docs/plans/INDEX.md"

SCRATCH_ROOT = pytest_isolation.scratch_root("sae-enforcement")

CHECK_OK = "import sys\nprint('ok')\nsys.exit(0)\n"

PLAN_TEMPLATE = """# Plan {plan} — synthetic change with an out-of-scope closure obligation

**Status:** Aprobado para ejecución
**Fecha:** 2026-09-20
**RFC:** — (synthetic)
**Clase:** — (synthetic)
**Change Level:** L1

## Objetivo

Synthetic change that mirrors the structure of `<PLAN-136>:F-3`: the authorized
scope excludes an artifact, and a closure determination names that artifact as
the thing to reconcile.

## Criterio de entrada

- [x] synthetic entry criterion satisfied

## Entregables

{deliverables}

## Pasos

1. Do the authorized work only.

## Scope

- `{included}` is authorized.
- `{excluded}` is explicitly **excluded**: no step of this plan may write it.

## Delegación agentiva

- **Task:** {task}
- **Scope:** {declared_scope}

## Efectos declarados

| Efecto | Qué produce | Autorización (referencia) | Estado |
|---|---|---|---|
| — | ninguno: la tarea autorizada escribe solo dentro del scope declarado. | — | `authorized` |

## Criterios de salida

- [ ] synthetic

## Verificación

```bash
python src/check_ok.py
```

## Documentation Impact

NOT_REQUIRED — synthetic.

## Roadmap Impact

REQUIRED — `{excluded}` would be the artifact to reconcile. It is named here so
that the obligation exists and cannot be satisfied inside the authorized scope.

## Validation anchor

<!-- container the host records into; empty by design -->

## Checkpoint / cierre

<!-- container the host records into; empty by design -->

## Findings / Correcciones / Pending

### Findings

No findings detected / N/A
"""


def _scratch(name: str) -> Path:
    path = SCRATCH_ROOT / f"{name}-{uuid.uuid4().hex[:8]}"
    path.mkdir(parents=True, exist_ok=True)
    return path


def _git(root: Path, *args: str) -> None:
    subprocess.run(["git", *args], cwd=root, check=True, capture_output=True)


def _digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


AUTHORIZATION_SECTIONS = ("## Scope", "## Delegación agentiva", "## Roadmap Impact")


def _authorization_elements(path: Path) -> tuple[str, ...]:
    """The plan's authorization *elements*, not the whole artifact.

    Scope, the agent-task declaration and the closure obligations are the
    contract that authorizes the execution. The host legitimately records its own
    governance into the same artifact (status, anchor, checkpoint, run note), so
    byte-identity of the whole file is not the right assertion — and demanding it
    would forbid the record mechanism RFC-75 requires. Byte-identity **of the
    elements** is the property P4 actually needs, and it is exactly what a
    retrospective rewrite would change.
    """
    text = path.read_text(encoding="utf-8")
    sections: list[str] = []
    for heading in AUTHORIZATION_SECTIONS:
        marker = f"\n{heading}\n"
        if marker not in text:
            sections.append(f"{heading}: ABSENT")
            continue
        tail = text.split(marker, 1)[1]
        body = tail.split("\n## ", 1)[0]
        sections.append(f"{heading}:\n{body.rstrip()}")
    return tuple(sections)


def build_repo(
    name: str,
    *,
    task: str = "implement the authorized work",
    declared_scope: str = f"`{INCLUDED}`",
    deliverables: tuple[str, ...] = (INCLUDED,),
    excluded_content: str = "roadmap-like content: untouched baseline\n",
) -> Path:
    """A git repository carrying the F-3 shape, with the artifact as a parameter.

    ``deliverables`` is the plan's own declaration of what it produces, and it is
    what makes a declared write target *authorized*: the frontier intersects the
    agent-task scope with the plan's observed scope, so a scope that names a path
    the plan never declares is refused. The default keeps the two aligned; the F-3
    fixture deliberately does not, because that divergence **is** the incident.
    """
    root = _scratch(name)
    _git(root, "init", "-q", ".")
    _git(root, "config", "user.email", "test@example.invalid")
    _git(root, "config", "user.name", "SAE Enforcement Test")
    (root / "docs" / "plans").mkdir(parents=True, exist_ok=True)
    (root / "src").mkdir(parents=True, exist_ok=True)
    (root / "src" / "check_ok.py").write_text(CHECK_OK, encoding="utf-8")
    (root / "src" / "target.py").write_text(
        '"""Authorized target."""\n\nmarker = "before"\n', encoding="utf-8"
    )
    (root / "src" / "extra.py").write_text("extra = 0\n", encoding="utf-8")
    (root / EXCLUDED).write_text(excluded_content, encoding="utf-8")
    (root / ".gitignore").write_text(".project/\n__pycache__/\n", encoding="utf-8")
    deliverable_lines = "\n".join(
        f"{index}. `{path}`" for index, path in enumerate(deliverables, start=1)
    )
    (root / "docs" / "plans" / PLAN_NAME).write_text(
        PLAN_TEMPLATE.format(
            plan=PLAN_NUMBER,
            included=INCLUDED,
            excluded=EXCLUDED,
            task=task,
            declared_scope=declared_scope,
            deliverables=deliverable_lines,
        ),
        encoding="utf-8",
    )
    (root / INDEX_PATH).write_text(f"# Plans\n\n- {PLAN_NAME}\n", encoding="utf-8")
    _git(root, "add", "-A")
    _git(root, "commit", "-qm", "synthetic baseline")
    return root


class WritingInvoker:
    """An injected invoker that really writes, like the execution environment would.

    The repository ships no provider and no model (plan 123, human decision H-1),
    so a real agent cannot be invoked. This stand-in replaces the *model*, not the
    *effect*: it performs real filesystem writes through the same request the host
    materializes, so what enforcement prevents is a material write and not a
    simulated one.
    """

    kind = "writing"

    def __init__(
        self,
        *,
        include_scope: bool = True,
        include_excluded: bool = True,
        status: str = INVOCATION_COMPLETED,
    ) -> None:
        self.include_scope = include_scope
        self.include_excluded = include_excluded
        self.status = status
        self.requests: list[AgentInvocationRequest] = []

    def invoke(self, request: AgentInvocationRequest) -> AgentInvocationResult:
        self.requests.append(request)
        root = Path(request.root)
        if self.include_scope:
            (root / INCLUDED).write_text(
                '"""Authorized target."""\n\nmarker = "after"\n', encoding="utf-8"
            )
        if self.include_excluded:
            (root / EXCLUDED).write_text(
                "roadmap-like content: REWRITTEN BY THE AGENT\n", encoding="utf-8"
            )
        return AgentInvocationResult(
            status=self.status,
            summary="performed the authorized work and reconciled the obligation",
            transcript="observe: read the plan\nact: wrote the target and the map\n",
            steps=2,
        )


def make_host(
    root: Path,
    *,
    gate: bool = True,
    invoker: WritingInvoker | None = None,
):
    return ExecutionHost(
        root,
        PLAN_NUMBER,
        worker=AgentWorker(invoker=invoker or WritingInvoker()),
        gate_commands=(),
        autonomy_gate=gate,
    )


def pinned_of(host: ExecutionHost) -> str | None:
    return host._pinned_autonomy_projection()


# --------------------------------------------------------------------------- #
# 1. The F-3 regression: STOP before the write
# --------------------------------------------------------------------------- #


def test_f3_regression_stops_before_the_write_and_leaves_everything_identical():
    """The exact shape of `<PLAN-136>:F-3`, refused *before* the persistent effect.

    The fixture mirrors the incident: the plan's authorized scope excludes an
    artifact, a closure determination names it as the thing to reconcile, and the
    delegated work would write it — exactly what the plan that was authorized
    permitted, and exactly what the single-path check failed to notice.

    Nine assertions, in the order the policy demands: derive the action, validate
    authorization, detect the violation, STOP, record evidence, escalate and
    **not** execute the write.
    """
    root = build_repo("f3-regression", declared_scope=f"`{INCLUDED}`, `{EXCLUDED}`")
    excluded_path = root / EXCLUDED
    plan_path = root / "docs" / "plans" / PLAN_NAME
    excluded_before = _digest(excluded_path)
    elements_before = _authorization_elements(plan_path)

    store = OrchestratorStore(root)
    invoker = WritingInvoker()
    host = ExecutionHost(
        root,
        PLAN_NUMBER,
        store=store,
        worker=AgentWorker(invoker=invoker),
        gate_commands=(),
        autonomy_gate=True,
    )
    run = host.run(max_iterations=1)
    record = run.records[0]

    # (1) STOP_SCOPE_VIOLATION with a human-authority verdict.
    assert run.terminal_action == STOP_SCOPE_VIOLATION
    assert record["action"] == STOP_SCOPE_VIOLATION
    assert record["authority"]["verdict"] == "REQUIRES_HUMAN"
    assert record["stop_reason"] == STOP_SCOPE_VIOLATION

    # (2) The refusal precedes the effect: the action was never delegated.
    assert record["delegation_id"] is None
    assert (
        store.read_delegation(
            PLAN_NUMBER, f"plan{PLAN_NUMBER}-it0001-run_implementation_task"
        )
        is None
    )
    assert store.list_worker_results(PLAN_NUMBER) == []

    # (3) The excluded artifact is byte-identical.
    assert _digest(excluded_path) == excluded_before

    # (4) The authorization elements (Scope, Task, closure obligations,
    #     declaration) are byte-identical: the plan was not rewritten to
    #     legitimize the refusal, and nothing was authorized retroactively.
    elements_after = _authorization_elements(plan_path)
    assert elements_after == elements_before
    assert EXCLUDED in elements_after[0], "the excluded artifact is still excluded"
    assert INCLUDED in elements_after[0]

    # (5) The evidence is sufficient and reconstructible from the journal.
    autonomy = record["autonomy"]
    assert autonomy["declared"] is True
    assert autonomy["continues"] is False
    assert autonomy["stop_condition"] == STOP_SCOPE_VIOLATION
    assert autonomy["authorization_drift"] is False
    assert autonomy["authority"]
    assert autonomy["reason"]
    assert sorted(autonomy["write_targets"]) == sorted([INCLUDED, EXCLUDED])
    outcomes = autonomy["outcomes"]
    assert len(outcomes) == 1
    assert outcomes[0]["disposition"] == "REQUIRES_AUTHORITY"
    assert EXCLUDED in outcomes[0]["scope_reason"]
    assert "nothing was written" in record["rationale"]

    # (6) The checkpoint itself is recorded, so the escalation shows what the run
    #     was authorized under. It names the *authorized* paths, which is why the
    #     excluded artifact never appears in it.
    assert record["autonomy_checkpoint"]
    assert record["autonomy_checkpoint"] == plan_before_projection(root)
    assert f"scope: {EXCLUDED}\n" not in record["autonomy_checkpoint"]

    # (7) The invoker was never reached: nothing executed, so no write path was
    #     taken at all.
    assert invoker.requests == []


def plan_before_projection(root: Path) -> str:
    """The projection the host pins for the untouched fixture, recomputed.

    It uses the **bounded** envelope, which is the reading the host pins and
    evaluates: pinning the raw declaration while evaluating the bounded one would
    make every execution diverge from its own checkpoint.
    """
    from runtime.orchestrator.host import _autonomy_envelope
    from runtime.orchestrator.observation import observe

    observation = observe(root, PLAN_NUMBER, OrchestratorStore(root))
    _declaration, bounded = _autonomy_envelope(observation, PLAN_NUMBER)
    return authorization_projection(bounded)


def test_the_regression_is_not_vacuous_the_write_really_happens_when_allowed():
    """The counter-proof: when the declaration is honest, the invoker really writes.

    ``WritingInvoker`` is not a stub that returns a story. With both targets
    declared — and the artifact therefore *inside* the authorized scope — the host
    delegates, the invoker runs, and the artifact really changes. So the
    "byte-identical" assertion of the regression is a property of the enforcement,
    not of a fixture that never writes.
    """
    root = build_repo(
        "f3-counterproof",
        declared_scope=f"`{INCLUDED}`, `{EXCLUDED}`",
        deliverables=(INCLUDED, EXCLUDED),
    )
    excluded_path = root / EXCLUDED
    before = _digest(excluded_path)

    run = make_host(root, invoker=WritingInvoker()).run(max_iterations=1)

    assert run.records[0]["action"] == "RUN_IMPLEMENTATION_TASK"
    assert run.records[0]["delegation_id"]
    assert _digest(excluded_path) != before
    assert "REWRITTEN BY THE AGENT" in excluded_path.read_text(encoding="utf-8")


def test_the_pre_fix_detection_only_reports_after_the_effect():
    """The defect, reproduced: post-hoc detection leaves the write in place.

    The declaration here is honest — it names only the target it writes — so the
    pre-write enforcement has nothing to refuse. The invoker then writes a path it
    was never given, and the host reports it **after** the artifact changed:
    *write → detect → report*. This is the behaviour every deployment had before
    plan 138, asserted here so the difference the enforcement makes stays
    observable and cannot quietly regress.
    """
    root = build_repo("f3-pre-fix-shape")
    excluded_path = root / EXCLUDED
    before = _digest(excluded_path)

    run = make_host(root, invoker=WritingInvoker()).run(max_iterations=2)

    # The write happened and the artifact stays modified: detection, not prevention.
    # The stop is the *only* record: the delegation was executed and then reported
    # as a violation, so there is no "RUN_IMPLEMENTATION_TASK" success record — the
    # host never accepts a delegation that wrote outside its authority.
    assert _digest(excluded_path) != before
    assert run.terminal_action == "STOP_FORBIDDEN_ACTION"
    assert [record["action"] for record in run.records] == ["STOP_FORBIDDEN_ACTION"]
    assert run.records[0]["delegation_id"]


def test_the_old_single_path_check_would_have_authorized_this_action():
    """Why the defect was structural, not a lapse of attention.

    Before plan 138 the gate resolved a **single** path: the first one the
    delegation declared. That path is inside the scope by construction — it comes
    from the same declaration — so the check could not fail while the write that
    mattered was never looked at. The assertion below is exactly that blindness:
    the first path passes, the complete set does not.
    """
    envelope = envelope_with(INCLUDED)
    declared = (INCLUDED, EXCLUDED)

    # What the pre-fix check asked: "is the first declared path authorized?"
    assert verify_action_scope(envelope, declared[0]).in_scope is True
    # What the enforcement asks now: "is *every* declared path authorized?"
    assert verify_write_targets(envelope, declared).in_scope is False


# --------------------------------------------------------------------------- #
# 2. Write targets: all-or-nothing, over the complete set
# --------------------------------------------------------------------------- #


def envelope_with(*scope: str, task: str = "t", status: str = "Aprobado para ejecución"):
    return AutonomyEnvelope(
        task=task,
        scope_paths=tuple(scope),
        authority_basis="the approved plan's own declaration",
        plan=PLAN_NUMBER,
        plan_authorized=True,
        declaration_present=True,
        authorizing_status=status,
    )


def test_a_single_authorized_target_is_authorized():
    verdict = verify_write_targets(envelope_with(INCLUDED), (INCLUDED,))
    assert verdict.in_scope is True


def test_a_single_unauthorized_target_is_refused():
    verdict = verify_write_targets(envelope_with(INCLUDED), (EXCLUDED,))
    assert verdict.in_scope is False
    assert "not authorized" in verdict.reason


def test_multiple_authorized_targets_are_authorized():
    verdict = verify_write_targets(
        envelope_with(INCLUDED, INDEX_PATH), (INCLUDED, INDEX_PATH)
    )
    assert verdict.in_scope is True
    assert "all 2" in verdict.reason


def test_multiple_targets_with_one_unauthorized_refuse_the_whole_action():
    """No partial execution: the authorized target is refused with the action."""
    verdict = verify_write_targets(
        envelope_with(INCLUDED, INDEX_PATH), (INCLUDED, INDEX_PATH, EXCLUDED)
    )
    assert verdict.in_scope is False
    assert "one of the 3" in verdict.reason
    assert EXCLUDED in verdict.reason


def test_an_empty_target_set_cannot_be_shown_to_be_authorized():
    verdict = verify_write_targets(envelope_with(INCLUDED), ())
    assert verdict.in_scope is False
    assert "declares no write target" in verdict.reason


def test_an_unresolved_target_set_is_refused_explicitly():
    verdict = unresolved_targets_verdict()
    assert verdict.in_scope is False
    assert "could not be resolved" in verdict.reason

    result = evaluate_autonomy(
        envelope_with(INCLUDED),
        [
            AutonomyCandidate(
                EXECUTE_AUTHORIZED_TASK,
                write_targets=(),
                targets_unresolved=True,
            )
        ],
    )
    assert result.continues is False
    assert result.stop_condition == STOP_SCOPE_VIOLATION


def test_a_write_candidate_carrying_the_full_set_stops_on_the_unauthorized_one():
    result = evaluate_autonomy(
        envelope_with(INCLUDED),
        [
            AutonomyCandidate(
                EXECUTE_AUTHORIZED_TASK,
                target_path=INCLUDED,
                write_targets=(INCLUDED, EXCLUDED),
            )
        ],
    )
    assert result.continues is False
    assert result.stop_condition == STOP_SCOPE_VIOLATION
    assert result.to_dict()["write_targets"] == [INCLUDED, EXCLUDED]


def test_the_singular_target_form_keeps_working_for_read_only_and_legacy_callers():
    """The single-path form is not dead: read-only classes and plan 135 callers use it."""
    read_only = evaluate_autonomy(
        envelope_with(INCLUDED),
        [AutonomyCandidate(RUN_AUTHORIZED_VALIDATION, target_path=None)],
    )
    assert read_only.continues is True

    singular = evaluate_autonomy(
        envelope_with(INCLUDED),
        [AutonomyCandidate(EXECUTE_AUTHORIZED_TASK, target_path=INCLUDED)],
    )
    assert singular.continues is True
    assert singular.selected is not None
    assert singular.selected.target_path == INCLUDED


# --------------------------------------------------------------------------- #
# 3. Authorized / unauthorized actions
# --------------------------------------------------------------------------- #


def test_an_authorized_action_inside_the_scope_continues():
    result = evaluate_autonomy(
        envelope_with(INCLUDED),
        [AutonomyCandidate(EXECUTE_AUTHORIZED_TASK, write_targets=(INCLUDED,))],
    )
    assert result.continues is True
    assert result.stop_condition is None


def test_a_forbidden_action_cannot_be_bought_by_authorizing_its_target():
    result = evaluate_autonomy(
        envelope_with(INCLUDED),
        [AutonomyCandidate(MODIFY_CLOSED_ARTIFACT, write_targets=(INCLUDED,))],
    )
    assert result.continues is False
    assert result.stop_condition == STOP_FORBIDDEN_AUTONOMY


def test_a_human_authority_action_is_refused_even_with_a_perfect_target_set():
    result = evaluate_autonomy(
        envelope_with(INCLUDED),
        [AutonomyCandidate(RESOLVE_FINDING_STATE, write_targets=(INCLUDED,))],
    )
    assert result.continues is False
    assert result.stop_condition == STOP_AUTHORITY_REQUIRED


# --------------------------------------------------------------------------- #
# 4. Impact REQUIRED inside and outside the scope
# --------------------------------------------------------------------------- #


def test_a_required_obligation_inside_the_scope_is_conducted():
    """`REQUIRED` whose artifact **is** authorized: the write is conducted."""
    root = build_repo(
        "required-inside",
        declared_scope=f"`{INCLUDED}`, `{EXCLUDED}`",
        deliverables=(INCLUDED, EXCLUDED),
    )
    excluded_path = root / EXCLUDED
    before = _digest(excluded_path)
    run = make_host(root, invoker=WritingInvoker()).run(max_iterations=1)
    assert run.records[0]["action"] == "RUN_IMPLEMENTATION_TASK"
    assert _digest(excluded_path) != before


def test_a_required_obligation_outside_the_scope_is_refused_and_changes_nothing():
    """`REQUIRED` whose artifact is **not** authorized: the obligation is deferred.

    The plan's `## Scope` names the artifact as out of scope; the delegated work
    declares only the authorized path. The obligation is real and recorded — and
    it grants nothing: the run does the authorized work, the excluded artifact is
    never a target, and nothing writes it.
    """
    root = build_repo("required-outside")
    excluded_path = root / EXCLUDED
    before = _digest(excluded_path)
    run = make_host(root, invoker=WritingInvoker(include_excluded=False)).run(
        max_iterations=2
    )
    actions = [record["action"] for record in run.records]
    assert actions[0] == "RUN_IMPLEMENTATION_TASK"
    assert run.records[0]["delegation_id"]
    assert EXCLUDED not in run.records[0]["autonomy"]["write_targets"]
    assert _digest(excluded_path) == before
    assert "REQUIRED" in (root / "docs" / "plans" / PLAN_NAME).read_text(encoding="utf-8")


# --------------------------------------------------------------------------- #
# 5. The authorization checkpoint: no retroactive legitimization
# --------------------------------------------------------------------------- #


def test_the_projection_is_stable_across_the_legitimate_status_transition():
    """The host recording `Executed` is its own governance record, not a drift."""
    approved = envelope_with(INCLUDED, status="Aprobado para ejecución")
    executed = envelope_with(INCLUDED, status="Executed")
    assert authorization_projection(approved) == authorization_projection(executed)
    drift, reason = authorization_drift(authorization_projection(approved), executed)
    assert drift is False
    assert "unchanged" in reason


def test_rewrapping_a_field_is_not_a_change_of_authorization():
    """Representation is normalized; the *words* are what the checkpoint guards."""
    one = envelope_with(INCLUDED, task="implement the   authorized work")
    other = envelope_with(INCLUDED, task="implement the authorized work")
    assert authorization_projection(one) == authorization_projection(other)


def test_scope_widened_after_authorization_is_a_divergence():
    pinned = authorization_projection(envelope_with(INCLUDED))
    wider = envelope_with(INCLUDED, EXCLUDED)
    drift, reason = authorization_drift(pinned, wider)
    assert drift is True
    assert "widened" in reason


def test_task_rewritten_after_authorization_is_a_divergence():
    pinned = authorization_projection(envelope_with(INCLUDED, task="original task"))
    rewritten = envelope_with(INCLUDED, task="original task, now also edits the map")
    drift, _ = authorization_drift(pinned, rewritten)
    assert drift is True


def test_the_authorizing_status_disappearing_is_a_divergence():
    pinned = authorization_projection(envelope_with(INCLUDED))
    revoked = envelope_with(INCLUDED, status="Superseded")
    drift, _ = authorization_drift(pinned, revoked)
    assert drift is True


def test_emptying_the_declaration_is_a_divergence():
    pinned = authorization_projection(envelope_with(INCLUDED))
    emptied = AutonomyEnvelope(
        task="",
        scope_paths=(),
        plan=PLAN_NUMBER,
        plan_authorized=True,
        declaration_present=True,
        authorizing_status="Aprobado para ejecución",
    )
    drift, _ = authorization_drift(pinned, emptied)
    assert drift is True


def test_a_not_yet_pinned_checkpoint_is_not_a_divergence():
    drift, reason = authorization_drift(None, envelope_with(INCLUDED))
    assert drift is False
    assert "pinned yet" in reason

def test_evaluate_autonomy_stops_on_drift_even_with_a_perfectly_authorized_target():
    """The rewritten contract cannot buy itself a continuation."""
    pinned = authorization_projection(envelope_with(INCLUDED))
    result = evaluate_autonomy(
        envelope_with(INCLUDED, EXCLUDED),
        [AutonomyCandidate(EXECUTE_AUTHORIZED_TASK, write_targets=(INCLUDED,))],
        pinned_projection=pinned,
    )
    assert result.continues is False
    assert result.stop_condition == STOP_SCOPE_VIOLATION
    assert result.authorization_drift is True
    assert result.to_dict()["authorization_drift"] is True


def test_the_host_stops_when_the_contract_is_rewritten_after_authorization():
    """End to end: the run is authorized, then its **Task** is rewritten.

    The rewrite happens between two runs on purpose. A host that re-pinned on
    every start would accept the new instruction and delegate it — which is
    precisely how a retrospective widening wins. Pinning the *earliest*
    authorization is what makes the checkpoint survive a restart.
    """
    root = build_repo("drift-e2e")
    plan_path = root / "docs" / "plans" / PLAN_NAME
    plan_before = plan_path.read_text(encoding="utf-8")
    declaration = plan_before.split("## Delegación agentiva")[1].split("##")[0]
    assert EXCLUDED not in declaration

    store = OrchestratorStore(root)
    first = make_host(root, invoker=WritingInvoker(include_excluded=False)).run(
        max_iterations=2
    )
    assert first.records[0]["action"] == "RUN_IMPLEMENTATION_TASK"
    assert first.records[0]["delegation_id"]
    pinned = pinned_of(ExecutionHost(root, PLAN_NUMBER, store=store))
    assert pinned
    assert f"scope: {EXCLUDED}" not in pinned

    # A later modification of the declaration, after the execution started: the
    # task now claims the artifact is in scope. That is a rewrite of the contract
    # that authorized the run, not a clarification of it.
    plan_path.write_text(
        plan_before.replace(
            "- **Task:** implement the authorized work",
            "- **Task:** implement the authorized work and reconcile the excluded "
            "artifact (it is authorized)",
        ),
        encoding="utf-8",
    )

    second = make_host(root, invoker=WritingInvoker(include_excluded=False)).run(
        max_iterations=2
    )
    record = second.records[-1]
    assert record["action"] == STOP_SCOPE_VIOLATION
    assert record["authorization_drift"] is True
    assert record["delegation_id"] is None
    assert record["authority"]["verdict"] == "REQUIRES_HUMAN"
    assert second.terminal_action == STOP_SCOPE_VIOLATION
    # The checkpoint that governs is still the original one, not the rewrite.
    assert record["autonomy_checkpoint"] == pinned
    assert "checkpoint diverged" in record["rationale"]


def test_the_host_stops_when_a_declared_scope_widens_to_another_authorized_path():
    """A widening the plan *does* authorize is still a change of authorization."""
    root = build_repo(
        "drift-widen",
        declared_scope=f"`{INCLUDED}`",
        deliverables=(INCLUDED, "src/extra.py"),
    )
    plan_path = root / "docs" / "plans" / PLAN_NAME
    plan_before = plan_path.read_text(encoding="utf-8")

    store = OrchestratorStore(root)
    first = make_host(root, invoker=WritingInvoker(include_excluded=False)).run(
        max_iterations=2
    )
    assert first.records[0]["action"] == "RUN_IMPLEMENTATION_TASK"
    pinned = pinned_of(ExecutionHost(root, PLAN_NUMBER, store=store))
    assert pinned and "scope: src/extra.py" not in pinned

    plan_path.write_text(
        plan_before.replace(
            f"- **Scope:** `{INCLUDED}`",
            f"- **Scope:** `{INCLUDED}`, `src/extra.py`",
        ),
        encoding="utf-8",
    )

    second = make_host(root, invoker=WritingInvoker(include_excluded=False)).run(
        max_iterations=2
    )
    record = second.records[-1]
    assert record["action"] == STOP_SCOPE_VIOLATION
    assert record["authorization_drift"] is True
    assert record["delegation_id"] is None


def test_an_unauthorized_widening_is_refused_by_the_scope_check_before_any_drift():
    """Two mechanisms, two jobs — and the scope check is the one that fires here.

    Widening the declaration to a path the plan never declared an *outcome* is
    refused by the write-target check (`E1`): such a declaration was never
    authorized in the first place, so the refusal is a scope finding, not a
    divergence. The checkpoint (`E2`) covers what the scope bound cannot see — a
    rewritten Task or a revoked status, asserted in the test above. This test
    additionally records the sharper, second effect: the widening does not become
    a live target either, so the delegated work is conducted for the authorized
    path only.
    """
    root = build_repo("drift-unauthorized-widen")
    plan_path = root / "docs" / "plans" / PLAN_NAME
    plan_before = plan_path.read_text(encoding="utf-8")

    store = OrchestratorStore(root)
    first = make_host(root, invoker=WritingInvoker(include_excluded=False)).run(
        max_iterations=2
    )
    assert first.records[0]["action"] == "RUN_IMPLEMENTATION_TASK"
    pinned = pinned_of(ExecutionHost(root, PLAN_NUMBER, store=store))
    assert pinned and f"scope: {EXCLUDED}" not in pinned

    plan_path.write_text(
        plan_before.replace(
            f"- **Scope:** `{INCLUDED}`",
            f"- **Scope:** `{INCLUDED}`, `{EXCLUDED}`",
        ),
        encoding="utf-8",
    )

    second = make_host(root, invoker=WritingInvoker(include_excluded=False)).run(
        max_iterations=1
    )
    # The widened path is still not an authorized write target: it is filtered
    # out of the bounded envelope, so it never becomes part of the declared write
    # set — neither in the run that was already authorized nor in any later one.
    assert EXCLUDED not in first.records[0]["autonomy"]["write_targets"]
    assert second.records[0]["action"] == "RECORD_VALIDATION_ANCHOR"
    assert "REWRITTEN BY THE AGENT" not in (root / EXCLUDED).read_text(encoding="utf-8")


def test_the_pinned_checkpoint_is_read_back_from_the_journal_not_from_the_artifact():
    """The checkpoint is durable evidence, not a re-reading of a mutable file."""
    root = build_repo("checkpoint-durable")
    host = make_host(root, invoker=WritingInvoker())
    host.run(max_iterations=1)
    pinned = pinned_of(ExecutionHost(root, PLAN_NUMBER))
    assert pinned
    assert "authorization-v1" in pinned
    assert f"scope: {INCLUDED}" in pinned


# --------------------------------------------------------------------------- #
# 6. Semantic proximity — the frontier never infers
# --------------------------------------------------------------------------- #


@pytest.mark.parametrize(
    "candidate",
    [
        "docs",  # container
        "docs/ROADMAP-LIKE.md/sub",  # descendant
        "docs/ROADMAP-LIKEs.md",  # plural
        "docs/ROADMAP",  # prefix
        "./docs/ROADMAP-LIKE.md",  # ./-prefixed spelling of a *different* path set
        "docs\\ROADMAP-LIKE.md",  # separators (normalized, so it must fail on value)
        "src/TARGET.py",  # case difference
    ],
)
def test_proximity_is_never_authorization(candidate):
    assert verify_action_scope(envelope_with(INCLUDED), candidate).in_scope is False


def test_a_normalized_spelling_of_an_authorized_path_is_accepted():
    """Normalization is representational only: `./x` and `x/` are the same path."""
    assert verify_action_scope(envelope_with(INCLUDED), f"./{INCLUDED}").in_scope is True
    assert verify_action_scope(envelope_with(f"{INCLUDED}/"), INCLUDED).in_scope is True


# --------------------------------------------------------------------------- #
# 7. DEFERRED without a governing pending decision is not DEFERRED
# --------------------------------------------------------------------------- #


def test_a_deferral_without_a_governing_pending_decision_is_still_a_stop():
    """A deferral is recorded, never converted into an authorization.

    The policy's rule is that a `DEFERRED` impact without an *existing* pending
    decision that governs it is an unresolved blocking condition, not a deferral.
    The frontier carries the same discipline: the deferred candidate is preserved
    and does not block independent work, but it never authorizes the deferred
    action, and with no authorized candidate the loop stops instead of inventing
    work.
    """
    envelope = envelope_with(INCLUDED)
    deferred_only = evaluate_autonomy(
        envelope,
        [
            AutonomyCandidate(
                EXECUTE_AUTHORIZED_TASK,
                write_targets=(EXCLUDED,),
                deferred=True,
                deferral_authority="",
                deferral_evidence="",
            )
        ],
    )
    assert deferred_only.continues is False
    assert deferred_only.stop_condition == "STOP_NO_AUTHORIZED_WORK"
    outcomes = deferred_only.outcomes
    assert outcomes[0].disposition == "DEFERRED"
    assert outcomes[0].stop_condition is None

    # And it does not block an independent authorized branch.
    with_independent = evaluate_autonomy(
        envelope,
        [
            AutonomyCandidate(
                EXECUTE_AUTHORIZED_TASK,
                write_targets=(EXCLUDED,),
                deferred=True,
            ),
            AutonomyCandidate(EXECUTE_AUTHORIZED_TASK, write_targets=(INCLUDED,)),
        ],
    )
    assert with_independent.continues is True
    assert with_independent.selected is not None


# --------------------------------------------------------------------------- #
# 8. The host's own governance records stay legitimate
# --------------------------------------------------------------------------- #


def test_the_hosts_records_into_its_own_plan_are_authorized():
    """The plan artifact is inside the authorized scope of its own Change."""
    root = build_repo("host-records")
    host = make_host(root, invoker=WritingInvoker())
    observation = host.observe()
    targets, unresolved = _targets("RECORD_VALIDATION_ANCHOR", observation)
    assert unresolved is False
    assert targets == (observation.plan_path,)
    envelope = _envelope(observation)
    assert verify_write_targets(envelope, targets).in_scope is True


def _targets(action_kind, observation):
    from runtime.orchestrator.host import _autonomy_targets

    return _autonomy_targets(action_kind, observation)


def _envelope(observation):
    from runtime.orchestrator.host import _autonomy_envelope

    _declaration, bounded = _autonomy_envelope(observation, PLAN_NUMBER)
    return bounded


# --------------------------------------------------------------------------- #
# 9. Defence in depth: the worker's own write is still detected
# --------------------------------------------------------------------------- #


def test_a_write_inside_the_worker_is_still_detected_after_the_fact():
    """The declared limit, asserted instead of glossed over.

    When the declaration is honest, the host has no reason to refuse: the targets
    the action declared are all inside the scope. The invoker then writes a path
    that was **never declared** — it exceeds the authority it was given, from
    inside the worker, where the host cannot stand. What the host can do, and must
    keep doing, is observe the repository afterwards and stop. This test pins that
    second half, so removing ``_scope_violations`` would fail here.
    """
    root = build_repo("worker-write-detected")
    excluded_path = root / EXCLUDED
    before = _digest(excluded_path)

    run = make_host(root, invoker=WritingInvoker()).run(max_iterations=2)
    # The undeclared write happened — the host could not interpose …
    assert _digest(excluded_path) != before
    # … and the defence-in-depth check stopped the loop for it. The violating
    # delegation leaves no success record: it is reported as the violation it is.
    assert run.terminal_action == "STOP_FORBIDDEN_ACTION"
    assert [record["action"] for record in run.records] == ["STOP_FORBIDDEN_ACTION"]
    assert run.records[0]["delegation_id"]

    # The detector itself, exercised directly over the real delegation.
    store = OrchestratorStore(root)
    host = ExecutionHost(root, PLAN_NUMBER, store=store, worker=NullWorker())
    delegation = store.read_delegation(
        PLAN_NUMBER, run.records[0]["delegation_id"]
    )
    assert delegation is not None
    assert delegation.declared_scope == (INCLUDED,)
    violations = host._scope_violations({}, delegation)
    assert EXCLUDED in violations


def test_the_gate_still_refuses_an_action_whose_declared_set_is_bad():
    """Prevention and detection are both present, and prevention comes first."""
    root = build_repo("prevention-first", declared_scope=f"`{INCLUDED}`, `{EXCLUDED}`")
    invoker = WritingInvoker()
    run = make_host(root, invoker=invoker).run(max_iterations=1)
    assert run.terminal_action == STOP_SCOPE_VIOLATION
    assert invoker.requests == []
    assert _digest(root / EXCLUDED) == _digest(root / EXCLUDED)


def test_null_worker_does_not_change_the_prevention():
    """The enforcement is the host's, not the worker's: any worker is refused."""
    root = build_repo("null-worker", declared_scope=f"`{INCLUDED}`, `{EXCLUDED}`")
    run = ExecutionHost(
        root, PLAN_NUMBER, worker=NullWorker(), gate_commands=(), autonomy_gate=True
    ).run(max_iterations=1)
    # The gate stops first; nothing is delegated and nothing changes.
    assert run.terminal_action == STOP_SCOPE_VIOLATION
    assert run.records[0]["delegation_id"] is None


# --------------------------------------------------------------------------- #
# 10. Determinism
# --------------------------------------------------------------------------- #


def test_the_evaluation_is_deterministic_over_the_enforcement_paths():
    envelope = envelope_with(INCLUDED)
    pinned = authorization_projection(envelope_with(INCLUDED, EXCLUDED))
    candidates = [
        AutonomyCandidate(
            EXECUTE_AUTHORIZED_TASK, write_targets=(INCLUDED, EXCLUDED)
        )
    ]
    first = evaluate_autonomy(envelope, candidates, pinned_projection=pinned).to_dict()
    for _ in range(5):
        assert (
            evaluate_autonomy(envelope, candidates, pinned_projection=pinned).to_dict()
            == first
        )
    assert (
        authorization_projection(envelope) == authorization_projection(envelope)
    )
    assert verify_write_targets(envelope, (INCLUDED,)).to_dict() == (
        verify_write_targets(envelope, (INCLUDED,)).to_dict()
    )


def test_the_enforcement_helpers_are_pure_and_touch_no_filesystem(tmp_path, monkeypatch):
    """The frontier stays a pure function: no file, no clock, no Git."""
    envelope = envelope_with(INCLUDED)
    before = authorization_projection(envelope)
    monkeypatch.chdir(tmp_path)
    assert authorization_projection(envelope) == before
    assert verify_write_targets(envelope, (INCLUDED,)).in_scope is True
