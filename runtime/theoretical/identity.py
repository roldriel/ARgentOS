"""Identity and provenance primitives of Theoretical Execution (DEV v1).

The design distinguishes two identities and refuses a third:

``InputIdentity``
    What was evaluated: the factual base, the declared overlay, the tool version
    and the check-set.  Deterministic and the only thing staleness depends on.
``RunIdentity`` (``te_id``)
    Which run produced this result: the input identity plus the declared
    producer, timestamp and nonce.  A label, never an identity of content.
``ResultContentIdentity``
    Deliberately absent.  Semantic findings depend on the producer; comparing
    two runs is a canonical-JSON comparison, not an identity claim.

No new identity primitive is introduced: the factual identity is made of Git
commit/tree ids and the projected identity is the structured declaration.
"""

from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from typing import Any, Mapping, Sequence

from .overlay import BaseState, DeclaredOverlay

TOOL_VERSION = "1"

CHECK_SET: tuple[tuple[str, str], ...] = (
    ("CH-1", "1"),
    ("CH-2", "1"),
    ("CH-3", "1"),
    ("CH-4", "1"),
    ("CH-5", "1"),
    ("CH-6", "1"),
    ("CH-7", "1"),
    ("CH-8", "1"),
)

CHECK_SET_VERSION: tuple[str, ...] = tuple(f"{name}:{version}" for name, version in CHECK_SET)


def canonical_json(payload: Any) -> str:
    """Deterministic JSON text: sorted keys, 2-space indent, LF, trailing LF."""
    return json.dumps(payload, sort_keys=True, indent=2, ensure_ascii=False) + "\n"


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z")


def factual_identity(base: BaseState) -> dict[str, str]:
    return {"commit": base.commit, "tree": base.tree}


def projected_identity(overlay: DeclaredOverlay) -> dict[str, Any]:
    return {
        "kind": "declared_overlay",
        "base": factual_identity(overlay.base),
        "paths": list(overlay.paths()),
        "effects": sorted(overlay.effects),
        "content": "unknown",
    }


def check_set_payload(check_set: Sequence[tuple[str, str]] = CHECK_SET) -> list[dict[str, str]]:
    return [{"id": name, "version": version} for name, version in check_set]


def input_identity(
    base: BaseState,
    overlay: DeclaredOverlay,
    *,
    tool_version: str = TOOL_VERSION,
    check_set: Sequence[tuple[str, str]] = CHECK_SET,
) -> dict[str, Any]:
    return {
        "factual": factual_identity(base),
        "projected": projected_identity(overlay),
        "tool_version": tool_version,
        "check_set": check_set_payload(check_set),
    }


def _slug(value: str) -> str:
    cleaned = "".join(ch.lower() if ch.isalnum() else "-" for ch in value.strip())
    while "--" in cleaned:
        cleaned = cleaned.replace("--", "-")
    return cleaned.strip("-") or "unknown"


def run_identity(
    inputs: Mapping[str, Any],
    *,
    plan: int,
    producer: str,
    created_at: str | None = None,
    nonce: str | None = None,
) -> dict[str, Any]:
    """Build the ``RunIdentity`` label.

    ``nonce`` and ``created_at`` are injectable so tests can be deterministic.
    The label is *not* an identity of the result: two runs over the same inputs
    may legitimately differ in their semantic findings.
    """
    created = created_at or utc_now()
    if nonce is None:
        nonce = hashlib.sha256(
            f"{created}:{producer}:{plan}:{id(inputs)}".encode("utf-8")
        ).hexdigest()[:8]
    factual = inputs.get("factual", {}) if isinstance(inputs, Mapping) else {}
    commit = str(factual.get("commit", ""))[:12]
    compact = created.replace("-", "").replace(":", "").replace("Z", "")
    te_id = f"te-{plan}-{commit}-{_slug(producer)}-{compact}-{nonce}"
    return {
        "te_id": te_id,
        "input_identity": dict(inputs),
        "producer": producer,
        "created_at": created,
        "nonce": nonce,
    }


def identity_payload(
    base: BaseState,
    overlay: DeclaredOverlay,
    *,
    plan: int,
    producer: str,
    created_at: str | None = None,
    nonce: str | None = None,
    tool_version: str = TOOL_VERSION,
    check_set: Sequence[tuple[str, str]] = CHECK_SET,
) -> dict[str, Any]:
    inputs = input_identity(
        base,
        overlay,
        tool_version=tool_version,
        check_set=check_set,
    )
    return {
        "factual": factual_identity(base),
        "projected": projected_identity(overlay),
        "inputs": inputs,
        "run": run_identity(
            inputs,
            plan=plan,
            producer=producer,
            created_at=created_at,
            nonce=nonce,
        ),
    }
