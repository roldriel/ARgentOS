"""Base extractor protocol."""

from __future__ import annotations

from abc import ABC, abstractmethod
from pathlib import Path

from ..models import DiscoveryResult


class Extractor(ABC):
    """Base class for project file extractors."""

    @property
    @abstractmethod
    def filenames(self) -> set[str]:
        """File names this extractor can handle."""
        ...

    def can_handle(self, path: Path) -> bool:
        """Return True if this extractor handles the given path."""
        return path.name in self.filenames

    @abstractmethod
    def extract(self, path: Path, result: DiscoveryResult) -> None:
        """Extract facts from ``path`` and add them to ``result``."""
        ...
