# Project Checks

Seven focused, audit-only Codex skills for building confidence without letting the checker silently repair what it grades.

## Included skills

| Skill | Owns |
|---|---|
| `$check-diff` | Defects and repository-hygiene problems introduced by a selected change |
| `$check-work` | Real end-to-end user-visible behavior |
| `$check-code` | Implementation correctness, reliability, data integrity, and maintainability |
| `$check-sec` | Practical security defects and unsafe trust assumptions |
| `$check-performance` | Measured bottlenecks and quantified expected benefits |
| `$check-polish` | UI, UX, responsiveness, accessibility, and interaction quality |
| `$check-release` | Repository and product release readiness with a final GO/NO-GO |

## Audit contract

The checks report `PASS`, `PASS WITH RISKS`, or `FAIL`; `$check-diff` may return `BLOCKED`, and `$check-polish` may return `NOT APPLICABLE`. Every finding is a `CONFIRMED DEFECT`, `LIKELY RISK`, or `VERIFICATION GAP` backed by evidence.

They never edit source, install dependencies, commit, push, publish, deploy, or trigger release automation.

## Install this pack

Extract `dist/GiftedLoser-Project-Checks.zip` and copy the seven skill folders into `~/.codex/skills`. Start a fresh Codex task before invoking them.
