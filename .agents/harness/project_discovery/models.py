"""Data models for project discovery."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(frozen=True)
class Fact:
    """A single discovered fact about the project."""

    category: str
    key: str
    value: Any
    source_file: str
    confidence: str = "deterministic"  # deterministic | synthesized

    def to_dict(self) -> dict[str, Any]:
        return {
            "category": self.category,
            "key": self.key,
            "value": self.value,
            "source_file": self.source_file,
            "confidence": self.confidence,
        }


@dataclass
class DiscoveryResult:
    """Aggregated discovery facts for a project."""

    facts: list[Fact] = field(default_factory=list)

    def add(self, fact: Fact) -> None:
        self.facts.append(fact)

    def by_category(self, category: str) -> list[Fact]:
        return [f for f in self.facts if f.category == category]

    def to_dict(self) -> dict[str, Any]:
        return {"facts": [f.to_dict() for f in self.facts]}
