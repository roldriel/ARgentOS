#!/usr/bin/env python3
"""
Protocol health check for the .agents protocol.

Validates that the protocol directory structure is intact and that optional
features (decision trees, rubrics, knowledge base) are well-formed when enabled.
"""

from __future__ import annotations

import json
import re
import sys
import tomllib
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

_HARNESS_DIR = Path(__file__).resolve().parent
if str(_HARNESS_DIR) not in sys.path:
    sys.path.insert(0, str(_HARNESS_DIR))

import decision_tree_evaluator
import feature_flags
import skill_validation
import technical_practices

PROJECT_ROOT = Path(__file__).resolve().parents[2]
AGENTS_DIR = PROJECT_ROOT / ".agents"
HARNESS_DIR = AGENTS_DIR / "harness"
ORCHESTRATORS_DIR = AGENTS_DIR / "orchestrators"
CORE_DIR = ORCHESTRATORS_DIR / "core"
DISCOVERY_DIR_DOMAIN = ORCHESTRATORS_DIR / "discovery"
SYSTEM_DIR_DOMAIN = ORCHESTRATORS_DIR / "system"
DECISION_TREES_DIR = CORE_DIR / "harness" / "decision_trees"
PROJECT_DIR = PROJECT_ROOT / ".project"
LAST_HEALTH_CHECK_FILE = PROJECT_DIR / ".last_health_check"

# Domains whose harness policies may require recovery decision trees.
# (domain name, policies dir, decision trees dir)
DECISION_TREE_DOMAINS: list[tuple[str, Path, Path]] = [
    (
        "core",
        CORE_DIR / "harness" / "policies",
        CORE_DIR / "harness" / "decision_trees",
    ),
    (
        "discovery",
        DISCOVERY_DIR_DOMAIN / "harness" / "policies",
        DISCOVERY_DIR_DOMAIN / "harness" / "decision_trees",
    ),
    (
        "system",
        SYSTEM_DIR_DOMAIN / "harness" / "policies",
        SYSTEM_DIR_DOMAIN / "harness" / "decision_trees",
    ),
]

# Policy triggers documented as intentionally having no decision tree
# (see .agents/harness/INDEX.md, "Recovery Mechanism").
TRIGGERS_WITHOUT_DECISION_TREES = {"H09", "H10"}


def expected_tree_triggers(policies_dir: Path) -> set[str]:
    """Derive the triggers that must have a decision tree from policy files."""
    triggers = set()
    if policies_dir.is_dir():
        for policy in policies_dir.glob("*.md"):
            trigger = policy.stem.split("-", 1)[0].upper()
            if trigger and trigger not in TRIGGERS_WITHOUT_DECISION_TREES:
                triggers.add(trigger)
    return triggers


def required_dirs() -> list[Path]:
    """Return the list of required protocol directories (resolved at call time)."""
    return [
        CORE_DIR / "states",
        AGENTS_DIR / "roles",
        CORE_DIR / "workflow",
        AGENTS_DIR / "contracts",
        HARNESS_DIR / "policies",
    ]


REQUIRED_INDEX_FILES = [
    AGENTS_DIR / "INDEX.md",
    CORE_DIR / "states" / "AGENT_STATE_MACHINE.md",
    CORE_DIR / "roles" / "orchestrator.md",
]


@dataclass
class HealthCheckResult:
    result: str  # PASS or FAIL
    checks: list[dict[str, Any]] = field(default_factory=list)
    timestamp: str = ""
    error: str | None = None

    def to_dict(self) -> dict[str, Any]:
        return {
            "result": self.result,
            "checks": self.checks,
            "timestamp": self.timestamp,
            "error": self.error,
        }


def _check(
    checks: list[dict[str, Any]],
    check_id: str,
    passed: bool,
    evidence: str,
) -> None:
    checks.append(
        {"id": check_id, "result": "PASS" if passed else "FAIL", "evidence": evidence}
    )


def check_required_directories(checks: list[dict[str, Any]]) -> bool:
    """Verify that all required protocol directories exist."""
    all_present = True
    for directory in required_dirs():
        present = directory.is_dir()
        _check(
            checks,
            f"required_dir_{directory.name}",
            present,
            f"{'Found' if present else 'Missing'} directory: {directory}",
        )
        if not present:
            all_present = False
    return all_present


def check_required_files(checks: list[dict[str, Any]]) -> bool:
    """Verify that all required index files exist and are readable."""
    all_present = True
    for path in REQUIRED_INDEX_FILES:
        readable = path.is_file() and path.stat().st_size > 0
        _check(
            checks,
            f"required_file_{path.name}",
            readable,
            f"{'Readable' if readable else 'Missing or empty'}: {path}",
        )
        if not readable:
            all_present = False
    return all_present


def check_decision_trees(checks: list[dict[str, Any]]) -> bool:
    """Validate decision-tree TOML files if the feature is enabled.

    Expected triggers are derived from the policy files of every domain that
    provides a decision_trees directory (core H*, discovery D*, system S*),
    minus the documented exemptions in TRIGGERS_WITHOUT_DECISION_TREES.
    Structural validation (node refs, cycles) is delegated to
    decision_tree_evaluator._validate_tree.
    """
    if not feature_flags.is_enabled("decision_trees"):
        _check(
            checks,
            "decision_trees_enabled",
            True,
            "decision_trees feature is disabled; skipping TOML validation",
        )
        return True

    all_valid = True
    parsed: dict[Path, dict[str, Any]] = {}

    for domain, policies_dir, trees_dir in DECISION_TREE_DOMAINS:
        if not trees_dir.is_dir():
            continue
        toml_files = sorted(trees_dir.glob("*_FAIL.toml"))
        found_triggers = {path.stem.replace("_FAIL", "") for path in toml_files}
        expected_triggers = expected_tree_triggers(policies_dir)
        missing = expected_triggers - found_triggers

        if missing:
            _check(
                checks,
                f"decision_trees_all_triggers_present_{domain}",
                False,
                f"Missing decision tree files for triggers: {', '.join(sorted(missing))}",
            )
            all_valid = False
        else:
            _check(
                checks,
                f"decision_trees_all_triggers_present_{domain}",
                True,
                f"Found decision tree files for all triggers: {', '.join(sorted(found_triggers))}",
            )

        for path in toml_files:
            try:
                parsed[path] = tomllib.loads(path.read_text(encoding="utf-8"))
                _check(
                    checks,
                    f"decision_tree_toml_valid_{path.stem}",
                    True,
                    f"{path.name} parsed successfully",
                )
            except tomllib.TOMLDecodeError as exc:
                _check(
                    checks,
                    f"decision_tree_toml_valid_{path.stem}",
                    False,
                    f"{path.name} TOML error: {exc}",
                )
                all_valid = False

    # Structural checks (start node, branches, node references, cycles).
    for path, data in parsed.items():
        try:
            decision_tree_evaluator._validate_tree(data)
            _check(
                checks,
                f"decision_tree_structure_valid_{path.stem}",
                True,
                f"{path.name} structure is valid (refs resolved, no cycles)",
            )
        except decision_tree_evaluator.DecisionTreeError as exc:
            _check(
                checks,
                f"decision_tree_structure_valid_{path.stem}",
                False,
                f"{path.name} invalid: {exc}",
            )
            all_valid = False

    return all_valid


def check_contracts_front_matter(checks: list[dict[str, Any]]) -> bool:
    """Validate that all contract files have a consistent TOML front matter."""
    all_valid = True
    contract_paths = sorted((AGENTS_DIR / "contracts").glob("*.md"))
    contract_paths += sorted(ORCHESTRATORS_DIR.glob("*/contracts/*.md"))
    for contract_path in contract_paths:
        content = contract_path.read_text(encoding="utf-8")
        try:
            match = re.match(r"^\+\+\+\s*\n(.*?)\n\+\+\+\s*\n", content, re.DOTALL)
            if not match:
                raise ValueError("No front matter")
            meta = tomllib.loads(match.group(1))
            required = {"artifact", "phase", "produced_by"}
            missing = required - set(meta.keys())
            if missing:
                raise ValueError(f"Missing fields: {', '.join(sorted(missing))}")
            if meta.get("artifact") != contract_path.name:
                raise ValueError(
                    f"artifact mismatch: {meta.get('artifact')} != {contract_path.name}"
                )
            _check(
                checks,
                f"contract_front_matter_{contract_path.name}",
                True,
                f"Valid front matter in {contract_path.name}",
            )
        except Exception as exc:
            _check(
                checks,
                f"contract_front_matter_{contract_path.name}",
                False,
                f"Invalid front matter in {contract_path.name}: {exc}",
            )
            all_valid = False
    return all_valid


def check_rubrics(checks: list[dict[str, Any]]) -> bool:
    """Validate rubrics configuration if the feature is enabled."""
    if not feature_flags.is_enabled("rubrics"):
        _check(
            checks,
            "rubrics_enabled",
            True,
            "rubrics feature is disabled; skipping rubrics validation",
        )
        return True

    all_valid = True
    rubrics_path = AGENTS_DIR / "standards" / "quality" / "RUBRICS.md"
    exists = rubrics_path.is_file()
    _check(
        checks,
        "rubrics_file_present",
        exists,
        f"{'Found' if exists else 'Missing'} {rubrics_path}",
    )
    if not exists:
        all_valid = False

    for role in ("reviewer", "verifier"):
        role_path = AGENTS_DIR / "roles" / f"{role}.md"
        present = role_path.is_file()
        _check(
            checks,
            f"rubrics_role_{role}_present",
            present,
            f"{'Found' if present else 'Missing'} {role_path}",
        )
        if not present:
            all_valid = False

    return all_valid


def check_knowledge_base(checks: list[dict[str, Any]]) -> bool:
    """Validate knowledge base layout if the feature is enabled."""
    if not feature_flags.is_enabled("knowledge_base"):
        _check(
            checks,
            "knowledge_base_enabled",
            True,
            "knowledge_base feature is disabled; skipping KB validation",
        )
        return True

    all_valid = True
    kb_dir = PROJECT_DIR / "knowledge"
    index_path = kb_dir / "INDEX.md"
    exists = index_path.is_file()
    _check(
        checks,
        "knowledge_base_index_present",
        exists,
        f"{'Found' if exists else 'Missing'} {index_path}",
    )
    if not exists:
        all_valid = False

    context_path = AGENTS_DIR / "standards" / "context" / "CONTEXT.md"
    context_exists = context_path.is_file()
    _check(
        checks,
        "knowledge_base_context_standard_present",
        context_exists,
        f"{'Found' if context_exists else 'Missing'} {context_path}",
    )
    if not context_exists:
        all_valid = False

    discoverer_path = AGENTS_DIR / "roles" / "context_discoverer.md"
    discoverer_exists = discoverer_path.is_file()
    _check(
        checks,
        "knowledge_base_context_discoverer_role_present",
        discoverer_exists,
        f"{'Found' if discoverer_exists else 'Missing'} {discoverer_path}",
    )
    if not discoverer_exists:
        all_valid = False

    for contract in (
        DISCOVERY_DIR_DOMAIN / "contracts" / "KB_DISCOVERY_REPORT.md",
        AGENTS_DIR / "contracts" / "SESSION_LOG.md",
    ):
        contract_path = contract
        present = contract_path.is_file()
        _check(
            checks,
            f"knowledge_base_contract_{contract_path.name.replace('.', '_')}_present",
            present,
            f"{'Found' if present else 'Missing'} {contract_path}",
        )
        if not present:
            all_valid = False

    return all_valid


def check_project_skills(checks: list[dict[str, Any]]) -> bool:
    """Validate .project/skills/ structurally when the folder exists.

    Non-blocking: an invalid project skill produces a WARNING entry in the
    health report and is excluded from activation for that session, but it
    never fails the health check. Reuses the same structural validation as
    the protocol-level test (skill_validation).
    """
    skills_dir = PROJECT_DIR / "skills"
    if not skills_dir.is_dir():
        _check(
            checks,
            "project_skills_dir",
            True,
            "No .project/skills/ directory; skipping project skill validation",
        )
        return True

    for skill_dir in skill_validation.iter_skill_dirs(skills_dir):
        problems = skill_validation.validate_skill(skill_dir)
        if problems:
            checks.append(
                {
                    "id": f"project_skill_{skill_dir.name}",
                    "result": "WARNING",
                    "evidence": (
                        f"Invalid project skill '{skill_dir.name}' excluded for "
                        f"this session: {'; '.join(problems)}"
                    ),
                }
            )
        else:
            _check(
                checks,
                f"project_skill_{skill_dir.name}",
                True,
                f"Valid project skill: {skill_dir.name}",
            )
    return True


TECHNICAL_PRACTICE_STANDARDS: dict[str, Path] = (
    technical_practices.TECHNICAL_PRACTICE_STANDARDS
)


def check_technical_practice_standards(checks: list[dict[str, Any]]) -> bool:
    """Validate that standards exist for enabled technical-practice flags."""
    any_enabled = any(
        feature_flags.is_enabled(flag) for flag in TECHNICAL_PRACTICE_STANDARDS
    )
    if not any_enabled:
        _check(
            checks,
            "technical_practice_standards_enabled",
            True,
            "No technical-practice flags are enabled; skipping standard validation",
        )
        return True

    all_valid = True
    for flag, standard_path in TECHNICAL_PRACTICE_STANDARDS.items():
        if not feature_flags.is_enabled(flag):
            _check(
                checks,
                f"{flag}_standard_enabled",
                True,
                f"{flag} feature is disabled; skipping standard validation",
            )
            continue

        exists = standard_path.is_file()
        _check(
            checks,
            f"{flag}_standard_present",
            exists,
            f"{'Found' if exists else 'Missing'} {standard_path}",
        )
        if not exists:
            all_valid = False

    return all_valid


def check_state_json_storage(checks: list[dict[str, Any]]) -> bool:
    """Verify that session state (state.json) can be written and read.

    `state.json` is the single source of truth for hook enforcement; this
    check performs a write/read/delete round-trip of a probe file inside
    `.project/` so a read-only or broken artifacts directory fails the
    health check before any session starts.
    """
    probe = PROJECT_DIR / ".state_check_probe"
    payload = '{"probe": true}\n'
    try:
        PROJECT_DIR.mkdir(parents=True, exist_ok=True)
        probe.write_text(payload, encoding="utf-8")
        read_back = probe.read_text(encoding="utf-8")
        probe.unlink()
    except OSError as exc:
        _check(
            checks,
            "state_json_writable",
            False,
            f"Cannot write/read state.json probe in {PROJECT_DIR}: {exc}",
        )
        return False
    ok = read_back == payload
    _check(
        checks,
        "state_json_writable",
        ok,
        "state.json write/read probe succeeded"
        if ok
        else "state.json probe read-back mismatch",
    )
    return ok


def run_health_check() -> HealthCheckResult:
    """Run the full protocol health check and return a structured result."""
    # Timestamp is taken from datetime.now(timezone.utc) on the system running the runner.
    timestamp = datetime.now(timezone.utc).isoformat()
    checks: list[dict[str, Any]] = []

    try:
        # Initialize the .project/knowledge infrastructure if it is missing.
        # This mirrors the ArgentOS System Agent's responsibility to prepare
        # the runtime environment before the health check validates it.
        kb_dir = PROJECT_DIR / "knowledge"
        entries_dir = kb_dir / "entries"
        index_path = kb_dir / "INDEX.md"
        index_template = AGENTS_DIR / "contracts" / "KNOWLEDGE_INDEX.md"
        PROJECT_DIR.mkdir(parents=True, exist_ok=True)
        kb_dir.mkdir(parents=True, exist_ok=True)
        entries_dir.mkdir(parents=True, exist_ok=True)
        if not index_path.exists() and index_template.exists():
            index_path.write_text(
                index_template.read_text(encoding="utf-8"), encoding="utf-8"
            )

        # Warn if the last health-check timestamp appears to be in the future.
        last = last_health_check_time()
        now = datetime.now(timezone.utc)
        if last and last > now:
            _check(
                checks,
                "last_health_check_not_future",
                False,
                f"Last health-check timestamp {last} is in the future (system time: {now})",
            )

        ok_dirs = check_required_directories(checks)
        ok_files = check_required_files(checks)
        ok_contracts = check_contracts_front_matter(checks)
        ok_dt = check_decision_trees(checks)
        ok_rubrics = check_rubrics(checks)
        ok_kb = check_knowledge_base(checks)
        ok_technical_practices = check_technical_practice_standards(checks)
        ok_project_skills = check_project_skills(checks)
        ok_state = check_state_json_storage(checks)

        passed = (
            ok_dirs
            and ok_files
            and ok_contracts
            and ok_dt
            and ok_rubrics
            and ok_kb
            and ok_technical_practices
            and ok_project_skills
            and ok_state
        )
        result = HealthCheckResult(
            result="PASS" if passed else "FAIL",
            checks=checks,
            timestamp=timestamp,
        )
    except Exception as exc:
        result = HealthCheckResult(
            result="FAIL",
            checks=checks,
            timestamp=timestamp,
            error=str(exc),
        )

    if result.result == "PASS":
        try:
            PROJECT_DIR.mkdir(parents=True, exist_ok=True)
            LAST_HEALTH_CHECK_FILE.write_text(result.timestamp, encoding="utf-8")
        except OSError as exc:
            result.error = f"Health check passed but failed to update timestamp: {exc}"

    return result


def last_health_check_time() -> datetime | None:
    """Return the timestamp of the last successful health check, or None."""
    if not LAST_HEALTH_CHECK_FILE.exists():
        return None
    try:
        raw = LAST_HEALTH_CHECK_FILE.read_text(encoding="utf-8").strip()
        return datetime.fromisoformat(raw)
    except (OSError, ValueError):
        return None


def should_run_health_check(ttl_hours: int | None = None) -> bool:
    """Return True if the health check should be run based on TTL.

    When ttl_hours is not provided, the configured TTL is used
    (`.agents/features.toml` [health_check] ttl_hours, overridable via the
    AGENTS_HEALTH_CHECK_TTL_HOURS environment variable; default 24).
    """
    if ttl_hours is None:
        ttl_hours = feature_flags.health_check_ttl_hours()
    last = last_health_check_time()
    if last is None:
        return True
    age = datetime.now(timezone.utc) - last
    return age.total_seconds() > ttl_hours * 3600


if __name__ == "__main__":
    res = run_health_check()
    print(json.dumps(res.to_dict(), indent=2))
    raise SystemExit(0 if res.result == "PASS" else 1)
