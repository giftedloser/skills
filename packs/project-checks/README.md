# Project Checks

Seven focused audit skills plus one productive repository-polishing skill. Codex routes the narrowest match from natural intent; explicit `$name` remains an override.

## Included skills

| Skill | Owns |
|---|---|
| `$check-diff` | Defects and repository-hygiene problems introduced by a selected change |
| `$check-work` | Real end-to-end user-visible behavior |
| `$check-code` | Implementation correctness, reliability, data integrity, and maintainability |
| `$check-sec` | Practical security defects and unsafe trust assumptions |
| `$check-performance` | Measured bottlenecks and quantified expected benefits |
| `$check-polish` | UI, UX, responsiveness, accessibility, and interaction quality |
| `$check-release` | One candidate's release readiness with GO, GO WITH RISKS, NO-GO, or decision unavailable |
| `$repo-polisher` | Evidence-backed repository documentation, metadata, templates, and hygiene improvements |

## Audit contract

The checks report `PASS`, `PASS WITH RISKS`, `FAIL`, `BLOCKED`, or `NOT APPLICABLE`, with mode `EXECUTED`, `STATIC ONLY`, or `SUPPLIED EVIDENCE`. Every finding is a `CONFIRMED DEFECT`, `LIKELY RISK`, or `VERIFICATION GAP` backed by evidence.

They never edit source, install dependencies, commit, push, publish, deploy, or trigger release automation.

Audit skills route only on a clear request to audit. Ambiguous mentions of speed, security, shipping, polish, or correctness do not trigger them, and they never run as an automatic suite. `$repo-polisher` may route on a direct request to improve repository presentation and can apply safe documentation and hygiene changes.

## Install this pack

Extract `dist/GiftedLoser-Project-Checks.zip` and copy the eight skill folders into `~/.codex/skills`. Start a fresh Codex task so automatic routing and explicit overrides use the new definitions.
