"""Artifact validators and trigger execution for the harness runner."""

from __future__ import annotations

import sys
from pathlib import Path

_HARNESS_DIR = Path(__file__).resolve().parent
if str(_HARNESS_DIR) not in sys.path:
    sys.path.insert(0, str(_HARNESS_DIR))

import re
import time
from datetime import datetime, timezone
from typing import Any

import feature_flags
import technical_practices
from runner_artifacts import artifact_path, report_path
from runner_markdown import extract_section, extract_toml_block, find_section_headings
from runner_models import CheckResult, HarnessResult
from runner_policies import load_policy


def validate_h07_scope_compliance(content: str) -> list[CheckResult]:
    checks: list[CheckResult] = []
    data = extract_toml_block(content, "Scope Compliance")
    if data is None:
        checks.append(
            CheckResult(
                id="scope_toml_parsable",
                result="FAIL",
                evidence="No valid TOML block found in ## Scope Compliance",
            )
        )
        return checks

    checks.append(
        CheckResult(
            id="scope_toml_parsable", result="PASS", evidence="TOML block parsed"
        )
    )

    scope = data.get("scope_compliance", {})
    scope_respected = scope.get("scope_respected")
    unplanned = scope.get("unplanned_changes", None)
    authorized = scope.get("user_authorized_extra_work", None)

    checks.append(
        CheckResult(
            id="scope_respected_true",
            result="PASS" if scope_respected is True else "FAIL",
            evidence=f"scope_respected={scope_respected}",
        )
    )
    checks.append(
        CheckResult(
            id="unplanned_changes_empty",
            result=(
                "PASS"
                if isinstance(unplanned, list) and len(unplanned) == 0
                else "FAIL"
            ),
            evidence=f"unplanned_changes={unplanned}",
        )
    )
    checks.append(
        CheckResult(
            id="no_unauthorized_extra_work",
            result="PASS" if authorized is False else "FAIL",
            evidence=f"user_authorized_extra_work={authorized}",
        )
    )
    return checks


def validate_h06_final_decision(content: str) -> list[CheckResult]:
    checks: list[CheckResult] = []
    data = extract_toml_block(content, "Final Decision")
    if data is None:
        checks.append(
            CheckResult(
                id="final_decision_toml_parsable",
                result="FAIL",
                evidence="No valid TOML block in ## Final Decision",
            )
        )
        return checks

    checks.append(
        CheckResult(
            id="final_decision_toml_parsable",
            result="PASS",
            evidence="TOML block parsed",
        )
    )

    decision = data.get("decision", {})
    result = decision.get("result")
    checks.append(
        CheckResult(
            id="final_decision_completed",
            result="PASS" if result == "COMPLETED" else "FAIL",
            evidence=f"decision.result={result}",
        )
    )
    return checks


def validate_h06_acceptance_criteria(content: str) -> list[CheckResult]:
    checks: list[CheckResult] = []
    data = extract_toml_block(content, "Acceptance Criteria Evaluation")
    if data is None:
        checks.append(
            CheckResult(
                id="acceptance_criteria_toml_parsable",
                result="FAIL",
                evidence="No valid TOML block in ## Acceptance Criteria Evaluation",
            )
        )
        return checks

    checks.append(
        CheckResult(
            id="acceptance_criteria_toml_parsable",
            result="PASS",
            evidence="TOML block parsed",
        )
    )

    criteria = data.get("acceptance_criteria", [])
    if not isinstance(criteria, list):
        checks.append(
            CheckResult(
                id="acceptance_criteria_list",
                result="FAIL",
                evidence="acceptance_criteria is not a list",
            )
        )
        return checks

    checks.append(
        CheckResult(
            id="acceptance_criteria_list",
            result="PASS",
            evidence=f"Found {len(criteria)} criteria",
        )
    )

    for idx, criterion in enumerate(criteria, start=1):
        if not isinstance(criterion, dict):
            checks.append(
                CheckResult(
                    id=f"acceptance_criterion_{idx}_is_dict",
                    result="FAIL",
                    evidence=f"Criterion {idx} is not a dictionary",
                )
            )
            continue

        res = criterion.get("result")
        if res == "FAIL":
            checks.append(
                CheckResult(
                    id=f"acceptance_criterion_{idx}_not_failed",
                    result="FAIL",
                    evidence=f"Criterion {idx} has result=FAIL",
                )
            )
        elif res == "PARTIAL":
            plan = criterion.get("action_plan")
            checks.append(
                CheckResult(
                    id=f"acceptance_criterion_{idx}_partial_has_action_plan",
                    result="PASS" if plan else "FAIL",
                    evidence=f"Criterion {idx} is PARTIAL with action_plan={plan}",
                )
            )

    # If there were no FAIL or PARTIAL without plan, add a global PASS check.
    failed = [c for c in checks if c.result == "FAIL"]
    if not failed:
        checks.append(
            CheckResult(
                id="no_failed_acceptance_criteria",
                result="PASS",
                evidence="No criterion has result=FAIL; PARTIAL criteria have action_plan",
            )
        )
    return checks


def validate_h05_execution_summary(
    session_uuid: str, iteration: str | None
) -> list[CheckResult]:
    checks: list[CheckResult] = []
    summary_path = artifact_path(session_uuid, "EXECUTION_SUMMARY.md", iteration)
    if not summary_path.exists():
        checks.append(
            CheckResult(
                id="execution_summary_exists",
                result="FAIL",
                evidence=f"EXECUTION_SUMMARY.md not found: {summary_path}",
            )
        )
        return checks

    checks.append(
        CheckResult(
            id="execution_summary_exists",
            result="PASS",
            evidence=f"EXECUTION_SUMMARY.md found: {summary_path}",
        )
    )
    content = summary_path.read_text(encoding="utf-8")

    data = extract_toml_block(content, "Final Project State")
    if data is None:
        checks.append(
            CheckResult(
                id="final_state_toml_parsable",
                result="FAIL",
                evidence="No valid TOML block in ## Final Project State",
            )
        )
        return checks

    checks.append(
        CheckResult(
            id="final_state_toml_parsable", result="PASS", evidence="TOML block parsed"
        )
    )

    state = data.get("final_state", {})
    status = state.get("status")
    valid_final_states = {"VERIFIABLE", "BLOCKED"}
    checks.append(
        CheckResult(
            id="final_state_status_valid",
            result="PASS" if status in valid_final_states else "FAIL",
            evidence=f"final_state.status={status} (valid values: {', '.join(sorted(valid_final_states))})",
        )
    )
    checks.append(
        CheckResult(
            id="final_state_verifiable",
            result="PASS" if status == "VERIFIABLE" else "FAIL",
            evidence=f"final_state.status={status}",
        )
    )

    steps_data = extract_toml_block(content, "Steps Executed")
    if steps_data is None:
        checks.append(
            CheckResult(
                id="steps_executed_toml_parsable",
                result="FAIL",
                evidence="No valid TOML block in ## Steps Executed",
            )
        )
        return checks

    steps = steps_data.get("steps_executed", [])
    if not isinstance(steps, list):
        checks.append(
            CheckResult(
                id="steps_executed_list",
                result="FAIL",
                evidence="steps_executed is not a list",
            )
        )
        return checks

    all_ok = True
    for idx, step in enumerate(steps, start=1):
        if not isinstance(step, dict):
            all_ok = False
            checks.append(
                CheckResult(
                    id=f"step_{idx}_is_dict",
                    result="FAIL",
                    evidence=f"Step {idx} is not a dictionary",
                )
            )
            continue

        status = step.get("status")
        notes = step.get("notes")
        valid_step_states = {"COMPLETED", "SKIPPED", "BLOCKED"}
        if status not in valid_step_states:
            all_ok = False
            checks.append(
                CheckResult(
                    id=f"step_{idx}_status_valid",
                    result="FAIL",
                    evidence=f"Step {idx} has status={status} (valid values: {', '.join(sorted(valid_step_states))})",
                )
            )
        elif status == "BLOCKED":
            all_ok = False
            checks.append(
                CheckResult(
                    id=f"step_{idx}_completed_or_skipped",
                    result="FAIL",
                    evidence=f"Step {idx} is BLOCKED",
                )
            )
        elif status == "SKIPPED" and not notes:
            all_ok = False
            checks.append(
                CheckResult(
                    id=f"step_{idx}_skipped_has_notes",
                    result="FAIL",
                    evidence=f"Step {idx} is SKIPPED without notes",
                )
            )

    if all_ok:
        checks.append(
            CheckResult(
                id="all_steps_completed_or_skipped",
                result="PASS",
                evidence="All steps are COMPLETED or SKIPPED with notes",
            )
        )

    return checks


TECHNICAL_PRACTICE_FLAGS: set[str] = technical_practices.TECHNICAL_PRACTICE_FLAGS


def _any_technical_practice_enabled() -> bool:
    """Return True if at least one technical-practice feature flag is enabled."""
    return any(feature_flags.is_enabled(flag) for flag in TECHNICAL_PRACTICE_FLAGS)


def validate_h01_technical_approach(
    session_uuid: str, iteration: str | None
) -> list[CheckResult]:
    """Validate that the technical approach section is consistent with enabled flags."""
    checks: list[CheckResult] = []

    if not _any_technical_practice_enabled():
        checks.append(
            CheckResult(
                id="technical_practices_disabled",
                result="PASS",
                evidence="No technical-practice flags are enabled; skipping validation",
            )
        )
        return checks

    spec_path = artifact_path(session_uuid, "TASK_SPECIFICATION.md", iteration)
    if not spec_path.exists():
        checks.append(
            CheckResult(
                id="technical_approach_spec_exists",
                result="FAIL",
                evidence=f"TASK_SPECIFICATION.md not found: {spec_path}",
            )
        )
        return checks

    checks.append(
        CheckResult(
            id="technical_approach_spec_exists",
            result="PASS",
            evidence=f"TASK_SPECIFICATION.md found: {spec_path}",
        )
    )
    content = spec_path.read_text(encoding="utf-8")
    data = extract_toml_block(content, "Technical Approach")

    if data is None:
        checks.append(
            CheckResult(
                id="technical_approach_section_present",
                result="PASS",
                evidence="## Technical Approach section absent; no practices selected",
            )
        )
        return checks

    checks.append(
        CheckResult(
            id="technical_approach_section_present",
            result="PASS",
            evidence="## Technical Approach section found",
        )
    )

    technical_approach = data.get("technical_approach", {})
    enabled = technical_approach.get("enabled", [])
    if not isinstance(enabled, list):
        checks.append(
            CheckResult(
                id="technical_approach_enabled_is_list",
                result="FAIL",
                evidence=f"technical_approach.enabled is not a list: {enabled}",
            )
        )
        return checks

    checks.append(
        CheckResult(
            id="technical_approach_enabled_is_list",
            result="PASS",
            evidence=f"technical_approach.enabled = {enabled}",
        )
    )

    if not enabled:
        checks.append(
            CheckResult(
                id="technical_approach_enabled_empty",
                result="PASS",
                evidence="No practices selected",
            )
        )
        return checks

    notes = technical_approach.get("notes", [])
    has_notes = isinstance(notes, list) and any(str(n).strip() for n in notes)
    checks.append(
        CheckResult(
            id="technical_approach_has_notes",
            result="PASS" if has_notes else "FAIL",
            evidence=f"notes={notes}",
        )
    )

    for practice in enabled:
        known = practice in TECHNICAL_PRACTICE_FLAGS
        checks.append(
            CheckResult(
                id=f"{practice}_flag_known",
                result="PASS" if known else "FAIL",
                evidence=practice,
            )
        )
        if known:
            enabled_at_protocol_level = feature_flags.is_enabled(practice)
            checks.append(
                CheckResult(
                    id=f"{practice}_flag_enabled",
                    result="PASS" if enabled_at_protocol_level else "FAIL",
                    evidence=f"{practice} enabled at protocol level = {enabled_at_protocol_level}",
                )
            )

    return checks


def validate_h05_technical_practice_evidence(
    session_uuid: str, iteration: str | None
) -> list[CheckResult]:
    """Validate evidence for every technical practice selected in the task specification."""
    checks: list[CheckResult] = []

    spec_path = artifact_path(session_uuid, "TASK_SPECIFICATION.md", iteration)
    summary_path = artifact_path(session_uuid, "EXECUTION_SUMMARY.md", iteration)

    if not spec_path.exists() or not summary_path.exists():
        checks.append(
            CheckResult(
                id="technical_practice_evidence_inputs",
                result="PASS",
                evidence="Missing inputs; skipping technical-practice evidence validation",
            )
        )
        return checks

    spec_data = (
        extract_toml_block(spec_path.read_text(encoding="utf-8"), "Technical Approach")
        or {}
    )
    enabled = spec_data.get("technical_approach", {}).get("enabled", [])

    if not enabled:
        checks.append(
            CheckResult(
                id="technical_practices_not_required",
                result="PASS",
                evidence="No practices selected in technical_approach.enabled",
            )
        )
        return checks

    summary_content = summary_path.read_text(encoding="utf-8")
    summary_data = (
        extract_toml_block(summary_content, "Technical Practice Evidence") or {}
    )
    evidence_root = summary_data.get("technical_practice_evidence", {})

    for practice in enabled:
        evidence = evidence_root.get(practice, {})
        applied = evidence.get("applied")
        checks.append(
            CheckResult(
                id=f"{practice}_evidence_present",
                result="PASS" if applied is not None else "FAIL",
                evidence=f"{practice}.applied={applied}",
            )
        )

        if applied is False:
            reason = evidence.get("reason", "")
            checks.append(
                CheckResult(
                    id=f"{practice}_not_applied_has_reason",
                    result="PASS" if reason and str(reason).strip() else "FAIL",
                    evidence=f"{practice}.applied=false with reason={reason!r}",
                )
            )
        elif applied is True:
            other_fields = {k: v for k, v in evidence.items() if k != "applied"}
            checks.append(
                CheckResult(
                    id=f"{practice}_evidence_nonempty",
                    result="PASS" if bool(other_fields) else "FAIL",
                    evidence=f"{practice} fields={sorted(other_fields.keys())}",
                )
            )

    return checks


BASE_RUBRICS: set[str] = {
    "TASK_SPECIFICATION_RUBRIC",
    "CONTEXT_ARTIFACT_RUBRIC",
    "CONTEXT_VALIDATION_REPORT_RUBRIC",
    "EXECUTION_PLAN_RUBRIC",
    "EXECUTION_SUMMARY_RUBRIC",
    "VERIFICATION_REPORT_RUBRIC",
}

TECHNICAL_PRACTICE_RUBRIC_MAP: dict[str, str] = (
    technical_practices.TECHNICAL_PRACTICE_RUBRIC_MAP
)


def expected_rubrics_for_session(session_uuid: str, iteration: str | None) -> set[str]:
    """Return base rubrics plus any technical-practice rubrics enabled for this task."""
    rubrics = set(BASE_RUBRICS)
    spec_path = artifact_path(session_uuid, "TASK_SPECIFICATION.md", iteration)
    if not spec_path.exists():
        return rubrics

    spec_data = (
        extract_toml_block(spec_path.read_text(encoding="utf-8"), "Technical Approach")
        or {}
    )
    enabled = spec_data.get("technical_approach", {}).get("enabled", [])
    if not isinstance(enabled, list):
        return rubrics

    for practice in enabled:
        rubric_name = TECHNICAL_PRACTICE_RUBRIC_MAP.get(practice)
        if rubric_name and feature_flags.is_enabled(practice):
            rubrics.add(rubric_name)

    return rubrics


def validate_rubric_evaluation(
    content: str, expected_rubrics: set[str] | None = None
) -> tuple[list[CheckResult], dict[str, str]]:
    """Validate the ## Rubric Evaluation section and extract rubric scores."""
    checks: list[CheckResult] = []
    scores: dict[str, str] = {}

    if expected_rubrics is None:
        expected_rubrics = set(BASE_RUBRICS)

    section_content = extract_section(content, "Rubric Evaluation")
    if not section_content:
        checks.append(
            CheckResult(
                id="rubric_evaluation_section_present",
                result="FAIL",
                evidence="Section '## Rubric Evaluation' not found",
            )
        )
        return checks, scores

    checks.append(
        CheckResult(
            id="rubric_evaluation_section_present",
            result="PASS",
            evidence="Section '## Rubric Evaluation' found",
        )
    )

    found_rubrics: dict[str, str] = {}
    # Match rubric subsections (### RUBRIC_NAME) and their bodies until next ### or end.
    for match in re.finditer(
        r"^###\s+([A-Z_]+_RUBRIC)\s*\n(.*?)(?=^###\s|\Z)",
        section_content,
        re.MULTILINE | re.DOTALL,
    ):
        rubric_name = match.group(1)
        rubric_body = match.group(2)
        found_rubrics[rubric_name] = rubric_body

    missing = expected_rubrics - set(found_rubrics)
    if missing:
        checks.append(
            CheckResult(
                id="rubric_evaluation_all_rubrics_present",
                result="FAIL",
                evidence=f"Missing rubric subsections: {', '.join(sorted(missing))}",
            )
        )
    else:
        checks.append(
            CheckResult(
                id="rubric_evaluation_all_rubrics_present",
                result="PASS",
                evidence=f"All {len(expected_rubrics)} rubric subsections found",
            )
        )

    for rubric_name, rubric_body in found_rubrics.items():
        # Look for the first Level line in the rubric body.
        level_match = re.search(
            r"^\s*-?\s*Level:\s*(INSUFFICIENT|MEETS|EXCEEDS)\s*$",
            rubric_body,
            re.MULTILINE,
        )
        if level_match:
            scores[rubric_name] = level_match.group(1)
            checks.append(
                CheckResult(
                    id=f"rubric_{rubric_name.lower()}_has_level",
                    result="PASS",
                    evidence=f"Found level {level_match.group(1)} for {rubric_name}",
                )
            )
        else:
            checks.append(
                CheckResult(
                    id=f"rubric_{rubric_name.lower()}_has_level",
                    result="FAIL",
                    evidence=f"No valid Level found for {rubric_name}",
                )
            )

        evidence_match = re.search(
            r"^\s*-?\s*Evidence:\s+.+$", rubric_body, re.MULTILINE
        )
        checks.append(
            CheckResult(
                id=f"rubric_{rubric_name.lower()}_has_evidence",
                result="PASS" if evidence_match else "FAIL",
                evidence=f"{'Found' if evidence_match else 'Missing'} Evidence for {rubric_name}",
            )
        )

    return checks, scores


# Common value domains that may be joined by "and" or "or" without being compound.
_VALUE_DOMAIN_TOKENS = {
    # HTTP methods
    "get",
    "post",
    "put",
    "patch",
    "delete",
    "head",
    "options",
    # Data formats
    "json",
    "xml",
    "yaml",
    "csv",
    "html",
    "plain text",
    "text/plain",
    "application/json",
    "application/xml",
    # Booleans
    "true",
    "false",
    # Common roles
    "admin",
    "user",
    "guest",
    "reader",
    "writer",
    "editor",
    "owner",
}

# Action verbs that, when appearing after "and" or "or", indicate a separate action.
_ACTION_VERBS = {
    "create",
    "send",
    "validate",
    "reject",
    "return",
    "accept",
    "update",
    "delete",
    "insert",
    "query",
    "process",
    "handle",
    "check",
    "verify",
    "store",
    "fetch",
    "retrieve",
    "compute",
    "generate",
    "import",
    "export",
    "transform",
    "parse",
    "serialize",
    "authenticate",
    "authorize",
    "add",
    "remove",
    "modify",
    "edit",
    "refactor",
    "fix",
    "implement",
    "build",
    "run",
    "execute",
    "perform",
}


def _is_compound_criterion(text: str) -> bool:
    """Return True if the criterion joins multiple independent actions or conditions.

    A criterion is compound when "and" or "or" separate independent actions
    ("create X and send Y") or conditions ("validate A or B"). It is not compound
    when those words enumerate values within the same domain ("return HTTP 200 or
    201", "accept JSON and XML").
    """
    if ";" in text:
        return True

    normalized = re.sub(r"\s+", " ", text.strip().lower())
    if not re.search(r"\band\b|\bor\b", normalized):
        return False

    # Enumerations of values within the same domain are not compound.
    value_patterns = [
        r"\b(?:get|post|put|patch|delete|head|options)(?:\s+(?:and|or)\s+(?:get|post|put|patch|delete|head|options))+\b",
        r"\b(?:json|xml|yaml|csv|html|plain text|text/plain|application/json|application/xml)(?:\s+(?:and|or)\s+(?:json|xml|yaml|csv|html|plain text|text/plain|application/json|application/xml))+\b",
        r"\b(?:true|false)(?:\s+(?:and|or)\s+(?:true|false))+\b",
        r"\b(?:admin|user|guest|reader|writer|editor|owner)(?:\s+(?:and|or)\s+(?:admin|user|guest|reader|writer|editor|owner))+\b",
        r"\b\d+(?:\s+(?:and|or)\s+\d+)+\b",
    ]
    for pattern in value_patterns:
        if re.search(pattern, normalized):
            # Ensure the whole criterion is not an enumeration; remove the matched part and
            # check that no remaining "and"/"or" join separate actions.
            remaining = re.sub(pattern, "", normalized, count=1).strip()
            if not re.search(r"\band\b|\bor\b", remaining):
                return False

    tokens = re.findall(r"[a-z0-9/]+|\d+", normalized)
    for i, token in enumerate(tokens):
        if token in ("and", "or"):
            # "and"/"or" followed by an action verb indicates a separate action.
            if i + 1 < len(tokens) and tokens[i + 1] in _ACTION_VERBS:
                return True
            # "and"/"or" between a verb and a non-value-domain token indicates multiple
            # independent conditions/actions.
            if i - 1 >= 0 and tokens[i - 1] in _ACTION_VERBS:
                if i + 1 < len(tokens) and tokens[i + 1] not in _VALUE_DOMAIN_TOKENS:
                    return True
    return False


def validate_ears(section_content: str) -> list[CheckResult]:
    """Validate that each bullet in the section follows an EARS pattern and is atomic."""
    checks: list[CheckResult] = []
    bullets = [
        line.strip()
        for line in section_content.splitlines()
        if re.match(r"^[-*]\s+", line.strip())
    ]

    if not bullets:
        checks.append(
            CheckResult(
                id="ears_criteria_present",
                result="FAIL",
                evidence="No acceptance criteria bullets found",
            )
        )
        return checks

    checks.append(
        CheckResult(
            id="ears_criteria_present",
            result="PASS",
            evidence=f"Found {len(bullets)} acceptance criterion/criteria",
        )
    )

    # EARS patterns
    patterns = [
        (r"^The\s+.+\s+shall\s+.+$", "ubiquitous"),
        (r"^When\s+.+\s*,\s*the\s+.+\s+shall\s+.+$", "event-driven"),
        (r"^While\s+.+\s*,\s*the\s+.+\s+shall\s+.+$", "state-driven"),
        (r"^If\s+.+\s*,\s*then\s+the\s+.+\s+shall\s+.+$", "unwanted-behavior"),
        (r"^Where\s+.+\s*,\s*the\s+.+\s+shall\s+.+$", "optional-feature"),
    ]

    for idx, bullet in enumerate(bullets, start=1):
        # Remove leading bullet marker
        text = re.sub(r"^[-*]\s+", "", bullet)

        # Check compound
        if _is_compound_criterion(text):
            checks.append(
                CheckResult(
                    id=f"ears_atomic_{idx}",
                    result="FAIL",
                    evidence=f"Criterion {idx} is compound: {text[:80]}",
                )
            )
            continue

        matched = any(re.match(pattern, text, re.IGNORECASE) for pattern, _ in patterns)
        if matched:
            checks.append(
                CheckResult(
                    id=f"ears_pattern_{idx}",
                    result="PASS",
                    evidence=f"Criterion {idx} follows an EARS pattern",
                )
            )
        else:
            checks.append(
                CheckResult(
                    id=f"ears_pattern_{idx}",
                    result="FAIL",
                    evidence=f"Criterion {idx} does not follow an EARS pattern: {text[:80]}",
                )
            )

    return checks


def validate_sections(
    artifact_content: str, required_sections: list[str]
) -> list[CheckResult]:
    headings = find_section_headings(artifact_content)
    checks: list[CheckResult] = []
    for section in required_sections:
        # Normalize comparison: ignore case and allow title-case variations
        normalized = {h.lower(): h for h in headings}
        if section.lower() in normalized:
            checks.append(
                CheckResult(
                    id=f"has_section_{section.lower().replace(' ', '_')}",
                    result="PASS",
                    evidence=f"Section '{normalized[section.lower()]}' found",
                )
            )
        else:
            checks.append(
                CheckResult(
                    id=f"has_section_{section.lower().replace(' ', '_')}",
                    result="FAIL",
                    evidence=f"Required section '{section}' not found",
                )
            )
    return checks


SEMANTIC_VALIDATORS = {
    "technical_approach": lambda session_uuid, iteration, content: (
        validate_h01_technical_approach(session_uuid, iteration)
    ),
    "execution_summary": lambda session_uuid, iteration, content: (
        validate_h05_execution_summary(session_uuid, iteration)
    ),
    "technical_practice_evidence": lambda session_uuid, iteration, content: (
        validate_h05_technical_practice_evidence(session_uuid, iteration)
    ),
    "final_decision": lambda session_uuid, iteration, content: (
        validate_h06_final_decision(content) if content is not None else []
    ),
    "acceptance_criteria_evaluation": lambda session_uuid, iteration, content: (
        validate_h06_acceptance_criteria(content) if content is not None else []
    ),
    "scope_compliance": lambda session_uuid, iteration, content: (
        validate_h07_scope_compliance(content) if content is not None else []
    ),
}


def run_trigger(
    session_uuid: str, trigger: str, iteration: str | None = None
) -> HarnessResult:
    start = time.perf_counter()
    timestamp = datetime.now(timezone.utc).isoformat()

    def _finish(result: HarnessResult) -> HarnessResult:
        result.duration_ms = int((time.perf_counter() - start) * 1000)
        return result

    try:
        policy = load_policy(trigger)
    except FileNotFoundError as exc:
        return _finish(
            HarnessResult(
                trigger=trigger,
                transition="UNKNOWN",
                result="FAIL",
                timestamp=timestamp,
                error=str(exc),
            )
        )
    except ValueError as exc:
        return _finish(
            HarnessResult(
                trigger=trigger,
                transition=(
                    policy.get("transition", "UNKNOWN")
                    if "policy" in locals()
                    else "UNKNOWN"
                ),
                result="FAIL",
                timestamp=timestamp,
                error=str(exc),
            )
        )

    transition = policy.get("transition", "UNKNOWN")
    artifact_name = policy.get("artifact")
    validation_type = policy.get("validation_type", "artifact")
    required_sections = policy.get("required_sections", [])

    result = HarnessResult(
        trigger=trigger,
        transition=transition,
        result="PASS",
        artifact=(
            str(artifact_path(session_uuid, artifact_name, iteration))
            if artifact_name
            else None
        ),
        report=str(report_path(session_uuid)),
        timestamp=timestamp,
    )

    if validation_type == "artifact" and artifact_name:
        artifact = artifact_path(session_uuid, artifact_name, iteration)
        if not artifact.exists():
            result.checks.append(
                CheckResult(
                    id="artifact_exists",
                    result="FAIL",
                    evidence=f"Artifact not found: {artifact}",
                )
            )
            result.result = "FAIL"
        else:
            result.checks.append(
                CheckResult(
                    id="artifact_exists",
                    result="PASS",
                    evidence=f"Artifact found: {artifact}",
                )
            )
            content = artifact.read_text(encoding="utf-8")
            section_checks = validate_sections(content, required_sections)
            result.checks.extend(section_checks)
            if any(c.result == "FAIL" for c in section_checks):
                result.result = "FAIL"

    # EARS validation for acceptance criteria sections
    if policy.get("ears_validation") and artifact_name and result.artifact:
        artifact = artifact_path(session_uuid, artifact_name, iteration)
        if artifact.exists():
            content = artifact.read_text(encoding="utf-8")
            section_name = policy.get("ears_section", "Acceptance criteria")
            section_content = extract_section(content, section_name)
            if section_content:
                ears_checks = validate_ears(section_content)
                result.checks.extend(ears_checks)
                if any(c.result == "FAIL" for c in ears_checks):
                    result.result = "FAIL"
            else:
                result.checks.append(
                    CheckResult(
                        id="ears_section_found",
                        result="FAIL",
                        evidence=f"EARS section '{section_name}' not found",
                    )
                )
                result.result = "FAIL"

    # Rubric evaluation structural validation
    if policy.get("rubric_validation") and artifact_name and result.artifact:
        artifact = artifact_path(session_uuid, artifact_name, iteration)
        if artifact.exists():
            content = artifact.read_text(encoding="utf-8")
            rubric_set = expected_rubrics_for_session(session_uuid, iteration)
            rubric_checks, rubric_scores = validate_rubric_evaluation(
                content, rubric_set
            )
            result.checks.extend(rubric_checks)
            result.rubric_scores.update(rubric_scores)
            if any(c.result == "FAIL" for c in rubric_checks):
                result.result = "FAIL"

    # Semantic validation declared by the policy front matter. The policy lists
    # the validator names it requires in `semantic_checks`; any name the runner
    # does not know how to execute is an explicit FAIL, never silently ignored.
    if policy.get("semantic_validation"):
        declared = policy.get("semantic_checks", [])
        content: str | None = None
        if artifact_name and result.artifact:
            artifact = artifact_path(session_uuid, artifact_name, iteration)
            if artifact.exists():
                content = artifact.read_text(encoding="utf-8")
        for name in declared:
            validator = SEMANTIC_VALIDATORS.get(name)
            if validator is None:
                result.checks.append(
                    CheckResult(
                        id=f"semantic_validator_{name}_known",
                        result="FAIL",
                        evidence=(
                            f"Policy declares unknown semantic validator '{name}'; "
                            f"known validators: {', '.join(sorted(SEMANTIC_VALIDATORS))}"
                        ),
                    )
                )
                result.result = "FAIL"
                continue
            semantic_checks = validator(session_uuid, iteration, content)
            result.checks.extend(semantic_checks)
            if any(c.result == "FAIL" for c in semantic_checks):
                result.result = "FAIL"

    return _finish(result)
