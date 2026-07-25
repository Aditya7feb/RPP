# API Discovery Execution Model

**File:** `skills/discovery/api-discovery/execution.md`

**Version:** 1.0.0

---

# Purpose

This document defines the execution model for the API Discovery Skill.

The execution model describes how the skill discovers the API surface of a target
and produces canonical Assets, Observations, Evidence, Findings, and Risk, gated
by the Policy Engine.

The model is deterministic given the same inputs and responses.

---

# Execution Overview

```
Receive Application Target

↓

Resolve Configuration

↓

For Each Planned Request:

  ├── Consult Policy Engine
  │     ├── deny → skip and record
  │     ├── requires_approval → route and defer
  │     └── allow → proceed (within rate ceiling)
  ├── Locate Definitions / Detect GraphQL / Probe Base Paths (HTTP Client)
  ├── Record Observation → Evidence
  └── Build API and Endpoint Assets

↓

Analyze For API-Exposure Weaknesses

↓

Emit Findings and Risk

↓

Emit Events

↓

Return Result
```

---

# Stage 1 — Configuration Resolution

The skill SHALL resolve specification hints, GraphQL settings, base-path
candidates, bounds, and analysis toggles using the precedence defined in
[configuration.md](configuration.md).

---

# Stage 2 — Policy Gating

Before every request, the skill SHALL consult the
[Policy Engine](../../shared/policy-engine/README.md) with the target, the
`discovery` action class, and `active` intrusiveness. GraphQL introspection
queries SHALL be gated as active actions.

- `deny` → the request SHALL be skipped and recorded
- `requires_approval` → the request SHALL be routed to approval and deferred
- `allow` → the request SHALL proceed within the attached rate ceiling

Out-of-scope targets SHALL never be probed.

---

# Stage 3 — Definition Location

The skill SHALL retrieve candidate specification paths through the
[HTTP Client](../../shared/http-client/README.md) and identify OpenAPI or Swagger
documents.

Located specifications SHALL yield declared operations as candidate `endpoint`
Assets with provenance to the specification.

The skill SHALL NOT perform HTTP input or output directly.

---

# Stage 4 — GraphQL Detection

Where enabled, the skill SHALL detect GraphQL endpoints and, subject to policy,
determine whether introspection is exposed.

---

# Stage 5 — Base-Path Probing

The skill SHALL probe common API base paths and versions, bounded by
`max_requests`, `max_concurrency`, and `per_request_timeout`.

---

# Stage 6 — Observation And Evidence

For each request, the skill SHALL record an
[Observation](../../../schemas/observation.md) and promote corroborated
observations to [Evidence](../../../schemas/evidence.md), redacting sensitive
specification content per Rules of Engagement.

---

# Stage 7 — Asset And Relationship Construction

The skill SHALL build canonical `api` and `endpoint`
[Assets](../../../schemas/asset.md) and `serves` and `references`
[Asset Relationships](../../../schemas/asset-relationship.md), deduplicating by
`canonical_key`.

Each Asset SHALL carry `scope_status` and provenance to its Evidence.

---

# Stage 8 — Weakness Analysis

Where enabled, the skill SHALL analyze the API surface for exposure weaknesses
such as public specifications, enabled introspection, and debug endpoints.

---

# Stage 9 — Finding And Risk Emission

For each confirmed weakness, the skill SHALL emit a
[Finding](../../../schemas/finding.md) referencing its Evidence and a
[Risk](../../../schemas/risk.md) scoring it.

A Finding SHALL NOT be emitted without supporting Evidence.

---

# Stage 10 — Events

The skill SHOULD emit lifecycle events to the Execution State.

---

# Determinism

Given identical inputs and responses, the skill SHALL produce identical Assets and
Findings apart from timestamps and identifiers.

---

# Interaction With Other Components

- The [Policy Engine](../../shared/policy-engine/README.md) authorizes every
  request.
- The [HTTP Client](../../shared/http-client/README.md) performs transport.
- The [Evidence](../../shared/evidence/README.md) package stores evidence.
- API Security skills consume the produced API operations for testing.

---

# Failure Handling

Execution failures SHALL be classified according to
[error-model.md](error-model.md).

A denial or failure for one request SHALL NOT abort the discovery; the outcome
SHALL be `partial` where some requests did not complete.

---

# Execution Outputs

The execution model SHALL produce

- API and endpoint Assets
- Observations and Evidence references
- Findings with Risk where weaknesses are confirmed

Outputs SHALL remain implementation independent.

---

# Related Documents

- [Interface](interface.md)
- [Configuration](configuration.md)
- [Error Model](error-model.md)
- [Policy Engine](../../shared/policy-engine/README.md)
- [HTTP Client](../../shared/http-client/README.md)
- [Execution Model](../../core/execution-model.md)
