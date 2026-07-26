# REST API Security Execution Model

**File:** `skills/api-security/rest/execution.md`

**Version:** 1.0.0

---

# Purpose

This document defines the deterministic execution model of the REST API Security
Skill, stage by stage. Given the same inputs, configuration, and API behavior,
execution SHALL be reproducible.

---

# Execution Overview

```
Validate Request

↓

Authorize (Policy Engine)

↓

Exercise Operations Across Controlled Identities (HTTP Client)

↓

Analyze Object, Function, And Property Authorization

↓

Analyze Resource Consumption

↓

Record Observations → Evidence

↓

Analyze For API Security Weaknesses

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
before every target-facing action. API testing is an `active` action. Only an `allow`
decision permits the action, and the attached rate ceiling SHALL be honored. A
`requires_approval` decision SHALL defer the action until approval is granted; a
denial SHALL yield a `denied` status with no testing.

---

# Stage 3 — Exercise Operations Across Controlled Identities

Using two authorized controlled identities, the skill SHALL exercise REST operations
enumerated by the specification or discovered endpoints through the
[HTTP Client](../../shared/http-client/README.md), including cross-identity object
access and privileged-function attempts. The skill SHALL use only controlled
identities and SHALL NOT perform requests directly.

---

# Stage 4 — Analyze Object, Function, And Property Authorization

The skill SHALL analyze whether object level and function level authorization are
enforced across identities and whether protected properties can be modified or
over-exposed, using deterministic criteria.

---

# Stage 5 — Analyze Resource Consumption

The skill SHALL analyze whether pagination and rate limiting constrain resource
consumption using bounded probes.

---

# Stage 6 — Record Observations And Evidence

Every check SHALL yield an [Observation](../../../schemas/observation.md) promoted
to [Evidence](../../../schemas/evidence.md), capturing the canonical
[HTTP Transaction](../../../schemas/http-transaction.md). Only minimal controlled
confirmation SHALL be recorded, and sensitive content SHALL be redacted.

---

# Stage 7 — Analyze For API Security Weaknesses

The skill SHALL analyze the observations for API security weaknesses using
deterministic criteria and classify them using canonical identifiers and OWASP API
Security Top 10 (2023) references. Analysis SHALL be separate from observation.

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
- Analysis is separated from operation probing and observation.
- Authorization testing uses only controlled identities and minimal reads.

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
