"""FC-6 / ``ID-8`` (plan 165): the retry discrepancy is **resolved by aligning the policy** with the code.

The declared discrepancy was: the policy enumerated ``retry`` among what the host may do inside the
scope, while the code implements **no** retry mechanism — a failure that requires redoing authorized
work is conducted as a **new derivation** over the observed state. ``ID-8`` chose to align the policy
with the code instead of implementing a retry with a lifecycle of its own.

This suite is the lockstep: it fails if either surface drifts back (policy claiming an internal retry,
or the behaviour notes claiming a live discrepancy), and its verifier is a **detector** — a text that
carries the old claims is rejected (counterproof matrix, ``FC-7``).

Anchored to the real repository on purpose (``tests/AGENTS.md``): the aligned wording *is* repository
state. Read-only; documentation only; never the ``protocol/`` payload.
"""

from __future__ import annotations

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]

POLICY = Path(".agents") / "policies" / "supervised-autonomous-execution.md"
NOTES = Path("docs") / "behavior-patterns.md"

#: What the policy must declare (compared on normalized, lowercased text).
POLICY_REQUIRED = (
    "no internal retry with its own lifecycle is implemented",
    "conducted as a new derivation",
)
#: What the policy must no longer claim.
POLICY_FORBIDDEN = (
    "correct, retry and recover inside the scope",
    "correct / retry",
    "recovery and retries are never hidden",
)
#: What the behaviour notes must declare, and must no longer declare.
NOTES_REQUIRED = (
    "la política está alineada con el código",
    "nueva derivación",
)
NOTES_FORBIDDEN = (
    "discrepancia declarada con la",
    "la política **sí** enumera el retry",
)


def _normalize(text: str) -> str:
    """Lowercase, drop markdown emphasis and collapse whitespace."""
    for token in ("**", "`", "*"):
        text = text.replace(token, " ")
    return " ".join(text.lower().split())


def violations(policy_text: str, notes_text: str) -> list[str]:
    """Reasons the two surfaces do NOT carry the aligned retry semantics."""
    policy = _normalize(policy_text)
    notes = _normalize(notes_text)
    problems = [f"policy missing: {c}" for c in POLICY_REQUIRED if c not in policy]
    problems += [f"policy still claims: {c}" for c in POLICY_FORBIDDEN if c in policy]
    problems += [f"notes missing: {c}" for c in NOTES_REQUIRED if c not in notes]
    problems += [f"notes still claim: {c}" for c in NOTES_FORBIDDEN if c in notes]
    return problems


def _read(relative: Path) -> str:
    return (REPO_ROOT / relative).read_text(encoding="utf-8")


def test_policy_and_behaviour_notes_are_in_lockstep() -> None:
    problems = violations(_read(POLICY), _read(NOTES))
    assert problems == [], problems


def test_verifier_rejects_the_old_policy_claim() -> None:
    """Counterproof: the policy enumerating an internal retry is rejected."""
    old_policy = (
        "Inside the envelope the host may correct, retry and recover inside the scope. "
        "failure -> diagnose -> correct / retry -> verify -> continue "
        "Recovery and retries are never hidden."
    )
    problems = violations(old_policy, "la política está alineada con el código y usa una nueva derivación")
    assert any(p.startswith("policy still claims") for p in problems), problems
    assert any(p.startswith("policy missing") for p in problems), problems


def test_verifier_rejects_a_live_discrepancy() -> None:
    """Counterproof: notes declaring the discrepancy unresolved are rejected."""
    notes = (
        "No hay un mecanismo de retry, y esto es una discrepancia declarada con la política. "
        "La política **sí** enumera el retry entre lo que el host puede hacer."
    )
    problems = violations(_read(POLICY), notes)
    assert any(p.startswith("notes still claim") for p in problems), problems


def test_recovery_does_not_expand_the_envelope() -> None:
    """The recovery text must keep the STOP on new scope/authority (envelope unchanged)."""
    policy = " ".join(_read(POLICY).lower().split())
    assert "a recovery that needs a new scope, new" in policy
    assert "authority, an rfc, an adr, a protocol change or a payload change **stops**" in policy
