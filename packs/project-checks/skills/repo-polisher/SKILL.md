---
name: repo-polisher
description: Do not use for UI polish, code correctness, security, performance, release-readiness audits, or ordinary feature implementation. Use when the user asks to improve, polish, professionalize, or update a repository's documentation, metadata, README, ignore rules, templates, badges, changelog, or overall credibility. Ask before changing releases, versions, licenses, or public/private positioning. Explicit $repo-polisher always invokes it.
---

# Repo Polisher

## Quality Bar

Make the repository look credible, maintainable, and ready for another engineer to trust. Optimize for factual clarity, operational usefulness, and boring professionalism.

Every visible claim must be traceable to repository evidence. Do not invent features, compatibility, benchmarks, customers, security posture, production readiness, package availability, roadmap commitments, or external integrations. Prefer no claim over a weak claim.

Preserve a repo's effective presentation style. If the README already has a distinctive, professional structure, hero treatment, screenshot, badge layout, feature table, or product voice, keep that identity and improve around it. Do not flatten a good README into a generic template.

## Default Workflow

1. Inspect the repo root, current git state, package/build files, README, docs, CI files, and .github files.
2. Identify the project type, intended audience, maturity, and likely distribution model from repository evidence.
3. Run `scripts/audit_repo.py` from a local checkout for a structural baseline:

   ```bash
   python path/to/repo-polisher/scripts/audit_repo.py /path/to/repo
   ```

4. Treat the script output as the starting map, not the final answer. Manually inspect any file before editing it.
5. Classify work as critical, recommended, or polish.
6. Apply safe documentation, metadata, .gitignore, and template improvements directly when the user asks for updates or polishing.
7. Ask only for decisions that change release/version/license/public posture.
8. Summarize changed files, validation performed, and remaining decisions.
9. After applying changes, rerun the audit script and manually review the README/rendered docs for voice, formatting, and claim quality.

## Decision Gates

Ask before:

- Changing version numbers or versioning policy.
- Creating, editing, publishing, or materially re-framing release notes/releases.
- Choosing a license when the repository does not already identify one.
- Changing or recommending public/private repository posture.

Do not ask before routine README cleanup, docs structure, .gitignore improvements, issue/PR templates, package metadata wording, typo fixes, stale template removal, or factual copy tightening.

## README Standard

Ensure the README includes the sections that are supported by the repo:

- Project name and one-sentence value proposition.
- Status or maturity note when ambiguity would mislead readers.
- Features grounded in code, docs, or existing metadata.
- Install/setup instructions.
- Quick start or usage example.
- Configuration and environment variables when applicable.
- Development workflow.
- Test/lint/build commands when discoverable.
- Project structure for non-trivial repos.
- Links to license, security, contributing, changelog, and support docs when those files exist.

Use concise, specific prose. Remove hype, filler, apologetic wording, placeholder text, and unsupported "production ready" language. Add badges only when they are accurate and derivable from existing repo metadata or live configuration.

Prefer compact additions over duplicate documentation. If the README links to strong docs for installation, configuration, or testing, add a short entry point and link deeper instead of copying the full guide into the README.

When tests, scripts, examples, or docs exist but are hard to discover, expose them through conventional commands or a short README section. For example, a Node repo with `tests/` but no `npm test` should usually get a package-level test script if a reliable test entry point already exists.

## Metadata Standard

Inspect ecosystem metadata before editing:

- Node: `package.json`, lockfiles, workspace config.
- Python: `pyproject.toml`, `setup.py`, `setup.cfg`, `requirements*.txt`.
- Rust: `Cargo.toml`.
- Go: `go.mod`.
- PHP: `composer.json`.
- .NET: `*.csproj`, `*.sln`.
- Docker: `Dockerfile`, compose files.

Improve descriptions, repository URLs, homepage/bugs URLs, keywords, classifiers, engines, files/include lists, and script names only when changes are factual and consistent with existing conventions. Preserve package names, entry points, module structure, and release fields unless the user explicitly asks.

## .gitignore Standard

Match the detected stack. Include common generated files, dependency directories, build outputs, caches, coverage, logs, editor/OS noise, and local environment files. Do not ignore source files, lockfiles, generated assets that are intentionally committed, migrations, deploy manifests, or package manager files unless the ecosystem convention clearly supports it.

## Documentation Set

Create or improve these when useful:

- `CONTRIBUTING.md`: local setup, branch/PR expectations, style, tests, issue guidance.
- `SECURITY.md`: private vulnerability reporting guidance; use an explicit maintainer placeholder only when no contact is known.
- `CHANGELOG.md`: Keep a Changelog style only when release history exists or the user asks.
- `.github/pull_request_template.md`: summary, testing, risk, checklist.
- `.github/ISSUE_TEMPLATE/*`: bug and feature templates for collaborative/public repos.
- `LICENSE`: add only when the user or existing metadata identifies the license.

Use `references/file-templates.md` for compact starter templates. Use `references/release-versioning.md` before touching changelogs, releases, or versions.

## Review Checklist

Check for:

- Empty, generated, or stale template text.
- Broken obvious internal links.
- Inconsistent project names across README, package metadata, and docs.
- Missing setup/test commands despite scripts or tooling existing.
- Sensitive local files likely committed accidentally.
- Contradictory install or run instructions.
- Unexplained environment variables.
- License mismatch between files and metadata.
- Public-facing docs that assume private context, or private docs that leak public positioning.
- Good linked docs that should satisfy README coverage rather than being duplicated.
- Existing test suites without conventional entry points in package scripts, task runners, or README commands.

## Editing Rules

- Keep changes minimal but complete.
- Preserve project behavior and user-specific conventions.
- Prefer deterministic, standard filenames and formats.
- Write Markdown that renders cleanly on GitHub.
- Prefer copy-pasteable commands, but mark uncertain commands as "if configured" or omit them.
- Do not add ornamental language, emojis, excessive badges, fake CI/coverage links, or marketing fluff.
- Do not rewrite distinctive project voice into generic corporate copy unless it is vague, misleading, or unprofessional.
- Preserve effective visual Markdown structures such as centered hero blocks, screenshots, tables, badge groups, and compact feature grids.

## Output Format

When auditing only, return:

```markdown
# Repo Health Audit

## Executive Summary
[2-4 sentences]

## Critical Fixes
[evidence-backed items]

## Recommended Fixes
[evidence-backed items]

## Polish
[evidence-backed items]

## Decisions Needed
[only release/version/license/public-private questions]
```

When applying changes, return:

```markdown
# Repo Polishing Complete

## Files Changed
[files and concise change summaries]

## Validation
[commands run and results]

## Decisions Needed
[only release/version/license/public-private questions]

## Remaining Recommendations
[items not safely changed]
```

## Reference Standards

Use these defaults unless the repo clearly uses another convention:

- Semantic Versioning for version numbers.
- Keep a Changelog structure for changelogs.
- SPDX license identifiers in package metadata.
- Conventional Commits wording for examples and PR guidance.
- GitHub Community Standards for baseline public repo hygiene.
