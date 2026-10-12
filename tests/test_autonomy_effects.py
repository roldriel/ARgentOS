"""Effect admission and the resource ceiling of the DEV autonomy envelope (plan 159).

Two frontiers of the envelope that ADR-19 decided and left unimplemented are
materialized here, and this module is their falsification:

- **Effect admission.** The plan declares the effects it may produce outside the
  immediate frontier (``## Efectos declarados``, the surface the authority act of
  plan 151 adopted). The host admits every declared effect — recognized class,
  authorizing status, resolvable reference — **before** the delegation exists, all
  or nothing, and it admits them independently of any path: an effect needs no
  ``write-target``, which is the operative reading of "``Effect`` is orthogonal to
  ``Scope``" (ADR-19 `AE-3`).
- **Resource ceiling.** The plan declares how much delegated execution it
  authorizes. The host reads it, accumulates consumption from the delegations
  actually registered in the journal, survives a restart because nothing is kept
  in the host, and stops when the ceiling is exhausted. The ceiling is an
  operational termination guard: it never produces authority (ADR-19 `AE-6`,
  decision `D-3`).

A test that passes before and after the implementation is not a falsification, so
each host-level case asserts the property the previous code could not satisfy: no
delegation recorded, no worker result, the invoker never reached, the artifact
byte-identical — and, for the counter-proof, that the write really happens when
the declaration is honest.

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
from runtime.orchestrator.agent_worker import AgentWorker
from runtime.orchestrator.autonomy import (
    EFFECT_AUTHORIZED_BY,
    EFFECT_KINDS,
    EFFECT_STATUSES,
    EffectAdmission,
    EXECUTE_AUTHORIZED_TASK,
    STOP_AUTHORITY_REQUIRED,
    STOP_MAX_ITERATIONS,
    AutonomyCandidate,
    AutonomyEnvelope,
    DeclaredEffectView,
    admit_declared_effects,
    authorization_effects_projection,
    authorization_projection,
    declared_effect_classes,
    evaluate_autonomy,
    evaluate_candidate,
)
from runtime.orchestrator.contracts import STOP_FORBIDDEN_ACTION, WorkerResult
from runtime.orchestrator.host import ExecutionHost
from runtime.orchestrator.observation import (
    observe,
    parse_declared_effects,
    parse_agent_task,
)
from runtime.orchestrator.store import OrchestratorStore
from runtime.orchestrator.worker import classify_executed_effects

PLAN_NUMBER = 902
PLAN_NAME = f"{PLAN_NUMBER:03d}-autonomy-effects.md"
INDEX_PATH = "docs/plans/INDEX.md"
TARGET = "src/target.py"
CHECK_OK = "import sys\nprint('ok')\nsys.exit(0)\n"

SCRATCH_ROOT = pytest_isolation.scratch_root("autonomy-effects")

#: The plan template. ``{effects}`` is the ``## Efectos declarados`` block, so a
#: test can build a plan that declares an authorized effect, one that declares an
#: unauthorized effect, one with an unknown class, or one that declares nothing at
#: all — the four shapes the admission has to tell apart.
PLAN_TEMPLATE = """# Plan {plan} — synthetic change with a declared effect frontier

**Status:** Aprobado para ejecución
**Fecha:** 2026-10-11
**RFC:** — (synthetic)
**Clase:** — (synthetic)
**Change Level:** L1

## Objetivo

Synthetic change that exercises the effect axis and the resource ceiling of the
DEV autonomy envelope.

## Criterio de entrada

- [x] synthetic entry criterion satisfied

## Entregables

1. `{target}`

## Pasos

1. Do the authorized work only.

## Delegación agentiva

- **Task:** implement the authorized work
- **Scope:** `{target}`
{ceiling}

{effects}

## Criterios de salida

- [ ] synthetic

## Verificación

```bash
python src/check_ok.py
```

## Validation anchor

<!-- container the host records into; empty by design -->

## Checkpoint / cierre

<!-- container the host records into; empty by design -->

## Findings / Correcciones / Pending

### Findings

N/A — sin registros reales.

### Correcciones

N/A

### Pending decisions

N/A
"""

NEGATIVE_EFFECTS = """## Efectos declarados

| Efecto | Qué produce | Autorización (referencia) | Estado |
|---|---|---|---|
| — | ninguno: la tarea autorizada escribe solo dentro del scope declarado. | — | `authorized` |"""


def effects_block(*rows: tuple[str, str, str, str]) -> str:
    lines = [
        "## Efectos declarados",
        "",
        "| Efecto | Qué produce | Autorización (referencia) | Estado |",
        "|---|---|---|---|",
    ]
    lines += ["| " + " | ".join(row) + " |" for row in rows]
    return "\n".join(lines)


AUTHORIZED_EFFECT = effects_block(
    ("network", "consulta un endpoint del proveedor", "`user`", "`authorized`")
)
UNAUTHORIZED_EFFECT = effects_block(
    ("remote_git", "empuja a un remoto", "`user`", "`not_authorized`")
)
PENDING_EFFECT = effects_block(
    ("install", "instala una dependencia", "`user`", "`pending_user_confirmation`")
)
UNKNOWN_CLASS_EFFECT = effects_block(
    ("teleport", "clase fuera del vocabulario", "`user`", "`authorized`")
)
UNRESOLVED_REFERENCE_EFFECT = effects_block(
    ("network", "consulta un endpoint", "—", "`authorized`")
)


def _scratch(name: str) -> Path:
    path = SCRATCH_ROOT / f"{name}-{uuid.uuid4().hex[:8]}"
    path.mkdir(parents=True, exist_ok=True)
    return path


def _git(root: Path, *args: str) -> None:
    subprocess.run(["git", *args], cwd=root, check=True, capture_output=True)


def _digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def build_repo(
    name: str,
    *,
    effects: str = NEGATIVE_EFFECTS,
    ceiling: str = "",
) -> Path:
    root = _scratch(name)
    _git(root, "init", "-q", ".")
    _git(root, "config", "user.email", "test@example.invalid")
    _git(root, "config", "user.name", "Autonomy Effects Test")
    (root / "docs" / "plans").mkdir(parents=True, exist_ok=True)
    (root / "src").mkdir(parents=True, exist_ok=True)
    (root / "src" / "check_ok.py").write_text(CHECK_OK, encoding="utf-8")
    (root / TARGET).write_text('"""Authorized target."""\n\nmarker = "before"\n', encoding="utf-8")
    (root / ".gitignore").write_text(".project/\n__pycache__/\n", encoding="utf-8")
    (root / "docs" / "plans" / PLAN_NAME).write_text(
        PLAN_TEMPLATE.format(
            plan=PLAN_NUMBER,
            target=TARGET,
            effects=effects,
            ceiling=ceiling,
        ),
        encoding="utf-8",
    )
    (root / INDEX_PATH).write_text(f"# Plans\n\n- {PLAN_NAME}\n", encoding="utf-8")
    _git(root, "add", "-A")
    _git(root, "commit", "-qm", "synthetic baseline")
    return root


class WritingInvoker:
    """An injected invoker that really writes, like an execution environment would.

    The repository ships no provider and no model, so a stand-in replaces the
    *model* and not the *effect*: when the delegation is admitted it performs a
    real filesystem write. That is what makes "the artifact is byte-identical" a
    property of the enforcement instead of a property of the fixture.
    """

    kind = "writing-effects"

    def __init__(self, *, write: bool = True) -> None:
        self.write = write
        self.requests: list[object] = []

    def invoke(self, request):  # noqa: ANN001, ANN201 - protocol shape
        self.requests.append(request)
        from runtime.orchestrator.agent_worker import (
            INVOCATION_COMPLETED,
            AgentInvocationResult,
        )

        if self.write:
            Path(request.root, TARGET).write_text(
                '"""Authorized target."""\n\nmarker = "after"\n', encoding="utf-8"
            )
        return AgentInvocationResult(
            status=INVOCATION_COMPLETED,
            summary="wrote the authorized target",
        )


class DeclaringWorker:
    """A worker that publishes an arbitrary set of executed effect classes.

    It stands in for an execution environment whose invocation produced an effect
    the plan never declared. The host reads the **persisted** result, not the
    worker's claim about itself, so the class-qualified entries are the whole
    input of the detection.
    """

    kind = "declaring"

    def __init__(self, executed: tuple[str, ...]) -> None:
        self.executed = executed

    def execute(self, delegation, *, store, run_id, **_: object) -> WorkerResult:  # noqa: ANN001
        result = WorkerResult(
            result_id=f"{delegation.delegation_id}-result",
            delegation_id=delegation.delegation_id,
            plan=delegation.plan,
            iteration=delegation.iteration,
            created_at="2026-10-11T00:00:00Z",
            status="completed",
            worker_kind=self.kind,
            delegation_received=delegation.to_dict(),
            intended_actions=(),
            performed_actions=(),
            artifacts_modified=(),
            commands_executed=(),
            results=(),
            evidence=(),
            problems=(),
            pending=(),
            recommended_next_action={"action": None, "advisory": True, "rationale": "test"},
            authority_used={"basis": delegation.authority_basis},
            effects_executed=self.executed,
            claims={"self_reported_completion": False},
            limitations=("test worker",),
        )
        store.write_worker_result(result)
        return result


def make_host(
    root: Path,
    *,
    worker=None,  # noqa: ANN001
    gate: bool = True,
) -> ExecutionHost:
    store = OrchestratorStore(root)
    return ExecutionHost(
        root,
        PLAN_NUMBER,
        store=store,
        worker=worker,
        gate_commands=(),
        autonomy_gate=gate,
    )


# --------------------------------------------------------------------------- #
# 1. The observation reads the declaration verbatim
# --------------------------------------------------------------------------- #


def test_the_effects_section_is_parsed_with_its_four_fields():
    effects = parse_declared_effects(AUTHORIZED_EFFECT)
    assert len(effects) == 1
    effect = effects[0]
    assert effect.effect_class == "network"
    assert effect.produced == "consulta un endpoint del proveedor"
    assert effect.authorization_reference == "`user`"
    assert effect.status == "authorized"
    assert effect.unreadable is False


def test_a_negative_declaration_states_absence_and_is_not_an_effect():
    assert parse_declared_effects(NEGATIVE_EFFECTS) == ()


def test_an_absent_section_declares_nothing():
    assert parse_declared_effects("## Objetivo\n\nNada.\n") == ()


def test_an_unknown_class_is_preserved_verbatim_never_interpreted():
    effects = parse_declared_effects(UNKNOWN_CLASS_EFFECT)
    assert [effect.effect_class for effect in effects] == ["teleport"]


def test_the_resource_ceiling_is_read_and_a_malformed_one_is_a_declared_gap():
    declared = parse_agent_task(
        "## Delegación agentiva\n\n- **Task:** t\n- **Scope:** `src/a.py`\n"
        "- **Resource ceiling:** `4` ejecuciones delegadas\n"
    )
    assert declared.resource_ceiling == 4
    assert declared.ceiling_declared is True
    assert declared.ceiling_gap == ""

    malformed = parse_agent_task(
        "## Delegación agentiva\n\n- **Task:** t\n- **Scope:** `src/a.py`\n"
        "- **Resource ceiling:** sin techo declarado\n"
    )
    assert malformed.resource_ceiling is None
    assert malformed.ceiling_declared is True
    assert "cannot be enforced" in malformed.ceiling_gap


def test_the_observation_declares_whether_the_effects_container_exists():
    declared = build_repo("obs-declared", effects=AUTHORIZED_EFFECT)
    absent = build_repo("obs-absent", effects="")
    assert observe(declared, PLAN_NUMBER, OrchestratorStore(declared)).declared_effects_unresolved is False
    assert observe(absent, PLAN_NUMBER, OrchestratorStore(absent)).declared_effects_unresolved is True


# --------------------------------------------------------------------------- #
# 2. Admission: the four verdicts, and effect ⊥ scope
# --------------------------------------------------------------------------- #


def envelope_with(*effects: DeclaredEffectView) -> AutonomyEnvelope:
    return AutonomyEnvelope(
        task="implement the authorized work",
        scope_paths=(TARGET,),
        authority_basis="synthetic",
        plan=PLAN_NUMBER,
        plan_authorized=True,
        declaration_present=True,
        authorizing_status="Aprobado para ejecución",
        plan_path=f"docs/plans/{PLAN_NAME}",
        declared_effects=tuple(effects),
    )


def view(
    effect_class: str,
    *,
    status: str = "authorized",
    reference: str = "`user`",
    unreadable: bool = False,
) -> DeclaredEffectView:
    return DeclaredEffectView(
        effect_class=effect_class,
        produced="synthetic",
        authorization_reference=reference,
        status=status,
        unreadable=unreadable,
    )


def test_the_adopted_vocabulary_is_the_one_the_repository_already_verified():
    assert EFFECT_KINDS == (
        "network",
        "remote_git",
        "install",
        "destructive",
        "write_outside_project",
    )
    assert EFFECT_AUTHORIZED_BY == ("user", "unattended_default")
    assert EFFECT_STATUSES == ("authorized", "not_authorized", "pending_user_confirmation")


def test_case_a_declared_and_authorized_admits():
    envelope = envelope_with(view("network"))
    verdict = admit_declared_effects(envelope, envelope.declared_effects)
    assert verdict.admitted is True
    assert verdict.admission == EffectAdmission.ADMITTED


def test_case_c_declared_without_authorization_stops():
    envelope = envelope_with(view("remote_git", status="not_authorized"))
    verdict = admit_declared_effects(envelope, envelope.declared_effects)
    assert verdict.admitted is False
    assert verdict.admission == EffectAdmission.NOT_AUTHORIZED
    assert "not_authorized" in verdict.reason


def test_case_c_pending_user_confirmation_is_not_a_continuation():
    envelope = envelope_with(view("install", status="pending_user_confirmation"))
    verdict = admit_declared_effects(envelope, envelope.declared_effects)
    assert verdict.admitted is False
    assert verdict.admission == EffectAdmission.NOT_AUTHORIZED


def test_case_c_an_unresolvable_authorization_reference_is_not_authorization():
    envelope = envelope_with(view("network", reference="—"))
    verdict = admit_declared_effects(envelope, envelope.declared_effects)
    assert verdict.admitted is False
    assert verdict.admission == EffectAdmission.NOT_AUTHORIZED


def test_case_d_an_unknown_class_stops_and_a_human_decides():
    envelope = envelope_with(view("teleport"))
    verdict = admit_declared_effects(envelope, envelope.declared_effects)
    assert verdict.admitted is False
    assert verdict.admission == EffectAdmission.UNKNOWN_CLASS
    assert verdict.effect_class == "teleport"
    assert "not in the adopted DEV vocabulary" in verdict.reason


def test_case_d_an_unreadable_entry_stops_rather_than_being_assumed():
    envelope = envelope_with(view("", unreadable=True))
    verdict = admit_declared_effects(envelope, envelope.declared_effects)
    assert verdict.admitted is False
    assert verdict.admission == EffectAdmission.UNREADABLE


def test_no_declared_effect_at_all_is_a_declared_absence_not_an_authorization():
    verdict = admit_declared_effects(envelope_with(), ())
    assert verdict.admitted is False
    assert verdict.admission == EffectAdmission.UNDECLARED


def test_case_e_an_authorized_effect_without_any_write_target_is_admissible():
    """``Effect`` is orthogonal to ``Scope``: no path is required for an effect."""
    envelope = AutonomyEnvelope(
        task="implement the authorized work",
        scope_paths=(TARGET,),
        authority_basis="synthetic",
        plan=PLAN_NUMBER,
        plan_authorized=True,
        declaration_present=True,
        authorizing_status="Aprobado para ejecución",
        declared_effects=(view("network"),),
    )
    candidate = AutonomyCandidate(
        action_class=EXECUTE_AUTHORIZED_TASK,
        # No target_path and no write_targets at all: the effects are the whole
        # declaration this action proceeds under.
        effects=(view("network"),),
    )
    outcome = evaluate_candidate(envelope, candidate)
    # The scope axis is not what decided it: the outcome reports both axes.
    assert outcome.effect_admission == EffectAdmission.ADMITTED
    assert outcome.stop_condition is None or "scope" in outcome.scope_reason


def test_scope_still_binds_when_the_effects_are_admitted():
    envelope = envelope_with(view("network"))
    candidate = AutonomyCandidate(
        action_class=EXECUTE_AUTHORIZED_TASK,
        target_path="src/outside.py",
        effects=(view("network"),),
    )
    outcome = evaluate_candidate(envelope, candidate)
    assert outcome.stop_condition == "STOP_SCOPE_VIOLATION"


def test_an_unadmitted_effect_stops_even_when_the_scope_is_authorized():
    envelope = envelope_with(view("remote_git", status="not_authorized"))
    candidate = AutonomyCandidate(
        action_class=EXECUTE_AUTHORIZED_TASK,
        write_targets=(TARGET,),
        effects=(view("remote_git", status="not_authorized"),),
    )
    outcome = evaluate_candidate(envelope, candidate)
    assert outcome.stop_condition == STOP_AUTHORITY_REQUIRED
    assert outcome.verdict == "REQUIRES_HUMAN"
    assert outcome.effect_admission == EffectAdmission.NOT_AUTHORIZED


def test_declared_effect_classes_are_normalized_and_exclude_negatives():
    envelope = envelope_with(view("NETWORK"), view("—"))
    assert declared_effect_classes(envelope) == {"network"}


def test_the_effect_declaration_is_part_of_the_authorization_projection():
    envelope = envelope_with(view("network"))
    projection = authorization_projection(envelope)
    assert "authorization-effects-v1" in projection
    assert "effect: network" in projection
    assert "authorization-effects-v1" in authorization_effects_projection(envelope)


def test_rewriting_the_effect_declaration_after_the_fact_is_a_divergence():
    pinned = authorization_projection(envelope_with(view("network")))
    rewritten = authorization_effects_projection(envelope_with(view("remote_git")))
    assert "remote_git" in rewritten
    assert "network" not in rewritten.split("plan:")[1]
    # The pinned projection is the contract: a later widening to another class
    # cannot be read as the same authorization.
    assert pinned != authorization_projection(envelope_with(view("remote_git")))


# --------------------------------------------------------------------------- #
# 3. The gate, end to end: refusal before the effect, and its counter-proof
# --------------------------------------------------------------------------- #


def test_case_c_the_gate_stops_before_the_delegation_and_nothing_writes():
    root = build_repo("gate-unauthorized", effects=UNAUTHORIZED_EFFECT)
    target = root / TARGET
    before = _digest(target)
    invoker = WritingInvoker()
    host = make_host(root, worker=AgentWorker(invoker=invoker))

    run = host.run(max_iterations=1)
    record = run.records[0]

    assert run.terminal_action == STOP_AUTHORITY_REQUIRED
    assert record["authority"]["verdict"] == "REQUIRES_HUMAN"
    # The refusal precedes the effect.
    assert record["delegation_id"] is None
    assert host.store.list_worker_results(PLAN_NUMBER) == []
    assert invoker.requests == []
    assert _digest(target) == before
    # The evidence names the axis and the class.
    autonomy = record["autonomy"]
    assert autonomy["continues"] is False
    assert autonomy["outcomes"][0]["effect_admission"] == EffectAdmission.NOT_AUTHORIZED
    assert "nothing was written" in record["rationale"]


def test_case_d_an_unknown_class_stops_the_loop_before_delegating():
    root = build_repo("gate-unknown", effects=UNKNOWN_CLASS_EFFECT)
    invoker = WritingInvoker()
    host = make_host(root, worker=AgentWorker(invoker=invoker))
    run = host.run(max_iterations=1)
    record = run.records[0]
    assert run.terminal_action == STOP_AUTHORITY_REQUIRED
    assert record["autonomy"]["outcomes"][0]["effect_admission"] == EffectAdmission.UNKNOWN_CLASS
    assert invoker.requests == []
    assert record["delegation_id"] is None


def test_case_d_a_plan_with_no_effects_container_stops_an_effect_bearing_action():
    root = build_repo("gate-absent", effects="")
    invoker = WritingInvoker()
    host = make_host(root, worker=AgentWorker(invoker=invoker))
    run = host.run(max_iterations=1)
    record = run.records[0]
    assert run.terminal_action == STOP_AUTHORITY_REQUIRED
    assert record["autonomy"]["outcomes"][0]["effect_admission"] == EffectAdmission.UNREADABLE
    assert invoker.requests == []
    assert record["delegation_id"] is None


def test_the_delegation_reference_resolves_or_the_effect_is_not_admitted():
    root = build_repo("gate-unresolved-ref", effects=UNRESOLVED_REFERENCE_EFFECT)
    host = make_host(root, worker=AgentWorker(invoker=WritingInvoker()))
    run = host.run(max_iterations=1)
    assert run.records[0]["autonomy"]["outcomes"][0]["effect_admission"] == (
        EffectAdmission.NOT_AUTHORIZED
    )


def test_case_a_and_the_counter_proof_the_write_really_happens_when_declared():
    """Case A and the counter-proof in one property: same fixture, same worker.

    With the effect declared and authorized the delegation is admitted and the
    injected invoker really writes the target. The companion test above shows the
    same invocation refused — so "the artifact is byte-identical" is a property of
    the admission, never of a fixture that does not write.
    """
    root = build_repo("gate-authorized", effects=AUTHORIZED_EFFECT)
    target = root / TARGET
    before = _digest(target)
    invoker = WritingInvoker()
    host = make_host(root, worker=AgentWorker(invoker=invoker))
    run = host.run(max_iterations=1)
    record = run.records[0]
    assert record["action"] == "RUN_IMPLEMENTATION_TASK"
    assert record["delegation_id"] is not None
    assert record["autonomy"]["continues"] is True
    assert record["autonomy"]["outcomes"][0]["effect_admission"] == EffectAdmission.ADMITTED
    assert len(invoker.requests) == 1
    assert _digest(target) != before, "the invoker really wrote the target"


# --------------------------------------------------------------------------- #
# 4. The resource ceiling
# --------------------------------------------------------------------------- #


def test_the_ceiling_bounds_the_first_delegation_and_stops_the_second():
    root = build_repo(
        "ceiling-1",
        effects=AUTHORIZED_EFFECT,
        ceiling="- **Resource ceiling:** `1` ejecución delegada",
    )
    host = make_host(root, worker=AgentWorker(invoker=WritingInvoker()))
    first = host.run(max_iterations=1)
    assert first.records[0]["action"] == "RUN_IMPLEMENTATION_TASK"
    assert first.records[0]["delegation_id"] is not None

    # A second delegated execution is refused: the declared ceiling is consumed,
    # and the consumption is read from the journal, not from the host's memory.
    second = host.run(max_iterations=1)
    record = second.records[0]
    assert record["terminal"] is True
    assert record["action"] == STOP_MAX_ITERATIONS
    assert record["delegation_id"] is None
    assert record["autonomy"]["resource_stop"] == STOP_MAX_ITERATIONS
    assert record["autonomy"]["resource_ceiling"] == 1
    assert record["autonomy"]["resource_consumed"] == 1


def test_resource_exhaustion_is_never_an_authorization():
    """`AE-6`: an operational limit reached produces no authority whatsoever."""
    root = build_repo(
        "ceiling-not-authority",
        effects=AUTHORIZED_EFFECT,
        ceiling="- **Resource ceiling:** `1` ejecución delegada",
    )
    host = make_host(root, worker=AgentWorker(invoker=WritingInvoker()))
    host.run(max_iterations=1)
    second = host.run(max_iterations=1)
    record = second.records[0]
    autonomy = record["autonomy"]
    assert autonomy["resource_stop"] == STOP_MAX_ITERATIONS
    assert autonomy["authority"].startswith("none:")
    assert record["authority"]["verdict"] != "AUTHORIZED_EXISTING"
    assert "produces no authorization" in record["rationale"]


def test_the_ceiling_survives_a_process_restart_because_it_is_read_from_evidence():
    """Two hosts, no shared memory: the consumption is the journal's, not the host's."""
    root = build_repo(
        "ceiling-restart",
        effects=AUTHORIZED_EFFECT,
        ceiling="- **Resource ceiling:** `1` ejecución delegada",
    )
    first_host = make_host(root, worker=AgentWorker(invoker=WritingInvoker()))
    first_host.run(max_iterations=1)

    # A brand-new host instance, as a restarted process would build.
    second_host = make_host(root, worker=AgentWorker(invoker=WritingInvoker()))
    record = second_host.run(max_iterations=1).records[0]
    assert second_host._last_autonomy is not None
    assert second_host._last_autonomy.resource_consumed == 1
    assert record["action"] == STOP_MAX_ITERATIONS


def test_an_exhausted_ceiling_stops_even_when_no_action_would_be_delegated():
    """The operational axis is checked before any continuation is granted."""
    root = build_repo("ceiling-noop", effects=AUTHORIZED_EFFECT)
    plan = root / "docs" / "plans" / PLAN_NAME
    text = plan.read_text(encoding="utf-8").replace(
        "- **Task:** implement the authorized work",
        "- **Task:** implement the authorized work\n- **Resource ceiling:** `0`",
    )
    plan.write_text(text, encoding="utf-8")
    _git(root, "add", "-A")
    _git(root, "commit", "-qm", "synthetic ceiling")

    observation = observe(root, PLAN_NUMBER, OrchestratorStore(root))
    assert observation.agent_task.resource_ceiling is None
    assert observation.agent_task.ceiling_gap
    assert any("ceiling" in gap for gap in observation.gaps)


def test_the_resource_axis_does_not_enter_the_declared_envelope():
    """The ceiling is not a declaration of autonomy: it neither grants nor widens it."""
    root = build_repo(
        "ceiling-outside-envelope",
        effects=AUTHORIZED_EFFECT,
        ceiling="- **Resource ceiling:** `1` ejecución delegada",
    )
    from runtime.orchestrator.host import _autonomy_envelope

    observation = observe(root, PLAN_NUMBER, OrchestratorStore(root))
    _declaration, bounded = _autonomy_envelope(observation, PLAN_NUMBER)
    assert not hasattr(bounded, "resource_ceiling"), (
        "the ceiling must not become a field of the autonomy envelope: that would "
        "make an operational limit part of what authorizes the execution"
    )
    assert observation.agent_task.resource_ceiling == 1


def test_evaluate_autonomy_reports_the_resource_stop_without_authority():
    result = evaluate_autonomy(
        envelope_with(view("network")),
        [AutonomyCandidate(action_class=EXECUTE_AUTHORIZED_TASK, write_targets=(TARGET,))],
        resource_ceiling=2,
        resource_consumed=2,
        resource_required=True,
    )
    assert result.continues is False
    assert result.resource_stop == STOP_MAX_ITERATIONS
    assert result.stop_condition == STOP_MAX_ITERATIONS
    assert result.authority.startswith("none:")
    assert result.resource_ceiling == 2
    assert result.resource_consumed == 2


def test_evaluate_autonomy_does_not_stop_while_the_ceiling_has_room():
    result = evaluate_autonomy(
        envelope_with(view("network")),
        [AutonomyCandidate(action_class=EXECUTE_AUTHORIZED_TASK, write_targets=(TARGET,))],
        resource_ceiling=3,
        resource_consumed=1,
        resource_required=True,
    )
    assert result.continues is True
    assert result.resource_stop is None


# --------------------------------------------------------------------------- #
# 5. Worker effects: declared vs executed
# --------------------------------------------------------------------------- #


def test_the_worker_publishes_qualified_effect_entries_and_nothing_else():
    python_only = classify_executed_effects(
        commands=[["python", "src/check_ok.py"], ["python", "-m", "pytest", "tests/"]]
    )
    assert python_only == ()
    network = classify_executed_effects(commands=[["curl", "https://example.invalid"]])
    assert network == ("effect:network",)
    remote = classify_executed_effects(
        commands=[["git", "push", "origin", "dev"]]
    )
    assert remote == ("effect:remote_git",)


def test_an_executed_effect_the_plan_never_declared_is_a_finding_and_stops():
    root = build_repo("executed-undeclared", effects=NEGATIVE_EFFECTS)
    host = make_host(
        root,
        worker=DeclaringWorker(("effect:network", "an honest narrative entry")),
    )
    run = host.run(max_iterations=1)
    record = run.records[0]
    assert record["action"] == STOP_FORBIDDEN_ACTION
    assert record["terminal"] is True
    assert "does not declare and authorize" in record["rationale"]
    assert any("effect violation" in note for note in record["notes"])


def test_an_executed_effect_the_plan_did_declare_does_not_stop():
    root = build_repo("executed-declared", effects=AUTHORIZED_EFFECT)
    host = make_host(root, worker=DeclaringWorker(("effect:network",)))
    run = host.run(max_iterations=1)
    record = run.records[0]
    assert record["action"] == "RUN_IMPLEMENTATION_TASK"
    assert record["terminal"] is False


def test_a_narrative_entry_is_not_read_as_an_effect_class():
    root = build_repo("executed-narrative", effects=NEGATIVE_EFFECTS)
    host = make_host(
        root,
        worker=DeclaringWorker(("network access was used", "effect:")),
    )
    run = host.run(max_iterations=1)
    assert run.records[0]["action"] == "RUN_IMPLEMENTATION_TASK"
