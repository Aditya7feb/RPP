# Cross-Site Scripting Execution Model

**File:** `skills/web-security/xss/execution.md`

**Version:** 1.0.0

---

# Purpose

This document defines the deterministic execution model of the Cross-Site Scripting
Skill, stage by stage. Given the same inputs, configuration, and application
behavior, execution SHALL be reproducible.

---

# Execution Overview

```
Validate Request

↓

Authorize (Policy Engine)

↓

Inject Bounded Marker Payloads (HTTP Client)

↓

Observe Reflection And Rendering (HTTP Client / Browser)

↓

Analyze Output Context And Encoding

↓

Record Observations → Evidence

↓

Analyze For XSS Weaknesses

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
before every target-facing action. Injection and rendering are `active` actions.
Only an `allow` decision permits the action, and the attached rate ceiling SHALL be
honored. A `requires_approval` decision SHALL defer the action until approval is
granted; stored-XSS testing SHALL require approval where the Rules of Engagement so
specify. A denial SHALL yield a `denied` status with no testing.

---

# Stage 3 — Inject Bounded Marker Payloads

For authorized injection points the skill SHALL inject bounded, non-destructive
marker payloads through the [HTTP Client](../../shared/http-client/README.md).
Markers SHALL be drawn from the managed payload set and SHALL cause no harmful side
effects. The skill SHALL NOT perform requests directly.

---

# Stage 4 — Observe Reflection And Rendering

The skill SHALL observe marker reflection in responses through the HTTP Client and
marker execution in rendered and DOM-based contexts through the
[Browser](../../shared/browser/README.md).

---

# Stage 5 — Analyze Output Context And Encoding

The skill SHALL determine the output context and whether encoding or sanitization is
context-appropriate and adequate using deterministic criteria.

---

# Stage 6 — Record Observations And Evidence

Every check SHALL yield an [Observation](../../../schemas/observation.md) promoted
to [Evidence](../../../schemas/evidence.md). The confirming marker SHALL be recorded
and sensitive surrounding content redacted.

---

# Stage 7 — Analyze For XSS Weaknesses

The skill SHALL analyze the observations for reflected, stored, and DOM-based XSS
using deterministic criteria and classify them using canonical weakness identifiers
such as CWE-79. Analysis SHALL be separate from observation.

---

# Stage 8 — Emit Findings And Risk

Where a weakness is identified the skill SHALL emit a
[Finding](../../../schemas/finding.md) with [Risk](../../../schemas/risk.md),
referencing supporting Evidence. No Finding SHALL be emitted without Evidence.

---

# Stage 9 — Return Result

The skill SHALL return findings, observations, evidence, a `status`, and metrics
per the [interface](interface.md).

---

# Determinism Guarantees

- Same inputs, configuration, and behavior yield the same Findings.
- Analysis is separated from injection and observation.
- Markers are drawn deterministically from the managed payload set.

---

# Failure Handling

Failures are mapped per the [error model](error-model.md). Partial results SHALL
be returned with Evidence where available. Policy denial SHALL always fail closed.

---

# Related Documents

- [Interface](interface.md)
- [Configuration](configuration.md)
- [Error Model](error-model.md)
- [Browser Execution](../../shared/browser/execution.md)
- [Policy Engine Execution](../../shared/policy-engine/execution.md)
