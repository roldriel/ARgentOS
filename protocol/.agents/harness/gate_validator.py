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
- profile-aware H04: for `trivial`-profile tasks the `Context Reference`
  section is not required (the EXECUTION_PLAN contract omits it in the reduced
  cycle); the profile is read from the session's TASK_ANALYSIS.md;
- machine-readable TOML blocks (parseable, required keys, enum values);
- citation resolution (``path:section``, ``path`` §section, TOML citation
  fields) against the project and session roots;
- EARS pattern of acceptance-criteria bullets (H01);
- structural presence of ``## Rubric Evaluation`` (H06, when the ``rubrics``
  flag is enabled);
- section-coherence conflicts (H00: sufficiency/next-state and HIGH-intent
  contradictions; H03: VALIDATED decision with INCOMPLETE/CONFLICTING
  evaluations);
- profile-aware review gate (H06: a `complex` task requires a
  ``REVIEW_REPORT.md`` in the iteration) and the ``Deferred Items`` TOML
  structure when present (H06);
- evidence model (H06: ``[[evidence]]`` entries with ``class``/``claim_id``/
  ``ref`` and the VERIFIED rule — every PASS claim needs non-attestation
  evidence or an explicit ``claim_class``).

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

_PROFILE_SECTION_RE = re.compile(
    r"^##\s+Task Profile\s*\n(.*?)(?=^##\s|\Z)", re.MULTILINE | re.DOTALL
)
_PROFILE_VALUE_RE = re.compile(r'^\s*value\s*=\s*"([^"]+)"', re.MULTILINE)
_VALID_PROFILES = ("trivial", "standard", "complex")

BASE_RUBRICS = (
    "TASK_SPECIFICATION_RUBRIC",
    "CONTEXT_ARTIFACT_RUBRIC",
    "CONTEXT_VALIDATION_REPORT_RUBRIC",
    "EXECUTION_PLAN_RUBRIC",
    "EXECUTION_SUMMARY_RUBRIC",
    "VERIFICATION_REPORT_RUBRIC",
)

EVIDENCE_CLASSES = {
    "observation",
    "measurement",
    "attestation",
    "assertion",
    "reference",
}

NON_ATTESTATION_EVIDENCE = EVIDENCE_CLASSES - {"attestation"}

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
            "Context Validation",
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


def read_task_profile(iterations: list[Path]) -> str | None:
    """Return the task profile declared in the session's TASK_ANALYSIS.md.

    Searches the session iteration directories (highest iteration wins) for a
    file ending in ``TASK_ANALYSIS.md`` and reads the ``value`` key of its
    ``Task Profile`` section. Returns None when the profile cannot be
    determined; H04 then applies the standard (full) section set.
    """
    for iter_dir in reversed(iterations):
        candidates = sorted(iter_dir.glob("*TASK_ANALYSIS.md"))
        if not candidates:
            continue
        try:
            content = candidates[-1].read_text(encoding="utf-8")
        except OSError:
            continue
        section = _PROFILE_SECTION_RE.search(content)
        if not section:
            continue
        match = _PROFILE_VALUE_RE.search(section.group(1))
        if match and match.group(1) in _VALID_PROFILES:
            return match.group(1)
    return None


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
    sections = list(spec.get("sections", []))
    if trigger == "H04" and read_task_profile(_roots_from_artifact(artifact)[2]) == "trivial":
        sections = [s for s in sections if s != "Context Reference"]
        checks.append(
            {
                "id": "profile",
                "result": "PASS",
                "evidence": (
                    "trivial task profile: Context Reference omitted per the "
                    "EXECUTION_PLAN.md contract"
                ),
            }
        )
    for section in sections:
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

    if trigger == "H00":
        checks.extend(_check_h00_conflicts(text))

    if trigger == "H03":
        checks.extend(_check_h03_conflicts(text))

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
    if trigger == "H06":
        checks.extend(_check_test_results(text, roots))
        checks.extend(_check_deferred_items(text))
        checks.append(_check_review_report(artifact))
        checks.extend(_check_evidence(text))
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
            evidence_entries = _evidence_entries(text)
            for criterion in value:
                if not isinstance(criterion, dict):
                    bad.append("non-object criterion")
                    continue
                result = criterion.get("result")
                if result not in ("PASS", "FAIL", "PARTIAL"):
                    bad.append(f"bad criterion result {result!r}")
                    continue
                elif result == "PARTIAL" and not criterion.get("action_plan"):
                    bad.append("PARTIAL criterion without action_plan")
                if result == "FAIL":
                    continue
                claim_class = criterion.get("claim_class")
                evidence = criterion.get("evidence")
                claims_verified = claim_class == "verified" or (
                    claim_class is None
                    and isinstance(evidence, str)
                    and bool(evidence.strip())
                )
                if claim_class is None and not claims_verified:
                    bad.append("criterion without evidence and without claim_class")
                elif claims_verified and not _has_non_attestation_evidence(
                    evidence_entries, criterion.get("claim_id")
                ):
                    bad.append(
                        "verified criterion without non-attestation evidence"
                    )
            if bad:
                checks.append({"id": "acceptance_criteria", "result": "FAIL",
                               "evidence": "; ".join(bad[:5])})
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


def _evidence_resolves(evidence: str, roots: tuple) -> bool:
    """True when an evidence path resolves to an existing file."""
    if not evidence.strip() or "<" in evidence or ">" in evidence:
        return False
    fp = evidence.replace("\\", "/")
    project, session, iterations = roots
    candidates = []
    if Path(fp).is_absolute():
        candidates.append(Path(fp))
    else:
        base_dirs = [project] if project else []
        if session:
            base_dirs.append(session)
        base_dirs.extend(iterations)
        for base in base_dirs:
            candidates.append(base / fp)
    return any(c.is_file() for c in candidates)


def _evidence_entries(text: str) -> list[dict]:
    """Collect ``[[evidence]]`` entries from the ``## Evidence`` section."""
    body = section_text(text, "Evidence")
    entries: list[dict] = []
    for block in toml_blocks(body):
        parsed = parse_toml(block)
        value = parsed.get("evidence")
        if isinstance(value, list):
            entries.extend(x for x in value if isinstance(x, dict))
    return entries


def _has_non_attestation_evidence(entries: list[dict], claim_id: object) -> bool:
    """True when an evidence entry supports the claim with class != attestation."""
    return any(
        e.get("class") in NON_ATTESTATION_EVIDENCE and e.get("claim_id") == claim_id
        for e in entries
    )


def _check_evidence(text: str) -> list[dict]:
    """H06: validate the ``[[evidence]]`` entries of ``## Evidence``."""
    entries = _evidence_entries(text)
    if not entries:
        return [
            {
                "id": "evidence",
                "result": "SKIP",
                "evidence": "no [[evidence]] entries",
            }
        ]
    bad: list[str] = []
    for i, entry in enumerate(entries, 1):
        cls = entry.get("class")
        if cls not in EVIDENCE_CLASSES:
            bad.append(f"entry {i}: bad class {cls!r}")
        claim_id = entry.get("claim_id")
        if not isinstance(claim_id, str) or not claim_id.strip():
            bad.append(f"entry {i}: missing claim_id")
        ref = entry.get("ref")
        if not isinstance(ref, str) or not ref.strip():
            bad.append(f"entry {i}: missing ref")
        if cls == "measurement":
            exit_code = entry.get("exit_code")
            if exit_code is not None and (
                not isinstance(exit_code, int) or exit_code < 0
            ):
                bad.append(
                    f"entry {i}: measurement exit_code must be a non-negative integer"
                )
        if cls == "attestation":
            actor = entry.get("actor")
            statement = entry.get("statement")
            if not isinstance(actor, str) or not actor.strip():
                bad.append(f"entry {i}: attestation missing actor")
            if not isinstance(statement, str) or not statement.strip():
                bad.append(f"entry {i}: attestation missing statement")
    if bad:
        return [
            {
                "id": "evidence",
                "result": "FAIL",
                "evidence": "; ".join(bad[:5]),
            }
        ]
    return [
        {
            "id": "evidence",
            "result": "PASS",
            "evidence": f"{len(entries)} valid evidence entr(y/ies)",
        }
    ]


def _check_test_results(text: str, roots: tuple) -> list[dict]:
    """Validate the test_results TOML block of H06 (VERIFICATION_REPORT.md).

    Per the contract (3.21.0) and H06 §Gate Checklist item 7: a result other
    than SKIPPED must either declare an ``evidence`` that resolves to an
    existing file, or its ``test`` command string must appear in the session's
    SESSION_LOG.md. When no ``[[test_results]]`` block exists the check is SKIP
    (compatible with prior artifacts that predate the block).
    """
    blocks: list[dict] = []
    for block in toml_blocks(text):
        parsed = parse_toml(block)
        value = parsed.get("test_results")
        if isinstance(value, list):
            blocks.extend(x for x in value if isinstance(x, dict))
    if not blocks:
        return [
            {
                "id": "test_results",
                "result": "SKIP",
                "evidence": "no test_results TOML block",
            }
        ]
    project, session, _ = roots
    log_text = ""
    if session is not None:
        log = session / "SESSION_LOG.md"
        if log.is_file():
            try:
                log_text = log.read_text(encoding="utf-8", errors="replace")
            except OSError:
                log_text = ""
    bad: list[str] = []
    for i, entry in enumerate(blocks, 1):
        result = entry.get("result")
        if result not in ("PASS", "FAIL", "SKIPPED"):
            bad.append(f"entry {i}: bad result {result!r}")
            continue
        if result == "SKIPPED":
            continue
        evidence = entry.get("evidence")
        test = entry.get("test", "")
        if evidence:
            if not _evidence_resolves(str(evidence), roots):
                bad.append(f"entry {i}: evidence does not resolve to an existing file")
        elif not (isinstance(test, str) and test and test in log_text):
            bad.append(f"entry {i}: no evidence and test command not found in SESSION_LOG.md")
        claim_class = entry.get("claim_class")
        claims_verified = claim_class == "verified" or (
            claim_class is None
            and isinstance(evidence, str)
            and bool(evidence.strip())
        )
        if claim_class is None and not claims_verified:
            bad.append(f"entry {i}: result without evidence and without claim_class")
        elif claims_verified and not _has_non_attestation_evidence(
            _evidence_entries(text), entry.get("claim_id")
        ):
            bad.append(
                f"entry {i}: verified result without non-attestation evidence"
            )
    if bad:
        return [
            {
                "id": "test_results",
                "result": "FAIL",
                "evidence": "; ".join(bad[:5]),
            }
        ]
    return [
        {
            "id": "test_results",
            "result": "PASS",
            "evidence": f"{len(blocks)} valid test result(s)",
        }
    ]


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


def _h00_next_state(text: str) -> str | None:
    """Return the declared ``recommended_next_state`` of a TASK_ANALYSIS."""
    body = section_text(text, "Recommended Next State")
    m = re.search(r'^\s*recommended_next_state\s*=\s*"([^"]+)"', body, re.MULTILINE)
    return m.group(1) if m else None


def _check_h00_conflicts(text: str) -> list[dict]:
    """H00 section-coherence checks (AL-004): TASK_ANALYSIS self-contradictions.

    A task analysis that declares the request ready for specification while
    recommending NEEDS_CLARIFICATION, or that declares HIGH intent confidence
    while recommending CONFIRMING_INTENT (HIGH auto-confirms), is internally
    conflicting and fails structurally.
    """
    recommended = _h00_next_state(text)
    if recommended is None:
        return []  # section presence is checked separately; nothing to compare
    checks: list[dict] = []
    sufficiency = parse_toml(section_text(text, "Sufficiency Assessment"))
    ready = sufficiency.get("sufficiency", {}).get("ready_for_specification")
    if ready is True and recommended == "NEEDS_CLARIFICATION":
        checks.append(
            {
                "id": "conflicting_sections",
                "result": "FAIL",
                "evidence": (
                    "sufficiency.ready_for_specification=true but "
                    "recommended_next_state=NEEDS_CLARIFICATION"
                ),
            }
        )
    else:
        checks.append(
            {
                "id": "conflicting_sections",
                "result": "PASS",
                "evidence": "sufficiency and recommended next state are coherent",
            }
        )
    intent = parse_toml(section_text(text, "Intent Confidence Assessment"))
    level = intent.get("intent_confidence", {}).get("level")
    if level == "HIGH" and recommended == "CONFIRMING_INTENT":
        checks.append(
            {
                "id": "conflict_high_intent_confirm",
                "result": "FAIL",
                "evidence": (
                    "intent_confidence.level=HIGH but "
                    "recommended_next_state=CONFIRMING_INTENT "
                    "(HIGH auto-confirms the reflection)"
                ),
            }
        )
    else:
        checks.append(
            {
                "id": "conflict_high_intent_confirm",
                "result": "PASS",
                "evidence": "intent confidence and recommended next state are coherent",
            }
        )
    return checks


def _check_h03_conflicts(text: str) -> list[dict]:
    """H03 section-coherence check (AL-004): VALIDATED with failing evaluations."""
    decision = parse_toml(section_text(text, "Validation Decision"))
    result = decision.get("decision", {}).get("result")
    if result != "VALIDATED":
        return []  # the conflict rule only applies to a VALIDATED decision
    completeness = parse_toml(section_text(text, "Completeness Evaluation"))
    consistency = parse_toml(section_text(text, "Consistency Evaluation"))
    problems = []
    if completeness.get("completeness", {}).get("status") == "INCOMPLETE":
        problems.append("completeness.status=INCOMPLETE")
    if consistency.get("consistency", {}).get("status") == "CONFLICTING":
        problems.append("consistency.status=CONFLICTING")
    if problems:
        return [
            {
                "id": "conflicting_sections",
                "result": "FAIL",
                "evidence": "decision.result=VALIDATED but " + "; ".join(problems),
            }
        ]
    return [
        {
            "id": "conflicting_sections",
            "result": "PASS",
            "evidence": "validation decision coherent with the evaluations",
        }
    ]


def _check_deferred_items(text: str) -> list[dict]:
    """H06: structurally validate the ``Deferred Items`` block when present."""
    body = section_text(text, "Deferred Items")
    if not body.strip():
        return [
            {
                "id": "deferred_items",
                "result": "SKIP",
                "evidence": "no Deferred Items section",
            }
        ]
    entries: list[dict] = []
    for block in toml_blocks(body):
        parsed = parse_toml(block)
        value = parsed.get("deferred_items")
        if isinstance(value, list):
            entries.extend(x for x in value if isinstance(x, dict))
    if not entries:
        return [
            {
                "id": "deferred_items",
                "result": "PASS",
                "evidence": "Deferred Items present and empty",
            }
        ]
    bad: list[str] = []
    for i, entry in enumerate(entries, 1):
        if entry.get("deferred") is not True:
            bad.append(f"entry {i}: deferred is not true")
        confirmed = entry.get("confirmed_by")
        if not isinstance(confirmed, str) or not confirmed.strip():
            bad.append(f"entry {i}: missing confirmed_by")
    if bad:
        return [
            {
                "id": "deferred_items",
                "result": "FAIL",
                "evidence": "; ".join(bad[:5]),
            }
        ]
    return [
        {
            "id": "deferred_items",
            "result": "PASS",
            "evidence": f"{len(entries)} deferred item(s) with confirmation",
        }
    ]


def _check_review_report(artifact: Path) -> dict:
    """H06 profile-aware: a `complex` task requires a REVIEW_REPORT.md."""
    profile = read_task_profile(_roots_from_artifact(artifact)[2])
    if profile != "complex":
        return {
            "id": "review_report",
            "result": "SKIP",
            "evidence": "task profile is not complex",
        }
    if any(
        p.is_file() and p.name.endswith("REVIEW_REPORT.md")
        for p in artifact.parent.iterdir()
    ):
        return {
            "id": "review_report",
            "result": "PASS",
            "evidence": "REVIEW_REPORT.md present for the complex task",
        }
    return {
        "id": "review_report",
        "result": "FAIL",
        "evidence": "complex task profile requires REVIEW_REPORT.md in the iteration",
    }


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
