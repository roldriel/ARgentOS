"""Shared test configuration for the harness test suite."""

from __future__ import annotations

import sys
from pathlib import Path

_harness_dir = Path(__file__).resolve().parents[1]
if str(_harness_dir) not in sys.path:
    sys.path.insert(0, str(_harness_dir))
