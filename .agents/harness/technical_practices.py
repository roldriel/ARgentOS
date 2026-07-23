"""Canonical catalog of technical practices (single source of truth).

Every technical-practice feature flag is declared here exactly once, together
with its rubric and its standard document. `runner.py`, `health_check.py` and
`feature_flags.py` derive their views from this catalog; adding a practice
requires editing only this file (plus its standard, rubric and flag default).
"""

from __future__ import annotations

from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
AGENTS_DIR = PROJECT_ROOT / ".agents"

_DESIGN = AGENTS_DIR / "standards" / "development" / "design"

# flag -> (rubric name, standard document)
TECHNICAL_PRACTICES: dict[str, tuple[str, Path]] = {
    "tdd": ("TDD_RUBRIC", AGENTS_DIR / "standards" / "testing" / "TDD.md"),
    "srp": ("SRP_RUBRIC", _DESIGN / "SOLID" / "SRP.md"),
    "ocp": ("OCP_RUBRIC", _DESIGN / "SOLID" / "OCP.md"),
    "lsp": ("LSP_RUBRIC", _DESIGN / "SOLID" / "LSP.md"),
    "isp": ("ISP_RUBRIC", _DESIGN / "SOLID" / "ISP.md"),
    "dip": ("DIP_RUBRIC", _DESIGN / "SOLID" / "DIP.md"),
    "screaming_architecture": (
        "SCREAMING_ARCHITECTURE_RUBRIC",
        _DESIGN / "SCREAMING_ARCHITECTURE.md",
    ),
    "clean_architecture": ("CLEAN_ARCHITECTURE_RUBRIC", _DESIGN / "CLEAN_ARCHITECTURE.md"),
    "dry": ("DRY_RUBRIC", _DESIGN / "DRY.md"),
    "layered_architecture": ("LAYERED_ARCHITECTURE_RUBRIC", _DESIGN / "LAYERED_ARCHITECTURE.md"),
    "grasp": ("GRASP_RUBRIC", _DESIGN / "GRASP.md"),
    "ddd_tactical": ("DDD_TACTICAL_RUBRIC", _DESIGN / "DDD_TACTICAL.md"),
    "ddd_strategic": ("DDD_STRATEGIC_RUBRIC", _DESIGN / "DDD_STRATEGIC.md"),
}

TECHNICAL_PRACTICE_FLAGS: set[str] = set(TECHNICAL_PRACTICES)

TECHNICAL_PRACTICE_RUBRIC_MAP: dict[str, str] = {
    flag: rubric for flag, (rubric, _path) in TECHNICAL_PRACTICES.items()
}

TECHNICAL_PRACTICE_STANDARDS: dict[str, Path] = {
    flag: path for flag, (_rubric, path) in TECHNICAL_PRACTICES.items()
}
