"""Behavioral tests for stable-prefix resolution (RFC-78 / plan 121).

Covers the resolution contract of RFC-78 sections 2-4: which elements are
eligible for the stable prefix (Stable + Worker scope + demonstrably
consumed/resolvable), the declared-empty `protocol-bootstrap` step, the
Project/KB exclusion, deterministic ordering, and the blocking rule: an
unresolvable element raises and the runtime never invents content (PC-009).

The suite is self-contained (stdlib + the runtime modules) and never depends on
the `protocol/` payload (tests/AGENTS.md): it builds a minimal fake payload in
`tmp_path`.
"""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT))

from runtime.toolcalls.context import ExecutionContext  # noqa: E402
from runtime.toolcalls.segment_resolution import (  # noqa: E402
    KIND_HARNESS_POLICY,
    KIND_PROFILE,
    KIND_PROTOCOL_BOOTSTRAP,
    KIND_ROLE,
    KIND_SKILL,
    KIND_WORKFLOW_MODULE,
    SegmentResolutionError,
    order_stable_segments,
    resolve_stable_segments,
    stable_segment_refs,
)

WORKFLOW = "orchestrators/core/workflow/06-execute.md"
POLICY = "orchestrators/core/harness/policies/H05-execution-completed.md"
WORKER_ROLE = "roles/worker.md"
ROLE = "roles/executor.md"
PROFILE = "roles/profiles/backend_engineer.md"
SKILL = "skills/self-review/SKILL.md"


def make_context(**overrides) -> ExecutionContext:
    """A delegation context naming every resolvable stable element."""
    defaults = dict(
        session_uuid="00000000-0000-0000-0000-000000000000",
        current_state="core:EXECUTING",
        target_phase=(WORKFLOW,),
        role_to_adopt="executor",
        task_summary="Apply the execution plan.",
        skills=(),
        knowledge_entries=(),
        context_budget=1000,
        harness_policy=(POLICY,),
        profile=None,
        input_artifacts=("01-EXECUTION_PLAN.md",),
    )
    defaults.update(overrides)
    return ExecutionContext(**defaults)


def build_payload(root: Path, files: dict[str, str] | None = None) -> Path:
    """Materialize a minimal fake protocol payload under `root`."""
    default_files = {
        WORKFLOW: "# Execute\n\nworkflow body\n",
        POLICY: "# H05\n\npolicy body\n",
        WORKER_ROLE: "# Role: Worker\n\nworker body\n",
        ROLE: "# Role: Executor\n\nexecutor body\n",
        PROFILE: "# Backend Engineer\n\nprofile body\n",
        SKILL: "---\nname: self-review\ndescription: Review own output\n---\n\nskill body\n",
    }
    default_files.update(files or {})
    for relative, content in default_files.items():
        target = root / ".agents" / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(content, encoding="utf-8", newline="")
    return root


@pytest.fixture()
def payload_root(tmp_path: Path) -> Path:
    return build_payload(tmp_path)


def kinds(resolutions) -> list[str]:
    return [resolution.kind for resolution in resolutions]


def test_refs_are_derived_from_payload_fields():
    refs = stable_segment_refs(make_context())
    ids = [(ref.kind, ref.logical_id) for ref in refs]
    assert (KIND_WORKFLOW_MODULE, WORKFLOW) in ids
    assert (KIND_ROLE, "executor") in ids
    assert (KIND_HARNESS_POLICY, POLICY) in ids
    assert (KIND_ROLE, "worker") in ids
    assert (KIND_PROFILE, "backend_engineer") not in ids


def test_refs_include_profile_when_delivered():
    refs = stable_segment_refs(make_context(profile="backend_engineer"))
    assert (KIND_PROFILE, "backend_engineer") in [
        (ref.kind, ref.logical_id) for ref in refs
    ]


def test_refs_include_each_activated_skill_in_order():
    class Skill:
        def __init__(self, name):
            self.name = name

    ctx = make_context(skills=(Skill("self-review"), Skill("tdd-reviewer")))
    ids = [
        ref.logical_id for ref in stable_segment_refs(ctx) if ref.kind == KIND_SKILL
    ]
    assert ids == ["self-review", "tdd-reviewer"]


def test_refs_accept_a_bare_string_phase():
    ctx = make_context(target_phase=WORKFLOW)
    ids = [
        ref.logical_id
        for ref in stable_segment_refs(ctx)
        if ref.kind == KIND_WORKFLOW_MODULE
    ]
    assert ids == [WORKFLOW]


def test_resolution_is_deterministic(payload_root: Path):
    ctx = make_context()
    first = resolve_stable_segments(ctx, payload_root)
    second = resolve_stable_segments(ctx, payload_root)
    assert first == second
    assert [s.content for s in first] == [s.content for s in second]


def test_resolution_returns_payload_bytes_verbatim(payload_root: Path):
    resolved = resolve_stable_segments(make_context(), payload_root)
    by_id = {resolution.logical_id: resolution for resolution in resolved}
    assert by_id["executor"].content == b"# Role: Executor\n\nexecutor body\n"
    assert by_id["worker"].content == b"# Role: Worker\n\nworker body\n"


def test_resolution_records_repo_relative_paths(payload_root: Path):
    resolved = resolve_stable_segments(make_context(), payload_root)
    by_id = {resolution.logical_id: resolution for resolution in resolved}
    assert by_id["executor"].relative_path == f".agents/{ROLE}"
    assert by_id[POLICY].relative_path == f".agents/{POLICY}"


def test_order_puts_stable_kinds_in_contract_order(payload_root: Path):
    class Skill:
        name = "self-review"

    ctx = make_context(profile="backend_engineer", skills=(Skill(),))
    ordered = order_stable_segments(resolve_stable_segments(ctx, payload_root))
    assert kinds(ordered) == [
        KIND_WORKFLOW_MODULE,
        KIND_ROLE,
        KIND_ROLE,
        KIND_PROFILE,
        KIND_HARNESS_POLICY,
        KIND_SKILL,
    ]


def test_order_is_stable_within_a_kind(payload_root: Path):
    second = "orchestrators/core/workflow/05-plan.md"
    build_payload(payload_root, {second: "# Plan\n\nplan body\n"})
    ctx = make_context(target_phase=(WORKFLOW, second))
    ordered = order_stable_segments(resolve_stable_segments(ctx, payload_root))
    workflow_ids = [
        resolution.logical_id
        for resolution in ordered
        if resolution.kind == KIND_WORKFLOW_MODULE
    ]
    assert workflow_ids == [WORKFLOW, second]


def test_unresolvable_workflow_raises_with_the_attempted_path(tmp_path: Path):
    build_payload(tmp_path, {WORKFLOW: "x"})
    (tmp_path / ".agents" / WORKFLOW).unlink()
    with pytest.raises(SegmentResolutionError) as excinfo:
        resolve_stable_segments(make_context(), tmp_path)
    assert "06-execute.md" in str(excinfo.value)
    assert ".agents/orchestrators/core/workflow/06-execute.md" in str(excinfo.value)


def test_unresolvable_role_raises(tmp_path: Path):
    build_payload(tmp_path)
    (tmp_path / ".agents" / ROLE).unlink()
    with pytest.raises(SegmentResolutionError) as excinfo:
        resolve_stable_segments(make_context(), tmp_path)
    assert KIND_ROLE in str(excinfo.value)


def test_unresolvable_policy_raises(tmp_path: Path):
    build_payload(tmp_path)
    (tmp_path / ".agents" / POLICY).unlink()
    with pytest.raises(SegmentResolutionError) as excinfo:
        resolve_stable_segments(make_context(), tmp_path)
    assert KIND_HARNESS_POLICY in str(excinfo.value)


def test_unresolvable_skill_raises(tmp_path: Path):
    build_payload(tmp_path)

    class Skill:
        name = "missing-skill"

    with pytest.raises(SegmentResolutionError) as excinfo:
        resolve_stable_segments(make_context(skills=(Skill(),)), tmp_path)
    assert "missing-skill" in str(excinfo.value)


def test_resolution_never_produces_invented_content(tmp_path: Path):
    build_payload(tmp_path)
    (tmp_path / ".agents" / WORKER_ROLE).unlink()
    with pytest.raises(SegmentResolutionError):
        resolve_stable_segments(make_context(), tmp_path)


def test_unknown_kind_raises(payload_root: Path):
    from runtime.toolcalls import segment_resolution

    with pytest.raises(SegmentResolutionError):
        segment_resolution._relative_path("mystery-kind", "x")


def test_path_escaping_the_payload_is_rejected(payload_root: Path):
    """A delivered path that leaves `.agents/` is rejected, never followed."""
    from runtime.toolcalls import segment_resolution

    with pytest.raises(SegmentResolutionError):
        segment_resolution._relative_path(KIND_WORKFLOW_MODULE, "../../etc/passwd")
    with pytest.raises(SegmentResolutionError):
        segment_resolution._relative_path(KIND_HARNESS_POLICY, "C:/Windows/x.md")


def test_absolute_phase_path_is_rejected(payload_root: Path):
    ctx = make_context(target_phase=("/absolute/path.md",))
    with pytest.raises(SegmentResolutionError):
        resolve_stable_segments(ctx, payload_root)


def test_project_and_kb_segments_are_never_resolved(payload_root: Path):
    """RFC-78 PC-010: the Project/KB segment is outside the MVP stable prefix."""
    resolved = resolve_stable_segments(make_context(), payload_root)
    assert all(resolution.kind != "project" for resolution in resolved)
    assert all("knowledge" not in resolution.relative_path for resolution in resolved)
    assert all(resolution.kind != KIND_PROTOCOL_BOOTSTRAP for resolution in resolved)


def test_protocol_bootstrap_is_not_resolved(payload_root: Path):
    """HD-1b/bootstrap: no Core bootstrap document is Worker-consumed."""
    (payload_root / "AGENTS.md").write_text("# bootstrap\n", encoding="utf-8")
    (payload_root / ".agents" / "INDEX.md").write_text("# index\n", encoding="utf-8")
    resolved = resolve_stable_segments(make_context(), payload_root)
    paths = {resolution.relative_path for resolution in resolved}
    assert ".agents/INDEX.md" not in paths
    assert not any("STATE_MACHINE" in path for path in paths)
    assert not any("orchestrator.md" in path for path in paths)


def test_unresolved_required_step_is_never_serialized_as_an_empty_region():
    """The serialization of the stable region is owned by `canonical`.

    This module resolves segments; it does not decide the bytes of the region.
    The bytes are produced by `canonical.encode_stable_region`, which is the only
    serializer RFC-78's stable prefix is built from, and it refuses to emit a
    region whose required steps were not resolved. A second, more permissive
    serializer here would silently produce a region missing the declared-empty
    structural markers the contract requires — so there is none to call.
    """
    from runtime.toolcalls.canonical import encode_stable_region

    with pytest.raises(SegmentResolutionError):
        encode_stable_region(())


def test_declared_empty_bootstrap_appears_in_the_contract_order():
    """`protocol-bootstrap` is a declared step even though it resolves to nothing."""
    from runtime.toolcalls.canonical import DECLARED_EMPTY_STEPS, ORDERING_CONTRACT_V2

    assert KIND_PROTOCOL_BOOTSTRAP in ORDERING_CONTRACT_V2.field_order
    assert ORDERING_CONTRACT_V2.field_order[0] == KIND_PROTOCOL_BOOTSTRAP
    assert DECLARED_EMPTY_STEPS == (KIND_PROTOCOL_BOOTSTRAP,)
