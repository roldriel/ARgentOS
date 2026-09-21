"""Dogfood: Scope/Authority enforcement over the real repository (plan 138).

Two halves, deliberately, because each protects something the other cannot:

- **Anchored, read-only assertions over the real tree.** They check that the
  enforcement point exists where the plan says it does, that the frontier now
  declares the rules the incident proved necessary, and — the part that matters
  most — that ``ROADMAP.md`` and the closed plan that recorded the incident are
  **unchanged**. A synthetic repository cannot express that: it is a statement
  about this repository's own state.
- **A functional end-to-end dogfood.** The same F-3 shape, driven through the
  whole ``observe → derive → authorize → STOP`` loop, proving the refusal precedes
  any invocation. It reuses the isolated fixture of
  ``tests/test_sae_scope_enforcement.py`` instead of duplicating it.

**Declared limit.** This repository ships no provider, no model and no network
(plan 123, human decision H-1), so a real language model cannot be invoked. The
substitution is deliberate and narrow: the *model* is replaced by an injected
``AgentInvoker`` that really performs the writes, so the effect the enforcement
prevents is a material filesystem write and not a simulated one. What is not
demonstrated — and is not claimed — is enforcement against a model that ignores
its instructions in a way this repository cannot run.

Nothing here mutates repository state.
"""

from __future__ import annotations

import hashlib
import re
import subprocess
from pathlib import Path

from runtime.orchestrator.agent_worker import AgentWorker
from runtime.orchestrator.host import ExecutionHost
from runtime.orchestrator.observation import observe
from runtime.orchestrator.store import OrchestratorStore

from test_sae_scope_enforcement import (
    EXCLUDED,
    INCLUDED,
    PLAN_NUMBER,
    PLAN_NAME,
    WritingInvoker,
    build_repo,
    make_host,
    pinned_of,
)

REPO_ROOT = Path(__file__).resolve().parents[1]
HOST = "runtime/orchestrator/host.py"
AUTONOMY = "runtime/orchestrator/autonomy.py"
SAE_POLICY = ".agents/policies/supervised-autonomous-execution.md"
CLOSURE_POLICY = ".agents/policies/validation-closure.md"
ORCHESTRATION_POLICY = ".agents/policies/autonomous-orchestration.md"
CLOSED_PLAN = "docs/plans/136-d01-mechanical-checker.md"
ROADMAP = "ROADMAP.md"
PLAN_138 = "docs/plans/138-sae-scope-authority-hardening.md"

# The append-only region the Change Lifecycle appends to a closed plan when a
# lifecycle record's state metadata transitions (LC-1).
CLOSED_PLAN_METADATA_HEADING = "## Metadatos de estado (evolucionables)"

# sha256 of the closed plan's **normative** content: the plan text up to the
# append-only metadata section, with the *values* of the evolvable lifecycle
# metadata canonicalized — a finding's `estado` and a pending decision's
# `resolución` (LC-1). Every other character is pinned: editing an observation,
# an evidence string, an immutable element or any normative section changes the
# digest and fails the test. Recompute it only when a legitimate lifecycle
# transition changes the canonical content.
CLOSED_PLAN_NORMATIVE_SHA256 = (
    "5ef36941f6445d82fb5b4501ca88259a4c8e641677bedc7c37e83a7aa346a40f"
)


def _text(rel: str) -> str:
    return (REPO_ROOT / rel).read_text(encoding="utf-8")


def _normative_digest(text: str) -> str:
    """Digest of a closed plan's content with its evolvable metadata normalized."""
    # The heading, located as a line: other records may *reference* its title.
    heading = re.search(
        r"^" + re.escape(CLOSED_PLAN_METADATA_HEADING) + r"\s*$",
        text,
        re.MULTILINE,
    )
    content = text[: heading.start()] if heading else text
    content = re.sub(r"estado: [^;]+;", "estado: <evolvable>;", content)
    content = re.sub(
        r"resolución:.*?(?=; evidencia:)",
        "resolución: <evolvable>",
        content,
        flags=re.DOTALL,
    )
    return hashlib.sha256(content.encode("utf-8")).hexdigest()


def _git(*args: str) -> str:
    proc = subprocess.run(
        ["git", "-C", str(REPO_ROOT), *args],
        check=False,
        capture_output=True,
        text=True,
    )
    return proc.stdout


# --------------------------------------------------------------------------- #
# 1. The enforcement point exists, in the component the plan named
# --------------------------------------------------------------------------- #


def test_the_enforcement_lives_in_the_host_before_the_delegation():
    """The refusal precedes the effect, and the decision did not move elsewhere."""
    host = _text(HOST)
    # The gate runs before the delegation is built and before any worker runs.
    assert "def _apply_autonomy_gate" in host
    assert "def _execute_delegation" in host
    assert "_apply_autonomy_gate(observation, action, boundary)" in host
    # It verifies the complete target set, not one path.
    assert "def _autonomy_targets" in host
    assert "write_targets=targets" in host
    assert "targets_unresolved=unresolved" in host
    # It compares the authorization checkpoint recorded in the journal.
    assert "def _pinned_autonomy_projection" in host
    assert "authorization_drift" in host
    # The authorization decision did not move into the derivation or the worker.
    assert "autonomy" not in _text("runtime/orchestrator/derivation.py")
    assert "_autonomy_targets" not in _text("runtime/orchestrator/worker.py")
    assert "_autonomy_targets" not in _text("runtime/orchestrator/agent_worker.py")


def test_the_detection_half_was_preserved_as_defence_in_depth():
    """Prevention did not replace detection: both are still present."""
    host = _text(HOST)
    assert "def _scope_violations" in host
    assert "forbidden_scope_action" in host
    assert "defence in depth" in host
    # The frontier module states the same boundary, so the policy and the code
    # cannot drift apart silently.
    assert "enforcement point" in host or "defence in depth" in host
    assert "declared limits" in _text(SAE_POLICY).casefold()


def test_no_new_registry_state_machine_or_authority_class_was_created():
    """The hardening reused the existing mechanism, as the plan required."""
    for forbidden in (
        ".project/orchestrator/authorization-registry.json",
        "runtime/orchestrator/authorization_store.py",
        "runtime/orchestrator/scope_store.py",
        "docs/authorization-registry.md",
    ):
        assert not (REPO_ROOT / forbidden).exists(), forbidden
    # The stop vocabulary was reused, not extended: no new stop was added for
    # this Change, which is what the plan required.
    contracts = _text("runtime/orchestrator/contracts.py")
    assert "STOP_AUTHORIZATION_DRIFT" not in contracts
    assert "STOP_SCOPE_VIOLATION" in contracts


# --------------------------------------------------------------------------- #
# 2. The frontier now declares what the incident proved necessary
# --------------------------------------------------------------------------- #


def test_the_sae_policy_declares_scope_precedence_checkpoint_and_no_retroactivity():
    policy = _text(SAE_POLICY)
    assert "### 1.1 Scope precedes every obligation (plan 138)" in policy
    assert "### 1.2 The authorization checkpoint (plan 138)" in policy
    assert "### 1.3 A write is authorized as a whole (plan 138)" in policy
    assert "obligation" in policy and "never an authorization to write" in policy
    assert "No retroactivity." in policy
    assert "No exception exists for any artifact" in policy


def test_the_determinations_declare_that_required_is_not_a_write_authorization():
    closure = _text(CLOSURE_POLICY)
    assert closure.count("never a write authorization") >= 2, (
        "both §5.1 and §5.2 must state it"
    )
    assert "<PLAN-136>:PC-4" in closure
    orchestration = _text(ORCHESTRATION_POLICY)
    assert "Prevention and detection are two different guarantees" in orchestration


# --------------------------------------------------------------------------- #
# 3. The closed plan and the roadmap are untouched — the frontier, verified
# --------------------------------------------------------------------------- #


def test_the_closed_plan_of_the_incident_keeps_its_history():
    """`Closed is terminal` for the **content**: the incident was used, not rewritten.

    The closed plan received two lifecycle transitions: Plan 139 closed
    `<PLAN-136>:F-3` (`open` -> `resolved`) and Plan 140 closed
    `<PLAN-136>:PC-5` (`pendiente` -> `superseded`). Both are metadata
    **evolvable** by the lineage convention (LC-1) and human decisions (CL-8).
    What must never change is the historical content: the observation, the
    evidence, the observed Git state, the provenance, the human decision of
    `<PLAN-136>:PC-4` and the recorded out-of-scope write.

    The invariant is deliberately state-independent: it asserts the content, it
    pins the normative text by digest with the evolvable metadata canonicalized,
    and it asserts that the append-only metadata section is the last region of
    the artifact. It does not depend on `git diff` against `HEAD` — that
    formulation only held while the transition was uncommitted and left the
    suite red on the committed state (`<PLAN-140>:F-1`).
    """
    text = _text(CLOSED_PLAN)
    # The finding, the human decisions and the incident are still there, verbatim.
    assert "<PLAN-136>:F-3" in text
    assert "estado: `resolved`" in text
    assert "<PLAN-136>:PC-4" in text
    assert "Roadmap Impact: REQUIRED" in text
    assert "la modificación **excedió el Scope**" in text
    # The immutable elements of the finding survive every transition.
    assert "`f0d9c0334c6256a1b4187d30a1cf37fe0ab0f816`, working tree limpio" in text
    assert "provenance original: lectura del propio Plan" in text
    # The correction that records the out-of-scope write keeps its finding
    # unauthorized: the transitions legitimize nothing retroactively.
    assert "**Autorización: NO establecida.**" in text
    # Both lifecycle transitions are recorded in the artifact that owns them.
    assert "resolución: **superseded**" in text
    # The metadata section is the designated append-only region, and it is last:
    # nothing may be appended after it outside that contract.
    metadata_line = re.search(
        r"^" + re.escape(CLOSED_PLAN_METADATA_HEADING) + r"\s*$",
        text,
        re.MULTILINE,
    )
    assert metadata_line is not None, "the state-metadata section is missing"
    tail = text[metadata_line.start():]
    assert not any(
        line.startswith("## ") and CLOSED_PLAN_METADATA_HEADING not in line
        for line in tail.splitlines()
    ), "content was appended to the closed plan after the metadata section"
    # Everything outside the evolvable lifecycle metadata is pinned by digest.
    assert _normative_digest(text) == CLOSED_PLAN_NORMATIVE_SHA256, (
        "the closed plan changed outside its evolvable lifecycle metadata: an "
        "observation, an evidence string, an immutable element or a normative "
        "section was edited"
    )


def test_the_governance_boundary_decisions_are_closed_as_decided():
    """Plan 139 closed the three decisions: F-3 resolved, PC-1 resolved, PC-2 deferred.

    The frontier this Change protects includes the governance boundary itself: an
    Impact classification is never an authorization, a scope expansion has no
    autonomous mechanism, and the incident's finding reaches a terminal state that
    its own artifact (not a third-party summary) records.
    """
    plan_136 = _text(CLOSED_PLAN)
    assert "estado: `resolved`" in plan_136
    assert "`resolved`; la transición no legitima" in plan_136 or "no legitima" in plan_136

    plan_138 = _text(PLAN_138)
    assert "resolución:\n  **resuelta**" in plan_138
    assert "Impact classification != authorization" in plan_138
    assert "resolución:\n  **deferred**" in plan_138
    assert "<PLAN-138>:PC-2" in plan_138

    # The rule and the boundary live in their canonical policies, not in a parallel one.
    closure = _text(CLOSURE_POLICY)
    assert "Authorization is **never inferred**" in closure
    assert "documentary dependency" in closure
    assert "closure requirement" in closure
    sae = _text(SAE_POLICY)
    assert "### 1.4 There is no autonomous Scope Expansion" in sae
    assert "STOP / REQUIRES_HUMAN" in sae
    # No scope-expansion mechanism was introduced.
    for forbidden in (
        "runtime/orchestrator/scope_expansion.py",
        ".project/orchestrator/scope-expansion.json",
    ):
        assert not (REPO_ROOT / forbidden).exists(), forbidden


def test_the_roadmap_is_not_modified_by_this_change():
    """The obligation was recorded `DEFERRED`; it was not turned into a write.

    This is the living demonstration of the rule: the Change that formalizes
    "`REQUIRED` is not a write authorization" is itself closed with a deferred
    roadmap obligation and a clean `ROADMAP.md`.

    Asserted over the plan's **own commits**, not over the working tree: the claim
    is historical — what this Change did — and a working-tree diff against `HEAD`
    makes the suite red for any later Change that legitimately reconciles the
    operational map (the same class of Git-state dependency as
    ``<PLAN-140>:F-1``).
    """
    shas = _git("log", "--format=%H", "--grep=(plan 138)").split()
    assert shas, "the plan-138 commits are not in history"
    moved: set[str] = set()
    for sha in shas:
        moved.update(_git("log", "-1", "--name-only", "--format=", sha).split())
    assert ROADMAP not in moved, f"ROADMAP.md was modified by plan 138: {sorted(moved)}"
    assert (REPO_ROOT / ROADMAP).is_file()


def test_the_plan_records_the_deferral_with_its_governing_pending_decision():
    plan = _text(PLAN_138)
    assert "Roadmap impact:** `DEFERRED`" in plan
    assert "<PLAN-138>:PC-1" in plan
    assert "<PLAN-138>:PC-2" in plan


def test_no_protected_path_moved():
    """The plan's own commits left the payload, RFCs, ADRs and the authority policy
    untouched.

    Asserted over **immutable history**, not over the working tree. The claim is
    about what this plan's change did, so it is verified on the plan's own commits.
    Comparing the working tree against ``HEAD`` (the previous form, the same class
    as ``<PLAN-140>:F-1``) made the suite red for any later, legitimate governance
    change to the same paths and green again only once the commit existed — a
    dependency on the Git state, not an invariant of the repository.
    """
    shas = _git("log", "--format=%H", "--grep=(plan 138)").split()
    assert shas, "the plan-138 commits are not in history"
    moved: set[str] = set()
    for sha in shas:
        moved.update(_git("log", "-1", "--name-only", "--format=", sha).split())
    protected = sorted(
        path
        for path in moved
        if path.startswith(("protocol/", "docs/rfc/", "docs/adr/"))
        or path == ".agents/policies/authority.md"
    )
    assert protected == [], f"a protected path was modified: {protected}"


# --------------------------------------------------------------------------- #
# 4. Functional dogfood: the whole loop refuses before it acts
# --------------------------------------------------------------------------- #


def test_functional_dogfood_the_loop_refuses_the_f3_shape_before_acting():
    """`observe → derive → authorize → STOP`, with nothing written and nothing run.

    The F-3 shape, driven through the real `ExecutionHost.run()`: the plan
    excludes an artifact, a closure obligation names it, and the delegated work
    would write it. The run stops at the frontier, the excluded artifact is
    byte-identical, no delegation is persisted and the invoker is never reached.
    """
    root = build_repo(
        "dogfood-f3-loop",
        declared_scope=f"`{INCLUDED}`, `{EXCLUDED}`",
    )
    excluded = root / EXCLUDED
    before = excluded.read_bytes()

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

    assert run.terminal_action == "STOP_SCOPE_VIOLATION"
    assert record["authority"]["verdict"] == "REQUIRES_HUMAN"
    assert record["delegation_id"] is None
    assert store.list_worker_results(PLAN_NUMBER) == []
    assert excluded.read_bytes() == before
    assert invoker.requests == []
    assert record["autonomy"]["authorization_drift"] is False
    assert "nothing was written" in record["rationale"]


def test_functional_dogfood_the_checkpoint_survives_a_rewrite_between_runs():
    """A rewrite after the first authorization is refused, and it acts on nothing.

    Between the two runs the plan's `Task` is rewritten to claim the excluded
    artifact is authorized — the retrospective move the incident produced. The
    second run stops on the divergence and never reaches its invoker.
    """
    root = build_repo("dogfood-drift")
    plan_path = root / "docs" / "plans" / PLAN_NAME
    original = plan_path.read_text(encoding="utf-8")

    store = OrchestratorStore(root)
    make_host(root, invoker=WritingInvoker(include_excluded=False)).run(max_iterations=2)
    pinned = pinned_of(ExecutionHost(root, PLAN_NUMBER, store=store))
    assert pinned

    plan_path.write_text(
        original.replace(
            "- **Task:** implement the authorized work",
            "- **Task:** implement the authorized work and also write the excluded "
            "artifact",
        ),
        encoding="utf-8",
    )

    invoker = WritingInvoker()
    second = make_host(root, invoker=invoker).run(max_iterations=2)
    last = second.records[-1]

    assert last["action"] == "STOP_SCOPE_VIOLATION"
    assert last["authorization_drift"] is True
    assert last["autonomy_checkpoint"] == pinned
    assert last["delegation_id"] is None
    assert invoker.requests == []
    assert "checkpoint diverged" in last["rationale"]


def test_the_real_plan_envelope_passes_the_new_enforcement():
    """The Change's own declaration must satisfy the frontier it introduces.

    A hardening that refused its own Change would be useless; a hardening the
    Change's own declaration could bypass would be worse. Both are excluded here,
    over the real artifact and read-only.
    """
    from runtime.orchestrator.autonomy import verify_write_targets
    from runtime.orchestrator.host import _autonomy_envelope, _autonomy_targets

    observation = observe(REPO_ROOT, 138, OrchestratorStore(REPO_ROOT))
    assert observation.agent_task.declared is True
    declaration, bounded = _autonomy_envelope(observation, 138)
    assert bounded.declared is True
    # Every path the plan declares for its agent task is a path the plan itself
    # declares: no circular authorization.
    assert sorted(declaration.scope_paths) == sorted(bounded.scope_paths)
    targets, unresolved = _autonomy_targets("RUN_IMPLEMENTATION_TASK", observation)
    assert unresolved is False
    assert verify_write_targets(bounded, targets).in_scope is True
    # And the governance records the host must write stay authorized.
    record_targets, record_unresolved = _autonomy_targets(
        "RECORD_VALIDATION_ANCHOR", observation
    )
    assert record_unresolved is False
    assert verify_write_targets(bounded, record_targets).in_scope is True
