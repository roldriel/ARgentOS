"""Tests for tools/check_protocol_invariants.py.

Covers the three invariants (reference resolution, distribution boundary,
H13 taxonomy metadata) plus the false-positive controls (artifact names,
example paths, URLs, session placeholders, fenced code).
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
TOOL = REPO_ROOT / "tools" / "check_protocol_invariants.py"

import check_protocol_invariants as cpi  # noqa: E402
from testsupport import assert_tool_imports_only_stdlib  # noqa: E402


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


def test_docs_reference_is_a_boundary_violation(tmp_path):
    """A `docs/` reference from an ordinary payload file is rejected.

    `docs/` is source-repository governance: it is not published to adopters
    (only `.agents/` + the entry file ship), so a reference to it would be a
    broken link in the distributed copy.
    """
    make_repo(tmp_path, {
        ".agents/roles/sample.md": ROLE_OK,
        ".agents/skills/INDEX.md": "See `docs/plans/anything.md`.\n",
        "docs/plans/anything.md": "# Doc\n",
    })
    v = cpi.verify(tmp_path)
    assert any(x.code == "BOUNDARY" and "docs/plans" in x.message for x in v)


def test_docs_provenance_reference_is_accepted_for_allowlisted_file(tmp_path):
    """The allowlisted normative-source citation is accepted, and the checker
    reports no violation for it."""
    make_repo(tmp_path, {
        ".agents/contracts/CHANGE_GOVERNANCE.md": (
            "---\ntaxonomy: \".agents/standards/runtime/PROTOCOL_TAXONOMY.md\"\n"
            "kind: contract\ndomain: cross-cutting\n---\n\n"
            "# Contract: Change Governance Artifact\n\n"
            "Its normative source is "
            "`docs/rfc/76-change-governance-artifact.md` (RFC-76).\n"
        ),
        "docs/rfc/76-change-governance-artifact.md": "# RFC-76\n",
    })
    v = [x for x in cpi.verify(tmp_path) if "76-change-governance" in x.message]
    assert v == []


def test_docs_allowlist_does_not_authorize_other_docs_paths(tmp_path):
    """The exception is exact: a listed file may name ONLY its registered
    path, never `docs/` in general."""
    make_repo(tmp_path, {
        ".agents/contracts/CHANGE_GOVERNANCE.md": (
            "---\ntaxonomy: \".agents/standards/runtime/PROTOCOL_TAXONOMY.md\"\n"
            "kind: contract\ndomain: cross-cutting\n---\n\n"
            "# Contract: Change Governance Artifact\n\n"
            "Its normative source is "
            "`docs/rfc/76-change-governance-artifact.md` (RFC-76), and see "
            "`docs/rfc/77-something-else.md`.\n"
        ),
        "docs/rfc/76-change-governance-artifact.md": "# RFC-76\n",
        "docs/rfc/77-something-else.md": "# RFC-77\n",
    })
    v = cpi.verify(tmp_path)
    assert any(
        x.code == "BOUNDARY" and "77-something-else" in x.message for x in v
    ), "an unregistered docs/ path from an allowlisted file must still fail"


def test_docs_allowlist_does_not_apply_to_unlisted_file(tmp_path):
    """A non-allowlisted payload file cannot cite the registered provenance
    path: the exception is per citing file, not global."""
    make_repo(tmp_path, {
        ".agents/roles/sample.md": ROLE_OK,
        ".agents/skills/INDEX.md": (
            "See `docs/rfc/76-change-governance-artifact.md`.\n"
        ),
        "docs/rfc/76-change-governance-artifact.md": "# RFC-76\n",
    })
    v = cpi.verify(tmp_path)
    assert any(
        x.code == "BOUNDARY" and "76-change-governance" in x.message for x in v
    ), "only the citing file registered in the allowlist may use the exception"


def test_agents_md_reference_ok(tmp_path):
    make_repo(tmp_path, {
        ".agents/roles/sample.md": ROLE_OK + "\nSee `AGENTS.md`.\n",
        "AGENTS.md": "# AGENTS\n",
    })
    assert cpi.verify(tmp_path) == []


def test_entry_file_relative_link_ok(tmp_path):
    """The allowlisted entry links resolve to the adopter's root AGENTS.md.

    Four levels up from .agents/standards/<dir>/ reach project/AGENTS.md once
    .agents/ is materialized at .argentos/.agents/."""
    make_repo(tmp_path, {
        ".agents/roles/sample.md": ROLE_OK,
        ".agents/standards/conduct/OPERATIONAL_RULES.md": (
            "See [AGENTS.md](../../../../AGENTS.md).\n"
        ),
    })
    assert cpi.verify(tmp_path) == []


def test_entry_link_with_wrong_adopted_depth_is_rejected(tmp_path):
    """The pre-F-01 three-level link resolved to .argentos/AGENTS.md.

    That path must not exist, so the checker rejects the link instead of
    accepting any path that happens to resolve in the source tree."""
    make_repo(tmp_path, {
        ".agents/roles/sample.md": ROLE_OK,
        ".agents/standards/conduct/OPERATIONAL_RULES.md": (
            "See [AGENTS.md](../../../AGENTS.md).\n"
        ),
    })
    violations = cpi.verify(tmp_path)
    assert any(
        v.code == "BOUNDARY" and "adopter's root AGENTS.md" in v.message
        for v in violations
    ), violations


def test_dev_root_agents_md_not_scanned(tmp_path):
    """The dev root AGENTS.md is not a protocol document; its content must
    not be scanned or used as a reference target."""
    make_repo(tmp_path, {
        ".agents/roles/sample.md": ROLE_OK,
    })
    (tmp_path / "AGENTS.md").write_text(
        "Development entry: see `AGENTS.md`.\n", encoding="utf-8"
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


def test_tool_uses_only_stdlib():
    assert_tool_imports_only_stdlib(TOOL, {"check_protocol_invariants"})


# --- SKILLS invariant -------------------------------------------------------

SKILL_OK = (
    "---\nname: sample-skill\ndescription: Does sample things.\n"
    "when_to_activate: In tests.\n---\n\n# Mission\n\nRead `references/spec.md`.\n"
)


def make_skill_repo(tmp_path: Path, index_rows: str = "| sample-skill | x |") -> Path:
    return make_repo(tmp_path, {
        ".agents/skills/sample-skill/SKILL.md": SKILL_OK,
        ".agents/skills/sample-skill/references/spec.md": "# Spec\n",
        ".agents/skills/INDEX.md": (
            "# Skills\n\n## Skill inventory\n\n| Skill | Description |\n"
            "| --- | --- |\n" + index_rows + "\n"
        ),
    })


def test_skills_clean_repo_passes(tmp_path):
    make_skill_repo(tmp_path)
    assert not [v for v in cpi.verify(tmp_path) if v.code == "SKILLS"]


def test_skills_missing_skill_md_flagged(tmp_path):
    make_skill_repo(tmp_path)
    (tmp_path / "protocol/.agents/skills/sample-skill/SKILL.md").unlink()
    violations = cpi.verify(tmp_path)
    assert any(v.code == "SKILLS" and "missing SKILL.md" in v.message
               for v in violations)


def test_skills_name_mismatch_flagged(tmp_path):
    make_repo(tmp_path, {
        ".agents/skills/sample-skill/SKILL.md": SKILL_OK.replace(
            "name: sample-skill", "name: other-name"
        ),
        ".agents/skills/INDEX.md": "## Skill inventory\n\n| Skill | D |\n| sample-skill | x |\n",
    })
    violations = cpi.verify(tmp_path)
    assert any(v.code == "SKILLS" and "name does not match" in v.message
               for v in violations)


def test_skills_broken_reference_flagged(tmp_path):
    make_repo(tmp_path, {
        ".agents/skills/sample-skill/SKILL.md": SKILL_OK,
        ".agents/skills/INDEX.md": "## Skill inventory\n\n| Skill | D |\n| sample-skill | x |\n",
    })
    violations = cpi.verify(tmp_path)
    assert any(v.code == "SKILLS" and "references/spec.md" in v.message
               for v in violations)


def test_skills_index_desync_flagged(tmp_path):
    make_skill_repo(tmp_path, index_rows="| ghost-skill | x |")
    violations = cpi.verify(tmp_path)
    messages = [v.message for v in violations if v.code == "SKILLS"]
    assert any("not listed" in m for m in messages)
    assert any("without skill directory" in m for m in messages)


# --- Source-layout inventory cross-check --------------------------------------


def test_allowlisted_entry_links_pass(tmp_path):
    """The two documented files may carry the adopted entry link."""
    make_repo(tmp_path, {
        ".agents/standards/conduct/OPERATIONAL_RULES.md": (
            "| entry | [AGENTS.md](../../../../AGENTS.md) |\n"
        ),
        ".agents/standards/quality/PREFLIGHT_CHECKLIST.md": (
            "- [ ] read [AGENTS.md](../../../../AGENTS.md)\n"
        ),
        "AGENTS.md": "# Entry\n",
    })
    assert cpi.verify(tmp_path) == []


def test_third_entry_link_is_a_violation(tmp_path):
    """A path-link to AGENTS.md from any other payload file is flagged."""
    make_repo(tmp_path, {
        ".agents/standards/conduct/OPERATIONAL_RULES.md": (
            "| entry | [AGENTS.md](../../../../AGENTS.md) |\n"
        ),
        ".agents/standards/runtime/OTHER.md": (
            "See [AGENTS.md](../../../../AGENTS.md) now.\n"
        ),
        "AGENTS.md": "# Entry\n",
    })
    violations = cpi.verify(tmp_path)
    assert any(
        v.code == "BOUNDARY" and "allowlist" in v.message for v in violations
    )
    assert any("OTHER.md" in v.source.as_posix() for v in violations)


def test_bare_prose_entry_mention_is_allowed(tmp_path):
    """Prose mentions of AGENTS.md (no path separator) are not links."""
    make_repo(tmp_path, {
        ".agents/INDEX.md": (
            "The entry point is `AGENTS.md` at the project root.\n"
        ),
        "AGENTS.md": "# Entry\n",
    })
    assert cpi.verify(tmp_path) == []


def test_source_layout_documents_entry_links():
    """docs/source-layout.md must document the two adopted entry links and
    their depth so an agent does not regress them (allowlist == inventory)."""
    doc = (REPO_ROOT / "docs" / "source-layout.md").read_text(
        encoding="utf-8"
    )
    assert (
        "protocol/.agents/standards/conduct/OPERATIONAL_RULES.md" in doc
    )
    assert (
        "protocol/.agents/standards/quality/PREFLIGHT_CHECKLIST.md" in doc
    )
    assert "../../../../AGENTS.md" in doc
