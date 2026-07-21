---
name: check-release
description: Determine whether a repository and product are ready for release, including documentation, versioning, build, packaging, installation, launch, update, and removal. Use when the user explicitly invokes $check-release or requests this named release-readiness audit; provide a GO or NO-GO decision without publishing or deploying.
---

# check-release

Determine whether the product can be reliably **built, packaged, installed, launched, updated, and removed by a real user.** GO/NO-GO gate.

## Hard restrictions

Never: publish, deploy, create a release, push tags, upload artifacts, modify production systems, change signing credentials.

**Machine-safety restriction:** install testing is limited to portable launch or disposable locations (temp directories, throwaway VMs when available). Anything requiring elevation, registry writes, service installation, shortcut creation, or file-association changes on the real machine is **report-only** — inspect the installer's declared behavior, do not execute it. State clearly which install behaviors were executed vs inspected.

Run builds in a disposable copy, temporary worktree, or isolated output directory when practical. Never clean, reset, or otherwise alter the user's working tree to manufacture a clean build.

## Audit areas

**Build:** clean-checkout build, release configuration, compiler warnings, missing generated files, environment assumptions, reproducibility.
**Versioning:** package/application/installer version agreement, release metadata, changelog consistency, artifact naming.
**Repository surface:** accurate description and README, verified installation and usage instructions, current documentation, links and screenshots, license and compatibility information when applicable, intentional layout, and absence of accidental scratch, local configuration, or generated test output.
**Packaging:** installer, portable build, archive contents, required runtime files, missing assets, platform and architecture targets.
**Installation:** permissions, elevation, install path, shortcuts, file associations, registry, services, first launch.
**Upgrade:** settings and data migration, backward compatibility, rollback, failed-upgrade recovery, stale files.
**Runtime integration:** autostart, tray, update checks, background processes, shutdown, uninstall cleanup, retained user data.
**Signing/trust:** signing configuration, certificate handling, unsigned artifacts, installer reputation implications, integrity verification.
**Automation:** CI, release workflows, artifact upload, release notes, secrets handling, branch and tag assumptions — **reviewed, never triggered.**

## Workflow

1. Identify the intended distribution method.
2. Inspect version and packaging configuration; verify version agreement across package, app, installer, and metadata.
3. Review the repository surface and verify user-facing setup, usage, compatibility, changelog, and release documentation against the current product.
4. Run a clean release build (fresh clone or clean working tree) when possible.
5. Inspect produced artifacts; verify required files are bundled.
6. Portable-launch the artifact from a disposable location.
7. Inspect (per the safety restriction) install, upgrade, migration, and uninstall behavior.
8. Review release automation without triggering it.
9. Identify platform-specific risks.

## Release blockers

Treat these as common blockers: the intended artifact cannot be built or packaged from the current source; required files are missing; the artifact cannot launch through the intended user path; version or architecture metadata would misidentify the artifact; required upgrade, data-preservation, or removal behavior fails; signing or policy requirements prevent intended users from running it; or a required primary release verification remains unresolved.

Treat repository-surface issues as blockers only when they materially mislead users about installation, usage, compatibility, licensing, version, or artifact selection. Cosmetic presentation issues are non-blocking.

For portable-only products, verify archive contents and integrity, extraction to a disposable directory, launch as a standard user outside the build tree, settings and data location, replacement-style upgrade, shutdown, removal by deleting application files, and the documented treatment of retained user data. Do not invent installer, registry, service, shortcut, or file-association requirements the product does not claim.

## Output

Contract report structure, plus per finding the affected release stage. Map the final gate deterministically: `PASS` = `GO`; `PASS WITH RISKS` = `NO-GO` until the stated risks or verification gaps are resolved; `FAIL` = `NO-GO`. End with: release artifacts verified, release actions deliberately not performed, install behaviors executed vs inspected, blocking issues, the **GO / NO-GO statement with reasoning**, remediation prompt, and the exact release checks to rerun.

## Subagents

`release-captain` for substantial packaging or release pipelines. `security-reviewer` when signing, updates, elevation, or distribution boundaries need security review.


---

## Audit Contract (shared, identical across all check skills)

**Audit-only.** This skill never: edits source files, repairs findings, installs dependencies, commits, pushes, publishes, deploys, changes configuration, or claims something works without executed evidence. If a fix is obvious, it goes in the remediation prompt, not into the repo.

**Results:** `PASS` | `PASS WITH RISKS` | `FAIL` (check-polish may also return `NOT APPLICABLE`).

**Severity:** `CRITICAL` | `HIGH` | `MEDIUM` | `LOW` | `INFORMATIONAL`.

**Classification:** every finding is exactly one of:
- `CONFIRMED DEFECT` — reproduced or proven from code/execution
- `LIKELY RISK` — strong evidence, not fully reproduced
- `VERIFICATION GAP` — could not be checked; state why

**Finding schema (every finding, no exceptions):**

```
[SEVERITY] Title
Classification: CONFIRMED DEFECT | LIKELY RISK | VERIFICATION GAP
Evidence: file:line references, command output, screenshot, or measurement
Consequence: what breaks and for whom
Correction: specific recommended fix, or for a `VERIFICATION GAP`, the exact verification required (do not apply or execute it)
```

**Evidence hierarchy (strongest first):** repository code with file:line → executed behavior → logs → tests → official documentation → reasoned inference explicitly labeled `INFERENCE`. Never present inference as observation.

**Blocked validation:** if something cannot run, report exactly what could not run, why, the next-best verification performed instead, and the residual uncertainty. A check that could not execute its primary verification cannot return `PASS`. Return `PASS WITH RISKS` when no stronger defect is proven; confirmed evidence may still require `FAIL`.

**Generated outputs:** repository-native checks may create derived build artifacts, caches, logs, or test output. Prefer disposable output locations or a temporary copy when practical. Inspect repository state before and after, report generated changes, and never clean, reset, delete, or overwrite user-owned work to restore the tree.

**Execution safety:** use disposable data, temporary locations, and non-production accounts or services. Never exercise production systems, real user data, or externally visible side effects without explicit authorization.

**Result thresholds:** `FAIL` when a confirmed defect breaks the skill's core objective, any confirmed `CRITICAL` or `HIGH` defect exists, or a release-blocking condition applies. `PASS WITH RISKS` when findings are limited to lower-severity defects, likely risks, or verification gaps. `PASS` only when primary verification ran and produced no actionable findings.

**Report structure:**

```
RESULT: PASS | PASS WITH RISKS | FAIL
Verified: <what was actually executed and confirmed>
Not verified: <what was not, and why>

Findings (severity-ordered, schema above)

REMEDIATION PROMPT
<ready-to-paste prompt for a separate fix session, scoped to the findings,
 including exact checks to rerun after remediation>
```

**No padding.** No generic essays, no restating the audit areas that produced nothing, no findings invented to look thorough. Zero findings is a valid, reportable outcome; omit the remediation prompt when there is nothing to remediate.
