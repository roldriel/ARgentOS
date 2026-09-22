"""Dogfood: the placement resolver run against the real repository.

This module is in the "tests anchored to the real repository" set of
``tests/AGENTS.md``: it reads the live working tree **on purpose** and is
strictly read-only. A synthetic repository cannot show that the resolver agrees
with the repository it was written for, which is the only thing that makes it
useful rather than merely self-consistent.

It asserts the two directions of the property plan 131 exists for:

1. **PLACE lands where the contract says.** The resolver states the canonical
   namespace of a family, and that namespace is the one the real tree uses.
2. **No applicable rule stops, and the consumer cannot continue.** A request the
   contract does not cover produces ``STOP`` with the rule it needed named — so
   an agent has nothing to act on and must escalate instead of picking a
   plausible path.

Evidence produced by this dogfood is quoted in the plan 131 record.
"""

from __future__ import annotations

from pathlib import Path

from runtime.placement import (
    DOMAIN_DEV,
    DOMAIN_PROTOCOL,
    PlacementOutcome,
    PlacementRequest,
    PlacementStop,
    resolve,
)

REPO_ROOT = Path(__file__).resolve().parents[1]


def test_the_contract_the_resolver_realizes_is_the_one_in_this_repository():
    decision = resolve(PlacementRequest(kind="adr", domain=DOMAIN_DEV))
    assert decision.result is not None
    assert decision.result.section.startswith("docs/placement-contract.md:")
    assert (REPO_ROOT / "docs" / "placement-contract.md").is_file()


def test_every_canonical_namespace_of_the_real_tree_is_contiguous():
    """A family's canonical namespace must be a directory path the tree can hold.

    The resolver never discovers a namespace; it reports one. This checks the
    reported namespaces are real locations of this repository rather than
    strings that look like paths.
    """
    checked = 0
    for kind, expected in (
        ("plan", "docs/plans"),
        ("adr", "docs/adr"),
        ("rfc", "docs/rfc"),
        ("glossary", "docs/glossary"),
        ("tool", "tools"),
        ("runtime", "runtime"),
        ("test", "tests"),
    ):
        decision = resolve(PlacementRequest(kind=kind, domain=DOMAIN_DEV))
        assert decision.placed, decision.evidence()
        assert decision.result is not None
        assert decision.result.canonical_namespace == expected
        assert (REPO_ROOT / expected).is_dir(), f"{expected} is not a directory here"
        checked += 1
    # Guard against a vacuous pass if the table is ever emptied.
    assert checked >= 7


def test_the_resolvers_own_artifacts_are_placed_by_its_own_rules():
    """The resolver is subject to the contract it implements.

    Its package is Reference runtime (``runtime/<package>/``) and its suites are
    the Test subsystem (``tests/``); both are reported, and both exist here. This
    is the PLACE half of the dogfood.
    """
    for module in ("rules.py", "resolver.py", "__init__.py"):
        assert (REPO_ROOT / "runtime" / "placement" / module).is_file()

    runtime = resolve(PlacementRequest(kind="runtime", domain=DOMAIN_DEV))
    suites = resolve(PlacementRequest(kind="test", domain=DOMAIN_DEV))
    assert runtime.result is not None and suites.result is not None
    assert runtime.result.canonical_namespace == "runtime"
    assert suites.result.canonical_namespace == "tests"

    verified = resolve(
        PlacementRequest(
            kind="test",
            domain=DOMAIN_DEV,
            path="tests/test_placement_resolver.py",
        )
    )
    assert verified.placed, verified.evidence()
    assert verified.result is not None and verified.result.path_verified


def test_an_artifact_the_contract_does_not_cover_stops_and_names_its_gap():
    """The STOP half of the dogfood, on a shape this repository could plausibly
    produce: a "specification" accepted as if it were a third governance class
    beside RFC, ADR and Plan. No family rule declares it, so there is no rule to
    place it by, and the resolver must not approximate one from the neighbours
    it does know."""
    decision = resolve(PlacementRequest(kind="specification", domain=DOMAIN_DEV))
    assert decision.outcome is PlacementOutcome.STOP
    assert decision.refusal is not None
    assert decision.refusal.reason is PlacementStop.NEW_FAMILY
    # The consumer receives what it needs to escalate, and nothing to act on.
    assert decision.result is None
    assert decision.refusal.considered
    assert decision.refusal.required
    assert "docs/placement-contract.md:" in decision.refusal.section


def test_a_guessed_path_is_refused_even_when_it_would_look_right():
    """The failure this Change removes: an agent noticing that decisions live in
    ``docs/adr/`` and placing a plan next to them. The path is refused and the
    canonical one reported, so the agent corrects rather than proceeds."""
    decision = resolve(
        PlacementRequest(kind="plan", domain=DOMAIN_DEV, path="docs/adr/73-plan.md")
    )
    assert decision.outcome is PlacementOutcome.STOP
    assert decision.refusal is not None
    assert decision.refusal.reason is PlacementStop.INVALID_PLACEMENT
    assert decision.refusal.considered == ("docs/plans",)


def test_the_declared_generated_area_is_the_one_the_host_actually_uses():
    """§21/§6: the session-state family is placeable because the host designates
    it. The designation is not a story — the host writes there."""
    decision = resolve(
        PlacementRequest(kind="run-log", domain=DOMAIN_PROTOCOL)
    )
    assert decision.placed, decision.evidence()
    assert decision.result is not None
    assert decision.result.canonical_namespace == ".project/orchestrator"
    store = (REPO_ROOT / "runtime" / "orchestrator" / "store.py").read_text(
        encoding="utf-8"
    )
    assert ".project" in store and "orchestrator" in store
