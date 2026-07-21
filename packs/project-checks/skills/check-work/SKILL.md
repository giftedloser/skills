---
name: check-work
description: Verify that a requested product or feature is genuinely implemented and works end to end from the user's perspective. Use when the user explicitly invokes $check-work or requests this named behavioral audit; run the real product and verify user-visible results.
---

# check-work

Determine whether the requested product or feature is **actually implemented and works end to end, from the user's seat.** This lane owns end-to-end user-visible behavior: does the thing the UI/CLI/docs claim exist, run, and produce real results. Implementation soundness (correctness, concurrency, reliability internals) belongs to `$check-code` — do not duplicate its territory; note a suspicion in one line and move on.

## Workflow

### 1. Establish expected behavior

Sources, in order: the user's stated goal, repository AGENTS.md, README, specs, issues, existing tests, and the product's own UI labels and claims. What the product *advertises* is the bar it is audited against.

Prior logs, screenshots, recordings, supplied artifacts, and user-provided runtime evidence can confirm a defect when they directly demonstrate the failure, identify the affected revision or artifact, and remain consistent with current code. Label their provenance and age. If freshness, authenticity, or revision mapping is uncertain, classify the finding as `LIKELY RISK` until reproduced.

### 2. Map the flow

For each primary feature, trace the full chain: user action → UI handler → application state → backend command or API → execution logic → result handling → persisted state → user-visible result. A break anywhere in the chain is a finding.

### 3. Hunt incomplete behavior

Search for: `TODO`, `FIXME`, `placeholder`, `mock`, `stub`, `fake`, `simulated`, hardcoded return values, disabled controls, empty handlers, swallowed errors, success returned before work completes, unreachable features, unimplemented commands, fake progress indicators.

### 4. Run the product

Use available execution capabilities such as the in-app browser, Chrome control, Windows computer use, or Playwright. **Running the product is the primary path, not optional.** Use disposable test data and non-production accounts; never modify production systems or real user data without explicit authorization. Verify: startup, primary workflows, failure behavior, real output, logs, process exit status, saved state, reload behavior. Fallback to static analysis only when the product genuinely cannot start or requires unavailable auth/dependencies — and in that case the overall result caps at `PASS WITH RISKS` regardless of how clean the code looks.

### 5. Assess tests

Do tests exercise production code, verify behavior (not implementation trivia), cover important failures, and detect regressions? Snapshot-only and mocked-success suites are findings, not coverage. Never weaken a test to make it pass — a failing test is evidence.

### 6. Compare claims to reality

Classify every advertised behavior as: fully working, partially working, disconnected (UI exists, backend doesn't), missing, or unverifiable.

## Output

Follow the contract report structure. Additionally list: verified workflows, unverified workflows, and per-workflow status from step 6. The remediation prompt must name the exact workflows to re-exercise after fixes.

## Subagents

`explorer` for complicated flow tracing. `reviewer` when regression analysis materially helps. No unnecessary fan-out.


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
