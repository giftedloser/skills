---
name: check-performance
description: Audit actual performance bottlenecks using measured evidence and quantified expected benefits. Use when the user explicitly invokes $check-performance or requests this named performance audit; do not recommend speculative optimization.
---

# check-performance

Audit actual performance bottlenecks using **measured evidence.** Two hard rules distinguish this lane:

1. **No optimization recommendation without a stated expected benefit.** "This could be faster" is not a finding.
2. **No finding above MEDIUM severity without a measurement.** Unmeasured scaling concerns are `LIKELY RISK`, capped at MEDIUM, and labeled inferred.

## Audit areas

**Startup:** cold start, warm start, initialization order, unnecessary or blocking startup work.
**Runtime:** CPU, memory, leaks, render frequency, blocking operations, repeated computation, polling, timers, unnecessary refreshes.
**I/O:** disk reads/writes, network requests, serialization, cache behavior, duplicate requests, large files, chatty IPC, synchronous I/O.
**Frontend:** render loops, unnecessary rerenders, bundle size, large assets, slow lists, layout thrashing, expensive effects, unbounded DOM growth.
**Backend:** hot paths, lock contention, inefficient parsing, excessive spawning, missing batching, poor caching, unbounded queues, unnecessary copies.
**Scaling:** data growth, large repositories, large files, many users, long-running sessions, repeated background work.

## Workflow

1. Identify the performance-sensitive workflows — what does the user actually wait on?
2. Collect existing measurements (CI timings, logs, benchmarks) where available.
3. Measure: startup time, execution time of key operations, memory, CPU, I/O counts. Use the simplest instrument that produces a number (timers, task manager, `Measure-Command`, browser performance panel, bundle analyzer).
4. Inspect likely hot paths in code.
5. Reproduce reported or suspected problems.
6. Separate measured defects from inferred scaling risks in the report — different sections.
7. For every recommended correction, state the expected benefit and the **exact measurement to rerun after the fix** to confirm it.

## Output

Contract report structure, plus per finding: measured vs inferred, affected workflow, expected benefit, and the exact post-fix measurement. Measured findings include the observed numbers. Inferred findings state the evidence and assumption without inventing numbers; quantify them only after measurement. When a reliable numeric benefit forecast is unavailable, state a measurable success target or expected direction plus the measurement that will validate it. End with: measurements performed, measurements unavailable and why, likely highest-value improvements, remediation prompt.

## Subagents

`explorer` for locating hot paths in larger repositories. Specialist delegation only when independent measurement materially helps.


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
