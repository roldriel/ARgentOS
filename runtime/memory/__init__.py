"""Reference runtime for the Memory System (RFC-80, Plan 150).

Placement ``ADAPT`` (Plan 150 Phase 0): the persistent memory data lives under
``.project/knowledge/`` (the existing ``Project-durable knowledge base`` family,
``docs/placement-contract.md`` §6); the runtime code lives here (the existing
``Reference runtime`` family, ``runtime/<package>/``). The store is derived and
rebuildable, never authoritative (RFC-80 §18 / I-011 / I-012).
"""

from .store import MemoryStore, atomic_write, canonical_json

__all__ = ["MemoryStore", "atomic_write", "canonical_json"]
