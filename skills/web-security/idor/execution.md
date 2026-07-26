# Insecure Direct Object Reference Execution Model

**File:** `skills/web-security/idor/execution.md`

**Version:** 1.0.0

---

# Purpose

This document defines the deterministic execution model of the Insecure Direct Object
Reference Skill, stage by stage. Given the same inputs, configuration, and application
behavior, execution SHALL be reproducible.

---

# Execution Overview

```
Validate Request

↓

Authorize (Policy Engine)

↓

Request Object References Across Controlled Identities (HTTP Client)

↓

Analyze Per-Object Authorization

↓

Record Observations → Evidence

↓

Analyze For IDOR Weaknesses

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
before every target-facing action. Cross-identity probing is an `active` action. Only
an `allow` decision permits the action, and the attached rate ceiling SHALL be
honored. A `requires_approval` decision SHALL defer the action until approval is
granted; a denial SHALL yield a `denied` status with no testing.

---

# Stage 3 — Request Object References Across Controlled Identities

Using two authorized controlled identities, the skill SHALL request each identity's
own object reference and then attempt the other identity's reference through the
[HTTP Client](../../shared/http-client/README.md). The skill SHALL use only controlled
identities and SHALL NOT perform requests directly.

---

# Stage 4 — Analyze Per-Object Authorization

The skill SHALL analyze whether the second identity is authorized to access the first
identity's object, and whether identifiers are predictable, using deterministic
criteria.

---

# Stage 5 — Record Observations And Evidence

Every check SHALL yield an [Observation](../../../schemas/observation.md) promoted
to [Evidence](../../../schemas/evidence.md). Only minimal controlled confirmation SHALL
be recorded, and sensitive content SHALL be redacted.

---

# Stage 6 — Analyze For IDOR Weaknesses

The skill SHALL analyze the observations for insecure direct object references using
deterministic criteria and classify them using canonical weakness identifiers such as
CWE-639. Analysis SHALL be separate from observation.

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
- Confirmation uses only controlled identities and minimal reads.

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
