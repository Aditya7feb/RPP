# Fuzzing Capability

**File:** `skills/active-testing/fuzzing/README.md`

**Version:** 1.0.0

---

# Purpose

The Fuzzing Capability is an Active-Testing-tier capability that delivers bounded sequences of
generated inputs to an in-scope target and records the target's responses within the Robust
PenTest Platform (RPP).

It drives payload delivery across a target surface, capturing responses and behavioral signals
as observations and artifacts for domain skills to interpret. It performs delivery only through
shared transport and produces no Findings.

The Fuzzing Capability consumes [Payload Generation](../payload-generation/README.md) and the
[Mutation Engine](../mutation-engine/README.md), drives the
[HTTP Client](../../shared/http-client/README.md), gates every delivery through the
[Policy Engine](../../shared/policy-engine/README.md), and emits
[Observations](../../../schemas/observation.md), [Artifacts](../../../schemas/artifact.md), and
[Metrics](../../../schemas/metrics.md).

---

# Goals

The Fuzzing Capability SHALL

- Deliver bounded sequences of [Payloads](../../../schemas/payload.md) to a target surface
- Record responses and behavioral signals as observations and artifacts
- Consult the [Policy Engine](../../shared/policy-engine/README.md) before every delivery
- Preserve non-destructive behavior and gate destructive payloads through approval
- Emit [Observations](../../../schemas/observation.md),
  [Artifacts](../../../schemas/artifact.md), and [Metrics](../../../schemas/metrics.md)
- Remain implementation independent
- Produce no Findings or Risk

---

# Non-Goals

The Fuzzing Capability SHALL NOT

- Issue requests directly rather than through the shared HTTP Client
- Interpret responses as vulnerabilities or produce Findings or Risk
- Deliver destructive payloads without an approved decision
- Perform denial of service or unbounded flooding
- Invoke command-line tools or parse their output

Interpretation of responses belongs to domain skills; weakness classification belongs to Web
Security and API Security skills.

---

# Design Principles

The Fuzzing Capability SHALL be

- Scope-confined and policy-gated
- Deterministic given the same corpus and target behavior
- Bounded in request volume and rate
- Non-destructive by default
- Implementation independent

---

# Architecture

```
Consuming Skill

↓

Fuzzing Capability

├── Policy Gate            → Policy Engine
├── Corpus Source          → Payload Generation / Mutation Engine
├── Delivery Requester     → HTTP Client
├── Response Recorder      → Observation
├── Artifact Emitter       → Artifact
└── Metrics Emitter        → Metrics

↓

Observations · Artifacts · Metrics
```

The Fuzzing Capability observes response signals and SHALL remain unaware of the transport
implementation.

---

# Responsibilities

The Fuzzing Capability is responsible for

- Consulting the [Policy Engine](../../shared/policy-engine/README.md) before each delivery
- Sourcing a corpus through [Payload Generation](../payload-generation/README.md) and the
  [Mutation Engine](../mutation-engine/README.md)
- Delivering payloads through the [HTTP Client](../../shared/http-client/README.md)
- Recording responses and behavioral signals
- Emitting [Observations](../../../schemas/observation.md),
  [Artifacts](../../../schemas/artifact.md), and [Metrics](../../../schemas/metrics.md)

---

# Inputs

```yaml
target:

surface:

corpus_ref:

bounds:
  max_requests:
  rate_ceiling:

scope_id:

roe_id:
```

`target` SHALL be an in-scope endpoint. `surface` identifies the injection points. `corpus_ref`
references generated Payloads. `bounds` limits request volume and rate.

---

# Outputs

Typical outputs MAY include

- Observations of responses and behavioral signals
- Artifacts capturing request and response interactions
- Metrics describing delivery counts, timing, and coverage

Outputs SHALL contain no Findings or Risk.

---

# Policy Enforcement

The Fuzzing Capability SHALL consult the
[Policy Engine](../../shared/policy-engine/README.md) before every delivery. Delivery is an
`active` action permitted only on an `allow` decision and within the attached rate ceiling.
A `requires_approval` decision, including for any payload marked `requires_approval`, SHALL
defer delivery. Delivery SHALL be non-destructive by default and SHALL NOT cause denial of
service. Out-of-scope targets SHALL never be fuzzed.

---

# Dependencies

The Fuzzing Capability depends on

- [HTTP Client](../../shared/http-client/README.md)
- [Payload Generation](../payload-generation/README.md)
- [Mutation Engine](../mutation-engine/README.md)
- [Policy Engine](../../shared/policy-engine/README.md)
- [Evidence](../../shared/evidence/README.md)
- [Observation Schema](../../../schemas/observation.md)
- [Artifact Schema](../../../schemas/artifact.md)
- [Metrics Schema](../../../schemas/metrics.md)

The Fuzzing Capability SHALL NOT depend on domain skills.

---

# Consumers

Typical consumers include

- Web Security and API Security skills requiring response corpora to interpret
- Replay, which reuses recorded fuzzing interactions

---

# Security Principles

The Fuzzing Capability SHALL

- Act only within scope and Rules of Engagement, enforced by the Policy Engine
- Bound request volume and rate and preserve non-destructive behavior
- Defer any payload marked as requiring approval
- Report responses as data, not findings
- Produce no Findings or Risk
- Preserve auditability

---

# Best Practices

Consumers SHOULD

- Provide an in-scope target and a bounded, generated corpus
- Rely on the capability for delivery and recording only
- Route interpretation and weakness classification to domain skills
- Capture emitted Observations and Artifacts

---

# Anti-Patterns

Consumers SHOULD NOT

- Deliver payloads directly
- Bypass the Policy Engine
- Request unbounded flooding
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
- adr/ADR-001-fuzzing-capability.md

---

# Related Packages

- [Payload Generation](../payload-generation/README.md)
- [Mutation Engine](../mutation-engine/README.md)
- [HTTP Client](../../shared/http-client/README.md)
- [Policy Engine](../../shared/policy-engine/README.md)

---

# Canonical Schemas

- [Observation](../../../schemas/observation.md)
- [Artifact](../../../schemas/artifact.md)
- [Metrics](../../../schemas/metrics.md)

---

# Architecture Decisions

- [ADR-001 — Fuzzing Capability](adr/ADR-001-fuzzing-capability.md)

---

# Future Extensions

Future versions MAY support

- Coverage-guided delivery feedback
- Stateful sequence fuzzing
- Response-clustering summaries

Backward compatibility SHOULD be maintained.

---

# Success Criteria

A compliant Fuzzing Capability delivers bounded, policy-gated, non-destructive payload
sequences and records responses as data, without interpreting them or producing Findings or
Risk.
