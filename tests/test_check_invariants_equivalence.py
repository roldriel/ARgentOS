"""Tests for check_invariants_equivalence.py.

The canonical invariants block is materialized twice (development repository
and payload) and must stay identical byte for byte inside the
``canonical-invariants-v1`` markers. These tests cover the equivalence gate
and its failure modes: any material drift, a lost row, a duplicated or
renamed identifier, and unusable sources.
"""

from __future__ import annotations

from pathlib import Path

import check_invariants_equivalence as ce

REPO_ROOT = Path(__file__).resolve().parents[1]

HEADER = (
    "| ID | NAME | FORMULATION | SCOPE | OUT_OF_SCOPE | ENFORCEMENT_STATUS | LIMIT |\n"
    "|---|---|---|---|---|---|---|"
)


def row(entry_id: str, formulation: str | None = None) -> str:
    formulation = formulation or f"Formulation {entry_id}."
    return (
        f"| {entry_id} | Name {entry_id} | {formulation} | Scope {entry_id} "
        f"| Out {entry_id} | NONE | Limit {entry_id} |"
    )


def block(ids=None, formulation=None) -> str:
    ids = ids or list(ce.EXPECTED_IDS)
    rows = [row(i) for i in ids]
    if formulation:
        rows = [formulation(entry_id, text) for entry_id, text in zip(ids, rows)]
    return HEADER + "\n" + "\n".join(rows)


def document(body: str) -> str:
    return (
        "# Catalog\n\n"
        f"{ce.BEGIN_MARKER}\n{body}\n{ce.END_MARKER}\n\n"
        "Domain prose that is deliberately not compared.\n"
    )


def write_pair(root: Path, dev_body: str, protocol_body: str) -> None:
    dev = root / ce.DEV_REL
    protocol = root / ce.PROTOCOL_REL
    dev.parent.mkdir(parents=True, exist_ok=True)
    protocol.parent.mkdir(parents=True, exist_ok=True)
    dev.write_text(document(dev_body), encoding="utf-8")
    protocol.write_text(document(protocol_body), encoding="utf-8")


def test_identical_blocks_pass(tmp_path):
    write_pair(tmp_path, block(), block())
    report, _ = ce.verify(tmp_path)
    assert report["identical"] is True
    assert report["problems"] == []
    assert report["dev_entries"] == len(ce.EXPECTED_IDS)


def test_domain_prose_is_not_compared(tmp_path):
    write_pair(tmp_path, block(), block())
    protocol = tmp_path / ce.PROTOCOL_REL
    protocol.write_text(
        protocol.read_text(encoding="utf-8").replace(
            "Domain prose that is deliberately not compared.",
            "Different prose: interpretation, mechanisms and local limits differ.",
        ),
        encoding="utf-8",
    )
    report, _ = ce.verify(tmp_path)
    assert report["identical"] is True
    assert report["problems"] == []


def test_line_endings_are_the_only_allowed_normalization(tmp_path):
    write_pair(tmp_path, block().replace("\n", "\r\n"), block())
    report, _ = ce.verify(tmp_path)
    assert report["identical"] is True
    assert report["problems"] == []


def test_material_change_fails(tmp_path):
    write_pair(tmp_path, block(), block(formulation=lambda i, r: r.replace("Formulation INV-03.", "Changed.")))
    report, _ = ce.verify(tmp_path)
    assert report["identical"] is False
    assert any("diverge" in problem for problem in report["problems"])


def test_lost_row_fails(tmp_path):
    write_pair(tmp_path, block(), block([i for i in ce.EXPECTED_IDS if i != "INV-07"]))
    report, _ = ce.verify(tmp_path)
    assert report["identical"] is False
    assert any("missing canonical ids" in problem for problem in report["problems"])


def test_duplicated_id_fails(tmp_path):
    write_pair(tmp_path, block(), block(list(ce.EXPECTED_IDS[:-1]) + ["INV-12"]))
    report, _ = ce.verify(tmp_path)
    assert report["identical"] is False
    assert any("duplicated ids" in problem for problem in report["problems"])


def test_renamed_id_fails(tmp_path):
    write_pair(tmp_path, block(), block(["INV-00"] + list(ce.EXPECTED_IDS[1:])))
    report, _ = ce.verify(tmp_path)
    assert report["identical"] is False
    assert any("INV-01" in problem for problem in report["problems"])


def test_identity_is_deterministic_and_line_ending_insensitive():
    body = block()
    assert ce.block_identity(body) == ce.block_identity(body)
    assert ce.block_identity(body) == ce.block_identity(body.replace("\n", "\r\n"))
    assert ce.block_identity(body) != ce.block_identity(body.replace("INV-01", "INV-99"))


def test_missing_markers_fail(tmp_path):
    dev = tmp_path / ce.DEV_REL
    protocol = tmp_path / ce.PROTOCOL_REL
    dev.parent.mkdir(parents=True, exist_ok=True)
    protocol.parent.mkdir(parents=True, exist_ok=True)
    dev.write_text(document(block()), encoding="utf-8")
    protocol.write_text("# no markers here\n", encoding="utf-8")
    report, _ = ce.verify(tmp_path)
    assert report["identical"] is False
    assert any("markers missing" in problem for problem in report["problems"])


def test_empty_block_fails(tmp_path):
    write_pair(tmp_path, block(), "")
    report, _ = ce.verify(tmp_path)
    assert report["identical"] is False
    assert any("empty" in problem for problem in report["problems"])


def test_missing_representation_fails(tmp_path):
    (tmp_path / ce.DEV_REL).parent.mkdir(parents=True, exist_ok=True)
    (tmp_path / ce.DEV_REL).write_text(document(block()), encoding="utf-8")
    report, _ = ce.verify(tmp_path)
    assert report["identical"] is False
    assert any("not found" in problem for problem in report["problems"])


def test_the_repository_itself_passes():
    report, _ = ce.verify(REPO_ROOT)
    assert report["problems"] == []
    assert report["identical"] is True
    assert report["dev_entries"] == len(ce.EXPECTED_IDS)


def test_tool_imports_only_stdlib():
    import testsupport

    testsupport.assert_tool_imports_only_stdlib(
        REPO_ROOT / "tools" / "check_invariants_equivalence.py"
    )
