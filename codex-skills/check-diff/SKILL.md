---
name: check-diff
description: Audit a branch, pull-request range, commit range, staged changes, or working-tree diff for defects and regressions introduced by that change. Use when the user explicitly invokes $check-diff or requests this named change review; inspect surrounding context as needed but leave broad repository health to $check-code.
---

# check-diff

Audit the **selected change**: determine whether this branch, commit range, staged work, or working-tree diff introduces defects, regressions, unsafe behavior, misleading success, or missing focused verification. This lane owns what the change caused. Whole-repository implementation health belongs to `$check-code`.

## Step 0 — Establish intent and scope

Identify what the change is supposed to accomplish from the user's request, linked issue or pull request when available, repository instructions, commit messages, tests, and the diff itself. State the intended behavior and exact review surface before judging it.

Select the diff in this order:

1. Use the user's explicit branch, pull request, baseline, or commit range.
2. For a branch review, compare the local merge base with the intended target branch to `HEAD`.
3. For current work, include staged, unstaged, and untracked files that belong to the requested change.

Never fetch, pull, switch branches, or change repository state to manufacture a baseline. If no reliable baseline or meaningful diff exists, return `BLOCKED`, explain what is missing, and request the exact range. Never substitute a whole-repository audit.

## Review priorities

**Correctness and regressions:** broken behavior, edge cases, invalid assumptions, incomplete wiring, incompatible interfaces, platform differences.
**Failure behavior:** swallowed errors, misleading success, partial failure, cleanup, cancellation, retries, timeouts, rollback, corrupted state.
**Security and data safety:** newly exposed trust boundaries, injection, authorization gaps, secret exposure, unsafe filesystem or process behavior, data loss.
**User-visible impact:** behavior that no longer matches the stated goal, tests, documentation, or established product behavior.
**Verification:** missing or weakened tests for meaningful changed behavior, checks that do not exercise production paths, failing focused checks.
**Change quality:** unnecessary complexity, duplication, dead code, or speculative abstraction introduced by the diff when it creates concrete maintenance or correctness risk. Style-only preferences are not findings.

## Workflow

1. Read repository instructions and inspect `git status`, branch state, and the selected diff without changing them.
2. State the exact baseline, target, and inclusion of committed, staged, unstaged, and untracked work.
3. Read the complete diff before forming findings.
4. Inspect enough surrounding callers, callees, tests, types, configuration, and history to understand changed behavior. Root-cause review is in scope; unrelated repository auditing is not.
5. Trace changed inputs through outputs, side effects, persistence, and failure paths.
6. Run the narrowest existing tests, type checks, lint, build, or focused reproduction that can confirm or reject suspected defects. Never install dependencies or modify code to make checks pass.
7. Report only defects introduced or materially exposed by the selected change. Mention a pre-existing issue only when it blocks evaluation, label it out of scope, and leave broad follow-up to `$check-code`.
8. Inspect repository state after validation and report any generated artifacts or changes.

## Evidence and coverage

Prefer findings anchored to changed lines. An unchanged location is acceptable only when the diff newly makes that existing path reachable or unsafe; explain the causal link. Prior logs, screenshots, review comments, supplied artifacts, and user-provided runtime evidence can confirm a defect when provenance, age, and revision mapping are reliable. Otherwise classify it as `LIKELY RISK` until reproduced.

Review every meaningful changed file. Generated, vendored, lock, snapshot, or binary changes may be inspected using the appropriate summary or integrity check rather than line-by-line review. If diff size, unavailable tooling, missing history, or generated content prevents material coverage, state the gap and do not return `PASS`.

## Output

Follow the audit contract. Additionally report:

- intended change and exact diff reviewed;
- committed, staged, unstaged, and untracked coverage;
- focused verification executed;
- coverage gaps or out-of-scope pre-existing blockers;
- a remediation prompt limited to change-caused findings, with exact checks to rerun in the separate correction session.

## Subagents

Use `reviewer` when the diff is substantial enough to benefit. Use `explorer` only when changed-flow mapping is complex. A subagent claim is never evidence—verify it against the repository, de-duplicate findings, and preserve the diff boundary.


---

## Audit Contract (shared, identical across all check skills)

**Audit-only.** This skill never: edits source files, repairs findings, installs dependencies, commits, pushes, publishes, deploys, changes configuration, or claims something works without executed evidence. If a fix is obvious, it goes in the remediation prompt, not into the repo.

**Results:** `PASS` | `PASS WITH RISKS` | `FAIL` (`check-diff` may also return `BLOCKED` when no reliable review target exists).

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

**Result thresholds:** `FAIL` when a confirmed defect breaks the change's stated purpose or any confirmed `CRITICAL` or `HIGH` defect exists. `PASS WITH RISKS` when findings are limited to lower-severity defects, likely risks, or verification gaps. `PASS` only when the meaningful diff was covered, primary verification ran, and no actionable findings remain.

**Report structure:**

```
RESULT: PASS | PASS WITH RISKS | FAIL | BLOCKED
Diff reviewed: <intended change, exact baseline and target, included working-tree surfaces>
Verified: <what was actually executed and confirmed>
Not verified: <what was not, and why>

Findings (severity-ordered, schema above)

REMEDIATION PROMPT
<ready-to-paste prompt for a separate correction session, scoped to the findings,
 including exact checks to rerun after remediation>
```

**No padding.** No generic essays, no restating review areas that produced nothing, no style nits presented as defects, and no findings invented to look thorough. Zero findings is a valid, reportable outcome; omit the remediation prompt when there is nothing to remediate.
