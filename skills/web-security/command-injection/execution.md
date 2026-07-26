# Command Injection Execution Model

**File:** `skills/web-security/command-injection/execution.md`

**Version:** 1.0.0

---

# Purpose

This document defines the deterministic execution model of the Command Injection
Skill, stage by stage. Given the same inputs, configuration, and application
behavior, execution SHALL be reproducible.

---

# Execution Overview

```
Validate Request

↓

Authorize (Policy Engine)

↓

Inject Bounded Probes (HTTP Client)

↓

Observe Time-Based And Out-Of-Band Signals

↓

Record Observations → Evidence

↓

Analyze For Command Injection Weaknesses

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

# Stage 3 — Inject Bounded Probes

For authorized injection points the skill SHALL inject bounded, non-destructive
probes through the [HTTP Client](../../shared/http-client/README.md). Probes SHALL be
drawn from the managed set, SHALL run no harmful commands, and time-based probes
SHALL bound induced delays. The skill SHALL NOT perform requests directly.

---

# Stage 4 — Observe Time-Based And Out-Of-Band Signals

The skill SHALL observe bounded induced delays, capturing the canonical
[HTTP Timing](../../../schemas/http-timing.md) representation, and, where a
controlled collector is authorized, out-of-band interaction signals.

---

# Stage 5 — Record Observations And Evidence

Every check SHALL yield an [Observation](../../../schemas/observation.md) promoted
to [Evidence](../../../schemas/evidence.md). The confirming signal SHALL be recorded
and sensitive surrounding content redacted.

---

# Stage 6 — Analyze For Command Injection Weaknesses

The skill SHALL analyze the observations for command injection using deterministic
criteria and classify them using canonical weakness identifiers such as CWE-78.
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

- Same inputs, configuration, and behavior yield the same Findings.
- Analysis is separated from injection and observation.
- Time-based confirmation uses bounded, repeated measurement to reduce noise.

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
