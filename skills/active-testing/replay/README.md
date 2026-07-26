# Replay Capability

**File:** `skills/active-testing/replay/README.md`

**Version:** 1.0.0

---

# Purpose

The Replay Capability is an Active-Testing-tier capability that re-delivers previously recorded
traffic to an in-scope target and records the resulting responses within the Robust PenTest
Platform (RPP).

It reconstructs exchanges from recorded [Artifacts](../../../schemas/artifact.md), optionally
adjusting selected fields, and re-delivers them so that domain skills can observe deterministic,
reproducible target behavior. It performs delivery only through shared transport and produces no
Findings.

The Replay Capability consumes [Traffic Recording](../traffic-recording/README.md) artifacts,
drives the [HTTP Client](../../shared/http-client/README.md), gates every delivery through the
[Policy Engine](../../shared/policy-engine/README.md), and emits
[Observations](../../../schemas/observation.md), [Artifacts](../../../schemas/artifact.md), and
[Metrics](../../../schemas/metrics.md).

---

# Goals

The Replay Capability SHALL

- Reconstruct exchanges from recorded [Artifacts](../../../schemas/artifact.md)
- Re-deliver reconstructed requests to an in-scope target
- Support bounded field adjustment while preserving safety
- Consult the [Policy Engine](../../shared/policy-engine/README.md) before every delivery
- Emit [Observations](../../../schemas/observation.md),
  [Artifacts](../../../schemas/artifact.md), and [Metrics](../../../schemas/metrics.md)
- Remain implementation independent
- Produce no Findings or Risk

---

# Non-Goals

The Replay Capability SHALL NOT

- Issue requests directly rather than through the shared HTTP Client
- Interpret responses as vulnerabilities or produce Findings or Risk
- Replay destructive exchanges without an approved decision
- Perform denial of service or unbounded replay
- Invoke command-line tools or parse their output

Interpretation belongs to domain skills; recording belongs to Traffic Recording.

---

# Design Principles

The Replay Capability SHALL be

- Scope-confined and policy-gated
- Deterministic given the same recording and target behavior
- Bounded in volume and rate
- Non-destructive by default
- Implementation independent

---

# Architecture

```
Consuming Skill

↓

Replay Capability

├── Policy Gate            → Policy Engine
├── Recording Source       → Traffic Recording
├── Request Reconstructor
├── Field Adjuster
├── Delivery Requester     → HTTP Client
├── Response Recorder      → Observation
├── Artifact Emitter       → Artifact
└── Metrics Emitter        → Metrics

↓

Observations · Artifacts · Metrics
```

The Replay Capability re-delivers exchanges and SHALL remain unaware of the transport
implementation.

---

# Responsibilities

The Replay Capability is responsible for

- Consulting the [Policy Engine](../../shared/policy-engine/README.md) before each delivery
- Reconstructing requests from [Traffic Recording](../traffic-recording/README.md) artifacts
- Applying bounded, safety-preserving field adjustments
- Delivering through the [HTTP Client](../../shared/http-client/README.md)
- Recording responses and emitting
  [Observations](../../../schemas/observation.md),
  [Artifacts](../../../schemas/artifact.md), and [Metrics](../../../schemas/metrics.md)

---

# Inputs

```yaml
target:

recording_ref:

adjustments:

bounds:
  max_requests:
  rate_ceiling:

scope_id:

roe_id:
```

`target` SHALL be an in-scope endpoint. `recording_ref` references a recorded traffic Artifact.
`adjustments` specifies bounded field changes. `bounds` limits volume and rate.

---

# Outputs

Typical outputs MAY include

- Observations of replay responses
- Artifacts capturing replay interactions
- Metrics describing replay counts and timing

Outputs SHALL contain no Findings or Risk.

---

# Policy Enforcement

The Replay Capability SHALL consult the
[Policy Engine](../../shared/policy-engine/README.md) before every delivery. Replay is an
`active` action permitted only on an `allow` decision and within the attached rate ceiling. A
`requires_approval` decision, including for adjustments that could alter target state, SHALL
defer delivery. Replay SHALL be non-destructive by default and SHALL NOT cause denial of
service. Out-of-scope targets SHALL never be replayed against.

---

# Dependencies

The Replay Capability depends on

- [HTTP Client](../../shared/http-client/README.md)
- [Traffic Recording](../traffic-recording/README.md)
- [Policy Engine](../../shared/policy-engine/README.md)
- [Evidence](../../shared/evidence/README.md)
- [Observation Schema](../../../schemas/observation.md)
- [Artifact Schema](../../../schemas/artifact.md)
- [Metrics Schema](../../../schemas/metrics.md)

The Replay Capability SHALL NOT depend on domain skills.

---

# Consumers

Typical consumers include

- Web Security and API Security skills reproducing target behavior
- Traffic Comparison, which compares original and replayed exchanges

---

# Security Principles

The Replay Capability SHALL

- Act only within scope and Rules of Engagement, enforced by the Policy Engine
- Bound volume and rate and preserve non-destructive behavior
- Defer replay whose adjustments could alter target state
- Report responses as data, not findings
- Produce no Findings or Risk
- Preserve auditability

---

# Best Practices

Consumers SHOULD

- Provide an in-scope target and a recorded Artifact
- Keep adjustments minimal and bounded
- Route interpretation to domain skills
- Capture emitted Observations and Artifacts

---

# Anti-Patterns

Consumers SHOULD NOT

- Deliver requests directly
- Bypass the Policy Engine
- Replay unbounded volumes
- Expect vulnerability findings from this capability

---

# Documentation Requirements

This capability includes

- README.md
- capabilities.md
- interface.md
- configuration.md
- execution.md
- error-model.md
- examples.md
- adr/ADR-001-replay-capability.md

---

# Related Packages

- [Traffic Recording](../traffic-recording/README.md)
- [Traffic Comparison](../traffic-comparison/README.md)
- [HTTP Client](../../shared/http-client/README.md)
- [Policy Engine](../../shared/policy-engine/README.md)

---

# Canonical Schemas

- [Observation](../../../schemas/observation.md)
- [Artifact](../../../schemas/artifact.md)
- [Metrics](../../../schemas/metrics.md)

---

# Architecture Decisions

- [ADR-001 — Replay Capability](adr/ADR-001-replay-capability.md)

---

# Future Extensions

Future versions MAY support

- Session-aware sequenced replay
- Correlated multi-request replay
- Timing-faithful replay

Backward compatibility SHOULD be maintained.

---

# Success Criteria

A compliant Replay Capability re-delivers recorded exchanges through bounded, policy-gated,
non-destructive delivery and records responses as data, without interpreting them or producing
Findings or Risk.
