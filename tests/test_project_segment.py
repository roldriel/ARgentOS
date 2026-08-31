"""Behavioral tests for the derived Project Segment (plan 90, RFC-73).

Implements the testable properties of RFC-73 (section 25) and the mandatory
scenarios of plan 90 at the reference runtime level: ProjectIdentity /
project_namespace, cross-project isolation, the derived store, discovery
fingerprint non-equivalence, freshness vs invalidation, revalidation,
provenance, the project-without-registry behavior and RFC-72 identity parity.
The suite is self-contained (stdlib + the runtime modules) and never depends
on the `protocol/` payload (tests/AGENTS.md).
"""

from __future__ import annotations

import json
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT))

from runtime.toolcalls import budget as runtime_budget  # noqa: E402
from runtime.toolcalls.canonical import PROTOCOL_VERSION  # noqa: E402
from runtime.toolcalls import identity as identity_mod  # noqa: E402
from runtime.toolcalls import project_segment  # noqa: E402
from runtime.toolcalls import project_store  # noqa: E402

# PROTOCOL_VERSION is the single runtime semantic anchor (RFC-71): the canonical
# materialization suite shares it, and tools/check_version_state.py pins it to
# protocol/.agents/VERSION so it cannot silently drift on future bumps.
NOW = datetime(2026, 8, 31, 12, 0, 0, tzinfo=timezone.utc)


def make_entry(
    path: str = "environment.md",
    title: str = "Environment",
    kind: str = "snapshot",
    **overrides,
) -> dict:
    """A KB entry front matter in the shape of KB_DISCOVERY_ENTRY."""
    entry = {
        "path": path,
        "artifact": "KB_DISCOVERY_ENTRY.md",
        "kind": kind,
        "title": title,
        "generated_at": "2026-08-30T12:00:00Z",
        "tags": ["discovery", "environment"],
        "source_files": ["pyproject.toml"],
        "source_sessions": [],
        "status": "active",
    }
    entry.update(overrides)
    return entry


def make_manifest(
    *,
    ttl_hours: int = 24,
    project_root: str = "/repo",
    active: tuple[str, ...] = ("environment.md",),
    stale: tuple[str, ...] = (),
    hashes: dict | None = None,
) -> dict:
    """A discovery manifest in the shape of DISCOVERY_MANIFEST."""
    return {
        "knowledge_base": {
            "version": "1.0.0",
            "generated_at": "2026-08-30T12:00:00Z",
            "updated_at": "2026-08-30T12:00:00Z",
            "ttl_hours": ttl_hours,
            "role_version": "discovery_orchestrator:v1",
            "task_scope": "full",
            "project_root": project_root,
            "project_shape": "library",
        },
        "hashes": hashes
        or {
            "config_files_hash": "sha256:cfg-a",
            "sample_files_hash": "sha256:sample-a",
            "environment_hash": "sha256:env-a",
            "structure_hash": "sha256:struct-a",
        },
        "entries": {"active": list(active), "stale": list(stale)},
        "workers": {"invoked": [], "completed": []},
    }


def last_discovery_at(hours_ago: int) -> dict:
    """A ``.last_discovery`` marker whose timestamp is ``hours_ago`` before NOW."""
    timestamp = (NOW - timedelta(hours=hours_ago)).isoformat().replace(
        "+00:00", "Z"
    )
    return {"timestamp": timestamp, "scope": "full", "status": "DISCOVERY_READY"}


def build_fake_kb(
    tmp_path: Path,
    *,
    subdir: str = "project",
    entry_path: str = "environment.md",
    title: str = "Environment",
    source_files: list[str] | None = None,
    stale: tuple[str, ...] = (),
    ttl_hours: int = 24,
    hours_ago: int = 1,
    project_root: str | None = None,
) -> tuple[Path, dict, list[dict]]:
    """A minimal real KB: project root, source files, marker, manifest."""
    root = tmp_path / subdir
    source_files = source_files or ["pyproject.toml"]
    for source in source_files:
        target = root / source
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text("x", encoding="utf-8")
    project_dir = root / ".project"
    project_dir.mkdir(parents=True, exist_ok=True)
    kb_root = project_dir / "knowledge" / "discovery"
    kb_root.mkdir(parents=True, exist_ok=True)
    marker = last_discovery_at(hours_ago)
    (project_dir / ".last_discovery").write_text(
        json.dumps(marker), encoding="utf-8"
    )
    entry = make_entry(
        path=entry_path,
        title=title,
        source_files=source_files,
    )
    manifest = make_manifest(
        ttl_hours=ttl_hours,
        project_root=project_root or str(root),
        active=(entry_path,),
        stale=stale,
    )
    return kb_root, manifest, [entry]


# --- ProjectIdentity / project_namespace --------------------------------------


def test_project_namespace_is_the_registry_id():
    assert project_segment.project_namespace("PRJ-0001") == "PRJ-0001"
    assert project_segment.project_namespace("PRJ-0042") == "PRJ-0042"


def test_project_without_registry_has_no_namespace():
    # No PROJECT_REGISTRY.project_id ⇒ no ProjectIdentity ⇒ no namespace and
    # no fallback derived from path, name or hash.
    assert project_segment.project_namespace(None) is None
    assert project_segment.project_namespace("") is None
    assert project_segment.project_namespace("   ") is None


def test_project_namespace_is_logical_not_physical():
    # The function has no path input: the namespace depends only on the
    # registry ID, so the same project at /path/a and /path/b keeps the same
    # logical identity (PROJECT_REGISTRY "Identity and locator"; D-022).
    assert project_segment.project_namespace("PRJ-0001") == (
        project_segment.project_namespace("PRJ-0001")
    )
    assert project_segment.project_namespace("PRJ-0001") != (
        project_segment.project_namespace("PRJ-0002")
    )


def test_no_fallback_from_path_or_hash():
    # The registry is the only source of ProjectIdentity: the namespace
    # function takes a registry ID (never a path/hash and never computes one),
    # and an absent registry ID yields no namespace instead of a fallback.
    import inspect

    parameters = list(inspect.signature(project_segment.project_namespace).parameters)
    assert parameters == ["project_registry_id"]
    assert project_segment.project_namespace(None) is None


# --- SegmentIdentity(project) --------------------------------------------------


def test_segment_identity_same_components_same_identity():
    content = project_segment.kb_canonical_content(make_manifest(), [make_entry()])
    cid = project_segment.segment_content_identity(content)
    first = project_segment.project_segment_identity(
        PROTOCOL_VERSION, cid, "PRJ-0001"
    )
    second = project_segment.project_segment_identity(
        PROTOCOL_VERSION, cid, "PRJ-0001"
    )
    assert first == second


def test_same_content_different_namespace_different_identity():
    content = project_segment.kb_canonical_content(make_manifest(), [make_entry()])
    cid = project_segment.segment_content_identity(content)
    a = project_segment.project_segment_identity(
        PROTOCOL_VERSION, cid, "PRJ-0001"
    )
    b = project_segment.project_segment_identity(
        PROTOCOL_VERSION, cid, "PRJ-0002"
    )
    assert a != b  # I-PROJ-001/002: no cross-project reuse


def test_segment_identity_changes_with_version_or_content():
    content = project_segment.kb_canonical_content(make_manifest(), [make_entry()])
    cid = project_segment.segment_content_identity(content)
    base = project_segment.project_segment_identity(
        PROTOCOL_VERSION, cid, "PRJ-0001"
    )
    other_version = project_segment.project_segment_identity(
        "10.1.0", cid, "PRJ-0001"
    )
    other_content = project_segment.project_segment_identity(
        PROTOCOL_VERSION,
        project_segment.segment_content_identity(b"other"),
        "PRJ-0001",
    )
    assert base != other_version
    assert base != other_content
    assert "semantic_version" in base and "namespace" in base


def test_parity_with_plan89_identity_formula():
    # Plan 90 replicates the exact RFC-71 formula of plan 89's identity module:
    # same components ⇒ same serialized SegmentIdentity (no second definition).
    cid = project_segment.segment_content_identity(b"kb")
    ours = project_segment.project_segment_identity(
        PROTOCOL_VERSION, cid, "PRJ-0001"
    )
    theirs = identity_mod.segment_identity(
        PROTOCOL_VERSION, cid, "PRJ-0001"
    )
    assert ours == theirs
    assert ours == identity_mod.SegmentIdentity(
        PROTOCOL_VERSION, cid, "PRJ-0001"
    ).serialize()


def test_project_segment_participates_in_semantic_context_identity():
    # Project persistence → Context Composition → SemanticContextIdentity:
    # the derived project segment is a valid RFC-71 segment for composition and
    # no alternative identity is created (RFC-73 §11-12; I-PROJ-008).
    manifest = make_manifest()
    entry = make_entry()
    content = project_segment.kb_canonical_content(manifest, [entry])
    cid = project_segment.segment_content_identity(content)
    seg = identity_mod.Segment(
        kind="project",
        semantic_version=PROTOCOL_VERSION,
        namespace="PRJ-0001",
        content=content,
    )
    sci = identity_mod.semantic_context_identity(
        PROTOCOL_VERSION, "PRJ-0001", (seg,)
    )
    expected = identity_mod.segment_identity(PROTOCOL_VERSION, cid, "PRJ-0001")
    assert expected in [s.serialize() for s in sci.segments]


# --- Discovery fingerprints ≠ SegmentContentIdentity ---------------------------


def test_discovery_hashes_are_fingerprints_not_content_identity():
    manifest = make_manifest()
    content = project_segment.kb_canonical_content(manifest, [make_entry()])
    cid = project_segment.segment_content_identity(content)
    hashes = project_segment.discovery_hashes(manifest)
    assert set(hashes) == {
        "config_files_hash",
        "sample_files_hash",
        "environment_hash",
        "structure_hash",
    }
    for fingerprint in hashes.values():
        assert fingerprint != cid  # RFC-73 §5: never unified
    assert project_segment.discovery_hashes(None) == {}


# --- Freshness / revalidation ---------------------------------------------------


def test_reuse_eligibility_fresh():
    status = project_segment.reuse_eligibility(
        make_manifest(),
        last_discovery_at(1),
        [make_entry()],
        lambda entry: True,
        now=NOW,
    )
    assert status == "FRESH"


def test_reuse_eligibility_ttl_expiry_is_stale_not_invalid():
    status = project_segment.reuse_eligibility(
        make_manifest(ttl_hours=24),
        last_discovery_at(25),
        [make_entry()],
        lambda entry: True,
        now=NOW,
    )
    assert status == "STALE"  # I-PROJ-005: stale ≠ invalid
    assert status != "INVALID"


def test_reuse_eligibility_missing_marker_is_stale_not_invalid():
    # DISCOVERY_STATE_MACHINE: missing/unparsable marker ⇒ TTL treated as
    # expired; never a semantic verdict.
    status = project_segment.reuse_eligibility(
        make_manifest(),
        None,
        [make_entry()],
        lambda entry: True,
        now=NOW,
    )
    assert status == "STALE"
    assert status != "INVALID"


def test_reuse_eligibility_stale_manifest_entries():
    status = project_segment.reuse_eligibility(
        make_manifest(stale=("old_feature.md",)),
        last_discovery_at(1),
        [make_entry()],
        lambda entry: True,
        now=NOW,
    )
    assert status == "STALE"


def test_reuse_eligibility_unresolved_provenance_is_stale():
    status = project_segment.reuse_eligibility(
        make_manifest(),
        last_discovery_at(1),
        [make_entry()],
        lambda entry: False,
        now=NOW,
    )
    assert status == "STALE"
    assert status != "INVALID"


def test_reuse_eligibility_unknown_without_ttl():
    manifest = make_manifest()
    del manifest["knowledge_base"]["ttl_hours"]
    assert (
        project_segment.reuse_eligibility(
            manifest, last_discovery_at(1), [make_entry()], lambda e: True, now=NOW
        )
        == "UNKNOWN"
    )
    assert (
        project_segment.reuse_eligibility(
            None, last_discovery_at(1), [], lambda e: True, now=NOW
        )
        == "UNKNOWN"
    )


def test_fresh_does_not_imply_eligible():
    status = project_segment.reuse_eligibility(
        make_manifest(),
        last_discovery_at(1),
        [make_entry()],
        lambda entry: True,
        now=NOW,
    )
    assert status == "FRESH"
    # Freshness is not an eligibility verdict (RFC-73 §9): scope, policy and
    # the Context Budget still govern selection (I-PROJ-006/007).
    assert status not in {"ELIGIBLE", "NOT ELIGIBLE"}


def test_revalidation_same_fingerprint_keeps_current():
    manifest_a = make_manifest()
    manifest_b = make_manifest()
    assert project_segment.discovery_hashes(manifest_a) == (
        project_segment.discovery_hashes(manifest_b)
    )
    assert (
        project_segment.reuse_eligibility(
            manifest_b, last_discovery_at(1), [make_entry()], lambda e: True, now=NOW
        )
        == "FRESH"
    )


def test_revalidation_changed_fingerprint_is_stale_via_manifest():
    manifest = make_manifest(
        active=(),
        stale=("environment.md",),
        hashes={
            "config_files_hash": "sha256:cfg-b",
            "sample_files_hash": "sha256:sample-a",
            "environment_hash": "sha256:env-a",
            "structure_hash": "sha256:struct-a",
        },
    )
    status = project_segment.reuse_eligibility(
        manifest, last_discovery_at(1), [make_entry()], lambda e: True, now=NOW
    )
    assert status == "STALE"  # affected claims need revalidation, not invalidity


def test_source_unavailable_is_stale_not_invalid():
    # Source unavailable (no marker, unresolved provenance) must not be
    # converted into semantic invalidity (RFC-73 §27F).
    assert (
        project_segment.reuse_eligibility(
            make_manifest(), None, [make_entry()], lambda e: False, now=NOW
        )
        == "STALE"
    )


# --- Canonical content / entry key addressing -----------------------------------


def test_canonical_content_manifest_section_order():
    content = project_segment.kb_canonical_content(make_manifest(), [make_entry()])
    text = content.decode("utf-8")
    assert text.index('"knowledge_base"') < text.index('"hashes"')
    assert text.index('"hashes"') < text.index('"entries"')


def test_canonical_content_orders_entries_by_entry_key():
    entry_b = make_entry(path="b.md", title="B")
    entry_a = make_entry(path="a.md", title="A")
    manifest = make_manifest(active=("a.md", "b.md"))
    first = project_segment.kb_canonical_content(manifest, [entry_b, entry_a])
    second = project_segment.kb_canonical_content(manifest, [entry_a, entry_b])
    assert first == second  # input order is irrelevant
    assert first.index(b'"a.md"') < first.index(b'"b.md"')


def test_entry_key_is_addressing_not_identity():
    # The same entry key (title/path + kind) addresses the entry; changing the
    # entry's content changes the content identity while the addressing is
    # preserved (RFC-73 §7). No new identity types exist (I-PROJ-011).
    manifest = make_manifest()
    first = project_segment.kb_canonical_content(
        manifest, [make_entry(generated_at="2026-08-30T12:00:00Z")]
    )
    second = project_segment.kb_canonical_content(
        manifest, [make_entry(generated_at="2026-08-31T12:00:00Z")]
    )
    assert project_segment.segment_content_identity(first) != (
        project_segment.segment_content_identity(second)
    )
    for serialized in (first, second):
        assert b'"environment.md"' in serialized
        assert b'"snapshot"' in serialized
    for module in (project_segment, project_store):
        assert not hasattr(module, "ProjectKnowledgeIdentity")
        assert not hasattr(module, "KnowledgeIdentity")
        assert not hasattr(module, "EntryIdentity")


# --- Derived store ---------------------------------------------------------------


def test_store_roundtrip(tmp_path):
    kb_root, manifest, entries = build_fake_kb(tmp_path)
    store = project_store.rebuild(kb_root, manifest, entries, "PRJ-0001", PROTOCOL_VERSION)
    path = tmp_path / "project" / ".project" / "knowledge" / project_store.STORE_FILENAME
    project_store.write(path, store)
    assert project_store.load(path) == store
    assert project_store.load(tmp_path / "missing.json") is None


def test_store_load_corrupted_is_none(tmp_path):
    path = tmp_path / project_store.STORE_FILENAME
    path.write_text("{not json", encoding="utf-8")
    assert project_store.load(path) is None
    path.write_text(json.dumps({"segment_identity": "x"}), encoding="utf-8")
    assert project_store.load(path) is None  # incomplete schema ⇒ corrupt
    path.write_text(json.dumps(["not", "a", "dict"]), encoding="utf-8")
    assert project_store.load(path) is None


def test_store_write_is_atomic_on_failure(tmp_path):
    path = tmp_path / project_store.STORE_FILENAME
    path.write_text("previous", encoding="utf-8")
    with pytest.raises(TypeError):
        project_store.write(path, {"segment_identity": "x", "bad": object()})
    assert path.read_text(encoding="utf-8") == "previous"
    leftovers = [p for p in tmp_path.iterdir() if p.name.endswith(".tmp")]
    assert leftovers == []


def test_store_write_leaves_no_temp_files(tmp_path):
    path = tmp_path / project_store.STORE_FILENAME
    kb_root, manifest, entries = build_fake_kb(tmp_path)
    store = project_store.rebuild(kb_root, manifest, entries, "PRJ-0001", PROTOCOL_VERSION)
    project_store.write(path, store)
    names = {p.name for p in tmp_path.iterdir()}
    assert project_store.STORE_FILENAME in names
    assert not {n for n in names if n.endswith(".tmp")}


def test_store_rebuild_is_derived_and_deterministic(tmp_path):
    kb_root, manifest, entries = build_fake_kb(tmp_path)
    store = project_store.rebuild(kb_root, manifest, entries, "PRJ-0001", PROTOCOL_VERSION)
    assert store["schema_version"] == project_store.STORE_SCHEMA_VERSION
    assert store["project_namespace"] == "PRJ-0001"
    assert store["semantic_version"] == PROTOCOL_VERSION
    expected_cid = project_segment.segment_content_identity(
        project_segment.kb_canonical_content(manifest, entries)
    )
    assert store["content_identity"] == expected_cid
    assert store["segment_identity"] == project_segment.project_segment_identity(
        PROTOCOL_VERSION, expected_cid, "PRJ-0001"
    )
    assert store["freshness"] == "FRESH"
    assert store["rebuildable"] is True
    assert store["provenance_refs"] == [
        {
            "entry": "environment.md",
            "kind": "snapshot",
            "source_files": ["pyproject.toml"],
            "source_sessions": [],
        }
    ]
    again = project_store.rebuild(kb_root, manifest, entries, "PRJ-0001", PROTOCOL_VERSION)
    assert again["content_identity"] == store["content_identity"]
    assert again["segment_identity"] == store["segment_identity"]
    assert again["freshness"] == store["freshness"]


def test_store_requires_registered_namespace(tmp_path):
    kb_root, manifest, entries = build_fake_kb(tmp_path)
    with pytest.raises(ValueError):
        project_store.rebuild(kb_root, manifest, entries, None, PROTOCOL_VERSION)
    with pytest.raises(ValueError):
        project_store.rebuild(kb_root, manifest, entries, "", PROTOCOL_VERSION)


def test_store_delete_is_cleanup_not_semantic_mutation(tmp_path):
    kb_root, manifest, entries = build_fake_kb(tmp_path)
    store = project_store.rebuild(kb_root, manifest, entries, "PRJ-0001", PROTOCOL_VERSION)
    path = tmp_path / "project" / ".project" / "knowledge" / project_store.STORE_FILENAME
    project_store.write(path, store)
    project_store.delete(path)
    assert not path.exists()
    rebuilt = project_store.rebuild(kb_root, manifest, entries, "PRJ-0001", PROTOCOL_VERSION)
    assert rebuilt["content_identity"] == store["content_identity"]
    assert rebuilt["segment_identity"] == store["segment_identity"]
    assert rebuilt["freshness"] == store["freshness"]


def test_store_rebuild_after_corruption_recovers_identity(tmp_path):
    kb_root, manifest, entries = build_fake_kb(tmp_path)
    store = project_store.rebuild(kb_root, manifest, entries, "PRJ-0001", PROTOCOL_VERSION)
    path = tmp_path / "project" / ".project" / "knowledge" / project_store.STORE_FILENAME
    path.write_text("corrupted{", encoding="utf-8")
    assert project_store.load(path) is None
    recovered = project_store.rebuild(kb_root, manifest, entries, "PRJ-0001", PROTOCOL_VERSION)
    assert recovered["segment_identity"] == store["segment_identity"]


# --- Cross-project isolation (mandatory) ----------------------------------------


def test_cross_project_store_isolation_same_entry_key(tmp_path):
    # Project A and Project B share the same canonical KB content — including
    # the same entry key (`environment.md` / `Environment` / `snapshot`) — but
    # receive distinct namespaces. The namespace is part of the identity, so
    # the same entry key stays isolated (I-PROJ-001/002; plan 90 §31).
    kb_a, manifest_a, entries_a = build_fake_kb(tmp_path, subdir="proj-a")
    kb_b, manifest_b, entries_b = build_fake_kb(tmp_path, subdir="proj-b")
    # Same canonical content: same project_root string, same entry.
    manifest_b = make_manifest(project_root=str(tmp_path / "proj-a"))
    store_a = project_store.rebuild(kb_a, manifest_a, entries_a, "PRJ-0001", PROTOCOL_VERSION)
    store_b = project_store.rebuild(kb_b, manifest_b, entries_b, "PRJ-0002", PROTOCOL_VERSION)
    assert store_a["content_identity"] == store_b["content_identity"]
    assert store_a["project_namespace"] != store_b["project_namespace"]
    assert store_a["segment_identity"] != store_b["segment_identity"]
    assert store_a["provenance_refs"] == store_b["provenance_refs"]  # same key


def test_cross_project_no_contamination(tmp_path):
    # A write → A read = allowed; A write → B read = denied/unavailable; the
    # separation is semantic (namespace inside SegmentIdentity), not only a
    # different storage folder.
    kb_a, manifest_a, entries_a = build_fake_kb(tmp_path, subdir="proj-a")
    kb_b, manifest_b, entries_b = build_fake_kb(tmp_path, subdir="proj-b")
    store_a = project_store.rebuild(kb_a, manifest_a, entries_a, "PRJ-0001", PROTOCOL_VERSION)
    store_b = project_store.rebuild(kb_b, manifest_b, entries_b, "PRJ-0002", PROTOCOL_VERSION)
    path_a = tmp_path / "proj-a" / ".project" / "knowledge" / project_store.STORE_FILENAME
    path_b = tmp_path / "proj-b" / ".project" / "knowledge" / project_store.STORE_FILENAME
    project_store.write(path_a, store_a)
    project_store.write(path_b, store_b)
    loaded_a = project_store.load(path_a)
    loaded_b = project_store.load(path_b)
    assert loaded_a == store_a  # A read → K_A
    assert loaded_b == store_b  # B read → K_B
    assert loaded_a["segment_identity"] != loaded_b["segment_identity"]
    assert loaded_a["project_namespace"] != loaded_b["project_namespace"]
    # B's identity never equals A's knowledge identity, and vice versa.
    assert loaded_a["segment_identity"] not in {
        loaded_b["segment_identity"],
    }


# --- Move / clone / copy / fork semantics ---------------------------------------


def test_move_preserves_logical_identity(tmp_path):
    # Same registered project moved from /path/a to /path/b: the Project
    # Identity (namespace) is unchanged — the locator updates, the identity
    # does not (PROJECT_REGISTRY "Identity and locator"; D-022).
    at_a = project_segment.project_namespace("PRJ-0001")
    at_b = project_segment.project_namespace("PRJ-0001")
    assert at_a == at_b == "PRJ-0001"
    kb_a, manifest_a, entries_a = build_fake_kb(
        tmp_path, subdir="at-a", project_root=str(tmp_path / "at-a")
    )
    kb_b, manifest_b, entries_b = build_fake_kb(
        tmp_path, subdir="at-b", project_root=str(tmp_path / "at-b")
    )
    sid_a = project_store.rebuild(
        kb_a, manifest_a, entries_a, "PRJ-0001", PROTOCOL_VERSION
    )["segment_identity"]
    sid_b = project_store.rebuild(
        kb_b, manifest_b, entries_b, "PRJ-0001", PROTOCOL_VERSION
    )["segment_identity"]
    # The namespace component (the ProjectIdentity) is identical in both
    # locations; the path is never the identity.
    assert json.loads(sid_a)["namespace"] == json.loads(sid_b)["namespace"] == "PRJ-0001"


def test_clone_copy_fork_receives_distinct_identity():
    # A registered copy/fork is its own project with its own Project ID: same
    # canonical content ⇒ same content identity, but distinct namespaces ⇒
    # distinct SegmentIdentity, so no knowledge contamination (RFC-73 §2).
    content = project_segment.kb_canonical_content(make_manifest(), [make_entry()])
    cid = project_segment.segment_content_identity(content)
    original = project_segment.project_segment_identity(
        PROTOCOL_VERSION, cid, "PRJ-0001"
    )
    copy = project_segment.project_segment_identity(
        PROTOCOL_VERSION, cid, "PRJ-0002"
    )
    assert original != copy


# --- Context Budget and RFC-72 boundary ------------------------------------------


def test_context_budget_not_bypassed(tmp_path):
    kb_root, manifest, entries = build_fake_kb(tmp_path)
    store = project_store.rebuild(kb_root, manifest, entries, "PRJ-0001", PROTOCOL_VERSION)
    # The store is identity/freshness metadata only: it carries no context
    # payload and no budget accounting, so persisted knowledge can never be
    # free context (I-PROJ-007; RFC-71 I-010).
    assert set(store) == {
        "schema_version",
        "project_namespace",
        "semantic_version",
        "content_identity",
        "segment_identity",
        "generated_at",
        "freshness",
        "provenance_refs",
        "rebuildable",
    }
    assert "context_budget" not in store
    assert "tokens" not in store
    # The runtime's budget mechanism still applies to any composed content.
    assert runtime_budget.estimate_tokens("x" * 100) == 25


def test_no_provider_cache_duplication():
    # RFC-72/plan 89 owns the provider cache: the project persistence layer
    # introduces no ProviderCacheReference or materialization machinery.
    for module in (project_segment, project_store):
        assert not hasattr(module, "ProviderCacheReference")
        assert not hasattr(module, "MaterializationIdentity")
