# GraphQL API Security Execution Model

**File:** `skills/api-security/graphql/execution.md`

**Version:** 1.0.0

---

# Purpose

This document defines the deterministic execution model of the GraphQL API Security
Skill, stage by stage. Given the same inputs, configuration, and API behavior,
execution SHALL be reproducible.

---

# Execution Overview

```
Validate Request

↓

Authorize (Policy Engine)

↓

Submit Bounded Queries Across Controlled Identities (HTTP Client)

↓

Analyze Introspection, Depth, Authorization, And Batching

↓

Record Observations → Evidence

↓

Analyze For GraphQL Security Weaknesses

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
before every target-facing action. Query probing is an `active` action. Only an
`allow` decision permits the action, and the attached rate ceiling SHALL be honored. A
`requires_approval` decision SHALL defer the action until approval is granted; a
denial SHALL yield a `denied` status with no testing.

---

# Stage 3 — Submit Bounded Queries Across Controlled Identities

Using two authorized controlled identities, the skill SHALL submit bounded GraphQL
queries — including an introspection query and depth- and complexity-bounded probes —
through the [HTTP Client](../../shared/http-client/README.md). Depth and complexity
SHALL be bounded to avoid denial of service, and the skill SHALL NOT perform requests
directly.

---

# Stage 4 — Analyze Introspection, Depth, Authorization, And Batching

The skill SHALL analyze whether introspection is enabled, whether depth and complexity
limits are enforced, whether field- and object-level authorization is enforced across
identities, and whether batching or alias amplification is constrained, using
deterministic criteria.

---

# Stage 5 — Record Observations And Evidence

Every check SHALL yield an [Observation](../../../schemas/observation.md) promoted
to [Evidence](../../../schemas/evidence.md), capturing the canonical
[HTTP Transaction](../../../schemas/http-transaction.md). Only bounded, minimal
confirmation SHALL be recorded, and sensitive content SHALL be redacted.

---

# Stage 6 — Analyze For GraphQL Security Weaknesses

The skill SHALL analyze the observations for GraphQL security weaknesses using
deterministic criteria and classify them using canonical identifiers and OWASP API
Security Top 10 (2023) references. Analysis SHALL be separate from observation.

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
- Analysis is separated from query probing and observation.
- Depth and complexity probes are bounded and reproducible.

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
