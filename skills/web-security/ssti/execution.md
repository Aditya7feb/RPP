# Server-Side Template Injection Execution Model

**File:** `skills/web-security/ssti/execution.md`

**Version:** 1.0.0

---

# Purpose

This document defines the deterministic execution model of the Server-Side Template
Injection Skill, stage by stage. Given the same inputs, configuration, and application
behavior, execution SHALL be reproducible.

---

# Execution Overview

```
Validate Request

↓

Authorize (Policy Engine)

↓

Inject Bounded Expression Markers (HTTP Client)

↓

Observe Evaluation And Engine Indicators

↓

Record Observations → Evidence

↓

Analyze For Template Injection Weaknesses

↓

Emit Findings And Risk

↓

Return Result
```

---

# Stage 1 — Validate Request

The skill SHALL validate that `target`, `scope_id`, and `roe_id` are present and
well formed. Invalid requests SHALL fail closed with a validation error and no
action.

---

# Stage 2 — Authorize

The skill SHALL consult the [Policy Engine](../../shared/policy-engine/README.md)
before every target-facing action. Injection probing is an `active`, high-impact
action. Only an `allow` decision permits the action, and the attached rate ceiling
SHALL be honored. A `requires_approval` decision SHALL defer the action until
approval is granted; a denial SHALL yield a `denied` status with no testing.

---

# Stage 3 — Inject Bounded Expression Markers

For authorized injection points the skill SHALL inject bounded, non-destructive
expression markers through the [HTTP Client](../../shared/http-client/README.md).
Markers SHALL be drawn from the managed set and SHALL NOT escalate to code execution.
The skill SHALL NOT perform requests directly.

---

# Stage 4 — Observe Evaluation And Engine Indicators

The skill SHALL observe whether a marker is evaluated — for example, a bounded
arithmetic expression yielding its computed result — and which template engine class
is indicated by evaluation behavior.

---

# Stage 5 — Record Observations And Evidence

Every check SHALL yield an [Observation](../../../schemas/observation.md) promoted
to [Evidence](../../../schemas/evidence.md). The evaluated marker SHALL be recorded
and sensitive surrounding content redacted.

---

# Stage 6 — Analyze For Template Injection Weaknesses

The skill SHALL analyze the observations for server-side template injection using
deterministic criteria and classify them using canonical weakness identifiers such as
CWE-1336. Analysis SHALL be separate from observation.

---

# Stage 7 — Emit Findings And Risk

Where a weakness is identified the skill SHALL emit a
[Finding](../../../schemas/finding.md) with [Risk](../../../schemas/risk.md),
referencing supporting Evidence. No Finding SHALL be emitted without Evidence.

---

# Stage 8 — Return Result

The skill SHALL return findings, observations, evidence, a `status`, and metrics
per the [interface](interface.md).

---

# Determinism Guarantees

- Same inputs, configuration, and behavior yield the same Findings.
- Analysis is separated from injection and observation.
- Markers are drawn deterministically from the managed set.

---

# Failure Handling

Failures are mapped per the [error model](error-model.md). Partial results SHALL
be returned with Evidence where available. Policy denial SHALL always fail closed.

---

# Related Documents

- [Interface](interface.md)
- [Configuration](configuration.md)
- [Error Model](error-model.md)
- [HTTP Client Execution](../../shared/http-client/execution.md)
- [Policy Engine Execution](../../shared/policy-engine/execution.md)
