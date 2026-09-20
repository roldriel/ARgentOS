"""Dogfood: the D01 mechanical checker against the real repository (plan 136).

This module is an **anchored test** in the sense of ``tests/AGENTS.md``: it reads
the live working tree and the real payload on purpose, and only reads them. A
synthetic payload cannot express what it protects — that the checker's contract
resolution still works against the **real** discovery contracts, which are the
single source of the requirements (D01 item 12; plan 47/RFC-48).

Its stability contract is the documented one: it may name canonical paths and
artifact names of the real repository, so it is updated when that canonical state
legitimately changes. It is not portable and is not meant to be.

Nothing here mutates repository state.
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))

import check_discovery_output as checker  # noqa: E402

REPO_ROOT = Path(__file__).resolve().parents[1]
TOOL = REPO_ROOT / "tools" / "check_discovery_output.py"
PAYLOAD = REPO_ROOT / "protocol" / ".agents"


def _run(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(TOOL), *args],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
    )


# --------------------------------------------------------------------------- #
# The tool over the real repository
# --------------------------------------------------------------------------- #


def test_the_real_repository_has_no_knowledge_base_and_that_is_not_a_failure():
    """The DEV repository is not a discovery target: absence is declared, exit 0."""
    result = _run("--root", ".")
    assert result.returncode == 0, result.stdout + result.stderr
    assert "N/A" in result.stdout
    assert "declared absence" in result.stdout


def test_the_json_report_is_machine_readable_on_the_real_repository():
    import json

    result = _run("--root", ".", "--json")
    assert result.returncode == 0
    payload = json.loads(result.stdout)
    assert payload["tool"] == "check_discovery_output"
    assert payload["plan"] == 136
    assert payload["counts"]["ANOMALY"] == 0


def test_a_contract_directory_that_does_not_exist_is_a_read_error_not_a_pass(tmp_path):
    """An unreadable payload is exit 2: never a claim about content."""
    result = _run("--root", str(REPO_ROOT), "--payload", str(tmp_path / "absent"))
    assert result.returncode == 2
    assert "discovery contracts directory not found" in result.stderr


# --------------------------------------------------------------------------- #
# Contract resolution against the real payload
# --------------------------------------------------------------------------- #


def test_every_per_entry_contract_declares_its_runtime_path():
    """Each entry contract names the KB file it governs; nothing is guessed.

    This is what removes a hardcoded contract->artifact table from the checker:
    the naive lowercasing of a contract filename would map
    ``ENVIRONMENT_DISCOVERY`` to ``environment_discovery.md`` instead of the real
    ``environment.md``, and ``API_SURFACE`` to ``api_surface.md`` instead of
    ``api.md``.
    """
    contracts = checker.load_contracts(PAYLOAD, "protocol/.agents")
    assert contracts, "no discovery entry contracts resolved"
    for name, contract in contracts.items():
        assert name == contract.runtime_name
        assert name.endswith(".md"), name
        assert contract.source.startswith("protocol/.agents/"), contract.source
    # The two cases a naive rule would get wrong.
    assert "environment.md" in contracts
    assert "api.md" in contracts
    assert "environment_discovery.md" not in contracts
    assert "api_surface.md" not in contracts


def test_the_environment_contract_is_the_only_probe_admitting_one():
    contracts = checker.load_contracts(PAYLOAD)
    probe = sorted(n for n, c in contracts.items() if c.is_environment)
    assert probe == ["environment.md"], probe


def test_required_sections_are_resolved_from_the_real_contracts():
    contracts = checker.load_contracts(PAYLOAD)
    # A contract that declares extra sections beyond the base ones.
    architecture = contracts["architecture.md"]
    for section in ("Module Responsibilities", "Strong Couplings", "Security"):
        assert section in architecture.required_sections, architecture.required_sections
    # The executive summary declares its sections as backticked prose, and the
    # ``## Project Shape`` requirement must be resolved from there.
    summary = contracts["executive_summary.md"]
    assert "Project Shape" in summary.required_sections, summary.required_sections
    assert summary.required_sections[0] == "Project Shape"


def test_the_base_contract_sections_are_resolved():
    base = checker.load_base_required_sections(PAYLOAD)
    assert "Discovered Facts" in base
    assert "Summary" in base
    # No duplicate and no leftover ``##`` prefix.
    assert len(set(base)) == len(base)
    assert all(not name.startswith("#") for name in base)


def test_the_manifest_contract_yields_its_required_tables_and_fields():
    tables = dict(checker.load_manifest_required_sections(PAYLOAD))
    assert set(tables) >= {"knowledge_base", "hashes", "entries", "workers"}
    assert "project_shape" in tables["knowledge_base"]
    assert "active" in tables["entries"]
    assert "stale" in tables["entries"]
    # ``[runtime]`` is declared optional by the contract and must not be required.
    assert "model_used" in tables.get("runtime", ())


def test_the_project_shape_enum_matches_the_manifest_contract():
    """The six admitted shapes are the contract's, not an invention of the tool."""
    text = (PAYLOAD / checker.CONTRACTS_DIR / checker.MANIFEST_CONTRACT).read_text(
        encoding="utf-8"
    )
    for shape in sorted(checker.PROJECT_SHAPES):
        assert shape in text, shape


def test_distribution_is_mandatory_for_the_shapes_the_contract_names():
    text = (
        PAYLOAD / checker.CONTRACTS_DIR / "DISTRIBUTION.md"
    ).read_text(encoding="utf-8")
    assert "library" in text
    assert "cli" in text
    assert checker.DISTRIBUTION_SHAPES == frozenset({"library", "cli"})


# --------------------------------------------------------------------------- #
# The declared frontier
# --------------------------------------------------------------------------- #


def test_the_tool_targets_only_the_mechanical_subset():
    """The judgement items are named as out of scope in the tool itself.

    A reader and a future maintainer must be able to see, in the shipped source,
    which D01 items this tool does **not** perform, so the boundary cannot be
    mistaken for an approval.
    """
    source = TOOL.read_text(encoding="utf-8")
    assert "What it deliberately does **not** do" in source
    assert "F-17" in source
    assert "F-16" in source
    assert "never** ``ANOMALY``" in source


def test_the_real_payload_is_never_written(tmp_path):
    """Running the checker over the real repository changes nothing in it."""
    before = _payload_digest()
    _run("--root", ".")
    assert _payload_digest() == before


def _payload_digest() -> str:
    import hashlib

    digest = hashlib.sha256()
    for path in sorted(PAYLOAD.rglob("*")):
        if path.is_file():
            digest.update(path.relative_to(PAYLOAD).as_posix().encode("utf-8"))
            digest.update(path.read_bytes())
    return digest.hexdigest()
