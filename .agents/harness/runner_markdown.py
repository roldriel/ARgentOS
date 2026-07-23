"""Markdown/TOML parsing helpers for the harness runner."""

from __future__ import annotations

import sys
from pathlib import Path

_HARNESS_DIR = Path(__file__).resolve().parent
if str(_HARNESS_DIR) not in sys.path:
    sys.path.insert(0, str(_HARNESS_DIR))

import re
import tomllib
from typing import Any


def parse_front_matter(content: str) -> dict[str, Any]:
    """Parse TOML front matter delimited by '+++' markers."""
    match = re.match(r"^\+\+\+\s*\n(.*?)\n\+\+\+\s*\n", content, re.DOTALL)
    if not match:
        raise ValueError("No TOML front matter found (expected +++ block)")
    return tomllib.loads(match.group(1))



def find_section_headings(content: str) -> set[str]:
    """Find all Markdown ## headings in the content."""
    headings: set[str] = set()
    for line in content.splitlines():
        match = re.match(r"^##\s+(.+?)\s*$", line)
        if match:
            headings.add(match.group(1).strip())
    return headings


def extract_section(content: str, section_name: str) -> str:
    """Extract the content of a Markdown ## section until the next ## heading."""
    pattern = rf"^##\s+{re.escape(section_name)}\s*\n(.*?)(?=^##\s|\Z)"
    match = re.search(pattern, content, re.MULTILINE | re.DOTALL)
    if not match:
        return ""
    return match.group(1).strip()


def extract_toml_block(content: str, section_name: str) -> dict[str, Any] | None:
    """Extract the first ```toml block from a given ## section.

    Returns the parsed dict or None if there is no block or it is not
    valid TOML. tomllib always produces a dict at the top level.
    """
    section = extract_section(content, section_name)
    if not section:
        return None
    match = re.search(r"```toml\n(.*?)\n```", section, re.DOTALL)
    if not match:
        return None
    try:
        return tomllib.loads(match.group(1))
    except tomllib.TOMLDecodeError:
        return None

