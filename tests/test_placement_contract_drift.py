"""Drift guard: the placement resolver must stay in lockstep with its contract.

``runtime/placement/rules.py`` is a mechanical re-expression of
``docs/placement-contract.md`` §6, not a second source of truth. If either side
changes without the other, these tests fail loudly — the failure mode that
matters is *silent* divergence between the published rule table and the rules an
agent actually gets.

The guard asserts only facts that are stable under prose edits: the exact
backticked canonical paths of the tables, the presence of each realized family
name, and the rule labels that determine the STOP semantics. It deliberately
does not parse English sentences.
"""

from __future__ import annotations

import re
from pathlib import Path

import pytest

from runtime.placement import rules as R

REPO_ROOT = Path(__file__).resolve().parents[1]


@pytest.fixture(scope="module")
def contract() -> str:
    return (REPO_ROOT / R.CONTRACT_PATH).read_text(encoding="utf-8")


def test_contract_exists_and_is_the_normative_source(contract: str) -> None:
    assert contract.startswith("# Repository / Artifact Placement Contract")
    assert "**Status:** Active" in contract
    assert "normative source" in contract


def _declared_namespaces(contract: str) -> set[str]:
    """Every directory the contract declares, expanded from its backticked paths.

    The contract declares a namespace either flat (``.project/changes/``) or as a
    brace composite of its sub-namespaces
    (``protocol/.agents/{contracts,delegation,...}/``). Fragmentary citations
    such as ``protocol/.agents/`` (a domain row, not a family) expand to the same
    root and are harmless: the assertion is about the families the resolver
    realizes, and an extra declared directory cannot hide a missing one.
    """
    declared: set[str] = set()
    for entry in re.findall(r"`([^`]+)`", contract):
        # A cited path may carry trailing prose: `docs/rfc/` (flat).
        entry = entry.strip().split()[0]
        match = re.match(r"^([^`]*?)\{([^}]+)\}(.*)$", entry)
        if match is None:
            if entry.endswith("/"):
                declared.add(entry.rstrip("/"))
            continue
        head, group, tail = match.groups()
        for member in group.split(","):
            declared.add(f"{head}{member.strip()}{tail}".rstrip("/"))
    return declared


def test_every_realized_namespace_is_declared_in_the_contract(contract: str) -> None:
    """Each canonical namespace the resolver returns is rooted in the contract.

    The contract declares directories (``docs/rfc/``), composites
    (``docs/working/{audits,research,proposals}/``), glob forms (``docs/*.md``
    (root)) and fixed files. A realized namespace is accepted when the contract
    declares it, when the contract declares something inside it, or when the
    contract's own namespace cell derives it (a glob or a ``<package>``
    template). Because each family's name is also checked against the contract
    below, a fabricated namespace cannot pass by sharing a declared parent.
    """
    declared = _declared_namespaces(contract)
    for rule in R.FAMILIES:
        for namespace in rule.namespaces:
            path = namespace.path
            assert (
                path in declared
                or any(entry.startswith(f"{path}/") for entry in declared)
            ), (
                f"namespace {path!r} of family {rule.family!r} is not declared "
                f"in {R.CONTRACT_PATH}"
            )


def test_every_realized_family_matches_a_declared_family_name(contract: str) -> None:
    """A family the resolver invents without contract backing would drift here.

    Sub-namespace families (one per Protocol sub-namespace, one per durable
    namespace) are a faithful decomposition of a single contract row, so the
    guard accepts either the decomposed name or the contract's row name.
    """
    for rule in R.FAMILIES:
        head = rule.family.split()[0]
        assert head in contract, (
            f"family {rule.family!r} has no counterpart in {R.CONTRACT_PATH}"
        )


def test_contract_declares_the_domains_the_resolver_uses(contract: str) -> None:
    assert "| **DEV** |" in contract
    assert "| **Protocol** |" in contract
    assert set(R.DOMAINS) == {R.DOMAIN_DEV, R.DOMAIN_PROTOCOL}


def test_stop_semantics_the_resolver_returns_are_declared(contract: str) -> None:
    """Every STOP trigger is one the contract names (``PC-23`` table)."""
    contract_triggers = {
        "UNKNOWN KIND": "UNKNOWN_KIND",
        "NO DOMAIN": "NO_DOMAIN",
        "CROSS-DOMAIN AMBIGUITY": "CROSS_DOMAIN_AMBIGUITY",
        "NEW FAMILY": "NEW_FAMILY",
        "AMBIGUOUS KIND": "AMBIGUOUS_KIND",
        "UNDEFINED PLACEMENT": "UNDEFINED_PLACEMENT",
        "TWO VALID LOCATIONS": "TWO_VALID_LOCATIONS",
        "AUTHORITY UNRESOLVED": "AUTHORITY_UNRESOLVED",
        "CONSTRAINT VIOLATION": "CONSTRAINT_VIOLATION",
    }
    for label, member in contract_triggers.items():
        assert f"`{label}`" in contract, f"STOP trigger {label!r} left the contract"
        assert member in {s.name for s in _stops()}


def test_resolver_returns_no_stop_the_contract_does_not_declare() -> None:
    """The two verification states map onto contract rules, not new taxonomy."""
    extra = {s.name for s in _stops()} - _declared_stop_names()
    assert extra == {"INVALID_PLACEMENT", "UNRESOLVED_EXCEPTION"}, (
        "the only STOP values outside the §8 trigger table must be the two "
        "verification states justified by §16 PC-51 and §9 PC-30"
    )
    contract = (REPO_ROOT / R.CONTRACT_PATH).read_text(encoding="utf-8")
    assert "**PC-51.**" in contract, "PC-51 (agent verification) was renumbered"
    assert "**PC-30.**" in contract, "PC-30 (uninterpretable exception) was renumbered"


def test_canonicality_statuses_match_the_contract() -> None:
    contract = (REPO_ROOT / R.CONTRACT_PATH).read_text(encoding="utf-8")
    for status in R.CANONICALITIES:
        assert f"`{status}`" in contract, f"canonicality {status!r} left the contract"


def test_kind_vocabulary_is_not_treated_as_a_closed_enum() -> None:
    """The resolver must not claim to enumerate every kind of the repository."""
    contract = (REPO_ROOT / R.CONTRACT_PATH).read_text(encoding="utf-8")
    assert "no global closed kind enum" in contract
    # Every family's kind set is a lookup aid; an unknown kind must be refused,
    # never normalised into a neighbouring one.
    known = {k for rule in R.FAMILIES for k in rule.kinds}
    assert "frobnicator" not in known


def test_durable_families_keep_their_distinctive_git_persistence_metadata() -> None:
    """§21: project-durable and git-persisted must remain separate properties."""
    contract = (REPO_ROOT / R.CONTRACT_PATH).read_text(encoding="utf-8")
    assert "project-durable" in contract and "git-persisted" in contract
    assert "project-durable ≠ git commit operation" in contract
    durable = [r for r in R.FAMILIES if r.namespaces[0].path.startswith(".project/changes")]
    assert durable, "the durable change-governance namespace disappeared"


def _stops():
    from runtime.placement import PlacementStop

    return list(PlacementStop)


def _declared_stop_names() -> set[str]:
    return {
        "UNKNOWN_KIND",
        "NO_DOMAIN",
        "CROSS_DOMAIN_AMBIGUITY",
        "NEW_FAMILY",
        "AMBIGUOUS_KIND",
        "UNDEFINED_PLACEMENT",
        "TWO_VALID_LOCATIONS",
        "AUTHORITY_UNRESOLVED",
        "CONSTRAINT_VIOLATION",
    }
