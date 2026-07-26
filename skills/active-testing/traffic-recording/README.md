# Traffic Recording Capability

**File:** `skills/active-testing/traffic-recording/README.md`

**Version:** 1.0.0

---

# Purpose

The Traffic Recording Capability is an Active-Testing-tier capability that captures request and
response traffic exchanged with in-scope targets within the Robust PenTest Platform (RPP).

It records traffic passing through the platform's proxy into durable, referenced artifacts so
that replay, comparison, and domain skills can reuse exact interactions. It captures traffic as
data and produces no Findings.

The Traffic Recording Capability routes through the [Proxy](../../shared/proxy/README.md),
gates recording scope through the [Policy Engine](../../shared/policy-engine/README.md), and
emits [Artifacts](../../../schemas/artifact.md) and [Metrics](../../../schemas/metrics.md).

---

# Goals

The Traffic Recording Capability SHALL

- Capture request and response traffic for in-scope targets
- Store captured traffic as durable, referenced [Artifacts](../../../schemas/artifact.md)
- Redact sensitive content from stored traffic
- Bound capture volume and duration
- Emit [Artifacts](../../../schemas/artifact.md) and [Metrics](../../../schemas/metrics.md)
- Remain implementation independent
- Produce no Findings or Risk

---

# Non-Goals

The Traffic Recording Capability SHALL NOT

- Generate or deliver payloads (those are Payload Generation and Fuzzing)
- Replay recorded traffic (that is Replay)
- Interpret traffic or produce Findings or Risk
- Persist secrets in the clear
- Invoke command-line tools or parse their output

Replay belongs to the Replay capability; interpretation belongs to domain skills.

---

# Design Principles

The Traffic Recording Capability SHALL be

- Scope-confined and policy-gated
- Faithful to captured traffic
- Bounded in volume and duration
- Redaction-aware
- Implementation independent

---

# Architecture

```
Platform Traffic

↓

Traffic Recording Capability

├── Policy Gate            → Policy Engine
├── Capture Tap            → Proxy
├── Redactor
├── Artifact Writer        → Artifact
└── Metrics Emitter        → Metrics

↓

Artifacts · Metrics
```

The Traffic Recording Capability records exchanges and SHALL remain unaware of the proxy
implementation.

---

# Responsibilities

The Traffic Recording Capability is responsible for

- Consulting the [Policy Engine](../../shared/policy-engine/README.md) for recording scope
- Capturing traffic through the [Proxy](../../shared/proxy/README.md)
- Redacting sensitive content
- Writing durable [Artifacts](../../../schemas/artifact.md)
- Emitting [Metrics](../../../schemas/metrics.md)

---

# Inputs

```yaml
scope_selector:

bounds:
  max_transactions:
  max_duration:

redaction:

scope_id:

roe_id:
```

`scope_selector` selects which in-scope exchanges to record. `bounds` limits capture.
`redaction` configures sensitive-content removal.

---

# Outputs

Typical outputs MAY include

- Artifacts of type `traffic-recording`
- Metrics describing captured transaction counts and duration

Outputs SHALL contain no Findings or Risk.

---

# Policy Enforcement

The Traffic Recording Capability SHALL consult the
[Policy Engine](../../shared/policy-engine/README.md) to confirm that recording is authorized
for the selected in-scope exchanges. Recording SHALL be bounded and SHALL redact sensitive
content. Out-of-scope traffic SHALL never be recorded.

---

# Dependencies

The Traffic Recording Capability depends on

- [Proxy](../../shared/proxy/README.md)
- [Policy Engine](../../shared/policy-engine/README.md)
- [Evidence](../../shared/evidence/README.md)
- [Artifact Schema](../../../schemas/artifact.md)
- [Metrics Schema](../../../schemas/metrics.md)

The Traffic Recording Capability SHALL NOT depend on domain skills.

---

# Consumers

Typical consumers include

- The Replay and Traffic Comparison capabilities
- Domain skills reusing exact interactions

---

# Security Principles

The Traffic Recording Capability SHALL

- Record only authorized, in-scope traffic
- Bound capture volume and duration
- Redact sensitive content from stored artifacts
- Produce no Findings or Risk
- Preserve auditability

---

# Best Practices

Consumers SHOULD

- Scope recording narrowly
- Bound capture volume and duration
- Rely on stored Artifacts for replay and comparison

---

# Anti-Patterns

Consumers SHOULD NOT

- Record out-of-scope traffic
- Persist secrets in the clear
- Expect interpretation or findings from this capability

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
- adr/ADR-001-traffic-recording-capability.md

---

# Related Packages

- [Proxy](../../shared/proxy/README.md)
- [Replay](../replay/README.md)
- [Traffic Comparison](../traffic-comparison/README.md)

---

# Canonical Schemas

- [Artifact](../../../schemas/artifact.md)
- [Metrics](../../../schemas/metrics.md)

---

# Architecture Decisions

- [ADR-001 — Traffic Recording Capability](adr/ADR-001-traffic-recording-capability.md)

---

# Future Extensions

Future versions MAY support

- Selective field-level redaction policies
- Session-scoped capture grouping
- Streaming-protocol capture

Backward compatibility SHOULD be maintained.

---

# Success Criteria

A compliant Traffic Recording Capability captures authorized, in-scope traffic into redacted,
referenced artifacts within bounds, without interpreting it or producing Findings or Risk.
