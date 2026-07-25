# DNS Enumeration Execution Model

**File:** `skills/discovery/dns-enumeration/execution.md`

**Version:** 1.0.0

---

# Purpose

This document defines the execution model for the DNS Enumeration Skill.

The execution model describes how the skill enumerates DNS for a target and
produces canonical Assets, Relationships, Observations, Evidence, Findings, and
Risk, gated by the Policy Engine.

The model is deterministic given the same inputs and DNS responses.

---

# Execution Overview

```
Receive Target

↓

Resolve Configuration

↓

For Each Planned Action:

  ├── Consult Policy Engine
  │     ├── deny → skip and record
  │     ├── requires_approval → route and defer
  │     └── allow → proceed
  ├── Enumerate Records (DNS Client)
  ├── Record Observation → Evidence
  ├── Build Assets and Relationships
  └── Analyze For Weaknesses

↓

Emit Findings and Risk

↓

Emit Events

↓

Return Result
```

---

# Stage 1 — Configuration Resolution

The skill SHALL resolve record types, bounds, and analysis toggles using the
precedence defined in [configuration.md](configuration.md).

---

# Stage 2 — Policy Gating

Before every target-facing action, the skill SHALL consult the
[Policy Engine](../../shared/policy-engine/README.md) with the action target,
class, and intrusiveness.

- `deny` → the action SHALL be skipped and recorded
- `requires_approval` → the action SHALL be routed to approval and deferred
- `allow` → the action SHALL proceed, attaching the returned rate ceiling

Out-of-scope targets SHALL never be queried.

---

# Stage 3 — Record Enumeration

The skill SHALL enumerate records through the
[DNS Client](../../shared/dns-client/README.md), bounded by `max_names`,
`max_depth`, and `per_name_timeout`.

The skill SHALL NOT perform DNS input or output directly.

---

# Stage 4 — Observation And Evidence

For each result, the skill SHALL record an
[Observation](../../../schemas/observation.md) and promote corroborated
observations to [Evidence](../../../schemas/evidence.md) through the
[Evidence](../../shared/evidence/README.md) shared package.

---

# Stage 5 — Asset And Relationship Construction

The skill SHALL build canonical [Assets](../../../schemas/asset.md) and
[Asset Relationships](../../../schemas/asset-relationship.md), deduplicating by
`canonical_key` so that repeated discovery converges on one Asset.

Each Asset SHALL carry `scope_status` from the Scope evaluation and provenance to
its Observations and Evidence.

---

# Stage 6 — Weakness Analysis

Where enabled, the skill SHALL analyze results for weaknesses such as
zone-transfer exposure, dangling records, and broad wildcards.

Zone-transfer testing SHALL be treated as an `active` action and gated by the
Policy Engine.

---

# Stage 7 — Finding And Risk Emission

For each confirmed weakness, the skill SHALL emit a
[Finding](../../../schemas/finding.md) referencing its Evidence and a
[Risk](../../../schemas/risk.md) scoring it.

A Finding SHALL NOT be emitted without supporting Evidence.

---

# Stage 8 — Events

The skill SHOULD emit lifecycle events to the Execution State.

---

# Determinism

Given identical inputs and DNS responses, the skill SHALL produce identical
Assets, Relationships, and Findings apart from timestamps and identifiers.

---

# Recursion And Bounds

Recursive enumeration SHALL respect `max_depth` and `max_names`. Newly discovered
in-scope names MAY be enumerated within bounds; out-of-scope names SHALL be
recorded as Assets with `scope_status: out_of_scope` and SHALL NOT be queried.

---

# Interaction With Other Components

- The [Policy Engine](../../shared/policy-engine/README.md) authorizes every
  action.
- The [DNS Client](../../shared/dns-client/README.md) performs resolution.
- The [Evidence](../../shared/evidence/README.md) package stores evidence.
- Later Discovery skills consume the produced Assets.

---

# Failure Handling

Execution failures SHALL be classified according to
[error-model.md](error-model.md).

A denial or resolution failure for one name SHALL NOT abort enumeration of other
names; the outcome SHALL be `partial` where some actions did not complete.

---

# Execution Outputs

The execution model SHALL produce

- Domain-object references (Assets, Relationships, Observations, Findings)
- Enumeration metrics
- Evidence references

Outputs SHALL remain implementation independent.

---

# Related Documents

- [Interface](interface.md)
- [Configuration](configuration.md)
- [Error Model](error-model.md)
- [Policy Engine](../../shared/policy-engine/README.md)
- [DNS Client](../../shared/dns-client/README.md)
- [Execution Model](../../core/execution-model.md)
