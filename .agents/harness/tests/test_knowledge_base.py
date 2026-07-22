"""Tests for the Knowledge Base and Context Engineering standard."""

from __future__ import annotations

import re
from pathlib import Path

import pytest

PROJECT_ROOT = Path(__file__).resolve().parents[3]


def test_context_standard_exists():
    path = PROJECT_ROOT / ".agents" / "standards" / "context" / "CONTEXT.md"
    assert path.is_file()
    content = path.read_text(encoding="utf-8")
    assert "Priority of information" in content
    assert "8000" in content
    assert "4000" in content


def test_knowledge_directory_structure_exists():
    assert (PROJECT_ROOT / ".project" / "knowledge" / "INDEX.md").is_file()
    assert (PROJECT_ROOT / ".project" / "knowledge" / "entries").is_dir()
    assert (PROJECT_ROOT / ".project" / "knowledge" / "discovery").is_dir()


def test_knowledge_entry_has_required_front_matter():
    entries = list((PROJECT_ROOT / ".project" / "knowledge" / "entries").glob("*.md"))
    if not entries:
        pytest.skip("No KB entries to validate")
    for entry in entries:
        content = entry.read_text(encoding="utf-8")
        assert "+++" in content
        for field in ("session_uuid", "objective", "tags", "files_modified", "outcome"):
            assert field in content, f"Missing {field} in {entry.name}"


def test_knowledge_entry_has_lessons_learned():
    entries = list((PROJECT_ROOT / ".project" / "knowledge" / "entries").glob("*.md"))
    if not entries:
        pytest.skip("No KB entries to validate")
    for entry in entries:
        content = entry.read_text(encoding="utf-8")
        assert (
            "## Lessons learned" in content
        ), f"Missing lessons learned in {entry.name}"


def test_context_discoverer_role_exists():
    path = PROJECT_ROOT / ".agents" / "roles" / "context_discoverer.md"
    assert path.is_file()
    content = path.read_text(encoding="utf-8")
    assert "KB_DISCOVERY_REPORT.md" in content


def test_kb_discovery_contract_exists():
    path = (
        PROJECT_ROOT
        / ".agents"
        / "orchestrators"
        / "discovery"
        / "contracts"
        / "KB_DISCOVERY_REPORT.md"
    )
    assert path.is_file()
    content = path.read_text(encoding="utf-8")
    assert "recommended_entries" in content
    assert "context_budget_recommendation" in content


def test_session_log_contract_exists():
    path = PROJECT_ROOT / ".agents" / "contracts" / "SESSION_LOG.md"
    assert path.is_file()
    content = path.read_text(encoding="utf-8")
    assert "SESSION_LOG.md" in content
    assert "feature flags" in content.lower()


def test_delegation_contract_includes_kb_fields():
    path = PROJECT_ROOT / ".agents" / "delegation" / "WORKER_DELEGATION_CONTRACT.md"
    content = path.read_text(encoding="utf-8")
    assert "knowledge_entries" in content
    assert "context_budget" in content


def test_indexer_documented_not_implemented():
    index = PROJECT_ROOT / ".project" / "knowledge" / "INDEX.md"
    content = index.read_text(encoding="utf-8")
    assert "indexer" in content.lower()
    assert "not implemented" in content.lower()
    assert not (PROJECT_ROOT / ".project" / "knowledge" / "indexer.py").exists()


def test_worker_doc_distinguishes_context_roles():
    path = PROJECT_ROOT / ".agents" / "roles" / "worker.md"
    content = path.read_text(encoding="utf-8")
    assert "context_gatherer" in content
    assert "context_discoverer" in content
    assert "does not access the Knowledge Base" in content
