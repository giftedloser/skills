# GiftedLoser Skills

Ten Codex skills for checking your own work. Finish a chunk, run the one that fits, move on. They're sorted into three packs, but each one is its own tool. Grab whatever the moment calls for.

![Skills](https://img.shields.io/badge/skills-10-6d5dfc)
![Packs](https://img.shields.io/badge/packs-3-167d68)
![Invocation](https://img.shields.io/badge/invocation-automatic%20%2B%20explicit-3974c6)
[![License: MIT](https://img.shields.io/badge/license-MIT-c47716)](LICENSE)

Built for Codex. Not currently compatible with Claude Code or other runtimes.

## Say it plainly, get the right tool

Describe what you're after and Codex picks the skill, or type the name yourself. Either works.

| When you're thinking... | You reach for |
|---|---|
| "Is this idea worth building?" | **new-idea** — value, gaps, scope, feasibility, and risk, ending in `docs/PROJECT.md` |
| "Set this project up right." | **project-init** — verified commands, structure, Git hygiene, safe defaults |
| "Did I break anything?" | **check-diff** — defects and regressions from what you just changed |
| "Does this actually work?" | **check-work** — the real workflow, run end to end from the user's side |
| "Is the code solid?" | **check-code** — correctness, reliability, data integrity, unfinished behavior |
| "Could someone break this?" | **check-sec** — real security holes and bad trust assumptions, hardening kept separate |
| "Why is this slow?" | **check-performance** — measured bottlenecks and the numbers to rerun after a fix |
| "Does the UI feel done?" | **check-polish** — visuals, interaction, responsiveness, accessibility, run for real |
| "Can I ship this?" | **check-release** — GO / GO WITH RISKS / NO-GO across build, install, upgrade, signing, removal |
| "Make this repo look legit." | **repo-polisher** — README, diagrams, badges, templates, metadata, without touching your code |

Force a specific one when you want it:

```text
$check-diff
$check-sec
```

Run one, run three, run none. There's no batch and no required order. The checks stay out of your way unless you ask for one.

## The three packs

<details>
<summary><b>Project Start</b> — new-idea, project-init</summary>

**new-idea** reads your notes, mockups, and existing files first, then pushes back on the idea honestly. It can say the thing's strong, it needs decisions, or don't build it yet. The only thing it writes is `docs/PROJECT.md`, with one status:

- `READY FOR PROJECT-INIT`
- `NEEDS DECISIONS`
- `DO NOT BUILD YET`

`READY` means the idea holds up. It doesn't mean start building.

**project-init** picks up that handoff automatically when it exists, treats it as approved intent, and checks every technical claim against the real repo. No handoff, no problem — it just sets things up normally. new-idea is always optional.

[Pack README](packs/project-start/README.md)
</details>

<details>
<summary><b>Project Checks</b> — seven checks</summary>

Seven checks, one question each. Run the one that matches what you're unsure about.

- **check-diff** — what did this change break?
- **check-work** — does the feature work end to end?
- **check-code** — is the implementation sound?
- **check-sec** — can someone misuse or break it?
- **check-performance** — where's the measured slowdown?
- **check-polish** — does the interface hold up under real use?
- **check-release** — is this build safe to ship?

They only look, they don't touch. No repairs, commits, pushes, or deploys. And they won't fake a result: a check that can't run the real thing returns `BLOCKED` instead of a green pass. Findings tell confirmed defects apart from likely risks apart from what couldn't be verified.

[Pack README](packs/project-checks/README.md)
</details>

<details>
<summary><b>Project Polish</b> — repo-polisher</summary>

**repo-polisher** handles how the project looks: README, diagrams, badges, issue and PR templates, metadata. It shapes the repo's public face and leaves your source alone. Ask for an audit and it audits; ask it to apply safe doc and metadata fixes and it does.

[Pack README](packs/project-polish/README.md)
</details>

## Install

<details>
<summary>Download, extract, copy in</summary>

Grab the ZIP you want, copy the skill folders into your Codex skills directory.

> [!WARNING]
> These overwrite installed skills with the same folder name. Back up local changes first.

**Windows PowerShell**

```powershell
New-Item -ItemType Directory -Force "$env:USERPROFILE\.codex\skills" | Out-Null
Copy-Item -Recurse -Force .\* "$env:USERPROFILE\.codex\skills\"
```

**macOS or Linux**

```bash
mkdir -p ~/.codex/skills
cp -R ./* ~/.codex/skills/
```

Start a fresh Codex task afterward so the catalog reloads.

**ZIPs**

- `dist/GiftedLoser-Skills-Complete.zip` — all ten
- `dist/GiftedLoser-Project-Start.zip`
- `dist/GiftedLoser-Project-Checks.zip`
- `dist/GiftedLoser-Project-Polish.zip`

</details>

<details>
<summary>Config and development</summary>

No environment variables, no repo-level config. Routing metadata lives in each skill's `agents/openai.yaml`; restart your Codex task after installing or updating one.

Edit source under `packs/*/skills/`. Keep each `SKILL.md` and its `agents/openai.yaml` in sync, then rebuild:

```powershell
.\scripts\build-dist.ps1
```

Check the ZIPs still match source:

```powershell
.\scripts\build-dist.ps1 -Check
```

Exits with an error if an archive is missing or stale.

</details>

<details>
<summary>Ground rules</summary>

- new-idea writes only `docs/PROJECT.md`.
- `READY FOR PROJECT-INIT` records readiness, doesn't authorize building.
- project-init sets up or normalizes a repo, never publishes without explicit go-ahead.
- Every check is look-only: no repairs, commits, pushes, or deploys.
- Checks run on request, never as a batch.
- repo-polisher handles presentation, not product UI, code behavior, or release calls.
- Findings separate confirmed defects, likely risks, and verification gaps.
- Missing evidence lowers the verdict instead of passing as success.

</details>

<details>
<summary>Layout</summary>

```text
skills/
├── packs/
│   ├── project-start/    (new-idea, project-init)
│   ├── project-checks/   (check-*)
│   └── project-polish/   (repo-polisher)
├── dist/                 (the four ZIPs)
├── scripts/
│   └── build-dist.ps1
├── LICENSE
└── README.md
```

</details>
