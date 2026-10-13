"""FC-2 (plan 165, decision ``ID-3``): the declared absence of isolation is published and verifiable.

``ID-3`` is normative: **ARgentOS does not provide isolation for the actor**. Plan 165 designates two
publication surfaces. This suite verifies that the declaration is present in both and — more to the
point — that the verifier is a **detector**: a text that omits the declaration, or that claims an
isolation guarantee, is **rejected** (falsification, ``FC-7``).

Anchored to the real repository on purpose: the published declaration *is* repository state, so the
suite names the canonical paths and must be updated when that state legitimately changes
(``tests/AGENTS.md``). It reads documentation only: no runtime code, no ``protocol/`` payload.
"""

from __future__ import annotations

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]

#: The two surfaces Plan 165 designates for publishing the declaration.
SURFACES = (
    Path("runtime") / "README.md",
    Path(".agents") / "policies" / "supervised-autonomous-execution.md",
)

#: Clauses the declaration must carry (compared on whitespace-normalized, lowercased text).
REQUIRED_CLAUSES = (
    "does not provide isolation for the actor",
    "prevention where the host controls the effect",
    "detection where it does not",
    "not an isolation guarantee",
)

#: Claims that contradict the declared absence (a text carrying them is not a valid declaration).
FORBIDDEN_CLAIMS = (
    "provides isolation for the actor",
    "guarantees isolation",
    "sandbox is provided",
)


def violations(text: str) -> list[str]:
    """Reasons ``text`` does NOT carry the declared absence of isolation."""
    normalized = " ".join(text.lower().split())
    problems = [
        f"missing clause: {clause}"
        for clause in REQUIRED_CLAUSES
        if clause not in normalized
    ]
    problems += [
        f"forbidden claim: {claim}"
        for claim in FORBIDDEN_CLAIMS
        if claim in normalized
    ]
    return problems


def test_declaration_is_published_in_every_designated_surface() -> None:
    for relative in SURFACES:
        text = (REPO_ROOT / relative).read_text(encoding="utf-8")
        problems = violations(text)
        assert problems == [], f"{relative}: {problems}"


def test_verifier_rejects_a_text_that_omits_the_declaration() -> None:
    """Counterproof: a plausible 'declared limits' text without the declaration is rejected."""
    assert violations("Declared limits: no provider, no model, no network.") != []


def test_verifier_rejects_an_isolation_guarantee() -> None:
    """Counterproof: claiming isolation is rejected even if the rest of the wording is present."""
    text = (
        "ARgentOS provides isolation for the actor and runs the agent inside a sandbox. "
        "It is not an isolation guarantee."
    )
    problems = violations(text)
    assert any(p.startswith("forbidden claim") for p in problems), problems


def test_declaration_keeps_the_frontier_distinction() -> None:
    """The absence of isolation must not be read as 'the frontier does nothing'."""
    policy = " ".join(
        (REPO_ROOT / SURFACES[1]).read_text(encoding="utf-8").lower().split()
    )
    assert "prevention where the host controls the effect" in policy
    assert "detection where it does not" in policy
