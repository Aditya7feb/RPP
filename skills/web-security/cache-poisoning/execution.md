# Web Cache Poisoning Execution Model

**File:** `skills/web-security/cache-poisoning/execution.md`

**Version:** 1.0.0

---

# Purpose

This document defines the deterministic execution model of the Web Cache Poisoning
Skill, stage by stage. Given the same inputs, configuration, and caching behavior,
execution SHALL be reproducible.

---

# Execution Overview

```
Validate Request

↓

Authorize (Policy Engine)

↓

Submit Bounded Probes Against Controlled Cache Key (HTTP Client)

↓

Analyze Unkeyed Input Reflection Into Cache

↓

Record Observations → Evidence

↓

Analyze For Cache Poisoning Weaknesses

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
before every target-facing action. Cache probing is an `active`, higher-impact
action. Only an `allow` decision permits the action, and the attached rate ceiling
SHALL be honored. A `requires_approval` decision SHALL defer the action until approval
is granted; a denial SHALL yield a `denied` status with no testing.

---

# Stage 3 — Submit Bounded Probes Against Controlled Cache Key

For authorized endpoints the skill SHALL submit bounded probes with candidate unkeyed
inputs, scoped to a controlled cache key, through the
[HTTP Client](../../shared/http-client/README.md), capturing the canonical
[HTTP Header](../../../schemas/http-header.md) representation. The skill SHALL NOT
poison a shared user-facing cache key and SHALL NOT perform requests directly.

---

# Stage 4 — Analyze Unkeyed Input Reflection Into Cache

The skill SHALL analyze whether unkeyed inputs are reflected into a cached response
under the controlled cache key and whether influential inputs are excluded from the
cache key, using deterministic criteria.

---

# Stage 5 — Record Observations And Evidence

Every check SHALL yield an [Observation](../../../schemas/observation.md) promoted
to [Evidence](../../../schemas/evidence.md). Only controlled-cache-key confirmation
SHALL be recorded, and sensitive content SHALL be redacted.

---

# Stage 6 — Analyze For Cache Poisoning Weaknesses

The skill SHALL analyze the observations for web cache poisoning using deterministic
criteria and classify them using canonical weakness identifiers such as CWE-444.
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
- Analysis is separated from probing and observation.
- Confirmation is scoped to a controlled cache key, never real users' entries.

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
