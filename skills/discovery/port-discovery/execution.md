# Port Discovery Execution Model

**File:** `skills/discovery/port-discovery/execution.md`

**Version:** 1.0.0

---

# Purpose

This document defines the execution model for the Port Discovery Skill.

The execution model describes how the skill probes ports for a host and produces
canonical Assets, Relationships, Observations, Evidence, Findings, and Risk, gated
by the Policy Engine.

The model is deterministic given the same inputs and connectivity results.

---

# Execution Overview

```
Receive Host Target

↓

Resolve Configuration

↓

For Each Planned Probe:

  ├── Consult Policy Engine
  │     ├── deny → skip and record
  │     ├── requires_approval → route and defer
  │     └── allow → proceed (within rate ceiling)
  ├── Probe Port (TCP / UDP Client)
  ├── Classify State
  ├── Record Observation → Evidence
  └── Build Assets and Relationships

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

The skill SHALL resolve port sets, protocols, bounds, and analysis toggles using
the precedence defined in [configuration.md](configuration.md).

---

# Stage 2 — Policy Gating

Before every probe, the skill SHALL consult the
[Policy Engine](../../shared/policy-engine/README.md) with the target, the
`discovery` action class, and `active` intrusiveness.

- `deny` → the probe SHALL be skipped and recorded
- `requires_approval` → the probe SHALL be routed to approval and deferred
- `allow` → the probe SHALL proceed within the attached rate ceiling

Out-of-scope hosts SHALL never be probed.

---

# Stage 3 — Probing

The skill SHALL probe ports through the
[TCP Client](../../shared/tcp-client/README.md) and
[UDP Client](../../shared/udp-client/README.md), bounded by `max_ports`,
`max_concurrency`, and `per_port_timeout`.

The skill SHALL NOT perform socket input or output directly.

---

# Stage 4 — State Classification

The skill SHALL classify each port as open, closed, or filtered from the
connectivity result.

UDP no-response outcomes SHALL be classified conservatively as
open-or-filtered, consistent with the
[UDP Client](../../shared/udp-client/README.md) semantics.

---

# Stage 5 — Observation And Evidence

For each probe, the skill SHALL record an
[Observation](../../../schemas/observation.md) and promote corroborated
observations to [Evidence](../../../schemas/evidence.md).

---

# Stage 6 — Asset And Relationship Construction

For open ports, the skill SHALL build canonical `port` and `service`
[Assets](../../../schemas/asset.md) and `exposes` and `serves`
[Asset Relationships](../../../schemas/asset-relationship.md), deduplicating by
`canonical_key`.

Each Asset SHALL carry `scope_status` and provenance to its Evidence.

---

# Stage 7 — Weakness Analysis

Where enabled, the skill SHALL analyze exposed services for weaknesses such as
administrative or plaintext services and services outside a documented baseline.

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

Given identical inputs and connectivity results, the skill SHALL produce identical
Assets, Relationships, and Findings apart from timestamps and identifiers.

UDP results remain influenced by external delivery and are reflected in
port-state classification.

---

# Bounds And Pacing

Probing SHALL respect `max_ports`, `max_concurrency`, and the Policy Engine rate
ceiling enforced by the [Rate Limiter](../../shared/rate-limiter/README.md), so
that discovery does not disrupt the target.

---

# Interaction With Other Components

- The [Policy Engine](../../shared/policy-engine/README.md) authorizes every
  probe.
- The [TCP Client](../../shared/tcp-client/README.md) and
  [UDP Client](../../shared/udp-client/README.md) perform transport.
- The [Evidence](../../shared/evidence/README.md) package stores evidence.
- The Fingerprinting and TLS Analysis skills consume the produced service Assets.

---

# Failure Handling

Execution failures SHALL be classified according to
[error-model.md](error-model.md).

A denial or failure for one port SHALL NOT abort probing of other ports; the
outcome SHALL be `partial` where some probes did not complete.

---

# Execution Outputs

The execution model SHALL produce

- Domain-object references (Assets, Relationships, Observations, Findings)
- Probe metrics
- Evidence references

Outputs SHALL remain implementation independent.

---

# Related Documents

- [Interface](interface.md)
- [Configuration](configuration.md)
- [Error Model](error-model.md)
- [Policy Engine](../../shared/policy-engine/README.md)
- [TCP Client](../../shared/tcp-client/README.md)
- [Execution Model](../../core/execution-model.md)
