"""Context Budget estimation for the reference runtime.

The prompt runtime materializes the Context Budget in estimated tokens with
the rule `ceil(chars / 4)` (`protocol/.agents/standards/context/BUDGET_MATERIALIZATION.md`,
sections 1-2). That standard explicitly allows other runtimes to declare
their own unit and estimation rule (same document, section 6); the tool-call
runtime declares a dual unit: estimated tokens for the textual portion plus
a count of tool declarations for the invocable portion. What does not change:
the Budget is finite and every materialized value is a finite, positive
ceiling in the declared unit.
"""

from __future__ import annotations

import math
from dataclasses import dataclass


def estimate_tokens(text: str) -> int:
    """Estimate the token cost of a text: ceil(character_count / 4)."""
    return math.ceil(len(text) / 4)


@dataclass(frozen=True)
class MaterializationCost:
    """Cost of a materialized representation in the runtime's declared unit.

    - `initial_tokens`: estimated tokens the Worker receives up front.
    - `deferred_tokens`: estimated tokens paid only on demand (per skill load
      or tool invocation).
    - `tool_declarations`: number of invocable declarations in the
      representation (zero for the prompt materialization).
    """

    initial_tokens: int
    deferred_tokens: int
    tool_declarations: int = 0

    @property
    def total_tokens_if_fully_loaded(self) -> int:
        """Total estimated tokens if every deferred portion is consumed."""
        return self.initial_tokens + self.deferred_tokens
