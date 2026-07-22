---
name: check-performance
description: Audit actual performance bottlenecks using measured evidence and quantified expected benefits. Use when the user explicitly invokes $check-performance or requests this named performance audit; do not recommend speculative optimization.
---

# check-performance

Audit one named workflow and symptom using **measured evidence.** Require a representative workload and a usable measurement path before treating the audit as executable. Two hard rules distinguish this lane:

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

1. State the named workflow, reported or observable symptom, representative workload, and measurement path.
2. Establish a representative baseline using existing timings or the simplest instrument that produces a useful number.
3. Reproduce the symptom under the same workload.
4. Locate the bottleneck in the named workflow; do not expand into a repository-wide performance audit.
5. Separate measured defects from inferred risks. Unmeasured concerns remain `LIKELY RISK` and are capped at `MEDIUM`.
6. State the expected benefit and smallest justified correction.
7. Repeat the same measurement after remediation; make that measurement the finding's exact recheck.

## Output

Follow the audit contract. Report the workflow, symptom, workload, baseline, bottleneck, expected benefit, and repeat measurement. Return `BLOCKED` when no usable representative measurement can be obtained. Inferred concerns must state their evidence and assumption without invented numbers.

## Subagents

`explorer` for locating hot paths in larger repositories. Specialist delegation only when independent measurement materially helps.


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
