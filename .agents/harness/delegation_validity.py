"""Delegation validity checks for harness policy H15 (delegation-validity).

A delegation is *valid* when its payload is not only well formed but also
executable: the profile resolves under ``.agents/roles/profiles/``, every
skill resolves under ``.project/skills/`` or ``.agents/skills/`` (project
level wins on name collision), every input artifact exists inside the
session, and ``context_budget`` is a finite, positive constraint. The return
report is valid when it complies with the delegation contract schema and its
``blockers``/``deviations`` entries declare their failure class.

Failure classes (see the failure taxonomy inline in
``.agents/delegation/WORKER_DELEGATION_CONTRACT.md``, §"Failure classes in
`blockers` and `deviations`"):

- F1 (blocker): prevents completing the phase; destination recovery.
  Applies to an unresolvable profile (V1), an incoherent budget (V3), a
  missing input artifact (V4) and an invalid return report (V5).
- F2 (deviation): does not prevent completing the phase; destination
  logged warning. Applies to an unresolvable skill (V2) — the Worker
  reports it as a deviation and never invents the skill's content.

The runner CLI does not execute H15 (a delegation payload is not a session
artifact); machine evaluation lives in this module and in the policy's test
suite (``.agents/harness/tests/test_delegation_validity.py``). The
Orchestrator and Worker agents apply the same checks at the two gates
declared by the policy (pre-delegation and post-return).
"""

from __future__ import annotations

import math
import sys
from pathlib import Path
from typing import Any

_HARNESS_DIR = Path(__file__).resolve().parent
if str(_HARNESS_DIR) not in sys.path:
    sys.path.insert(0, str(_HARNESS_DIR))

import runner_paths
from runner_models import CheckResult

PROJECT_ROOT = runner_paths.PROJECT_ROOT

# Valid failure-class prefixes for `deviations` entries in a return report,
# per the delegation contract (blockers carry class blocker implicitly).
DEVIATION_CLASS_PREFIXES = ("deviation:", "ambiguity:", "inconsistency:")

# Mandatory fields of the Worker return report (contract §"Worker Return
# Report"). `project_changes` and `recommendation` are optional per phase.
RETURN_REPORT_REQUIRED_FIELDS = (
    "output_artifact",
    "role_executed",
    "phase_completed",
    "summary",
    "blockers",
    "deviations",
)


def _profiles_dir(project_root: Path) -> Path:
    return project_root / ".agents" / "roles" / "profiles"


def _resolve_skill(name: str, project_root: Path) -> Path | None:
    """Resolve a skill name to its SKILL.md, project level first."""
    candidates = (
        project_root / ".project" / "skills" / name / "SKILL.md",
        project_root / ".agents" / "skills" / name / "SKILL.md",
    )
    for candidate in candidates:
        if candidate.is_file():
            return candidate
    return None


def validate_delegation_payload(
    payload: dict[str, Any], project_root: Path | str | None = None
) -> list[CheckResult]:
    """Evaluate the pre-delegation gate (V1–V4) over a delegation payload.

    ``project_root`` overrides the repository root used to resolve profiles,
    skills and input artifacts (used mainly by tests).
    """
    root = Path(project_root).resolve() if project_root else PROJECT_ROOT
    checks: list[CheckResult] = []

    # V1 — Profile resolvability (F1 blocker on violation).
    profile = payload.get("profile")
    if profile is None:
        checks.append(
            CheckResult(
                id="v1_profile_resolvable",
                result="PASS",
                evidence="profile is null; generic worker applies",
            )
        )
    elif not isinstance(profile, str) or not profile:
        checks.append(
            CheckResult(
                id="v1_profile_resolvable",
                result="FAIL",
                evidence=f"F1 blocker: profile must be a string or null, got {profile!r}",
            )
        )
    else:
        profile_path = _profiles_dir(root) / f"{profile}.md"
        checks.append(
            CheckResult(
                id="v1_profile_resolvable",
                result="PASS" if profile_path.is_file() else "FAIL",
                evidence=(
                    f"Profile resolves: {profile_path}"
                    if profile_path.is_file()
                    else f"F1 blocker: profile '{profile}' not found under {_profiles_dir(root)}"
                ),
            )
        )

    # V2 — Skill resolvability (F2 deviation on violation; non-blocking).
    skills = payload.get("skills")
    if skills is None:
        skills = []
    if not isinstance(skills, list):
        checks.append(
            CheckResult(
                id="v2_skills_resolvable",
                result="FAIL",
                evidence=f"F2 deviation: skills must be a list, got {skills!r}",
            )
        )
    else:
        for skill in skills:
            resolved = _resolve_skill(str(skill), root) if isinstance(skill, str) else None
            checks.append(
                CheckResult(
                    id=f"v2_skill_resolvable_{skill}",
                    result="PASS" if resolved else "FAIL",
                    evidence=(
                        f"Skill resolves: {resolved}"
                        if resolved
                        else (
                            f"F2 deviation (non-blocking): skill {skill!r} does not resolve "
                            f"under .project/skills/ or .agents/skills/; the Worker MUST report "
                            f"it as a deviation and MUST NOT invent its content"
                        )
                    ),
                )
            )
        if not skills:
            checks.append(
                CheckResult(
                    id="v2_skills_resolvable",
                    result="PASS",
                    evidence="No skills declared; nothing to resolve",
                )
            )

    # V3 — Budget coherence (F1 blocker when not finite and positive).
    budget = payload.get("context_budget")
    if budget is None:
        checks.append(
            CheckResult(
                id="v3_budget_coherent",
                result="PASS",
                evidence="context_budget is optional and absent",
            )
        )
    else:
        coherent = (
            isinstance(budget, (int, float))
            and not isinstance(budget, bool)
            and math.isfinite(budget)
            and budget > 0
        )
        checks.append(
            CheckResult(
                id="v3_budget_coherent",
                result="PASS" if coherent else "FAIL",
                evidence=(
                    f"context_budget={budget} is a finite, positive constraint"
                    if coherent
                    else (
                        f"F1 blocker: context_budget={budget!r} is not a finite, positive "
                        f"constraint on the runtime's Budget resource"
                    )
                ),
            )
        )

    # V4 — Input artifact existence (F1 blocker on violation).
    input_artifacts = payload.get("input_artifacts")
    if input_artifacts is None:
        input_artifacts = []
    if not isinstance(input_artifacts, list):
        checks.append(
            CheckResult(
                id="v4_input_artifacts_exist",
                result="FAIL",
                evidence=f"F1 blocker: input_artifacts must be a list, got {input_artifacts!r}",
            )
        )
    else:
        for artifact in input_artifacts:
            rel = Path(str(artifact))
            in_session_tree = (
                rel.parts
                and rel.parts[0] == ".project"
                and len(rel.parts) >= 4
            )
            exists = in_session_tree and (root / rel).is_file()
            checks.append(
                CheckResult(
                    id=f"v4_input_artifact_exists_{rel.name}",
                    result="PASS" if exists else "FAIL",
                    evidence=(
                        f"Input artifact found: {root / rel}"
                        if exists
                        else (
                            f"F1 blocker: input artifact {artifact!r} does not exist inside "
                            f".project/<session-uuid>/<iteration>/"
                        )
                    ),
                )
            )
        if not input_artifacts:
            checks.append(
                CheckResult(
                    id="v4_input_artifacts_exist",
                    result="PASS",
                    evidence="No input artifacts declared; nothing to check",
                )
            )

    return checks


def validate_return_report(report: dict[str, Any]) -> list[CheckResult]:
    """Evaluate the post-return gate (V5) over a Worker return report."""
    checks: list[CheckResult] = []

    # V5 — Required fields present.
    for field_name in RETURN_REPORT_REQUIRED_FIELDS:
        present = field_name in report and report[field_name] is not None
        checks.append(
            CheckResult(
                id=f"v5_field_present_{field_name}",
                result="PASS" if present else "FAIL",
                evidence=(
                    f"Field '{field_name}' present"
                    if present
                    else f"F1 blocker: return report missing required field '{field_name}'"
                ),
            )
        )

    # V5 — blockers is a list of entries of class blocker (implicit; any
    # string entry is acceptable, but class-prefixed entries are rejected:
    # blockers must not redeclare deviation/ambiguity/inconsistency).
    blockers = report.get("blockers")
    if isinstance(blockers, list):
        for idx, entry in enumerate(blockers, start=1):
            misclassified = isinstance(entry, str) and entry.startswith(
                DEVIATION_CLASS_PREFIXES
            )
            checks.append(
                CheckResult(
                    id=f"v5_blocker_{idx}_class_blocker",
                    result="PASS" if not misclassified else "FAIL",
                    evidence=(
                        f"blockers entry {idx} is class blocker"
                        if not misclassified
                        else (
                            f"F1 blocker: blockers entry {idx} declares a deviation-class "
                            f"prefix; blockers reports entries of class blocker only"
                        )
                    ),
                )
            )
    elif "blockers" in report:
        checks.append(
            CheckResult(
                id="v5_blockers_is_list",
                result="FAIL",
                evidence=f"F1 blocker: blockers must be a list, got {blockers!r}",
            )
        )

    # V5 — deviations entries are prefixed with their failure class.
    deviations = report.get("deviations")
    if isinstance(deviations, list):
        for idx, entry in enumerate(deviations, start=1):
            prefixed = isinstance(entry, str) and entry.startswith(
                DEVIATION_CLASS_PREFIXES
            )
            checks.append(
                CheckResult(
                    id=f"v5_deviation_{idx}_class_prefixed",
                    result="PASS" if prefixed else "FAIL",
                    evidence=(
                        f"deviations entry {idx} declares its failure class"
                        if prefixed
                        else (
                            f"F1 blocker: deviations entry {idx} is not prefixed with its "
                            f"class ({', '.join(p.rstrip(':') for p in DEVIATION_CLASS_PREFIXES)})"
                        )
                    ),
                )
            )
    elif "deviations" in report:
        checks.append(
            CheckResult(
                id="v5_deviations_is_list",
                result="FAIL",
                evidence=f"F1 blocker: deviations must be a list, got {deviations!r}",
            )
        )

    return checks
