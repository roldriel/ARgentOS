"""Lifecycle install tests: layout, collisions and bootstrap.

Plan 154 unit U4. Criteria: GATE 3 #1–#5, #16–#22, #24, #30.
"""

from __future__ import annotations

import json

import lifecycle as L
import lifecycle_contract as contract


def test_clean_install_layout_and_bootstrap(project, make_engine):
    """#1, #18, #19 — canonical layout, no second bootstrap, valid bootstrap."""
    result = make_engine(project).install()
    assert result.state == L.SUCCESS
    assert (project / "AGENTS.md").is_file()
    assert (project / ".argentos" / "features.toml").is_file()
    assert (project / ".argentos" / ".agents" / "INDEX.md").is_file()
    manifest = contract.load_manifest(project)
    assert manifest is not None
    assert (project / contract.MANIFEST_REL).is_file()
    assert (project / ".argentos" / ".backup").is_dir()
    # Single bootstrap: no AGENTS.md inside .argentos/.
    assert not (project / ".argentos" / "AGENTS.md").exists()
    # Adapter points to the real bootstrap.
    adapter = (project / "AGENTS.md").read_text(encoding="utf-8")
    assert ".argentos/.agents/INDEX.md" in adapter


def test_adapter_case_absent_is_generated(project, make_engine):
    """#2 (a) — no AGENTS.md ⇒ generated adapter recorded as installed."""
    result = make_engine(project).install()
    assert result.state == L.SUCCESS
    manifest = contract.load_manifest(project)
    generated = manifest["generated"]
    assert len(generated) == 1
    assert generated[0]["path"] == "AGENTS.md"
    assert generated[0]["kind"] == "adapter"
    assert generated[0]["origin"] == "installed"


def test_adapter_case_preexisting_is_preserved(project, make_engine):
    """#2 (b) — preexisting AGENTS.md ⇒ no-op + manual integration."""
    (project / "AGENTS.md").write_text("MINE\n", encoding="utf-8")
    result = make_engine(project).install()
    assert result.state == L.SUCCESS
    assert (project / "AGENTS.md").read_text(encoding="utf-8") == "MINE\n"
    assert contract.load_manifest(project)["generated"] == []
    assert "manual" in result.message.lower() or result.details.get("gitignore_modified") is False


def test_adapter_case_already_managed_is_noop(project, make_engine):
    """#2 (c) — already-managed adapter ⇒ idempotent no-op."""
    make_engine(project).install()
    before = (project / "AGENTS.md").read_text(encoding="utf-8")
    result = make_engine(project).install()
    assert result.state == L.NOOP
    assert (project / "AGENTS.md").read_text(encoding="utf-8") == before


def test_adapter_case_authorized_substitution(project, make_engine):
    """#2 (d) — explicit opt-in replaces with a verifiable backup."""
    (project / "AGENTS.md").write_text("OLD\n", encoding="utf-8")
    result = make_engine(project, replace_agents_md=True).install()
    assert result.state == L.SUCCESS
    manifest = contract.load_manifest(project)
    generated = manifest["generated"]
    assert generated and generated[0]["origin"] == "substituted-authorized"
    backups = manifest["backups"]
    assert backups and backups[0]["replaced"] == "AGENTS.md"
    backup_file = project / backups[0]["path"]
    assert backup_file.read_text(encoding="utf-8") == "OLD\n"


def test_adapter_case_change_between_inspection_and_operation(project, make_engine):
    """#2 (e) — later change blocks replacement (fail closed)."""
    (project / "AGENTS.md").write_text("OLD\n", encoding="utf-8")

    def mutate(name, engine):
        if name == "inventory":
            (project / "AGENTS.md").write_text("CHANGED MIDWAY\n", encoding="utf-8")

    result = make_engine(project, replace_agents_md=True, hook=mutate).install()
    assert result.state == L.CONFLICT
    assert (project / "AGENTS.md").read_text(encoding="utf-8") == "CHANGED MIDWAY\n"


def test_historical_agents_detected_and_preserved(project, make_engine):
    """#3 — historical ``.agents/`` is reported, never touched by default."""
    (project / ".agents").mkdir()
    (project / ".agents" / "legacy.txt").write_text("legacy\n", encoding="utf-8")
    result = make_engine(project).install()
    assert result.state == L.SUCCESS
    assert result.details["historical_agents_detected"] is True
    assert (project / ".agents" / "legacy.txt").read_text(encoding="utf-8") == "legacy\n"


def test_gitignore_never_modified(project, make_engine):
    """#4 — ``.gitignore`` is byte-identical after install."""
    (project / ".gitignore").write_text("node_modules\n", encoding="utf-8")
    result = make_engine(project).install()
    assert result.state == L.SUCCESS
    assert result.details["gitignore_modified"] is False
    assert (project / ".gitignore").read_text(encoding="utf-8") == "node_modules\n"


def test_unrecognized_argentos_stops(project, make_engine):
    """#5 — ``.argentos/`` without a manifest ⇒ STOP."""
    (project / ".argentos").mkdir()
    (project / ".argentos" / "something.txt").write_text("x\n", encoding="utf-8")
    result = make_engine(project).install()
    assert result.state == L.CONFLICT
    assert (project / ".argentos" / "something.txt").read_text(encoding="utf-8") == "x\n"


def test_reinstall_after_uninstall(project, make_engine):
    """#16 — reinstall over a previously uninstalled layout succeeds."""
    assert make_engine(project).install().state == L.SUCCESS
    assert make_engine(project).uninstall().state == L.SUCCESS
    assert contract.load_manifest(project)["install"]["managed"] is False
    assert make_engine(project).install().state == L.SUCCESS
    assert contract.load_manifest(project)["install"]["managed"] is True
    assert (project / ".argentos" / ".agents" / "INDEX.md").is_file()


def test_project_root_is_explicit(project, make_engine):
    """#20 — the operation targets the declared root (never inferred)."""
    result = make_engine(project).install()
    assert result.state == L.SUCCESS
    assert (project / contract.MANIFEST_REL).is_file()
    # No root ⇒ the contract refuses to invent one.
    import roots
    import pytest

    with pytest.raises(roots.RootResolutionError):
        roots.resolve(None)


def test_staging_isolation_is_enforced(project, make_engine, staging_parent):
    """#21 — staging (and the origin) cannot be the project."""
    inside = make_engine(project, payload_dir=project).install()
    assert inside.state == L.CONFLICT
    # A staging host inside the project is rejected too.
    nested = make_engine(project, staging_parent=project / "stage").install()
    assert nested.state == L.CONFLICT
    assert not (project / ".argentos").exists()


def test_config_seeded_once_and_not_overwritten(project, make_engine):
    """#22, #30 — a single active config, never overwritten once it exists."""
    assert make_engine(project).install().state == L.SUCCESS
    (project / contract.ACTIVE_CONFIG_REL).write_text("USER\n", encoding="utf-8")
    assert make_engine(project).uninstall().state == L.SUCCESS
    assert make_engine(project).install().state == L.SUCCESS
    assert (project / contract.ACTIVE_CONFIG_REL).read_text(encoding="utf-8") == "USER\n"
    # Exactly one active config; the payload copy is the inert template.
    assert (project / ".argentos" / "features.toml").is_file()
    manifest = contract.load_manifest(project)
    assert manifest["config"]["active_path"] == contract.ACTIVE_CONFIG_REL


def test_foreign_files_are_not_destroyed(project, make_engine):
    """#24 — unrelated adopter files stay intact."""
    (project / "src").mkdir()
    (project / "src" / "app.py").write_text("print('hi')\n", encoding="utf-8")
    make_engine(project).install()
    assert (project / "src" / "app.py").read_text(encoding="utf-8") == "print('hi')\n"


def test_git_checkout_staging(project, make_engine, tmp_path, staging_parent):
    """#17 — the git-checkout acquisition method is supported and recorded."""
    import subprocess

    repo = tmp_path / "repo"
    (repo / "protocol" / ".agents").mkdir(parents=True)
    (repo / "protocol" / ".agents" / "VERSION").write_text("12.0.0\n", encoding="utf-8")
    (repo / "protocol" / ".agents" / "INDEX.md").write_text("# i\n", encoding="utf-8")
    subprocess.run(["git", "init", "-q", str(repo)], check=True)
    subprocess.run(["git", "-C", str(repo), "add", "."], check=True)
    subprocess.run(
        ["git", "-C", str(repo), "-c", "user.email=a@b.c", "-c", "user.name=t",
         "commit", "-q", "-m", "payload"],
        check=True,
    )
    engine = L.LifecycleEngine(
        project, source_ref="HEAD", repo=repo, staging_parent=staging_parent
    )
    result = engine.install()
    assert result.state == L.SUCCESS
    manifest = json.loads((project / contract.MANIFEST_REL).read_text(encoding="utf-8"))
    assert manifest["install"]["method"] == "git-checkout"
    assert manifest["install"]["source"]["commit"]
