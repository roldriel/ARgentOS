"""Isolation and boundary tests of the MAR prototype package.

The package is a DEV-only, experimental, advisory-only, read-only instrument: it
must not import the protocol, the host or any third party, it must not write
files, it must not carry adjudication machinery, and its module docstrings must
declare its advisory / no-authority nature. These are structural tests over the
package source plus one subprocess import check; every artifact used is either
read from the repository or created under ``tmp_path`` — nothing is written
inside the repository (``tests/AGENTS.md``).
"""

from __future__ import annotations

import ast
import os
import subprocess
import sys
from pathlib import Path

from test_adversarial_review import REPO_ROOT

from runtime.adversarial_review import SIGNAL_KEYS, recommend_review

PACKAGE_DIR = REPO_ROOT / "runtime" / "adversarial_review"
SOURCE_FILES = sorted(PACKAGE_DIR.glob("*.py"))
PACKAGE_MODULE = "runtime.adversarial_review"
STDLIB_MODULES = frozenset(sys.stdlib_module_names)

#: Identifiers/keys that would express adjudication. The validator *detects*
#: these field names as data (a set literal is not an identifier or a key), but
#: the package must never use one as a name, an attribute or a dict key.
FORBIDDEN_ADJUDICATION_NAMES = frozenset(
    {
        "verdict",
        "vote",
        "votes",
        "voting",
        "judge",
        "jury",
        "court",
        "majority",
        "authorization",
        "decision_authority",
    }
)

#: Attribute names that write or delete something.
WRITE_ATTRIBUTES = frozenset(
    {"write_text", "write_bytes", "write", "unlink", "remove", "rmtree", "rename", "replace"}
)


def _parse(path: Path) -> ast.Module:
    return ast.parse(path.read_text(encoding="utf-8"))


def _open_mode(node: ast.Call) -> str:
    for keyword in node.keywords:
        if (
            keyword.arg == "mode"
            and isinstance(keyword.value, ast.Constant)
            and isinstance(keyword.value.value, str)
        ):
            return keyword.value.value
    if (
        len(node.args) >= 2
        and isinstance(node.args[1], ast.Constant)
        and isinstance(node.args[1].value, str)
    ):
        return node.args[1].value
    return "r"


def test_package_imports_are_stdlib_or_intra_package() -> None:
    for path in SOURCE_FILES:
        for node in ast.walk(_parse(path)):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    root = alias.name.split(".")[0]
                    allowed = (
                        root in STDLIB_MODULES
                        or alias.name == PACKAGE_MODULE
                        or alias.name.startswith(PACKAGE_MODULE + ".")
                    )
                    assert allowed, f"{path.name} imports {alias.name!r}"
                    assert not alias.name.startswith("protocol"), (
                        f"{path.name} imports the protocol payload"
                    )
            elif isinstance(node, ast.ImportFrom):
                if node.level:
                    continue  # intra-package relative import
                module = node.module or ""
                root = module.split(".")[0]
                allowed = (
                    root in STDLIB_MODULES
                    or module == PACKAGE_MODULE
                    or module.startswith(PACKAGE_MODULE + ".")
                )
                assert allowed, f"{path.name} imports from {module!r}"
                assert not module.startswith("protocol"), (
                    f"{path.name} imports from the protocol payload"
                )


def test_package_performs_no_write_operations() -> None:
    for path in SOURCE_FILES:
        for node in ast.walk(_parse(path)):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    assert alias.name.split(".")[0] != "shutil", (
                        f"{path.name} imports shutil"
                    )
            elif isinstance(node, ast.ImportFrom):
                if node.level == 0:
                    assert (node.module or "").split(".")[0] != "shutil", (
                        f"{path.name} imports from shutil"
                    )
            elif isinstance(node, ast.Call):
                func = node.func
                name = (
                    func.id
                    if isinstance(func, ast.Name)
                    else func.attr
                    if isinstance(func, ast.Attribute)
                    else ""
                )
                assert name not in WRITE_ATTRIBUTES, f"{path.name} calls {name}()"
                if name == "open":
                    mode = _open_mode(node)
                    assert not any(flag in mode for flag in "wax+"), (
                        f"{path.name} opens a file in writing mode {mode!r}"
                    )


def test_package_does_not_carry_adjudication_machinery() -> None:
    for path in SOURCE_FILES:
        for node in ast.walk(_parse(path)):
            if isinstance(node, ast.Name):
                assert node.id not in FORBIDDEN_ADJUDICATION_NAMES, (
                    f"{path.name} names {node.id!r}"
                )
            elif isinstance(node, ast.Attribute):
                assert node.attr not in FORBIDDEN_ADJUDICATION_NAMES, (
                    f"{path.name} uses attribute {node.attr!r}"
                )
            elif isinstance(node, ast.Dict):
                for key in node.keys:
                    if isinstance(key, ast.Constant) and isinstance(key.value, str):
                        assert key.value not in FORBIDDEN_ADJUDICATION_NAMES, (
                            f"{path.name} uses dict key {key.value!r}"
                        )


def test_importing_the_package_leaves_no_files_behind(tmp_path: Path) -> None:
    env = os.environ.copy()
    env["PYTHONPATH"] = str(REPO_ROOT) + os.pathsep + env.get("PYTHONPATH", "")
    proc = subprocess.run(
        [sys.executable, "-B", "-c", "import runtime.adversarial_review"],
        cwd=tmp_path,
        capture_output=True,
        text=True,
        encoding="utf-8",
        env=env,
        check=False,
    )
    assert proc.returncode == 0, proc.stderr
    assert list(tmp_path.iterdir()) == []


def test_every_selectivity_result_is_advisory_only() -> None:
    base = {key: "LOW" for key in SIGNAL_KEYS}
    cases = [
        base,
        {**base, "materiality_potential": "LOW", "ambiguity": "UNKNOWN"},
        {**base, "materiality_potential": "HIGH", "ambiguity": "HIGH"},
        {**base, "materiality_potential": "MEDIUM", "impact": "MEDIUM"},
        {**base, "materiality_potential": "HIGH"},
    ]
    for signals in cases:
        result = recommend_review(signals)
        assert result["advisory"] is True
        assert "advisory" in result["note"]


def test_module_docstrings_declare_advisory_and_no_authority() -> None:
    for path in SOURCE_FILES:
        docstring = ast.get_docstring(_parse(path))
        assert docstring, f"{path.name} must start with a module docstring"
        lowered = docstring.lower()
        for phrase in (
            "dev-only",
            "experimental",
            "advisory",
            "not integrated",
            "no authority",
        ):
            assert phrase in lowered, f"{path.name} docstring is missing {phrase!r}"
    init_docstring = (ast.get_docstring(_parse(PACKAGE_DIR / "__init__.py")) or "").lower()
    assert "no consumer" in init_docstring
