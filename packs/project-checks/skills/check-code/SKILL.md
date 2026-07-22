---
name: check-code
description: Audit implementation correctness, reliability, data integrity, and concrete operational risks in a declared module or three critical paths. Use when the user explicitly invokes $check-code or requests this named code audit; leave end-to-end user-visible behavior to $check-work.
---

# check-code

Audit **implementation soundness** for a declared module or the three most critical changed or high-risk paths. End-to-end behavior belongs to `$check-work`, exploitable security to `$check-sec`, and measured optimization to `$check-performance`.

## Step 0 — Scope first

Use the user's declared module when supplied. Otherwise identify and declare the three highest-value changed or critical paths before reviewing them. State which categories apply; do not expand into an audit of everything.

## Category reference

**Correctness:** edge cases, invalid assumptions, invalid states, off-by-one, overflow/truncation, locale and encoding, path handling, platform differences.
**Concurrency:** races, deadlocks, shared-state errors, double execution, cancellation, thread safety, async lifetimes.
**Reliability:** retries, timeouts, backoff, cleanup, partial failure, rollback, resource/handle leaks, temp file cleanup, interrupted operations.
**Data integrity:** atomic writes, corrupted state, migrations, cache consistency, stale data, partial persistence, invalid serialization.
**Errors and logging:** swallowed errors, silent fallbacks, misleading success, missing context, unusable messages, failure paths that leave bad state.
**Operational maintainability:** duplication, unclear ownership, unnecessary abstraction, or fragile coupling only when it creates a concrete correctness, reliability, or operational risk.
**Incomplete production behavior:** TODO production paths, mocks/placeholders/fakes in production, hardcoded success, disabled validation, temporary shortcuts, partially wired internals.

## Workflow

1. Read repository instructions and declare the requested module or three selected paths.
2. Map each selected path and trace all callers before declaring a root cause.
3. Review correctness and failure handling on those paths.
4. Review concurrency, cancellation, timeout, and cleanup behavior where applicable.
5. Review persistence and data integrity where applicable.
6. Search for incomplete or fake implementation in production paths.
7. Run tests, lint, type checks, and build where available. Command failures are evidence, not obstacles — never modify anything to make them pass.
8. Reproduce important findings at runtime when practical; reproduction upgrades `LIKELY RISK` to `CONFIRMED DEFECT`.
9. Exclude style commentary, generic maintainability advice, exploitable security findings owned by `$check-sec`, and optimization claims without measurement.

## React Doctor

Only when the repository actually uses React, only as supporting evidence. Advisory. Its score is never the result, it never runs on non-React projects, it never replaces repository checks, and its recommendations are not auto-applied — they are triaged like any other input.

## Output

Follow the audit contract. Report the declared module or three selected paths, caller tracing performed, and concrete operational risks. Include the strongest verified implementation property only when it helps explain the result.

## Subagents

`reviewer` for substantial correctness review. `explorer` for codebase mapping. De-duplicate agent findings before reporting.


---

## Audit Contract

**Audit-only.** Do not edit source, repair findings, install dependencies, commit, push, publish, deploy, or change configuration. Repository-native checks may create derived artifacts; inspect state before and after, report generated changes, and never clean or overwrite user work.

Before any work, state:

- `Target:` exact workflow, module, boundary, interface, candidate, or diff.
- `Applicable categories:` what applies and what does not.
- `Primary verification:` the defining proof required for this audit.
- `User restrictions:` read-only, environment, data, credential, or side-effect limits.

**Mode:** `EXECUTED` | `STATIC ONLY` | `SUPPLIED EVIDENCE`.

**Outcome:** `PASS` | `PASS WITH RISKS` | `FAIL` | `BLOCKED` | `NOT APPLICABLE`.

Return `FAIL` when a confirmed defect breaks the defining objective or any confirmed `CRITICAL` or `HIGH` defect exists. Use `PASS WITH RISKS` only for actionable lower-severity defects or explicitly bounded residual risk after defining verification completes.

Return `BLOCKED` when the defining verification cannot run. Never launder missing proof into `PASS WITH RISKS`. Use `NOT APPLICABLE` only when the skill's subject does not exist. `PASS` requires completed defining verification and no actionable findings. Confirmed lower-severity defects require `PASS WITH RISKS`.

Use disposable data and non-production systems. Do not cause destructive or externally visible effects without explicit authorization. Tie evidence to the relevant revision or artifact; label inference as `INFERENCE`.

**Severity:** `CRITICAL` | `HIGH` | `MEDIUM` | `LOW` | `INFORMATIONAL`.

**Classification:** `CONFIRMED DEFECT` | `LIKELY RISK` | `VERIFICATION GAP`.

```text
[SEVERITY] Title
Classification: <classification>
Evidence: <source, execution, artifact, or measurement>
Consequence: <what breaks and for whom>
Correction: <smallest practical correction or required verification>
Recheck: <exact check that proves resolution>
```

Report `RESULT`, `MODE`, scope, verified evidence, unverified items, and only the highest-value findings in severity order. Do not pad the report or recap empty categories. Include a ready-to-paste `REMEDIATION PROMPT` only when actionable findings exist.
