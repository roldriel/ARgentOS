"""Behaviour of the mechanical placement resolver (plan 131).

These tests protect the property the whole Change exists for:

    explicit rule        -> PLACE
    no applicable rule   -> STOP
    ambiguous rule       -> STOP
    insufficient info    -> STOP
    plausible guess      -> never PLACE

No test asserts a path discovered by looking at the filesystem: every expected
location is asserted against the rule the contract publishes, so a test failure
means the resolver diverged from its normative source.
"""

from __future__ import annotations

from runtime.placement import (
    DOMAIN_DEV,
    DOMAIN_PROTOCOL,
    PlacementDecision,
    PlacementOutcome,
    PlacementRequest,
    PlacementStop,
    resolve,
    verify_path,
)


def _stop_reason(subject):
    """Accept either a request (resolved here) or an already-made decision."""
    decision = subject if isinstance(subject, PlacementDecision) else resolve(subject)
    assert decision.outcome is PlacementOutcome.STOP, decision.evidence()
    assert decision.refusal is not None
    return decision.refusal.reason


# --- Discriminator 1: domain / owner ----------------------------------------


def test_unknown_domain_stops():
    assert _stop_reason(
        PlacementRequest(kind="adr", domain="Platform")
    ) is PlacementStop.NO_DOMAIN


def test_same_kind_resolves_differently_per_domain():
    """Domain is the first discriminator: kind alone cannot decide placement."""
    protocol = resolve(
        PlacementRequest(kind="contract", domain=DOMAIN_PROTOCOL)
    )
    assert protocol.placed
    assert protocol.result is not None
    assert protocol.result.canonical_namespace == "protocol/.agents/contracts"

    dev = resolve(PlacementRequest(kind="contract", domain=DOMAIN_DEV))
    assert dev.outcome is PlacementOutcome.STOP
    assert dev.refusal is not None
    assert dev.refusal.reason is PlacementStop.NEW_FAMILY


def test_cross_domain_ambiguity_stops_rather_than_picking_a_domain():
    """A DEV/Protocol collision must escalate, never resolve by preference."""
    decision = resolve(PlacementRequest(kind="harness"))
    assert decision.outcome is PlacementOutcome.STOP
    assert decision.refusal is not None
    assert decision.refusal.reason is PlacementStop.CROSS_DOMAIN_AMBIGUITY


def test_a_flat_namespace_does_not_authorize_a_nested_path():
    """The contract's ``docs/*.md`` (root) and ``docs/rfc/`` (flat) forms admit
    the files directly inside, not an invented subdirectory of them."""
    reason = _stop_reason(
        PlacementRequest(
            kind="policy", domain=DOMAIN_DEV, path="docs/notes/policy.md"
        )
    )
    assert reason is PlacementStop.INVALID_PLACEMENT


def test_operational_artifact_goes_to_its_declared_subdirectory():
    expected = {
        "operational-instruction": ".agents/policies",
        "dev-workflow": ".agents/workflows",
    }
    for kind, namespace in expected.items():
        decision = resolve(PlacementRequest(kind=kind, domain=DOMAIN_DEV))
        assert decision.placed, f"{kind} did not place: {decision.evidence()}"
        assert decision.result is not None
        assert decision.result.canonical_namespace == namespace


def test_a_dev_artifact_about_the_payload_is_still_dev_owned():
    """PC-5: 'about the Protocol' is not 'owned by the Protocol'."""
    decision = resolve(PlacementRequest(kind="plan", domain=DOMAIN_DEV))
    assert decision.placed
    assert decision.result is not None
    assert decision.result.canonical_namespace == "docs/plans"


# --- Discriminator 2: kind / family -----------------------------------------


def test_known_kinds_resolve_to_their_published_namespace():
    expected = {
        "policy": "docs",
        "rfc": "docs/rfc",
        "adr": "docs/adr",
        "plan": "docs/plans",
        "working": "docs/working",
        "glossary": "docs/glossary",
        "tool": "tools",
        "runtime": "runtime",
        "test": "tests",
    }
    for kind, namespace in expected.items():
        decision = resolve(PlacementRequest(kind=kind, domain=DOMAIN_DEV))
        assert decision.placed, f"{kind} did not place: {decision.evidence()}"
        assert decision.result is not None
        assert decision.result.canonical_namespace == namespace


def test_unnameable_kind_stops():
    assert _stop_reason(PlacementRequest(kind="   ")) is PlacementStop.UNKNOWN_KIND


def test_unknown_kind_stops_as_new_family_and_never_guesses_a_neighbour():
    """Falsification: 'spec' looks like it belongs with the plans, but no rule
    authorizes that, so the resolver must refuse rather than approximate."""
    reason = _stop_reason(PlacementRequest(kind="spec", domain=DOMAIN_DEV))
    assert reason is PlacementStop.NEW_FAMILY


def test_an_unasserted_domain_is_never_broken_by_an_arbitrary_tie_break():
    """Falsification: with the domain unasserted the resolver may place, but it
    must never pick between defensible readings by an undocumented preference.
    Repeating the resolution must yield byte-identical evidence."""
    request = PlacementRequest(kind="harness")
    decisions = [resolve(request) for _ in range(5)]
    assert len({d.evidence() for d in decisions}) == 1
    assert decisions[0].outcome is PlacementOutcome.STOP


# --- Qualifier: canonicality never selects a namespace ----------------------


def test_canonicality_does_not_change_the_selected_namespace():
    """Switching a qualifier must not move the artifact between namespaces."""
    base = resolve(PlacementRequest(kind="adr", domain=DOMAIN_DEV))
    derived = resolve(
        PlacementRequest(kind="adr", domain=DOMAIN_DEV, canonicality="derived")
    )
    assert base.result is not None and derived.result is not None
    assert base.result.canonical_namespace == derived.result.canonical_namespace


def test_generated_without_a_designated_location_stops():
    """PC-47: generated has no default; it is not 'outside canonical state'."""
    reason = _stop_reason(
        PlacementRequest(kind="adr", domain=DOMAIN_DEV, canonicality="generated")
    )
    assert reason is PlacementStop.UNDEFINED_PLACEMENT


def test_generated_with_a_designated_location_places():
    """A family rule that designates a location makes generated content placeable."""
    decision = resolve(
        PlacementRequest(
            kind="run-log", domain=DOMAIN_PROTOCOL, canonicality="generated"
        )
    )
    assert decision.placed
    assert decision.result is not None
    assert decision.result.canonical_namespace == ".project/orchestrator"


def test_scratch_never_lands_in_a_canonical_namespace():
    reason = _stop_reason(
        PlacementRequest(kind="adr", domain=DOMAIN_DEV, canonicality="scratch")
    )
    assert reason is PlacementStop.UNDEFINED_PLACEMENT


def test_fixture_belongs_to_the_test_subsystem_namespace():
    decision = resolve(
        PlacementRequest(kind="fixture", domain=DOMAIN_DEV, canonicality="fixture")
    )
    assert decision.placed
    assert decision.result is not None
    assert decision.result.canonical_namespace == "tests/fixtures"


def test_frozen_historical_artifact_retains_its_existing_location():
    """PC-39/PC-41: a frozen artifact keeps where it is; that is not a rule."""
    decision = resolve(
        PlacementRequest(
            kind="adr",
            domain=DOMAIN_DEV,
            canonicality="historical",
            frozen=True,
            path="docs/working/research/legacy-decision.md",
        )
    )
    assert decision.placed
    assert decision.result is not None
    assert decision.result.canonical_namespace == "docs/working/research/legacy-decision.md"


def test_historical_is_not_a_licence_to_keep_any_location():
    """Falsification: without the frozen lifecycle established, an arbitrary
    path must not become canonical merely by being labelled historical."""
    reason = _stop_reason(
        PlacementRequest(
            kind="adr",
            domain=DOMAIN_DEV,
            canonicality="historical",
            path="docs/working/research/legacy-decision.md",
        )
    )
    assert reason is PlacementStop.UNDEFINED_PLACEMENT


def test_a_new_artifact_never_uses_the_historical_shortcut():
    """PC-41: the historical location of an old artifact is not a rule for a new
    one, so a new artifact at that path is still refused."""
    reason = _stop_reason(
        PlacementRequest(
            kind="adr",
            domain=DOMAIN_DEV,
            path="docs/working/research/new-decision.md",
        )
    )
    assert reason is PlacementStop.INVALID_PLACEMENT


def test_historical_without_a_location_stops():
    reason = _stop_reason(
        PlacementRequest(kind="adr", domain=DOMAIN_DEV, canonicality="historical")
    )
    assert reason is PlacementStop.UNDEFINED_PLACEMENT


def test_unknown_canonicality_status_stops():
    reason = _stop_reason(
        PlacementRequest(kind="adr", domain=DOMAIN_DEV, canonicality="temporary")
    )
    assert reason is PlacementStop.UNDEFINED_PLACEMENT


# --- Verification (§16 PC-51) -----------------------------------------------


def test_valid_path_is_verified():
    decision = verify_path(
        PlacementRequest(kind="adr", domain=DOMAIN_DEV, path="docs/adr/18-x.md")
    )
    assert decision.placed
    assert decision.result is not None
    assert decision.result.path_verified


def test_invalid_path_stops():
    reason = _stop_reason(
        PlacementRequest(kind="adr", domain=DOMAIN_DEV, path="docs/plans/18-x.md")
    )
    assert reason is PlacementStop.INVALID_PLACEMENT


def test_a_declared_exception_makes_the_non_canonical_path_admissible():
    decision = verify_path(
        PlacementRequest(
            kind="adr",
            domain=DOMAIN_DEV,
            path="docs/plans/analysis.md",
            authorized_exceptions=("docs/plans",),
        )
    )
    assert decision.placed


def test_an_exception_never_authorizes_a_path_outside_itself():
    """PC-27: bounded to the artifact or family, never to a namespace class."""
    reason = _stop_reason(
        PlacementRequest(
            kind="adr",
            domain=DOMAIN_DEV,
            path="runtime/rogue.py",
            authorized_exceptions=("docs/plans",),
        )
    )
    assert reason is PlacementStop.UNRESOLVED_EXCEPTION


def test_verification_without_a_path_stops():
    reason = _stop_reason(
        verify_path(PlacementRequest(kind="adr", domain=DOMAIN_DEV))
    )
    assert reason is PlacementStop.INVALID_PLACEMENT


# --- Constraints ------------------------------------------------------------


def test_payload_dependency_on_dev_stops():
    reason = _stop_reason(
        PlacementRequest(
            kind="contract",
            domain=DOMAIN_PROTOCOL,
            declares_payload_dependency=True,
        )
    )
    assert reason is PlacementStop.CONSTRAINT_VIOLATION


def test_unresolved_authority_stops():
    reason = _stop_reason(
        PlacementRequest(kind="adr", domain=DOMAIN_DEV, authority_resolved=False)
    )
    assert reason is PlacementStop.AUTHORITY_UNRESOLVED


# --- Determinism and provenance ---------------------------------------------


def test_resolution_is_deterministic():
    request = PlacementRequest(kind="plan", domain=DOMAIN_DEV)
    decisions = [resolve(request) for _ in range(5)]
    assert len({d.result.canonical_namespace for d in decisions if d.result}) == 1
    assert len({d.evidence() for d in decisions}) == 1


def test_place_evidence_names_the_rule_and_the_qualifier():
    decision = resolve(PlacementRequest(kind="adr", domain=DOMAIN_DEV))
    evidence = " | ".join(decision.evidence())
    assert "domain=DEV" in evidence
    assert "family=ADR" in evidence
    assert "docs/placement-contract.md" in evidence
    assert "canonicality" in evidence


def test_stop_evidence_names_the_reason_and_the_contract():
    decision = resolve(PlacementRequest(kind="spec", domain=DOMAIN_DEV))
    evidence = " | ".join(decision.evidence())
    assert "NEW_FAMILY" in evidence
    assert "docs/placement-contract.md" in evidence
    assert decision.refusal is not None
    assert decision.refusal.required


def test_a_plausible_but_unauthorized_location_is_never_placed():
    """Falsification: 'docs/specs' resembles 'docs/plans', but resemblance is
    not an authorization, so the resolver must not invent the namespace."""
    decision = verify_path(
        PlacementRequest(kind="spec", domain=DOMAIN_DEV, path="docs/specs/x.md")
    )
    assert decision.outcome is PlacementOutcome.STOP
    assert decision.refusal is not None
    assert decision.refusal.reason is PlacementStop.NEW_FAMILY
