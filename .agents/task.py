#!/usr/bin/env python3
"""Task runner for common project and agent-protocol commands.

This file is part of the ARgentOS agent protocol (`.agents/`). It is kept
inside `.agents/` so that the only protocol artifact that lives outside
`.agents/` or `.project/` is `AGENTS.md` in the project root, which serves as
the human/agent entry point.
"""

from __future__ import annotations

import argparse
import os
import shutil
import subprocess
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
RUNNER_PATH = PROJECT_ROOT / ".agents" / "harness" / "runner.py"


def _find_venv_python() -> str:
    """Return the path to the project venv interpreter, or fall back to sys.executable."""
    candidates = [
        PROJECT_ROOT / "venv" / "Scripts" / "python.exe",
        PROJECT_ROOT / "venv" / "bin" / "python",
        PROJECT_ROOT / ".venv" / "Scripts" / "python.exe",
        PROJECT_ROOT / ".venv" / "bin" / "python",
    ]
    for candidate in candidates:
        if candidate.exists():
            return str(candidate)
    return sys.executable


def run(
    cmd: list[str], *, cwd: Path | None = None, env: dict[str, str] | None = None
) -> int:
    """Run a command and return its exit code."""
    print(f"$ {' '.join(cmd)}")
    result = subprocess.run(cmd, cwd=cwd or PROJECT_ROOT, env=env)
    return result.returncode


def cmd_test_project(args: argparse.Namespace) -> int:
    python = _find_venv_python()
    return run([python, "-m", "pytest", "tests/", "-v"])


def cmd_test_harness(args: argparse.Namespace) -> int:
    code = run([sys.executable, "-m", "pytest", ".agents/harness/tests/", "-v"])
    cmd_clean_pycache(args)
    return code


def cmd_test_all(args: argparse.Namespace) -> int:
    code = cmd_test_project(args)
    code = cmd_test_harness(args) or code
    return code


def cmd_health_check(args: argparse.Namespace) -> int:
    return run([sys.executable, str(RUNNER_PATH), "health-check"])


def cmd_features(args: argparse.Namespace) -> int:
    return run([sys.executable, str(RUNNER_PATH), "features"])


def cmd_clean_pycache(args: argparse.Namespace) -> int:
    """Remove __pycache__ directories and .pyc files under the project tree.

    The virtual environment (venv/) is intentionally skipped.
    """
    removed = 0
    skipped_roots = {PROJECT_ROOT / "venv", PROJECT_ROOT / ".venv"}
    for root, dirs, files in os.walk(PROJECT_ROOT):
        root_path = Path(root)
        if any(
            skipped in root_path.parents or root_path == skipped
            for skipped in skipped_roots
        ):
            dirs[:] = []
            continue

        for d in list(dirs):
            if d == "__pycache__":
                pycache_path = root_path / d
                shutil.rmtree(pycache_path)
                print(f"Removed {pycache_path}")
                dirs.remove(d)
                removed += 1
        for f in files:
            if f.endswith(".pyc"):
                pyc_path = root_path / f
                pyc_path.unlink()
                print(f"Removed {pyc_path}")
                removed += 1
    print(f"Cleaned {removed} pycache entries.")
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Run common project tasks")
    subparsers = parser.add_subparsers(dest="command", required=True)

    subparsers.add_parser("test-project", help="Run project user tests with the venv")
    subparsers.add_parser("test-harness", help="Run agent harness tests")
    subparsers.add_parser("test-all", help="Run both project and harness tests")
    subparsers.add_parser("health-check", help="Run agent protocol health-check")
    subparsers.add_parser("features", help="Show resolved agent feature flags")
    subparsers.add_parser("clean-pycache", help="Remove pycache under the project tree")

    args = parser.parse_args(argv)
    commands = {
        "test-project": cmd_test_project,
        "test-harness": cmd_test_harness,
        "test-all": cmd_test_all,
        "health-check": cmd_health_check,
        "features": cmd_features,
        "clean-pycache": cmd_clean_pycache,
    }
    return commands[args.command](args)


if __name__ == "__main__":
    sys.exit(main())
