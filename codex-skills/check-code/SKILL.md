---
name: check-code
description: Audit implementation correctness, reliability, data integrity, maintainability, and production readiness. Use when the user explicitly invokes $check-code or requests this named code audit; leave end-to-end user-visible behavior to $check-work.
---

# check-code

Audit **implementation soundness**: correctness, reliability, maintainability, and production readiness of the code itself. End-to-end user-visible behavior belongs to `$check-work` — if a feature is missing or disconnected from the user's perspective, note it in one line and leave it to that lane. This lane owns whether the code that exists is *right*.

## Step 0 — Scope first

Identify which categories apply to this repository and state the scoping decision in the report. A single-threaded script gets no concurrency audit; a stateless tool gets no migration audit. Depth goes to applicable categories.

## Category reference

**Correctness:** edge cases, invalid assumptions, invalid states, off-by-one, overflow/truncation, locale and encoding, path handling, platform differences.
**Concurrency:** races, deadlocks, shared-state errors, double execution, cancellation, thread safety, async lifetimes.
**Reliability:** retries, timeouts, backoff, cleanup, partial failure, rollback, resource/handle leaks, temp file cleanup, interrupted operations.
**Data integrity:** atomic writes, corrupted state, migrations, cache consistency, stale data, partial persistence, invalid serialization.
**Errors and logging:** swallowed errors, silent fallbacks, misleading success, missing context, unusable messages, failure paths that leave bad state.
**Code quality:** duplication, dead code, oversized functions, weak typing, unclear ownership, unnecessary abstraction, speculative architecture, inconsistent conventions, fragile coupling.
**Incomplete production behavior:** TODO production paths, mocks/placeholders/fakes in production, hardcoded success, disabled validation, temporary shortcuts, partially wired internals.

## Workflow

1. Read repository instructions (AGENTS.md, README) and identify the primary architecture.
2. Map critical execution paths.
3. Review correctness and failure handling on those paths.
4. Review concurrency, cancellation, timeout, and cleanup behavior where applicable.
5. Review persistence and data integrity where applicable.
6. Search for incomplete or fake implementation in production paths.
7. Run tests, lint, type checks, and build where available. Command failures are evidence, not obstacles — never modify anything to make them pass.
8. Reproduce important findings at runtime when practical; reproduction upgrades `LIKELY RISK` to `CONFIRMED DEFECT`.

## React Doctor

Only when the repository actually uses React, only as supporting evidence. Advisory. Its score is never the result, it never runs on non-React projects, it never replaces repository checks, and its recommendations are not auto-applied — they are triaged like any other input.

## Output

Contract report structure, plus: the scoping decision, the strongest parts of the implementation (one short paragraph — credit what's genuinely good, no flattery), highest-risk code paths, and a remediation prompt with the exact verification commands to rerun.

## Subagents

`reviewer` for substantial correctness review. `explorer` for codebase mapping. De-duplicate agent findings before reporting.


---

## Audit Contract (shared, identical across all check skills)

**Audit-only.** This skill never: edits source files, repairs findings, installs dependencies, commits, pushes, publishes, deploys, changes configuration, or claims something works without executed evidence. If a fix is obvious, it goes in the remediation prompt, not into the repo.

**Results:** `PASS` | `PASS WITH RISKS` | `FAIL` (check-polish may also return `NOT APPLICABLE`).

**Severity:** `CRITICAL` | `HIGH` | `MEDIUM` | `LOW` | `INFORMATIONAL`.

**Classification:** every finding is exactly one of:
- `CONFIRMED DEFECT` — reproduced or proven from code/execution
- `LIKELY RISK` — strong evidence, not fully reproduced
- `VERIFICATION GAP` — could not be checked; state why

**Finding schema (every finding, no exceptions):**

```
[SEVERITY] Title
Classification: CONFIRMED DEFECT | LIKELY RISK | VERIFICATION GAP
Evidence: file:line references, command output, screenshot, or measurement
Consequence: what breaks and for whom
Correction: specific recommended fix, or for a `VERIFICATION GAP`, the exact verification required (do not apply or execute it)
```

**Evidence hierarchy (strongest first):** repository code with file:line → executed behavior → logs → tests → official documentation → reasoned inference explicitly labeled `INFERENCE`. Never present inference as observation.

**Blocked validation:** if something cannot run, report exactly what could not run, why, the next-best verification performed instead, and the residual uncertainty. A check that could not execute its primary verification cannot return `PASS`. Return `PASS WITH RISKS` when no stronger defect is proven; confirmed evidence may still require `FAIL`.

**Generated outputs:** repository-native checks may create derived build artifacts, caches, logs, or test output. Prefer disposable output locations or a temporary copy when practical. Inspect repository state before and after, report generated changes, and never clean, reset, delete, or overwrite user-owned work to restore the tree.

**Execution safety:** use disposable data, temporary locations, and non-production accounts or services. Never exercise production systems, real user data, or externally visible side effects without explicit authorization.

**Result thresholds:** `FAIL` when a confirmed defect breaks the skill's core objective, any confirmed `CRITICAL` or `HIGH` defect exists, or a release-blocking condition applies. `PASS WITH RISKS` when findings are limited to lower-severity defects, likely risks, or verification gaps. `PASS` only when primary verification ran and produced no actionable findings.

**Report structure:**

```
RESULT: PASS | PASS WITH RISKS | FAIL
Verified: <what was actually executed and confirmed>
Not verified: <what was not, and why>

Findings (severity-ordered, schema above)

REMEDIATION PROMPT
<ready-to-paste prompt for a separate fix session, scoped to the findings,
 including exact checks to rerun after remediation>
```

**No padding.** No generic essays, no restating the audit areas that produced nothing, no findings invented to look thorough. Zero findings is a valid, reportable outcome; omit the remediation prompt when there is nothing to remediate.
