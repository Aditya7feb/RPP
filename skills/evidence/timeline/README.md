# Timeline Capability

**File:** `skills/evidence/timeline/README.md`

**Version:** 1.0.0

---

# Purpose

The Timeline Capability is an Evidence-tier capability that correlates Observations and Evidence
into a chronological, causal timeline within the Robust PenTest Platform (RPP).

It assembles referenced Observations and Evidence into an ordered timeline that preserves
chronology and causal relationships. **Timeline is descriptive, not analytical**: it correlates
what happened and when, and does not interpret, classify, or prioritize.

The Timeline Capability emits a timeline [Artifact](../../../schemas/artifact.md) and
[Metrics](../../../schemas/metrics.md), and MAY invoke the shared
[Evidence](../../shared/evidence/README.md) lifecycle to promote the timeline into durable
Evidence.

---

# Goals

The Timeline Capability SHALL

- Preserve chronology across referenced Observations and Evidence
- Correlate Observations
- Correlate Evidence
- Maintain causal relationships between correlated items
- Emit a timeline [Artifact](../../../schemas/artifact.md) referencing canonical objects by ID
- Emit [Metrics](../../../schemas/metrics.md) describing correlation counts
- Remain implementation independent
- Produce no Findings or Risk

---

# Non-Goals

The Timeline Capability SHALL NOT

- Infer vulnerabilities
- Classify Findings
- Prioritize Risk
- Perform security analysis
- Interpret the meaning of correlated items
- Duplicate referenced Observations or Evidence

Interpretation, vulnerability inference, Finding generation, and Risk prioritization belong to
Domain Security capabilities. Timeline is descriptive correlation only.

---

# Design Principles

The Timeline Capability SHALL be

- Descriptive, not analytical
- Deterministic given the same references
- Reference-based rather than duplicating content
- Chronology- and causality-preserving
- Implementation independent

---

# Architecture

```
Consuming Skill Or Workflow

↓

Timeline Capability

├── Reference Loader       (Observation / Evidence refs)
├── Chronology Orderer
├── Correlator
├── Causal Linker
├── Timeline Writer        → Artifact
├── Evidence Promoter      → Evidence (shared lifecycle)
└── Metrics Emitter        → Metrics

↓

Timeline Artifact · Evidence · Metrics
```

The Timeline Capability correlates references and SHALL NOT interpret their security meaning.

---

# Responsibilities

The Timeline Capability is responsible for

- Loading referenced [Observations](../../../schemas/observation.md) and
  [Evidence](../../../schemas/evidence.md)
- Ordering them chronologically and correlating them
- Maintaining causal relationships
- Emitting a timeline [Artifact](../../../schemas/artifact.md) that references canonical objects by
  ID
- Emitting [Metrics](../../../schemas/metrics.md)

---

# Inputs

```yaml
observation_refs:

evidence_refs:

correlation:
  causal_links:

bounds:
  max_items:
```

`observation_refs` and `evidence_refs` reference the items to correlate. `correlation` configures
causal linking. `bounds` limits timeline size.

---

# Outputs

Typical outputs MAY include

- A timeline Artifact of type `timeline` referencing Observation and Evidence IDs
- Evidence references produced through the shared lifecycle
- Metrics describing correlation counts

Outputs SHALL contain no Findings or Risk and SHALL NOT contain security interpretation.

---

# Dependencies

The Timeline Capability depends on

- [Configuration Model](../../core/configuration-model.md)
- [Execution Model](../../core/execution-model.md)
- [Error Handling](../../core/error-handling.md)
- [Evidence](../../shared/evidence/README.md)
- [Artifact Schema](../../../schemas/artifact.md)
- [Observation Schema](../../../schemas/observation.md)
- [Metrics Schema](../../../schemas/metrics.md)

The Timeline Capability SHALL NOT depend on domain skills.

---

# Consumers

Typical consumers include

- Domain Security skills interpreting a correlated sequence of events
- Reporting, through the promoted timeline Evidence

---

# Security Principles

The Timeline Capability SHALL

- Correlate only referenced Observations and Evidence
- Preserve chronology and causal relationships faithfully
- Reference canonical objects by ID rather than duplicating them
- Perform no interpretation, classification, prioritization, or analysis
- Produce no Findings or Risk
- Preserve auditability

---

# Best Practices

Consumers SHOULD

- Provide relevant Observation and Evidence references
- Rely on the timeline for correlation only
- Route interpretation to Domain Security capabilities

---

# Anti-Patterns

Consumers SHOULD NOT

- Expect vulnerability inference, findings, or risk from this capability
- Expect security analysis from this capability
- Duplicate referenced content into the timeline

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
- adr/ADR-001-timeline-capability.md

---

# Related Packages

- [Evidence](../../shared/evidence/README.md)
- [HTTP Archive](../http-archive/README.md)
- [Network Trace](../network-trace/README.md)

---

# Canonical Schemas

- [Artifact](../../../schemas/artifact.md)
- [Observation](../../../schemas/observation.md)
- [Evidence](../../../schemas/evidence.md)
- [Metrics](../../../schemas/metrics.md)

---

# Architecture Decisions

- [ADR-001 — Timeline Capability](adr/ADR-001-timeline-capability.md)

---

# Future Extensions

Future versions MAY support

- Multi-assessment timeline correlation
- Causal-graph export
- Tolerance windows for correlation

Backward compatibility SHOULD be maintained.

---

# Success Criteria

A compliant Timeline Capability correlates Observations and Evidence into a chronological, causal
timeline that references canonical objects by ID, remaining descriptive and never inferring
vulnerabilities, classifying Findings, prioritizing Risk, or performing security analysis.
