"""Release-trigger contract: `publish-dist` is push-triggered, not tag-triggered.

The workflow, `docs/VERSIONING.md` and the root `AGENTS.md` must express one
interpretation: a push to `master` that modifies ``protocol/**`` publishes
``dist``; the release tag is created on the same promotion commit and does not
trigger the workflow. ``workflow_dispatch`` is a manual recovery trigger and
does not create a version or a tag.

These tests read the real workflow and the real policy on purpose; they are the
regression guard for F-11. See ``tests/AGENTS.md``.
"""

from __future__ import annotations

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
WORKFLOW = REPO_ROOT / ".github" / "workflows" / "publish-dist.yml"
VERSIONING = REPO_ROOT / "docs" / "VERSIONING.md"
ROOT_AGENTS = REPO_ROOT / "AGENTS.md"


def workflow_text() -> str:
    return WORKFLOW.read_text(encoding="utf-8")


def trigger_block() -> str:
    """The workflow's ``on:`` block, without the rest of the file."""
    text = workflow_text()
    after_on = text.split("\non:\n", 1)[1]
    return after_on.split("\npermissions:", 1)[0]


def test_publish_dist_triggers_on_a_push_to_master_that_changes_protocol():
    block = trigger_block()

    assert "push:" in block
    assert "branches: [master]" in block
    assert '- "protocol/**"' in block
    assert "tags:" not in block
    assert "workflow_dispatch:" in block


def test_workflow_declares_that_the_tag_does_not_trigger_it():
    normalized = " ".join(
        line.lstrip("# ").strip() for line in workflow_text().splitlines()
    )
    assert "push a `master` que modifique `protocol/**`" in normalized
    assert "El tag de release NO dispara este workflow" in normalized


def test_versioning_documents_the_push_trigger_only():
    text = VERSIONING.read_text(encoding="utf-8")

    assert "Corre en cada push a `master` que modifique `protocol/**`" in text
    assert "**el tag no dispara el workflow**" in text
    assert "Corre al taggear" not in text
    assert "`publish-dist` corre con el tag" not in text


def test_root_agents_documents_the_push_trigger():
    text = ROOT_AGENTS.read_text(encoding="utf-8")
    assert "on pushes that change" in text
    assert "`protocol/**`" in text
