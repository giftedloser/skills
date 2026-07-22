---
name: repo-polisher
description: >-
  Do not use for product UI, code correctness, security, performance, release readiness, feature work, or generic repository hygiene. Use when the user wants an existing repository's public-facing presentation improved: README hierarchy and copy, project identity, evidence-backed visuals, diagrams, badges, or repository-facing metadata. Make only justified presentation changes, preserve the project's voice, and prefer no change over generic polish. Never change application behavior or invent claims. Ask before changing GitHub settings, licenses, versions, releases, visibility, or publishing. Explicit $repo-polisher always invokes it.
---

# repo-polisher

Make a repository easier to understand, trust, and remember without making it look AI-generated. Polish is editorial judgment, not a completeness checklist.

## Boundaries

Change only repository-facing presentation such as README files, documentation landing pages, visual assets, and user-requested community templates. Do not change source, dependencies, package scripts, build configuration, ignore rules, application UI, runtime behavior, releases, or deployment.

Every claim must have a repository source. Do not infer production readiness, compatibility, performance, security, adoption, integrations, or availability from silence. Ask before changing licenses, versions, changelogs, package metadata, repository visibility, or any GitHub setting. Never push, publish, or deploy unless explicitly requested.

## Read before styling

1. Resolve the actual Git worktree root, read repository instructions, and inspect status from that root without disturbing existing work. When polishing a subdirectory, note pre-existing changes that overlap it; never call a scoped view "clean" without checking the worktree root.
2. Resolve `scripts/audit_repo.py` relative to this `SKILL.md`, run it against the target repository, and treat its output as evidence—not a score or a to-do list.
3. Read the existing README, relevant manifests, docs landing pages, screenshots, visual assets, and CI/release metadata needed to verify visible claims.
4. Read [references/repo-quality-checklist.md](references/repo-quality-checklist.md).
5. Identify the audience, the project's actual character, and the single largest presentation problem.

If the repository already communicates well, stop and say so. Missing files and short READMEs are not defects by themselves.

## Choose a direction

State a brief direction grounded in the project: what should become clearer, what existing character to preserve, and what will remain untouched. Ask only when multiple identity directions would materially change the result; otherwise proceed with the best-supported one.

Use the smallest change set that fixes the main problem. Prefer editing, tightening, reordering, or deleting weak material before adding anything. A typical pass changes the README and, only when it earns its place, one visual asset. Do not create a documentation suite, template set, badge wall, logo system, or brand guide unless the repository genuinely needs it or the user asks.

## Craft rules

- Lead with a specific answer to: what is this, who is it for, and what can the reader do next?
- Preserve strong existing copy, screenshots, identity, and project-specific language.
- Replace generic claims such as "powerful," "seamless," "modern," and "production-ready" with concrete facts or delete them.
- Include install, usage, configuration, development, testing, architecture, support, or contributing material only when that reader needs it and the repository proves it.
- Keep commands exact and verify them through manifests, task files, CI, or a safe execution path. Do not invent or "standardize" commands.
- Use badges only when each answers a likely reader question and its target resolves. Existing real CI does not require a badge.
- Add a diagram only when real relationships are clearer visually than in prose. Keep labels project-specific and verify Mermaid syntax when used.
- Add identity art only when it expresses something specific to the project. Prefer existing assets. Avoid generic gradients, glowing blobs, floating cards, stock mascots, decorative terminal chrome, emoji section labels, and ornamental SVG animation.
- Use HTML tables and `<details>` only when they improve scanning or disclosure; never as default layout decoration.
- Keep accessible alt text, readable contrast, sensible image dimensions, and useful light/dark behavior.

## Evidence discipline

Maintain a small working ledger of each new or materially rewritten claim and its source. If a claim cannot be supported, omit it or label the uncertainty plainly. Report invalid manifests, broken references, or suspected secrets to the user; do not repair them under this skill unless the repair is itself presentation-only and requested.

Do not turn scanner observations into automatic changes. In particular, the absence of `SECURITY.md`, `CHANGELOG.md`, contribution templates, issue templates, a package manifest, a license, or conventional README sections is contextual—not proof of poor presentation.

## Verify

Review the final diff for scope and voice. Then verify only what changed:

- local README links and images resolve;
- edited commands and visible claims trace to evidence;
- badges and external links resolve when network access is available;
- Mermaid or SVG parses when added;
- images remain legible at GitHub desktop and narrow widths;
- no unrelated content or user work was removed.

Use a real GitHub render or browser preview when practical. State exactly what could not be rendered or checked. Do not stage, commit, branch, or push unless the user asked.

## Output

Report the presentation problem addressed, the direction taken, changed paths, verification performed, and any outward-facing proposals still awaiting approval. Mention skipped additions only when their omission may surprise the user.
