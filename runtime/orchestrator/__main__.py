#!/usr/bin/env python3
"""CLI of the DEV Autonomous Orchestrator (plan 122).

Usage::

    python -m runtime.orchestrator --plan 122 [--root REPO_ROOT]
        [--max-iterations N] [--run-id ID] [--worker command|agent|none]
    python -m runtime.orchestrator --plan 122 --observe [--json]
    python -m runtime.orchestrator --plan 122 --reconstruct [RUN_ID] [--json]

Modes:

``--observe``      observe and derive once; write nothing, run nothing.
``--reconstruct``  rebuild a run's recorrido from persisted evidence only.
default            run the loop until a terminal derivation or a stop condition.

Workers:

``command``  really executes the delegated command-set (the default).
``agent``    delegates the plan's authorized task to the Agent Worker. The CLI can
             only build the honest default (``NullAgentInvoker``: no provider, no
             model, no network exists in this repository); an embedding execution
             environment injects its own ``AgentInvoker`` by constructing
             ``ExecutionHost(..., worker=AgentWorker(invoker=...))``.
``none``     executes nothing and reports exactly that.

Exit codes (declared contract):

- ``0`` — the loop reached a settled terminal derivation (including the stops
  that require human authority: a stop is a correct outcome, not a failure);
- ``1`` — the loop settled on a signal class that requires attention
  (``ANOMALY``/``FAIL``/invalid worker result): the host never reports it as PASS;
- ``2`` — unrecoverable read error while observing the repository.

Standard library only. No network. Nothing under ``protocol/.agents/`` is read as
instructions and nothing there is ever written.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from .authority import AuthorityBoundary
from .contracts import (
    STOP_FINDING_REQUIRES_HUMAN,
    STOP_GATE_ANOMALY,
    STOP_GATE_INCOMPLETE,
    STOP_VALIDATION_FAIL,
    STOP_WORKER_RESULT_INVALID,
    STOP_WORKER_RESULT_MISSING,
)
from .derivation import derive_next_action
from .host import DEFAULT_MAX_ITERATIONS, ExecutionHost
from .observation import ObservationError, observe
from .store import OrchestratorStore
from .agent_worker import AgentWorker
from .worker import CommandWorker, NullWorker, WorkerAdapter

#: Terminal derivations whose signal class requires attention (exit 1).
ATTENTION_ACTIONS = frozenset(
    {
        STOP_GATE_ANOMALY,
        STOP_GATE_INCOMPLETE,
        STOP_VALIDATION_FAIL,
        STOP_FINDING_REQUIRES_HUMAN,
        STOP_WORKER_RESULT_MISSING,
        STOP_WORKER_RESULT_INVALID,
    }
)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="python -m runtime.orchestrator",
        description=(
            "Conduct one DEV Change autonomously: observe → derive → authorize → "
            "delegate → execute → ingest → verify → decide → continue/stop."
        ),
    )
    parser.add_argument("--plan", type=int, required=True, help="plan number")
    parser.add_argument("--root", type=Path, default=None)
    parser.add_argument(
        "--max-iterations",
        type=int,
        default=DEFAULT_MAX_ITERATIONS,
        help=f"iteration limit of this run (default {DEFAULT_MAX_ITERATIONS})",
    )
    parser.add_argument("--run-id", default=None)
    parser.add_argument(
        "--worker",
        choices=("command", "agent", "none"),
        default="command",
        help=(
            "command: really execute the delegated command-set; agent: delegate "
            "the plan's authorized task to the Agent Worker; none: execute nothing"
        ),
    )
    parser.add_argument(
        "--observe",
        action="store_true",
        help="observe and derive once without executing or writing anything",
    )
    parser.add_argument(
        "--reconstruct",
        nargs="?",
        const="",
        default=None,
        metavar="RUN_ID",
        help="rebuild the recorrido of a run from persisted evidence",
    )
    parser.add_argument("--json", action="store_true", help="machine-readable output")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    root = (args.root or Path(__file__).resolve().parents[2]).resolve()
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")

    store = OrchestratorStore(root)

    if args.observe:
        try:
            observation = observe(root, args.plan, store)
        except ObservationError as exc:
            print(f"error: {exc}", file=sys.stderr)
            return 2
        boundary = AuthorityBoundary(
            plan_authorized=observation.authorized_for_execution
        )
        action = derive_next_action(
            observation,
            boundary,
            validation_signals=observation.validation_signals,
            gate_signals=observation.gate_signals,
        )
        payload = {
            "observation": observation.to_dict(),
            "derived_action": action.to_dict(),
        }
        if args.json:
            print(json.dumps(payload, indent=2, ensure_ascii=False, sort_keys=True))
        else:
            print(f"plan {args.plan}: status={observation.status!r}")
            print(f"anchor={observation.anchor.present} stale={observation.anchor_stale}"
                  f" checkpoint={observation.checkpoint.present}")
            print(f"derived action: {action.kind}")
            print(f"  {action.rationale}")
            if action.authority is not None:
                print(f"  authority: {action.authority.verdict} — {action.authority.basis}")
        return 0

    if args.reconstruct is not None:
        host = ExecutionHost(
            root, args.plan, store=store, run_id=args.run_id or "run"
        )
        report = host.reconstruct(args.reconstruct or None)
        print(report)
        return 0

    worker: WorkerAdapter
    if args.worker == "agent":
        # The CLI can only construct the honest default: this repository ships no
        # provider and no model. An embedding environment injects its own
        # AgentInvoker through `ExecutionHost(..., worker=AgentWorker(invoker=...))`.
        worker = AgentWorker()
    elif args.worker == "none":
        worker = NullWorker()
    else:
        worker = CommandWorker()
    host = ExecutionHost(
        root,
        args.plan,
        store=store,
        worker=worker,
        max_iterations=args.max_iterations,
        run_id=args.run_id,
    )
    try:
        run = host.run()
    except ObservationError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2

    if args.json:
        print(json.dumps(run.to_dict(), indent=2, ensure_ascii=False, sort_keys=True))
    else:
        print(f"run {run.run_id} — plan {run.plan} — {run.iterations} iteration(s)")
        for record in run.records:
            mark = "STOP" if record.get("terminal") else "CONT"
            print(
                f"  [{mark}] {record.get('iteration')}: {record.get('action')} — "
                f"{record.get('rationale')}"
            )
        print("derived conditions:", json.dumps(run.derived_conditions, sort_keys=True))
        print(f"evidence store: {store.plan_dir(args.plan)}")
        print(f"reconstruction: python -m runtime.orchestrator --plan {args.plan} "
              f"--reconstruct {run.run_id}")

    return 1 if run.terminal_action in ATTENTION_ACTIONS else 0


if __name__ == "__main__":
    sys.exit(main())
