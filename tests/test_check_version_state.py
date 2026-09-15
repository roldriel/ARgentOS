"""Tests for tools/check_version_state.py (dev-only, no payload dependency)."""

from __future__ import annotations

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]

import check_version_state as cvs  # noqa: E402


def make_repo(
    tmp_path: Path,
    version="1.2.3",
    sections=None,
    tags=None,
    anchor=None,
    with_canonical=True,
):
    (tmp_path / "protocol" / ".agents").mkdir(parents=True)
    (tmp_path / "protocol" / ".agents" / "VERSION").write_text(version + "\n", encoding="utf-8")
    section_list = sections if sections is not None else [version]
    body = "# Changelog\n\n" + "".join(
        f"## [{s}] — 2026-08-14\n\n- item\n\n" for s in section_list
    )
    (tmp_path / "CHANGELOG.md").write_text(body, encoding="utf-8")
    if with_canonical:
        anchor_value = version if anchor is None else anchor
        (tmp_path / "runtime" / "toolcalls").mkdir(parents=True)
        (tmp_path / "runtime" / "toolcalls" / "canonical.py").write_text(
            f'PROTOCOL_VERSION = "{anchor_value}"\n', encoding="utf-8"
        )
    cvs.get_tags = lambda root: tags if tags is not None else []
    return tmp_path


def test_ok_with_dev_exception(tmp_path):
    root = make_repo(tmp_path, version="1.2.3", sections=["1.2.3", "1.1.0"], tags=["1.1.0"])
    errors, warnings = cvs.verify(root)
    assert errors == []
    assert any("1.2.3" in w for w in warnings)


def test_version_without_changelog_section(tmp_path):
    root = make_repo(tmp_path, version="1.2.3", sections=["1.1.0"], tags=[])
    errors, _ = cvs.verify(root)
    assert any("has no ## [1.2.3] section" in e for e in errors)


def test_tag_without_changelog_section(tmp_path):
    root = make_repo(tmp_path, version="1.2.3", sections=["1.2.3"], tags=["1.2.3", "0.9.0"])
    errors, _ = cvs.verify(root)
    assert any("tag 0.9.0 has no" in e for e in errors)


def test_bad_semver(tmp_path):
    root = make_repo(tmp_path, version="banana")
    errors, _ = cvs.verify(root)
    assert any("not semver" in e for e in errors)


def test_runtime_anchor_matches_payload(tmp_path):
    root = make_repo(tmp_path, version="1.2.3")
    errors, _ = cvs.verify(root)
    assert not any("PROTOCOL_VERSION" in e for e in errors)


def test_runtime_anchor_mismatch(tmp_path):
    root = make_repo(tmp_path, version="1.2.3", anchor="1.1.0")
    errors, _ = cvs.verify(root)
    assert any("PROTOCOL_VERSION (1.1.0) does not match" in e for e in errors)


def test_runtime_anchor_missing_declaration(tmp_path):
    root = make_repo(tmp_path, version="1.2.3")
    (root / "runtime" / "toolcalls" / "canonical.py").write_text(
        "VALUE = 1\n", encoding="utf-8"
    )
    errors, _ = cvs.verify(root)
    assert any("declares no parseable PROTOCOL_VERSION" in e for e in errors)


def test_runtime_anchor_missing_file(tmp_path):
    root = make_repo(tmp_path, version="1.2.3", with_canonical=False)
    errors, _ = cvs.verify(root)
    assert any("missing runtime/toolcalls/canonical.py" in e for e in errors)
