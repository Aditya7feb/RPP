# XML External Entity Execution Model

**File:** `skills/web-security/xxe/execution.md`

**Version:** 1.0.0

---

# Purpose

This document defines the deterministic execution model of the XML External Entity
Skill, stage by stage. Given the same inputs, configuration, and application behavior,
execution SHALL be reproducible.

---

# Execution Overview

```
Validate Request

↓

Authorize (Policy Engine)

↓

Submit Bounded Entity Probes (HTTP Client)

↓

Observe In-Band And Out-Of-Band Resolution

↓

Record Observations → Evidence

↓

Analyze For XXE Weaknesses

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
before every target-facing action. Entity probing is an `active`, high-impact action.
Only an `allow` decision permits the action, and the attached rate ceiling SHALL be
honored. A `requires_approval` decision SHALL defer the action until approval is
granted; a denial SHALL yield a `denied` status with no testing.

---

# Stage 3 — Submit Bounded Entity Probes

For authorized XML endpoints the skill SHALL submit bounded entity probes referencing
a non-sensitive marker or a controlled collector through the
[HTTP Client](../../shared/http-client/README.md). The skill SHALL NOT reference
sensitive files and SHALL NOT perform requests directly.

---

# Stage 4 — Observe In-Band And Out-Of-Band Resolution

The skill SHALL observe whether the non-sensitive entity is resolved in the response
and, where a controlled collector is authorized, whether an out-of-band interaction
occurs.

---

# Stage 5 — Record Observations And Evidence

Every check SHALL yield an [Observation](../../../schemas/observation.md) promoted
to [Evidence](../../../schemas/evidence.md). Only the non-sensitive resolution signal
SHALL be recorded, and any incidental sensitive content SHALL be redacted.

---

# Stage 6 — Analyze For XXE Weaknesses

The skill SHALL analyze the observations for unsafe external-entity resolution using
deterministic criteria and classify them using canonical weakness identifiers such as
CWE-611. Analysis SHALL be separate from observation.

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
- Confirmation references only non-sensitive or controlled resources.

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
