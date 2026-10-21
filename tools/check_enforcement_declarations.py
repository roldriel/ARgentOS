#!/usr/bin/env python3
"""Verify the enforcement declarations of the harness guarantee catalog (G-04).

Reads ``protocol/.agents/harness/INDEX.md`` and verifies the three rules the
document states about itself:

- **ENF-001** — a guarantee labeled "mechanically enforced" must not depend on
  agent judgment: its "Verified by" cell must name a runtime/mechanism, not the
  agent or the harness alone.
- **ENF-002** — in declarative mode every "verifiable" guarantee is declared and
  its verification source is named; a "verifiable" guarantee may not be verified
  by a human alone (that is an external-actor class, not a verifiable one).
- **ENF-003** — the document must state that hooks remain fail-open and must not
  declare them an absolute control.

**Limit (INV-12).** This verifies the *declaration*: that the catalog is
well-formed and that the stated rules are respected by it. It does **not**
verify that a named mechanism exists or works, nor that the declared class is
truthful. Class accuracy is a meta-property and is not auto-verifiable; the
checker does not claim otherwise.

Usage: python tools/check_enforcement_declarations.py [--root REPO_ROOT]

Exit code: 0 when the declarations pass, 1 when they fail, 2 on a read/parse
error. Standard library only; read-only.
"""

from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass
from pathlib import Path

_INDEX_REL = "protocol/.agents/harness/INDEX.md"

_CLASSES = frozenset(
    {
        "declarative",
        "verifiable",
        "mechanically enforced",
        "agent-judgment-dependent",
        "external-actor-dependent",
    }
)

#: Tokens that name a mechanism (runtime/hooks/tooling) rather than a judge.
_MECHANISM_TOKENS = (
    "runtime",
    "runner_state",
    "hook",
    "gate_validator",
    "lifecycle",
    "dev tool",
)

#: Tokens that name a verification source for a "verifiable" guarantee.
_VERIFICATION_TOKENS = _MECHANISM_TOKENS + (
    "agent",
    "harness",
    "attest",
    "audit_gates",
    "tool",
)

_TABLE_HEADER_RE = re.compile(
    r"^\|\s*Guarantee\s*\|\s*Class\s*\|\s*Verified by\s*\|", re.IGNORECASE
)


class DeclarationError(Exception):
    """The catalog could not be read or parsed."""


@dataclass(frozen=True)
class Row:
    guarantee: str
    klass: str
    verified_by: str

    @property
    def base_class(self) -> str:
        """Class without a free-form qualifier: 'Verifiable (best-effort)'."""
        return re.sub(r"\s*\(.*?\)\s*$", "", self.klass).strip().casefold()


def catalog_text(index_path: Path) -> str:
    if not index_path.is_file():
        raise DeclarationError(f"not found: {index_path}")
    return index_path.read_text(encoding="utf-8", errors="replace")


def parse_catalog(text: str) -> list[Row]:
    """Rows of the guarantee catalog table (the first three-column table)."""
    lines = text.splitlines()
    start = next(
        (i for i, line in enumerate(lines) if _TABLE_HEADER_RE.match(line)),
        None,
    )
    if start is None:
        raise DeclarationError("guarantee catalog table not found")
    rows: list[Row] = []
    for line in lines[start + 2 :]:
        if not line.lstrip().startswith("|"):
            break
        cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
        if len(cells) != 3:
            continue
        rows.append(Row(cells[0], cells[1], cells[2]))
    if not rows:
        raise DeclarationError("guarantee catalog table is empty")
    return rows


def _names(cell: str, tokens: tuple[str, ...]) -> bool:
    folded = cell.casefold()
    return any(token in folded for token in tokens)


def verify(index_path: Path) -> list[str]:
    """Return the declaration failures (empty list = pass)."""
    text = catalog_text(index_path)
    rows = parse_catalog(text)
    failures: list[str] = []

    unknown = sorted({row.klass for row in rows if row.base_class not in _CLASSES})
    if unknown:
        failures.append(
            "class outside the closed five-class catalog: " + ", ".join(unknown)
        )

    for row in rows:
        if row.base_class == "mechanically enforced" and not _names(
            row.verified_by, _MECHANISM_TOKENS
        ):
            failures.append(
                "ENF-001: mechanically enforced guarantee has no runtime/mechanism "
                f"verifier: {row.guarantee!r} ({row.verified_by!r})"
            )
        if row.base_class == "verifiable":
            if not _names(row.verified_by, _VERIFICATION_TOKENS):
                failures.append(
                    "ENF-002: verifiable guarantee names no verification source: "
                    f"{row.guarantee!r} ({row.verified_by!r})"
                )
            elif "human" in row.verified_by.casefold() and not _names(
                row.verified_by, tuple(t for t in _VERIFICATION_TOKENS if t != "tool")
            ):
                failures.append(
                    "ENF-002: verifiable guarantee is verified by a human alone: "
                    f"{row.guarantee!r}"
                )

    folded = text.casefold()
    normalized = " ".join(text.split())
    if "fail-open" not in folded:
        failures.append("ENF-003: the fail-open declaration is absent")
    else:
        occurrences = [
            match.start()
            for match in re.finditer(
                "absolute control", normalized, re.IGNORECASE
            )
        ]
        if not occurrences:
            failures.append(
                "ENF-003: no statement ties fail-open to the absence of an "
                "absolute control"
            )
        for position in occurrences:
            window = normalized[max(0, position - 160) : position]
            if not re.search(r"\b(not|never|no)\b", window, re.IGNORECASE):
                failures.append(
                    "ENF-003: the document declares an absolute control for hooks"
                )
                break

    for label in ("ENF-001", "ENF-002", "ENF-003"):
        if label not in text:
            failures.append(f"ENF: the rule {label} is not declared in the document")

    return failures


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument(
        "--root",
        type=Path,
        default=Path(__file__).resolve().parents[1],
        help="Repository root (default: parent of this script's directory).",
    )
    args = parser.parse_args(argv)
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    try:
        failures = verify(args.root.resolve() / _INDEX_REL)
    except DeclarationError as exc:
        print(f"Enforcement declarations check: ERROR — {exc}", file=sys.stderr)
        return 2
    print("Enforcement declarations check (G-04, declaration-level):")
    if not failures:
        print("- ENF-001/ENF-002/ENF-003: PASS")
        print("Summary: PASS")
        return 0
    for failure in failures:
        print(f"- {failure}")
    print("Summary: FAIL")
    return 1


if __name__ == "__main__":
    sys.exit(main())
