"""Dogfood: the EARS coverage guard against the real repository (plan 137).

This module is an **anchored test** in the sense of ``tests/AGENTS.md``: it reads
the live payload on purpose, and only reads it. A synthetic payload cannot express
what it protects — that the three sources of truth of the real payload still
agree: the standard declares the five EARS patterns, the contract declares the
Markdown-bullet form canonical, and ``gate_validator.py`` really activates and
materializes the ``ears`` check for ``H01``.

Its stability contract is the documented one: it may name canonical paths,
sections and artifact numbers of the real repository, so it is updated when that
canonical state legitimately changes. It is not portable and is not meant to be.

**Corpus limitation, declared and not asserted away** (plan 137 §Dogfood 3).
``TASK_SPECIFICATION.md`` is a *session* artifact under
``.project/<session-uuid>/<iteration>/``, and ``.project/`` is ephemeral and not
versioned, so the DEV repository has **no versioned corpus** of acceptance
criteria. The coverage of R1/R2 over production data is therefore **not**
demonstrated here; what this module demonstrates is the parity and documentary
coherence of the payload (R3/R4/R5), which is what protects against the ``F-01``
regression. The R1/R2 evidence comes from specimens with provenance, in
``tests/test_check_ears_coverage_falsification.py``.

Nothing here mutates repository state.
"""

from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from pathlib import Path

import check_ears_coverage as checker

REPO_ROOT = Path(__file__).resolve().parents[1]
TOOL = REPO_ROOT / "tools" / "check_ears_coverage.py"
PAYLOAD = REPO_ROOT / "protocol" / ".agents"
EARS = PAYLOAD / checker.EARS_REL
CONTRACT = PAYLOAD / checker.CONTRACT_REL
POLICY = PAYLOAD / checker.POLICY_REL
VALIDATOR = PAYLOAD / checker.VALIDATOR_REL


def _run(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(TOOL), *args],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
        encoding="utf-8",
    )


def _document(*args: str) -> dict:
    result = _run(*args, "--json")
    assert result.returncode in (0, 1), result.stdout + result.stderr
    return json.loads(result.stdout)


def _signals(document: dict, rule: str) -> set[str]:
    return {item["signal"] for item in document["results"] if item["rule"] == rule}


def _reasons(document: dict) -> str:
    return " | ".join(item["reason"] for item in document["results"])


# --------------------------------------------------------------------------- #
# The three sources of truth are present and readable
# --------------------------------------------------------------------------- #


def test_the_three_sources_of_truth_exist():
    for path in (EARS, CONTRACT, POLICY, VALIDATOR):
        assert path.is_file(), path
        assert path.read_text(encoding="utf-8").strip(), path


def test_the_standard_declares_the_five_patterns_of_the_mechanical_set():
    """R5 derives its set here: five templates, each with placeholders."""
    module = checker.load_validator(PAYLOAD)
    mechanical = checker.load_mechanical_set(PAYLOAD, module)
    assert len(mechanical.patterns) == 5
    assert [pattern.template for pattern in mechanical.patterns] == [
        "The <system name> shall <system response>",
        "When <event>, the <system name> shall <system response>",
        "While <state>, the <system name> shall <system response>",
        "If <optional pre-condition>, then the <system name> shall <system response>",
        "Where <feature>, the <system name> shall <system response>",
    ]
    # No pattern list is maintained by the tool: the templates are the standard's.
    text = EARS.read_text(encoding="utf-8")
    for pattern in mechanical.patterns:
        assert pattern.template in text, pattern.template


def test_the_standard_still_carries_the_writing_rules_the_guard_excludes():
    """The excluded subset is real: the rules exist and stay out of the gate."""
    text = EARS.read_text(encoding="utf-8").casefold()
    assert "use \"shall\"" in text
    assert "avoid negations" in text
    assert "one criterion per bullet" in text


def test_the_contract_declares_the_canonical_form_verbatim():
    """R3 reads these two declarations; they are the contract's own words."""
    text = CONTRACT.read_text(encoding="utf-8")
    assert "The canonical form is one Markdown bullet per criterion" in text
    assert "only in the TOML block does not satisfy the canonical form" in text


def test_the_policy_requires_the_bullets_for_h01():
    """The rule's normative source: H01's Gate Checklist item 3."""
    text = POLICY.read_text(encoding="utf-8")
    assert "## Gate Checklist" in text
    assert "contains at least one bullet" in text
    assert "EARS patterns" in text


def test_the_validator_activates_ears_for_h01_in_its_spec():
    """R4's first half: the activation flag, read from the payload module."""
    module = checker.load_validator(PAYLOAD)
    assert module.TRIGGERS["H01"]["ears"] is True
    assert module.TRIGGERS["H01"]["artifact"] == "TASK_SPECIFICATION.md"
    assert hasattr(module, "EARS_RE")
    assert callable(module.validate)


# --------------------------------------------------------------------------- #
# R3/R4/R5 over the real payload
# --------------------------------------------------------------------------- #


def test_r3_r4_and_r5_are_valid_on_the_real_payload():
    """The guard is green on the real payload: no `ANOMALY`, exit 0."""
    document = _document("--payload", str(PAYLOAD))
    assert _signals(document, "R3") == {checker.VALID}, _reasons(document)
    assert _signals(document, "R4") == {checker.VALID}, _reasons(document)
    assert _signals(document, "R5") == {checker.VALID}, _reasons(document)
    assert document["counts"]["ANOMALY"] == 0, _reasons(document)
    result = _run("--payload", str(PAYLOAD))
    assert result.returncode == 0, result.stdout + result.stderr


def test_r4_reports_the_validators_own_decision_as_evidence():
    """The check is *invoked*: the decision reported is the payload's."""
    document = _document("--payload", str(PAYLOAD))
    r4 = [item for item in document["results"] if item["rule"] == "R4"]
    assert len(r4) == 1, _reasons(document)
    assert "the payload spec activates `ears` for H01" in r4[0]["reason"]
    assert "validator decision:" in r4[0]["reason"]
    assert r4[0]["source"] == checker.VALIDATOR_REF


def test_r5_reports_the_derived_pattern_set_as_evidence():
    document = _document("--payload", str(PAYLOAD))
    assert len(document["patterns"]) == 5
    for pattern in document["patterns"]:
        assert "<" in pattern["template"]
        assert "<" not in pattern["filled"]
        assert pattern["placeholders"]
    r5 = [item for item in document["results"] if item["rule"] == "R5"]
    assert len(r5) == 1
    assert "declared and implemented sets are in parity" in r5[0]["reason"]


def test_the_guard_invokes_the_payload_validator_instead_of_reimplementing_it():
    """The source has no pattern literal: the accepted set is the payload's."""
    source = TOOL.read_text(encoding="utf-8")
    assert "importlib.util.spec_from_file_location" in source
    assert checker.VALIDATOR_REL in source
    # No second copy of the five alternatives: the only place the pattern text
    # appears is the docstring/report, never a compiled matcher of this tool.
    assert "shall .+" not in source
    assert "EARS_RE" in source


# --------------------------------------------------------------------------- #
# The declared corpus limitation
# --------------------------------------------------------------------------- #


def test_without_a_corpus_r1_and_r2_are_a_declared_absence_not_a_pass():
    """Plan 137 §Contrato 1 and §Dogfood 3: no corpus is an explicit N/A."""
    document = _document("--payload", str(PAYLOAD))
    assert _signals(document, "R1") == {checker.NOT_APPLICABLE}, _reasons(document)
    assert _signals(document, "R2") == {checker.NOT_APPLICABLE}, _reasons(document)
    assert checker.GAP not in _signals(document, "R1")
    assert "no `--corpus` was given" in _reasons(document)


def test_the_repository_has_no_versioned_task_specification_corpus():
    """The limitation is a fact, not an assertion: `.project/` is outside git.

    ``TASK_SPECIFICATION.md`` lives under ``.project/<session>/<iteration>/`` and
    ``.project/`` is ephemeral and not versioned (root ``AGENTS.md``), so no
    corpus can be cited from the repository. The only versioned files with that
    name are the payload *contracts* (the templates), which are not session
    artifacts. If a versioned specimen ever appears, this test fails and the
    corpus limitation declared in the module docstring must be revisited.
    """
    versioned = [
        path
        for path in REPO_ROOT.rglob("*TASK_SPECIFICATION.md")
        if ".project" not in path.parts and ".git" not in path.parts
    ]
    outside_payload = [path for path in versioned if "protocol" not in path.parts]
    assert outside_payload == [], [str(path) for path in outside_payload]
    assert all(path.name == "TASK_SPECIFICATION.md" for path in versioned)
    assert PAYLOAD / checker.CONTRACT_REL in versioned


def test_a_corpus_path_outside_the_repository_is_read_only_evidence(tmp_path):
    """A real corpus may be passed by path; nothing about it is copied in."""
    specimen = tmp_path / "TASK_SPECIFICATION.md"
    specimen.write_text(
        "# Specimen\n\n## Acceptance Criteria\n\n"
        "- The API shall reject a POST /users request with an empty name.\n"
        "- When the email is already registered, the API shall return HTTP 409.\n"
        "- While the database is unavailable, the API shall return HTTP 503.\n"
        "- If the user ID is not a number, then the API shall return HTTP 400.\n"
        "- Where email validation is enabled, the API shall reject malformed email addresses.\n",
        encoding="utf-8",
    )
    document = _document("--payload", str(PAYLOAD), "--corpus", str(specimen))
    assert _signals(document, "R1") == {checker.VALID}, _reasons(document)
    assert _signals(document, "R2") == {checker.VALID}, _reasons(document)
    assert document["counts"]["ANOMALY"] == 0, _reasons(document)


def test_the_non_acceptable_bullet_of_the_standard_is_caught_with_the_real_validator(tmp_path):
    """The real payload validator operates: this is R2's live falsification.

    The specimen is the standard's own non-acceptable bullet, so the case comes
    from `EARS.md:Examples for this project` and not from this suite.
    """
    specimen = tmp_path / "TASK_SPECIFICATION.md"
    specimen.write_text(
        "# Specimen\n\n## Acceptance Criteria\n\n"
        "- The API should handle errors gracefully.\n",
        encoding="utf-8",
    )
    result = _run("--payload", str(PAYLOAD), "--corpus", str(specimen))
    assert result.returncode == 1, result.stdout + result.stderr
    document = json.loads(_run("--payload", str(PAYLOAD), "--corpus", str(specimen), "--json").stdout)
    assert _signals(document, "R2") == {checker.ANOMALY}
    assert "do not match EARS" in " | ".join(
        item["evidence"] for item in document["results"]
    )


# --------------------------------------------------------------------------- #
# The declared frontier and the read-only policy
# --------------------------------------------------------------------------- #


def test_the_tool_declares_what_it_does_not_do():
    """A reader must see the excluded block in the shipped source."""
    source = TOOL.read_text(encoding="utf-8")
    assert "does **not** do" in source
    assert "a declared boundary, not an approval" in " ".join(source.split())
    for item in ("compound", "negations", "should", "unconfirmed assumption"):
        assert item in source.casefold(), item
    for _description, _classification in checker.EXCLUDED_SUBSET:
        assert _classification


def test_the_report_names_the_excluded_subset_and_its_classification():
    result = _run("--payload", str(PAYLOAD))
    assert result.returncode == 0
    for description, classification in checker.EXCLUDED_SUBSET:
        assert description in result.stdout, description
        assert classification in result.stdout, classification


def test_the_guard_is_read_only_over_the_real_payload():
    """Running the guard over the real payload changes nothing in it.

    The snapshot covers bytes *and* modification times, because the failure mode
    is a bytecode cache: loading the payload validator by its real path would rewrite
    ``protocol/.agents/harness/__pycache__/gate_validator.cpython-*.pyc`` if the
    guard let the interpreter write it.
    """
    before = _payload_snapshot()
    _run("--payload", str(PAYLOAD))
    _run("--payload", str(PAYLOAD), "--json")
    assert _payload_snapshot() == before


def test_two_runs_over_the_real_payload_are_byte_identical():
    first = _run("--payload", str(PAYLOAD), "--json")
    second = _run("--payload", str(PAYLOAD), "--json")
    assert first.stdout == second.stdout
    assert first.returncode == second.returncode == 0


def _payload_digest() -> str:
    digest = hashlib.sha256()
    for path in sorted(PAYLOAD.rglob("*")):
        if path.is_file():
            digest.update(path.relative_to(PAYLOAD).as_posix().encode("utf-8"))
            digest.update(path.read_bytes())
    return digest.hexdigest()


def _payload_snapshot() -> dict[str, tuple[int, str]]:
    """Every payload file as (size, mtime_ns), so a rewritten cache is visible."""
    snapshot: dict[str, tuple[int, str]] = {}
    for path in sorted(PAYLOAD.rglob("*")):
        if path.is_file():
            stat = path.stat()
            snapshot[path.relative_to(PAYLOAD).as_posix()] = (stat.st_size, str(stat.st_mtime_ns))
    return snapshot
