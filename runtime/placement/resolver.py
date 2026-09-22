"""Deterministic placement resolution: ``PLACE`` or ``STOP`` — never a guess.

The procedure realized here is the contract's §7 algorithm, in its order:

1. semantic identification (the caller supplies the kind; this module cannot
   infer it from a filename, an extension or a folder's resemblance);
2. domain / owner — discriminator 1;
3. kind / family — discriminator 2, looked up **within** the domain;
4. canonical namespace from the family rule;
5. canonicality qualification — a qualifier that never selects a namespace;
6. authority / lifetime — metadata, never selecting;
7. constraint validation;
8. place, with recorded evidence.

Anything the procedure cannot resolve with an **explicit and applicable** rule
returns :class:`PlacementStop` instead. There is no fallback, no "closest
match", no inference from an existing folder, and no implicit exception. That
is the whole point: ``explicit rule -> PLACE``, otherwise ``STOP``.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum

from . import rules as R


class PlacementOutcome(str, Enum):
    """The two admissible results of a resolution."""

    PLACE = "PLACE"
    STOP = "STOP"


class PlacementStop(str, Enum):
    """STOP triggers of the contract §8, plus its two verification states.

    ``INVALID_PLACEMENT`` and ``UNRESOLVED_EXCEPTION`` are the verification
    counterparts of §16 (``PC-51``): they do not create placement rules, they
    report that a proposed location is not the one an explicit rule designates.
    """

    UNKNOWN_KIND = "UNKNOWN_KIND"
    NO_DOMAIN = "NO_DOMAIN"
    CROSS_DOMAIN_AMBIGUITY = "CROSS_DOMAIN_AMBIGUITY"
    NEW_FAMILY = "NEW_FAMILY"
    AMBIGUOUS_KIND = "AMBIGUOUS_KIND"
    UNDEFINED_PLACEMENT = "UNDEFINED_PLACEMENT"
    TWO_VALID_LOCATIONS = "TWO_VALID_LOCATIONS"
    AUTHORITY_UNRESOLVED = "AUTHORITY_UNRESOLVED"
    CONSTRAINT_VIOLATION = "CONSTRAINT_VIOLATION"
    INVALID_PLACEMENT = "INVALID_PLACEMENT"
    UNRESOLVED_EXCEPTION = "UNRESOLVED_EXCEPTION"


@dataclass(frozen=True)
class PlacementRequest:
    """What the caller knows about the artifact. Fields are inputs, not guesses.

    ``kind`` is free text: the contract's kind vocabulary is non-exhaustive
    (``PC-8``), so this module matches it against the rule table and stops when
    nothing matches rather than normalising it into something plausible.
    """

    #: Semantic identification of the artifact (step 1). Free text, for evidence.
    description: str = ""
    #: Domain/owner if the caller has established it; ``None`` selects the
    #: unambiguous default of the resolved family (see :func:`resolve`).
    domain: str | None = None
    #: Kind or family name (step 3).
    kind: str = ""
    #: Canonicality status (step 5). A qualifier; defaults to source-of-truth.
    canonicality: str = R.CANONICALITY_SOURCE
    #: Repository-relative path whose placement is being verified (``PC-51``).
    #: When ``None`` the request asks only for the canonical namespace.
    path: str | None = None
    #: Namespaces the caller has already located and interpreted as authorized
    #: exceptions in the artifact that owns the decision (``PC-27``/``PC-29``).
    #: This is an explicit input, never a lookup: the resolver has no exception
    #: registry and must not invent one.
    authorized_exceptions: tuple[str, ...] = ()
    #: Constraint inputs the contract checks in step 7.
    declares_payload_dependency: bool = False
    authority_resolved: bool = True
    #: Whether the caller has established that a ``historical`` artifact is
    #: genuinely frozen after closure (§12 ``PC-39``, §5 ``PC-14``). ``historical``
    #: is not a way to legitimise an arbitrary location: without this input the
    #: status is treated as unestablished and the resolution stops. Like
    #: ``authority_resolved``, this is an assertion the caller makes and must be
    #: able to support — the resolver cannot inspect a lifecycle state.
    frozen: bool = False


@dataclass(frozen=True)
class PlacementResult:
    """A ``PLACE`` decision, with the evidence that produced it."""

    canonical_namespace: str
    family: str
    section: str
    evidence: tuple[str, ...] = ()
    #: True when the request carried a path that the rule also confirms.
    path_verified: bool = False


@dataclass(frozen=True)
class PlacementRefusal:
    """A ``STOP`` decision, with everything needed to escalate it."""

    reason: PlacementStop
    detail: str
    unresolved: str = ""
    considered: tuple[str, ...] = ()
    required: tuple[str, ...] = ()
    section: str = R.CONTRACT_SECTIONS["stop"]


@dataclass(frozen=True)
class PlacementDecision:
    """The resolver's answer: exactly one of ``result`` or ``refusal``."""

    outcome: PlacementOutcome
    result: PlacementResult | None = None
    refusal: PlacementRefusal | None = None

    @property
    def placed(self) -> bool:
        return self.outcome is PlacementOutcome.PLACE

    def evidence(self) -> tuple[str, ...]:
        """Provenance of this decision, for the caller's records."""
        if self.result is not None:
            return self.result.evidence
        assert self.refusal is not None
        return (
            f"STOP {self.refusal.reason.value}",
            self.refusal.detail,
            f"contract: {self.refusal.section}",
        )


def _stop(
    reason: PlacementStop,
    detail: str,
    *,
    unresolved: str = "",
    considered: tuple[str, ...] = (),
    required: tuple[str, ...] = (),
    section: str | None = None,
) -> PlacementDecision:
    return PlacementDecision(
        outcome=PlacementOutcome.STOP,
        refusal=PlacementRefusal(
            reason=reason,
            detail=detail,
            unresolved=unresolved,
            considered=considered,
            required=required,
            section=section or R.CONTRACT_SECTIONS["stop"],
        ),
    )


def _matches_any(namespace: R.Namespace, exceptions: tuple[str, ...]) -> bool:
    return any(namespace.contains(entry) for entry in exceptions)


def _conforms(candidate: str, rule: R.FamilyRule) -> bool:
    return any(namespace.contains(candidate) for namespace in rule.namespaces)


def resolve(request: PlacementRequest) -> PlacementDecision:
    """Resolve placement, or refuse explicitly. Pure and deterministic.

    Same request against the same contract revision yields the same decision:
    nothing here reads the filesystem, the clock, the branch or the environment.
    """
    # STEP 1 / 3 — the kind must be nameable and must resolve inside a domain.
    if not request.kind.strip():
        return _stop(
            PlacementStop.UNKNOWN_KIND,
            "the artifact kind was not identified",
            unresolved="kind",
            required=("the artifact kind (a domain-scoped family name or alias)",),
            section=R.CONTRACT_SECTIONS["kind"],
        )

    if request.domain is not None and request.domain not in R.DOMAINS:
        return _stop(
            PlacementStop.NO_DOMAIN,
            f"unknown domain {request.domain!r}",
            unresolved="domain",
            considered=R.DOMAINS,
            required=("one of the two contract domains",),
            section=R.CONTRACT_SECTIONS["domain"],
        )

    if request.domain is None:
        # No domain was asserted: accept only an unambiguous DEV-wide match.
        dev_rules = R.families_for_kind(R.DOMAIN_DEV, request.kind)
        other_rules = R.families_for_kind(R.DOMAIN_PROTOCOL, request.kind)
        if len(dev_rules) == 1 and not other_rules:
            rule = dev_rules[0]
        elif not dev_rules and not other_rules:
            named = R.family_by_name(request.kind)
            if named is None:
                return _stop(
                    PlacementStop.NEW_FAMILY,
                    f"no family rule in any domain matches kind {request.kind!r}",
                    unresolved="kind/family",
                    considered=tuple(f.family for f in R.FAMILIES),
                    required=("a family rule for this kind, or an authorized exception",),
                    section=R.CONTRACT_SECTIONS["kind"],
                )
            rule = named
        else:
            return _stop(
                PlacementStop.CROSS_DOMAIN_AMBIGUITY,
                f"kind {request.kind!r} is defensible in more than one domain",
                unresolved="domain/owner",
                considered=tuple(f.family for f in (*dev_rules, *other_rules)),
                required=("an explicit domain/owner identification",),
                section=R.CONTRACT_SECTIONS["domain"],
            )
    else:
        rule = resolve_family(request.domain, request.kind)
        if isinstance(rule, PlacementDecision):
            return rule

    # STEP 4 — the family rule must yield exactly one canonical namespace.
    if not rule.namespaces:
        return _stop(
            PlacementStop.UNDEFINED_PLACEMENT,
            f"family {rule.family!r} declares no canonical namespace",
            unresolved="canonical namespace",
            considered=(rule.family,),
            required=("a family rule that designates a namespace",),
        )
    if len(rule.namespaces) > 1 and request.path is None:
        return _stop(
            PlacementStop.TWO_VALID_LOCATIONS,
            f"family {rule.family!r} declares several canonical namespaces and "
            "the contract defines no precedence between them",
            unresolved="canonical namespace",
            considered=tuple(n.path for n in rule.namespaces),
            required=("a path to verify, or an explicit selection among the namespaces",),
        )

    namespace = rule.namespaces[0]
    if request.path is not None or request.canonicality == R.CANONICALITY_HISTORICAL:
        candidate = (
            request.path.replace("\\", "/").strip("/")
            if request.path is not None
            else None
        )
        # §12 PC-41: a historical placement is NOT a canonical placement rule, so
        # the path of a frozen artifact is not measured against the canonical
        # namespace. It is recorded as what it is — the artifact's existing
        # location — while the family's canonical namespace is reported from the
        # rule. A new artifact of the same kind still has to go to the canonical
        # namespace, which is why this is confined to the historical status.
        historical = request.canonicality == R.CANONICALITY_HISTORICAL
        if historical and candidate is None:
            return _stop(
                PlacementStop.UNDEFINED_PLACEMENT,
                "a historical artifact retains its existing location; none was given",
                unresolved="existing location",
                required=("the artifact's current path",),
                section=R.CONTRACT_SECTIONS["canonicality"],
            )
        if historical and not request.frozen:
            # "Historical" is a lifecycle property, not a placement claim (§5
            # PC-14: frozen after closure). Accepting it unestablished would turn
            # the status into a general licence to keep any path, so it stops.
            return _stop(
                PlacementStop.UNDEFINED_PLACEMENT,
                "a historical placement requires the artifact to be frozen after "
                "closure; that was not established",
                unresolved="lifecycle status of the artifact",
                required=(
                    "confirmation that the artifact is frozen, or the canonical "
                    "namespace of its family",
                ),
                section=R.CONTRACT_SECTIONS["canonicality"],
            )
        assert candidate is not None
        conforming = next(
            (option for option in rule.namespaces if option.contains(candidate)),
            None,
        )
        if conforming is not None:
            namespace = conforming
        elif historical:
            namespace = R.Namespace(candidate, prefix=False)
        elif any(
            candidate == entry.strip("/") or candidate.startswith(entry.strip("/") + "/")
            for entry in request.authorized_exceptions
        ):
            # An exception the caller already located and interpreted in the
            # owning artifact (PC-27) makes the non-canonical path admissible.
            # The check is containment of the path in the declared exception:
            # a declared exception never authorizes a path outside itself.
            namespace = R.Namespace(candidate, prefix=False)
        elif request.authorized_exceptions:
            return _stop(
                PlacementStop.UNRESOLVED_EXCEPTION,
                f"{candidate!r} is not canonical and no declared exception covers it",
                unresolved="exception",
                considered=request.authorized_exceptions,
                required=("an exception whose owning artifact can be located",),
                section=R.CONTRACT_SECTIONS["exceptions"],
            )
        else:
            return _stop(
                PlacementStop.INVALID_PLACEMENT,
                f"{candidate!r} is not the canonical namespace of family "
                f"{rule.family!r}",
                unresolved="authorized exception",
                considered=tuple(n.path for n in rule.namespaces),
                required=(
                    "an exception located and interpreted in the artifact "
                    "that owns the decision",
                ),
                section=R.CONTRACT_SECTIONS["agent"],
            )

    # STEP 5 — canonicality is a qualifier; it never selects a namespace.
    status = request.canonicality
    if status not in R.CANONICALITIES:
        return _stop(
            PlacementStop.UNDEFINED_PLACEMENT,
            f"unknown canonicality status {status!r}",
            unresolved="canonicality",
            considered=R.CANONICALITIES,
            required=("a canonicality status defined by the contract",),
            section=R.CONTRACT_SECTIONS["canonicality"],
        )
    if status == R.CANONICALITY_GENERATED:
        # PC-47: generated has NO default location; it is placeable only where a
        # family rule, generator or governing mechanism designates a location.
        # The session-state family does designate one (the host's evidence area),
        # so it is admissible there and nowhere else. Canonicality still selects
        # nothing: the namespace came from the family rule, not from the status.
        if R.CANONICALITY_GENERATED not in rule.canonicality:
            return _stop(
                PlacementStop.UNDEFINED_PLACEMENT,
                f"family {rule.family!r} designates no location for generated "
                "content, and canonicality alone cannot supply one",
                unresolved="explicit location designation for a generated artifact",
                considered=tuple(n.path for n in rule.namespaces),
                required=(
                    "a family rule, generator or governing mechanism that "
                    "explicitly designates the location",
                ),
                section=R.CONTRACT_SECTIONS["canonicality"],
            )
        namespace = rule.namespaces[0]
    if status == R.CANONICALITY_SCRATCH:
        # PC-44: scratch is disposable and non-canonical. It must live in the
        # designated disposable mechanism, which no family rule here designates —
        # so a scratch artifact is never placed inside a canonical namespace.
        return _stop(
            PlacementStop.UNDEFINED_PLACEMENT,
            "scratch content is disposable and non-canonical; no family rule "
            "designates a disposable mechanism for this input",
            unresolved="designated disposable location",
            considered=tuple(n.path for n in rule.namespaces),
            required=(
                "the designated disposable mechanism (e.g. the session scratch "
                "area or the test session temp root)",
            ),
            section=R.CONTRACT_SECTIONS["canonicality"],
        )
    # The historical status needs no further work here: step 4 already captured
    # the retained location and established the frozen condition.

    # STEP 6 — authority and lifetime are metadata, recorded not selecting.
    if not request.authority_resolved:
        return _stop(
            PlacementStop.AUTHORITY_UNRESOLVED,
            "the artifact's authority class is unresolved",
            unresolved="authority",
            required=("an authority class established independently of placement",),
        )

    # STEP 7 — constraints. Distribution is checked because a payload placement
    # is an RFC-56 matter, not a placement choice (PC-37).
    if request.declares_payload_dependency and rule.domain == R.DOMAIN_PROTOCOL:
        return _stop(
            PlacementStop.CONSTRAINT_VIOLATION,
            "the payload must not depend on DEV (ADR-18 RS-10)",
            unresolved="dependency direction",
            considered=(rule.family,),
            required=("removal of the DEV dependency",),
        )

    evidence = (
        f"domain={rule.domain}",
        f"family={rule.family}",
        f"canonical_namespace={namespace.path}",
        f"canonicality={status} (qualifier; did not select the namespace)",
        f"distributed={'yes' if rule.distributed else 'no'}",
        f"rule={rule.section}",
    )
    return PlacementDecision(
        outcome=PlacementOutcome.PLACE,
        result=PlacementResult(
            canonical_namespace=namespace.path,
            family=rule.family,
            section=rule.section,
            evidence=evidence,
            path_verified=request.path is not None,
        ),
    )


def resolve_family(domain: str, kind: str) -> R.FamilyRule | PlacementDecision:
    """Map ``kind`` to exactly one family of ``domain`` (§4, §7 step 3)."""
    matches = R.families_for_kind(domain, kind)
    if len(matches) == 1:
        return matches[0]
    if not matches:
        named = R.family_by_name(kind)
        if named is not None and named.domain == domain:
            return named
        return _stop(
            PlacementStop.NEW_FAMILY,
            f"no family rule of domain {domain} matches kind {kind!r}",
            unresolved="kind/family",
            considered=tuple(f.family for f in R.FAMILIES if f.domain == domain),
            required=("a family rule for this kind, or an authorized exception",),
            section=R.CONTRACT_SECTIONS["kind"],
        )
    # Several families accept the kind. This is not evidence of ambiguity when
    # the contract defines one of them as the narrower category of the other
    # (a test fixture is a specialization of the test subsystem, PC-42): the
    # most specific declared kind set wins. Any other overlap is real ambiguity
    # and must stop rather than be resolved by a tie-break the contract does not
    # define.
    narrowest = min(matches, key=lambda rule: len(rule.kinds))
    if all(narrowest.kinds != other.kinds for other in matches if other is not narrowest):
        return narrowest
    return _stop(
        PlacementStop.AMBIGUOUS_KIND,
        f"kind {kind!r} matches several families of domain {domain}",
        unresolved="kind/family",
        considered=tuple(f.family for f in matches),
        required=("an unambiguous family identification",),
        section=R.CONTRACT_SECTIONS["kind"],
    )


def verify_path(request: PlacementRequest) -> PlacementDecision:
    """Verify a proposed or existing path against its family rule (``PC-51``).

    Convenience over :func:`resolve` that requires a path, so a caller checking
    where an artifact *is* cannot accidentally ask only for a namespace.
    """
    if request.path is None:
        return _stop(
            PlacementStop.INVALID_PLACEMENT,
            "path verification requires a path",
            unresolved="path",
            required=("the artifact's path",),
            section=R.CONTRACT_SECTIONS["agent"],
        )
    return resolve(request)
