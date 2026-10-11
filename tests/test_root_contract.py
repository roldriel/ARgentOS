"""Bootstrap model of the adopted layout (GATE 1/2, Test G).

The effective bootstrap of an adopting project is exactly::

    project/AGENTS.md
        -> project/.argentos/.agents/INDEX.md
        -> the rest of the protocol

``project/.argentos/AGENTS.md`` is not part of the layout and no component may
depend on it. The adapter at the project root is a generated file; this test
proves the model against the payload source and the shared root contract.
"""

from __future__ import annotations

import shutil
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
PAYLOAD = REPO_ROOT / "protocol" / ".agents"
#: The payload entry file; `dist` publishes it as `AGENTS.md` at the project root.
ENTRY_SOURCE = REPO_ROOT / "protocol" / "_AGENTS.md"

sys.path.insert(0, str(PAYLOAD / "harness"))
import roots  # noqa: E402


def test_entry_file_is_a_pointer_to_the_payload_index():
    """The root `AGENTS.md` delegates to the payload bootstrap, not a copy of it."""
    text = ENTRY_SOURCE.read_text(encoding="utf-8")

    assert ".agents/INDEX.md" in text
    assert ".argentos/AGENTS.md" not in text


def test_adapter_chain_resolves_without_argentos_agents_md(tmp_path: Path):
    """`project/AGENTS.md` -> `.argentos/.agents/INDEX.md`, with no second entry."""
    project = tmp_path / "adopted"
    payload = project / ".argentos" / ".agents"
    payload.mkdir(parents=True)
    shutil.copy(ENTRY_SOURCE, project / "AGENTS.md")  # the adapter
    shutil.copy(PAYLOAD / "INDEX.md", payload / "INDEX.md")  # the bootstrap

    resolved = roots.resolve(project)
    bootstrap = resolved.resolve_reference(".agents/INDEX.md")

    assert bootstrap == payload / "INDEX.md"
    assert bootstrap.is_file()
    assert not (project / ".argentos" / "AGENTS.md").exists()


def test_no_payload_file_depends_on_argentos_agents_md():
    """No component references the entry point that must not exist."""
    forbidden = ".argentos/AGENTS.md"
    offenders = [
        str(path.relative_to(REPO_ROOT))
        for path in PAYLOAD.rglob("*")
        if path.is_file()
        and path.suffix in (".md", ".py", ".toml")
        and forbidden in path.read_text(encoding="utf-8", errors="replace")
    ]
    assert offenders == []


# ── GATE_2 remediation F1: a single active features.toml source


def test_payload_features_file_is_declared_inert_template():
    """F1 — the payload copy is inert data, never active configuration."""
    payload_file = PAYLOAD / "features.toml"
    assert payload_file.is_file()
    text = payload_file.read_text(encoding="utf-8")
    assert "NOT ACTIVE CONFIGURATION" in text
    assert "ARGENTOS_ROOT/features.toml" in text


def test_no_payload_document_declares_the_payload_as_configuration():
    """F1 — no operative instruction points the config at the payload copy."""
    offenders = [
        str(path.relative_to(REPO_ROOT))
        for path in PAYLOAD.rglob("*.md")
        if ".agents/features.toml" in path.read_text(encoding="utf-8")
    ]
    assert offenders == []


def test_no_payload_module_reads_the_payload_as_configuration():
    offenders = [
        str(path.relative_to(REPO_ROOT))
        for path in PAYLOAD.rglob("*.py")
        if ".agents/features.toml" in path.read_text(encoding="utf-8")
    ]
    assert offenders == []


def test_argentos_root_features_is_the_declared_configuration(tmp_path: Path):
    """F1 — the anchor distinguishes the active config from the payload."""
    resolved = roots.resolve(tmp_path / "proj")

    assert resolved.features_file == (
        tmp_path / "proj" / ".argentos" / "features.toml"
    ).resolve()
    assert (
        resolved.resolve_reference(".agents/features.toml")
        == resolved.payload_root / "features.toml"
    )


def test_adoption_docs_point_configuration_at_argentos_root():
    for name in ("ADOPTION.md", "MIGRATION.md"):
        text = (REPO_ROOT / "docs" / name).read_text(encoding="utf-8")
        assert ".argentos/features.toml" in text, name
        assert ".agents/features.toml" not in text, name


# ── GATE_2 remediation F4: DEV-only tooling stays out of the payload


def test_dev_tools_are_not_installed_into_the_payload():
    assert not (PAYLOAD / "tools").exists()
    for dev_only in (
        "scoped_content_identity.py",
        "determine_execution_state.py",
        "check_ears_coverage.py",
    ):
        assert not (PAYLOAD / "harness" / dev_only).exists()
        assert (REPO_ROOT / "tools" / dev_only).is_file()


def test_no_reference_to_the_false_payload_tools_path():
    # Assembled so this guard does not match its own source text.
    needle = "protocol/.agents/" + "tools"
    suffixes = (".md", ".py", ".toml", ".json", ".yml", ".yaml")
    offenders = []
    for base in ("protocol", "tools", "tests", "docs", "runtime", ".agents"):
        for path in (REPO_ROOT / base).rglob("*"):
            if not path.is_file() or path.suffix not in suffixes:
                continue
            if needle in path.read_text(encoding="utf-8", errors="replace"):
                offenders.append(str(path.relative_to(REPO_ROOT)))
    assert offenders == []
