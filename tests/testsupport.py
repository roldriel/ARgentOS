"""Small helpers shared by the DEV tooling suites in ``tests/``.

This module exists for exactly one reason: the "this tool imports only the
standard library" check was duplicated, byte for byte, in seven suites, with the
only difference being the set of first-party modules each tool may import
(``tests/test_check_*.py``). The duplication is accidental — the assertion is
the same contract — so it lives here once.

It is deliberately **not** a test framework: there is no registry, no plugin, no
base class and no collection. It is a plain function plus one constant, kept in
the same style as ``tests/pytest_isolation.py`` (a module imported by the suites
after the session bootstrap).

Parsing is done with ``ast`` rather than by importing the tool, so the check is
independent of ``sys.path`` and of the tool's own import side effects. That keeps
the assertion meaningful: it reports what the tool's source declares, not what
happens to be importable.
"""

from __future__ import annotations

import ast
import sys
from collections.abc import Iterable
from pathlib import Path

#: Module top-level names that are always importable: the standard library, plus
#: whatever ``local_modules`` the caller declares (the first-party modules of
#: ``tools/`` a given tool is allowed to import).
STDLIB_MODULE_NAMES = frozenset(sys.stdlib_module_names)


def assert_tool_imports_only_stdlib(
    tool_path: Path,
    local_modules: Iterable[str] = (),
) -> None:
    """Assert ``tool_path`` imports only the stdlib and ``local_modules``.

    ``local_modules`` names the first-party modules the tool is allowed to
    import (for example ``legacy_paths`` for ``check_plan_citations.py``). Pass
    nothing when the tool must be strictly stdlib-only — that is the strictest
    form of the check and it is preserved, not weakened.

    Raises ``AssertionError`` listing the offending top-level module names, so a
    failure still points at the tool under test and names what leaked.
    """
    tree = ast.parse(tool_path.read_text(encoding="utf-8"))
    imported: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            imported.update(alias.name.split(".")[0] for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.level == 0 and node.module:
            imported.add(node.module.split(".")[0])

    allowed = STDLIB_MODULE_NAMES | set(local_modules)
    third_party = imported - allowed
    assert third_party == set(), (
        f"{tool_path.name} imports third-party modules: {sorted(third_party)}"
    )
