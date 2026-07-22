# Repo Quality Checklist

Use this checklist as the quality bar for repo polishing.

## Essential

- README explains what the project is, why it exists, how to install it, and how to run it.
- README commands are supported by package files, scripts, Makefiles, task runners, or documented tooling.
- README preserves any existing professional visual identity, screenshot placement, badge layout, or feature presentation.
- Metadata descriptions are concise, factual, and searchable.
- `.gitignore` matches the stack and excludes local secrets, caches, logs, dependencies, and build outputs.
- License references are consistent across `LICENSE`, README, and package metadata.
- Project name is consistent across docs and metadata.
- No generated placeholder copy remains visible.
- No public claim depends on information that cannot be found in the repository.

## Professional

- README has quick start, configuration, development, testing, and project structure sections when applicable.
- README links to deeper docs instead of duplicating long installation, configuration, or testing guides.
- Existing test suites are exposed through conventional commands or clear README entry points.
- Issue and PR templates are present for public or collaborative repos.
- SECURITY.md exists for public-facing repos or software that could be deployed by others.
- CONTRIBUTING.md gives practical local workflow instructions.
- CHANGELOG.md is present when the project has releases or versioned distribution.
- Badges, links, package names, and repository URLs resolve or are clearly derived from existing metadata.
- Environment variables are documented with purpose, required/optional status, and safe example values where useful.
- Documentation explains limitations or maturity honestly when the repo is experimental, internal, or incomplete.

## Avoid

- Fake badges or unsupported claims.
- "Production ready" claims without evidence.
- Choosing a license without user input.
- Overwriting distinctive project voice with generic corporate copy.
- Ignoring lockfiles by default.
- Recommending release or version changes without explicit maintainer approval.
- Adding generic docs that do not match the repo's actual workflow.
- Expanding a strong README with bulky duplicated content when a short link to existing docs would be cleaner.
