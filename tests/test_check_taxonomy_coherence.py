"""Tests for tools/check_taxonomy_coherence.py (dev-only, no payload dependency)."""

from __future__ import annotations

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "tools"))

import check_taxonomy_coherence as ctc  # noqa: E402


TAXONOMY = """# Taxonomy
```yaml
domains:
  core: {}
entities:
  "core:A":
    kind: state
    domain: core
    previous: []
    next:
      - core:B
  "core:B":
    kind: state
    domain: core
    previous:
      - core:A
    next: []
  workflow:00-sample:
    kind: workflow
    domain: core
    state: core:A
    previous_states: []
    next_states:
      - core:B
    input_artifacts: []
    output_artifacts:
      - OUT_A.md
    harness: []
    actor: orchestrator
    profile: null
    file: .agents/orchestrators/core/workflow/00-sample.md
  task_analyst:
    kind: worker
    domain: core
    worker_id: task_analyst
  H00-sample:
    kind: harness
    domain: core
    harness_id: H00
    name: sample
    state: core:A
    gates:
      - "core:A -> core:B"
    policy_file: .agents/orchestrators/core/harness/policies/H00-sample.md
  contract:SAMPLE.md:
    kind: contract
    domain: core
    artifact: SAMPLE.md
    produced_by: [core:A]
    consumed_by: [core:B]
    file: .agents/orchestrators/core/contracts/SAMPLE.md
```
"""

SM = """---
taxonomy: ".agents/standards/runtime/PROTOCOL_TAXONOMY.md"
kind: state_machine
domain: core
actor: orchestrator
states_defined:
  - A
  - B
---
# Sample

## A

### Required Output Artifacts

```text
.project/<session-uuid>/<iteration>/<order>-OUT_A.md
```
"""

WF = """---
taxonomy: ".agents/standards/runtime/PROTOCOL_TAXONOMY.md"
kind: workflow
domain: core
state: A
lifecycle: task
previous_states: []
next_states: [core:B]
input_artifacts: []
output_artifacts: [OUT_A.md]
harness: []
actor: orchestrator
profile: null
---
# Workflow
"""

POLICY = """+++
trigger = "H00"
transition = "A -> B"
+++
---
taxonomy: ".agents/standards/runtime/PROTOCOL_TAXONOMY.md"
kind: harness
domain: core
harness_id: H00
name: sample
state: core:A
gates:
  - "core:A -> core:B"
---
# Policy
"""

CONTRACT = """+++
artifact = "SAMPLE.md"
phase = "00"
produced_by = "task_analyst"
schema_version = "1.0.0"
+++
"""


def make_payload(tmp_path: Path) -> Path:
    agents = tmp_path / "protocol" / ".agents"
    (agents / "standards" / "runtime").mkdir(parents=True)
    (agents / "standards" / "runtime" / "PROTOCOL_TAXONOMY.md").write_text(
        TAXONOMY, encoding="utf-8"
    )
    states = agents / "orchestrators" / "core" / "states"
    states.mkdir(parents=True)
    (states / "SAMPLE_STATE_MACHINE.md").write_text(SM, encoding="utf-8")
    wf = agents / "orchestrators" / "core" / "workflow"
    wf.mkdir(parents=True)
    (wf / "00-sample.md").write_text(WF, encoding="utf-8")
    pol = agents / "orchestrators" / "core" / "harness" / "policies"
    pol.mkdir(parents=True)
    (pol / "H00-sample.md").write_text(POLICY, encoding="utf-8")
    ctr = agents / "orchestrators" / "core" / "contracts"
    ctr.mkdir(parents=True)
    (ctr / "SAMPLE.md").write_text(CONTRACT, encoding="utf-8")
    return tmp_path


def test_clean_payload_passes(tmp_path):
    root = make_payload(tmp_path)
    assert ctc.violations_for_root(root, root / "protocol") == []


def test_workflow_next_not_in_taxonomy(tmp_path):
    root = make_payload(tmp_path)
    wf = root / "protocol" / ".agents" / "orchestrators" / "core" / "workflow" / "00-sample.md"
    wf.write_text(WF.replace("next_states: [core:B]", "next_states: [core:Z]"), encoding="utf-8")
    v = ctc.violations_for_root(root, root / "protocol")
    assert any("next_states not in taxonomy core:A.next" in x for x in v)


def test_gate_target_not_in_taxonomy(tmp_path):
    root = make_payload(tmp_path)
    pol = root / "protocol" / ".agents" / "orchestrators" / "core" / "harness" / "policies" / "H00-sample.md"
    pol.write_text(POLICY.replace('"core:A -> core:B"', '"core:A -> core:Z"'), encoding="utf-8")
    v = ctc.violations_for_root(root, root / "protocol")
    assert any("gate" in x and "not in taxonomy core:A.next" in x for x in v)


def test_duplicate_entity_key(tmp_path):
    root = make_payload(tmp_path)
    taxonomy = root / "protocol" / ".agents" / "standards" / "runtime" / "PROTOCOL_TAXONOMY.md"
    text = taxonomy.read_text(encoding="utf-8")
    idx = text.find('"core:A":')
    idx = text.rfind("\n", 0, idx) + 1  # insert at the start of the key line
    dup = '  "core:A":\n    kind: state\n    domain: core\n    previous: []\n    next: []\n'
    taxonomy.write_text(text[:idx] + dup + text[idx:], encoding="utf-8")
    v = ctc.violations_for_root(root, root / "protocol")
    assert any(x.startswith("DUPLICATE") for x in v)


def test_state_declared_not_in_taxonomy(tmp_path):
    root = make_payload(tmp_path)
    sm = root / "protocol" / ".agents" / "orchestrators" / "core" / "states" / "SAMPLE_STATE_MACHINE.md"
    sm.write_text(SM.replace("  - B\n", "  - B\n  - C\n"), encoding="utf-8")
    v = ctc.violations_for_root(root, root / "protocol")
    assert any("core:C" in x and "not a taxonomy state" in x for x in v)


def test_contract_produced_by_not_canonical(tmp_path):
    root = make_payload(tmp_path)
    ctr = root / "protocol" / ".agents" / "orchestrators" / "core" / "contracts" / "SAMPLE.md"
    ctr.write_text(CONTRACT.replace('"task_analyst"', '"bogus"'), encoding="utf-8")
    v = ctc.violations_for_root(root, root / "protocol")
    assert any("produced_by 'bogus' is not a canonical producer name" in x for x in v)


def test_contract_produced_by_state_rejected(tmp_path):
    root = make_payload(tmp_path)
    ctr = root / "protocol" / ".agents" / "orchestrators" / "core" / "contracts" / "SAMPLE.md"
    ctr.write_text(CONTRACT.replace('"task_analyst"', '"core:A"'), encoding="utf-8")
    v = ctc.violations_for_root(root, root / "protocol")
    assert any("produced_by 'core:A' is not a canonical producer name" in x for x in v)


def test_contract_missing_schema_version(tmp_path):
    root = make_payload(tmp_path)
    ctr = root / "protocol" / ".agents" / "orchestrators" / "core" / "contracts" / "SAMPLE.md"
    ctr.write_text(CONTRACT.replace('schema_version = "1.0.0"\n', ""), encoding="utf-8")
    v = ctc.violations_for_root(root, root / "protocol")
    assert any("missing schema_version" in x for x in v)


def test_contract_bad_schema_version(tmp_path):
    root = make_payload(tmp_path)
    ctr = root / "protocol" / ".agents" / "orchestrators" / "core" / "contracts" / "SAMPLE.md"
    ctr.write_text(CONTRACT.replace('"1.0.0"', '"banana"'), encoding="utf-8")
    v = ctc.violations_for_root(root, root / "protocol")
    assert any("schema_version 'banana' is not semver" in x for x in v)


def test_workflow_profile_not_canonical(tmp_path):
    root = make_payload(tmp_path)
    wf = root / "protocol" / ".agents" / "orchestrators" / "core" / "workflow" / "00-sample.md"
    wf.write_text(WF.replace("profile: null", "profile: bogus"), encoding="utf-8")
    v = ctc.violations_for_root(root, root / "protocol")
    assert any("profile 'bogus' is not a canonical worker/role name" in x for x in v)


def test_profile_catalog_missing_entity(tmp_path):
    root = make_payload(tmp_path)
    profiles = root / "protocol" / ".agents" / "roles" / "profiles"
    profiles.mkdir(parents=True)
    (profiles / "ghost.md").write_text("# Ghost\n", encoding="utf-8")
    v = ctc.violations_for_root(root, root / "protocol")
    assert any(
        "PROFILE .agents/roles/profiles/ghost.md has no taxonomy worker entity" in x
        for x in v
    )


def test_state_output_missing_from_workflow(tmp_path):
    root = make_payload(tmp_path)
    wf = root / "protocol" / ".agents" / "orchestrators" / "core" / "workflow" / "00-sample.md"
    wf.write_text(
        WF.replace("output_artifacts: [OUT_A.md]", "output_artifacts: []"),
        encoding="utf-8",
    )
    taxonomy = root / "protocol" / ".agents" / "standards" / "runtime" / "PROTOCOL_TAXONOMY.md"
    text = taxonomy.read_text(encoding="utf-8")
    text = text.replace(
        "    output_artifacts:\n      - OUT_A.md\n",
        "    output_artifacts: []\n",
    )
    taxonomy.write_text(text, encoding="utf-8")
    v = ctc.violations_for_root(root, root / "protocol")
    assert any("requires output OUT_A.md missing in workflow" in x for x in v)


def test_workflow_output_missing_from_state_machine(tmp_path):
    root = make_payload(tmp_path)
    sm = root / "protocol" / ".agents" / "orchestrators" / "core" / "states" / "SAMPLE_STATE_MACHINE.md"
    sm.write_text(SM.replace("OUT_A.md", "OUT_B.md"), encoding="utf-8")
    v = ctc.violations_for_root(root, root / "protocol")
    assert any("output_artifacts OUT_A.md missing in state machine" in x for x in v)
    assert any("requires output OUT_B.md missing in workflow" in x for x in v)


def test_output_order_prefixes_normalized(tmp_path):
    root = make_payload(tmp_path)
    sm = root / "protocol" / ".agents" / "orchestrators" / "core" / "states" / "SAMPLE_STATE_MACHINE.md"
    sm.write_text(
        SM.replace("<order>-OUT_A.md", "D<order>-OUT_A.md"),
        encoding="utf-8",
    )
    assert ctc.violations_for_root(root, root / "protocol") == []


def test_gate_source_not_policy_state(tmp_path):
    root = make_payload(tmp_path)
    pol = root / "protocol" / ".agents" / "orchestrators" / "core" / "harness" / "policies" / "H00-sample.md"
    pol.write_text(
        POLICY.replace(
            '  - "core:A -> core:B"',
            '  - "core:A -> core:B"\n  - "core:B -> core:A"',
        ),
        encoding="utf-8",
    )
    v = ctc.violations_for_root(root, root / "protocol")
    assert any("source core:B != policy state core:A" in x for x in v)


def test_transition_header_gate_missing(tmp_path):
    root = make_payload(tmp_path)
    pol = root / "protocol" / ".agents" / "orchestrators" / "core" / "harness" / "policies" / "H00-sample.md"
    pol.write_text(
        POLICY.replace('transition = "A -> B"', 'transition = "A -> B, C"'),
        encoding="utf-8",
    )
    v = ctc.violations_for_root(root, root / "protocol")
    assert any("transition header names A -> C missing from gates" in x for x in v)


def test_transition_header_dead_gate(tmp_path):
    root = make_payload(tmp_path)
    pol = root / "protocol" / ".agents" / "orchestrators" / "core" / "harness" / "policies" / "H00-sample.md"
    pol.write_text(
        POLICY.replace(
            '  - "core:A -> core:B"',
            '  - "core:A -> core:B"\n  - "core:A -> core:C"',
        ),
        encoding="utf-8",
    )
    v = ctc.violations_for_root(root, root / "protocol")
    assert any("gates core:A -> core:C not named in transition header" in x for x in v)
