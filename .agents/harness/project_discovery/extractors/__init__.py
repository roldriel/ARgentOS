"""Project file extractors."""

from __future__ import annotations

from .base import Extractor
from .container import ContainerExtractor
from .generic import GenericExtractor
from .node import NodeExtractor
from .python import PythonExtractor

DEFAULT_EXTRACTORS: list[type[Extractor]] = [
    PythonExtractor,
    NodeExtractor,
    ContainerExtractor,
    GenericExtractor,
]

__all__ = [
    "Extractor",
    "PythonExtractor",
    "NodeExtractor",
    "ContainerExtractor",
    "GenericExtractor",
    "DEFAULT_EXTRACTORS",
]
