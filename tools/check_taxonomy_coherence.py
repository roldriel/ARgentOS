#!/usr/bin/env python3
"""Verify mechanical coherence between PROTOCOL_TAXONOMY.md and the payload.

This dev-only checker restores, as a safety net, the invariants that the
former ``test_protocol_taxonomy.py`` enforced before it was removed (the
runtime still evaluates H13 by judgment; see
``protocol/.agents/harness/policies/H13-protocol-taxonomy.md``). It is not
part of the distributed protocol.

Checks:

1. No duplicate entity keys inside the taxonomy ``entities:`` block.
2. Every state declared by a state machine file (``states_defined`` +
   ``domain``) exists as a ``kind: state`` entity in the taxonomy.
3. Every workflow file's YAML front matter matches its taxonomy
   ``workflow:<basename>`` entity (H13 rule 10), and the workflow's
   ``next_states`` / ``previous_states`` are subsets of the taxonomy state's
   ``next`` / ``previous`` (H13 rule 2 — this catches e.g. a taxonomy
   ``core:RECOVERY.next`` that omits transitions the workflow already uses).
4. Every harness policy's YAML ``gates`` targets are in the taxonomy ``next``
   of the gate's source state, harness IDs are unique, and the taxonomy
   ``policy_file`` matches the file path.
5. Every contract entity's ``produced_by`` / ``consumed_by`` reference
   existing taxonomy states.
6. Every state is reachable within its domain (roots are states with no
   ``previous``; a domain with no root is checked for internal connectivity).

Usage:
  python tools/check_taxonomy_coherence.py [--root REPO_ROOT]
                                           [--payload PROTOCOL]

Exit code: 0 when all invariants hold, 1 otherwise.
Standard library only.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


def parse_simple_map(text: str) -> dict:
    """Parse a small YAML subset: scalar fields, inline lists, block lists."""
    data: dict = {}
    lines = text.splitlines()
    i = 0
    while i < len(lines):
        line = lines[i]
        if not line.strip() or line.lstrip().startswith("#"):
            i += 1
            continue
        m = re.match(r"^([A-Za-z0-9_.]+):\s*(.*)$", line)
        if not m:
            i += 1
            continue
        key, rest = m.group(1), m.group(2).strip()
        if rest:
            if rest.startswith("[") and rest.endswith("]"):
                inner = rest[1:-1].strip()
                data[key] = (
                    [strip_quotes(x.strip()) for x in inner.split(",")]
                    if inner
                    else []
                )
            else:
                data[key] = strip_quotes(rest)
            i += 1
            continue
        # Block list: following lines at deeper indentation, "- item".
        base = len(line) - len(line.lstrip(" "))
        items: list[str] = []
        i += 1
        while i < len(lines):
            nl = lines[i]
            if not nl.strip():
                i += 1
                continue
            ml = re.match(r"^(\s*)- (.+)$", nl)
            if ml and len(ml.group(1)) > base:
                items.append(strip_quotes(ml.group(2).strip()))
                i += 1
                continue
            break
        data[key] = items
    return data


def strip_quotes(value: str) -> str:
    value = value.strip()
    if len(value) >= 2 and value[0] == value[-1] and value[0] in "\"'":
        return value[1:-1]
    return value


def read_front_matter(text: str, after_toml: bool = False) -> dict:
    """Read the first YAML block of a payload document.

    Contracts and policies start with a ``+++`` TOML block followed by the
    YAML block; state machines and workflows start directly with ``---``.
    """
    if after_toml:
        marker = text.find("+++", 0)
        if marker == -1:
            # No TOML block: fall back to a plain YAML front matter
            # (e.g. the cross-cutting H13 policy).
            return read_front_matter(text, after_toml=False)
        end_toml = text.find("+++", marker + 3)
        if end_toml == -1:
            return {}
        head = text[end_toml + 3 :]
        start = head.find("---")
        if start == -1:
            return {}
        head = head[start:]
    else:
        head = text
        if not head.lstrip().startswith("---"):
            return {}
    lines = head.splitlines()
    # Skip the opening "---".
    body: list[str] = []
    seen_open = False
    for line in lines:
        stripped = line.strip()
        if not seen_open:
            if stripped == "---":
                seen_open = True
            continue
        if stripped == "---":
            break
        body.append(line)
    return parse_simple_map("\n".join(body))


def parse_taxonomy_entities(payload: Path) -> tuple[dict, list[str]]:
    """Return (entities dict, list of duplicate keys)."""
    taxonomy_file = (
        payload / ".agents" / "standards" / "runtime" / "PROTOCOL_TAXONOMY.md"
    )
    text = taxonomy_file.read_text(encoding="utf-8", errors="replace")
    fence = re.search(r"```yaml\n(.*?)\n```", text, re.DOTALL)
    if not fence:
        return {}, []
    lines = fence.group(1).splitlines()
    start = next(
        (i for i, l in enumerate(lines) if re.match(r"^entities:\s*$", l)),
        None,
    )
    if start is None:
        return {}, []
    entities: dict = {}
    duplicates: list[str] = []
    i = start + 1
    while i < len(lines):
        line = lines[i]
        if not line.strip() or line.lstrip().startswith("#"):
            i += 1
            continue
        m = re.match(r'^  ([^ ].*?):\s*$', line)
        if not m:
            i += 1
            continue
        key = strip_quotes(m.group(1))
        if key in entities:
            duplicates.append(key)
        i += 1
        entity: dict = {}
        while i < len(lines):
            inner = lines[i]
            if not inner.strip() or inner.lstrip().startswith("#"):
                i += 1
                continue
            if re.match(r"^  [^ ].*?:\s*$", inner):
                break
            if not inner.startswith("    "):
                break
            mi = re.match(r"^    ([A-Za-z0-9_.]+):\s*(.*)$", inner)
            if not mi:
                i += 1
                continue
            k, rest = mi.group(1), mi.group(2).strip()
            if rest:
                if rest.startswith("[") and rest.endswith("]"):
                    inner_list = rest[1:-1].strip()
                    entity[k] = (
                        [strip_quotes(x.strip()) for x in inner_list.split(",")]
                        if inner_list
                        else []
                    )
                else:
                    entity[k] = strip_quotes(rest)
                i += 1
            else:
                items: list[str] = []
                i += 1
                while i < len(lines):
                    ml = re.match(r"^      - (.+)$", lines[i])
                    if not ml:
                        break
                    items.append(strip_quotes(ml.group(1)))
                    i += 1
                entity[k] = items
        entities[key] = entity
    return entities, duplicates


def violations_for_root(
    root: Path, payload: Path
) -> list[str]:
    """Return a human-readable list of coherence violations."""
    out: list[str] = []
    entities, duplicates = parse_taxonomy_entities(payload)
    for key in duplicates:
        out.append(f"DUPLICATE taxonomy entity key: {key}")

    states = {
        key: ent
        for key, ent in entities.items()
        if ent.get("kind") == "state"
    }

    # 2. State machines declare states that exist in the taxonomy.
    state_machines = sorted(
        (payload / ".agents" / "orchestrators").rglob("states/*.md")
    )
    for sm in state_machines:
        fm = read_front_matter(sm.read_text(encoding="utf-8", errors="replace"))
        domain = fm.get("domain")
        for state in fm.get("states_defined", []):
            key = f"{domain}:{state}"
            if key not in states:
                out.append(
                    f"STATE {sm.relative_to(root)} declares {key} "
                    "which is not a taxonomy state"
                )

    # 3. Workflow front matter matches the taxonomy workflow entity.
    workflows = sorted(
        (payload / ".agents" / "orchestrators").rglob("workflow/*.md")
    )
    workflow_by_file = {
        ent.get("file"): key
        for key, ent in entities.items()
        if ent.get("kind") == "workflow"
    }
    for wf in workflows:
        if wf.name in ("INDEX.md", "README.md"):
            continue
        rel = wf.relative_to(payload).as_posix()
        fm = read_front_matter(wf.read_text(encoding="utf-8", errors="replace"))
        wf_key = workflow_by_file.get(rel)
        ent = entities.get(wf_key) if wf_key else None
        if ent is None:
            out.append(f"WORKFLOW {rel} has no taxonomy workflow entity")
            continue
        if ent.get("file") != rel:
            out.append(f"WORKFLOW {rel} taxonomy file field mismatch: {ent.get('file')}")
        if ent.get("domain") != fm.get("domain"):
            out.append(f"WORKFLOW {rel} domain mismatch (taxonomy {ent.get('domain')} vs file {fm.get('domain')})")
        state_key = f"{fm.get('domain')}:{fm.get('state')}"
        if ent.get("state") != state_key:
            out.append(f"WORKFLOW {rel} state mismatch (taxonomy {ent.get('state')} vs file {state_key})")
        for field in ("previous_states", "next_states", "input_artifacts", "output_artifacts", "harness"):
            if set(ent.get(field, [])) != set(fm.get(field, [])):
                out.append(
                    f"WORKFLOW {rel} {field} mismatch "
                    f"(taxonomy {sorted(ent.get(field, []))} vs file {sorted(fm.get(field, []))})"
                )
        if ent.get("actor") != fm.get("actor"):
            out.append(f"WORKFLOW {rel} actor mismatch")
        tax_state = states.get(state_key)
        if tax_state is not None:
            if not set(fm.get("next_states", [])).issubset(set(tax_state.get("next", []))):
                out.append(
                    f"WORKFLOW {rel} next_states not in taxonomy {state_key}.next: "
                    f"{sorted(set(fm.get('next_states', [])) - set(tax_state.get('next', [])))}"
                )
            if not set(fm.get("previous_states", [])).issubset(set(tax_state.get("previous", []))):
                out.append(
                    f"WORKFLOW {rel} previous_states not in taxonomy {state_key}.previous: "
                    f"{sorted(set(fm.get('previous_states', [])) - set(tax_state.get('previous', [])))}"
                )

    # 4. Harness policies: gates within taxonomy next, unique IDs, policy_file.
    policies = sorted(
        list((payload / ".agents" / "harness" / "policies").glob("*.md"))
        + list((payload / ".agents" / "orchestrators").rglob("harness/policies/*.md"))
    )
    seen_ids: set[str] = set()
    for policy in policies:
        rel = policy.relative_to(payload).as_posix()
        fm = read_front_matter(
            policy.read_text(encoding="utf-8", errors="replace"), after_toml=True
        )
        hid = fm.get("harness_id")
        if hid is None:
            continue  # not a harness policy YAML block
        if hid in seen_ids:
            out.append(f"POLICY {rel} duplicates harness_id {hid}")
        seen_ids.add(hid)
        key = f"{hid}-{fm.get('name', '')}"
        ent = entities.get(key)
        if ent is None:
            out.append(f"POLICY {rel} has no taxonomy harness entity {key}")
            continue
        if ent.get("policy_file") != rel:
            out.append(f"POLICY {rel} taxonomy policy_file mismatch: {ent.get('policy_file')}")
        for gate in fm.get("gates", []):
            m = re.match(r"^([^ ]+) -> ([^ ]+)$", gate)
            if not m:
                out.append(f"POLICY {rel} unparsable gate: {gate}")
                continue
            src, dst = m.group(1), m.group(2)
            src_ent = states.get(src)
            if src_ent is None:
                out.append(f"POLICY {rel} gate source not a taxonomy state: {src}")
            elif dst not in src_ent.get("next", []):
                out.append(
                    f"POLICY {rel} gate {gate} target not in taxonomy {src}.next"
                )

    # 5. Contract produced_by / consumed_by reference existing states.
    for key, ent in entities.items():
        if ent.get("kind") != "contract":
            continue
        for field in ("produced_by", "consumed_by"):
            for ref in ent.get(field, []):
                if ref not in states:
                    out.append(
                        f"CONTRACT {key} {field} references unknown state: {ref}"
                    )

    # 6. Reachability per domain.
    by_domain: dict[str, list[str]] = {}
    for key, ent in states.items():
        by_domain.setdefault(ent.get("domain", "?"), []).append(key)
    for domain, keys in by_domain.items():
        roots = [k for k in keys if not states[k].get("previous")]
        if roots:
            frontier = list(roots)
            seen = set(frontier)
            while frontier:
                cur = frontier.pop()
                for nxt in states[cur].get("next", []):
                    if nxt in states and nxt not in seen:
                        seen.add(nxt)
                        frontier.append(nxt)
            unreachable = sorted(set(keys) - seen)
            if unreachable:
                out.append(
                    f"STATE domain {domain} has unreachable states: {unreachable}"
                )
        else:
            # No root in the domain: verify internal connectivity only.
            seen: set[str] = set()
            for k in keys:
                if k in seen:
                    continue
                frontier = [k]
                component: set[str] = set()
                while frontier:
                    cur = frontier.pop()
                    if cur in component:
                        continue
                    component.add(cur)
                    for nxt in states[cur].get("next", []):
                        if nxt in states and nxt not in component:
                            frontier.append(nxt)
                seen |= component
            if seen != set(keys):
                out.append(
                    f"STATE domain {domain} has isolated components: "
                    f"{sorted(set(keys) - seen)}"
                )
    return out


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--root", type=Path, default=None)
    parser.add_argument("--payload", type=Path, default=Path("protocol"))
    args = parser.parse_args(argv)
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    root = (args.root or Path(__file__).resolve().parents[1]).resolve()
    payload = (root / args.payload).resolve()
    violations = violations_for_root(root, payload)
    if not violations:
        print("Taxonomy coherence OK.")
        return 0
    print(f"Taxonomy coherence violations: {len(violations)}")
    for v in violations:
        print(f"- {v}")
    return 1


if __name__ == "__main__":
    sys.exit(main())
