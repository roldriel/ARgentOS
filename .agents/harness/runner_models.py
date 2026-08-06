"""Result dataclasses for the harness runner."""

from __future__ import annotations

import sys
from pathlib import Path

_HARNESS_DIR = Path(__file__).resolve().parent
if str(_HARNESS_DIR) not in sys.path:
    sys.path.insert(0, str(_HARNESS_DIR))

from dataclasses import dataclass, field
from typing import Any


@dataclass
class CheckResult:
    id: str
    result: str  # PASS or FAIL
    evidence: str


@dataclass
class HarnessResult:
    trigger: str
    transition: str
    result: str  # PASS or FAIL
    checks: list[CheckResult] = field(default_factory=list)
    artifact: str | None = None
    report: str | None = None
    timestamp: str = ""
    error: str | None = None
    duration_ms: int = 0
    rubric_scores: dict[str, str] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "trigger": self.trigger,
            "transition": self.transition,
            "result": self.result,
            "checks": [
                {"id": c.id, "result": c.result, "evidence": c.evidence}
                for c in self.checks
            ],
            "artifact": self.artifact,
            "report": self.report,
            "timestamp": self.timestamp,
            "error": self.error,
            "duration_ms": self.duration_ms,
            "rubric_scores": self.rubric_scores,
        }
