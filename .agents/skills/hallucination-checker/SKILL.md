---
name: hallucination-checker
description: Confront the factual claims of an artifact against the evidence actually available in the repository or the session (files, prior artifacts, verified outputs). Use when a worker must detect invented facts, phantom paths, or unverified assertions before an artifact is trusted — typically in phase 04-validate-context or 07-verify. Evaluates only; never edits the artifact and never supplies missing facts.
when_to_activate: The delegated phase is 04-validate-context or 07-verify, or the task asks to check an artifact for fabricated or unsupported claims, per `.agents/standards/conduct/ANTI_CIRCUMVENTION.md`.
when_not: The task is to validate an artifact's structure against its contract (use artifact-validator — hallucination-checker verifies CLAIMS against evidence, artifact-validator verifies STRUCTURE against contract), to critique a proposal's approach (use critic), or no artifact with factual claims exists.
---

# Mission

Inventing project facts, user intent, or implementation details is a protocol violation (`.agents/standards/conduct/ANTI_CIRCUMVENTION.md`, "What counts as circumvention"). This skill confronts every load-bearing claim of an artifact with the evidence on disk or in the session and reports which claims are supported, unsupported, or contradicted. It does not fix the artifact — it produces the finding report that lets the delegating phase decide.

---

# Protocol Boundary

This skill assists the Worker inside the phase that delegated it (commonly 04-validate-context or 07-verify). Its output is embedded as a section inside the artifact that governs that phase; the phase contract defines the envelope. On any conflict between this skill and the protocol, the protocol wins. This skill describes a capability; it grants no authority or permissions.

---

# Workflow

1. **Read the artifact** under review and identify its factual claims: file paths, symbols, APIs, behaviors, prior decisions, user statements, test results, tool outputs.
2. **Classify each claim** as checkable (verifiable against the repo or session record) or uncheckable (external knowledge the session cannot confirm).
3. **Gather evidence** for each checkable claim: read the cited file, search for the cited symbol, re-read the cited artifact or user message. Use the actual repository, never memory of it.
4. **Verdict per claim**:
   - SUPPORTED — evidence on disk or in the session confirms it.
   - UNSUPPORTED — no evidence found; the claim may be invented or assumed.
   - CONTRADICTED — evidence exists and says otherwise (quote both).
5. **Flag high-risk patterns**: paths or symbols that do not exist, version numbers not in the manifest, "the user said" with no matching message, test results never run, claims introduced to avoid asking for clarification.
6. **Report**: every UNSUPPORTED or CONTRADICTED claim gets a severity and its evidence (or the failed search that found none).

---

# Rules

- Verify against the real repository and session record; never accept a claim because it sounds plausible.
- No fabricated findings: a claim is UNSUPPORTED only after an actual search; name what you searched.
- Do not modify the artifact under review and do not supply the correct facts — correction belongs to the authoring role.
- Uncheckable claims are reported as such, not silently passed.
- If every claim checks out, say so explicitly and list what was verified — a clean report is a valid result.

---

# Output Format

```markdown
## Hallucination Check

- Artifact: <path or description>
- Claims examined: <n> (checkable: <n>, uncheckable: <n>)

### Findings

| # | Severity | Claim | Verdict | Evidence |
|---|----------|-------|---------|----------|
| 1 | CRITICAL | "config lives in src/settings.toml" | CONTRADICTED | file does not exist; manifest lists `config/app.toml` |

### Uncheckable Claims

- <claim> — requires external knowledge not present in the session

### Verified Without Findings

- <claim or area checked>
```

Severities: CRITICAL (decision or phase transition depends on a false/unsupported claim), MAJOR (claim misleads but is not load-bearing), MINOR (imprecision worth correcting).
