"""Change Governance Artifact identity + materialization (RFC-76, D-01/D-02/D-03).

Verifies the operationalization decisions: deterministic derived identity via
RFC-71 ``SegmentIdentity``, ``project_identity`` namespace, the four-line
canonical representation, and content-addressed persistence under
``.project/changes/``.
"""

import hashlib

from runtime.toolcalls.change_governance import (
    PROJECT_NAMESPACE_VALUE,
    canonical_representation,
    change_governance_content_identity,
    change_governance_filename,
    change_governance_identity,
    materialize_change_governance_artifact,
)

TARGET = "protocol/.agents/contracts/CHANGE_GOVERNANCE.md"
DECLARATION = "Add an illustrative append-only governance entry example."
VERSION = "11.1.0"


def test_same_inputs_same_identity():
    # Behavior 1: same target+declaration+protocol_version+namespace => same identity.
    assert change_governance_identity(TARGET, DECLARATION, VERSION) == (
        change_governance_identity(TARGET, DECLARATION, VERSION)
    )


def test_declaration_change_changes_identity():
    # Behavior 3: changing the declaration changes the identity.
    assert change_governance_identity(TARGET, DECLARATION, VERSION) != (
        change_governance_identity(TARGET, DECLARATION + " (revised)", VERSION)
    )


def test_target_change_changes_identity():
    assert change_governance_identity(TARGET, DECLARATION, VERSION) != (
        change_governance_identity(TARGET + "#Governance", DECLARATION, VERSION)
    )


def test_protocol_version_change_changes_identity():
    assert change_governance_identity(TARGET, DECLARATION, "11.1.0") != (
        change_governance_identity(TARGET, DECLARATION, "11.2.0")
    )


def test_canonical_is_deterministic_and_uses_utf8_sha256():
    # Behaviors 4 and 5: deterministic canonical form; SHA-256 over UTF-8.
    canon = canonical_representation(TARGET, DECLARATION, VERSION)
    assert canon == (
        f"target={TARGET}\n"
        f"declaration={DECLARATION}\n"
        f"protocol_version={VERSION}\n"
        f"namespace={PROJECT_NAMESPACE_VALUE}"
    )
    assert change_governance_content_identity(TARGET, DECLARATION, VERSION) == (
        hashlib.sha256(canon.encode("utf-8")).hexdigest()
    )
    assert canonical_representation(TARGET, DECLARATION, VERSION) == canon


def test_declaration_is_trimmed_only():
    # Behavior 4 (determinism): declaration is trimmed, no internal normalization.
    padded = f"  {DECLARATION}  "
    assert change_governance_identity(TARGET, padded, VERSION) == (
        change_governance_identity(TARGET, DECLARATION, VERSION)
    )
    # Internal whitespace is preserved (no additional normalization).
    internal = DECLARATION.replace(" ", "  ")
    assert change_governance_identity(TARGET, internal, VERSION) != (
        change_governance_identity(TARGET, DECLARATION, VERSION)
    )


def test_governance_state_excluded_from_identity():
    # Behaviors 2 and 9: governance facts and metadata do not participate in identity.
    canon = canonical_representation(TARGET, DECLARATION, VERSION)
    for excluded in ("decisions", "authorization", "closure", "execution", "evidence"):
        assert excluded not in canon
    # The identity is a pure function of the four identity inputs only.
    assert change_governance_identity(TARGET, DECLARATION, VERSION) == (
        change_governance_identity(TARGET, DECLARATION, VERSION)
    )


def test_namespace_is_project_identity():
    # Behavior 8: the namespace value is `project_identity`.
    assert PROJECT_NAMESPACE_VALUE == "project_identity"
    assert canonical_representation(TARGET, DECLARATION, VERSION).endswith(
        "namespace=project_identity"
    )


def test_materialization_writes_to_changes_dir(tmp_path):
    # Behavior 6: the artifact is materialized at .project/changes/<identity>.md.
    changes_dir = tmp_path / ".project" / "changes"
    path = materialize_change_governance_artifact(
        target=TARGET,
        declaration=DECLARATION,
        protocol_version=VERSION,
        changes_dir=changes_dir,
    )
    assert path.parent == changes_dir
    assert path.exists()
    assert path.suffix == ".md"
    text = path.read_text(encoding="utf-8")
    assert TARGET in text
    assert DECLARATION in text
    assert "namespace: project_identity" in text


def test_filename_derived_from_identity_and_path_does_not_alter_identity(tmp_path):
    # Behavior 7: filename is derived from identity; the path does not affect identity.
    identity = change_governance_identity(TARGET, DECLARATION, VERSION)
    assert change_governance_filename(identity) == change_governance_filename(identity)

    p1 = materialize_change_governance_artifact(
        target=TARGET, declaration=DECLARATION, protocol_version=VERSION,
        changes_dir=tmp_path / "a" / "changes",
    )
    p2 = materialize_change_governance_artifact(
        target=TARGET, declaration=DECLARATION, protocol_version=VERSION,
        changes_dir=tmp_path / "b" / "changes",
    )
    # Same identity => same filename, regardless of the base directory.
    assert p1.name == p2.name
    assert p1.name == change_governance_filename(identity)
    # Identity is unchanged by the filesystem location.
    assert change_governance_identity(TARGET, DECLARATION, VERSION) == identity


def test_append_only_governance_does_not_mutate_identity(tmp_path):
    # Behavior 10: appending governance facts does not mutate identity-bearing fields.
    identity = change_governance_identity(TARGET, DECLARATION, VERSION)
    path = materialize_change_governance_artifact(
        target=TARGET,
        declaration=DECLARATION,
        protocol_version=VERSION,
        decisions=("approve: maintainer"),
        authorizations=("authorize-apply: maintainer"),
        closure_decisions=(),
        changes_dir=tmp_path / ".project" / "changes",
    )
    text = path.read_text(encoding="utf-8")
    # The derived identity recorded in the artifact is unchanged by governance facts.
    assert f"change_identity: {identity}" in text
    assert change_governance_identity(TARGET, DECLARATION, VERSION) == identity
