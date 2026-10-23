"""Repository-anchored check of the adoption layout contract (F-01).

The manual adoption procedure and the lifecycle must produce the same layout:
the payload is materialized under ``.argentos/.agents/`` and the project root
carries a **non-normative adapter** whose only bootstrap target is
``.argentos/.agents/INDEX.md``. The payload entry (``protocol/_AGENTS.md``,
published by ``dist`` as ``AGENTS.md``) is *not* that adapter: its
``.agents/...`` references are anchored to the payload root.

These tests read the real payload and the canonical adoption guide on purpose.
They are the dogfood of the contract; see ``tests/AGENTS.md``.
"""

from __future__ import annotations

import re
import shutil
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
ENTRY_SOURCE = REPO_ROOT / "protocol" / "_AGENTS.md"
PAYLOAD = REPO_ROOT / "protocol" / ".agents"
ADOPTION = REPO_ROOT / "docs" / "ADOPTION.md"
LIFECYCLE = PAYLOAD / "harness" / "lifecycle.py"

#: The payload-relative references written in the published entry point.
_ENTRY_REF_RE = re.compile(r"`\.agents/([^`]+?)`")
#: Markdown inline links; used to find every payload reference to AGENTS.md.
_MD_LINK_RE = re.compile(r"\[[^\]]*\]\(([^)]+)\)")
#: The documented manual adapter, delimited by its own marker.
_ADAPTER_BLOCK_RE = re.compile(
    r"<!-- canonical-adapter -->\s*```markdown\n(.*?)```", re.DOTALL
)
_BOOTSTRAP = ".argentos/.agents/INDEX.md"

#: The two payload files allowed to carry a path-link to the root adapter.
ENTRY_LINK_FILES = (
    PAYLOAD / "standards" / "conduct" / "OPERATIONAL_RULES.md",
    PAYLOAD / "standards" / "quality" / "PREFLIGHT_CHECKLIST.md",
)


def canonical_adapter() -> str:
    """Return the adapter content the manual procedure installs."""
    match = _ADAPTER_BLOCK_RE.search(ADOPTION.read_text(encoding="utf-8"))
    assert match is not None, (
        "docs/ADOPTION.md must publish the manual adapter in a "
        "<!-- canonical-adapter --> fenced markdown block"
    )
    return match.group(1)


def test_payload_entry_references_resolve_in_the_payload_tree():
    """Every concrete `.agents/...` reference of the entry exists in the payload."""
    text = ENTRY_SOURCE.read_text(encoding="utf-8")
    references = {
        ref for ref in _ENTRY_REF_RE.findall(text) if "*" not in ref
    }
    assert ".agents/INDEX.md" in text
    missing = sorted(ref for ref in references if not (PAYLOAD / ref).is_file())
    assert missing == [], f"payload entry cites missing payload paths: {missing}"


def test_payload_entry_is_not_the_root_adapter():
    """The entry is payload-relative; the root adapter is a separate artifact."""
    entry = ENTRY_SOURCE.read_text(encoding="utf-8")
    adapter = canonical_adapter()

    assert ".agents/INDEX.md" in entry
    assert ".argentos/.agents/INDEX.md" not in entry
    assert _BOOTSTRAP in adapter
    assert ".agents/INDEX.md" not in adapter.replace(_BOOTSTRAP, "")


def test_manual_adapter_targets_the_canonical_bootstrap(tmp_path: Path):
    """The documented adapter resolves inside the canonical adopted layout."""
    project = tmp_path / "adopted"
    payload = project / ".argentos" / ".agents"
    payload.mkdir(parents=True)
    (payload / "INDEX.md").write_text("# bootstrap\n", encoding="utf-8")
    (project / "AGENTS.md").write_text(canonical_adapter(), encoding="utf-8")

    bootstrap = project / _BOOTSTRAP
    assert bootstrap.is_file()
    assert not (project / ".agents").exists()
    assert not (project / ".argentos" / "AGENTS.md").exists()


def test_manual_procedure_does_not_install_the_payload_entry_as_adapter():
    """The dist AGENTS.md is the payload entry, never the root adapter."""
    text = ADOPTION.read_text(encoding="utf-8")

    assert "`AGENTS.md` (raíz de `dist`) | `<proyecto>/AGENTS.md`" not in text
    assert "Adapter de §1.3.1.1 (no el `AGENTS.md` de `dist`)" in text
    assert "es el **entry del payload**" in text.replace("\n", " ")


def test_lifecycle_generates_the_same_bootstrap_target():
    """The manual adapter and the generated adapter declare one bootstrap."""
    source = LIFECYCLE.read_text(encoding="utf-8")
    assert _BOOTSTRAP in source
    assert canonical_adapter().count(_BOOTSTRAP) == 1


def agents_md_links(root: Path):
    """Yield ``(source, target)`` for every Markdown link to AGENTS.md under root."""
    for source in sorted(root.rglob("*.md")):
        text = source.read_text(encoding="utf-8", errors="replace")
        for match in _MD_LINK_RE.finditer(text):
            target = match.group(1).strip()
            if target.startswith(("#", "/")) or "://" in target:
                continue
            path_part = target.split("#", 1)[0]
            if Path(path_part).name == "AGENTS.md":
                yield source, target


def test_known_entry_links_use_the_adopted_depth():
    """The two allowlisted links reach project/AGENTS.md, not .argentos/AGENTS.md."""
    for source in ENTRY_LINK_FILES:
        text = source.read_text(encoding="utf-8")
        targets = [m.group(1).strip() for m in _MD_LINK_RE.finditer(text)]
        assert targets.count("../../../../AGENTS.md") >= 1, source
        assert "../../../AGENTS.md" not in targets, source


def test_payload_agents_md_links_resolve_to_the_adopters_root(tmp_path: Path):
    """Simulate dist/.agents/ -> project/.argentos/.agents/ and resolve every link."""
    project = tmp_path / "adopted"
    adopted_payload = project / ".argentos" / ".agents"
    adopted_payload.parent.mkdir(parents=True)
    shutil.copytree(PAYLOAD, adopted_payload)
    (project / "AGENTS.md").write_text(canonical_adapter(), encoding="utf-8")

    links = list(agents_md_links(adopted_payload))
    assert len(links) >= len(ENTRY_LINK_FILES), links

    expected = (project / "AGENTS.md").resolve()
    for source, target in links:
        resolved = (source.parent / target.split("#", 1)[0]).resolve()
        assert resolved == expected, f"{source}: {target} -> {resolved}"

    # The adopted contract never creates a second entry at .argentos/AGENTS.md.
    assert not (project / ".argentos" / "AGENTS.md").exists()
