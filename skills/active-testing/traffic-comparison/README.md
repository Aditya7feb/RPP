# Traffic Comparison Capability

**File:** `skills/active-testing/traffic-comparison/README.md`

**Version:** 1.0.0

---

# Purpose

The Traffic Comparison Capability is an Active-Testing-tier capability that compares two
recorded traffic sets and produces a structured difference within the Robust PenTest Platform
(RPP).

It analyzes recorded [Artifacts](../../../schemas/artifact.md) — such as a baseline recording
and a replayed recording — and emits a difference artifact describing status, header, timing,
and body variations for domain skills to interpret. It contacts no target and produces no
Findings.

The Traffic Comparison Capability consumes recorded
[Artifacts](../../../schemas/artifact.md) and emits a difference
[Artifact](../../../schemas/artifact.md) and [Metrics](../../../schemas/metrics.md).

---

# Goals

The Traffic Comparison Capability SHALL

- Compare two recorded traffic sets across status, headers, timing, and body
- Produce a structured difference [Artifact](../../../schemas/artifact.md)
- Emit [Metrics](../../../schemas/metrics.md) describing difference counts
- Redact sensitive content in difference output
- Remain implementation independent
- Produce no Findings or Risk

---

# Non-Goals

The Traffic Comparison Capability SHALL NOT

- Contact targets or perform any network action
- Record or replay traffic (those are Traffic Recording and Replay)
- Interpret differences as vulnerabilities or produce Findings or Risk
- Persist secrets in the clear
- Invoke command-line tools or parse their output

Interpretation of differences belongs to domain skills; recording and replay belong to their
capabilities.

---

# Design Principles

The Traffic Comparison Capability SHALL be

- Deterministic given the same input recordings
- Bounded in comparison scope
- Redaction-aware
- Non-target-facing
- Implementation independent

---

# Architecture

```
Consuming Skill

↓

Traffic Comparison Capability

├── Recording Loader
├── Aligner
├── Difference Analyzer
├── Redactor
├── Difference Artifact Emitter  → Artifact
└── Metrics Emitter              → Metrics

↓

Difference Artifact · Metrics
```

The Traffic Comparison Capability analyzes stored data and SHALL contact no target.

---

# Responsibilities

The Traffic Comparison Capability is responsible for

- Loading two recorded [Artifacts](../../../schemas/artifact.md)
- Aligning corresponding exchanges
- Computing status, header, timing, and body differences
- Redacting sensitive content
- Emitting a difference [Artifact](../../../schemas/artifact.md) and
  [Metrics](../../../schemas/metrics.md)

---

# Inputs

```yaml
baseline_ref:

candidate_ref:

comparison:
  dimensions:

bounds:
  max_transactions:
```

`baseline_ref` and `candidate_ref` reference recorded traffic Artifacts. `comparison.dimensions`
selects the compared dimensions. `bounds` limits comparison scope.

---

# Outputs

Typical outputs MAY include

- A difference Artifact of type `traffic-diff`
- Metrics describing difference counts by dimension

Outputs SHALL contain no Findings or Risk.

---

# Dependencies

The Traffic Comparison Capability depends on

- [Configuration Model](../../core/configuration-model.md)
- [Execution Model](../../core/execution-model.md)
- [Error Handling](../../core/error-handling.md)
- [Evidence](../../shared/evidence/README.md)
- [Artifact Schema](../../../schemas/artifact.md)
- [Metrics Schema](../../../schemas/metrics.md)

The Traffic Comparison Capability SHALL NOT depend on domain skills.

---

# Consumers

Typical consumers include

- Web Security and API Security skills interpreting behavioral differences
- Workflows correlating baseline and replayed behavior

---

# Security Principles

The Traffic Comparison Capability SHALL

- Perform no target-facing action
- Bound comparison scope
- Redact sensitive content in difference output
- Produce no Findings or Risk
- Preserve auditability

---

# Best Practices

Consumers SHOULD

- Provide comparable, redacted recordings
- Bound comparison scope
- Route interpretation of differences to domain skills

---

# Anti-Patterns

Consumers SHOULD NOT

- Expect target interaction from this capability
- Expect vulnerability findings from this capability
- Persist secrets in difference output

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
- adr/ADR-001-traffic-comparison-capability.md

---

# Related Packages

- [Traffic Recording](../traffic-recording/README.md)
- [Replay](../replay/README.md)

---

# Canonical Schemas

- [Artifact](../../../schemas/artifact.md)
- [Metrics](../../../schemas/metrics.md)

---

# Architecture Decisions

- [ADR-001 — Traffic Comparison Capability](adr/ADR-001-traffic-comparison-capability.md)

---

# Future Extensions

Future versions MAY support

- Semantic body diffing
- Tolerance policies for expected variation
- Multi-way comparison

Backward compatibility SHOULD be maintained.

---

# Success Criteria

A compliant Traffic Comparison Capability produces a deterministic, redacted, structured
difference between two recordings without contacting targets, interpreting differences, or
producing Findings or Risk.
