# Supervised Autonomous Execution — DEV Operational Policy (Plan 135)

Operational definition of **Supervised Autonomous Execution (SAE)** for the DEV
Autonomous Orchestrator: how the host conducts every step that is already inside
its granted scope and authority, and where it must stop.

Binds once and everywhere:

> **The human does not operate the workflow; the human is the authority.**

SAE reduces **operational** handoffs. It does not reduce human control over
scope, authority, normative decisions, architecture, Protocol, release or
promotion. Autonomy is **operational, not decisional**.

Normative depth is unchanged and is not restated here: RFC-75 governs the Change
Lifecycle, ADR-16 the authority classes and the conflict protocol, and RFC-56 the
payload authorization path. This policy **conducts** those mechanisms; it does not
extend, amend or reinterpret them. `.agents/policies/autonomous-orchestration.md`
defines the host itself; this policy defines the frontier of what that host may
execute without asking again.

Implementation: `runtime/orchestrator/autonomy.py` (deterministic frontier),
`runtime/orchestrator/host.py` (`autonomy_gate`), CLI `--sae`. Tests:
`tests/test_autonomous_scope.py`.

## 1. The three separations

```text
AUTHORITY   what is authorized
    ↓       sources: RFC Accepted, ADR, approved Plan, and the Decision class
            held by the maintainer (ADR-16). Never created by the host.

SCOPE       which work is authorized
    ↓       source: the approved plan's own declaration (## Delegación agentiva:
            the authorized task and the paths it may modify) plus its declared
            deliverables. Never widened by the host.

AUTONOMY    which actions the host may execute without asking again
            the subset of the authorized work the host may conduct alone.
```

The binding rule:

```text
autonomy ⊆ authorized scope
autonomy ⊆ granted authority
```

**Autonomy never widens scope or authority.** If a step is not inside both, it is
not autonomous — whatever it looks like, however close it is, and however obvious
the correction appears.

## 2. The two gates, in order

1. **The plan authorizes the work.** Existing mechanism: a plan
   `Aprobado para ejecución` (or `Executed` for continuation) with entry criteria
   met. The host does not grant, extend or infer this.
2. **SAE verifies the action is inside what was authorized.** For each derived
   action, before acting:

   ```text
   action ∈ authorized scope
   AND action ∈ granted authority
   AND action ∉ stop conditions (§5)
   ```

   Refusal rule: if membership **cannot be established with sufficient evidence**,
   the answer is **STOP**. Authorization is never assumed by semantic proximity —
   not by a similar name, a shared directory, a containing or contained path, a
   plural, a precedent, or an "obvious" inference.

## 3. The autonomy envelope

The envelope is **derived from declarations the approved plan already owns**. It
is not a new declaration surface, not a registry and not a second source of truth:

| Envelope field | Read from |
|---|---|
| authorized task | the plan's `## Delegación agentiva` → `Task` |
| authorized scope | the same section → `Scope` (paths), or the declared deliverables when the scope is not explicit |
| authority basis | the plan's execution status + the plan's own declaration |
| stop conditions | §5 of this policy (fixed vocabulary) |

Absence is honest: **no declaration ⇒ no autonomy**. A plan without the
declaration delegates no semantic work, and the host reports the absence instead
of filling it in.

**Write actions must name their write target**; a write that names no path cannot
be shown to be in scope, so it stops. A **read-only** action (a validation, a
revalidation, a gate run) consumes the authorized change and writes nowhere, so it
needs no path: demanding one would be a check no honest input could satisfy.

Scope comparison is **exact membership** after pure representational
normalization (`./`, separators, a trailing slash). It never produces a new path
and never widens or narrows the scope.

## 4. Autonomous continuation

Inside the envelope the host continues **without an operational handoff**. It may:

- observe; reconstruct state; derive the next step;
- plan the next step; delegate; execute; verify;
- correct, retry and recover inside the scope;
- revalidate and rebuild evidence;
- update the artifacts of its own Change and the documentation it is authorized
  to update;
- run checkers and tests;
- continue to the next derived step;
- derive closure when the conditions are satisfied.

No human authorization is requested merely to move from one of these to the next
when the step is already covered. The host **does not** ask a human to confirm a
step it is already authorized to take.

## 5. Stop conditions (escalate with evidence)

The host stops and escalates, and **never resolves these by inference**:

| Condition | Why it is a frontier |
|---|---|
| scope change | scope is authorized by the human; the host does not widen it |
| authority change | authority classes belong to ADR-16; only the maintainer holds DECISION |
| RFC required | RFC-56: an RFC `Accepted` is required first |
| ADR required | ADR-worthiness is a human judgement (ADR-16 `AU-6`) |
| Protocol change | `protocol/.agents/` is product data with its own RFC-56 path |
| payload change | a payload change follows RFC-56, never the host's authority |
| lifecycle change | RFC-75 governs the lifecycle; the host conducts, it does not extend |
| new authority class, entity, registry or identity primitive | these are architecture decisions, not operations |
| new state machine, or a lifecycle-state change | same: a mechanism decision |
| conflict between normative sources | no source wins automatically (ADR-16 `AU-3`) |
| normative decision | the maintainer decides; the host records and escalates |
| ambiguity not resolvable by evidence | evidence absent or contradictory ⇒ do not guess |
| release, promotion or tag | `FORBIDDEN` for the host regardless of any authorization |
| action explicitly reserved to the human | the reservation is the boundary |
| any modification exceeding the initial authorization | autonomy ⊆ authority, always |

A reached frontier is reported as a stop with the authority that decides instead,
the reason, and the action the host was about to take. **An escalation is a
correct outcome, not a failure.**

## 6. Findings

A **finding** is detected and recorded by the host in the artifact that owns it,
using the existing lineage mechanism (LC-1: `<artifact>:F-<n>`, immutable original
observation/evidence/Git state/provenance).

**Autonomous correction.** The host may **correct** a finding inside the scope.
The authority is not new: the approved plan already authorizes the correction, and
the `C-<n>` record is factual/traceability, never a normative source.

All of these must hold. If any is false, the correction is not autonomous:

1. it is inside the authorized scope;
2. it is inside the granted authority;
3. the correction changes no normative decision;
4. it requires no RFC;
5. it requires no ADR;
6. it changes no Protocol;
7. it changes no payload;
8. it changes no authority;
9. it changes no lifecycle or state machine;
10. there is sufficient evidence to determine the correction;
11. the correction can be verified reproducibly.

When all hold:

```text
DETECT → DIAGNOSE → CORRECT → VERIFY → REVALIDATE → CONTINUE
```

**The finding's own lifecycle state is never written by the host.** The transition
`open → partially-resolved / resolved / deferred / superseded` is a **human
decision with evidence** (CL-8; ADR-16 `AU-3`). SAE pre-authorizes the *action of
correcting*; it does not transfer the *resolution*. This is the operative reading
of "autonomy ⊆ granted authority": the host executes authority it was granted, it
does not acquire the authority to declare the problem settled.

A finding is never marked resolved because the host believes it is resolved.
Evidence is required — and the resolution itself is the human's record.

### 6.1 Blocked findings do not block independent work

```text
Change
 ├── Task A → corrected, verified
 ├── Task B → corrected, verified
 ├── Task C → requires RFC → blocked (preserved + escalated)
 └── Task D → independent, inside the scope → CONTINUE
```

The host must:

1. preserve the evidence of the blocked branch;
2. record why that branch stopped;
3. **not** widen the scope to work around it;
4. continue with independent authorized work when it is safe to do so.

A deferral is recorded, never converted into an implicit authorization, and never
authorizes the deferred action itself.

## 7. Recovery

A recoverable error inside the scope continues:

```text
failure → diagnose → correct / retry → verify → continue
```

The same envelope binds the recovery. A recovery that needs a new scope, new
authority, an RFC, an ADR, a Protocol change or a payload change **stops**.
Recovery and retries are never hidden: they are recorded as evidence like any
other step, and a recovery is not a redefinition of the original plan.

## 8. Human boundary

The human remains exclusively the authority for:

- authorizing scope, and authorizing scope changes;
- accepting/rejecting normative decisions;
- resolving authority conflicts;
- authorizing an RFC;
- authorizing an ADR when it applies;
- authorizing Protocol changes;
- accepting/rejecting architecture changes;
- authorizing release;
- authorizing promotion;
- aborting the Change;
- resolving anything explicitly escalated;
- the transition of state of a finding.

The host **cannot** turn a `STOP` into a `CONTINUE` by its own inference.

## 9. Documentation and Roadmap impact

Both reuse the existing mechanisms
(`.agents/policies/validation-closure.md` §5.1/§5.2); SAE adds no determination
and changes neither.

The host may update documentation when the Change is authorized to do it,
`Documentation Impact = REQUIRED`, the update derives directly from the work
executed, a clear source of truth exists, and no additional normative decision is
required. Documentation is **not** updated merely because it "seems convenient",
and an update that requires a normative decision **stops**.

`Roadmap Impact = REQUIRED` does **not** mean "always edit `ROADMAP.md`": the
obligation is to reconcile the operational state in the artifact that owns it.
Work generated inside the Change's own authority is recorded and reconciled; work
that needs additional authorization is recorded as pending, and the host stops
only where the boundary actually is.

## 10. Evidence

Each autonomous cycle must leave enough evidence to reconstruct: what was
observed; what state was reconstructed; what was derived; what action was taken;
**which authority permitted it**; which worker executed; what result it produced;
what was verified; what was corrected; what was revalidated; why the host
continued; and why it stopped, if it stopped.

No new tracing system is created: the host records all of it in its existing
journal, delegations and Worker Results (`.project/orchestrator/`), and the
durable governance record stays in the plan artifact, written only through the
existing plan-authorized record writer. Each iteration record carries the frontier
verdict (`autonomy`): the action considered, its class, the scope verdict, the
authority, the disposition and the stop condition.

## 11. Execution summary and the autonomy metric

The plan/run records the following, when applicable, derived from evidence that
already exists:

```text
authorized_steps
autonomous_steps
human_operational_interventions
human_authority_decisions
findings_detected
findings_autonomously_corrected
findings_escalated
recoveries
stop_conditions
deferred_branches
```

The two human counts are **strictly distinct** and are never merged:

```text
human_operational_intervention   a step the host could not conduct;
                                 the cost of incomplete autonomy.
human_authority_decision         a decision that exceeds the granted autonomy;
                                 the boundary working as designed. NOT an
                                 autonomy failure.
```

`runtime/orchestrator/autonomy.py:summarize_autonomy` derives the summary from the
journal and the Worker Results; the run report carries it. It is a **view**, not a
tracking system: no new metric store, no database, no registry.

The metric answers one question:

> How much authorized work did the host execute without human operational
> intervention?

Reported as `autonomous_steps / authorized_steps`. With no authorized step the
ratio is **N/A**, never `0` and never a perfect score, so an empty run cannot look
like success. The Change is never optimized to obtain a high number: **the metric
observes real autonomy, it does not incentivize it.**

## 12. Declared limits

- SAE grants no authority. Every verdict cites the existing authority the action
  executes under.
- The frontier is a **derivation**, not a state: no `next_state`, no lifecycle
  state, no registry, no entity and no second representation of the change.
- The gate is **opt-in** (`--sae`): without it the host behaves exactly as before
  this policy existed. That is deliberate — the frontier is additive.
- Determinism is the guarantee: same envelope + same candidates ⇒ same result.
  `runtime/orchestrator/autonomy.py` is a pure function (no filesystem, clock,
  branch, CWD or cache).
- The classification of a finding as autonomously correctable rests on declared
  facts (evidence present, verification reproducible). The host never assumes a
  condition it cannot establish; it stops instead.
- No new mechanism exists for metrics, tracing, tracking, identity or storage. If
  a future need requires one, it is an architecture decision and stops at §5.
