"""F-C host integration (plan 165): the flow is wired to the real execution path.

The unit suites prove the primitives; this suite proves they are **on the real route**: the host's
delegation path runs ``AgentWorker.execute``, and that method now uses ``fc_flow`` (``FC-3`` memory
context, ``FC-5`` containment frontier) instead of leaving the flow isolated behind tests. Its purpose
is to **detect an accidental disconnection** between the host path and the F-C flow.

It is deliberately a wiring detector, not an end-to-end actor run: the end-to-end run needs the
adopter's external actor (``FC-1`` / ``FC-6``, external demonstration pending).
"""

from __future__ import annotations

import inspect
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from runtime.orchestrator import agent_worker, fc_flow, host  # noqa: E402
from runtime.orchestrator.agent_worker import AgentWorker  # noqa: E402

#: The primitives the real route must keep calling (a gap in any of them is a disconnection).
REQUIRED_IN_EXECUTE = (
    "contain_actor_result",
    "build_memory_context",
    "with_memory_context",
)


def wiring_gaps(*, execute_source: str, host_source: str) -> list[str]:
    """Reasons the F-C flow is NOT wired to the real execution path."""
    gaps = [p for p in REQUIRED_IN_EXECUTE if p not in execute_source]
    drives_a_worker = "WorkerAdapter" in host_source and any(
        shape in host_source for shape in (".execute(", "self.worker(", "worker.run(", "worker.execute")
    )
    if not drives_a_worker:
        gaps.append("host does not drive a WorkerAdapter: the flow has no route")
    if "fc_containment" not in execute_source:
        gaps.append("the containment verdict is not recorded with the result")
    if "memory_store" not in inspect.getsource(AgentWorker):
        gaps.append("the worker cannot receive a memory store")
    if fc_flow.contains_memory_parameter(fc_flow.contain_actor_result):
        gaps.append("the containment frontier accepts a memory parameter")
    return gaps


def test_the_flow_is_wired_to_the_real_execution_path() -> None:
    gaps = wiring_gaps(
        execute_source=inspect.getsource(AgentWorker.execute),
        host_source=inspect.getsource(host),
    )
    assert gaps == [], gaps


def test_memory_is_absent_by_default_and_therefore_a_no_op() -> None:
    worker = AgentWorker()
    assert worker.memory_store is None


def test_detector_catches_a_disconnection() -> None:
    """Counterproof: an unwired route is reported, so the detector is not a tautology."""
    gaps = wiring_gaps(
        execute_source="def execute(self): return None",
        host_source="def nothing(): return None",
    )
    assert any("contain_actor_result" in gap for gap in gaps), gaps
    assert any("host does not drive" in gap for gap in gaps), gaps


def test_the_frontier_still_cannot_be_reached_by_memory() -> None:
    """``ID-4`` holds on the integrated route, not only in the unit suite."""
    assert fc_flow.contains_memory_parameter(fc_flow.contain_actor_result) is False
    assert "memory" not in _parameters(fc_flow.contain_actor_result)


def _parameters(function: object) -> str:
    return " ".join(inspect.signature(function).parameters)


def test_the_actor_remains_external_on_the_route() -> None:
    """``ID-1``: the integration adds no provider/model/SDK/CLI and no model invocation."""
    source = (inspect.getsource(agent_worker) + inspect.getsource(fc_flow)).lower()
    for forbidden in ("openai", "anthropic", "import requests", "httpx", "api_key", "subprocess"):
        assert forbidden not in source, forbidden
