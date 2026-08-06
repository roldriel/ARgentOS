"""Coverage invariant: every artifact contract declares `enforcement`, and
`gated` declarations correspond bidirectionally with runner policies.

- Every contract declares `enforcement` in {"gated", "informational"}.
- A `gated` contract names the policies that gate it (`gated_by`), each of
  which must exist and cite the contract's artifact via `artifact =`.
- Every runner policy whose `artifact` matches a contract's artifact belongs
  to that contract's `gated_by` list, and the contract is `gated`.

A new contract without a declaration, or a policy/contract mismatch, breaks
the build. Policies without TOML front matter (suite-enforced, e.g. H13) or
whose artifact is not a contract artifact (e.g. S00's `.project/.last_health_check`,
H15 without artifact) are outside this correspondence.
"""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

_harness_dir = Path(__file__).resolve().parents[1]
if str(_harness_dir) not in sys.path:
    sys.path.insert(0, str(_harness_dir))

import runner_markdown
import runner_paths
import runner_policies

VALID_ENFORCEMENT = {"gated", "informational"}


def _contract_files() -> list[Path]:
    files: list[Path] = []
    for directory in runner_policies._contract_dirs():
        files += sorted(directory.glob("*.md"))
    return files


def _contract_meta(path: Path) -> dict:
    return runner_markdown.parse_front_matter(path.read_text(encoding="utf-8"))


def _runner_policies() -> list[tuple[Path, dict]]:
    """Policies loadable by the runner (TOML front matter with a trigger)."""
    policies: list[tuple[Path, dict]] = []
    for policies_dir in runner_paths.POLICIES_DIRS:
        if not policies_dir.is_dir():
            continue
        for path in sorted(policies_dir.glob("*.md")):
            try:
                meta = runner_markdown.parse_front_matter(
                    path.read_text(encoding="utf-8")
                )
            except ValueError:
                continue
            if meta.get("trigger"):
                policies.append((path, meta))
    return policies


@pytest.mark.parametrize("path", _contract_files(), ids=lambda p: p.name)
def test_contract_declares_enforcement(path):
    meta = _contract_meta(path)
    enforcement = meta.get("enforcement")
    assert enforcement in VALID_ENFORCEMENT, (
        f"{path}: missing or invalid enforcement declaration "
        f"(got {enforcement!r}; valid: {sorted(VALID_ENFORCEMENT)})"
    )
    if enforcement == "gated":
        gated_by = meta.get("gated_by")
        assert (
            isinstance(gated_by, list) and gated_by
        ), f"{path}: gated contract must declare a non-empty gated_by list"
    else:
        assert (
            "gated_by" not in meta
        ), f"{path}: informational contract must not declare gated_by"


def _gated_contracts() -> list[Path]:
    return [
        p for p in _contract_files() if _contract_meta(p).get("enforcement") == "gated"
    ]


@pytest.mark.parametrize("path", _gated_contracts(), ids=lambda p: p.name)
def test_gated_contract_is_cited_by_its_policies(path):
    meta = _contract_meta(path)
    for trigger in meta["gated_by"]:
        policy = runner_policies.load_policy(trigger)
        assert policy.get("artifact") == meta["artifact"], (
            f"{path}: gated_by policy '{trigger}' cites artifact "
            f"'{policy.get('artifact')}' instead of '{meta['artifact']}'"
        )


@pytest.mark.parametrize(
    "policy_path,meta",
    _runner_policies(),
    ids=[p.name for p, _ in _runner_policies()],
)
def test_policy_artifact_is_a_gated_contract(policy_path, meta):
    artifact = meta.get("artifact")
    if not artifact:
        return  # policies without an artifact gate (e.g. H15) are out of scope
    contract_path = runner_policies._contract_map().get(artifact)
    if contract_path is None:
        return  # artifact is not a contract artifact (e.g. S00 health check)
    contract = _contract_meta(contract_path)
    assert contract.get("enforcement") == "gated", (
        f"{policy_path}: cites artifact '{artifact}' whose contract declares "
        f"enforcement={contract.get('enforcement')!r} instead of 'gated'"
    )
    assert meta["trigger"] in contract.get("gated_by", []), (
        f"{policy_path}: trigger '{meta['trigger']}' not listed in gated_by of "
        f"{contract_path}"
    )
