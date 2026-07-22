---
name: check-work
description: Verify that a requested product or feature is genuinely implemented and works end to end from the user's perspective. Use when the user explicitly invokes $check-work or requests this named behavioral audit; run the real product and verify user-visible results.
---

# check-work

Determine whether the explicitly requested workflows **work end to end from the user's seat.** This lane owns user-visible behavior. Keep implementation quality separate and defer internal correctness, concurrency, and reliability analysis to `$check-code`.

## Workflow

### 1. Establish expected behavior

Sources, in order: the user's stated goal, repository AGENTS.md, README, specs, issues, existing tests, and the product's own UI labels and claims. What the product *advertises* is the bar it is audited against.

Prior logs, screenshots, recordings, supplied artifacts, and user-provided runtime evidence can confirm a defect when they directly demonstrate the failure, identify the affected revision or artifact, and remain consistent with current code. Label their provenance and age. If freshness, authenticity, or revision mapping is uncertain, classify the finding as `LIKELY RISK` until reproduced.

### 2. Map the flow

For each requested workflow, trace the full chain: user action → UI handler → application state → backend command or API → execution logic → result handling → persisted state → user-visible result. A break anywhere in the chain is a finding.

### 3. Hunt incomplete behavior

On the requested workflow paths, search for: `TODO`, `FIXME`, `placeholder`, `mock`, `stub`, `fake`, `simulated`, hardcoded return values, disabled controls, empty handlers, swallowed errors, success returned before work completes, unreachable features, unimplemented commands, fake progress indicators.

### 4. Run the product

Use available execution capabilities such as the in-app browser, Chrome control, Windows computer use, or Playwright. Running the product is the defining verification. Use disposable test data and non-production accounts; never modify production systems or real user data without explicit authorization. Verify the requested workflows, relevant failure behavior, real output, logs, process exit status, saved state, and reload behavior. If meaningful behavioral verification cannot run, use static or supplied evidence as far as it reaches and return `BLOCKED` unless that evidence directly proves a defect.

### 5. Assess tests

Do tests exercise production code, verify behavior (not implementation trivia), cover important failures, and detect regressions? Snapshot-only and mocked-success suites are findings, not coverage. Never weaken a test to make it pass — a failing test is evidence.

### 6. Compare claims to reality

Classify each requested workflow as: `WORKING`, `PARTIAL`, `BROKEN`, or `UNVERIFIED`.

## Output

Follow the audit contract and report `MODE`. Include:

| Requested workflow | Status | Evidence |
|---|---|---|
| `<workflow>` | `WORKING | PARTIAL | BROKEN | UNVERIFIED` | `<executed or supplied proof>` |

Return `BLOCKED` when meaningful behavioral verification is unavailable. The remediation prompt, when needed, must name the exact workflows to re-exercise.

## Subagents

`explorer` for complicated flow tracing. `reviewer` when regression analysis materially helps. No unnecessary fan-out.


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
