"""Tests for harness policy H13: protocol taxonomy coherence.

Validates that `.agents/standards/runtime/PROTOCOL_TAXONOMY.md` (the master
dictionary) stays coherent with the real protocol files: state machines,
workflows, harness policies, contracts, roles and workers.

See `.agents/harness/policies/H13-protocol-taxonomy.md` for the rules.
"""

from __future__ import annotations

import re
from pathlib import Path

import pytest
import yaml

PROJECT_ROOT = Path(__file__).resolve().parents[3]
AGENTS_DIR = PROJECT_ROOT / ".agents"
TAXONOMY_PATH = AGENTS_DIR / "standards" / "runtime" / "PROTOCOL_TAXONOMY.md"

# H13 validates the explicit core harness list. H08 is intentionally omitted
# and H12 is free (former H12 became D01); neither is reported as missing.
EXPECTED_CORE_HARNESS_IDS = [f"H{i:02d}" for i in range(8)] + ["H09", "H10", "H11"]
INTENTIONALLY_ABSENT_IDS = {"H08", "H12"}

DOMAIN_PREFIX = {"core": "H", "discovery": "D", "system": "S"}
CROSS_CUTTING_HARNESS_IDS = {"H13"}

TERMINAL_STATES = {
    "core:COMPLETED",
    "core:ABORT",
    "discovery:DISCOVERY_READY",
    "discovery:DISCOVERY_FAILED",
}
ROOT_STATES = {"system:SYSTEM_INIT", "discovery:DISCOVERY_INIT"}


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def load_taxonomy() -> dict:
    content = TAXONOMY_PATH.read_text(encoding="utf-8")
    match = re.search(r"```yaml\n(.*?)\n```", content, re.DOTALL)
    assert match, "No ```yaml block found in PROTOCOL_TAXONOMY.md"
    data = yaml.safe_load(match.group(1))
    assert isinstance(data, dict), "Taxonomy YAML block must be a mapping"
    return data


def extract_metadata_block(path: Path) -> dict | None:
    """Extract the YAML taxonomy metadata block from a protocol file.

    Files that start with a TOML front matter block (+++ ... +++) carry the
    YAML taxonomy block immediately after it; all other files carry it at the
    very top of the file.
    """
    content = path.read_text(encoding="utf-8")
    toml = re.match(r"^\+\+\+\s*\n(.*?)\n\+\+\+\s*\n", content, re.DOTALL)
    rest = content[toml.end() :] if toml else content
    match = re.match(r"^---\s*\n(.*?)\n---\s*\n", rest, re.DOTALL)
    if not match:
        return None
    data = yaml.safe_load(match.group(1))
    return data if isinstance(data, dict) else None


@pytest.fixture(scope="module")
def taxonomy() -> dict:
    return load_taxonomy()


@pytest.fixture(scope="module")
def entities(taxonomy) -> dict:
    return taxonomy["entities"]


@pytest.fixture(scope="module")
def states(entities) -> dict:
    return {k: v for k, v in entities.items() if v.get("kind") == "state"}


@pytest.fixture(scope="module")
def artifacts(entities) -> dict:
    return {k: v for k, v in entities.items() if v.get("kind") == "artifact"}


@pytest.fixture(scope="module")
def harnesses(entities) -> dict:
    return {k: v for k, v in entities.items() if v.get("kind") == "harness"}


@pytest.fixture(scope="module")
def workers(entities) -> dict:
    return {k: v for k, v in entities.items() if v.get("kind") == "worker"}


@pytest.fixture(scope="module")
def workflow_entities(entities) -> dict:
    return {k: v for k, v in entities.items() if v.get("kind") == "workflow"}


@pytest.fixture(scope="module")
def contract_entities(entities) -> dict:
    return {k: v for k, v in entities.items() if v.get("kind") == "contract"}


# ---------------------------------------------------------------------------
# Taxonomy structure
# ---------------------------------------------------------------------------


def test_taxonomy_file_exists():
    assert TAXONOMY_PATH.is_file(), f"Missing {TAXONOMY_PATH}"


def test_taxonomy_has_required_sections(taxonomy):
    for section in ("domains", "lifecycles", "entities", "tags"):
        assert section in taxonomy, f"Taxonomy missing section '{section}'"
    for domain in ("core", "discovery", "system", "cross-cutting"):
        assert domain in taxonomy["domains"], f"Missing domain '{domain}'"


def test_lifecycles_reference_valid_domains(taxonomy):
    for name, lifecycle in taxonomy["lifecycles"].items():
        assert (
            lifecycle["domain"] in taxonomy["domains"]
        ), f"Lifecycle '{name}' references unknown domain '{lifecycle['domain']}'"


# ---------------------------------------------------------------------------
# States
# ---------------------------------------------------------------------------


def test_every_state_has_domain_previous_next(states):
    assert states, "No states defined in taxonomy"
    for key, state in states.items():
        assert state.get("domain"), f"State '{key}' missing domain"
        assert "previous" in state, f"State '{key}' missing previous"
        assert "next" in state, f"State '{key}' missing next"
        assert key.startswith(
            f"{state['domain']}:"
        ), f"State key '{key}' does not match its domain '{state['domain']}'"


def test_state_references_exist(states):
    for key, state in states.items():
        for rel in ("previous", "next"):
            for ref in state.get(rel) or []:
                assert (
                    ref in states
                ), f"State '{key}' {rel} references unknown state '{ref}'"


def test_state_transitions_are_symmetric(states):
    """If A lists B in next, B must list A in previous (and vice versa)."""
    for key, state in states.items():
        for nxt in state.get("next") or []:
            assert key in (
                states[nxt].get("previous") or []
            ), f"'{key}' -> '{nxt}' in next, but '{nxt}' does not list '{key}' in previous"
        for prev in state.get("previous") or []:
            assert key in (
                states[prev].get("next") or []
            ), f"'{key}' <- '{prev}' in previous, but '{prev}' does not list '{key}' in next"


def test_no_orphan_states(states):
    """Every non-terminal state has a next transition and is reachable from a root."""
    for key, state in states.items():
        if key in TERMINAL_STATES:
            continue
        assert state.get("next"), f"Orphan state '{key}': no next transitions"

    reachable: set[str] = set()
    stack = list(ROOT_STATES)
    while stack:
        current = stack.pop()
        if current in reachable:
            continue
        reachable.add(current)
        stack.extend(states[current].get("next") or [])
    unreachable = set(states) - reachable
    assert not unreachable, f"Unreachable states: {sorted(unreachable)}"


def test_core_states_cover_state_machine(states):
    """All core states of AGENT_STATE_MACHINE.md are present."""
    expected = {
        "SYSTEM_READY",
        "TASK_RECEIVED",
        "ANALYZING_TASK",
        "CONFIRMING_INTENT",
        "BUILDING_TASK_SPECIFICATION",
        "NEEDS_CLARIFICATION",
        "TASK_READY",
        "GATHERING_CONTEXT",
        "CONTEXT_GATHERED",
        "VALIDATING_CONTEXT",
        "CONTEXT_READY",
        "PLANNING",
        "PLAN_READY",
        "EXECUTING",
        "VERIFYING",
        "RECOVERY",
        "COMPLETED",
        "ABORT",
    }
    core_states = {
        key.split(":", 1)[1] for key, s in states.items() if s["domain"] == "core"
    }
    missing = expected - core_states
    assert not missing, f"Core states missing from taxonomy: {sorted(missing)}"


# ---------------------------------------------------------------------------
# Artifacts
# ---------------------------------------------------------------------------


def test_artifacts_have_produced_by_and_consumed_by(artifacts, states):
    assert artifacts, "No artifacts defined in taxonomy"
    for name, artifact in artifacts.items():
        assert artifact.get("produced_by"), f"Artifact '{name}' missing produced_by"
        assert (
            artifact.get("consumed_by") is not None
        ), f"Artifact '{name}' missing consumed_by"
        for ref in artifact["produced_by"]:
            assert ref in states, f"Artifact '{name}' produced_by unknown state '{ref}'"
        for ref in artifact["consumed_by"]:
            assert ref in states, f"Artifact '{name}' consumed_by unknown state '{ref}'"


def test_artifact_contract_files_exist(artifacts):
    for name, artifact in artifacts.items():
        contract = artifact.get("contract")
        assert contract, f"Artifact '{name}' missing contract path"
        assert (
            PROJECT_ROOT / contract
        ).is_file(), f"Contract file for artifact '{name}' not found: {contract}"


# ---------------------------------------------------------------------------
# Harness policies
# ---------------------------------------------------------------------------


def test_harness_namespace_prefixes(harnesses):
    for name, harness in harnesses.items():
        hid = harness.get("harness_id")
        domain = harness.get("domain")
        assert hid and domain, f"Harness '{name}' missing harness_id or domain"
        if hid in CROSS_CUTTING_HARNESS_IDS:
            assert (
                domain == "cross-cutting"
            ), f"Cross-cutting harness '{name}' must have domain cross-cutting"
            continue
        expected_prefix = DOMAIN_PREFIX.get(domain)
        assert expected_prefix, f"Harness '{name}' has unexpected domain '{domain}'"
        assert hid.startswith(expected_prefix), (
            f"Harness '{name}' id '{hid}' does not respect prefix '{expected_prefix}' "
            f"of domain '{domain}'"
        )


def test_no_harness_id_collisions_between_domains(harnesses):
    by_id: dict[str, str] = {}
    for name, harness in harnesses.items():
        hid = harness["harness_id"]
        domain = harness["domain"]
        if hid in by_id:
            assert (
                by_id[hid] == domain
            ), f"Harness id '{hid}' used in domains '{by_id[hid]}' and '{domain}'"
        by_id[hid] = domain


def test_expected_core_harnesses_present(harnesses):
    core_ids = {h["harness_id"] for h in harnesses.values() if h["domain"] == "core"}
    for hid in EXPECTED_CORE_HARNESS_IDS:
        assert hid in core_ids, f"Core harness '{hid}' missing from taxonomy"


def test_h08_and_h12_not_reported_missing(harnesses):
    """H08 (intentionally omitted) and H12 (freed, renamed to D01) are not errors."""
    all_ids = {h["harness_id"] for h in harnesses.values()}
    for hid in INTENTIONALLY_ABSENT_IDS:
        assert hid not in all_ids, f"'{hid}' should not exist in the taxonomy"
    # Recompute the expected core list explicitly instead of a numeric range:
    # this is the mechanism by which H08/H12 are never reported as missing.
    core_ids = {h["harness_id"] for h in harnesses.values() if h["domain"] == "core"}
    missing = set(EXPECTED_CORE_HARNESS_IDS) - core_ids
    assert not missing, f"Missing core harnesses: {sorted(missing)}"
    assert INTENTIONALLY_ABSENT_IDS.isdisjoint(set(EXPECTED_CORE_HARNESS_IDS))


def test_harness_gates_are_allowed_transitions(harnesses, states):
    for name, harness in harnesses.items():
        for gate in harness.get("gates") or []:
            assert " -> " in gate, f"Harness '{name}' gate malformed: {gate!r}"
            src, dst = (part.strip() for part in gate.split(" -> ", 1))
            assert src in states, f"Harness '{name}' gate source unknown: '{src}'"
            assert dst in states, f"Harness '{name}' gate target unknown: '{dst}'"
            assert dst in (states[src].get("next") or []), (
                f"Harness '{name}' gates transition '{src} -> {dst}' "
                f"not allowed by the taxonomy"
            )


def test_harness_policy_files_exist(harnesses):
    for name, harness in harnesses.items():
        policy_file = harness.get("policy_file")
        assert policy_file, f"Harness '{name}' missing policy_file"
        if harness.get("status") == "planned":
            continue  # created by PLAN_DISCOVERY_ORCHESTRATOR
        assert (
            PROJECT_ROOT / policy_file
        ).is_file(), f"Policy file for harness '{name}' not found: {policy_file}"


# ---------------------------------------------------------------------------
# Workers, actors, roles
# ---------------------------------------------------------------------------


def test_workers_reference_valid_entities(workers, states, entities, taxonomy):
    actors = {k for k, v in entities.items() if v.get("kind") == "actor"}
    assert workers, "No workers defined in taxonomy"
    for name, worker in workers.items():
        state = worker.get("state")
        actor = worker.get("actor")
        domain = worker.get("domain")
        assert state in states, f"Worker '{name}' references unknown state '{state}'"
        assert actor in actors, f"Worker '{name}' references unknown actor '{actor}'"
        assert (
            domain in taxonomy["domains"]
        ), f"Worker '{name}' unknown domain '{domain}'"
        assert (
            states[state]["domain"] in (domain, "core", "cross-cutting")
            or domain == "cross-cutting"
        ), f"Worker '{name}' domain '{domain}' inconsistent with state '{state}'"


def test_actor_role_files_exist(entities):
    for name, actor in entities.items():
        if actor.get("kind") != "actor":
            continue
        role_file = actor.get("role_file")
        assert role_file, f"Actor '{name}' missing role_file"
        if actor.get("status") == "planned":
            continue
        assert (
            PROJECT_ROOT / role_file
        ).is_file(), f"Role file for actor '{name}' not found: {role_file}"


# ---------------------------------------------------------------------------
# Metadata blocks on real protocol files
# ---------------------------------------------------------------------------


def _workflow_files() -> list[Path]:
    return [
        p
        for p in sorted(AGENTS_DIR.glob("orchestrators/*/workflow/*.md"))
        if p.name != "INDEX.md"
    ]


def _policy_files() -> list[Path]:
    files = sorted(AGENTS_DIR.glob("orchestrators/*/harness/policies/*.md"))
    files += sorted((AGENTS_DIR / "harness" / "policies").glob("*.md"))
    return files


def _contract_files() -> list[Path]:
    files = sorted((AGENTS_DIR / "contracts").glob("*.md"))
    files += sorted(AGENTS_DIR.glob("orchestrators/*/contracts/*.md"))
    return files


def _state_machine_files() -> list[Path]:
    return sorted(AGENTS_DIR.glob("orchestrators/*/states/*.md"))


def _role_files() -> list[Path]:
    files = [
        AGENTS_DIR / "orchestrators" / "core" / "roles" / "orchestrator.md",
        AGENTS_DIR / "orchestrators" / "system" / "roles" / "argentos.md",
        AGENTS_DIR / "roles" / "worker.md",
    ]
    files += sorted((AGENTS_DIR / "roles" / "profiles").glob("*.md"))
    return [p for p in files if p.name != "README.md" and p.is_file()]


def _check_common_block(path: Path) -> dict:
    meta = extract_metadata_block(path)
    assert meta is not None, f"{path}: missing taxonomy metadata block"
    for field in ("taxonomy", "kind", "domain"):
        assert field in meta, f"{path}: metadata block missing field '{field}'"
    assert (
        meta["taxonomy"] == ".agents/standards/runtime/PROTOCOL_TAXONOMY.md"
    ), f"{path}: wrong taxonomy pointer {meta['taxonomy']!r}"
    return meta


@pytest.mark.parametrize("path", _workflow_files(), ids=lambda p: p.name)
def test_workflow_metadata(path, states):
    meta = _check_common_block(path)
    assert meta["kind"] == "workflow", f"{path}: kind must be workflow"
    domain = meta["domain"]
    state = meta.get("state")
    assert state, f"{path}: workflow missing state"
    ref = state if ":" in state else f"{domain}:{state}"
    assert ref in states, f"{path}: unknown state '{ref}'"
    assert (
        states[ref]["domain"] == domain
    ), f"{path}: state '{ref}' belongs to another domain"


@pytest.mark.parametrize("path", _policy_files(), ids=lambda p: p.name)
def test_policy_metadata(path, harnesses, taxonomy):
    meta = _check_common_block(path)
    assert meta["kind"] == "harness", f"{path}: kind must be harness"
    hid = meta.get("harness_id")
    assert hid, f"{path}: policy missing harness_id"
    entry = next((h for h in harnesses.values() if h["harness_id"] == hid), None)
    assert entry, f"{path}: harness_id '{hid}' not registered in taxonomy"
    assert (
        meta["domain"] == entry["domain"]
    ), f"{path}: domain '{meta['domain']}' != taxonomy domain '{entry['domain']}'"
    if hid in CROSS_CUTTING_HARNESS_IDS:
        return
    expected_prefix = DOMAIN_PREFIX[entry["domain"]]
    assert hid.startswith(
        expected_prefix
    ), f"{path}: id '{hid}' violates prefix '{expected_prefix}'"


@pytest.mark.parametrize("path", _contract_files(), ids=lambda p: p.name)
def test_contract_metadata(path, artifacts):
    meta = _check_common_block(path)
    assert meta["kind"] == "contract", f"{path}: kind must be contract"
    artifact = meta.get("artifact")
    assert artifact == path.name, f"{path}: artifact field must equal the file name"
    assert artifact in artifacts, f"{path}: artifact '{artifact}' not in taxonomy"
    assert meta["domain"] == artifacts[artifact]["domain"], (
        f"{path}: domain '{meta['domain']}' != taxonomy domain "
        f"'{artifacts[artifact]['domain']}'"
    )


@pytest.mark.parametrize("path", _state_machine_files(), ids=lambda p: p.name)
def test_state_machine_metadata(path, states):
    meta = _check_common_block(path)
    assert meta["kind"] == "state_machine", f"{path}: kind must be state_machine"
    domain = meta["domain"]
    defined = meta.get("states_defined") or []
    assert defined, f"{path}: state machine must list states_defined"
    for state in defined:
        ref = state if ":" in state else f"{domain}:{state}"
        assert ref in states, f"{path}: defines unknown state '{ref}'"


@pytest.mark.parametrize("path", _role_files(), ids=lambda p: p.name)
def test_role_metadata(path, taxonomy):
    meta = _check_common_block(path)
    assert meta["kind"] in ("role", "worker"), f"{path}: kind must be role or worker"
    assert (
        meta["domain"] in taxonomy["domains"]
    ), f"{path}: unknown domain '{meta['domain']}'"


# ---------------------------------------------------------------------------
# Workflow and contract entities vs real front matter
# ---------------------------------------------------------------------------


def _rel(path: Path) -> str:
    return path.relative_to(PROJECT_ROOT).as_posix()


def _namespaced(value: str, domain: str) -> str:
    return value if ":" in value else f"{domain}:{value}"


@pytest.mark.parametrize("path", _workflow_files(), ids=lambda p: p.name)
def test_workflow_has_matching_taxonomy_entity(
    path, workflow_entities, states, artifacts, harnesses
):
    meta = extract_metadata_block(path)
    assert meta is not None, f"{path}: missing taxonomy metadata block"
    entity = next(
        (e for e in workflow_entities.values() if e.get("file") == _rel(path)), None
    )
    assert entity, f"{path}: no workflow entity in taxonomy with file={_rel(path)}"

    assert (
        entity["domain"] == meta["domain"]
    ), f"{path}: domain {entity['domain']!r} != front matter {meta['domain']!r}"
    assert entity["state"] == _namespaced(
        meta["state"], meta["domain"]
    ), f"{path}: state {entity['state']!r} != front matter {meta['state']!r}"
    assert entity["state"] in states, f"{path}: unknown state '{entity['state']}'"
    assert entity.get("lifecycle") == meta.get(
        "lifecycle"
    ), f"{path}: lifecycle mismatch"
    for field in ("previous_states", "next_states"):
        expected = {_namespaced(s, meta["domain"]) for s in (meta.get(field) or [])}
        actual = set(entity.get(field) or [])
        assert (
            actual == expected
        ), f"{path}: {field} {sorted(actual)} != {sorted(expected)}"
        for ref in actual:
            assert ref in states, f"{path}: {field} references unknown state '{ref}'"
    for field in ("input_artifacts", "output_artifacts"):
        expected = set(meta.get(field) or [])
        actual = set(entity.get(field) or [])
        assert (
            actual == expected
        ), f"{path}: {field} {sorted(actual)} != {sorted(expected)}"
        for ref in actual:
            if ref.endswith(".md"):
                assert (
                    ref in artifacts
                ), f"{path}: {field} references unknown artifact '{ref}'"
    expected_harness = set(meta.get("harness") or [])
    actual_harness = set(entity.get("harness") or [])
    assert (
        actual_harness == expected_harness
    ), f"{path}: harness {sorted(actual_harness)} != {sorted(expected_harness)}"
    for ref in actual_harness:
        assert ref in harnesses, f"{path}: harness references unknown policy '{ref}'"
    assert entity.get("actor") == meta.get("actor"), f"{path}: actor mismatch"


@pytest.mark.parametrize("path", _contract_files(), ids=lambda p: p.name)
def test_contract_has_matching_taxonomy_entity(path, contract_entities, states):
    meta = extract_metadata_block(path)
    assert meta is not None, f"{path}: missing taxonomy metadata block"
    entity = next(
        (e for e in contract_entities.values() if e.get("file") == _rel(path)), None
    )
    assert entity, f"{path}: no contract entity in taxonomy with file={_rel(path)}"

    assert (
        entity["domain"] == meta["domain"]
    ), f"{path}: domain {entity['domain']!r} != front matter {meta['domain']!r}"
    assert (
        entity["artifact"] == meta["artifact"] == path.name
    ), f"{path}: artifact mismatch"
    assert entity.get("lifecycle") == meta.get(
        "lifecycle"
    ), f"{path}: lifecycle mismatch"
    for field in ("produced_by", "consumed_by"):
        expected = {_namespaced(s, meta["domain"]) for s in (meta.get(field) or [])}
        actual = set(entity.get(field) or [])
        assert (
            actual == expected
        ), f"{path}: {field} {sorted(actual)} != {sorted(expected)}"
        for ref in actual:
            assert ref in states, f"{path}: {field} references unknown state '{ref}'"


def test_every_workflow_entity_file_exists(workflow_entities):
    assert workflow_entities, "No workflow entities defined in taxonomy"
    for name, entity in workflow_entities.items():
        assert (
            PROJECT_ROOT / entity["file"]
        ).is_file(), (
            f"Workflow entity '{name}' references missing file: {entity['file']}"
        )


def test_every_contract_entity_file_exists(contract_entities):
    assert contract_entities, "No contract entities defined in taxonomy"
    for name, entity in contract_entities.items():
        assert (
            PROJECT_ROOT / entity["file"]
        ).is_file(), (
            f"Contract entity '{name}' references missing file: {entity['file']}"
        )
