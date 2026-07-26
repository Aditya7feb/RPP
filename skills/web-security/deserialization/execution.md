# Insecure Deserialization Execution Model

**File:** `skills/web-security/deserialization/execution.md`

**Version:** 1.0.0

---

# Purpose

This document defines the deterministic execution model of the Insecure
Deserialization Skill, stage by stage. Given the same inputs, configuration, and
application behavior, execution SHALL be reproducible.

---

# Execution Overview

```
Validate Request

↓

Authorize (Policy Engine)

↓

Submit Bounded Serialized Probes (HTTP Client)

↓

Observe Out-Of-Band And Differential Signals

↓

Record Observations → Evidence

↓

Analyze For Insecure Deserialization Weaknesses

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
before every target-facing action. Serialized probing is an `active`, high-impact
action. Only an `allow` decision permits the action, and the attached rate ceiling
SHALL be honored. A `requires_approval` decision SHALL defer the action until approval
is granted; a denial SHALL yield a `denied` status with no testing.

---

# Stage 3 — Submit Bounded Serialized Probes

For authorized endpoints the skill SHALL submit bounded, non-destructive serialized
probes drawn from the managed set through the
[HTTP Client](../../shared/http-client/README.md). Probes SHALL NOT deliver a
functional gadget chain, and the skill SHALL NOT perform requests directly.

---

# Stage 4 — Observe Out-Of-Band And Differential Signals

The skill SHALL observe whether an out-of-band interaction reaches a controlled
collector and whether response or timing differentials indicate serialized-object
processing, capturing the canonical
[HTTP Timing](../../../schemas/http-timing.md) representation.

---

# Stage 5 — Record Observations And Evidence

Every check SHALL yield an [Observation](../../../schemas/observation.md) promoted
to [Evidence](../../../schemas/evidence.md). Only bounded probe interaction SHALL be
recorded, and sensitive content SHALL be redacted.

---

# Stage 6 — Analyze For Insecure Deserialization Weaknesses

The skill SHALL analyze the observations for insecure deserialization using
deterministic criteria and classify them using canonical weakness identifiers such as
CWE-502. Analysis SHALL be separate from observation.

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
- Analysis is separated from probing and observation.
- Confirmation uses only bounded probes and authorized collectors.

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
