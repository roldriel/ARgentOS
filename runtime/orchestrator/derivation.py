"""Derivation of the next valid action (plan 122 §7).

This is the logic a human performs manually today, expressed as a pure,
deterministic function of an observation. Nothing is persisted here: there is no
``next_state``, no cursor and no second representation of the change. The same
observation always derives the same action, and a restart derives it again from
the repository.

Every rule is a *reading* of an existing mechanism (RFC-75's plan lifecycle,
anchors, checkpoints, findings, pending decisions and derived conditions). No new
state is invented to express any of these conditions.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Iterable, Mapping, Sequence

from .authority import AuthorityBoundary
from .contracts import (
    ANOMALY,
    BOUNDARY,
    CLOSED_DERIVED,
    EXCLUDED,
    FAIL,
    GAP,
    NOT_APPLICABLE,
    RECORD_CHECKPOINT,
    RECORD_PLAN_STATUS_EXECUTED,
    RECORD_REVALIDATION_ANCHOR,
    RECORD_VALIDATION_ANCHOR,
    RUN_IMPLEMENTATION_TASK,
    RUN_LIFECYCLE_GATES,
    RUN_REVALIDATION,
    RUN_VALIDATION,
    STOP_AWAIT_PLAN_AUTHORIZATION,
    STOP_BLOCKING_PENDING_DECISION,
    STOP_ENTRY_CRITERIA_UNMET,
    STOP_FINDING_REQUIRES_HUMAN,
    STOP_FORBIDDEN_ACTION,
    STOP_GATE_ANOMALY,
    STOP_GATE_INCOMPLETE,
    STOP_MAX_ITERATIONS,
    STOP_NO_PROGRESS,
    STOP_OPEN_FINDINGS,
    STOP_PLAN_NOT_FOUND,
    STOP_PLAN_SUPERSEDED,
    STOP_VALIDATION_FAIL,
    STOP_WORKER_RESULT_INVALID,
    STOP_WORKER_RESULT_MISSING,
    VALID,
    AuthorityDecision,
    is_terminal,
)
from .observation import ChangeObservation

#: Gate identity -> the checkers of the lifecycle that produce it.
GATE_NAMES = ("C-1", "C-2", "C-3")

#: Gate signals that are acceptable when the gate is not yet applicable.
_NON_BLOCKING_GATE_SIGNALS = frozenset({VALID, NOT_APPLICABLE, EXCLUDED})


@dataclass(frozen=True)
class NextAction:
    """The derived next action. Terminal actions end the iteration sequence."""

    kind: str
    rationale: str
    evidence_refs: tuple[str, ...] = ()
    authority: AuthorityDecision | None = None

    @property
    def terminal(self) -> bool:
        return is_terminal(self.kind)

    def to_dict(self) -> dict[str, Any]:
        return {
            "kind": self.kind,
            "rationale": self.rationale,
            "evidence_refs": list(self.evidence_refs),
            "terminal": self.terminal,
            "authority": None if self.authority is None else self.authority.to_dict(),
        }


def _decision(
    kind: str,
    rationale: str,
    boundary: AuthorityBoundary,
    evidence_refs: Sequence[str] = (),
    basis_hint: str = "",
) -> NextAction:
    return NextAction(
        kind=kind,
        rationale=rationale,
        evidence_refs=tuple(evidence_refs),
        authority=boundary.evaluate(kind, basis_hint=basis_hint),
    )


def stop_action(
    kind: str,
    rationale: str,
    boundary: AuthorityBoundary,
    evidence_refs: Sequence[str] = (),
) -> NextAction:
    """Build a host-level stop (max iterations, missing result, no progress)."""
    return _decision(kind, rationale, boundary, evidence_refs)


def gate_signals_by_name(
    gate_signals: Mapping[str, str] | None,
) -> dict[str, str]:
    """Normalise the observed gate signals into the closed gate vocabulary."""
    out: dict[str, str] = {}
    for name in GATE_NAMES:
        signal = (gate_signals or {}).get(name)
        if signal:
            out[name] = signal
    return out


def anchor_gate_problems(
    observation: ChangeObservation, gate_signals: Mapping[str, str] | None
) -> tuple[str, ...]:
    """Gate evidence a recorded anchor needs, at the anchor's own level.

    Only C-1 is required here (the anchor must be structurally valid) and C-3
    must never contradict. C-2 is deliberately *not* required at this level: a
    gate reading taken before the checkpoint existed cannot be evidence about a
    checkpoint that does not exist yet — the closure level checks that, after a
    reading for the closure state.
    """
    signals = gate_signals_by_name(gate_signals)
    problems: list[str] = []
    if observation.anchor.present:
        signal = signals.get("C-1")
        if signal != VALID:
            problems.append(
                f"C-1 reported {signal or 'no signal'} for a recorded anchor"
            )
    signal_c3 = signals.get("C-3")
    if signal_c3 not in _NON_BLOCKING_GATE_SIGNALS:
        problems.append(f"C-3 reported {signal_c3}")
    return tuple(problems)


def closure_gate_problems(
    observation: ChangeObservation, gate_signals: Mapping[str, str] | None
) -> tuple[str, ...]:
    """Gate evidence a derived closure needs, at the closure level."""
    signals = gate_signals_by_name(gate_signals)
    problems: list[str] = []
    if observation.anchor.present:
        signal = signals.get("C-1")
        if signal != VALID:
            problems.append(
                f"C-1 reported {signal or 'no signal'} for a recorded anchor"
            )
    if observation.checkpoint.present:
        signal = signals.get("C-2")
        if signal != VALID:
            problems.append(
                f"C-2 reported {signal or 'no signal'} for a recorded checkpoint"
            )
    signal_c3 = signals.get("C-3")
    if signal_c3 not in _NON_BLOCKING_GATE_SIGNALS:
        problems.append(f"C-3 reported {signal_c3}")
    return tuple(problems)


def derive_next_action(
    observation: ChangeObservation,
    boundary: AuthorityBoundary,
    *,
    validation_signals: Sequence[str] | None = None,
    gate_signals: Mapping[str, str] | None = None,
    drift: str | None = None,
) -> NextAction:
    """Derive the next valid action from the observation, deterministically.

    ``validation_signals`` are the real signals of the last executed validation
    command-set; ``gate_signals`` maps ``C-1``/``C-2``/``C-3`` to their real
    classification. Neither is inferred from an exit code. Both default to the
    values the observation already carries, so a caller cannot accidentally
    derive from *no* evidence while evidence exists.
    """
    if validation_signals is None:
        validation_signals = observation.validation_signals
    if gate_signals is None:
        gate_signals = observation.gate_signals
    refs: tuple[str, ...] = (observation.plan_path or f"plan-{observation.plan}",)

    # 1 — the change must exist and be authorized for execution.
    if not observation.plan_present:
        return _decision(
            STOP_PLAN_NOT_FOUND,
            f"plan {observation.plan} was not found under docs/plans/",
            boundary,
            refs,
        )
    status = (observation.status or "").strip()
    if not status or status.startswith("Aprobado para redacción"):
        return _decision(
            STOP_AWAIT_PLAN_AUTHORIZATION,
            (
                f"plan status is {status or 'absent'!r}: execution requires "
                "'Aprobado para ejecución'. The host does not grant authorization."
            ),
            boundary,
            refs,
        )
    if status.startswith("Superseded"):
        return _decision(
            STOP_PLAN_SUPERSEDED,
            "the plan is Superseded: its change is no longer the active one",
            boundary,
            refs,
        )

    # 2 — entry criteria are a gate, not a formality.
    if not observation.entry_criteria.satisfied:
        return _decision(
            STOP_ENTRY_CRITERIA_UNMET,
            (
                "entry criteria unmet: "
                + "; ".join(observation.entry_criteria.unchecked)
            ),
            boundary,
            refs,
        )

    # 3 — a blocking pending decision always stops the loop.
    blocking = observation.blocking_pending
    if blocking:
        return _decision(
            STOP_BLOCKING_PENDING_DECISION,
            "blocking pending decision(s): "
            + ", ".join(record.ref for record in blocking),
            boundary,
            refs,
        )

    # 4 — findings: detection is the host's; resolution is the human's.
    open_findings = observation.open_findings
    if open_findings:
        anomaly_reported = any(
            signal in (ANOMALY, BOUNDARY) for signal in validation_signals
        ) or any(
            signal in (ANOMALY, BOUNDARY) for signal in set((gate_signals or {}).values())
        )
        kind = STOP_FINDING_REQUIRES_HUMAN if anomaly_reported else STOP_OPEN_FINDINGS
        return _decision(
            kind,
            (
                "open finding(s) require human resolution or explicit deferral "
                "with owner: "
                + ", ".join(record.ref for record in open_findings)
            ),
            boundary,
            refs + tuple(record.ref for record in open_findings),
        )

    # 5 — a mechanical violation (FAIL) must be fixed or explicitly deferred by
    #     the maintainer; the host never reports it as PASS.
    failures = [signal for signal in validation_signals if signal == FAIL]
    if failures:
        return _decision(
            STOP_VALIDATION_FAIL,
            (
                f"the declared validation command-set produced {len(failures)} "
                "FAIL signal(s): a mechanical violation must be fixed or its "
                "deviation accepted by the maintainer (a declared environmental "
                "class is reported as GAP, never as PASS)"
            ),
            boundary,
            refs,
        )

    # 6 — contradictions and ambiguity in the gates stop the loop.
    blocking_gates = sorted(
        name
        for name, signal in gate_signals_by_name(gate_signals).items()
        if signal in (ANOMALY, BOUNDARY)
    )
    if blocking_gates:
        return _decision(
            STOP_GATE_ANOMALY,
            "lifecycle gate(s) reported a blocking signal: "
            + ", ".join(blocking_gates),
            boundary,
            refs,
        )

    # 7 — the plan declares authorized semantic work and no worker result exists
    #     for the *current* content state. The work comes before the validation
    #     that must read its result: validating first would produce evidence
    #     about a state the implementation is about to change.
    if (
        observation.agent_task.declared
        and not observation.implementation_done_for_current_state
        and not observation.implementation_already_satisfied
    ):
        return _decision(
            RUN_IMPLEMENTATION_TASK,
            (
                "the authorized plan declares an agent task and no worker result "
                "covers the current content state: delegate the declared work to a "
                "worker (the plan authorizes it; the host only conducts it)"
            ),
            boundary,
            refs,
        )

    # 8 — no validation evidence for the current state yet.
    if not observation.anchor.present:
        if observation.validation_done_for_current_state:
            return _decision(
                RECORD_VALIDATION_ANCHOR,
                (
                    "the declared validation command-set really ran over the "
                    "current content: record the Validation Anchor from the "
                    "observed evidence (the record is factual, not a decision)"
                ),
                boundary,
                refs,
            )
        return _decision(
            RUN_VALIDATION,
            (
                "no validation anchor is recorded for this change: execute the "
                "plan's declared validation command-set"
            ),
            boundary,
            refs,
        )

    # 9 — a recorded anchor that no longer matches the observed content.
    if observation.anchor_stale:
        if observation.revalidation_done_for_current_state:
            return _decision(
                RECORD_REVALIDATION_ANCHOR,
                (
                    "the same contract was re-run over the new state: record A2 "
                    "with its own anchor; A1 is preserved and never mutated"
                ),
                boundary,
                refs,
            )
        return _decision(
            RUN_REVALIDATION,
            (
                "the recorded validation anchor is stale for the current scoped "
                "content (delta "
                f"{observation.anchor.delta_identity} != "
                f"{observation.current_delta_identity}): re-run the same contract "
                "over the new state (A2)"
            ),
            boundary,
            refs,
        )

    # 10 — the anchor exists; the lifecycle gates have not been read for *this*
    #     state yet. A previous gate reading is not evidence about a new state.
    if not observation.gates_run_for_current_state:
        return _decision(
            RUN_LIFECYCLE_GATES,
            (
                "the lifecycle gates have not read the current validated state "
                "yet (a previous reading is not evidence about a new state)"
            ),
            boundary,
            refs,
        )

    problems = anchor_gate_problems(observation, gate_signals)
    if problems:
        return _decision(
            STOP_GATE_INCOMPLETE,
            "lifecycle gate evidence is insufficient at the anchor level: "
            + "; ".join(problems),
            boundary,
            refs,
        )

    # 11 — implementation + validation is claimed only after real PASS evidence.
    if not status.startswith("Executed"):
        return _decision(
            RECORD_PLAN_STATUS_EXECUTED,
            (
                "implementation and validation are evidenced (anchor + gates): "
                "record the plan status Executed"
            ),
            boundary,
            refs,
        )

    # 12 — the checkpoint is the documented relation closure ↔ Git state, and it
    #       must correspond to the state that is actually being closed.
    if (
        not observation.checkpoint.present
        or observation.checkpoint.closure_tree != observation.current_state_identity
    ):
        return _decision(
            RECORD_CHECKPOINT,
            (
                "no checkpoint corresponds to the current closure state: record "
                "closure ↔ Git state (GC-1)"
            ),
            boundary,
            refs,
        )

    # 13 — the gates must be re-read for the closure state.
    if not observation.gates_run_for_current_closure:
        return _decision(
            RUN_LIFECYCLE_GATES,
            (
                "the checkpoint has not been checked against its anchor for this "
                "closure state yet (C-2)"
            ),
            boundary,
            refs,
        )

    problems = closure_gate_problems(observation, gate_signals)
    if problems:
        return _decision(
            STOP_GATE_INCOMPLETE,
            "closure gate evidence is insufficient: " + "; ".join(problems),
            boundary,
            refs,
        )

    # 14 — Closed is derived here and released nowhere: release is human authority.
    return _decision(
        CLOSED_DERIVED,
        (
            "Closed conditions satisfied: Executed + governance + checkpoint + "
            "consistency + PASS evidence for the closure state. Closed is "
            "derived, not written as a status; release requires human authority "
            "and the host never executes it"
        ),
        boundary,
        refs,
    )


def max_iterations_action(
    boundary: AuthorityBoundary, limit: int
) -> NextAction:
    return stop_action(
        STOP_MAX_ITERATIONS,
        f"iteration limit reached ({limit}) without a terminal derivation",
        boundary,
    )


def no_progress_action(
    boundary: AuthorityBoundary, kind: str, fingerprint: str
) -> NextAction:
    return stop_action(
        STOP_NO_PROGRESS,
        (
            f"no progress: the derived action {kind} repeats with an unchanged "
            f"governance observation ({fingerprint[:16]}…)"
        ),
        boundary,
    )


def missing_result_action(
    boundary: AuthorityBoundary, delegation_id: str
) -> NextAction:
    return stop_action(
        STOP_WORKER_RESULT_MISSING,
        (
            f"delegation {delegation_id} has no persistent worker result: the "
            "evidence is absent (GAP), so no claim can be made about it"
        ),
        boundary,
    )


def invalid_result_action(
    boundary: AuthorityBoundary, delegation_id: str, problems: Sequence[str]
) -> NextAction:
    return stop_action(
        STOP_WORKER_RESULT_INVALID,
        (
            f"worker result for delegation {delegation_id} does not satisfy the "
            "M4 contract: " + "; ".join(problems)
        ),
        boundary,
    )


def forbidden_scope_action(
    boundary: AuthorityBoundary,
    delegation_id: str,
    violations: Sequence[str],
    authorized: Sequence[str],
) -> NextAction:
    """A worker modified content outside the scope the delegation authorized.

    The host detects it from the repository (not from the worker's claim) and
    stops: accepting the modification would be the host expanding the authorized
    scope, which belongs to the human who authorized the plan.
    """
    return stop_action(
        STOP_FORBIDDEN_ACTION,
        (
            f"delegation {delegation_id} modified {len(violations)} path(s) "
            "outside the authorized scope: "
            + ", ".join(violations)
            + ". The authorized scope was: "
            + (", ".join(authorized) if authorized else "(none declared)")
            + ". Widening the scope of an authorized change is a human decision; "
            "the host records the evidence and does not accept the modification."
        ),
        boundary,
        evidence_refs=tuple(violations),
    )
