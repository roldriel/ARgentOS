"""Falsification of the EARS coverage guard: the table of plan 137 §Tests (plan 137).

These are the negative cases, written to **refute** the guard rather than to
confirm it. Two halves, and both matter:

- **The guard must flag**: a criteria section with no bullet, criteria only in the
  ``acceptance_criteria`` TOML block, a bullet matching no EARS pattern, an
  unresolvable citation, a missing source of truth, a payload validator that
  stops checking EARS, and a validator whose accepted pattern set diverges from
  the standard (the false positive / false negative case).
- **The guard must stay silent**: a compound bullet, a negative bullet and a
  bullet using ``should``/``must``/``will``/``may``. Those are ``[agent]``
  judgement or writing rules H01 does not mark ``[gate]``; the silence is the
  declared boundary, not an approval — so the cases that pass are deliberately
  *bad* criteria, and the test says so.

Everything is isolated (``tests/AGENTS.md``): the payload is a synthetic tree
built in a repository-external temporary, through ``tests/pytest_isolation.py``.
"""

from __future__ import annotations

import io
import json
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path

import pytest

import pytest_isolation

import check_ears_coverage as checker
import test_check_ears_coverage as base

# --------------------------------------------------------------------------- #
# Scaffolding
# --------------------------------------------------------------------------- #


def workspace(name: str) -> Path:
    """A throw-away tree outside the repository, owned by this suite."""
    root = pytest_isolation.scratch_root("test_check_ears_coverage_falsification")
    tree = root / name
    tree.mkdir(parents=True, exist_ok=True)
    return tree


def invoke(*args: str) -> tuple[int, dict | None, str]:
    """Run the CLI in-process; return exit code, parsed JSON (or ``None``) and stderr."""
    out, err = io.StringIO(), io.StringIO()
    with redirect_stdout(out), redirect_stderr(err):
        code = checker.main([str(arg) for arg in args])
    text = out.getvalue()
    return code, (json.loads(text) if text.strip() else None), err.getvalue()


def signals(document: dict, rule: str) -> set[str]:
    return {
        item["signal"] for item in document["results"] if item["rule"] == rule
    }


def reasons(document: dict) -> str:
    return " | ".join(item["reason"] for item in document["results"])


def build(name: str, **kwargs) -> Path:
    return base.make_payload(workspace(name), **kwargs)


def spec(name: str, bullets: list[str] | str, **kwargs) -> Path:
    tree = workspace(name)
    return base.write_specimen(tree / "TASK_SPECIFICATION.md", bullets, **kwargs)


# --------------------------------------------------------------------------- #
# The negative table: each case must fail explicitly and reproducibly
# --------------------------------------------------------------------------- #


def test_no_bullets_in_the_criteria_section_is_declared_not_a_pass():
    """Plan 137 §Tests: a section without bullets is a declared GAP, exit 0."""
    payload = build("no_bullets")
    specimen = spec("no_bullets", "To be defined later.")
    code, document, err = invoke("--payload", payload, "--corpus", specimen, "--json")
    assert code == 0, err
    assert signals(document, "R1") == {checker.GAP}
    assert checker.VALID not in signals(document, "R1")
    assert "never `VALID` by emptiness" in reasons(document)


def test_a_missing_criteria_section_is_declared_not_a_pass():
    payload = build("missing_section")
    specimen = spec("missing_section", "", section=False)
    code, document, _err = invoke("--payload", payload, "--corpus", specimen, "--json")
    assert code == 0
    assert signals(document, "R1") == {checker.GAP}
    assert signals(document, "R2") == {checker.NOT_APPLICABLE}


def test_criteria_only_in_the_toml_block_violate_the_canonical_form():
    """Plan 137 §Tests: the TOML-only form is the R3 violation of F-01."""
    payload = build("toml_only")
    specimen = spec(
        "toml_only",
        '```toml\nacceptance_criteria = ["The API shall respond."]\n```',
    )
    code, document, _err = invoke("--payload", payload, "--corpus", specimen, "--json")
    assert code == 0
    assert signals(document, "R1") == {checker.GAP}
    assert "acceptance_criteria` TOML block" in reasons(document)


def test_a_bullet_matching_no_pattern_is_an_anomaly():
    """Plan 137 §Tests: the standard's own non-acceptable bullet, exit 1."""
    payload = build("no_pattern")
    specimen = spec("no_pattern", ["The API should handle errors gracefully."])
    code, document, err = invoke("--payload", payload, "--corpus", specimen, "--json")
    assert code == 1, err
    assert signals(document, "R2") == {checker.ANOMALY}
    assert "reports FAIL" in reasons(document)


def test_the_non_acceptable_bullet_of_the_standard_is_caught_alone():
    payload = build("non_acceptable")
    specimen = spec("non_acceptable", ["The API should handle errors gracefully."])
    code, document, _err = invoke("--payload", payload, "--corpus", specimen, "--json")
    assert code == 1
    evidence = " | ".join(item["evidence"] for item in document["results"])
    assert "do not match EARS" in evidence


def test_an_unresolvable_citation_is_an_anomaly():
    """Plan 137 §Contrato 10: present but contradictory evidence is an ANOMALY.

    The contract keeps both declarations — so the form is declared — but grounds
    them on a citation into the payload that does not resolve (the file exists,
    the section does not). The declaration can therefore not be relied on, and the
    guard reports ``ANOMALY`` rather than ``VALID``.
    """
    contract = (
        "# Contract\n\n## Acceptance Criteria\n\n"
        "The canonical form is one Markdown bullet per criterion, as declared in "
        f"`{checker.EARS_REL}:No Such Section`.\n\n"
        "An artifact whose criteria appear only in the TOML block does not satisfy "
        "the canonical form.\n"
    )
    payload = build("citation_unresolved", contract=contract)
    code, document, err = invoke("--payload", payload, "--json")
    assert code == 1, err
    assert signals(document, "R3") == {checker.ANOMALY}
    assert "cites" in reasons(document)
    assert "section absent" in reasons(document)


def test_a_citation_whose_file_is_absent_is_an_anomaly():
    contract = (
        "# Contract\n\n## Acceptance Criteria\n\n"
        "The canonical form is one Markdown bullet per criterion, as declared in "
        "`standards/requirements/ABSENT.md:Patterns`.\n\n"
        "An artifact whose criteria appear only in the TOML block does not satisfy "
        "the canonical form.\n"
    )
    payload = build("citation_absent_file", contract=contract)
    code, document, err = invoke("--payload", payload, "--json")
    assert code == 1, err
    assert signals(document, "R3") == {checker.ANOMALY}
    assert "file absent" in reasons(document)


def test_a_resolvable_citation_is_not_an_anomaly():
    """The falsification's control: a citation that resolves stays VALID."""
    contract = (
        "# Contract\n\n## Acceptance Criteria\n\n"
        "The canonical form is one Markdown bullet per criterion, as declared in "
        f"`{checker.EARS_REL}:Patterns`.\n\n"
        "An artifact whose criteria appear only in the TOML block does not satisfy "
        "the canonical form.\n"
    )
    payload = build("citation_resolved", contract=contract)
    code, document, err = invoke("--payload", payload, "--json")
    assert code == 0, err
    assert signals(document, "R3") == {checker.VALID}


def test_a_missing_source_of_truth_is_gap_and_never_valid():
    """Plan 137 §Tests: an absent EARS.md is a GAP, never a VALID."""
    payload = build("missing_contract", contract=None)
    code, document, _err = invoke("--payload", payload, "--json")
    assert code == 0
    assert signals(document, "R3") == {checker.GAP}
    assert checker.VALID not in signals(document, "R3")


def test_a_missing_standard_is_a_read_error_not_a_pass():
    payload = build("missing_standard", ears_standard=None)
    code, document, err = invoke("--payload", payload, "--json")
    assert code == 2
    assert document is None, "a read error produces no report"
    assert "EARS standard not found" in err


def test_a_payload_regression_that_stops_checking_ears_is_an_anomaly():
    """Plan 137 §Tests: H01's spec without ``ears`` is an R4 regression."""
    payload = build("no_ears_flag", validator=base.fake_validator_source(ears=False))
    code, document, err = invoke("--payload", payload, "--json")
    assert code == 1, err
    assert signals(document, "R4") == {checker.ANOMALY}
    assert "does not activate the `ears` check" in reasons(document)


def test_a_payload_regression_producing_no_ears_entry_is_an_anomaly():
    payload = build(
        "no_ears_entry",
        fenced=(
            "\n\ndef validate(trigger, artifact, root=None):\n"
            '    return ([{"id": "existence", "result": "PASS", "evidence": "ok"}], "PASS")\n'
        ),
    )
    code, document, _err = invoke("--payload", payload, "--json")
    assert code == 1
    assert signals(document, "R4") == {checker.ANOMALY}
    assert "produced no `ears` entry" in reasons(document)


def test_a_pattern_the_validator_accepts_and_the_standard_does_not_declare_is_an_anomaly():
    """Plan 137 §Tests: a false positive of the validator is an ANOMALY.

    The fifth alternative is widened past the placeholders the standard declares,
    so the implemented set accepts a sentence shape the standard never declares.
    """
    source = base.fake_validator_source().replace(
        'r"|Where .+, the .+ shall .+"', 'r"|Where .+, the .+ shall .+ and .+"'
    )
    payload = build("false_positive", validator=source)
    code, document, err = invoke("--payload", payload, "--json")
    assert code == 1, err
    assert signals(document, "R5") == {checker.ANOMALY}


def test_a_pattern_the_standard_declares_and_the_validator_rejects_is_an_anomaly():
    """Plan 137 §Tests: a false negative of the validator is an ANOMALY."""
    source = base.fake_validator_source().replace(
        '    r"|Where .+, the .+ shall .+"\n', ""
    )
    payload = build("false_negative", validator=source)
    code, document, err = invoke("--payload", payload, "--json")
    assert code == 1, err
    assert signals(document, "R5") == {checker.ANOMALY}
    assert "rejects a sentence formed from" in reasons(document)


def test_a_sixth_declared_pattern_is_an_anomaly():
    """A pattern added to one side and not the other is exactly the guard's job."""
    extra = (
        "### 6. Synthetic extra\n\n"
        "```text\n"
        "Where <feature>, the <system name> shall <system response> and <other>\n"
        "```\n\n"
    )
    standard = base.EARS_STANDARD.replace("## Writing rules", extra + "## Writing rules")
    payload = build("sixth_pattern", ears_standard=standard)
    code, document, err = invoke("--payload", payload, "--json")
    assert code == 1, err
    assert signals(document, "R5") == {checker.ANOMALY}


def test_a_contract_redeclaring_the_toml_block_canonical_is_an_anomaly():
    """The F-01 relapse: the contract contradicting the form it must declare."""
    contract = (
        "# Contract\n\n## Acceptance Criteria\n\n"
        "The canonical form is one Markdown bullet per criterion. Criteria appear "
        "only in the TOML block does not satisfy the canonical form.\n\n"
        "The TOML block is the canonical form and replaces the bullets.\n"
    )
    payload = build("contradiction", contract=contract)
    code, document, err = invoke("--payload", payload, "--json")
    assert code == 1, err
    assert signals(document, "R3") == {checker.ANOMALY}
    assert "would re-derive `F-01`" in reasons(document)


def test_one_half_of_the_declaration_is_a_gap_not_a_pass():
    contract = (
        "# Contract\n\n## Acceptance Criteria\n\n"
        "The canonical form is one Markdown bullet per criterion.\n"
    )
    payload = build("half_declaration", contract=contract)
    code, document, _err = invoke("--payload", payload, "--json")
    assert code == 0
    assert signals(document, "R3") == {checker.GAP}
    assert "only in part" in reasons(document)


def test_the_exit_code_is_one_only_for_an_anomaly():
    """``GAP`` is advisory; only ``ANOMALY`` moves the exit code."""
    gap_payload = build("exit_gap")
    gap_specimen = spec("exit_gap", "Prose without bullets.")
    gap_code, gap_document, _ = invoke(
        "--payload", gap_payload, "--corpus", gap_specimen, "--json"
    )
    assert checker.GAP in signals(gap_document, "R1")
    assert gap_code == 0

    bad_payload = build("exit_anomaly")
    bad_specimen = spec("exit_anomaly", ["The API should handle errors gracefully."])
    bad_code, bad_document, _ = invoke(
        "--payload", bad_payload, "--corpus", bad_specimen, "--json"
    )
    assert checker.ANOMALY in signals(bad_document, "R2")
    assert bad_code == 1


# --------------------------------------------------------------------------- #
# The deliberately-passing bad bullets: the guard must NOT flag them
# --------------------------------------------------------------------------- #


@pytest.mark.parametrize(
    "bullet, judgement",
    [
        (
            "The API shall validate input and return errors.",
            "H01 item 12 `[agent]`: compoundness is declared judgement",
        ),
        (
            "Users can't create accounts with bad data.",
            "EARS.md:Writing rules 3 (avoid negations) is not marked `[gate]` by H01",
        ),
        (
            "The API should handle errors gracefully.",
            "EARS.md:Writing rules 2 (use `shall`) is not marked `[gate]` by H01",
        ),
        (
            "The API must validate the request.",
            "`must` is not a declared pattern: the writing rule stays out of the gate",
        ),
        (
            "The API will log every request.",
            "`will` is not a declared pattern: the writing rule stays out of the gate",
        ),
        (
            "The API may cache responses.",
            "`may` is not a declared pattern: the writing rule stays out of the gate",
        ),
    ],
)
def test_bad_bullets_the_guard_must_not_flag_are_not_flagged(bullet, judgement):
    """Each case is a **bad** criterion the guard must leave alone.

    The assertion is structural: whatever the payload validator verdict is, the
    guard produces findings only under its five declared rules, and never a
    finding that names the judgement. The quotation of the offending bullet in the
    validator's evidence is evidence, not a finding of the guard.
    """
    payload = build(f"boundary_{abs(hash(bullet))}")
    specimen = spec(f"boundary_{abs(hash(bullet))}", [bullet, "The API shall respond."])
    _code, document, err = invoke(
        "--payload", payload, "--corpus", specimen, "--json"
    )
    assert err == "", err
    assert {item["rule"] for item in document["results"]} <= {
        rule for rule, _description, _source in checker.MECHANICAL_SUBSET
    }
    for item in document["results"]:
        # The guard's own reason never carries the judgement vocabulary; the
        # validator's evidence may quote the bullet verbatim.
        assert "compound" not in item["reason"].casefold(), judgement
        assert "negation" not in item["reason"].casefold(), judgement
    assert judgement  # the case is recorded above: silence is deliberate


def test_the_guard_has_no_rule_that_could_flag_the_excluded_subset():
    """The exclusion is structural, not a matter of wording.

    Every rule the guard can emit is in ``MECHANICAL_SUBSET``; the block B items
    are declared in ``EXCLUDED_SUBSET`` and no rule corresponds to them.
    """
    rules = {rule for rule, _description, _source in checker.MECHANICAL_SUBSET}
    assert rules == {"R1", "R2", "R3", "R4", "R5"}
    excluded = " ".join(description for description, _ in checker.EXCLUDED_SUBSET)
    for item in (
        "specific",
        "verifiable",
        "compound",
        "negation",
        "should",
        "domain",
        "assumption",
    ):
        assert item in excluded
    assert len(checker.EXCLUDED_SUBSET) == 7


def test_the_boundary_bullets_produce_no_non_standard_signal():
    """Signals are the repository's five; the guard invents none."""
    payload = build("boundary_signals")
    specimen = spec(
        "boundary_signals",
        [
            "The API shall validate input and return errors.",
            "Users can't create accounts with bad data.",
            "The API should handle errors gracefully.",
        ],
    )
    _code, document, _err = invoke("--payload", payload, "--corpus", specimen, "--json")
    assert set(document["counts"]) == {
        checker.VALID,
        checker.GAP,
        checker.ANOMALY,
        checker.NOT_APPLICABLE,
        checker.BOUNDARY,
    }
    assert set(document["counts"]) <= set(document["counts"])
    for item in document["results"]:
        assert item["signal"] in document["counts"]


# --------------------------------------------------------------------------- #
# Falsifying the guard's own inputs
# --------------------------------------------------------------------------- #


def test_an_empty_standard_forces_a_gap_instead_of_a_pass():
    payload = build("empty_standard", ears_standard="# EARS\n\n## Patterns\n")
    code, document, _err = invoke("--payload", payload, "--json")
    assert code == 0
    assert signals(document, "R5") == {checker.GAP}


def test_a_standard_whose_template_is_not_a_sentence_is_an_anomaly():
    """A declared template the validator rejects is a divergence, not a pass."""
    standard = base.EARS_STANDARD.replace(
        "The <system name> shall <system response>",
        "The <system name> must <system response>",
    )
    payload = build("bad_template", ears_standard=standard)
    code, document, _err = invoke("--payload", payload, "--json")
    assert code == 1
    assert signals(document, "R5") == {checker.ANOMALY}


def test_the_guard_reads_the_templates_from_the_standard_it_is_given():
    """A different standard yields a different mechanical set: nothing is hardcoded."""
    standard = base.EARS_STANDARD.replace(
        "### 5. Optional feature\n\n"
        "```text\n"
        "Where <feature>, the <system name> shall <system response>\n"
        "```\n",
        "",
    )
    payload = build("four_patterns", ears_standard=standard)
    module = checker.load_validator(payload)
    mechanical = checker.load_mechanical_set(payload, module)
    assert len(mechanical.patterns) == 4
    assert not any("Where" in pattern.template for pattern in mechanical.patterns)


def test_the_json_report_is_a_single_parseable_document():
    payload = build("json_document")
    specimen = spec("json_document", ["The API should be nice."])
    out = io.StringIO()
    with redirect_stdout(out):
        checker.main(["--payload", str(payload), "--corpus", str(specimen), "--json"])
    document = json.loads(out.getvalue())
    assert document["results"]
