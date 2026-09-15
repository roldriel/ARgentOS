"""Tests for tools/check_lifecycle_checkpoint.py (C-2, Plan 98 / Increment 4;
F-1 correction, Plan 99).

Covers the C-2 rules from
docs/plans/98-change-lifecycle-unit-d-increment-4.md §11/§16.2: checkpoint
records as relations, Git tree identity vs commit SHA locators, GC-1
consistency against the applicable anchor (A1/A2), revalidation lineage,
absence of any reachability requirement from dev/origin, GAP vs ANOMALY
semantics and deterministic behavior. Since Plan 99 (F-1), GC-1 selects the
anchor of the validation whose validated state corresponds to the closure
state (final closing commit tree, or declared closure literal); selection
never uses "latest A2" or generic tree membership among the closing commits
(docs/plans/99-change-lifecycle-f1-c2-gc1-correction.md §14). Fixtures build
real git repositories in tmp_path; no network and no dependency on the real
origin state.
"""

from __future__ import annotations

import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[1]
TOOL = REPO_ROOT / "tools" / "check_lifecycle_checkpoint.py"

import check_lifecycle_checkpoint as clc  # noqa: E402
from testsupport import assert_tool_imports_only_stdlib  # noqa: E402

pytestmark = pytest.mark.skipif(
    shutil.which("git") is None, reason="git CLI not available"
)


_GIT_ENV = {
    "GIT_AUTHOR_NAME": "t",
    "GIT_AUTHOR_EMAIL": "t@t",
    "GIT_COMMITTER_NAME": "t",
    "GIT_COMMITTER_EMAIL": "t@t",
    "PATH": os.environ.get("PATH", ""),
    "HOME": os.environ.get("HOME", ""),
    "SYSTEMROOT": os.environ.get("SYSTEMROOT", ""),
}


def git(root: Path, *args: str) -> None:
    subprocess.run(
        ["git", "-C", str(root), *args],
        check=True, capture_output=True, env=_GIT_ENV,
    )


def git_out(root: Path, *args: str) -> str:
    result = subprocess.run(
        ["git", "-C", str(root), *args],
        check=True, capture_output=True, text=True, env=_GIT_ENV,
    )
    return result.stdout.strip()


def init_repo(tmp_path: Path) -> Path:
    git(tmp_path, "init", "-q", "-b", "main")
    return tmp_path


def commit(root: Path, files: dict[str, str], message: str) -> tuple[str, str]:
    """Write files, commit everything, return (sha, tree)."""
    for rel, content in files.items():
        path = root / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
    git(root, "add", "-A")
    git(root, "commit", "-qm", message)
    sha = git_out(root, "rev-parse", "HEAD")
    tree = git_out(root, "rev-parse", "HEAD^{tree}")
    return sha, tree


def empty_commit(root: Path, message: str) -> tuple[str, str]:
    """A new commit over the same tree (same content, different SHA)."""
    git(root, "commit", "--allow-empty", "-qm", message)
    sha = git_out(root, "rev-parse", "HEAD")
    tree = git_out(root, "rev-parse", "HEAD^{tree}")
    return sha, tree


def regime_doc(
    status: str,
    anchor_body: str,
    checkpoint_body: str,
    checkpoint_heading: str = "Checkpoint / cierre",
) -> str:
    return (
        "# Plan 99 — Sample\n\n"
        f"**Status:** {status}\n"
        "**Change Level:** L2\n"
        "**RFC:** RFC-75\n\n"
        "## Objetivo\n\nTexto.\n\n"
        "## Validation anchor\n"
        f"{anchor_body}\n"
        f"## {checkpoint_heading}\n"
        f"{checkpoint_body}\n"
    )


def anchor_a1(tree: str, validity: str = "`vigente` (V1)") -> str:
    delta = "b" * 64
    return (
        "- Declared scope: battery of the repo.\n"
        "- Validation command-set: `python -m pytest tests/`\n"
        "- Effective inputs (repo content): repo content.\n"
        "- Observed dependencies: no instrumentado\n"
        "- Environmental factors: OS Windows; sin red.\n"
        "- Scoped Content Identity:\n"
        f"  - State identity (estado validado): T1 = `{tree}`\n"
        f"  - Delta scoped identity: `{delta}`\n"
        f"- Validity / stale: {validity}\n"
    )


def checkpoint_record(
    commits: list[str],
    tree: str,
    consistency: str = "V1 == C1 tree → **PASS**.",
    condition: str = "**`Closed` (docs-only, sin release)**",
) -> str:
    closing = "\n".join(
        f"  - C{index + 1} `{sha}` — commit de cierre."
        for index, sha in enumerate(commits)
    )
    return (
        "- Commits de cierre:\n"
        f"{closing}\n"
        f"- Estado validado: `## Validation anchor` (V1); "
        f"State identity T1 = `{tree}`.\n"
        f"- Estado de cierre (tree id): `{tree}`\n"
        f"- Consistencia checkpoint↔anchor: {consistency}\n"
        "- Governance aplicada: Plan Executed; docs-only.\n"
        f"- Condición derivada: {condition}\n"
    )


def write_plan(root: Path, doc: str, name: str = "99-sample.md") -> Path:
    path = root / "docs" / "plans" / name
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(doc, encoding="utf-8")
    return path


def run_tool(root: Path) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, str(TOOL), "--root", str(root)],
        capture_output=True, text=True, cwd=str(root),
    )


def one_finding(root: Path) -> clc.CheckpointFinding:
    findings = clc.verify_all(root)
    assert len(findings) == 1
    return findings[0]


# --- Valid checkpoints ---------------------------------------------------------


def test_valid_checkpoint_is_valid(tmp_path):
    root = init_repo(tmp_path)
    sha_a, tree_a = commit(root, {"content.txt": "v1\n"}, "content A")
    doc = regime_doc(
        "Executed", anchor_a1(tree_a), checkpoint_record([sha_a], tree_a)
    )
    write_plan(root, doc)
    finding = one_finding(root)
    assert finding.classification == "VALID"
    assert run_tool(root).returncode == 0


def test_closure_tree_identity_matches_closing_commit(tmp_path):
    root = init_repo(tmp_path)
    sha_a, tree_a = commit(root, {"content.txt": "v1\n"}, "content A")
    doc = regime_doc(
        "Executed", anchor_a1(tree_a), checkpoint_record([sha_a], tree_a)
    )
    write_plan(root, doc)
    finding = one_finding(root)
    assert finding.classification == "VALID"
    assert not any("tree" in reason for reason in finding.reasons)


def test_a1_closure_is_valid(tmp_path):
    """A1-only closure: the validated state is the closure state."""
    root = init_repo(tmp_path)
    sha_a, tree_a = commit(root, {"content.txt": "v1\n"}, "content A")
    doc = regime_doc(
        "Executed", anchor_a1(tree_a), checkpoint_record([sha_a], tree_a)
    )
    write_plan(root, doc)
    assert one_finding(root).classification == "VALID"


def test_same_tree_different_commit_sha_is_valid(tmp_path):
    """R-C2-3: a different commit SHA with the identical tree is valid;
    commit SHA is a locator, never the material identity."""
    root = init_repo(tmp_path)
    sha_a, tree_a = commit(root, {"content.txt": "v1\n"}, "content A")
    sha_b, tree_b = empty_commit(root, "amend-like commit, same content")
    assert sha_a != sha_b
    assert tree_a == tree_b
    doc = regime_doc(
        "Executed", anchor_a1(tree_a), checkpoint_record([sha_b], tree_a)
    )
    write_plan(root, doc)
    finding = one_finding(root)
    assert finding.classification == "VALID"


def test_checkpoint_heading_variant_of_plan_96_is_member(tmp_path):
    """The corpus record of plan 96 uses '## Checkpoint' for the same
    container heading; it must be treated as a regime member."""
    root = init_repo(tmp_path)
    sha_a, tree_a = commit(root, {"content.txt": "v1\n"}, "content A")
    doc = regime_doc(
        "Executed",
        anchor_a1(tree_a),
        checkpoint_record([sha_a], tree_a),
        checkpoint_heading="Checkpoint",
    )
    write_plan(root, doc)
    finding = one_finding(root)
    assert finding.classification == "VALID"


# --- A1 / A2 semantics -----------------------------------------------------------


def anchor_a1_a2(tree_a: str, tree_b: str) -> str:
    delta = "b" * 64
    return (
        "- Declared scope: battery of the repo.\n"
        "- Validation command-set: `python -m pytest tests/`\n"
        "- Effective inputs (repo content): repo content.\n"
        "- Observed dependencies: no instrumentado\n"
        "- Environmental factors: OS Windows; sin red.\n"
        "- Scoped Content Identity:\n"
        f"  - State identity (estado validado = C1): T1 = `{tree_a}`\n"
        f"  - Delta scoped identity: `{delta}`\n"
        "- Validity / stale: `vigente` (V1); revalidada por **V2** (A2)\n"
        "- **A2 (revalidación)** — referencia al anchor original: **A1**;\n"
        "  estado revalidado (C2):\n"
        f"  - State identity (estado revalidado = C2): T2 = `{tree_b}`\n"
        "  command-set idéntico al de A1; factores ambientales sin cambios;\n"
        "  resultado PASS.\n"
    )


def anchor_a1_a2_a3(tree_a: str, tree_b: str, tree_c: str) -> str:
    """A1 plus two independent revalidations (A2a/A2b), each with its own
    embedded validated state (T1/T2/T3 in registration order)."""
    delta = "b" * 64
    return (
        "- Declared scope: battery of the repo.\n"
        "- Validation command-set: `python -m pytest tests/`\n"
        "- Effective inputs (repo content): repo content.\n"
        "- Observed dependencies: no instrumentado\n"
        "- Environmental factors: OS Windows; sin red.\n"
        "- Scoped Content Identity:\n"
        f"  - State identity (estado validado = C1): T1 = `{tree_a}`\n"
        f"  - Delta scoped identity: `{delta}`\n"
        "- Validity / stale: `vigente` (V1); revalidada por V2a (A2a) y V2b "
        "(A2b), resultados PASS.\n"
        "- **A2a (revalidación)** — referencia al anchor original: **A1**;\n"
        "  estado revalidado (C2):\n"
        f"  - State identity (estado revalidado = C2): T2 = `{tree_b}`\n"
        "- **A2b (revalidación)** — referencia al anchor original: **A1**;\n"
        "  estado revalidado (C3):\n"
        f"  - State identity (estado revalidado = C3): T3 = `{tree_c}`\n"
    )


def checkpoint_a2(
    commits: list[str],
    tree_b: str,
    consistency: str = "A2: estado de cierre == T2 → **PASS**.",
) -> str:
    closing = "\n".join(
        f"  - C{index + 1} `{sha}` — commit de cierre."
        for index, sha in enumerate(commits)
    )
    return (
        "- Commits de cierre:\n"
        f"{closing}\n"
        "- Estado validado: V1 sobre C1; revalidación A2 sobre C2 "
        f"(State identity T2 = `{tree_b}`).\n"
        f"- Estado de cierre (tree id): `{tree_b}`\n"
        f"- Consistencia checkpoint↔anchor: {consistency}\n"
        "- Governance aplicada: Plan Executed; docs-only.\n"
        "- Condición derivada: **`Closed` (docs-only, sin release)**\n"
    )


def test_a2_revalidation_referencing_a1_is_valid(tmp_path):
    """A2 is a new validation over a new state; it references A1 and the
    closure is checked against A2 (the applicable anchor for closure)."""
    root = init_repo(tmp_path)
    sha_a, tree_a = commit(root, {"content.txt": "v1\n"}, "content A")
    sha_b, tree_b = commit(root, {"content.txt": "v2\n"}, "content B")
    doc = regime_doc(
        "Executed",
        anchor_a1_a2(tree_a, tree_b),
        checkpoint_a2([sha_a, sha_b], tree_b),
    )
    write_plan(root, doc)
    finding = one_finding(root)
    assert finding.classification == "VALID"
    assert "A1" in anchor_a1_a2(tree_a, tree_b)


def test_closure_against_different_tree_with_a2_is_valid(tmp_path):
    """A different tree is evaluated against the anchors: with an applicable
    A2 it is valid, not an automatic invalidation (R-C2-3/CL-2)."""
    root = init_repo(tmp_path)
    sha_a, tree_a = commit(root, {"content.txt": "v1\n"}, "content A")
    sha_b, tree_b = commit(root, {"content.txt": "v2\n"}, "content B")
    assert tree_a != tree_b
    doc = regime_doc(
        "Executed",
        anchor_a1_a2(tree_a, tree_b),
        checkpoint_a2([sha_a, sha_b], tree_b),
    )
    write_plan(root, doc)
    finding = one_finding(root)
    assert finding.classification == "VALID"


def test_closure_incompatible_with_a1_and_no_a2_is_anomaly(tmp_path):
    """Closure state differs from A1's validated state while PASS is declared
    and no applicable A2 exists -> ANOMALY (R-C2-4; single-commit case)."""
    root = init_repo(tmp_path)
    sha_a, tree_a = commit(root, {"content.txt": "v1\n"}, "content A")
    sha_b, tree_b = commit(root, {"content.txt": "v2\n"}, "content B")
    doc = regime_doc(
        "Executed", anchor_a1(tree_a), checkpoint_record([sha_b], tree_b)
    )
    write_plan(root, doc)
    finding = one_finding(root)
    assert finding.classification == "ANOMALY"
    assert (
        "closure state has no corresponding validation while consistency "
        "declares PASS" in " ".join(finding.reasons)
    )
    assert run_tool(root).returncode == 1


def test_a2_declared_without_a1_reference_is_anomaly(tmp_path):
    root = init_repo(tmp_path)
    sha_a, tree_a = commit(root, {"content.txt": "v1\n"}, "content A")
    body = anchor_a1(tree_a, validity="revalidada por V2 sobre el estado final")
    checkpoint = (
        "- Commits de cierre:\n"
        f"  - C1 `{sha_a}` — commit de cierre.\n"
        "- Estado validado: revalidación A2 sin anchor original.\n"
        f"- Estado de cierre (tree id): `{tree_a}`\n"
        "- Consistencia checkpoint↔anchor: A2 → **PASS**.\n"
        "- Governance aplicada: Plan Executed; docs-only.\n"
        "- Condición derivada: **`Closed` (docs-only, sin release)**\n"
    )
    doc = regime_doc("Executed", body, checkpoint)
    write_plan(root, doc)
    finding = one_finding(root)
    assert finding.classification == "ANOMALY"
    assert "revalidation (A2) declared without reference" in " ".join(
        finding.reasons
    )


# --- GAP cases -----------------------------------------------------------------


def test_missing_checkpoint_is_na(tmp_path):
    """Member without a closure record is N/A: Executed without Closed is
    legal (CL-4)."""
    root = init_repo(tmp_path)
    sha_a, tree_a = commit(root, {"content.txt": "v1\n"}, "content A")
    doc = regime_doc(
        "Executed",
        anchor_a1(tree_a),
        "<!-- Se completa al cerrar. -->",
    )
    write_plan(root, doc)
    finding = one_finding(root)
    assert finding.classification == "N/A"
    assert run_tool(root).returncode == 0


def test_planned_member_without_checkpoint_is_na(tmp_path):
    root = init_repo(tmp_path)
    _, tree_a = commit(root, {"content.txt": "v1\n"}, "content A")
    doc = regime_doc(
        "Aprobado para ejecución",
        "<!-- Se completa al ejecutar. -->",
        "<!-- Se completa al cerrar. -->",
    )
    write_plan(root, doc)
    finding = one_finding(root)
    assert finding.classification == "N/A"


def test_missing_checkpoint_field_is_gap(tmp_path):
    root = init_repo(tmp_path)
    sha_a, tree_a = commit(root, {"content.txt": "v1\n"}, "content A")
    checkpoint = checkpoint_record([sha_a], tree_a).replace(
        "- Governance aplicada: Plan Executed; docs-only.\n", ""
    )
    doc = regime_doc("Executed", anchor_a1(tree_a), checkpoint)
    write_plan(root, doc)
    finding = one_finding(root)
    assert finding.classification == "GAP"
    assert "Governance aplicada" in finding.reasons[0]
    assert run_tool(root).returncode == 0


def test_closed_without_pass_evidence_is_gap(tmp_path):
    root = init_repo(tmp_path)
    sha_a, tree_a = commit(root, {"content.txt": "v1\n"}, "content A")
    checkpoint = checkpoint_record(
        [sha_a], tree_a, consistency="V1 == C1 tree (revisión manual)."
    )
    doc = regime_doc("Executed", anchor_a1(tree_a), checkpoint)
    write_plan(root, doc)
    finding = one_finding(root)
    assert finding.classification == "GAP"
    assert "Closed declared without PASS evidence" in " ".join(
        finding.reasons
    )


def test_unresolvable_commit_locator_is_gap(tmp_path):
    root = init_repo(tmp_path)
    _, tree_a = commit(root, {"content.txt": "v1\n"}, "content A")
    checkpoint = checkpoint_record(["f" * 40], tree_a)
    doc = regime_doc("Executed", anchor_a1(tree_a), checkpoint)
    write_plan(root, doc)
    finding = one_finding(root)
    assert finding.classification == "GAP"
    assert "not resolvable" in " ".join(finding.reasons)


def test_missing_anchor_is_gap(tmp_path):
    root = init_repo(tmp_path)
    sha_a, tree_a = commit(root, {"content.txt": "v1\n"}, "content A")
    checkpoint = checkpoint_record([sha_a], tree_a)
    doc = regime_doc("Executed", "<!-- vacío -->", checkpoint)
    write_plan(root, doc)
    finding = one_finding(root)
    assert finding.classification == "GAP"
    assert "not registered in this artifact" in " ".join(finding.reasons)


# --- Anomalies -------------------------------------------------------------------


def test_wrong_declared_closure_tree_is_anomaly(tmp_path):
    """Declared closure tree id differs from the closing commit's tree while
    the record claims consistency -> ANOMALY (tree identity is semantic)."""
    root = init_repo(tmp_path)
    sha_a, tree_a = commit(root, {"content.txt": "v1\n"}, "content A")
    wrong = "c" * 40
    checkpoint = checkpoint_record([sha_a], tree_a).replace(
        f"- Estado de cierre (tree id): `{tree_a}`",
        f"- Estado de cierre (tree id): `{wrong}`",
    )
    doc = regime_doc("Executed", anchor_a1(tree_a), checkpoint)
    write_plan(root, doc)
    finding = one_finding(root)
    assert finding.classification == "ANOMALY"
    assert "declared closure tree differs" in " ".join(finding.reasons)
    assert run_tool(root).returncode == 1


# --- No reachability requirement ---------------------------------------------------


def test_valid_unreachable_commit_is_accepted(tmp_path):
    """A valid local object is verifiable even when no branch reaches it:
    C-2 never requires reachability from dev/origin (R-C2-6)."""
    root = init_repo(tmp_path)
    commit(root, {"content.txt": "v1\n"}, "content A")
    git(root, "checkout", "-qb", "temp")
    sha_u, tree_u = commit(root, {"content.txt": "v2\n"}, "content U")
    git(root, "checkout", "-q", "main")
    git(root, "branch", "-D", "temp")
    doc = regime_doc(
        "Executed", anchor_a1(tree_u), checkpoint_record([sha_u], tree_u)
    )
    write_plan(root, doc)
    finding = one_finding(root)
    assert finding.classification == "VALID"
    assert run_tool(root).returncode == 0


# --- F-1 regressions (Plan 99): closure-state correspondence, not recency ---


def test_closure_on_a1_state_with_later_a2_is_valid_anchor_a1(tmp_path):
    """F-1 Case A (T1): closure on A1's state is VALID with applicable anchor
    A1 even when a later A2 exists whose validated tree is not among the
    closing commits. The pre-fix implementation chose the latest A2 and raised
    a false ANOMALY."""
    root = init_repo(tmp_path)
    sha_a, tree_a = commit(root, {"content.txt": "v1\n"}, "content A")
    _, tree_b = commit(root, {"content.txt": "v2\n"}, "content B")
    sha_c, tree_c = commit(root, {"content.txt": "v1\n"}, "content A again")
    assert tree_a == tree_c
    doc = regime_doc(
        "Executed",
        anchor_a1_a2(tree_a, tree_b),
        checkpoint_record([sha_a, sha_c], tree_a),
    )
    write_plan(root, doc)
    finding = one_finding(root)
    assert finding.classification == "VALID"
    assert "applicable validation anchor (GC-1): A1" in " ".join(
        finding.reasons
    )
    assert run_tool(root).returncode == 0


def test_closure_on_first_a2_with_later_a2_is_valid_anchor_a2(tmp_path):
    """F-1 Case B (T2): closure on the first A2's state is VALID with that
    A2; a later A2b must not displace it by recency (pre-fix implementation:
    latest A2 wins -> false ANOMALY when A2b's tree is not among the closing
    commits)."""
    root = init_repo(tmp_path)
    sha_a, tree_a = commit(root, {"content.txt": "v1\n"}, "content A")
    sha_b, tree_b = commit(root, {"content.txt": "v2\n"}, "content B")
    tree_c = "c" * 40  # A2b validated state, not present in closing commits
    sha_d, tree_d = empty_commit(root, "content B again")
    assert tree_b == tree_d
    doc = regime_doc(
        "Executed",
        anchor_a1_a2_a3(tree_a, tree_b, tree_c),
        checkpoint_record([sha_a, sha_b, sha_d], tree_b),
    )
    write_plan(root, doc)
    finding = one_finding(root)
    assert finding.classification == "VALID"
    assert "applicable validation anchor (GC-1): A2" in " ".join(
        finding.reasons
    )
    assert run_tool(root).returncode == 0


def test_closure_state_without_corresponding_validation_and_pass_is_anomaly(
    tmp_path,
):
    """F-1 Case C (T3/T9): a multi-commit closure state with no corresponding
    validation while PASS/Closed are declared is ANOMALY. The pre-fix
    implementation produced a false VALID because A1's tree appeared among the
    closing commits."""
    root = init_repo(tmp_path)
    sha_a, tree_a = commit(root, {"content.txt": "v1\n"}, "content A")
    sha_b, tree_b = commit(root, {"content.txt": "v2\n"}, "content B")
    doc = regime_doc(
        "Executed",
        anchor_a1(tree_a),
        checkpoint_record([sha_a, sha_b], tree_b),
    )
    write_plan(root, doc)
    finding = one_finding(root)
    assert finding.classification == "ANOMALY"
    assert (
        "closure state has no corresponding validation while consistency "
        "declares PASS" in " ".join(finding.reasons)
    )
    assert run_tool(root).returncode == 1


def test_closure_state_without_corresponding_validation_without_pass_is_gap(
    tmp_path,
):
    """F-1 Case C without PASS evidence: GAP (advisory), never ANOMALY;
    absence of evidence is not converted into a contradiction."""
    root = init_repo(tmp_path)
    sha_a, tree_a = commit(root, {"content.txt": "v1\n"}, "content A")
    sha_b, tree_b = commit(root, {"content.txt": "v2\n"}, "content B")
    checkpoint = checkpoint_record([sha_a, sha_b], tree_b).replace(
        "V1 == C1 tree → **PASS**.",
        "V1 == C1 tree (revisión manual).",
    )
    doc = regime_doc("Executed", anchor_a1(tree_a), checkpoint)
    write_plan(root, doc)
    finding = one_finding(root)
    assert finding.classification == "GAP"
    assert run_tool(root).returncode == 0


def test_declared_closure_tree_must_match_final_closing_commit(tmp_path):
    """T5: the declared closure tree must match the FINAL closing commit's
    tree; a literal matching only an intermediate commit is contradictory.
    Pre-fix generic membership accepted it as VALID."""
    root = init_repo(tmp_path)
    sha_a, tree_a = commit(root, {"content.txt": "v1\n"}, "content A")
    sha_b, tree_b = commit(root, {"content.txt": "v2\n"}, "content B")
    sha_c, tree_c = commit(root, {"content.txt": "v1\n"}, "content A again")
    assert tree_a == tree_c
    doc = regime_doc(
        "Executed",
        anchor_a1(tree_a),
        checkpoint_record([sha_a, sha_b, sha_c], tree_b),
    )
    write_plan(root, doc)
    finding = one_finding(root)
    assert finding.classification == "ANOMALY"
    assert "declared closure tree differs" in " ".join(finding.reasons)
    assert run_tool(root).returncode == 1


def test_corpus_declared_revalidation_over_final_state_is_valid(tmp_path):
    """Corpus v1 pattern (plans 96-98): the final closing commit is identified
    by message (no embedded SHA, anti-self-reference) and the Validation
    Anchor declares a single V2 over the final content with PASS -> VALID with
    applicable anchor A2 (declared). Historical records must not regress."""
    root = init_repo(tmp_path)
    sha_a, tree_a = commit(root, {"content.txt": "v1\n"}, "content A")
    validity = (
        "`vigente` (V1); revalidada por **V2** (batería completa) sobre el "
        "contenido final C2 antes del cierre"
    )
    checkpoint = (
        "- Commits de cierre:\n"
        f"  - C1 `{sha_a}` — commit de contenido.\n"
        "  - C2 — este commit de registro; su SHA se identifica por el "
        "mensaje (auto-referencia excluida).\n"
        "- Estado validado: `## Validation anchor` (V1); revalidación V2 "
        "sobre C2.\n"
        "- Estado de cierre: tree id del último commit de cierre (C2) = "
        "`git rev-parse C2^{tree}` (no embebido por auto-referencia).\n"
        "- Consistencia checkpoint↔anchor: V1 ↔ C1 → **PASS**; V2 sobre el "
        "contenido final → **PASS**.\n"
        "- Governance aplicada: Plan Executed; docs-only.\n"
        "- Condición derivada: **`Closed` (docs-only, sin release)**\n"
    )
    doc = regime_doc(
        "Executed",
        anchor_a1(tree_a, validity=validity),
        checkpoint,
    )
    write_plan(root, doc)
    finding = one_finding(root)
    assert finding.classification == "VALID"
    assert "applicable validation anchor (GC-1): A2 (declared)" in " ".join(
        finding.reasons
    )
    assert run_tool(root).returncode == 0


def test_multiple_declared_revalidations_without_embedded_trees_are_gap(
    tmp_path,
):
    """Two declared revalidations both referencing the closure state, without
    embedded identities and with an unresolvable final commit, are ambiguous:
    GAP (no invented tie-break, no false VALID, no false ANOMALY)."""
    root = init_repo(tmp_path)
    sha_a, tree_a = commit(root, {"content.txt": "v1\n"}, "content A")
    validity = (
        "`vigente` (V1); revalidada por **V2a** (batería completa) sobre el "
        "contenido final C2 antes del cierre"
    )
    anchor = (
        anchor_a1(tree_a, validity=validity)
        + "\n- **A2b (revalidación)** — referencia al anchor original: "
        "**A1**; estado revalidado: contenido final C2 (resultado PASS)."
    )
    checkpoint = (
        "- Commits de cierre:\n"
        f"  - C1 `{sha_a}` — commit de contenido.\n"
        "  - C2 — este commit de registro; su SHA se identifica por el "
        "mensaje (auto-referencia excluida).\n"
        "- Estado validado: `## Validation anchor` (V1); revalidación V2a/V2b "
        "sobre C2.\n"
        "- Estado de cierre: tree id del último commit de cierre (C2) = "
        "`git rev-parse C2^{tree}` (no embebido por auto-referencia).\n"
        "- Consistencia checkpoint↔anchor: V2a/V2b sobre el contenido final "
        "→ **PASS**.\n"
        "- Governance aplicada: Plan Executed; docs-only.\n"
        "- Condición derivada: **`Closed` (docs-only, sin release)**\n"
    )
    doc = regime_doc("Executed", anchor, checkpoint)
    write_plan(root, doc)
    finding = one_finding(root)
    assert finding.classification == "GAP"
    assert "multiple declared revalidations could correspond" in " ".join(
        finding.reasons
    )
    assert run_tool(root).returncode == 0


def test_fail_with_closed_is_anomaly(tmp_path):
    """T12: a genuine inconsistency (declared FAIL while Closed) is ANOMALY
    with exit code 1."""
    root = init_repo(tmp_path)
    sha_a, tree_a = commit(root, {"content.txt": "v1\n"}, "content A")
    checkpoint = checkpoint_record(
        [sha_a], tree_a, consistency="V1 == C1 tree → **FAIL**."
    )
    doc = regime_doc("Executed", anchor_a1(tree_a), checkpoint)
    write_plan(root, doc)
    finding = one_finding(root)
    assert finding.classification == "ANOMALY"
    assert (
        "condition declares Closed while consistency declares FAIL"
        in " ".join(finding.reasons)
    )
    assert run_tool(root).returncode == 1


# --- Population / determinism --------------------------------------------------------


def test_legacy_artifact_excluded(tmp_path):
    root = init_repo(tmp_path)
    write_plan(
        root,
        "# Plan 01 — Legacy\n\n**Status:** Executed\n\n## Objetivo\n\nTexto.\n",
        "01-legacy.md",
    )
    finding = one_finding(root)
    assert finding.classification == "EXCLUDED"


def test_deterministic_report(tmp_path):
    root = init_repo(tmp_path)
    sha_a, tree_a = commit(root, {"content.txt": "v1\n"}, "content A")
    doc = regime_doc(
        "Executed", anchor_a1(tree_a), checkpoint_record([sha_a], tree_a)
    )
    write_plan(root, doc)
    first = clc.format_report(clc.verify_all(root))
    second = clc.format_report(clc.verify_all(root))
    assert first == second
    assert clc.verify_all(root) == clc.verify_all(root)


def test_real_repo_expected_classifications():
    """Dogfooding expectations on the real repo (Plan 98 §17.2/§36):
    plans 96/97 VALID, legacy plans EXCLUDED, plan 98 is a regime member —
    N/A while PLANNED and VALID once its own checkpoint is registered (self-
    dogfooding); never EXCLUDED/GAP/ANOMALY. Since Plan 99 (F-1), plan 99 is a
    regime member too: N/A while PLANNED and VALID once its checkpoint is
    registered."""
    res = run_tool(REPO_ROOT)
    assert res.returncode == 0, res.stdout
    assert "96-change-lifecycle-unit-b-increments-1-3.md: VALID" in res.stdout
    assert "97-change-lifecycle-unit-c-increment-2.md: VALID" in res.stdout
    assert re.search(
        r"98-change-lifecycle-unit-d-increment-4\.md: (?:N/A|VALID)", res.stdout
    )
    assert re.search(
        r"99-change-lifecycle-f1-c2-gc1-correction\.md: (?:N/A|VALID)",
        res.stdout,
    )
    assert "94-change-lifecycle-master-action-plan.md: EXCLUDED" in res.stdout
    assert "95-change-lifecycle-unit-a-increment-0.md: EXCLUDED" in res.stdout
    assert "ANOMALY=0" in res.stdout


# --- stdlib only ----------------------------------------------------------------------

def test_tool_uses_only_stdlib():
    assert_tool_imports_only_stdlib(TOOL, {"check_lifecycle_checkpoint"})
