"""Behaviour and falsification tests of the D01 mechanical checker (plan 136).

Two halves, deliberately:

- **behaviour** — a valid discovery knowledge base is ``VALID`` and exits 0, and
  a project with no knowledge base is a declared absence, not a failure;
- **falsification** — the checker *refuses* to accept: a title that does not
  match, a wrong ``artifact``/``kind``, a missing required section, a
  ``system_probe`` used outside the environment entry, a ``project_scan`` used in
  the environment entry, an unresolvable ``source_files`` entry that is not a
  reserved value, a manifest that disagrees with the files, a shape outside the
  enum, a shape that contradicts ``executive_summary``, ``distribution.md``
  absent for a ``library``/``cli`` shape, corrupt front matter.

The frontier tests are the point of the suite: the checker must **not** silently
perform the judgement items of D01 and must **not** grant an ad-hoc exemption for
an unresolvable ``source_files`` entry. Since RFC-79 decision 2 the contract can
express the absence/tree-fact class (``project_scan``), so an unresolvable entry
that is not a reserved value is a violation of D01 item 5 and is reported
``ANOMALY``; while the class had no value, the same case was the declared ``F-17``
boundary and was reported ``GAP``.

Everything here is isolated (``tests/AGENTS.md``): the fixtures are synthetic and
the contracts are a synthetic payload, so the real payload can evolve without
breaking these tests. The payload coupling is exercised on purpose by
``tests/test_discovery_output_dogfood.py`` instead.
"""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))

import check_discovery_output as checker  # noqa: E402

# --------------------------------------------------------------------------- #
# Synthetic fixtures
# --------------------------------------------------------------------------- #

#: A synthetic payload contract for one entry type, in the same shape the real
#: contracts use: a ``## Location`` line declaring the runtime path, and
#: backticked level-2 headings declaring the required sections.
CONTRACT_TEMPLATE = """+++
artifact = "{stem}.md"
+++

# {stem} Contract

## Purpose

Synthetic contract used only by this suite.

## Location

`.project/knowledge/discovery/{runtime}`

## Required sections

### `## Summary`

### `## Discovered Facts`

{extra_sections}## Base format

The entry follows the base KB entry contract defined in KB_DISCOVERY_ENTRY.md.
"""

BASE_CONTRACT = """+++
artifact = "KB_DISCOVERY_ENTRY.md"
+++

# KB Discovery Entry Contract

## Required Front Matter

TOML front matter delimited by `+++`.

## Sections

### `## Summary`

### `## Discovered Facts`

## Optional Front Matter (provenance)

`status` is `active`, `stale` or `legacy`.

`system_probe` is a valid source only for environment entries. `project_scan` is
a valid source only for an absence or a tree fact, and never in an environment
entry.
"""

MANIFEST_CONTRACT = """# DISCOVERY_MANIFEST Contract

## Location

`.project/knowledge/discovery/.discovery_manifest`

## Required sections

### `[knowledge_base]`

- `version`: string
- `project_shape`: string

### `[hashes]`

- `config_files_hash`: string

### `[entries]`

- `active`: list of strings
- `stale`: list of strings
- `legacy`: list of strings

### `[workers]`

- `invoked`: list of strings
"""

ENTRY_TEMPLATE = """+++
artifact = "KB_DISCOVERY_ENTRY.md"
kind = "snapshot"
title = "{title}"
generated_at = "2026-09-15T00:00:00Z"
tags = ["discovery", "{tag}"]
source_files = [{sources}]
+++

# {title}

{custom_sections}## Summary

_No deterministic facts found for this category._

## Discovered Facts

- **synthetic**: value
"""

#: The ``## Project Shape`` section needs a recognizable value, which the
#: contract makes the first content section after the front matter.
SHAPE_SECTION = "## Project Shape\n\n`{shape}`\n\n"

PROJECT_FILES = ("pyproject.toml", "src/main.py", "docker-compose.yml")


def write_payload(
    payload: Path,
    *,
    extra_types: dict[str, str] | None = None,
    base: str = BASE_CONTRACT,
    manifest: str = MANIFEST_CONTRACT,
) -> Path:
    """Build a synthetic payload whose contracts declare runtime paths."""
    contracts = payload / checker.CONTRACTS_DIR
    contracts.mkdir(parents=True, exist_ok=True)
    (contracts / "KB_DISCOVERY_ENTRY.md").write_text(base, encoding="utf-8")
    (contracts / "DISCOVERY_MANIFEST.md").write_text(manifest, encoding="utf-8")
    # A default set of entry types: one ordinary entry, the environment entry,
    # the executive summary and the distribution entry.
    types = {
        "STACK": ("stack.md", ""),
        "ENVIRONMENT_DISCOVERY": ("environment.md", ""),
        "EXECUTIVE_SUMMARY": ("executive_summary.md", "### `## Project Shape`\n\n"),
        "DISTRIBUTION": ("distribution.md", ""),
        # Entry types whose contracts declare an extra section, used by the
        # structural and provenance cases below.
        "CONTAINERS": ("containers.md", "### `## Container Definitions`\n\n"),
        "FILE_MAP": ("file_map.md", "### `## Map`\n\n"),
        "ARCHITECTURE": ("architecture.md", "### `## Security`\n\n"),
    }
    types.update(extra_types or {})
    for stem, (runtime, extra) in types.items():
        (contracts / f"{stem}.md").write_text(
            CONTRACT_TEMPLATE.format(stem=stem, runtime=runtime, extra_sections=extra),
            encoding="utf-8",
        )
    # The environment contract is the one that mentions the probe token, exactly
    # as the real ENVIRONMENT_DISCOVERY.md does.
    if "ENVIRONMENT_DISCOVERY" in types:
        env = contracts / "ENVIRONMENT_DISCOVERY.md"
        env.write_text(
            env.read_text(encoding="utf-8")
            + "\nEnvironment facts may use `system_probe` as a source.\n",
            encoding="utf-8",
        )
    return payload


def write_entry(
    kb: Path,
    name: str,
    *,
    title: str | None = None,
    artifact: str = "KB_DISCOVERY_ENTRY.md",
    kind: str = "snapshot",
    tag: str = "stack",
    sources: tuple[str, ...] = ("pyproject.toml",),
    custom_sections: tuple[str, ...] = (),
    shape: str | None = None,
    omit_facts: bool = False,
    omit_summary: bool = False,
) -> Path:
    """Write one KB entry; ``title`` defaults to a name derived from ``name``.

    ``custom_sections`` are rendered **before** the base sections so a required
    ``## Project Shape`` can be the first content section, as its contract demands.
    """
    heading = title if title is not None else name.replace(".md", "").replace("_", " ").title()
    # ``shape`` writes the Project Shape section first; ``custom_sections`` follow
    # it, so an explicit order can be produced without ``shape``.
    rendered = SHAPE_SECTION.format(shape=shape) if shape is not None else ""
    rendered += "".join(f"## {section}\n\ncontent\n\n" for section in custom_sections)
    body = ENTRY_TEMPLATE.format(
        title=heading,
        tag=tag,
        sources=", ".join(f'"{s}"' for s in sources),
        custom_sections=rendered,
    )
    if omit_facts:
        body = body.replace("## Discovered Facts\n\n- **synthetic**: value\n", "")
    if omit_summary:
        body = body.replace("## Summary\n\n_No deterministic facts found for this category._\n\n", "")
    if artifact != "KB_DISCOVERY_ENTRY.md":
        body = body.replace('artifact = "KB_DISCOVERY_ENTRY.md"', f'artifact = "{artifact}"')
    if kind != "snapshot":
        body = body.replace('kind = "snapshot"', f'kind = "{kind}"')
    path = kb / name
    path.write_text(body, encoding="utf-8")
    return path


def write_manifest(
    kb: Path,
    *,
    shape: str = "application",
    active: tuple[str, ...] = (),
    stale: tuple[str, ...] = (),
    legacy: tuple[str, ...] = (),
    omit_shape: bool = False,
    omit_legacy: bool = False,
    corrupt: bool = False,
    extra: str = "",
) -> Path:
    if corrupt:
        body = "this is not = valid toml [[[\n"
    else:
        shape_line = "" if omit_shape else f'project_shape = "{shape}"\n'
        active_list = ", ".join(f'"{name}"' for name in active)
        stale_list = ", ".join(f'"{name}"' for name in stale)
        legacy_list = ", ".join(f'"{name}"' for name in legacy)
        # ``[entries] legacy`` is a required list of the contract (RFC-79
        # decision 1): absent means the manifest violates its own contract.
        legacy_line = "" if omit_legacy else f"legacy = [{legacy_list}]\n"
        body = f"""[knowledge_base]
version = "1.0.0"
generated_at = "2026-09-15T00:00:00Z"
updated_at = "2026-09-15T00:00:00Z"
ttl_hours = 24
role_version = "discovery_orchestrator:v1"
task_scope = "full"
project_root = "/tmp/project"
{shape_line}
[hashes]
config_files_hash = "sha256:aaa"

[entries]
active = [{active_list}]
stale = [{stale_list}]
{legacy_line}
[workers]
invoked = ["stack_worker"]
{extra}"""
    path = kb / checker.MANIFEST_NAME
    path.write_text(body, encoding="utf-8")
    return path


def make_project(tmp_path: Path, *, shape: str = "application") -> tuple[Path, Path, Path]:
    """A valid project: root, payload and knowledge base.

    The project files the entries cite really exist, so the valid baseline has no
    ``GAP``: the point of the baseline is that everything mechanical holds.
    """
    root = tmp_path / "project"
    payload = tmp_path / "payload"
    kb = root / checker.PLANS_KB_DIR
    kb.mkdir(parents=True, exist_ok=True)
    write_payload(payload)
    for relative in PROJECT_FILES:
        target = root / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text("# synthetic project file\n", encoding="utf-8")
    write_entry(kb, "stack.md", tag="stack")
    write_entry(
        kb,
        "executive_summary.md",
        title="Executive Summary",
        tag="executive_summary",
        shape=shape,
    )
    write_manifest(kb, shape=shape, active=("stack.md", "executive_summary.md"))
    return root, payload, kb


def run(root: Path, payload: Path) -> tuple[int, checker.Report]:
    report = checker.Report()
    checker.check_knowledge_base(root, payload, report, payload_rel="payload")
    return (1 if report.has_anomaly else 0), report


def signals(report: checker.Report, target: str | None = None) -> set[str]:
    return {
        finding.signal
        for finding in report.findings
        if target is None or finding.target == target
    }


def reasons(report: checker.Report) -> str:
    return " | ".join(finding.reason for finding in report.findings)


# --------------------------------------------------------------------------- #
# Positives
# --------------------------------------------------------------------------- #


def test_a_valid_knowledge_base_is_valid_and_exits_zero(tmp_path):
    root, payload, _ = make_project(tmp_path)
    code, report = run(root, payload)
    assert code == 0
    assert report.has_anomaly is False
    assert checker.ANOMALY not in signals(report)


def test_a_library_shape_with_distribution_present_is_valid(tmp_path):
    root, payload, kb = make_project(tmp_path, shape="library")
    write_entry(kb, "distribution.md", tag="distribution")
    write_manifest(
        kb,
        shape="library",
        active=("stack.md", "executive_summary.md", "distribution.md"),
    )
    code, report = run(root, payload)
    assert code == 0, reasons(report)


def test_system_probe_is_valid_in_the_environment_entry(tmp_path):
    root, payload, kb = make_project(tmp_path)
    write_entry(kb, "environment.md", tag="environment", sources=("system_probe",))
    write_manifest(
        kb, active=("stack.md", "executive_summary.md", "environment.md")
    )
    code, report = run(root, payload)
    assert code == 0, reasons(report)
    assert checker.VALID in signals(report, "environment.md")


def test_a_project_without_a_knowledge_base_is_a_declared_absence(tmp_path):
    root = tmp_path / "empty"
    root.mkdir()
    payload = tmp_path / "payload"
    write_payload(payload)
    code, report = run(root, payload)
    assert code == 0
    assert signals(report) == {checker.NOT_APPLICABLE}
    assert "declared absence" in reasons(report)


def test_an_empty_knowledge_base_directory_is_a_declared_absence(tmp_path):
    root = tmp_path / "empty"
    (root / checker.PLANS_KB_DIR).mkdir(parents=True)
    payload = tmp_path / "payload"
    write_payload(payload)
    code, report = run(root, payload)
    assert code == 0
    assert signals(report) == {checker.NOT_APPLICABLE}


# --------------------------------------------------------------------------- #
# Negatives: entry structure
# --------------------------------------------------------------------------- #


def test_title_differing_from_the_heading_is_an_anomaly(tmp_path):
    """The body's ``#`` heading must match the front-matter ``title``."""
    root, payload, kb = make_project(tmp_path)
    path = kb / "stack.md"
    path.write_text(
        path.read_text(encoding="utf-8").replace("\n# Stack\n", "\n# Something Else\n"),
        encoding="utf-8",
    )
    code, report = run(root, payload)
    assert code == 1
    assert checker.ANOMALY in signals(report, "stack.md")
    assert "does not match the `title` field" in reasons(report)


def test_wrong_artifact_is_an_anomaly(tmp_path):
    root, payload, kb = make_project(tmp_path)
    write_entry(kb, "stack.md", tag="stack", artifact="OTHER.md")
    code, report = run(root, payload)
    assert code == 1
    assert "`artifact` must be" in reasons(report)


def test_wrong_kind_is_an_anomaly(tmp_path):
    root, payload, kb = make_project(tmp_path)
    write_entry(kb, "stack.md", tag="stack", kind="note")
    code, report = run(root, payload)
    assert code == 1
    assert "`kind` must be" in reasons(report)


def test_missing_discovered_facts_is_an_anomaly(tmp_path):
    root, payload, kb = make_project(tmp_path)
    write_entry(kb, "stack.md", tag="stack", omit_facts=True)
    code, report = run(root, payload)
    assert code == 1
    assert "`## Discovered Facts` is missing" in reasons(report)


def test_missing_contract_declared_section_is_an_anomaly(tmp_path):
    root, payload, kb = make_project(
        tmp_path,
        shape="application",
    )
    # The contract for ``architecture.md`` declares extra sections; the entry
    # omits them.
    write_payload(
        payload,
        extra_types={"ARCHITECTURE": ("architecture.md", "### `## Security`\n\n")},
    )
    write_entry(kb, "architecture.md", tag="architecture")
    write_manifest(
        kb,
        active=("stack.md", "executive_summary.md", "architecture.md"),
    )
    code, report = run(root, payload)
    assert code == 1
    assert "`## Security` is missing" in reasons(report)


def test_missing_summary_is_an_anomaly(tmp_path):
    root, payload, kb = make_project(tmp_path)
    text = (kb / "stack.md").read_text(encoding="utf-8")
    (kb / "stack.md").write_text(
        text.replace("## Summary\n\n_No deterministic facts found for this category._\n\n", ""),
        encoding="utf-8",
    )
    code, report = run(root, payload)
    assert code == 1
    assert "`## Summary` is missing" in reasons(report)


def test_a_non_list_tags_field_is_an_anomaly(tmp_path):
    root, payload, kb = make_project(tmp_path)
    text = (kb / "stack.md").read_text(encoding="utf-8")
    (kb / "stack.md").write_text(
        text.replace('tags = ["discovery", "stack"]', 'tags = "discovery"'),
        encoding="utf-8",
    )
    code, report = run(root, payload)
    assert code == 1
    assert "`tags` must be a non-empty list" in reasons(report)


def test_a_missing_required_field_is_an_anomaly(tmp_path):
    root, payload, kb = make_project(tmp_path)
    text = (kb / "stack.md").read_text(encoding="utf-8")
    (kb / "stack.md").write_text(
        text.replace('generated_at = "2026-09-15T00:00:00Z"\n', ""),
        encoding="utf-8",
    )
    code, report = run(root, payload)
    assert code == 1
    assert "missing the required field `generated_at`" in reasons(report)


# --------------------------------------------------------------------------- #
# Negatives: invalid data
# --------------------------------------------------------------------------- #


def test_front_matter_without_delimiters_is_an_anomaly(tmp_path):
    root, payload, kb = make_project(tmp_path)
    (kb / "stack.md").write_text("# Stack\n\n## Summary\n\ntext\n", encoding="utf-8")
    code, report = run(root, payload)
    assert code == 1
    assert "well-formed, delimited TOML front matter" in reasons(report)


def test_unparseable_front_matter_is_an_anomaly(tmp_path):
    root, payload, kb = make_project(tmp_path)
    (kb / "stack.md").write_text(
        '+++\nartifact = "unterminated\n+++\n\n# Stack\n', encoding="utf-8"
    )
    code, report = run(root, payload)
    assert code == 1
    assert "well-formed, delimited TOML front matter" in reasons(report)


def test_an_empty_entry_is_an_anomaly(tmp_path):
    root, payload, kb = make_project(tmp_path)
    (kb / "stack.md").write_text("", encoding="utf-8")
    code, report = run(root, payload)
    assert code == 1
    assert "the entry is empty" in reasons(report)


def test_an_unparseable_manifest_is_an_anomaly(tmp_path):
    root, payload, kb = make_project(tmp_path)
    write_manifest(kb, corrupt=True)
    code, report = run(root, payload)
    assert code == 1
    assert "is not parseable TOML" in reasons(report)


# --------------------------------------------------------------------------- #
# Negatives: provenance (RFC-79 decision 2 replaces the F-17 boundary)
# --------------------------------------------------------------------------- #


def test_an_unresolvable_source_file_is_an_anomaly(tmp_path):
    """D01 item 5 now has a value for the absence class, so an unresolvable path
    that is not reserved is a violation, not missing evidence.

    ``F-17`` was a declared boundary only while the contract had no provenance
    value for absences and tree facts. RFC-79 decision 2 added ``project_scan``,
    so the ambiguity is gone: a path that does not resolve and is not a reserved
    value contradicts D01 item 5.
    """
    root, payload, kb = make_project(tmp_path)
    write_entry(
        kb,
        "containers.md",
        tag="containers",
        sources=("compose-not-in-this-project.yml",),
        custom_sections=("Container Definitions",),
    )
    write_manifest(
        kb, active=("stack.md", "executive_summary.md", "containers.md")
    )
    code, report = run(root, payload)
    assert code == 1, reasons(report)
    assert checker.ANOMALY in signals(report, "containers.md")
    assert checker.GAP not in signals(report, "containers.md")
    assert "project_scan" in reasons(report)


def test_project_scan_is_valid_for_an_absence_outside_the_environment_entry(tmp_path):
    """The reserved value RFC-79 decision 2 introduced, in its legal class."""
    root, payload, kb = make_project(tmp_path)
    write_entry(
        kb,
        "containers.md",
        tag="containers",
        sources=("project_scan",),
        custom_sections=("Container Definitions",),
    )
    write_manifest(
        kb, active=("stack.md", "executive_summary.md", "containers.md")
    )
    code, report = run(root, payload)
    assert code == 0, reasons(report)
    assert checker.VALID in signals(report, "containers.md")
    assert checker.ANOMALY not in signals(report, "containers.md")


def test_project_scan_in_the_environment_entry_is_an_anomaly(tmp_path):
    """The boundary case: ``project_scan`` is never the environment class."""
    root, payload, kb = make_project(tmp_path)
    write_entry(
        kb,
        "environment.md",
        tag="environment",
        sources=("project_scan",),
    )
    write_manifest(
        kb, active=("stack.md", "executive_summary.md", "environment.md")
    )
    code, report = run(root, payload)
    assert code == 1
    assert "only for an absence or a tree fact" in reasons(report)


def test_both_reserved_values_are_rejected_outside_their_class(tmp_path):
    """Cross-check: neither reserved value leaks into the other's class."""
    root, payload, kb = make_project(tmp_path)
    write_entry(kb, "stack.md", tag="stack", sources=("system_probe",))
    write_entry(
        kb,
        "environment.md",
        tag="environment",
        sources=("project_scan",),
    )
    write_manifest(
        kb, active=("stack.md", "executive_summary.md", "environment.md")
    )
    code, report = run(root, payload)
    assert code == 1
    assert "valid source only for environment entries" in reasons(report)
    assert "only for an absence or a tree fact" in reasons(report)


def test_system_probe_outside_the_environment_entry_is_an_anomaly(tmp_path):
    root, payload, kb = make_project(tmp_path)
    write_entry(kb, "stack.md", tag="stack", sources=("system_probe",))
    code, report = run(root, payload)
    assert code == 1
    assert "valid source only for environment entries" in reasons(report)


def test_an_absolute_source_file_path_is_an_anomaly(tmp_path):
    root, payload, kb = make_project(tmp_path)
    write_entry(kb, "stack.md", tag="stack", sources=("/etc/passwd",))
    code, report = run(root, payload)
    assert code == 1
    assert "not a project-relative path" in reasons(report)


def test_a_traversing_source_file_path_is_an_anomaly(tmp_path):
    root, payload, kb = make_project(tmp_path)
    write_entry(kb, "stack.md", tag="stack", sources=("../../secrets.env",))
    code, report = run(root, payload)
    assert code == 1
    assert "not a project-relative path" in reasons(report)


# --------------------------------------------------------------------------- #
# Negatives: manifest and shape coherence
# --------------------------------------------------------------------------- #


def test_manifest_listing_an_absent_file_is_an_anomaly(tmp_path):
    root, payload, kb = make_project(tmp_path)
    write_manifest(kb, active=("stack.md", "executive_summary.md", "ghost.md"))
    code, report = run(root, payload)
    assert code == 1
    assert "lists `ghost.md` as active but the file does not exist" in reasons(report)


def test_an_entry_the_manifest_omits_is_an_anomaly(tmp_path):
    root, payload, kb = make_project(tmp_path)
    write_entry(kb, "extra.md", tag="extra")
    code, report = run(root, payload)
    assert code == 1
    assert "the manifest does not list it" in reasons(report)


def test_a_stale_entry_that_is_present_is_an_anomaly(tmp_path):
    root, payload, kb = make_project(tmp_path)
    write_entry(kb, "old.md", tag="old")
    write_manifest(
        kb,
        active=("stack.md", "executive_summary.md"),
        stale=("old.md",),
    )
    code, report = run(root, payload)
    assert code == 1
    assert "lists `old.md` as stale and the file is present" in reasons(report)


def test_an_entry_both_active_and_stale_is_an_anomaly(tmp_path):
    root, payload, kb = make_project(tmp_path)
    write_manifest(
        kb,
        active=("stack.md", "executive_summary.md"),
        stale=("stack.md",),
    )
    code, report = run(root, payload)
    assert code == 1


def test_a_shape_outside_the_enum_is_an_anomaly(tmp_path):
    root, payload, kb = make_project(tmp_path, shape="spaceship")
    code, report = run(root, payload)
    assert code == 1
    assert "`project_shape` must be one of" in reasons(report)


def test_a_missing_project_shape_is_reported(tmp_path):
    """A manifest without ``project_shape`` is reported, never silently accepted.

    The contract makes ``project_shape`` a required ``[knowledge_base]`` field, so
    its absence is a contradiction. Which shape is *correct* remains a
    classification decision the checker never makes (`F-16`).
    """
    root, payload, kb = make_project(tmp_path)
    write_manifest(kb, omit_shape=True, active=("stack.md", "executive_summary.md"))
    code, report = run(root, payload)
    assert code == 1
    assert "missing the required field `project_shape`" in reasons(report)


def test_the_documentation_shape_is_admitted(tmp_path):
    """RFC-79 decision 3: ``documentation`` is a declared shape, not ``unknown``.

    A documentary/standards/protocol product with no software surface of its own
    is determinable, so the enum admits it; ``unknown`` would assert that the
    shape could not be determined, and ``distribution.md`` stays legitimately
    absent because it is mandatory only for ``library``/``cli``.
    """
    root, payload, kb = make_project(tmp_path, shape="documentation")
    write_manifest(
        kb, shape="documentation", active=("stack.md", "executive_summary.md")
    )
    code, report = run(root, payload)
    assert code == 0, reasons(report)
    assert checker.ANOMALY not in signals(report, "stack.md")


def test_a_shape_outside_the_enum_is_not_silently_accepted(tmp_path):
    """``F-16``: the tool accepts only the declared enum; it never decides the
    right shape, and it never admits an undeclared synonym."""
    root, payload, kb = make_project(tmp_path)
    write_manifest(
        kb, shape="monolith", active=("stack.md", "executive_summary.md")
    )
    code, report = run(root, payload)
    assert code == 1
    assert "`project_shape` must be one of" in reasons(report)


def test_missing_project_shape_section_in_executive_summary_is_an_anomaly(tmp_path):
    root, payload, kb = make_project(tmp_path)
    write_entry(
        kb, "executive_summary.md", title="Executive Summary", tag="executive_summary"
    )
    code, report = run(root, payload)
    assert code == 1
    assert "`## Project Shape` is missing" in reasons(report)


def test_project_shape_not_first_section_is_an_anomaly(tmp_path):
    """The contract requires ``## Project Shape`` to be the first content section."""
    root, payload, kb = make_project(tmp_path)
    # A shape whose section is NOT first: bypass the helper's ordering.
    write_entry(
        kb,
        "executive_summary.md",
        title="Executive Summary",
        tag="executive_summary",
        custom_sections=("Project Purpose",),
    )
    path = kb / "executive_summary.md"
    path.write_text(
        path.read_text(encoding="utf-8").replace(
            "## Project Purpose\n", "## Project Purpose\n\n`application`\n\n## Project Shape\n"
        ),
        encoding="utf-8",
    )
    code, report = run(root, payload)
    assert code == 1
    assert "must be the first content section" in reasons(report)


def test_project_shape_disagreeing_with_the_manifest_is_an_anomaly(tmp_path):
    root, payload, kb = make_project(tmp_path, shape="application")
    write_entry(
        kb,
        "executive_summary.md",
        title="Executive Summary",
        tag="executive_summary",
        shape="cli",
    )
    code, report = run(root, payload)
    assert code == 1
    assert "but the manifest declares" in reasons(report)


def test_distribution_missing_for_a_library_shape_is_an_anomaly(tmp_path):
    root, payload, kb = make_project(tmp_path, shape="library")
    code, report = run(root, payload)
    assert code == 1
    assert "`distribution.md` is required for that shape" in reasons(report)


def test_an_unknown_entry_type_is_a_boundary_not_an_anomaly(tmp_path):
    root, payload, kb = make_project(tmp_path)
    write_entry(kb, "mystery.md", tag="mystery")
    write_manifest(
        kb, active=("stack.md", "executive_summary.md", "mystery.md")
    )
    code, report = run(root, payload)
    assert code == 0, reasons(report)
    assert checker.BOUNDARY in signals(report, "mystery.md")


# --------------------------------------------------------------------------- #
# The frontier: what the checker must NOT do
# --------------------------------------------------------------------------- #


def test_the_checker_does_not_perform_the_judgement_items(tmp_path):
    """Stack reality, dependency reality and unsourced claims stay judgement.

    The checker must say nothing about them: silence is the declared boundary,
    not an approval. A KB whose facts are entirely fictional yet structurally
    valid is ``VALID`` — the checker never claims the facts are true.
    """
    root, payload, kb = make_project(tmp_path)
    write_entry(
        kb,
        "stack.md",
        tag="stack",
        sources=("pyproject.toml",),
    )
    (root / "pyproject.toml").write_text("[project]\nname='x'\n", encoding="utf-8")
    code, report = run(root, payload)
    assert code == 0, reasons(report)
    text = reasons(report)
    for judgement in (
        "stack",
        "dependenc",
        "pattern",
        "secret",
        "claim",
        "merge",
        "api",
    ):
        assert judgement not in text.casefold(), judgement


def test_no_ad_hoc_exemption_is_granted_for_f17(tmp_path):
    """Every unresolvable source is reported; none is silently allowed."""
    root, payload, kb = make_project(tmp_path)
    write_entry(
        kb,
        "file_map.md",
        tag="file_map",
        sources=("does-not-exist.md", "also-missing.yml"),
        custom_sections=("Map",),
    )
    write_manifest(kb, active=("stack.md", "executive_summary.md", "file_map.md"))
    code, report = run(root, payload)
    assert code == 1
    unresolved = [
        finding
        for finding in report.findings
        if finding.target == "file_map.md" and finding.signal == checker.ANOMALY
    ]
    assert len(unresolved) == 2, reasons(report)


def test_a_manifest_without_the_legacy_list_is_an_anomaly(tmp_path):
    """RFC-79 decision 1: ``[entries] legacy`` is part of the manifest contract.

    The manifest declares its ``[entries]`` fields as required, and ``legacy`` is
    now one of them; a manifest that omits it violates its own contract.
    """
    root, payload, kb = make_project(tmp_path)
    write_manifest(
        kb, omit_legacy=True, active=("stack.md", "executive_summary.md")
    )
    code, report = run(root, payload)
    assert code == 1
    assert "missing the required field `legacy`" in reasons(report)


def test_a_manifest_with_a_legacy_list_is_valid(tmp_path):
    """The added list is admitted, and an empty one is the ordinary case."""
    root, payload, kb = make_project(tmp_path)
    write_manifest(
        kb,
        legacy=("stack.md",),
        active=("stack.md", "executive_summary.md"),
    )
    code, report = run(root, payload)
    assert code == 0, reasons(report)
    assert checker.ANOMALY not in signals(report, checker.MANIFEST_NAME)


def test_an_entry_with_no_contract_is_not_silently_approved(tmp_path):
    root, payload, kb = make_project(tmp_path)
    write_entry(kb, "uncontracted.md", tag="x")
    write_manifest(kb, active=("stack.md", "executive_summary.md", "uncontracted.md"))
    code, report = run(root, payload)
    assert checker.BOUNDARY in signals(report, "uncontracted.md")
    assert "human review, never" in reasons(report)


def test_the_checker_never_writes_to_the_project(tmp_path):
    root, payload, kb = make_project(tmp_path)
    before = {path: path.read_bytes() for path in sorted(root.rglob("*")) if path.is_file()}
    run(root, payload)
    after = {path: path.read_bytes() for path in sorted(root.rglob("*")) if path.is_file()}
    assert before == after


# --------------------------------------------------------------------------- #
# Determinism, exit-code contract and tool contract
# --------------------------------------------------------------------------- #


def test_the_report_is_deterministic(tmp_path):
    root, payload, kb = make_project(tmp_path, shape="library")
    write_entry(
        kb,
        "containers.md",
        tag="containers",
        sources=("compose.yml",),
        custom_sections=("Container Definitions",),
    )
    write_manifest(
        kb,
        shape="library",
        active=("stack.md", "executive_summary.md", "containers.md", "distribution.md"),
    )
    first = checker.render_json(run(root, payload)[1])
    second = checker.render_json(run(root, payload)[1])
    assert first == second
    order = [entry[0] for entry in run(root, payload)[1].per_target()]
    assert order == sorted(order)


def test_gap_does_not_change_the_exit_code_but_anomaly_does(tmp_path):
    """``GAP`` is advisory missing evidence; ``ANOMALY`` is a contradiction.

    The unresolvable ``source_files`` case that used to demonstrate ``GAP`` is a
    violation of D01 item 5 since RFC-79 decision 2 (the contract can express the
    absence/tree-fact class), so the remaining advisory case of this checker is the
    absent manifest: the knowledge base exists and is valid, but the evidence that
    indexes it does not.
    """
    root, payload, kb = make_project(tmp_path)
    write_entry(kb, "stack.md", tag="stack")
    (kb / checker.MANIFEST_NAME).unlink()
    code, report = run(root, payload)
    assert checker.GAP in signals(report), reasons(report)
    assert checker.ANOMALY not in signals(report), reasons(report)
    assert code == 0

    # A real contradiction now: the body heading no longer matches ``title``.
    path = kb / "stack.md"
    path.write_text(
        path.read_text(encoding="utf-8").replace("\n# Stack\n", "\n# Mismatch\n"),
        encoding="utf-8",
    )
    code, report = run(root, payload)
    assert checker.ANOMALY in signals(report), reasons(report)
    assert code == 1


def test_the_tool_is_stdlib_only():
    import testsupport

    testsupport.assert_tool_imports_only_stdlib(
        Path(__file__).resolve().parents[1] / "tools" / "check_discovery_output.py"
    )


def test_the_cli_returns_two_on_an_unreadable_payload(tmp_path, capsys):
    root, _, _ = make_project(tmp_path)
    missing_payload = tmp_path / "no-payload"
    code = checker.main(["--root", str(root), "--payload", str(missing_payload)])
    assert code == 2
    assert "discovery contracts directory not found" in capsys.readouterr().err


def test_the_cli_reports_valid_on_a_valid_project(tmp_path, capsys):
    root, payload, _ = make_project(tmp_path)
    code = checker.main(["--root", str(root), "--payload", str(payload)])
    assert code == 0
    output = capsys.readouterr().out
    assert "Discovery output check" in output
    assert "Summary:" in output
