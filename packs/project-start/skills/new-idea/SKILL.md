---
name: new-idea
description: Pressure-test a rough project idea and supplied conversations, notes, mockups, or planning files; expose contradictions, missing decisions, unnecessary scope, weak value, and feasibility risks honestly; ask focused questions only when needed; and produce an approved docs/PROJECT.md handoff for $project-init. Use only when the user explicitly invokes $new-idea.
---

# new-idea

Turn a rough idea and any existing material into an honest, internally consistent project definition. The goal is not to sell the idea back to the user. Determine whether it deserves to become a project, what must change, and what `$project-init` should receive.

This skill may create or update only `docs/PROJECT.md`. It never writes application code, scaffolds a repository, initializes Git, commits, publishes, creates `AGENTS.md` or `CLAUDE.md`, or manufactures a changelog.

## 1. Read before asking

Inspect the user's supplied conversations, notes, documents, mockups, screenshots, and existing project files first. Treat AI-generated material as claims to evaluate, not accepted truth. Preserve source files and identify disagreements between them.

If the evidence already answers a question, do not ask it again. If no material exists, start from the user's description.

## 2. Restate the idea

Summarize in plain language:

- the problem;
- intended users;
- proposed solution and value;
- primary user workflows;
- stated constraints and preferences;
- assumptions currently being made.

Ask the user to correct the summary only when a mistaken interpretation would change the project.

## 3. Challenge it

Review the idea with direct, specific reasoning:

**Value:** whether the problem is real, the intended user benefits, and the proposed solution addresses the stated problem.

**Consistency:** contradictions between goals, requirements, workflows, constraints, mockups, and source materials.

**Scope:** unnecessary features, missing essentials, hidden complexity, premature architecture, and the smallest version that proves value.

**Feasibility:** technical dependencies, platform limits, data needs, external services, permissions, operational burden, maintenance, and release constraints.

**Failure and trust:** important error paths, destructive behavior, privacy, security, abuse, recovery, and user-data implications.

**Experience direction, when a UI exists:** what the product should feel like, primary hierarchy and interaction model, accessibility and responsive expectations, useful references, and specific patterns the user wants to avoid. Translate vague preferences such as "no AI slop" into observable design constraints; do not invent a generic anti-pattern checklist.

State plainly when the idea is strong, workable only with changes, not ready, or bad as proposed. Do not force optimism, a score, or implementation.

## 4. Resolve material gaps

Discuss contradictions, blockers, and decisions that would materially change the outcome before finalizing the handoff. Ask one question at a time. For each question, explain why it matters and give a recommended answer with its tradeoff when one is defensible.

Do not grill the user for optional details, preferences that can safely wait, or answers already present in the evidence. When a decision can remain open without corrupting the MVP, record it instead of blocking.

## 5. Decide readiness

Use exactly one handoff status:

- `READY FOR PROJECT-INIT` — the project is coherent enough to initialize.
- `NEEDS DECISIONS` — named decisions must be resolved before initialization.
- `DO NOT BUILD YET` — the idea has a fundamental value, feasibility, safety, or consistency problem.

Explain the status with evidence. A bad result is valid. When a smaller or materially different direction is better, recommend it without silently replacing the user's idea.

## 6. Write the handoff

After material issues have been discussed, create or update `docs/PROJECT.md`. Preserve an existing handoff unless the user agrees to the substantive changes. Scale detail to the project; a small utility should receive a short brief, not a ceremonial PRD.

Use applicable sections only:

```md
# Project

Status: READY FOR PROJECT-INIT | NEEDS DECISIONS | DO NOT BUILD YET

## Executive assessment
## Problem and intended users
## Proposed solution and value
## Primary user workflows
## Goals and non-goals
## MVP scope
## Requirements and acceptance criteria
## Experience direction
### Desired experience
### Avoid
### References
## Constraints and dependencies
## Risks and failure modes
## Assumptions and decisions
## Open decisions
## Release definition
## Recommended verification lanes
## Project-init handoff
```

Create additional files under `docs/specs/` only when the user explicitly requests them or one genuinely independent, complex subsystem cannot be expressed clearly in `PROJECT.md`. Do not create overlapping PRD, requirements, plan, and specification documents by default.

## Completion

Report the verdict, strongest reason to build or not build, material decisions made, unresolved items, and the path written. When status is `READY FOR PROJECT-INIT`, end with this exact next step:

```text
$project-init

Use docs/PROJECT.md as the source of truth.
```
