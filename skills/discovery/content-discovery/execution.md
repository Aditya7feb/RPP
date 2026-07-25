# Content Discovery Execution Model

**File:** `skills/discovery/content-discovery/execution.md`

**Version:** 1.0.0

---

# Purpose

This document defines the execution model for the Content Discovery Skill.

The execution model describes how the skill enumerates web content for an
application and produces canonical Assets, Observations, Evidence, Findings, and
Risk, gated by the Policy Engine.

The model is deterministic given the same inputs and responses.

---

# Execution Overview

```
Receive Application Target

↓

Resolve Configuration

↓

For Each Candidate Path / Link:

  ├── Consult Policy Engine
  │     ├── deny → skip and record
  │     ├── requires_approval → route and defer
  │     └── allow → proceed (within rate ceiling)
  ├── Probe Path (HTTP Client)
  ├── Classify Response
  ├── Extract In-Scope Links
  ├── Record Observation → Evidence
  └── Build Endpoint Assets

↓

Analyze For Exposure Weaknesses

↓

Emit Findings and Risk

↓

Emit Events

↓

Return Result
```

---

# Stage 1 — Configuration Resolution

The skill SHALL resolve wordlists, crawl settings, bounds, and analysis toggles
using the precedence defined in [configuration.md](configuration.md).

---

# Stage 2 — Policy Gating

Before every request, the skill SHALL consult the
[Policy Engine](../../shared/policy-engine/README.md) with the target, the
`discovery` action class, and `active` intrusiveness.

- `deny` → the request SHALL be skipped and recorded
- `requires_approval` → the request SHALL be routed to approval and deferred
- `allow` → the request SHALL proceed within the attached rate ceiling

Out-of-scope applications SHALL never be probed.

---

# Stage 3 — Path Probing

The skill SHALL probe candidate paths through the
[HTTP Client](../../shared/http-client/README.md), bounded by `max_requests`,
`max_concurrency`, and `per_request_timeout`.

The skill SHALL NOT perform HTTP input or output directly.

---

# Stage 4 — Response Classification And Link Extraction

The skill SHALL classify responses to distinguish present, absent, and redirected
content, and SHALL extract in-scope links.

Only links whose scope evaluates to `in_scope` SHALL be enqueued for further
probing, bounded by `max_depth`.

---

# Stage 5 — Observation And Evidence

For each probe, the skill SHALL record an
[Observation](../../../schemas/observation.md) and promote corroborated
observations to [Evidence](../../../schemas/evidence.md), redacting sensitive
content per Rules of Engagement.

---

# Stage 6 — Asset And Relationship Construction

For present content, the skill SHALL build canonical `endpoint` and
`web-application` [Assets](../../../schemas/asset.md) and `serves` and
`references` [Asset Relationships](../../../schemas/asset-relationship.md),
deduplicating by `canonical_key`.

---

# Stage 7 — Weakness Analysis

Where enabled, the skill SHALL analyze responses for exposure weaknesses such as
directory listing, exposed backup files, and reachable administrative interfaces.

---

# Stage 8 — Finding And Risk Emission

For each confirmed weakness, the skill SHALL emit a
[Finding](../../../schemas/finding.md) referencing its Evidence and a
[Risk](../../../schemas/risk.md) scoring it.

A Finding SHALL NOT be emitted without supporting Evidence.

---

# Stage 9 — Events

The skill SHOULD emit lifecycle events to the Execution State.

---

# Determinism

Given identical inputs and responses, the skill SHALL produce identical Assets and
Findings apart from timestamps and identifiers.

---

# Bounds And Pacing

Probing SHALL respect `max_requests`, `max_concurrency`, `max_depth`, and the
Policy Engine rate ceiling enforced by the
[Rate Limiter](../../shared/rate-limiter/README.md).

---

# Interaction With Other Components

- The [Policy Engine](../../shared/policy-engine/README.md) authorizes every
  request.
- The [HTTP Client](../../shared/http-client/README.md) performs transport.
- The [Evidence](../../shared/evidence/README.md) package stores evidence.
- Fingerprinting, API Discovery, and Endpoint Enumeration consume the produced
  endpoints.

---

# Failure Handling

Execution failures SHALL be classified according to
[error-model.md](error-model.md).

A denial or failure for one path SHALL NOT abort probing of other paths; the
outcome SHALL be `partial` where some requests did not complete.

---

# Execution Outputs

The execution model SHALL produce

- Domain-object references (Assets, Relationships, Observations, Findings)
- Discovery metrics
- Evidence references

Outputs SHALL remain implementation independent.

---

# Related Documents

- [Interface](interface.md)
- [Configuration](configuration.md)
- [Error Model](error-model.md)
- [Policy Engine](../../shared/policy-engine/README.md)
- [HTTP Client](../../shared/http-client/README.md)
- [Execution Model](../../core/execution-model.md)
