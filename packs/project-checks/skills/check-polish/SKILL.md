---
name: check-polish
description: Audit a product interface for UI and UX quality, responsiveness, accessibility, and interaction defects by running it. Use when the user explicitly invokes $check-polish or requests this named interface audit; return NOT APPLICABLE for repositories without a UI.
---

# check-polish

Audit UI, UX, responsiveness, accessibility, and interaction quality of the product's interface.

## Applicability gate

Runs only when the repository contains a user interface. For non-UI repositories, return `RESULT: NOT APPLICABLE`, explain why in one line, and stop. This is the local `NOT APPLICABLE` variant. Never invent UI findings.

## Execution is the primary path

Use available browser or app execution capabilities such as the in-app browser, Chrome control, Windows computer use, or Playwright. Run the product and interact with it using disposable test data and non-production accounts. When execution is unavailable, report `MODE: STATIC ONLY`; decisive static evidence may prove a defect, but missing interaction proof returns `BLOCKED`, not a visual pass.

## Coverage

**CORE:** requested primary workflow, keyboard operation, focus visibility and movement, relevant error state, and minimum supported window or viewport size.

**CONDITIONAL:** DPI scaling, browser zoom, mobile layout, tray behavior, reduced motion, network failure, modal focus restoration, additional breakpoints, long or localized text, and platform-specific window behavior. Test only the conditions applicable to the requested interface.

Across applicable coverage, inspect visual hierarchy, spacing, typography, contrast, clipping, overflow, component consistency, interaction feedback, loading/empty/error/disabled states, accessible names, semantics, target sizes, and recovery behavior.

## Workflow

1. Identify the requested surface and applicable CORE and CONDITIONAL coverage.
2. Launch the application when possible and exercise the requested workflow.
3. Complete CORE coverage, then only applicable CONDITIONAL checks.
4. For web interfaces, inspect console errors, failed network requests, layout overflow, and focus behavior when runtime access exists.
5. Capture screenshots for visual findings whenever execution is available; identify the tested viewport or window size and interaction.
6. Separate defects from taste. A defect violates accessibility, established product behavior, or a platform convention; personal redesign preference is `INFORMATIONAL` at most or omitted.

## React Doctor

React projects only, supporting evidence only. Never replaces visual and interaction testing.

## Output

Follow the audit contract. Report CORE and CONDITIONAL coverage separately and identify the affected screen, interaction, viewport, and screenshot for each visual finding when available. Name the exact views and interactions to retest after remediation.

## Subagents

`ui-polisher` when the UI is substantial enough to benefit. `explorer` only when UI flow mapping is complicated.


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
