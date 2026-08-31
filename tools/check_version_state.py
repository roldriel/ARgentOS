#!/usr/bin/env python3
"""Verify the version-state invariant: VERSION <-> changelog <-> tags.

Per ``docs/VERSIONING.md`` §2, every version in ``protocol/.agents/VERSION``
must have a section in ``CHANGELOG.md`` and a tag on ``master``; every tag
corresponds to a published version with a changelog section.

It also verifies the runtime semantic anchor: ``runtime/toolcalls/canonical.py``
``PROTOCOL_VERSION`` must equal ``protocol/.agents/VERSION`` (RFC-71: under
block versioning, ``semantic_version`` is the protocol version governing the
segment content). This prevents the reference runtime from silently freezing
an outdated semantic identity anchor on future version bumps.

This dev-only checker implements that invariant with the declared ``dev``
exception: on ``dev``, changelog sections and the current ``VERSION`` without a
matching tag are expected (in-progress releases, tagged only at promotion), so
they are reported as warnings, never as failures.

Usage:
  python tools/check_version_state.py [--root REPO_ROOT]

Exit code: 0 when no errors are found, 1 otherwise.
Standard library only (uses the git CLI to list tags).
"""

from __future__ import annotations

import argparse
import re
import subprocess
import sys
from pathlib import Path


SEMVER = re.compile(r"^\d+\.\d+\.\d+$")
SECTION = re.compile(r"^## \[(\d+\.\d+\.\d+)\]", re.MULTILINE)
RUNTIME_ANCHOR = re.compile(
    r'^PROTOCOL_VERSION\s*=\s*"(\d+\.\d+\.\d+)"', re.MULTILINE
)


def get_tags(root: Path) -> list[str]:
    """Return the semver tags of the repository (empty when git is unusable)."""
    try:
        result = subprocess.run(
            ["git", "-C", str(root), "tag", "--list"],
            capture_output=True,
            text=True,
            timeout=30,
        )
    except (OSError, subprocess.SubprocessError):
        return []
    return sorted(
        {line.strip() for line in result.stdout.splitlines() if SEMVER.match(line.strip())}
    )


def _runtime_protocol_version(canonical_file: Path) -> str | None:
    """Return the PROTOCOL_VERSION literal declared by canonical.py, if any."""
    try:
        text = canonical_file.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return None
    match = RUNTIME_ANCHOR.search(text)
    return match.group(1) if match else None


def verify(root: Path) -> tuple[list[str], list[str]]:
    """Return (errors, warnings)."""
    errors: list[str] = []
    warnings: list[str] = []

    version_file = root / "protocol" / ".agents" / "VERSION"
    changelog_file = root / "CHANGELOG.md"
    if not version_file.is_file():
        errors.append("missing protocol/.agents/VERSION")
        return errors, warnings
    if not changelog_file.is_file():
        errors.append("missing CHANGELOG.md")
        return errors, warnings

    version = version_file.read_text(encoding="utf-8", errors="replace").strip()
    if not SEMVER.match(version):
        errors.append(f"VERSION is not semver: {version!r}")
        return errors, warnings

    canonical_file = root / "runtime" / "toolcalls" / "canonical.py"
    if not canonical_file.is_file():
        errors.append("missing runtime/toolcalls/canonical.py")
        return errors, warnings
    anchor = _runtime_protocol_version(canonical_file)
    if anchor is None:
        errors.append(
            "runtime/toolcalls/canonical.py declares no parseable PROTOCOL_VERSION"
        )
        return errors, warnings
    if anchor != version:
        errors.append(
            f"runtime semantic anchor PROTOCOL_VERSION ({anchor}) does not "
            f"match protocol/.agents/VERSION ({version})"
        )

    changelog = changelog_file.read_text(encoding="utf-8", errors="replace")
    sections = set(SECTION.findall(changelog))
    if version not in sections:
        errors.append(f"VERSION {version} has no ## [{version}] section in CHANGELOG.md")

    tags = get_tags(root)
    for tag in tags:
        if tag not in sections:
            errors.append(f"tag {tag} has no ## [{tag}] section in CHANGELOG.md")

    for section in sorted(sections - {version}):
        if section not in tags:
            warnings.append(
                f"changelog section [{section}] has no tag (expected on dev until promotion)"
            )
    if version not in tags:
        warnings.append(
            f"VERSION {version} has no tag (expected on dev until promotion)"
        )
    return errors, warnings


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--root", type=Path, default=None)
    args = parser.parse_args(argv)
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    root = (args.root or Path(__file__).resolve().parents[1]).resolve()
    errors, warnings = verify(root)
    for w in sorted(warnings):
        print(f"warning: {w}")
    if not errors:
        print("Version state OK.")
        return 0
    print(f"Version state errors: {len(errors)}")
    for e in sorted(errors):
        print(f"- {e}")
    return 1


if __name__ == "__main__":
    sys.exit(main())
