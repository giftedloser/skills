# GiftedLoser Skills


![Skills](https://img.shields.io/badge/skills-10-6d5dfc)
![Packs](https://img.shields.io/badge/packs-3-167d68)
![Invocation](https://img.shields.io/badge/invocation-automatic%20%2B%20explicit-3974c6)
[![License: MIT](https://img.shields.io/badge/license-MIT-c47716)](LICENSE)

GiftedLoser Skills is a collection of personal Codex workflows. Project Start turns an uncertain idea into a well-formed project, Project Checks audits work already done, and Project Polish improves repository presentation and identity.

The skills are built for Codex and are not currently compatible with Claude Code or other agent runtimes.

Each skill is independent. Together they cover the full range from idea to release, but they are not a pipeline and are not meant to run as a sequence. Install the whole collection or only the pack you need, and invoke skills one at a time as the work calls for them.

## From idea to release

![Project lifecycle from idea to release](assets/project-lifecycle.svg)

Describe the result you want. Codex routes the narrowest applicable skill, and audit skills stay silent unless the request clearly asks for an audit. Explicit `$name` invocation remains available as an override. Audits never run as an automatic suite.

## Packs

| Pack | Skills | Purpose |
|---|---|---|
| [Project Start](packs/project-start/README.md) | `$new-idea`, `$project-init` | Challenge the idea, create an approved project handoff, and establish the repository safely |
| [Project Checks](packs/project-checks/README.md) | Seven `$check-*` skills | Audit the change, behavior, implementation, security, performance, interface, and release |
| [Project Polish](packs/project-polish/README.md) | `$repo-polisher` | Improve repository identity, README craft, diagrams, templates, badges, and metadata without changing source behavior |

### Complete bundle

`dist/GiftedLoser-Skills-Complete.zip` contains all ten skills from all three packs. Use it when you want the full idea-to-release workflow plus repository polishing.

The pack ZIPs remain available when you want only one part:

- `dist/GiftedLoser-Project-Start.zip`
- `dist/GiftedLoser-Project-Checks.zip`
- `dist/GiftedLoser-Project-Polish.zip`

## Skills at a glance

| You are thinking... | Use | What you get |
|---|---|---|
| “Is this idea actually worth building?” | `$new-idea` | A candid review of value, contradictions, gaps, scope, feasibility, risks, and experience direction, ending in `docs/PROJECT.md` |
| “Set this project up properly.” | `$project-init` | A clean foundation with verified commands, repository instructions, structure, Git hygiene, and safe defaults |
| “Review what I just changed.” | `$check-diff` | A focused review of change-caused defects, regressions, accidental files, and missing verification |
| “Does this actually work?” | `$check-work` | Real end-to-end product workflows executed from the user's perspective |
| “Is the implementation solid?” | `$check-code` | Correctness, reliability, data integrity, maintainability, and incomplete production behavior |
| “Could someone misuse or break this?” | `$check-sec` | Practical security defects, unsafe trust assumptions, and clearly separated hardening advice |
| “Why is this slow?” | `$check-performance` | Measured bottlenecks, expected benefits, and exact measurements to rerun after fixes |
| “Does the interface feel finished?” | `$check-polish` | Real UI testing for visual quality, interaction, responsiveness, accessibility, and platform behavior |
| “Can I confidently ship this?” | `$check-release` | A GO, GO WITH RISKS, NO-GO, or unavailable decision covering docs, versions, build, packaging, installation, upgrades, signing, and removal |
| “Make this repository look credible and complete.” | `$repo-polisher` | Evidence-backed identity, README craft, diagrams, badges, templates, metadata, and repository presentation |

## The project handoff

`$new-idea` reads existing conversations, notes, mockups, and project files before asking questions. It challenges the proposal honestly and may conclude that the project is strong, needs decisions, or should not be built yet.

Its only project mutation is an approved `docs/PROJECT.md` with one status:

- `READY FOR PROJECT-INIT`
- `NEEDS DECISIONS`
- `DO NOT BUILD YET`

`$project-init` looks for that handoff automatically. When present, it respects the status and uses the document as approved product intent while verifying technical claims against the repository. When absent, initialization behaves normally; `$new-idea` is always optional.


## Operating model

- `$new-idea` may create or update only `docs/PROJECT.md`.
- `READY FOR PROJECT-INIT` records readiness but does not authorize initialization or building.
- `$project-init` may establish or normalize the repository but never publishes without explicit authorization.
- Every `$check-*` skill is audit-only and never repairs, commits, pushes, publishes, or deploys.
- Audit skills require clear audit intent and never run as an automatic suite.
- `$repo-polisher` handles cosmetic repository presentation and identity, not product UI, code behavior, or release decisions.
- Findings distinguish confirmed defects, likely risks, and verification gaps.
- Missing execution evidence lowers confidence instead of being presented as success.

## Repository layout

```text
skills/
├── assets/
│   └── project-lifecycle.svg
├── packs/
│   ├── project-start/
│   │   ├── README.md
│   │   └── skills/
│   │       ├── new-idea/
│   │       └── project-init/
│   ├── project-checks/
│   │   ├── README.md
│   │   └── skills/
│   │       └── check-*/
│   └── project-polish/
│       ├── README.md
│       └── skills/
│           └── repo-polisher/
├── dist/
│   ├── GiftedLoser-Project-Start.zip
│   ├── GiftedLoser-Project-Checks.zip
│   ├── GiftedLoser-Project-Polish.zip
│   └── GiftedLoser-Skills-Complete.zip
├── scripts/
│   └── build-dist.ps1
├── .gitattributes
├── .gitignore
├── LICENSE
└── README.md
```


