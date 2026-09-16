"""Mechanical realization of the Placement Contract (DEV, plan 131).

Answers one question — *where does this artifact belong?* — with ``PLACE`` or
``STOP``, never a guess. The normative source is ``docs/placement-contract.md``;
this package consumes it and never replaces it (``PC-64``/``PC-75``).

Public surface:

- :class:`PlacementRequest` / :class:`PlacementDecision` — the resolver's I/O.
- :func:`resolve` — the §7 algorithm.
- :func:`verify_path` — the §16 (``PC-51``) location check.
"""

from .resolver import (
    PlacementDecision,
    PlacementOutcome,
    PlacementRefusal,
    PlacementRequest,
    PlacementResult,
    PlacementStop,
    resolve,
    verify_path,
)
from .rules import CONTRACT_PATH, DOMAIN_DEV, DOMAIN_PROTOCOL, DOMAINS

__all__ = [
    "CONTRACT_PATH",
    "DOMAINS",
    "DOMAIN_DEV",
    "DOMAIN_PROTOCOL",
    "PlacementDecision",
    "PlacementOutcome",
    "PlacementRefusal",
    "PlacementRequest",
    "PlacementResult",
    "PlacementStop",
    "resolve",
    "verify_path",
]
