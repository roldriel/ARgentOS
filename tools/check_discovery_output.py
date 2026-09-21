#!/usr/bin/env python3
"""Check the mechanical subset of D01 over a discovery knowledge base.

D01 is the discovery domain's single validation gate
(``protocol/.agents/orchestrators/discovery/harness/policies/D01-discovery-output.md``,
``DISCOVERY_VALIDATE -> DISCOVERY_READY``). It covers structural validation and
ground truth, and today every one of its twelve items is ``[agent]`` judgement
because the harness has no executable runner (plan 60). The same contract
declares the items whose structure is deterministic as ``[gate]`` candidates,
"objectively checkable without interpretation if a future implementation
restores mechanical checks". **This tool materializes exactly that subset and
nothing more** (plan 136).

What it checks (deterministic; decided by reading bytes and comparing them):

1.  every entry and the manifest exist and are non-empty;
2.  the entry carries parseable, delimited TOML front matter;
3.  the required front-matter fields are present with the right type;
4.  ``artifact`` is ``KB_DISCOVERY_ENTRY.md`` and ``kind`` is ``snapshot``;
5.  the ``#`` heading of the body matches the ``title`` field;
6.  the required sections are present: ``## Discovered Facts`` plus the
    sections its per-entry contract declares;
7.  every ``source_files`` path resolves in the project, with the reserved
    values ``system_probe`` (environment entries only) and ``project_scan``
    (absences and tree facts only, never in an environment entry) admitted
    under their declared classes;
8.  ``[entries] active`` and the files present agree in both directions;
9.  a manifest entry's front matter agrees with the manifest entry list;
10. ``executive_summary.md`` declares ``## Project Shape`` as its first content
    section and the value matches the manifest's ``project_shape``;
11. ``distribution.md`` is present when ``project_shape`` is ``library`` or
    ``cli``.

What it deliberately does **not** do. The remaining D01 items are judgement and
are not converted into checks (plan 136): whether a stack or dependency really
appears in a configuration file, whether a pattern has a verifiable example,
whether secrets leaked, whether a qualitative claim has a source, whether the
merge was consistent, and whether ``api.md`` matches the shape's variant rules.
Silence about them is a declared boundary, not an approval.

Two payload decisions that were formerly boundaries are now **materialized** by
RFC-79 (plan 142) and enforced here:

* ``F-17`` — ``containers.md``/``database.md`` declare absences and
  ``file_map.md`` declares tree facts. The base contract now admits the reserved
  value ``project_scan`` for exactly that class, so ``project_scan`` is
  ``VALID`` outside an environment entry and ``ANOMALY`` inside one; an
  unresolvable entry that is not a reserved value is a **violation** of D01 item
  5 (``ANOMALY``), not missing evidence. The ``GAP`` that this tool reported
  while the contract had no value for the class was a declared boundary, and it
  is gone because the underlying contract gap is gone.
* ``F-16`` — the classification model now admits ``documentation`` for a
  documentary/standards/protocol product. Which shape a repository *should* have
  remains a classification decision, so a *missing* shape is still reported as a
  boundary (human review); an out-of-enum value is an ``ANOMALY``.

Requirements are resolved **from the contracts**, never from a list maintained
here: the per-entry contracts declare both their runtime KB path and their
required sections, and D01 item 12 states that D01 "does not maintain a section
list of its own" (plan 47, RFC-48). If this tool and a contract disagree, the
contract governs and the implementation defect is escalated and corrected.

Usage::

    python tools/check_discovery_output.py [--root REPO_ROOT] [--payload PROTOCOL] [--json]

Exit codes (the contract of the repository's checkers):

* ``0`` — no ``ANOMALY`` found. ``GAP`` is advisory and never changes the exit
  code; a missing knowledge base is a valid absence, not a failure.
* ``1`` — at least one ``ANOMALY`` (present but contradictory information).
* ``2`` — unrecoverable read error.

Standard library only. Read-only: nothing is written, repaired or archived.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
import tomllib
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Iterable, Mapping, Sequence

PLANS_KB_DIR = ".project/knowledge/discovery"
MANIFEST_NAME = ".discovery_manifest"
MANIFEST_CONTRACT = "DISCOVERY_MANIFEST.md"
BASE_CONTRACT = "KB_DISCOVERY_ENTRY.md"
CONTRACTS_DIR = "orchestrators/discovery/contracts"

#: Signals (the repository's existing vocabulary; never conflated).
VALID = "VALID"
GAP = "GAP"
ANOMALY = "ANOMALY"
BOUNDARY = "BOUNDARY"
NOT_APPLICABLE = "N/A"
EXCLUDED = "EXCLUDED"

_SIGNAL_PRECEDENCE = (ANOMALY, BOUNDARY, GAP, NOT_APPLICABLE, EXCLUDED, VALID)

#: The seven values the manifest contract admits for ``project_shape``.
PROJECT_SHAPES = frozenset(
    {"library", "cli", "service", "application", "monorepo", "documentation", "unknown"}
)

#: Shapes that make ``distribution.md`` mandatory (D01 item 10 / DISTRIBUTION.md).
DISTRIBUTION_SHAPES = frozenset({"library", "cli"})

#: The D01 item this tool materializes, per check, for the report.
DOC_REF = "protocol/.agents/orchestrators/discovery/harness/policies/D01-discovery-output.md"

#: Front-matter fields the base entry contract requires, with their kind.
REQUIRED_STRING_FIELDS = ("artifact", "kind", "title", "generated_at")
REQUIRED_LIST_FIELDS = ("tags", "source_files")

#: The base contract's own required sections (KB_DISCOVERY_ENTRY.md:Completion
#: Criteria plus its ``## Discovered Facts`` section).
BASE_REQUIRED_SECTIONS = ("## Discovered Facts",)

#: ``kind`` every discovery entry must declare (base contract: Required Front Matter).
REQUIRED_KIND = "snapshot"
REQUIRED_ARTIFACT = "KB_DISCOVERY_ENTRY.md"

#: The provenance token the base contract admits only for environment entries.
SYSTEM_PROBE = "system_probe"

#:: The reserved provenance value for an absence or a tree/structural fact
#: observed by scanning the project tree (RFC-79 decision 2). Valid only outside
#: an environment entry, whose reserved value is :data:`SYSTEM_PROBE`.
PROJECT_SCAN = "project_scan"

_FRONT_MATTER_RE = re.compile(r"\A\+\+\+\r?\n(.*?)\r?\n\+\+\+\s*(?:\r?\n|\Z)", re.DOTALL)
_H1_RE = re.compile(r"^#\s+(.+?)\s*$", re.MULTILINE)
_SECTION_RE = re.compile(r"^(#{2,3})\s+(.+?)\s*$", re.MULTILINE)
_LOCATION_RE = re.compile(r"`\.project/knowledge/discovery/([^`]+)`")
_TOML_LIST_RE = re.compile(r"^(?P<key>[A-Za-z_][A-Za-z0-9_]*)\s*=\s*\[(?P<body>[^\]]*)\]", re.MULTILINE)


class ReadError(RuntimeError):
    """An input could not be read at all (exit 2, never a claim about content)."""


# --------------------------------------------------------------------------- #
# Contract resolution (read-only; the contracts are the single source)
# --------------------------------------------------------------------------- #


@dataclass(frozen=True)
class Contract:
    """One discovery entry contract, as read from the payload.

    ``runtime_name`` and ``required_sections`` are **read from the contract**,
    not maintained here: the contract declares its runtime path in its
    ``## Location`` section and its required sections as backticked headings.
    """

    stem: str
    runtime_name: str
    required_sections: tuple[str, ...]
    is_environment: bool
    source: str

    def to_dict(self) -> dict[str, Any]:
        return {
            "stem": self.stem,
            "runtime_name": self.runtime_name,
            "required_sections": list(self.required_sections),
            "is_environment": self.is_environment,
            "source": self.source,
        }


def _section_name(token: str) -> str | None:
    """Normalize a contract-declared section token to its bare heading name.

    Contracts declare required sections in two forms, both of which name the
    heading in backticks:

    * as ``### `## Section` `` items (most per-entry contracts);
    * inside numbered prose, as ``the `## Project Shape` section``
      (``EXECUTIVE_SUMMARY.md``).

    Only level-2 headings are returned. The level-1 placeholder ``# <Title>`` is
    validated as the title match instead, and any other backticked token (a
    field name, a value) is ignored rather than mistaken for a section.
    """
    heading = re.sub(r"\s+", " ", token.strip())
    if not heading.startswith("## "):
        return None
    name = heading[3:].strip()
    return name or None


def _backticked_headings(text: str) -> tuple[str, ...]:
    """Required level-2 section names a contract declares in backticks.

    Resolved from the contract itself, never from a list maintained here: D01
    item 12 states that D01 "does not maintain a section list of its own"
    (plan 47, RFC-48).
    """
    found: list[str] = []
    for match in re.finditer(r"`([^`\n]+)`", text):
        name = _section_name(match.group(1))
        if name is not None and name not in found:
            found.append(name)
    return tuple(found)


def read_contract(path: Path, payload_rel: str) -> Contract | None:
    """Read one contract; ``None`` when it is not a discovery entry contract.

    A contract participates when it declares a runtime path under
    ``.project/knowledge/discovery/`` (the manifest is handled separately, and
    the base/inter-worker/report contracts declare no such path).
    """
    try:
        text = path.read_text(encoding="utf-8")
    except OSError as exc:
        raise ReadError(f"cannot read contract {path}: {exc}") from exc

    location = _LOCATION_RE.search(text)
    if location is None:
        return None
    runtime_name = location.group(1).strip()
    if runtime_name.startswith(".") or "/" in runtime_name:
        # The manifest (``.discovery_manifest``) and any nested path are not
        # entry contracts.
        return None
    if not runtime_name.endswith(".md"):
        return None

    return Contract(
        stem=path.stem,
        runtime_name=runtime_name,
        required_sections=_backticked_headings(text),
        is_environment=SYSTEM_PROBE in text,
        source=f"{payload_rel}/{CONTRACTS_DIR}/{path.name}",
    )


def load_contracts(payload: Path, payload_rel: str | None = None) -> dict[str, Contract]:
    """Map runtime artifact name -> contract, read from the payload.

    ``payload_rel`` is the citation prefix recorded on every finding, so a report
    names the contract by its real repository path (``protocol/.agents/...``)
    rather than by the payload directory's basename.
    """
    contracts_dir = payload / CONTRACTS_DIR
    if not contracts_dir.is_dir():
        raise ReadError(f"discovery contracts directory not found: {contracts_dir}")
    prefix = payload_rel or payload.name
    contracts: dict[str, Contract] = {}
    for path in sorted(contracts_dir.glob("*.md")):
        contract = read_contract(path, prefix)
        if contract is None:
            continue
        contracts[contract.runtime_name] = contract
    return contracts


def load_base_required_sections(payload: Path) -> tuple[str, ...]:
    """Sections every entry must carry, read from the base contract.

    ``KB_DISCOVERY_ENTRY.md`` documents its sections with ``### `## X` `` headings
    and its Completion Criteria require ``## Discovered Facts``. Both are read;
    the level-1 placeholder and ``## Summary`` are handled as the title match and
    as a per-entry requirement respectively, so only level-2 headings are added
    here beyond the always-required ``## Discovered Facts``.
    """
    path = payload / CONTRACTS_DIR / BASE_CONTRACT
    try:
        text = path.read_text(encoding="utf-8")
    except OSError as exc:
        raise ReadError(f"cannot read base contract {path}: {exc}") from exc
    sections = [name[3:] for name in BASE_REQUIRED_SECTIONS]
    for name in _backticked_headings(text):
        if name not in sections:
            sections.append(name)
    return tuple(sections)


def load_manifest_required_sections(payload: Path) -> tuple[tuple[str, tuple[str, ...]], ...]:
    """The manifest's required tables and their fields, read from its contract.

    Returns ``((table, (field, ...)), ...)`` for the TOML tables the contract
    declares under ``## Required sections``, excluding the optional ``[runtime]``.
    """
    path = payload / CONTRACTS_DIR / MANIFEST_CONTRACT
    try:
        text = path.read_text(encoding="utf-8")
    except OSError as exc:
        raise ReadError(f"cannot read manifest contract {path}: {exc}") from exc

    tables: list[tuple[str, tuple[str, ...]]] = []
    current: str | None = None
    fields: list[str] = []
    for line in text.splitlines():
        section = re.match(r"^###\s+`\[([A-Za-z_]+)\]`\s*$", line)
        if section:
            if current is not None:
                tables.append((current, tuple(fields)))
            current = section.group(1)
            fields = []
            continue
        field_match = re.match(r"^-\s+`([A-Za-z_]+)`", line)
        if field_match and current is not None:
            fields.append(field_match.group(1))
    if current is not None:
        tables.append((current, tuple(fields)))
    return tuple(tables)


# --------------------------------------------------------------------------- #
# Findings
# --------------------------------------------------------------------------- #


@dataclass(frozen=True)
class Finding:
    """One check result: a signal, the reason, and the rule it comes from."""

    target: str
    signal: str
    reason: str
    rule: str = ""
    item: str = ""

    def to_dict(self) -> dict[str, Any]:
        return {
            "target": self.target,
            "signal": self.signal,
            "reason": self.reason,
            "rule": self.rule,
            "d01_item": self.item,
        }


def _worst(signals: Iterable[str]) -> str:
    present = set(signals)
    for signal in _SIGNAL_PRECEDENCE:
        if signal in present:
            return signal
    return NOT_APPLICABLE


@dataclass
class Report:
    """The accumulated findings of one run, grouped per inspected artifact."""

    findings: list[Finding] = field(default_factory=list)

    def add(self, finding: Finding) -> None:
        self.findings.append(finding)

    @property
    def has_anomaly(self) -> bool:
        return any(item.signal == ANOMALY for item in self.findings)

    def per_target(self) -> list[tuple[str, str, list[Finding]]]:
        grouped: dict[str, list[Finding]] = {}
        for finding in self.findings:
            grouped.setdefault(finding.target, []).append(finding)
        return [
            (target, _worst(item.signal for item in items), items)
            for target, items in sorted(grouped.items())
        ]

    def counts(self) -> dict[str, int]:
        counts = {signal: 0 for signal in _SIGNAL_PRECEDENCE}
        for target, signal, _ in self.per_target():
            counts[signal] += 1
        return counts


# --------------------------------------------------------------------------- #
# Entry checks
# --------------------------------------------------------------------------- #


@dataclass(frozen=True)
class Entry:
    """A parsed KB entry: its front matter, its body and its headings."""

    name: str
    text: str
    front_matter: Mapping[str, Any]
    body: str
    headings: tuple[str, ...]

    @property
    def title_heading(self) -> str | None:
        match = _H1_RE.search(self.body)
        return match.group(1).strip() if match else None


def parse_entry(name: str, text: str) -> Entry | None:
    """Parse an entry; ``None`` when the front matter cannot be read."""
    match = _FRONT_MATTER_RE.match(text)
    if match is None:
        return None
    try:
        front_matter = tomllib.loads(match.group(1))
    except tomllib.TOMLDecodeError:
        return None
    body = text[match.end() :]
    headings = tuple(
        re.sub(r"\s+", " ", m.group(2).strip()) for m in _SECTION_RE.finditer(body)
    )
    return Entry(
        name=name,
        text=text,
        front_matter=front_matter,
        body=body,
        headings=headings,
    )


def _check_required_fields(entry: Entry, report: Report) -> None:
    for field_name in REQUIRED_STRING_FIELDS:
        value = entry.front_matter.get(field_name)
        if value is None:
            report.add(
                Finding(
                    entry.name,
                    ANOMALY,
                    f"front matter is missing the required field `{field_name}`",
                    f"{BASE_CONTRACT}:Required Front Matter",
                    "8/12",
                )
            )
        elif not isinstance(value, str) or not value.strip():
            report.add(
                Finding(
                    entry.name,
                    ANOMALY,
                    f"front matter field `{field_name}` must be a non-empty string "
                    f"(found {type(value).__name__})",
                    f"{BASE_CONTRACT}:Required Front Matter",
                    "8/12",
                )
            )
    for field_name in REQUIRED_LIST_FIELDS:
        value = entry.front_matter.get(field_name)
        if value is None:
            report.add(
                Finding(
                    entry.name,
                    ANOMALY,
                    f"front matter is missing the required field `{field_name}`",
                    f"{BASE_CONTRACT}:Required Front Matter",
                    "8/12",
                )
            )
        elif not isinstance(value, list) or not value:
            report.add(
                Finding(
                    entry.name,
                    ANOMALY,
                    f"front matter field `{field_name}` must be a non-empty list "
                    f"(found {type(value).__name__})",
                    f"{BASE_CONTRACT}:Required Front Matter",
                    "8/12",
                )
            )


def _check_identity(entry: Entry, report: Report) -> None:
    artifact = entry.front_matter.get("artifact")
    if isinstance(artifact, str) and artifact != REQUIRED_ARTIFACT:
        report.add(
            Finding(
                entry.name,
                ANOMALY,
                f"`artifact` must be `{REQUIRED_ARTIFACT}` (found `{artifact}`)",
                f"{BASE_CONTRACT}:Completion Criteria",
                "8",
            )
        )
    kind = entry.front_matter.get("kind")
    if isinstance(kind, str) and kind != REQUIRED_KIND:
        report.add(
            Finding(
                entry.name,
                ANOMALY,
                f"`kind` must be `{REQUIRED_KIND}` (found `{kind}`)",
                f"{BASE_CONTRACT}:Required Front Matter",
                "8",
            )
        )
    title = entry.front_matter.get("title")
    heading = entry.title_heading
    if heading is None:
        report.add(
            Finding(
                entry.name,
                ANOMALY,
                "the body declares no `#` title heading",
                f"{BASE_CONTRACT}:Completion Criteria",
                "8",
            )
        )
    elif isinstance(title, str) and title.strip() and heading != title.strip():
        report.add(
            Finding(
                entry.name,
                ANOMALY,
                f"the `#` heading `{heading}` does not match the `title` field "
                f"`{title.strip()}`",
                f"{BASE_CONTRACT}:Completion Criteria",
                "8",
            )
        )


def _check_sections(
    entry: Entry, contract: Contract | None, base_sections: Sequence[str], report: Report
) -> None:
    required = list(base_sections)
    rule = f"{BASE_CONTRACT}:Sections"
    if contract is not None:
        for name in contract.required_sections:
            if name not in required:
                required.append(name)
        rule = f"{contract.source}:Required sections"
    for name in required:
        if name not in entry.headings:
            report.add(
                Finding(
                    entry.name,
                    ANOMALY,
                    f"the required section `## {name}` is missing",
                    rule,
                    "8/12",
                )
            )


def _check_provenance(
    entry: Entry, contract: Contract | None, root: Path, report: Report
) -> None:
    """Resolve every ``source_files`` entry.

    Two reserved values are admitted under the classes the base contract
    declares: ``system_probe`` for environment entries and ``project_scan`` for
    an absence or a tree fact outside one. Each is an ``ANOMALY`` in the wrong
    class. Any other entry must resolve: since the contract can express the
    absence/tree-fact class (RFC-79 decision 2), an unresolvable path is a
    violation of D01 item 5 and is reported ``ANOMALY``.
    """
    sources = entry.front_matter.get("source_files")
    if not isinstance(sources, list):
        return
    is_environment = bool(contract is not None and contract.is_environment)
    for source in sources:
        if not isinstance(source, str) or not source.strip():
            report.add(
                Finding(
                    entry.name,
                    ANOMALY,
                    "`source_files` contains a non-string or empty entry",
                    f"{BASE_CONTRACT}:Optional Front Matter (provenance)",
                    "5",
                )
            )
            continue
        candidate = source.strip()
        if candidate == SYSTEM_PROBE:
            if is_environment:
                report.add(
                    Finding(
                        entry.name,
                        VALID,
                        f"`{SYSTEM_PROBE}` is admitted: this is the environment entry",
                        f"{BASE_CONTRACT}:Optional Front Matter (provenance)",
                        "5",
                    )
                )
            else:
                report.add(
                    Finding(
                        entry.name,
                        ANOMALY,
                        f"`{SYSTEM_PROBE}` is a valid source only for environment "
                        f"entries, and this entry is not one",
                        f"{BASE_CONTRACT}:Optional Front Matter (provenance)",
                        "5",
                    )
                )
            continue
        if candidate == PROJECT_SCAN:
            if is_environment:
                report.add(
                    Finding(
                        entry.name,
                        ANOMALY,
                        f"`{PROJECT_SCAN}` is a valid source only for an absence or a "
                        f"tree fact outside an environment entry, and this entry is "
                        f"the environment entry",
                        f"{BASE_CONTRACT}:Optional Front Matter (provenance)",
                        "5",
                    )
                )
            else:
                report.add(
                    Finding(
                        entry.name,
                        VALID,
                        f"`{PROJECT_SCAN}` is admitted: a reserved provenance value "
                        f"for an absence or a tree fact established by scanning the "
                        f"project tree",
                        f"{BASE_CONTRACT}:Optional Front Matter (provenance)",
                        "5",
                    )
                )
            continue
        if candidate.startswith("/") or ".." in Path(candidate).parts:
            report.add(
                Finding(
                    entry.name,
                    ANOMALY,
                    f"`source_files` entry `{candidate}` is not a project-relative path",
                    f"{BASE_CONTRACT}:Optional Front Matter (provenance)",
                    "5",
                )
            )
            continue
        if (root / candidate).exists():
            continue
        report.add(
            Finding(
                entry.name,
                ANOMALY,
                f"`source_files` entry `{candidate}` does not resolve in the project, "
                f"and it is not a reserved value: D01 item 5 requires every "
                f"`source_files` entry to point to an existing path, and an absence "
                f"or a tree fact is declared with `{PROJECT_SCAN}` "
                f"(RFC-79 decision 2)",
                f"{BASE_CONTRACT}:Optional Front Matter (provenance)",
                "5",
            )
        )


def check_entry(
    name: str,
    text: str,
    *,
    contract: Contract | None,
    base_sections: Sequence[str],
    root: Path,
    report: Report,
) -> Entry | None:
    """Run every deterministic entry check; return the parsed entry."""
    entry = parse_entry(name, text)
    if entry is None:
        report.add(
            Finding(
                name,
                ANOMALY,
                "the entry does not begin with a well-formed, delimited TOML front "
                "matter block (`+++` ... `+++`)",
                f"{BASE_CONTRACT}:Required Front Matter",
                "8",
            )
        )
        return None
    _check_required_fields(entry, report)
    _check_identity(entry, report)
    _check_sections(entry, contract, base_sections, report)
    _check_provenance(entry, contract, root, report)
    return entry


# --------------------------------------------------------------------------- #
# Manifest checks
# --------------------------------------------------------------------------- #


def parse_manifest(text: str) -> Mapping[str, Any] | None:
    try:
        return tomllib.loads(text)
    except tomllib.TOMLDecodeError:
        return None


def check_manifest(
    text: str,
    *,
    present_files: Sequence[str],
    required_tables: Sequence[tuple[str, Sequence[str]]],
    contract_ref: str,
    report: Report,
) -> Mapping[str, Any] | None:
    """Validate the manifest's structure and its coherence with the files."""
    target = MANIFEST_NAME
    manifest = parse_manifest(text)
    if manifest is None:
        report.add(
            Finding(
                target,
                ANOMALY,
                "the manifest is not parseable TOML",
                f"{contract_ref}:Format",
                "8",
            )
        )
        return None

    for table, fields in required_tables:
        if table == "runtime":
            continue
        section = manifest.get(table)
        if not isinstance(section, Mapping):
            report.add(
                Finding(
                    target,
                    ANOMALY,
                    f"the required TOML section `[{table}]` is missing",
                    f"{contract_ref}:Required sections",
                    "8",
                )
            )
            continue
        for field_name in fields:
            if field_name not in section:
                report.add(
                    Finding(
                        target,
                        ANOMALY,
                        f"`[{table}]` is missing the required field `{field_name}`",
                        f"{contract_ref}:Required sections",
                        "8",
                    )
                )

    shape = None
    knowledge_base = manifest.get("knowledge_base")
    if isinstance(knowledge_base, Mapping):
        shape = knowledge_base.get("project_shape")
        if isinstance(shape, str) and shape not in PROJECT_SHAPES:
            report.add(
                Finding(
                    target,
                    ANOMALY,
                    f"`project_shape` must be one of "
                    f"{', '.join(sorted(PROJECT_SHAPES))} (found `{shape}`)",
                    f"{contract_ref}:Required sections",
                    "11",
                )
            )
        if "project_shape" not in knowledge_base:
            # ``F-16``: which shape a repository should have is a classification
            # decision, so a *missing* shape is reported as a boundary (human
            # review), not as a contradiction this tool may resolve.
            report.add(
                Finding(
                    target,
                    BOUNDARY,
                    "`[knowledge_base] project_shape` is absent: the shape drives "
                    "`api.md` and `distribution.md`, and deciding it is a "
                    "classification decision (`F-16`), so it is left to human review",
                    f"{contract_ref}:Required sections",
                    "9/10/11",
                )
            )

    entries = manifest.get("entries")
    active: list[str] = []
    stale: list[str] = []
    if isinstance(entries, Mapping):
        raw_active = entries.get("active")
        raw_stale = entries.get("stale")
        if not isinstance(raw_active, list):
            report.add(
                Finding(
                    target,
                    ANOMALY,
                    "`[entries] active` must be a list",
                    f"{contract_ref}:Required sections",
                    "8",
                )
            )
        else:
            active = [item for item in raw_active if isinstance(item, str)]
        if not isinstance(raw_stale, list):
            report.add(
                Finding(
                    target,
                    ANOMALY,
                    "`[entries] stale` must be a list",
                    f"{contract_ref}:Required sections",
                    "8",
                )
            )
        else:
            stale = [item for item in raw_stale if isinstance(item, str)]

    present = set(present_files)
    listed = set(active) | set(stale)
    for name in sorted(present - listed):
        report.add(
            Finding(
                target,
                ANOMALY,
                f"`{name}` exists in the knowledge base but the manifest does not "
                "list it in `[entries]`",
                f"{contract_ref}:Notes",
                "8",
            )
        )
    for name in sorted(set(active) - present):
        report.add(
            Finding(
                target,
                ANOMALY,
                f"the manifest lists `{name}` as active but the file does not exist",
                f"{contract_ref}:Notes",
                "8",
            )
        )
    for name in sorted(set(stale) & present):
        report.add(
            Finding(
                target,
                ANOMALY,
                f"the manifest lists `{name}` as stale and the file is present",
                f"{contract_ref}:Notes",
                "8",
            )
        )
    for name in sorted(set(active) & set(stale)):
        report.add(
            Finding(
                target,
                ANOMALY,
                f"`{name}` is listed as both active and stale",
                f"{contract_ref}:Notes",
                "8",
            )
        )
    return manifest


# --------------------------------------------------------------------------- #
# The knowledge base as a whole
# --------------------------------------------------------------------------- #


def _read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except OSError as exc:
        raise ReadError(f"cannot read {path}: {exc}") from exc


def check_knowledge_base(
    root: Path,
    payload: Path,
    report: Report,
    *,
    payload_rel: str | None = None,
) -> None:
    """Inspect the whole discovery knowledge base and populate the report."""
    contracts = load_contracts(payload, payload_rel)
    base_sections = load_base_required_sections(payload)
    manifest_tables = load_manifest_required_sections(payload)

    kb_dir = root / PLANS_KB_DIR
    if not kb_dir.is_dir():
        report.add(
            Finding(
                PLANS_KB_DIR,
                NOT_APPLICABLE,
                "no discovery knowledge base in this project: declared absence, "
                "which is valid (nothing is claimed about it and nothing is a "
                "failure)",
                f"{DOC_REF}:Input",
                "",
            )
        )
        return

    entry_files = sorted(
        path for path in kb_dir.iterdir() if path.is_file() and path.name.endswith(".md")
    )
    manifest_path = kb_dir / MANIFEST_NAME

    if not entry_files and not manifest_path.is_file():
        report.add(
            Finding(
                PLANS_KB_DIR,
                NOT_APPLICABLE,
                "the knowledge base directory exists and declares no entries and no "
                "manifest: declared absence",
                f"{DOC_REF}:Input",
                "",
            )
        )
        return

    entries: dict[str, Entry] = {}
    for path in entry_files:
        text = _read_text(path)
        if not text.strip():
            report.add(
                Finding(
                    path.name,
                    ANOMALY,
                    "the entry is empty",
                    f"{BASE_CONTRACT}:Completion Criteria",
                    "8",
                )
            )
            continue
        contract = contracts.get(path.name)
        if contract is None:
            report.add(
                Finding(
                    path.name,
                    BOUNDARY,
                    "no per-entry contract declares this file as its runtime "
                    "artifact, so its required sections cannot be resolved from a "
                    "contract (`F-16`-class model question): human review, never "
                    "guessed",
                    f"{DOC_REF}:Checklist item 12",
                    "12",
                )
            )
        entry = check_entry(
            path.name,
            text,
            contract=contract,
            base_sections=base_sections,
            root=root,
            report=report,
        )
        if entry is not None:
            entries[path.name] = entry

    manifest: Mapping[str, Any] | None = None
    if manifest_path.is_file():
        manifest = check_manifest(
            _read_text(manifest_path),
            present_files=[path.name for path in entry_files],
            required_tables=manifest_tables,
            contract_ref=f"protocol/.agents/{CONTRACTS_DIR}/{MANIFEST_CONTRACT}",
            report=report,
        )
    else:
        report.add(
            Finding(
                MANIFEST_NAME,
                GAP,
                "the knowledge base has entries but no manifest: the entry list and "
                "the shape cannot be cross-checked (missing evidence, advisory)",
                f"protocol/.agents/{CONTRACTS_DIR}/{MANIFEST_CONTRACT}:Location",
                "8",
            )
        )

    _check_project_shape(entries, manifest, report)
    _check_distribution(entries, manifest, report)


def _manifest_shape(manifest: Mapping[str, Any] | None) -> str | None:
    if not isinstance(manifest, Mapping):
        return None
    knowledge_base = manifest.get("knowledge_base")
    if not isinstance(knowledge_base, Mapping):
        return None
    shape = knowledge_base.get("project_shape")
    return shape if isinstance(shape, str) else None


def _check_project_shape(
    entries: Mapping[str, Entry],
    manifest: Mapping[str, Any] | None,
    report: Report,
) -> None:
    """Check ``## Project Shape``: present, first content section, and matching.

    The contract requires the section to be the first content section after the
    front matter and to match the manifest. Which shape is *correct* is a
    classification decision and is never judged here.
    """
    summary = entries.get("executive_summary.md")
    if summary is None:
        return
    contract_ref = f"protocol/.agents/{CONTRACTS_DIR}/EXECUTIVE_SUMMARY.md"
    if "Project Shape" not in summary.headings:
        report.add(
            Finding(
                summary.name,
                ANOMALY,
                "the required section `## Project Shape` is missing",
                f"{contract_ref}:Required sections",
                "9",
            )
        )
        return
    if summary.headings and summary.headings[0] != "Project Shape":
        report.add(
            Finding(
                summary.name,
                ANOMALY,
                f"`## Project Shape` must be the first content section after the "
                f"front matter (found `## {summary.headings[0]}` first)",
                f"{contract_ref}:Required sections",
                "9",
            )
        )
    manifest_shape = _manifest_shape(manifest)
    declared = _first_heading_value(summary, "Project Shape")
    if manifest_shape is None:
        return
    if declared is None:
        report.add(
            Finding(
                summary.name,
                BOUNDARY,
                "`## Project Shape` declares no recognizable value, so it cannot be "
                "compared with the manifest: human review",
                f"{contract_ref}:Required sections",
                "9",
            )
        )
        return
    if declared != manifest_shape:
        report.add(
            Finding(
                summary.name,
                ANOMALY,
                f"`## Project Shape` declares `{declared}` but the manifest declares "
                f"`{manifest_shape}`",
                f"{contract_ref}:Required sections",
                "9",
            )
        )


def _first_heading_value(entry: Entry, heading: str) -> str | None:
    """The first recognizable shape token in the body of ``## <heading>``."""
    pattern = re.compile(
        r"^##\s+" + re.escape(heading) + r"\s*$(?P<body>.*?)(?=^##\s|\Z)",
        re.MULTILINE | re.DOTALL,
    )
    match = pattern.search(entry.body)
    if match is None:
        return None
    body = match.group("body")
    backticked = re.search(r"`([^`]+)`", body)
    token = backticked.group(1).strip() if backticked else None
    if token is None:
        words = re.findall(r"[A-Za-z]+", body)
        token = words[0] if words else None
    if token is None:
        return None
    candidate = token.strip().strip("*_").strip().casefold()
    return candidate or None


def _check_distribution(
    entries: Mapping[str, Entry],
    manifest: Mapping[str, Any] | None,
    report: Report,
) -> None:
    """``distribution.md`` is mandatory for the ``library`` and ``cli`` shapes."""
    shape = _manifest_shape(manifest)
    if shape is None:
        return
    if shape not in DISTRIBUTION_SHAPES:
        return
    if "distribution.md" in entries:
        return
    report.add(
        Finding(
            "distribution.md",
            ANOMALY,
            f"`project_shape` is `{shape}` and `distribution.md` is required for "
            "that shape, but the entry is absent",
            f"protocol/.agents/{CONTRACTS_DIR}/DISTRIBUTION.md:Required sections",
            "10",
        )
    )


# --------------------------------------------------------------------------- #
# Reporting
# --------------------------------------------------------------------------- #


def render_text(report: Report) -> str:
    lines = ["Discovery output check (D01 mechanical subset, plan 136):"]
    for target, signal, items in report.per_target():
        lines.append(f"- {target}: {signal} - {items[0].reason}")
        for item in items[1:]:
            lines.append(f"    - {item.signal}: {item.reason}")
    counts = report.counts()
    summary = ", ".join(
        f"{signal}={counts[signal]}" for signal in _SIGNAL_PRECEDENCE if counts[signal]
    )
    lines.append(f"Summary: {summary or 'no artifacts inspected'}")
    return "\n".join(lines)


def render_json(report: Report) -> str:
    payload = {
        "tool": "check_discovery_output",
        "plan": 136,
        "d01_item_scope": "mechanical subset: structure and resolvable provenance",
        "results": [item.to_dict() for item in report.findings],
        "per_target": [
            {"target": target, "signal": signal, "findings": len(items)}
            for target, signal, items in report.per_target()
        ],
        "counts": report.counts(),
    }
    return json.dumps(payload, indent=2, ensure_ascii=False, sort_keys=True)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="python tools/check_discovery_output.py",
        description=(
            "Check the mechanical subset of D01 (discovery output structure and "
            "resolvable provenance) over a discovery knowledge base."
        ),
    )
    parser.add_argument(
        "--root",
        type=Path,
        default=None,
        help="project root holding .project/knowledge/discovery (default: cwd)",
    )
    parser.add_argument(
        "--payload",
        type=Path,
        default=None,
        help="protocol payload holding the discovery contracts (default: <root>/protocol/.agents)",
    )
    parser.add_argument("--json", action="store_true", help="machine-readable output")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    root = (args.root or Path.cwd()).resolve()
    payload = (
        args.payload.resolve()
        if args.payload is not None
        else root / "protocol" / ".agents"
    )
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")

    report = Report()
    payload_rel = _citation_prefix(root, payload)
    try:
        check_knowledge_base(root, payload, report, payload_rel=payload_rel)
    except ReadError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2

    print(render_json(report) if args.json else render_text(report))
    return 1 if report.has_anomaly else 0


def _citation_prefix(root: Path, payload: Path) -> str:
    """The repository-relative prefix used to cite payload contracts.

    Falls back to the absolute path when the payload is not inside the project
    root, so a finding never cites a contract by an ambiguous fragment.
    """
    try:
        return payload.relative_to(root).as_posix()
    except ValueError:
        return payload.as_posix()


if __name__ == "__main__":
    sys.exit(main())
