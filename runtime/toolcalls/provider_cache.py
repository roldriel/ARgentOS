"""Provider Prompt Cache capability boundary for the reference runtime.

Implements RFC-72 sections 6-8: the abstract provider capability contract,
the Provider Adapter boundary, the opaque `ProviderCacheReference`, and a
null adapter for tests and default (RFC-72, section 13: a provider that does
not support prompt caching means cache unavailable, while the materialization
and the semantic context stay valid).

This is the first provider abstraction in the repository (plan 89, U3). It is
deliberately minimal: no concrete provider API, no pricing, no universal TTL
or eviction, no telemetry (RFC-74). The adapter owns all provider-specific
semantics; ARgentOS consumes only the abstract capability and the opaque
reference.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass

_MECHANISMS = frozenset({"none", "implicit", "explicit"})
_ISOLATION_SCOPES = frozenset({"account", "org", "project"})
_CACHE_RESULTS = frozenset({"hit", "miss", "unavailable"})


@dataclass(frozen=True)
class ProviderCapability:
    """Abstract prompt-cache capability of a provider (RFC-72, section 6).

    Exact fields of the RFC's abstract contract:

    - `mechanism`: `none` | `implicit` | `explicit`.
    - `prefix_only`: whether only prefix reuse is supported.
    - `breakpoints`: whether explicit cache breakpoints are supported.
    - `min_cacheable_tokens`: the provider's minimum prefix size.
    - `ttl`: `(min, max)`; `None` on either side means unbounded.
    - `extended_ttl`: whether extended TTL is supported.
    - `model_scoped`: whether the provider cache is scoped per model.
    - `isolation_scope`: `account` | `org` | `project`.

    The capability describes what the provider supports; it says nothing
    about whether ARgentOS attempts or the provider effectively uses the
    cache (I-MAT-008).
    """

    mechanism: str
    prefix_only: bool
    breakpoints: bool
    min_cacheable_tokens: int
    ttl: tuple[int | None, int | None]
    extended_ttl: bool
    model_scoped: bool
    isolation_scope: str

    def __post_init__(self) -> None:
        if self.mechanism not in _MECHANISMS:
            raise ValueError(
                f"invalid mechanism {self.mechanism!r} "
                f"(allowed: {sorted(_MECHANISMS)})"
            )
        if self.isolation_scope not in _ISOLATION_SCOPES:
            raise ValueError(
                f"invalid isolation scope {self.isolation_scope!r} "
                f"(allowed: {sorted(_ISOLATION_SCOPES)})"
            )
        if self.min_cacheable_tokens < 0:
            raise ValueError("min_cacheable_tokens must be non-negative")
        if len(self.ttl) != 2:
            raise ValueError("ttl must be a (min, max) pair")
        for bound in self.ttl:
            if bound is not None and bound < 0:
                raise ValueError("ttl bounds must be non-negative or None")


@dataclass(frozen=True)
class ProviderCacheReference:
    """Opaque reference to provider-owned cache state (RFC-72, section 8).

    ARgentOS does not interpret `opaque`; the provider/adapter creates,
    returns, changes, expires, invalidates or replaces it. The reference is
    retained only as observability/diagnostic/correlation metadata and is
    never an authority of correctness (I-MAT-004).
    """

    opaque: str


@dataclass(frozen=True)
class ProviderResponse:
    """The adapter's answer to a request (RFC-72, sections 7 and 9)."""

    reference: ProviderCacheReference | None
    cache_result: str  # "hit" | "miss" | "unavailable"

    def __post_init__(self) -> None:
        if self.cache_result not in _CACHE_RESULTS:
            raise ValueError(
                f"invalid cache result {self.cache_result!r} "
                f"(allowed: {sorted(_CACHE_RESULTS)})"
            )


class ProviderAdapter(ABC):
    """Provider Adapter boundary (RFC-72, section 7).

    Every provider-specific behavior stays behind this boundary. ARgentOS
    knows the abstract capability and consumes the materialized
    representation; the adapter knows the provider API; the provider owns its
    cache.
    """

    @abstractmethod
    def capability(self) -> ProviderCapability:
        """The provider's abstract prompt-cache capability."""

    @abstractmethod
    def request(
        self,
        prompt: bytes,
        reference: ProviderCacheReference | None,
    ) -> ProviderResponse:
        """Send a materialized prompt and observe the cache result.

        `reference` is the previously returned opaque reference, if any.
        A provider failure degrades optimization, never semantic correctness
        (RFC-72, section 13): the adapter reports `unavailable` instead of
        raising when caching is the only concern.
        """


class NullProviderAdapter(ProviderAdapter):
    """Adapter for providers without prompt-cache support (mechanism `none`).

    Default and tests (RFC-72, section 13): cache is unavailable, the
    materialization and the semantic context remain valid. No network calls.
    """

    def capability(self) -> ProviderCapability:
        return ProviderCapability(
            mechanism="none",
            prefix_only=False,
            breakpoints=False,
            min_cacheable_tokens=0,
            ttl=(None, None),
            extended_ttl=False,
            model_scoped=False,
            isolation_scope="account",
        )

    def request(
        self,
        prompt: bytes,
        reference: ProviderCacheReference | None,
    ) -> ProviderResponse:
        return ProviderResponse(reference=None, cache_result="unavailable")
