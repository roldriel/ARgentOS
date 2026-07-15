"""Project discovery for the .agents protocol."""

from __future__ import annotations

from .discovery import run_discovery
from .writers import write_kb_entries

__all__ = ["run_discovery", "write_kb_entries"]
