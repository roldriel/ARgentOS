---
name: planner
description: Fixture skill that decomposes an objective into ordered, verifiable steps. Used by tests/test_toolcalls.py as a self-contained stand-in for the payload skill.
when_to_activate: Only in tests.
when_not: Never in production.
---

# Mission

Fixture content for the planner skill. It exists so that runtime tests do not
read the product payload (`protocol/.agents/skills/`); see `tests/AGENTS.md`.
