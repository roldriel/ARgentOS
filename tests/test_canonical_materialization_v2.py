"""Behavioral tests for the ordering-contract-v2 canonical materialization.

Implements the testable properties of RFC-78 (plan 121): the stable prefix, the
ordered contract, the dynamic suffix, the identity separation, the isolation
guarantees, the honest `MaterializationIdentity`, and the rejection behaviour of
the ordering contracts. `tests/test_canonical_materialization.py` keeps covering
the v1 contract and the RFC-72 invariants.

The suite is self-contained (stdlib + the runtime modules) and never depends on
the `protocol/` payload (tests/AGENTS.md): it builds a minimal fake payload in
`tmp_path`.
"""

from __future__ import annotations

import dataclasses
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT))

from runtime.toolcalls.canonical import (  # noqa: E402
    CONTENT_CONTRACT_VERSION,
    DECLARED_EMPTY_STEPS,
    ORDERING_CONTRACT_V1,
    ORDERING_CONTRACT_V2,
    REQUIRED_STABLE_STEPS,
    canonical_materialize,
    ordering_contract,
    stable_prefix,
    stable_region_structure,
)
from runtime.toolcalls.context import ExecutionContext  # noqa: E402
from runtime.toolcalls.identity import (  # noqa: E402
    MaterializationVersion,
    materialization_identity,
)
from runtime.toolcalls.segment_resolution import (  # noqa: E402
    KIND_HARNESS_POLICY,
    KIND_PROFILE,
    KIND_PROTOCOL_BOOTSTRAP,
    KIND_ROLE,
    KIND_SKILL,
    KIND_WORKFLOW_MODULE,
    SegmentResolutionError,
)

WORKFLOW = "orchestrators/core/workflow/06-execute.md"
POLICY = "orchestrators/core/harness/policies/H05-execution-completed.md"
PROFILE = "roles/profiles/backend_engineer.md"
SKILL = "skills/self-review/SKILL.md"


def make_context(**overrides) -> ExecutionContext:
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
    default_files = {
        WORKFLOW: "# Execute\n\nworkflow body\n",
        POLICY: "# H05\n\npolicy body\n",
        "roles/worker.md": "# Role: Worker\n\nworker body\n",
        "roles/executor.md": "# Role: Executor\n\nexecutor body\n",
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


def mi_v2(**overrides) -> str:
    version = MaterializationVersion(
        variant=overrides.pop("variant", "prompt"),
        ordering_contract_version="2",
        serialization_version="1",
        content_contract_version=CONTENT_CONTRACT_VERSION,
    )
    return materialization_identity(materialization_version=version, **overrides)


def mi_v1(variant: str = "prompt") -> str:
    return materialization_identity(
        materialization_version=MaterializationVersion(
            variant=variant,
            ordering_contract_version="1",
            serialization_version="1",
        )
    )


def materialize(context: ExecutionContext, root: Path, variant: str = "prompt",
                mi: str | None = None):
    return canonical_materialize(
        context, mi or mi_v2(variant=variant), variant, protocol_root=str(root)
    )


# --- PC-001 determinism ------------------------------------------------------


def test_pc001_materialization_is_deterministic(payload_root: Path):
    first = materialize(make_context(), payload_root)
    second = materialize(make_context(), payload_root)
    assert first.payload == second.payload
    assert first.stable_prefix_bytes == second.stable_prefix_bytes
    assert first.dynamic_suffix == second.dynamic_suffix


def test_pc001_stable_region_is_byte_identical_across_calls(payload_root: Path):
    first = materialize(make_context(), payload_root)
    second = materialize(make_context(), payload_root)
    assert first.stable_prefix_bytes == second.stable_prefix_bytes
    assert first.payload == first.stable_prefix_bytes + first.dynamic_suffix


# --- PC-002 / PC-003 prefix and suffix ---------------------------------------


def test_pc002_declared_empty_step_precedes_every_content_step(payload_root: Path):
    materialization = materialize(make_context(), payload_root)
    order = ORDERING_CONTRACT_V2.field_order
    assert order[0] == KIND_PROTOCOL_BOOTSTRAP
    assert KIND_PROTOCOL_BOOTSTRAP in DECLARED_EMPTY_STEPS
    assert b"content: declared-empty" in materialization.stable_prefix_bytes


def test_pc002_stable_region_contains_every_resolved_segment(payload_root: Path):
    materialization = materialize(make_context(), payload_root)
    for segment in materialization.stable_segments:
        assert segment.content in materialization.stable_prefix_bytes
        assert segment.logical_id.encode("utf-8") in materialization.stable_prefix_bytes


def test_pc003_stable_region_is_invariant_to_session(payload_root: Path):
    a = materialize(make_context(session_uuid="11111111-1111-1111-1111-111111111111"), payload_root)
    b = materialize(make_context(session_uuid="22222222-2222-2222-2222-222222222222"), payload_root)
    assert a.stable_prefix_bytes == b.stable_prefix_bytes


def test_pc003_stable_region_is_invariant_to_task_and_artifacts(payload_root: Path):
    base = materialize(make_context(), payload_root)
    other_task = materialize(make_context(task_summary="Something else."), payload_root)
    other_artifacts = materialize(
        make_context(input_artifacts=("01-EXECUTION_PLAN.md", "02-NOTES.md")), payload_root
    )
    assert base.stable_prefix_bytes == other_task.stable_prefix_bytes
    assert base.stable_prefix_bytes == other_artifacts.stable_prefix_bytes


def test_pc003_stable_region_is_invariant_to_execution_metadata(payload_root: Path):
    base = materialize(make_context(), payload_root)
    metadata = materialize(
        make_context(communication_style="full", technical_approach="tdd"), payload_root
    )
    assert base.stable_prefix_bytes == metadata.stable_prefix_bytes


def test_pc003_dynamic_suffix_carries_the_parameters(payload_root: Path):
    materialization = materialize(
        make_context(session_uuid="abc", task_summary="Unique task"), payload_root
    )
    assert b"session_uuid: abc" in materialization.dynamic_suffix
    assert b"Unique task" in materialization.dynamic_suffix
    assert b"Unique task" not in materialization.stable_prefix_bytes


def test_pc003_stable_prefix_is_a_byte_prefix_of_the_payload(payload_root: Path):
    materialization = materialize(make_context(), payload_root)
    assert materialization.payload.startswith(materialization.stable_prefix_bytes)


# --- PC-004 completeness -----------------------------------------------------


def test_pc004_artifact_references_change_the_identity(payload_root: Path):
    a = materialize(make_context(input_artifacts=("01.md",)), payload_root)
    b = materialize(make_context(input_artifacts=("01.md", "02.md")), payload_root)
    assert a.semantic_context_identity != b.semantic_context_identity


def test_pc004_harness_policy_and_profile_reach_the_identity(payload_root: Path):
    base = materialize(make_context(), payload_root)
    profile = materialize(make_context(profile="backend_engineer"), payload_root)
    assert base.semantic_context_identity != profile.semantic_context_identity


# --- PC-005 identity separation ---------------------------------------------


def test_pc005_ordering_change_changes_mi_only(payload_root: Path):
    context = make_context()
    v1 = canonical_materialize(context, mi_v1(), "prompt", protocol_root=str(payload_root))
    v2 = materialize(context, payload_root)
    assert v1.materialization_identity != v2.materialization_identity
    assert v1.semantic_context_identity == v2.semantic_context_identity


def test_pc005_dynamic_change_keeps_mi(payload_root: Path):
    a = materialize(make_context(task_summary="One"), payload_root)
    b = materialize(make_context(task_summary="Two"), payload_root)
    assert a.materialization_identity == b.materialization_identity
    assert a.semantic_context_identity != b.semantic_context_identity


# --- PC-006 isolation --------------------------------------------------------


def test_pc006_session_uuid_participates_in_the_identity(payload_root: Path):
    a = materialize(make_context(session_uuid="a"), payload_root)
    b = materialize(make_context(session_uuid="b"), payload_root)
    assert a.semantic_context_identity != b.semantic_context_identity
    assert b"session_uuid: b" in b.dynamic_suffix


def test_pc006_cross_project_compositions_stay_distinct(payload_root: Path):
    context = make_context()
    project_a = canonical_materialize(
        context, mi_v2(), "prompt", protocol_root=str(payload_root),
        project_identity="project-a",
    )
    project_b = canonical_materialize(
        context, mi_v2(), "prompt", protocol_root=str(payload_root),
        project_identity="project-b",
    )
    assert project_a.semantic_context_identity != project_b.semantic_context_identity


# --- PC-007 provider boundary ------------------------------------------------


def test_pc007_no_provider_semantics_in_the_representation(payload_root: Path):
    materialization = materialize(make_context(), payload_root)
    text = materialization.payload.decode("utf-8").lower()
    for token in ("cache_control", "anthropic", "openai", "bedrock", "vertex", "cache_key"):
        assert token not in text


# --- PC-009 resolution failure ----------------------------------------------


def test_pc009_unresolved_required_step_raises(tmp_path: Path):
    build_payload(tmp_path)
    (tmp_path / ".agents" / WORKFLOW).unlink()
    with pytest.raises(SegmentResolutionError):
        materialize(make_context(), tmp_path)


def test_pc009_missing_role_raises(tmp_path: Path):
    build_payload(tmp_path)
    (tmp_path / ".agents" / "roles" / "executor.md").unlink()
    with pytest.raises(SegmentResolutionError):
        materialize(make_context(), tmp_path)


def test_pc009_required_steps_are_declared():
    assert KIND_WORKFLOW_MODULE in REQUIRED_STABLE_STEPS
    assert KIND_ROLE in REQUIRED_STABLE_STEPS
    assert KIND_HARNESS_POLICY in REQUIRED_STABLE_STEPS
    # Optional steps are not required: their absence is legitimate.
    assert KIND_PROFILE not in REQUIRED_STABLE_STEPS
    assert KIND_SKILL not in REQUIRED_STABLE_STEPS


def test_pc009_optional_profile_absence_is_not_a_failure(payload_root: Path):
    materialization = materialize(make_context(profile=None), payload_root)
    assert materialization.stable_prefix_bytes
    assert KIND_PROFILE not in {s.kind for s in materialization.stable_segments}


def test_pc009_no_invented_content_on_failure(tmp_path: Path):
    build_payload(tmp_path)
    (tmp_path / ".agents" / WORKFLOW).unlink()
    with pytest.raises(SegmentResolutionError) as excinfo:
        materialize(make_context(), tmp_path)
    assert "cannot read" in str(excinfo.value)


# --- PC-010 Project/KB exclusion --------------------------------------------


def test_pc010_project_segment_is_never_materialized(payload_root: Path):
    build_payload(payload_root, {
        "knowledge/discovery/stack.md": "# Stack\n\nkb body\n",
    })
    materialization = materialize(
        make_context(knowledge_entries=("kb-001", "kb-002")), payload_root
    )
    assert b"kb body" not in materialization.payload
    assert KIND_PROTOCOL_BOOTSTRAP not in {s.kind for s in materialization.stable_segments}
    assert "project" not in {s.kind for s in materialization.stable_segments}


def test_pc010_knowledge_entries_stay_in_the_dynamic_suffix(payload_root: Path):
    materialization = materialize(make_context(knowledge_entries=("kb-001",)), payload_root)
    assert b"kb-001" in materialization.dynamic_suffix
    assert b"kb-001" not in materialization.stable_prefix_bytes


def test_pc010_bootstrap_documents_are_not_materialized(payload_root: Path):
    (payload_root / "AGENTS.md").write_text("# bootstrap\n", encoding="utf-8")
    (payload_root / ".agents" / "INDEX.md").write_text("# index\n", encoding="utf-8")
    (payload_root / ".agents" / "orchestrators").mkdir(parents=True, exist_ok=True)
    materialization = materialize(make_context(), payload_root)
    assert b"# bootstrap" not in materialization.stable_prefix_bytes
    assert b"# index" not in materialization.stable_prefix_bytes


# --- ordering contract v2 ----------------------------------------------------


def test_ordering_contract_v2_field_order():
    assert ORDERING_CONTRACT_V2.version == "2"
    assert ORDERING_CONTRACT_V2.field_order == (
        KIND_PROTOCOL_BOOTSTRAP,
        KIND_WORKFLOW_MODULE,
        KIND_ROLE,
        KIND_PROFILE,
        KIND_HARNESS_POLICY,
        KIND_SKILL,
        "input-artifact-refs",
        "task-summary",
        "execution-metadata",
    )
    assert ORDERING_CONTRACT_V1.version == "1"


def test_stable_region_structure_is_the_stable_prefix_of_the_contract():
    assert stable_region_structure() == (
        KIND_PROTOCOL_BOOTSTRAP,
        KIND_WORKFLOW_MODULE,
        KIND_ROLE,
        KIND_PROFILE,
        KIND_HARNESS_POLICY,
        KIND_SKILL,
    )


def test_ordering_contract_lookup_rejects_unimplemented():
    assert ordering_contract("1").version == "1"
    assert ordering_contract("2").version == "2"
    with pytest.raises(ValueError):
        ordering_contract("3")


def test_v1_identity_is_rejected_when_it_declares_a_content_contract(payload_root: Path):
    bad = materialization_identity(
        materialization_version=MaterializationVersion(
            variant="prompt",
            ordering_contract_version="1",
            serialization_version="1",
            content_contract_version="1",
        )
    )
    with pytest.raises(ValueError):
        canonical_materialize(
            make_context(), bad, "prompt", protocol_root=str(payload_root)
        )


def test_v2_identity_is_rejected_without_a_content_contract(payload_root: Path):
    bad = materialization_identity(
        materialization_version=MaterializationVersion(
            variant="prompt",
            ordering_contract_version="2",
            serialization_version="1",
        )
    )
    with pytest.raises(ValueError) as excinfo:
        canonical_materialize(
            make_context(), bad, "prompt", protocol_root=str(payload_root)
        )
    assert "content_contract_version" in str(excinfo.value)


def test_v2_identity_is_rejected_with_an_unknown_content_contract(payload_root: Path):
    bad = materialization_identity(
        materialization_version=MaterializationVersion(
            variant="prompt",
            ordering_contract_version="2",
            serialization_version="1",
            content_contract_version="99",
        )
    )
    with pytest.raises(ValueError):
        canonical_materialize(
            make_context(), bad, "prompt", protocol_root=str(payload_root)
        )


def test_v2_requires_a_protocol_root():
    with pytest.raises(ValueError) as excinfo:
        canonical_materialize(make_context(), mi_v2(), "prompt")
    assert "protocol payload root" in str(excinfo.value)


def test_unimplemented_ordering_contract_is_rejected(payload_root: Path):
    bad = materialization_identity(
        materialization_version=MaterializationVersion(
            variant="prompt",
            ordering_contract_version="3",
            serialization_version="1",
            content_contract_version=CONTENT_CONTRACT_VERSION,
        )
    )
    with pytest.raises(ValueError):
        canonical_materialize(
            make_context(), bad, "prompt", protocol_root=str(payload_root)
        )


def test_variant_must_match_the_identity(payload_root: Path):
    with pytest.raises(ValueError):
        canonical_materialize(
            make_context(), mi_v2(variant="toolcalls"), "prompt",
            protocol_root=str(payload_root),
        )


def test_unsupported_variant_is_rejected(payload_root: Path):
    with pytest.raises(ValueError):
        canonical_materialize(
            make_context(), mi_v2(), "unknown-variant", protocol_root=str(payload_root)
        )


# --- both variants -----------------------------------------------------------


def test_toolcalls_variant_materializes_the_same_stable_region(payload_root: Path):
    """The reusable content is variant-independent; only the banner names it."""
    prompt = canonical_materialize(
        make_context(), mi_v2(variant="prompt"), "prompt",
        protocol_root=str(payload_root),
    )
    toolcalls = canonical_materialize(
        make_context(), mi_v2(variant="toolcalls"), "toolcalls",
        protocol_root=str(payload_root),
    )
    assert prompt.stable_region == toolcalls.stable_region
    assert prompt.materialization_identity != toolcalls.materialization_identity
    # The banner carries the identity, so the variant is visible in it.
    assert prompt.stable_prefix_bytes != toolcalls.stable_prefix_bytes


def test_stable_region_is_the_contract_content_independent_of_the_banner(payload_root: Path):
    materialization = materialize(make_context(), payload_root)
    assert materialization.stable_region
    assert materialization.stable_prefix_bytes.endswith(materialization.stable_region)
    assert b"materialization_identity:" not in materialization.stable_region


# --- stable_prefix (RFC-72 section 5) ---------------------------------------


def test_stable_prefix_is_the_full_payload_for_identical_invocations(payload_root: Path):
    a = materialize(make_context(), payload_root)
    b = materialize(make_context(), payload_root)
    assert stable_prefix(a, b) == a.payload


def test_stable_prefix_is_none_for_different_semantic_contexts(payload_root: Path):
    a = materialize(make_context(task_summary="One"), payload_root)
    b = materialize(make_context(task_summary="Two"), payload_root)
    assert stable_prefix(a, b) is None


def test_stable_prefix_is_none_for_different_materialization_identities(payload_root: Path):
    context = make_context()
    a = canonical_materialize(context, mi_v1(), "prompt", protocol_root=str(payload_root))
    b = materialize(context, payload_root)
    assert stable_prefix(a, b) is None


# --- serialization -----------------------------------------------------------


def test_serialization_is_utf8_without_bom_and_with_lf(payload_root: Path):
    materialization = materialize(make_context(), payload_root)
    assert not materialization.payload.startswith(b"\xef\xbb\xbf")
    assert b"\r\n" not in materialization.payload
    assert materialization.payload.endswith(b"\n")


def test_v1_materialization_has_no_resolved_stable_region(payload_root: Path):
    materialization = canonical_materialize(
        make_context(), mi_v1(), "prompt", protocol_root=str(payload_root)
    )
    assert materialization.stable_prefix_bytes == b""
    assert materialization.stable_region == b""
    assert materialization.stable_segments == ()
    assert materialization.dynamic_suffix == materialization.payload


def test_materialization_carries_no_repo_absolute_paths(payload_root: Path):
    materialization = materialize(make_context(), payload_root)
    text = materialization.payload.decode("utf-8")
    assert str(payload_root) not in text
    assert ".agents/" in text
