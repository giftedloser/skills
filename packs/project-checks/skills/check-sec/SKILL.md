---
name: check-sec
description: Do not use when security is mentioned in passing, for secure implementation requests, or for general code review. Use only when the user clearly asks for a security audit or threat review focused on practical exploitable defects and unsafe trust assumptions. Explicit $check-sec always invokes it.
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
**Credential lifecycle:** observable handling through command-line arguments, inherited environment variables, temporary files, logs, child processes, long-lived strings, and cleanup behavior. Do not claim forensic memory or crash-remnant inspection that was not performed.

## Workflow

1. Identify trust boundaries and privileged components; sketch them in two or three lines.
2. Trace each untrusted source through its entry point to a sensitive sink.
3. Review auth paths, then secrets, configuration, and observable credential-lifecycle handling.
4. Review process, filesystem, network, and IPC boundaries.
5. Review dependency and build-chain risk.
6. Verify significant findings with concrete code paths or safe proof. Never perform destructive exploitation or externally visible abuse; demonstrate reachability instead.
7. Treat unused permissions and defense-in-depth improvements as hardening unless a reachable compromise is proven.
8. Split the report: exploitable defects first, hardening suggestions after, clearly labeled.

## Output

Follow the audit contract and include the scoping decision and a brief trust-boundary summary. Every exploitable finding must state:

- attacker or untrusted source;
- entry point;
- sensitive sink or operation;
- required privileges and other preconditions;
- practical impact;
- safe evidence proving reachability.

Scope remediation to exploitable defects first.

Every exploitable defect uses the full finding schema. A hardening suggestion uses the full schema when it identifies a concrete, actionable risk. Optional defense-in-depth hygiene without a specific failure path belongs in a short `Hardening notes` list, is `INFORMATIONAL`, and is not counted as a defect.

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
