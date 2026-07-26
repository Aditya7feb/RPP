# Content Security Policy Execution Model

**File:** `skills/web-security/csp/execution.md`

**Version:** 1.0.0

---

# Purpose

This document defines the deterministic execution model of the Content Security
Policy Skill, stage by stage. Given the same inputs, configuration, and policy
content, execution SHALL be reproducible.

---

# Execution Overview

```
Validate Request

↓

Authorize (Policy Engine)

↓

Observe Content Security Policy (HTTP Client)

↓

Analyze Directives, Sources, And Bypasses

↓

Record Observations → Evidence

↓

Analyze For Weaknesses

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
before every target-facing action. Response probing is an `active` action. Only an
`allow` decision permits the action, and the attached rate ceiling SHALL be
honored. A `requires_approval` decision SHALL defer the action until approval is
granted; a denial SHALL yield a `denied` status with no testing.

---

# Stage 3 — Observe Content Security Policy

The skill SHALL observe the `Content-Security-Policy` header and any meta policy
through the [HTTP Client](../../shared/http-client/README.md), capturing the
canonical [HTTP Header](../../../schemas/http-header.md) representation. The skill
SHALL NOT perform requests directly.

---

# Stage 4 — Analyze Directives, Sources, And Bypasses

The skill SHALL analyze directive coverage, source-list strength, unsafe sources,
known bypasses, and enforcement mode using deterministic criteria.

---

# Stage 5 — Record Observations And Evidence

Every check SHALL yield an [Observation](../../../schemas/observation.md) promoted
to [Evidence](../../../schemas/evidence.md).

---

# Stage 6 — Analyze For Weaknesses

The skill SHALL analyze the observations for CSP weaknesses using deterministic
criteria and classify them using canonical weakness identifiers such as CWE-693.
Analysis SHALL be separate from observation.

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

- Same inputs, configuration, and policy content yield the same Findings.
- Analysis is separated from observation.
- All randomness, if any, SHALL be seeded and recorded.

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
