#!/usr/bin/env python3
"""Optional structural validator for harness gate checklists (RFC-57).

Implements the structurally checkable subset of the harness policies'
``[gate]`` items as a pure-stdlib CLI. For the supported triggers (H00-H07,
H09-H11, D00) the policies require the Orchestrator to run it before judging
PASS; a structural FAIL blocks PASS unless recorded as a documented deviation
(see ``.agents/harness/INDEX.md``, §Enforcement model). The validator is never
invoked by the hooks and never blocks at the environment level. Its results
may be recorded in ``HARNESS_REPORT.md`` as evidence.

Supported triggers (structural subset): H00-H07, H09-H11, D00. D01 (KB ground
truth) and S00 (probe) are not covered by design.

Checks per trigger:
- artifact existence;
- required normative sections of the contract;
- machine-readable TOML blocks (parseable, required keys, enum values);
- citation resolution (``path:section``, ``path`` §section, TOML citation
  fields) against the project and session roots;
- EARS pattern of acceptance-criteria bullets (H01);
- structural presence of ``## Rubric Evaluation`` (H06, when the ``rubrics``
  flag is enabled).

Usage:
  python .agents/harness/gate_validator.py --trigger <HXX> --artifact <path>
  python .agents/harness/gate_validator.py --list

Exit code: 0 when every check PASSes (or is SKIPPED), 1 when any check FAILs,
2 on usage errors. Standard library only.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path


KNOWN_TECH_PRACTICES = {
    "tdd",
    "srp",
    "ocp",
    "lsp",
    "isp",
    "dip",
    "screaming_architecture",
    "clean_architecture",
    "layered_architecture",
    "dry",
    "grasp",
    "ddd_tactical",
    "ddd_strategic",
}

BASE_RUBRICS = (
    "TASK_SPECIFICATION_RUBRIC",
    "CONTEXT_ARTIFACT_RUBRIC",
    "CONTEXT_VALIDATION_REPORT_RUBRIC",
    "EXECUTION_PLAN_RUBRIC",
    "EXECUTION_SUMMARY_RUBRIC",
    "VERIFICATION_REPORT_RUBRIC",
)

TRIGGERS = {
    "H00": {
        "artifact": "TASK_ANALYSIS.md",
        "sections": [
            "Metadata", "User Request", "Interpreted Objective", "Expected Outcome",
            "Explicit Requirements", "Explicit Restrictions", "Detected Ambiguities",
            "Intent Confidence Assessment", "Sufficiency Assessment",
            "Recommended Next State", "Confidence", "Task Profile",
        ],
    },
    "H01": {
        "artifact": "TASK_SPECIFICATION.md",
        "sections": [
            "Objective", "Expected Outcome", "Scope", "Constraints",
            "Acceptance Criteria", "Assumptions", "Unknowns", "Validation",
        ],
        "ears": True,
        "technical_approach": True,
    },
    "H02": {
        "artifact": "CONTEXT_ARTIFACT.md",
        "sections": [
            "Metadata", "Task Reference", "Context Objective", "Project Context",
            "Relevant Components", "Existing Behavior", "Dependencies",
            "Constraints Discovered", "Available Evidence", "Unknowns",
            "Context Validation", "State",
        ],
    },
    "H03": {
        "artifact": "CONTEXT_VALIDATION_REPORT.md",
        "sections": [
            "Metadata", "Context Reference", "Validation Objective",
            "Completeness Evaluation", "Relevance Evaluation",
            "Consistency Evaluation", "Risk Evaluation", "Validation Decision",
            "Required Actions", "Confidence", "State Transition",
        ],
    },
    "H04": {
        "artifact": "EXECUTION_PLAN.md",
        "sections": [
            "Metadata", "Task Reference", "Context Reference", "Objective",
            "Approach Summary", "Technical Approach", "Implementation Steps",
            "Affected Components", "Dependencies", "Risks", "Validation Strategy",
            "Rollback Considerations", "Plan Decision", "State Transition",
        ],
    },
    "H05": {
        "artifact": "EXECUTION_SUMMARY.md",
        "sections": [
            "Metadata", "Task Reference", "Execution Plan Reference",
            "Summary of Changes", "Steps Executed", "Project Files Modified",
            "Intermediate Validations", "Issues or Deviations",
            "Final Project State", "Confidence",
        ],
        "toml": ["final_state", "steps_executed"],
    },
    "H06": {
        "artifact": "VERIFICATION_REPORT.md",
        "sections": [
            "Metadata", "Task Reference", "Execution Plan Reference",
            "Verification Objective", "Acceptance Criteria Evaluation",
            "Test Results", "Issues Found", "Final Decision", "Confidence",
            "State Transition",
        ],
        "toml": ["decision", "acceptance_criteria"],
        "rubrics": True,
    },
    "H07": {
        "artifact": "VERIFICATION_REPORT.md",
        "sections": ["Scope Compliance"],
        "toml": ["scope_compliance"],
    },
    "H09": {
        "artifact": "RECOVERY_REPORT.md",
        "sections": [
            "Metadata", "Failure Reference", "Failure Summary",
            "Root Cause Classification", "Analysis Summary",
            "Corrective Action Recommendation", "Updated Artifacts", "Confidence",
        ],
    },
    "H10": {
        "artifact": "KB_RECOMMENDATION.md",
        "sections": [
            "Discovery Objective", "Recommended Entries",
            "Context Budget Recommendation", "Notes",
        ],
    },
    "H11": {
        "artifact": "INTENT_REFLECTION.md",
        "sections": [
            "Metadata", "Original Request", "Detected Intent", "Reflection",
            "Confidence", "Correction Cycle", "User Response", "Next State",
        ],
    },
    "D00": {
        "artifact": "KB_DISCOVERY_REPORT.md",
        "sections": [
            "Discovery Objective", "Scope and Inputs", "Invalidation Summary",
            "Selected Workers", "Notes",
        ],
    },
}

EARS_RE = re.compile(
    r"^(?:"
    r"The .+ shall .+"
    r"|When .+, the .+ shall .+"
    r"|While .+, the .+ shall .+"
    r"|If .+, then the .+ shall .+"
    r"|Where .+, the .+ shall .+"
    r")$"
)

HEADING_RE = re.compile(r"^##\s+(.+?)\s*#*\s*$", re.MULTILINE)
HEADING_ANY_RE = re.compile(r"^#{1,6}\s+(.+?)\s*#*\s*$", re.MULTILINE)


def _normalize(value: str) -> str:
    return re.sub(r"[.!:]+$", "", value.strip().strip("`")).casefold()


def headings_of(text: str) -> set[str]:
    return {_normalize(m.group(1)) for m in HEADING_ANY_RE.finditer(text)}


def parse_toml_value(raw: str):
    raw = raw.strip()
    if raw.startswith('"') and raw.endswith('"'):
        return raw[1:-1]
    if raw in ("true", "false"):
        return raw == "true"
    if raw.startswith("[") and raw.endswith("]"):
        inner = raw[1:-1].strip()
        if not inner:
            return []
        return [parse_toml_value(x.strip()) for x in inner.split(",")]
    try:
        return int(raw)
    except ValueError:
        pass
    try:
        return float(raw)
    except ValueError:
        return raw


def parse_toml(text: str) -> dict:
    """Parse a minimal TOML subset: [table], [[array]], key = value."""
    result: dict = {}
    current = None
    for line in text.splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        m = re.match(r"^\[\[([^\]]+)\]\]$", line)
        if m:
            key = m.group(1)
            result.setdefault(key, [])
            result[key].append({})
            current = result[key][-1]
            continue
        m = re.match(r"^\[([^\]]+)\]$", line)
        if m:
            key = m.group(1)
            result[key] = {}
            current = result[key]
            continue
        m = re.match(r"^([A-Za-z0-9_]+)\s*=\s*(.+)$", line)
        if m and current is not None:
            current[m.group(1)] = parse_toml_value(m.group(2))
    return result


def section_text(text: str, heading: str) -> str:
    """Return the text under a ``## <heading>`` section, until the next ``##``."""
    lines = text.splitlines()
    start = None
    for i, line in enumerate(lines):
        if HEADING_RE.match(line) and _normalize(HEADING_RE.match(line).group(1)) == _normalize(heading):
            start = i
            break
    if start is None:
        return ""
    body = []
    for line in lines[start + 1 :]:
        if HEADING_RE.match(line):
            break
        body.append(line)
    return "\n".join(body)


def toml_blocks(text: str) -> list[str]:
    return [m.group(1) for m in re.finditer(r"```toml\n(.*?)\n```", text, re.DOTALL)]


def features(root: Path) -> dict:
    """Read .agents/features.toml boolean flags (best-effort)."""
    data: dict = {}
    path = root / ".agents" / "features.toml"
    if path.is_file():
        for line in path.read_text(encoding="utf-8", errors="replace").splitlines():
            m = re.match(r"^\s*([A-Za-z0-9_]+)\s*=\s*(true|false)\s*$", line)
            if m:
                data[m.group(1)] = m.group(2) == "true"
    return data


def _roots_from_artifact(artifact: Path) -> tuple[Path, Path | None, list[Path]]:
    """Return (project root, session dir, iteration dirs) for citation checks."""
    resolved = artifact.resolve()
    parts = resolved.parts
    try:
        idx = parts.index(".project")
    except ValueError:
        return resolved.anchor or resolved.parent, None, []
    project = Path(*parts[:idx])
    session = None
    iterations: list[Path] = []
    if len(parts) > idx + 1:
        session = project / ".project" / parts[idx + 1]
        for candidate in sorted(session.iterdir()) if session.is_dir() else []:
            if candidate.is_dir() and re.fullmatch(r"\d+", candidate.name):
                iterations.append(candidate)
    return project, session, iterations


def citation_targets(text: str) -> list[tuple[str, str | None]]:
    """Extract (path, section) citation candidates from artifact prose."""
    targets: list[tuple[str, str | None]] = []
    for m in re.finditer(r"`([^`]+)`\s*§\s*([\w .-]+)", text):
        targets.append((m.group(1).strip(), m.group(2).strip()))
    for m in re.finditer(r"`([^`]+)`:\s*([\w .-]+)", text):
        path, section = m.group(1).strip(), m.group(2).strip()
        if "/" in path or path.lower().endswith((".md", ".py", ".toml", ".json")):
            targets.append((path, section))
    for block in toml_blocks(text):
        parsed = parse_toml(block)
        for table in parsed.values():
            if isinstance(table, dict):
                for key in ("specification", "execution_plan", "artifact", "validation_report"):
                    value = table.get(key)
                    if isinstance(value, str) and value:
                        targets.append((value, None))
    return targets


def citation_resolves(path: str, section: str | None, roots: tuple) -> bool:
    if "<" in path or ">" in path:
        return True  # placeholder
    fp = path.replace("\\", "/")
    project, session, iterations = roots
    candidates = []
    if fp.startswith("/"):
        candidates.append(Path(fp))
    else:
        base_dirs = [project] if project else []
        if session:
            base_dirs.append(session)
        base_dirs.extend(iterations)
        for base in base_dirs:
            candidates.append(base / fp)
    for candidate in candidates:
        if candidate.is_file():
            if section is None:
                return True
            if re.fullmatch(r"[\d.,\s-]+", section):
                return True
            text = candidate.read_text(encoding="utf-8", errors="replace")
            if _normalize(section) in headings_of(text):
                return True
    return False


def check_citations(text: str, roots: tuple) -> list[dict]:
    checks: list[dict] = []
    targets = citation_targets(text)
    if not targets:
        checks.append({"id": "citations", "result": "SKIP", "evidence": "no citations found"})
        return checks
    failed = 0
    for path, section in targets:
        if not citation_resolves(path, section, roots):
            failed += 1
            checks.append(
                {"id": "citation", "result": "FAIL",
                 "evidence": f"broken citation {path!r} section={section!r}"}
            )
            if failed >= 10:
                break
    if failed == 0:
        checks.append({"id": "citations", "result": "PASS", "evidence": f"{len(targets)} citations resolved"})
    return checks


def validate(trigger: str, artifact: Path, root: Path | None = None) -> tuple[list[dict], str]:
    """Run the structural checks for a trigger on an artifact.

    Returns (checks, decision) where decision is PASS or FAIL.
    """
    spec = TRIGGERS.get(trigger)
    if spec is None:
        raise ValueError(f"unsupported trigger: {trigger}")
    checks: list[dict] = []
    if not artifact.is_file():
        checks.append({"id": "existence", "result": "FAIL", "evidence": "artifact does not exist"})
        return checks, "FAIL"
    checks.append({"id": "existence", "result": "PASS", "evidence": str(artifact)})

    text = artifact.read_text(encoding="utf-8", errors="replace")
    headings = headings_of(text)
    for section in spec.get("sections", []):
        if _normalize(section) not in headings:
            checks.append(
                {"id": "section", "result": "FAIL", "evidence": f"missing section: {section}"}
            )
        else:
            checks.append({"id": "section", "result": "PASS", "evidence": f"section present: {section}"})

    if spec.get("ears"):
        body = section_text(text, "Acceptance Criteria")
        bullets = [
            line.lstrip("-* ").strip()
            for line in body.splitlines()
            if line.strip().startswith(("-", "*"))
        ]
        if not bullets:
            checks.append({"id": "ears", "result": "FAIL", "evidence": "no acceptance-criteria bullets"})
        else:
            bad = [b for b in bullets if not EARS_RE.match(b)]
            if bad:
                checks.append(
                    {"id": "ears", "result": "FAIL",
                     "evidence": f"{len(bad)} bullets do not match EARS: {bad[:2]}"}
                )
            else:
                checks.append({"id": "ears", "result": "PASS", "evidence": f"{len(bullets)} EARS bullets"})

    if spec.get("technical_approach"):
        body = section_text(text, "Technical Approach")
        enabled = []
        for block in toml_blocks(body):
            parsed = parse_toml(block)
            value = parsed.get("technical_approach", {}).get("enabled", [])
            if isinstance(value, list):
                enabled.extend(value)
        unknown = [p for p in enabled if p not in KNOWN_TECH_PRACTICES]
        if unknown:
            checks.append(
                {"id": "technical_approach", "result": "FAIL",
                 "evidence": f"unknown technical practices: {unknown}"}
            )
        else:
            checks.append(
                {"id": "technical_approach", "result": "PASS",
                 "evidence": f"{len(enabled)} known technical practices"}
            )

    for toml_key in spec.get("toml", []):
        checks.extend(_check_toml(toml_key, text))

    if spec.get("rubrics"):
        flags = features(root or Path(__file__).resolve().parents[2])
        if flags.get("rubrics", True):
            checks.extend(_check_rubrics(text))
        else:
            checks.append({"id": "rubrics", "result": "SKIP", "evidence": "rubrics flag disabled"})

    roots = _roots_from_artifact(artifact) if root is None else (root, None, [])
    checks.extend(check_citations(text, roots))

    failed = any(c["result"] == "FAIL" for c in checks)
    return checks, ("FAIL" if failed else "PASS")


def _check_toml(toml_key: str, text: str) -> list[dict]:
    checks: list[dict] = []
    found = False
    for block in toml_blocks(text):
        parsed = parse_toml(block)
        if toml_key not in parsed:
            continue
        found = True
        value = parsed[toml_key]
        if toml_key == "final_state":
            status = value.get("status")
            if status not in ("VERIFIABLE", "BLOCKED"):
                checks.append({"id": "final_state", "result": "FAIL",
                               "evidence": f"bad status {status!r}"})
            elif status == "BLOCKED":
                checks.append({"id": "final_state", "result": "FAIL",
                               "evidence": "status BLOCKED (gate requires VERIFIABLE)"})
            else:
                checks.append({"id": "final_state", "result": "PASS", "evidence": "status VERIFIABLE"})
        elif toml_key == "steps_executed":
            if not isinstance(value, list):
                checks.append({"id": "steps_executed", "result": "FAIL",
                               "evidence": "steps_executed is not a list"})
                continue
            bad = []
            for step in value:
                if not isinstance(step, dict):
                    bad.append("non-object step")
                    continue
                status = step.get("status")
                if status not in ("COMPLETED", "SKIPPED", "BLOCKED"):
                    bad.append(f"bad step status {status!r}")
                elif status == "BLOCKED":
                    bad.append("step BLOCKED")
                elif status == "SKIPPED" and not step.get("notes"):
                    bad.append("SKIPPED step without notes")
            if bad:
                checks.append({"id": "steps_executed", "result": "FAIL",
                               "evidence": f"{len(bad)} offending step(s)"})
            else:
                checks.append({"id": "steps_executed", "result": "PASS",
                               "evidence": f"{len(value)} valid step(s)"})
        elif toml_key == "decision":
            result = value.get("result")
            if result not in ("COMPLETED", "RECOVERY"):
                checks.append({"id": "decision", "result": "FAIL",
                               "evidence": f"bad decision.result {result!r}"})
            else:
                checks.append({"id": "decision", "result": "PASS",
                               "evidence": f"decision.result {result}"})
        elif toml_key == "acceptance_criteria":
            if not isinstance(value, list):
                checks.append({"id": "acceptance_criteria", "result": "FAIL",
                               "evidence": "acceptance_criteria is not a list"})
                continue
            bad = []
            for criterion in value:
                if not isinstance(criterion, dict):
                    bad.append("non-object criterion")
                    continue
                result = criterion.get("result")
                if result not in ("PASS", "FAIL", "PARTIAL"):
                    bad.append(f"bad criterion result {result!r}")
                elif result == "PARTIAL" and not criterion.get("action_plan"):
                    bad.append("PARTIAL criterion without action_plan")
            if bad:
                checks.append({"id": "acceptance_criteria", "result": "FAIL",
                               "evidence": f"{len(bad)} offending criterion/criteria"})
            else:
                checks.append({"id": "acceptance_criteria", "result": "PASS",
                               "evidence": f"{len(value)} valid criterion/criteria"})
        elif toml_key == "scope_compliance":
            respected = value.get("scope_respected")
            unplanned = value.get("unplanned_changes", [])
            authorized = value.get("user_authorized_extra_work", False)
            if respected is None:
                checks.append({"id": "scope_compliance", "result": "FAIL",
                               "evidence": "missing scope_respected"})
            elif not isinstance(unplanned, list):
                checks.append({"id": "scope_compliance", "result": "FAIL",
                               "evidence": "unplanned_changes is not a list"})
            elif not respected and authorized:
                checks.append({"id": "scope_compliance", "result": "FAIL",
                               "evidence": "scope_respected=false with user_authorized_extra_work=true"})
            elif respected and unplanned and not authorized:
                checks.append({"id": "scope_compliance", "result": "FAIL",
                               "evidence": "unplanned changes without user authorization (Branch A/B incoherent)"})
            else:
                checks.append({"id": "scope_compliance", "result": "PASS",
                               "evidence": "scope branch coherent"})
    if not found:
        checks.append({"id": toml_key, "result": "FAIL",
                       "evidence": f"no parseable TOML block with [{toml_key}]"})
    return checks


def _check_rubrics(text: str) -> list[dict]:
    checks: list[dict] = []
    body = section_text(text, "Rubric Evaluation")
    if not body.strip():
        checks.append({"id": "rubrics", "result": "FAIL", "evidence": "missing ## Rubric Evaluation"})
        return checks
    present = set(re.findall(r"^###\s+(.+?)\s*$", body, re.MULTILINE))
    missing = [r for r in BASE_RUBRICS if r not in present]
    if missing:
        checks.append({"id": "rubrics", "result": "FAIL",
                       "evidence": f"missing base rubrics: {missing}"})
    for name in present:
        sub = _subsection_text(body, name)
        level = re.search(r"^\s*(?:[-*]\s*)?Level:\s*(.+)$", sub, re.MULTILINE)
        evidence = re.search(r"^\s*(?:[-*]\s*)?Evidence:\s*(.+)$", sub, re.MULTILINE)
        if not level or level.group(1).strip() not in ("INSUFFICIENT", "MEETS", "EXCEEDS"):
            checks.append({"id": "rubric_level", "result": "FAIL",
                           "evidence": f"{name}: missing/invalid Level line"})
        if not evidence or not evidence.group(1).strip():
            checks.append({"id": "rubric_evidence", "result": "FAIL",
                           "evidence": f"{name}: missing/non-empty Evidence line"})
    if not missing and not any(
        c["id"] in ("rubric_level", "rubric_evidence") and c["result"] == "FAIL" for c in checks
    ):
        checks.append({"id": "rubrics", "result": "PASS",
                       "evidence": f"{len(present)} rubric subsections structurally valid"})
    return checks


def _subsection_text(body: str, name: str) -> str:
    lines = body.splitlines()
    start = None
    pattern = re.compile(r"^###\s+" + re.escape(name) + r"\s*$")
    for i, line in enumerate(lines):
        if pattern.match(line.strip()):
            start = i
            break
    if start is None:
        return ""
    out = []
    for line in lines[start + 1 :]:
        if line.strip().startswith("###"):
            break
        out.append(line)
    return "\n".join(out)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--trigger", help="harness trigger id (e.g. H01)")
    parser.add_argument("--artifact", type=Path, help="path to the artifact to validate")
    parser.add_argument("--root", type=Path, default=None, help="project root override")
    parser.add_argument("--list", action="store_true", help="list supported triggers")
    args = parser.parse_args(argv)
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    if args.list:
        rows = []
        for trigger, spec in TRIGGERS.items():
            rows.append(
                f"{trigger} -> {spec['artifact']} "
                f"({len(spec.get('sections', []))} sections)"
            )
        print("\n".join(rows))
        return 0
    if not args.trigger or not args.artifact:
        print("usage: gate_validator.py --trigger <HXX> --artifact <path>", file=sys.stderr)
        return 2
    try:
        checks, decision = validate(args.trigger, args.artifact, args.root)
    except ValueError as exc:
        print(f"gate_validator: error: {exc}", file=sys.stderr)
        return 2
    print(json.dumps(
        {"trigger": args.trigger, "artifact": str(args.artifact), "decision": decision, "checks": checks},
        indent=2,
        ensure_ascii=False,
    ))
    return 0 if decision == "PASS" else 1


if __name__ == "__main__":
    sys.exit(main())
