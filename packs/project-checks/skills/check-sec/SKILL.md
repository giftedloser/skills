---
name: check-sec
description: Audit a repository for practical, exploitable security defects and unsafe trust assumptions. Use when the user explicitly invokes $check-sec or requests this named security audit; separate exploitable defects from theoretical hardening.
---

# check-sec

Audit the repository for **practical, exploitable security defects and unsafe trust assumptions.** Exploitable defects and theoretical hardening are reported separately and never mixed.

## Step 0 — Scope first, always

Before auditing, identify which categories below actually apply to this repository and state the scoping decision in the report: applicable categories, skipped categories, and one line of reasoning per skip. A 200-line CLI does not get a web-session audit. Depth goes to applicable categories only.

## Category reference

**Auth:** identity validation, session handling, authorization checks, privilege escalation, insecure defaults, missing ownership checks.
**Secrets:** hardcoded credentials, keys, tokens, secrets in logs or source control, sensitive configuration.
**Input:** command/shell/SQL/template/script injection, path traversal, unsafe deserialization, malformed input, insufficient validation.
**System boundaries:** filesystem access, process launching, IPC, registry, services, permissions, elevation, browser-to-native and frontend-to-backend command exposure.
**Network:** URL validation, origin restrictions, redirects, TLS assumptions, credential forwarding, request limits, timeouts, unsafe downloads, RCE.
**Supply chain:** unsafe dependency sources, mutable remote execution, unpinned tooling, install scripts, abandoned or vulnerable dependencies, package confusion, insecure release pipelines.
**Desktop/local:** arbitrary command execution, unsafe path construction, writable privileged locations, insecure temp files, symlink/junction issues, unsafe updaters, untrusted plugin loading.
**Logging/privacy:** sensitive logs, excessive telemetry, personal data handling, credential exposure in errors.

## Workflow

1. Identify trust boundaries and privileged components; sketch them in two or three lines.
2. Trace untrusted input to sensitive sinks for each applicable category.
3. Review auth paths, then secrets and configuration handling.
4. Review process, filesystem, network, and IPC boundaries.
5. Review dependency and build-chain risk.
6. Verify significant findings with concrete code paths or **safe** tests. Never run an exploit that could damage state; demonstrate reachability instead.
7. Split the report: exploitable defects first, hardening suggestions after, clearly labeled.

## Output

Contract report structure, plus: the scoping decision from step 0, a brief trust-boundary summary, and for each finding the attack or failure path and affected boundary. Remediation prompt scoped to exploitable defects first.

Every exploitable defect uses the full finding schema. A hardening suggestion uses the full schema when it identifies a concrete, actionable risk. Optional defense-in-depth hygiene without a specific failure path belongs in a short `Hardening notes` list, is `INFORMATIONAL`, and is not counted as a defect.

## Subagents

`security-reviewer` when the repository has meaningful security-sensitive behavior. `explorer` when boundary mapping is complex. A subagent's claim is never evidence — verify against code.


---

## Audit Contract

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
