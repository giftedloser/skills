# GiftedLosers Check Skills

A personal set of on-demand Codex skills for turning broad requests such as “review your work,” “make it secure,” or “is this ready to release?” into focused, evidence-based technical checks.

## Skills

- `$project-init` — initialize a new project or safely normalize an existing repository.
- `$check-diff` — review a branch, commit range, staged work, or working-tree diff.
- `$check-work` — prove that a feature works end to end from the user's perspective.
- `$check-code` — audit correctness, reliability, maintainability, and production readiness.
- `$check-sec` — audit practical security defects and unsafe trust assumptions.
- `$check-performance` — investigate performance using measurements rather than guesses.
- `$check-polish` — audit UI, UX, responsiveness, accessibility, and interactions.
- `$check-release` — provide a GO or NO-GO decision for build and distribution readiness.

## How to use them

Start a fresh Codex task in the repository and explicitly invoke the relevant skill, for example:

```text
$check-diff
```

The `check-*` skills are audit-only. They report evidence and produce a focused remediation prompt without changing the repository.

Recommended workflow:

1. Run the relevant check in a dedicated audit task.
2. Paste its remediation prompt into a separate correction task.
3. Rerun the same check in a fresh task to verify the corrections.

Use only the lane that matches the current concern. There is no requirement to run every check.

## Installation

Copy the folders inside `codex-skills` into your personal Codex skills directory:

```text
C:\Users\<you>\.codex\skills
```

Then start a fresh Codex task so the skill catalog refreshes. The included ZIP contains the same eight skills.

`check-suite` is intentionally excluded.
