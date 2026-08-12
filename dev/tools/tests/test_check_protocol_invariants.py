"""Tests for dev/tools/check_protocol_invariants.py.

Covers the three invariants (reference resolution, distribution boundary,
H13 taxonomy metadata) plus the false-positive controls (artifact names,
example paths, URLs, session placeholders, fenced code).
"""

from __future__ import annotations

import ast
import subprocess
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[3]
TOOL = REPO_ROOT / "dev" / "tools" / "check_protocol_invariants.py"

sys.path.insert(0, str(REPO_ROOT / "dev" / "tools"))

import check_protocol_invariants as cpi  # noqa: E402


def make_repo(tmp_path: Path, files: dict[str, str]) -> Path:
    """Create a fake repo with the given files under the protocol/ payload.

    Keys use the legacy root layout (".agents/...", "AGENTS.md") and are
    translated to the source-containment layout ("protocol/.agents/...",
    "protocol/_AGENTS.md").
    """
    for rel, content in files.items():
        if rel == "AGENTS.md":
            rel = "protocol/_AGENTS.md"
        elif rel.startswith(".agents/"):
            rel = "protocol/" + rel
        p = tmp_path / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(content, encoding="utf-8")
    taxonomy = (
        tmp_path / "protocol" / ".agents" / "standards" / "runtime"
        / "PROTOCOL_TAXONOMY.md"
    )
    if not taxonomy.exists():
        taxonomy.parent.mkdir(parents=True, exist_ok=True)
        taxonomy.write_text("# Protocol Taxonomy\n", encoding="utf-8")
    return tmp_path


ROLE_OK = (
    '---\ntaxonomy: ".agents/standards/runtime/PROTOCOL_TAXONOMY.md"\n'
    "kind: role\ndomain: core\nrole_id: sample\n---\n\n# Role: Sample\n"
)


# --- Reference resolution ---------------------------------------------------


def test_clean_repo_passes(tmp_path):
    make_repo(tmp_path, {
        ".agents/roles/sample.md": ROLE_OK,
        ".agents/harness/INDEX.md": (
            "See `orchestrators/core/roles/orchestrator.md`.\n"
        ),
        ".agents/orchestrators/core/roles/orchestrator.md": ROLE_OK,
        ".agents/INDEX.md": "# Index\n",
        "AGENTS.md": "See `.agents/INDEX.md`.\n",
    })
    assert cpi.verify(tmp_path) == []


def test_missing_reference_reported(tmp_path):
    make_repo(tmp_path, {
        ".agents/roles/sample.md": ROLE_OK,
        ".agents/harness/INDEX.md": "Run `.agents/harness/runner.py`.\n",
    })
    codes = {v.code for v in cpi.verify(tmp_path)}
    assert "MISSING" in codes


def test_reference_resolves_relative_to_agents_root(tmp_path):
    make_repo(tmp_path, {
        ".agents/roles/sample.md": ROLE_OK,
        ".agents/harness/INDEX.md": (
            "See `standards/runtime/PROTOCOL_TAXONOMY.md`.\n"
        ),
        ".agents/standards/runtime/PROTOCOL_TAXONOMY.md": "# Taxonomy\n",
    })
    assert cpi.verify(tmp_path) == []


def test_fenced_code_ignored(tmp_path):
    make_repo(tmp_path, {
        ".agents/roles/sample.md": ROLE_OK,
        ".agents/harness/INDEX.md": "```\n.agents/harness/runner.py\n```\n",
    })
    assert cpi.verify(tmp_path) == []


# --- Distribution boundary ---------------------------------------------------


def test_boundary_violation_reported(tmp_path):
    make_repo(tmp_path, {
        ".agents/roles/sample.md": ROLE_OK,
        ".agents/skills/INDEX.md": "See `plans/rfc/24-skill-lifecycle-model.md`.\n",
        "plans/rfc/24-skill-lifecycle-model.md": "# RFC\n",
    })
    v = cpi.verify(tmp_path)
    assert any(
        x.code == "BOUNDARY" and "plans/rfc/24" in x.message for x in v
    )


def test_agents_md_reference_ok(tmp_path):
    make_repo(tmp_path, {
        ".agents/roles/sample.md": ROLE_OK + "\nSee `AGENTS.md`.\n",
        "AGENTS.md": "# AGENTS\n",
    })
    assert cpi.verify(tmp_path) == []


def test_entry_file_relative_link_ok(tmp_path):
    """The intentionally broken source links (../../../AGENTS.md) map to the
    payload entry file and are valid — they are correct in the dist layout."""
    make_repo(tmp_path, {
        ".agents/roles/sample.md": ROLE_OK,
        ".agents/standards/conduct/OPERATIONAL_RULES.md": (
            "See [AGENTS.md](../../../AGENTS.md).\n"
        ),
    })
    assert cpi.verify(tmp_path) == []


def test_dev_root_agents_md_not_scanned(tmp_path):
    """The dev root AGENTS.md is not a protocol document; its content must
    not be scanned or used as a reference target."""
    make_repo(tmp_path, {
        ".agents/roles/sample.md": ROLE_OK,
    })
    (tmp_path / "AGENTS.md").write_text(
        "Development entry: see `dev/README.md`.\n", encoding="utf-8"
    )
    assert cpi.verify(tmp_path) == []


def test_project_placeholders_ignored(tmp_path):
    make_repo(tmp_path, {
        ".agents/roles/sample.md": ROLE_OK,
        ".agents/standards/runtime/PROTOCOL_HEALTH.md": (
            "Path: `.project/<session-uuid>/<iteration>/state.json`.\n"
        ),
    })
    assert cpi.verify(tmp_path) == []


# --- Taxonomy metadata --------------------------------------------------------


def test_metadata_missing_reported(tmp_path):
    make_repo(tmp_path, {".agents/roles/executor.md": "# Role: Executor\n"})
    v = cpi.verify(tmp_path)
    assert any(
        x.code == "METADATA"
        and x.source == Path(".agents/roles/executor.md")
        for x in v
    )


def test_metadata_after_toml_block_ok(tmp_path):
    make_repo(tmp_path, {
        ".agents/contracts/EXAMPLE.md": (
            '+++\nartifact = "EXAMPLE.md"\nphase = "x"\nproduced_by = "y"\n+++\n\n'
            '---\ntaxonomy: ".agents/standards/runtime/PROTOCOL_TAXONOMY.md"\n'
            "kind: contract\ndomain: cross-cutting\n---\n\n# Contract\n"
        ),
    })
    assert cpi.verify(tmp_path) == []


def test_metadata_out_of_scope_ignored(tmp_path):
    make_repo(tmp_path, {".agents/skills/INDEX.md": "# Skills Index\n"})
    assert cpi.verify(tmp_path) == []


# --- False-positive controls --------------------------------------------------


def test_artifact_names_ignored(tmp_path):
    make_repo(tmp_path, {
        ".agents/roles/sample.md": ROLE_OK,
        ".agents/standards/runtime/PROTOCOL_HEALTH.md": (
            "See `TASK_SPECIFICATION.md` and `state.json`.\n"
        ),
    })
    assert cpi.verify(tmp_path) == []


def test_example_paths_ignored(tmp_path):
    make_repo(tmp_path, {
        ".agents/roles/sample.md": ROLE_OK,
        ".agents/standards/runtime/EXTERNAL_DEPENDENCIES.md": (
            "e.g. `app/services/user_service.py`, `payment_service.py`\n"
        ),
    })
    assert cpi.verify(tmp_path) == []


def test_urls_ignored(tmp_path):
    make_repo(tmp_path, {
        ".agents/roles/sample.md": ROLE_OK,
        ".agents/standards/runtime/EXTERNAL_DEPENDENCIES.md": (
            "See https://example.com/docs and <mailto:a@b.c>.\n"
        ),
    })
    assert cpi.verify(tmp_path) == []


# --- CLI -----------------------------------------------------------------------


def test_exit_codes_and_report(tmp_path):
    ok = make_repo(tmp_path / "ok", {".agents/roles/sample.md": ROLE_OK})
    res = subprocess.run(
        [sys.executable, str(TOOL), "--root", str(ok)],
        capture_output=True,
        text=True,
    )
    assert res.returncode == 0
    assert "invariants OK" in res.stdout

    bad = make_repo(tmp_path / "bad", {
        ".agents/roles/sample.md": ROLE_OK,
        ".agents/skills/INDEX.md": "See `plans/rfc/1.md`.\n",
        "plans/rfc/1.md": "# RFC\n",
    })
    res2 = subprocess.run(
        [sys.executable, str(TOOL), "--root", str(bad)],
        capture_output=True,
        text=True,
    )
    assert res2.returncode == 1
    assert "BOUNDARY" in res2.stdout
    assert "plans/rfc/1.md" in res2.stdout


# --- stdlib only ----------------------------------------------------------------


_STDLIB = set(sys.stdlib_module_names)


def test_tool_uses_only_stdlib():
    tree = ast.parse(TOOL.read_text(encoding="utf-8"))
    imported = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            imported.update(a.name.split(".")[0] for a in node.names)
        elif isinstance(node, ast.ImportFrom) and node.level == 0 and node.module:
            imported.add(node.module.split(".")[0])
    third_party = imported - _STDLIB - {"check_protocol_invariants"}
    assert third_party == set(), f"third-party imports: {third_party}"


# --- Source-layout inventory cross-check --------------------------------------


def test_source_layout_documents_intentionally_broken_links():
    """dev/source-layout.md must document the two intentionally broken source
    links so an agent knows not to fix them (allowlist == inventory)."""
    doc = (REPO_ROOT / "dev" / "source-layout.md").read_text(
        encoding="utf-8"
    )
    assert (
        "protocol/.agents/standards/conduct/OPERATIONAL_RULES.md" in doc
    )
    assert (
        "protocol/.agents/standards/quality/PREFLIGHT_CHECKLIST.md" in doc
    )
    assert "../../../AGENTS.md" in doc
