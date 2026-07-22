---
name: project-init
description: Do not use for discussion-only ideation or ordinary feature implementation in an established project. Use when the user asks to create, scaffold, initialize, or normalize a software repository without destroying valid work. New repositories may receive an initial Git commit, but never publish or change global Codex configuration. Explicit $project-init always invokes it.
---

# project-init

Initialize a new software project from an empty directory, or normalize an existing repository, without destroying valid work. This is the **only skill in this repository permitted to scaffold or mutate implementation by default**; `$new-idea` may write only `docs/PROJECT.md`. It never modifies global Codex configuration, approval rules, global agents, or user-managed files above the repository root. Repository-local dependency operations may use the package manager's normal external cache, but never install global packages or change global package-manager configuration unless explicitly requested.

## Inputs

Determine from the request and the directory itself: project goal, target platform, preferred stack if specified, empty vs existing directory, whether Git should be initialized, whether GitHub should be created or connected (visibility if specified), MVP boundary, explicit constraints. Do not interrogate the user when the goal is already clear. Ask only for decisions that change the outcome.

## Planning mode

When the user asks for a plan, simulation, dry run, or read-only review, inspect safely and describe the exact proposed files, commands, Git actions, and verification without performing them. Label unexecuted commands and outcomes as proposed or unverified. Otherwise, perform the requested initialization normally.

## Workflow

### 0. Optional project handoff

Look for `docs/PROJECT.md`, then `PROJECT.md`, before planning or asking questions. If neither exists, use the current request and directory exactly as normal; `$new-idea` is optional. If both exist and materially differ, stop and ask which is authoritative.

When a handoff exists, read it fully and use it as the approved product intent while continuing to verify technical claims against repository reality. Apply its status deterministically:

- `READY FOR PROJECT-INIT` — proceed, asking only about material conflicts or missing implementation decisions.
- `NEEDS DECISIONS` — resolve the named blocking decisions before changing the project.
- `DO NOT BUILD YET` — stop initialization and report the stated blockers.

Surface contradictions between the handoff, user request, and existing repository before changing files. Never silently rewrite the handoff's scope or decisions.

### 1. Inspect

Before touching anything, determine: existing files, Git state (initialized, remote, branch, uncommitted changes), detected language/framework, package manager, build system, test framework, lint/format tooling, existing docs, existing AGENTS.md or `.codex/` config.

### 2. Protect

Never overwrite working source. Never replace established conventions without evidence they are broken. Preserve unrelated and user-owned changes. No destructive Git recovery. Never delete files because they "look unused."

### 3. Structure

**Empty directory:** smallest correct structure for the requested project. No speculative architecture, no unnecessary dependencies, no placeholder systems, no abstraction the MVP doesn't need. Direct, concrete implementation.

**Existing project:** retain current architecture unless clearly broken or incompatible with the stated goal. Fill genuine setup gaps only. No redesign without justification stated to the user.

Organize files by lifecycle, not by who created them. Preserve equivalent established paths; otherwise use ignored `scratch/` for disposable work, ignored `html-mocks/` for temporary HTML prototypes, and ignored tool-native output paths or `artifacts/test-results/` for generated test evidence. Promote intentional references to tracked locations such as `docs/mocks/` or `docs/reports/`; keep durable project files such as `CHANGELOG.md` tracked.

### 4. AGENTS.md

Create or improve the repository AGENTS.md with only real, verified content: project purpose, actual stack, important architecture, real build/test/lint/type-check/format/dev commands, packaging or release command when applicable, constraints, file-placement and scratch conventions, caution areas, definition of done, verification expectations. When a project handoff exists, identify it as the product source of truth and require implementation tasks to read it without duplicating the full document. Every command listed must exist and be verified in step 6. No generic filler — if a section would be boilerplate, omit it.

### 5. Repo-local Codex config (only when justified)

`.codex/config.toml`, `.codex/rules/*.rules`, `.codex/agents/*.toml` only when the project has a real recurring need. Rules must be narrow, project-specific, based on commands that exist, limited to trusted repository work. Never broad, never global. Do not create project agents unless a recurring project-specific need cannot be served by built-in generic workers or the built-in read-heavy investigation role.

### 6. Commands

Derive commands from package files, manifests, task files, CI, and docs. Verify each documented command actually resolves (dry-run or `--help` where full execution is expensive). **Never invent commands.** A command that cannot be verified does not go in AGENTS.md.

### 7. Git

For an empty directory or newly initialized repository: initialize Git when needed, choose an appropriate initial branch, add a sensible `.gitignore`, inspect changes before staging, and create the initial commit. For an existing repository: preserve its history, branch, remotes, and existing ignore rules; add only missing project-appropriate rules and do not create an "initial" or normalization commit unless explicitly requested. Ensure local environment files, disposable scratch and HTML mocks, generated test results, build output, caches, and editor/OS debris are ignored without hiding source, durable documentation, changelogs, or release assets. Check for files already tracked despite the ignore policy; report them and get explicit approval before removing them from the index. Never add or change a remote, push, publish, or deploy unless explicitly requested.

### 8. GitHub

Only when requested. Default new repositories to **private** when visibility is unspecified. Verify the selected account and remote before any operation. No duplicate repo creation, no unrelated files published, push only when authorized.

### 9. Verify proportionately

Confirm the structure builds or parses at the shallowest meaningful level, such as dependency resolution or entry-point compilation. Run only the checks proportionate to the initialization performed. Do not chain an audit skill automatically; a formal behavioral audit requires clear user intent.

## Output

Report: detected prior state, project handoff used or absent, files created, files changed, stack and tooling selected, Git state, GitHub state, commands verified, checks passed, unresolved decisions, and real residual risks.

## Completion criteria

Structure matches the goal and any approved handoff, blocking handoff status was respected, existing work preserved, AGENTS.md contains only real verified instructions, no invented commands, no global Codex changes, failures clearly reported, proportionate verification completed, and residual risk stated.
