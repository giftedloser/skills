# GiftedLoser's Skills

![Skills](https://img.shields.io/badge/skills-10-6d5dfc)
![Packs](https://img.shields.io/badge/packs-3-167d68)
![Invocation](https://img.shields.io/badge/invocation-automatic%20%2B%20explicit-3974c6)
[![License: MIT](https://img.shields.io/badge/license-MIT-c47716)](LICENSE)

Ten Codex skills that read your work instead of writing it. Point one at a branch and it will run the app and see if the feature actually works, comb the diff for what the change broke, look for security holes, measure what is slow, check whether the UI holds up, or decide whether the thing is ready to ship. Two more run at the start, one to argue with the idea and one to set up the repo, and one cleans up how the repository presents itself.

Each stands alone. Install everything or just one pack, and call them when the work calls for it.

## Skills at a glance

| You are thinking... | Use | What you get |
|---|---|---|
| “Is this idea worth building?” | `$new-idea` | A review of value, contradictions, gaps, scope, feasibility, risks, and experience direction, ending in `docs/PROJECT.md` |
| “Set this project up properly.” | `$project-init` | A clean foundation with verified commands, repository instructions, structure, Git hygiene, and safe defaults |
| “Review what I just changed.” | `$check-diff` | A focused review of change-caused defects, regressions, accidental files, and missing verification |
| “Does this actually work?” | `$check-work` | Real end-to-end product workflows executed from the user's perspective |
| “Is the implementation solid?” | `$check-code` | Correctness, reliability, data integrity, maintainability, and incomplete production behavior |
| “Could someone misuse or break this?” | `$check-sec` | Practical security defects, unsafe trust assumptions, and clearly separated hardening advice |
| “Why is this slow?” | `$check-performance` | Measured bottlenecks, expected benefits, and exact measurements to rerun after fixes |
| “Does the interface feel finished?” | `$check-polish` | Real UI testing for visual quality, interaction, responsiveness, accessibility, and platform behavior |
| “Can I ship this?” | `$check-release` | A `GO`, `GO WITH RISKS`, `NO-GO`, or `unavailable` decision covering docs, versions, build, packaging, installation, upgrades, signing, and removal |
| “Make this repository clearer and more credible.” | `$repo-polisher` | Focused README and repository presentation improvements grounded in evidence, including a no-change result when appropriate |

## Packs

| Pack | Skills | Purpose |
|---|---|---|
| [Project Start](packs/project-start/README.md) | `$new-idea`, `$project-init` | Challenge the idea, create an approved project handoff, and establish the repository safely |
| [Project Checks](packs/project-checks/README.md) | Seven `$check-*` skills | Audit the change, behavior, implementation, security, performance, interface, and release |
| [Project Polish](packs/project-polish/README.md) | `$repo-polisher` | Improve README clarity and repository identity with evidence-led, presentation-only changes |

Prebuilt archives live in [`dist/`](dist/), one per pack plus `GiftedLoser-Skills-Complete.zip` for the whole collection.

## What the checks will not do

The seven `$check-*` skills are read-only. They open files, run the build, exercise the app, and take measurements, but they never edit, commit, push, publish, or deploy. Nothing they find gets quietly fixed on the way past.

What comes back is the finding, the evidence behind it, and an honest label on it. Confirmed defects, likely risks, and verification gaps stay separate, and missing execution evidence lowers confidence instead of being written up as success. Each report ends with remediation instructions you can hand to whatever agent does the fixing.

That separation also makes them safe to run in a subagent. A focused check can work on its own or in parallel without holding permission to change the project.

## Example workflow

![Project lifecycle from idea to release](assets/project-lifecycle.svg)

This is one example, not a required order. Most changes never need the deeper checks, and running all of them on a color tweak is a waste. Pick what the scope actually calls for.

## Invocation

Describe the result you want. Codex routes the narrowest applicable skill, and audit skills stay quiet unless the request clearly asks for an audit. Explicit `$name` invocation is always available as an override. Audits never run as an automatic suite.

## The project handoff

`$new-idea` reads existing conversations, notes, mockups, and project files before it asks you anything. It challenges the proposal honestly and may conclude that the project is strong, needs decisions, or should not be built yet.

Its only project mutation is an approved `docs/PROJECT.md` carrying one status:

| Status | Meaning |
|---|---|
| `READY FOR PROJECT-INIT` | The idea holds up. Readiness is recorded, but this does not authorize initialization or building. |
| `NEEDS DECISIONS` | Open questions have to be answered first. |
| `DO NOT BUILD YET` | The idea does not survive its own review. |

`$project-init` looks for that handoff automatically. When it is there, it respects the status and treats the document as approved product intent while verifying every technical claim against the repository. When it is absent, initialization behaves normally. `$new-idea` is always optional.

## Operating model

| Skill | May change | Never does |
|---|---|---|
| `$new-idea` | `docs/PROJECT.md` only | Anything else in the project |
| `$project-init` | Repository structure, tooling, Git hygiene | Publish without explicit authorization |
| `$check-*` | Nothing | Repair, commit, push, publish, deploy, or run as an automatic suite |
| `$repo-polisher` | README and repository presentation | Touch product UI, code behavior, or release decisions |

`$repo-polisher` collects its evidence with a dependency-free Python scanner so results are repeatable. It does not grade the repository, and a missing conventional file is not automatically work worth doing.

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

## License

MIT. See [LICENSE](LICENSE).
