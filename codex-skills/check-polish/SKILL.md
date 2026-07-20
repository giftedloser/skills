---
name: check-polish
description: Audit a product interface for UI and UX quality, responsiveness, accessibility, and interaction defects by running it. Use when the user explicitly invokes $check-polish or requests this named interface audit; return NOT APPLICABLE for repositories without a UI.
---

# check-polish

Audit UI, UX, responsiveness, accessibility, and interaction quality of the product's interface.

## Applicability gate

Runs only when the repository contains a user interface. For non-UI repositories: `RESULT: NOT APPLICABLE`, one line stating why, stop. **Never invent UI findings.**

## Execution is the primary path

Use available browser or app execution capabilities such as the in-app browser, Chrome control, Windows computer use, or Playwright. Run the product and interact with it using disposable test data and non-production accounts. Static review of components and styles is the fallback only when the product cannot start or requires unavailable auth/dependencies; fallback findings are labeled as unexecuted and the result caps at `PASS WITH RISKS`.

## Audit areas

**Visual:** spacing, typography, hierarchy, alignment, density, contrast, consistency, component reuse, icon consistency, color use, clipping, overflow.
**Layout:** window resizing, viewport changes, responsive behavior, DPI scaling, zoom, min/max sizes, long text, empty content, dense content, localization pressure.
**Interaction states:** hover, focus, active, selected, disabled, loading, empty, success, warning, failure, destructive confirmation.
**Accessibility:** keyboard navigation, focus visibility, semantic structure, labels and accessible names, contrast, reduced motion, screen-reader implications, target sizes.
**Product behavior:** discoverability, feedback, progress, error recovery, destructive-action clarity, consistency, navigation, text clarity, unnecessary friction.
**Desktop apps:** title bar, window controls, tray, startup state, resize, DPI, native conventions, modal behavior, focus restoration.

## Workflow

1. Identify supported UI surfaces.
2. Launch the application.
3. Exercise primary workflows.
4. Test relevant viewports or window sizes (desktop + narrow where relevant).
5. Walk the interface by keyboard only.
6. Inspect loading, empty, error, and disabled states.
7. For web frontends: check browser console errors, failed network requests, layout overflow, focus behavior.
8. Compare repeated components and interactions for consistency.
9. **Separate defects from taste.** A defect breaks a rule the product itself established or a platform convention; a redesign preference is `INFORMATIONAL` at most, or omitted.

## Minimum interaction matrix

Always exercise the primary workflow, keyboard navigation, focus visibility, loading, empty, error, disabled states, and resizing at the smallest supported surface. For web interfaces, also test desktop and narrow viewports, browser zoom, reduced motion when relevant, console errors, and failed network requests. For Windows desktop interfaces, also test minimum, normal, and maximized windows; 100%, 150%, and 200% DPI when available; modal focus restoration; and relevant title-bar, tray, and native-window behavior. Mark unavailable matrix cells as verification gaps rather than silently skipping them.

## React Doctor

React projects only, supporting evidence only. Never replaces visual and interaction testing.

## Output

Contract report structure (with `NOT APPLICABLE` available), plus per finding the affected screen or interaction. End with: strongest UI qualities (brief, honest), highest-priority polish issues, and a remediation prompt naming the exact views and interactions to retest.

## Subagents

`ui-polisher` when the UI is substantial enough to benefit. `explorer` only when UI flow mapping is complicated.


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
