---
name: repo-polisher
description: Do not use for UI polish, code correctness, security, performance, release-readiness audits, or feature implementation. Use when the user wants a repository to look finished, credible, and attractive — README craft, project identity (icon, title treatment), diagrams, collapsible structure, badges, templates, and metadata — tastefully and per-project. Cosmetic and presentational only; never changes source behavior, and every visible claim must trace to repository evidence. Ask before changing releases, versions, licenses, or public/private positioning. Explicit $repo-polisher always invokes it.
---

# repo-polisher

Make an existing repository look cared-for, credible, and worth landing on. This is presentation and identity work: the README, the project's visual identity, structure, diagrams, templates, and metadata. It is **cosmetic and additive**, never behavioral. It does not audit correctness (`$check-code`), gate a release (`$check-release`), or judge product UI (`$check-polish`); it makes the repository itself attractive and trustworthy.

## Two hard boundaries

It **changes only presentation**: docs, README, assets, templates, metadata, and repository-surface files, never application source, logic, or build behavior. And it **never misrepresents**: every visible claim traces to repository evidence. Do not invent features, compatibility, benchmarks, customers, security posture, production readiness, package availability, roadmap commitments, or external integrations. No fabricated build badges, invented metrics, or fake stars. Prefer no claim over a weak one. Polish is enhancement, not a costume.

## Ground the work in evidence

Before writing, run `scripts/audit_repo.py` against the repository to inventory what actually exists — package files, README sections, placeholders, missing pieces — and use its output as the factual base for every claim and badge. Consult `references/repo-quality-checklist.md` for the quality bar, `references/file-templates.md` for baseline file scaffolds, and `references/release-versioning.md` when touching versions or changelogs. The script and references are the skill's grounding; do not assert anything they contradict.

## Read the project before styling it

Style follows the project; the project does not follow a template. Determine the repository's language, domain, maturity, audience, and existing visual identity first. A terminal utility, a data library, a design system, and a game each deserve a different voice. Match it. Detect and preserve an established aesthetic rather than overwriting it. Refine a strong identity; propose a fitting one only where none exists. Never impose a house style. Restraint is the default: the smallest set of changes that makes the repository read as intentional. More polish is not better polish.

## What it can enhance

**Identity:** a project icon, logo, or banner; a title treatment rendered as an SVG header when custom type is wanted (GitHub Markdown cannot set fonts directly); a consistent accent and iconography drawn from the project's own character.

**README craft:** a clear hero and one-line value statement; scannable structure with a table of contents; a feature or comparison table; quickstart, install, and usage that match reality; tidy link sections. Lead with what the project is and why it matters, in its own terms.

**Structure and density:** collapsible `<details>` sections to fold secondary content; column and card layouts via HTML `<table>` where they aid scanning; grouped sections so a long README stays navigable.

**Diagrams:** Mermaid flowcharts, architecture, and sequence diagrams for real structure the project has. A diagram earns its place by replacing paragraphs, not decorating them.

**Motion, tastefully:** an animated SVG header, a short demo GIF or cast, a `<picture>` element swapping art between light and dark themes. A garnish with a low ceiling; one tasteful moment, never a carousel.

**Badges:** accurate, resolvable badges only — license, version, release, language, real CI status. Verify each target resolves and reflects reality. A badge that lies is worse than none.

**Templates and hygiene:** `CHANGELOG`, `LICENSE`, `CITATION.cff`, contributing and issue/PR templates, ignore-rule tidiness — added from `references/file-templates.md` when the project genuinely wants them, not as ceremony.

**Metadata and discoverability:** repository description and tagline; topics; homepage URL; social-preview image; and consistency of name, tagline, and description across the README, the package manifest, and the GitHub About panel.

## Render only what GitHub renders

GitHub Markdown is the primary target and it is constrained. Rely only on what renders: Mermaid fenced blocks, `<details>`/`<summary>`, `<img>` and inline SVG, `<table>` for layout, `<picture>` with `prefers-color-scheme`, and anchor-linked tables of contents. Do not propose what GitHub strips: no `<script>`, no external CSS, no custom web fonts in Markdown (use an SVG image for custom type). Richer treatments are fine on a docs site or Pages; keep the README within what GitHub renders so it never shows broken markup.

## Workflow

1. Run `scripts/audit_repo.py`; read its inventory and the references.
2. Inspect language, domain, audience, existing README and assets, package manifest, and current GitHub metadata where accessible.
3. State the project's character in two or three lines and the presentation direction that fits it. Get a quick read from the user when identity is genuinely open; otherwise proceed with a fitting default and show it.
4. Propose the change set as a short plan before writing: which surfaces, what treatment, what stays untouched.
5. Work on a branch. Add assets under a conventional path (`assets/`, `docs/`); show every file path before creating or modifying it. Never overwrite an existing asset or section without showing what is replaced.
6. Keep every change presentational and evidence-backed. If a change touches source, build, or behavior, stop — out of scope.
7. Verify: badges resolve, links work, Mermaid parses, images load, `<picture>` swaps in both themes, the README renders on GitHub without broken markup.
8. Report what changed, before/after of key surfaces, and any outward-facing changes held for approval.

## Approvals and safety

Show every path before writing. Never push, and never change GitHub settings, description, topics, homepage, or social preview without explicit approval — those are outward-facing. Never publish or deploy. Ask before changing releases, versions, licenses, or public/private positioning. Local file changes may proceed on a branch; outward-facing metadata is proposed, then applied only on a clear yes. Preserve existing content: fold, restructure, and augment rather than delete, and surface anything you would replace.

## Output

Report: the project character read, the presentation direction taken, files created or changed with paths, assets and badges added and verified, diagrams added, the `audit_repo.py` evidence used, and a separated list of proposed outward-facing metadata changes awaiting approval. End with optional further enhancements the user can take or leave — restraint over completeness.

## Subagents

`explorer` only when a large or unfamiliar repository needs mapping before its structure can be diagrammed honestly. Presentation work is otherwise single-agent.
