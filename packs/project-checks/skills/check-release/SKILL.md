---
name: check-release
description: Do not use when shipping or release is mentioned in passing, or to publish, deploy, tag, or implement release work. Use only when the user clearly asks for a release-readiness audit of one identified candidate and wants a GO, GO WITH RISKS, NO-GO, or unavailable decision. Explicit $check-release always invokes it.
---

# check-release

Determine whether one identified release candidate can be reliably **built, packaged, installed, launched, updated, and removed by a real user.**

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

1. Identify one intended candidate and distribution method. Record commit, version, architecture, build time, artifact filename, and SHA-256 hash. Without one identifiable candidate and complete artifact identity, artifact readiness is `BLOCKED` and the release decision is unavailable.
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

Follow the audit contract and report source readiness and artifact readiness separately. Include candidate identity and the affected release stage for each finding. Map the final decision deterministically:

- `PASS` → `GO`
- `PASS WITH RISKS` → `GO WITH RISKS`
- `FAIL` → `NO-GO`
- `BLOCKED` → `DECISION UNAVAILABLE`

A confirmed build failure is `FAIL` / `NO-GO`, not `BLOCKED`. End with artifacts verified, release actions deliberately not performed, install behaviors executed versus inspected, blockers, risks, and the exact release checks to rerun.

---

## Audit Contract

**Audit-only.** Do not edit source, repair findings, install dependencies, commit, push, publish, deploy, or change configuration. Repository-native checks may create derived artifacts; inspect state before and after, report generated changes, and never clean or overwrite user work.

Before any work, state:

- `Target:` exact workflow, module, boundary, interface, candidate, or diff.
- `Applicable categories:` what applies and what does not.
- `Primary verification:` the defining proof required for this audit.
- `User restrictions:` read-only, environment, data, credential, or side-effect limits.

**Mode:** `EXECUTED` | `STATIC ONLY` | `SUPPLIED EVIDENCE`.

**Outcome:** `PASS` | `PASS WITH RISKS` | `FAIL` | `BLOCKED` | `NOT APPLICABLE`.

Return `FAIL` when a confirmed defect breaks the defining objective or any confirmed `CRITICAL` or `HIGH` defect exists. Use `PASS WITH RISKS` only for actionable lower-severity defects or explicitly bounded residual risk after defining verification completes.

Return `BLOCKED` when the defining verification cannot run. Never launder missing proof into `PASS WITH RISKS`. Use `NOT APPLICABLE` only when the skill's subject does not exist. `PASS` requires completed defining verification and no actionable findings. Confirmed lower-severity defects require `PASS WITH RISKS`.

Use disposable data and non-production systems. Do not cause destructive or externally visible effects without explicit authorization. Tie evidence to the relevant revision or artifact; label inference as `INFERENCE`.

**Severity:** `CRITICAL` | `HIGH` | `MEDIUM` | `LOW` | `INFORMATIONAL`.

**Classification:** `CONFIRMED DEFECT` | `LIKELY RISK` | `VERIFICATION GAP`.

```text
[SEVERITY] Title
Classification: <classification>
Evidence: <source, execution, artifact, or measurement>
Consequence: <what breaks and for whom>
Correction: <smallest practical correction or required verification>
Recheck: <exact check that proves resolution>
```

Report `RESULT`, `MODE`, scope, verified evidence, unverified items, and only the highest-value findings in severity order. Do not pad the report or recap empty categories. Include a ready-to-paste `REMEDIATION PROMPT` only when actionable findings exist.
