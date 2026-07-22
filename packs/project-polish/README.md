# Project Polish

Make an existing repository clearer, more credible, and more distinctive without changing source behavior or manufacturing polish.

## Included skill

| Skill | Purpose |
|---|---|
| `$repo-polisher` | Evidence-led README craft, repository identity, visuals, diagrams, badges, and metadata—with restraint |

## Scope

`$repo-polisher` changes presentation only. It reads the project first, preserves its character, and keeps every visible claim tied to repository evidence. Missing conventional files are not automatic defects, and a repository that already communicates well may receive a no-change recommendation.

Application behavior, product UI auditing, release decisions, and outward-facing GitHub changes remain outside the skill or require explicit approval.

## How it works

1. Inspect the repository, its actual Git state, README, manifests, documentation, and existing visual identity.
2. Collect deterministic evidence with the bundled scanner.
3. Identify the single largest presentation problem and make the smallest justified change.
4. Verify the changed links, claims, commands, and assets against repository reality.

The skill supplies the judgment. The scripts supply repeatable facts.

## Why it includes Python

Repository presentation still has mechanical failure modes: broken local links, missing images, malformed package metadata, and stale evidence. Asking the model to rediscover those checks on every run is slower and less reliable, so the skill includes two small Python scripts:

- `scripts/audit_repo.py` reads a target repository and returns a JSON inventory of its README, local references, manifests, workflows, visible repository files, and visual assets. It reports confirmed parse/reference failures, not a quality score or a generic to-do list.
- `scripts/test_audit_repo.py` is the regression check for the scanner. It exercises realistic Markdown, HTML, path, and manifest edge cases in temporary directories.

Both use only the Python standard library and require Python 3.10 or newer. The audit is read-only; it does not rewrite the target repository. A missing `SECURITY.md`, changelog, template, license, or conventional README section remains context for the skill to judge—not an instruction to generate filler.

From this repository root:

```powershell
python packs/project-polish/skills/repo-polisher/scripts/audit_repo.py .
python -B packs/project-polish/skills/repo-polisher/scripts/test_audit_repo.py
```

## Install this pack

From the root of this repository, extract `dist/GiftedLoser-Project-Polish.zip` and copy its `repo-polisher` folder into `~/.codex/skills`. Start a fresh Codex task so automatic routing and the explicit `$repo-polisher` override use the new definition.
