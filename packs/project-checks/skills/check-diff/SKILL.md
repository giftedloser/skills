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
**Repository hygiene:** accidental secrets or local environment files, scratch work, temporary HTML mocks, generated test output, build/cache/editor/OS debris, unexpected binaries, weakened ignore rules, or durable docs and reports placed outside the repository's established structure. Distinguish intentional tracked artifacts from disposable output.

## Workflow

1. Read repository instructions and inspect `git status`, branch state, and the selected diff without changing them.
2. State the exact baseline, target, and inclusion of committed, staged, unstaged, and untracked work.
3. Read the complete diff before forming findings.
4. Compare changed and relevant untracked paths with repository placement and ignore policy; use Git ignore diagnostics when needed.
5. Inspect enough surrounding callers, callees, tests, types, configuration, and history to understand changed behavior. Root-cause review is in scope; unrelated repository auditing is not.
6. Trace changed inputs through outputs, side effects, persistence, and failure paths.
7. Run the narrowest existing tests, type checks, lint, build, or focused reproduction that can confirm or reject suspected defects. Never install dependencies or modify code to make checks pass.
8. Report only defects introduced or materially exposed by the selected change. Mention a pre-existing issue only when it blocks evaluation, label it out of scope, and leave broad follow-up to `$check-code`.
9. Inspect repository state after validation and report any generated artifacts or changes.

## Evidence and coverage

Prefer findings anchored to changed lines. An unchanged location is acceptable only when the diff newly makes that existing path reachable or unsafe; explain the causal link. Prior logs, screenshots, review comments, supplied artifacts, and user-provided runtime evidence can confirm a defect when provenance, age, and revision mapping are reliable. Otherwise classify it as `LIKELY RISK` until reproduced.

Review every meaningful changed file. Generated, vendored, lock, snapshot, or binary changes may be inspected using the appropriate summary or integrity check rather than line-by-line review. Declare `Coverage: FULL` or `Coverage: PARTIAL` and list the exact reviewed range and exclusions. Disclose actual coverage; do not invent a line-count threshold. Partial coverage cannot produce a full `PASS`.

## Output

Follow the audit contract. Additionally report:

- `Coverage: FULL | PARTIAL` and the exact reviewed range;
- intended change and exact diff reviewed;
- committed, staged, unstaged, and untracked coverage;
- focused verification executed;
- coverage gaps or out-of-scope pre-existing blockers;
- findings causally tied to the diff;
- tests only when the diff changes meaningful behavior.

Local outcome rule: return `BLOCKED` when no reliable baseline or meaningful diff exists, or when the defining review cannot run. Partial coverage cannot produce a full `PASS`.

## Subagents

Use `reviewer` when the diff is substantial enough to benefit. Use `explorer` only when changed-flow mapping is complex. A subagent claim is never evidence—verify it against the repository, de-duplicate findings, and preserve the diff boundary.


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
