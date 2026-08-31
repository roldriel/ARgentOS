"""Provider cache coordination for the reference runtime (RFC-72).

Implements the runtime flow of RFC-72 sections 9-11: lookup, hit/miss,
request, reference update, invalidation in the three non-conflatable domains
(semantic, materialization, provider), and the admission boundary as a policy
without thresholds.

This is a runtime component with deterministic behavior, not a protocol state
machine: it never writes telemetry (RFC-74), never persists state (RFC-73),
and a provider failure degrades optimization, never semantic correctness
(RFC-72, section 13). References are in-memory metadata only.

Invalidation domains map mechanically onto the lookup key
`(SemanticContextIdentity, MaterializationIdentity)`:

- semantic change: a different SCI produces a different key -> miss/rebuild;
- materialization change: a different MI produces a different key ->
  miss/rebuild;
- provider eviction / TTL / unavailability: the adapter reports `miss` or
  `unavailable` for the same key -> miss without semantic effect.
"""

from __future__ import annotations

from dataclasses import dataclass

from .identity import SemanticContextIdentity
from .provider_cache import (
    ProviderAdapter,
    ProviderCapability,
    ProviderCacheReference,
    ProviderResponse,
)


@dataclass(frozen=True)
class CacheLookup:
    """Outcome of a provider cache lookup (RFC-72, section 9).

    HIT/MISS/UNAVAILABLE describes provider cache state, never semantic
    validity: a hit or a miss does not determine whether the semantic context
    is valid (I-MAT-005).
    """

    result: str  # "HIT" | "MISS" | "UNAVAILABLE"
    reference: ProviderCacheReference | None


HIT = "HIT"
MISS = "MISS"
UNAVAILABLE = "UNAVAILABLE"

_RESULT_BY_CACHE_RESULT = {
    "hit": HIT,
    "miss": MISS,
    "unavailable": UNAVAILABLE,
}


def admission_policy(
    eligible: bool,
    capability: ProviderCapability,
) -> bool:
    """Admission boundary: whether ARgentOS should attempt prompt caching.

    A decision boundary without thresholds (RFC-72, section 11): `reuse >= 3`
    is not an invariant and no TTL, token-count or reuse-count threshold is
    applied here. Economic thresholds require telemetry evidence and belong
    to RFC-74. The boundary only requires semantic eligibility and an
    adapter that supports a mechanism.
    """
    return eligible and capability.mechanism != "none"


class ProviderCacheCoordinator:
    """Coordinates provider cache lookups for the reference runtime.

    State is in-memory only: the latest opaque reference per
    `(SemanticContextIdentity, MaterializationIdentity)`. Conceptual events
    (RFC-72, section 14: cache eligible | admitted | requested | hit | miss |
    unavailable) are exposed as coordinator metadata; they are not telemetry.
    """

    def __init__(self) -> None:
        self._references: dict[
            tuple[SemanticContextIdentity, str], ProviderCacheReference
        ] = {}
        self._events: list[str] = []

    @property
    def events(self) -> tuple[str, ...]:
        """Conceptual cache events emitted so far, in order (metadata)."""
        return tuple(self._events)

    def request(
        self,
        adapter: ProviderAdapter,
        sci: SemanticContextIdentity,
        mi: str,
        payload: bytes,
    ) -> ProviderResponse:
        """Perform the provider request under the current lookup key."""
        self._events.append("cache requested")
        reference = self._references.get((sci, mi))
        return adapter.request(payload, reference)

    def update_reference(
        self,
        sci: SemanticContextIdentity,
        mi: str,
        response: ProviderResponse,
    ) -> None:
        """Record the provider's latest reference for this lookup key.

        The provider owns the reference: it may create, change, expire,
        invalidate or replace it. A response without a reference clears the
        stored one; a response with a reference replaces it. This metadata is
        never an authority of correctness (I-MAT-004).
        """
        if response.reference is None:
            self._references.pop((sci, mi), None)
        else:
            self._references[(sci, mi)] = response.reference

    def lookup(
        self,
        adapter: ProviderAdapter,
        sci: SemanticContextIdentity,
        mi: str,
        payload: bytes,
    ) -> CacheLookup:
        """Run the lookup -> hit/miss -> request -> reference update flow.

        `payload` is the canonical materialization payload directed at the
        provider (RFC-72, section 7). A failure of the cache degrades
        optimization only: the semantic context is never invalidated here.
        """
        capability = adapter.capability()
        eligible = capability.mechanism != "none"
        if not eligible:
            self._events.append("cache unavailable")
            return CacheLookup(UNAVAILABLE, None)

        self._events.append("cache eligible")
        if not admission_policy(eligible, capability):
            self._events.append("cache unavailable")
            return CacheLookup(UNAVAILABLE, None)
        self._events.append("cache admitted")

        response = self.request(adapter, sci, mi, payload)
        self.update_reference(sci, mi, response)
        result = _RESULT_BY_CACHE_RESULT[response.cache_result]
        self._events.append(f"cache {response.cache_result}")
        return CacheLookup(result=result, reference=response.reference)
