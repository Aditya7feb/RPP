# Log Collection Capability

**File:** `skills/evidence/log-collection/README.md`

**Version:** 1.0.0

---

# Purpose

The Log Collection Capability is an Evidence-tier capability that collects application, service,
and infrastructure logs as durable evidence within the Robust PenTest Platform (RPP).

It gathers authorized log events, records them as durable log evidence by reference, and preserves
their ordering. It performs no interpretation and produces no Findings.

The Log Collection Capability consumes the shared [Logging](../../shared/logging/README.md)
package, records [Artifacts](../../../schemas/artifact.md) referencing the
[Log Event](../../../schemas/log-event.md) schema, and invokes the shared
[Evidence](../../shared/evidence/README.md) lifecycle to promote log collections into durable
Evidence.

---

# Goals

The Log Collection Capability SHALL

- Collect application, service, and infrastructure log events as evidence
- Record collections as [Artifacts](../../../schemas/artifact.md) referencing the
  [Log Event](../../../schemas/log-event.md) schema
- Preserve log ordering
- Invoke the shared [Evidence](../../shared/evidence/README.md) lifecycle to promote collections
- Redact sensitive log content where configured
- Bound collection volume and window
- Emit [Metrics](../../../schemas/metrics.md) describing collected log counts
- Remain implementation independent
- Produce no Findings or Risk

---

# Non-Goals

The Log Collection Capability SHALL NOT

- Emit or store logs directly rather than through the shared Logging package
- Interpret log content or produce Findings or Risk
- Own durable persistence, integrity, or retention (that is the shared Evidence lifecycle)
- Collect logs from unauthorized sources
- Invoke command-line tools or parse their output

Log primitives belong to the shared Logging package; interpretation belongs to Domain Security
capabilities; the durable evidence lifecycle belongs to the shared Evidence infrastructure.

---

# Design Principles

The Log Collection Capability SHALL be

- Scope-confined to authorized sources
- Faithful to collected log events and their ordering
- Bounded in volume and window
- Redaction-aware
- Implementation independent

---

# Architecture

```
Consuming Skill Or Workflow

↓

Log Collection Capability

├── Source Confiner
├── Log Reader             → Logging
├── Order Preserver
├── Redactor
├── Artifact Writer        → Artifact (Log Event)
├── Evidence Promoter      → Evidence (shared lifecycle)
└── Metrics Emitter        → Metrics

↓

Artifacts · Evidence · Metrics
```

The Log Collection Capability collects log events and SHALL remain unaware of the logging
implementation.

---

# Responsibilities

The Log Collection Capability is responsible for

- Confining collection to authorized sources
- Reading log events through the shared [Logging](../../shared/logging/README.md) package
- Preserving ordering and recording collections as
  [Artifacts](../../../schemas/artifact.md)
- Invoking the shared [Evidence](../../shared/evidence/README.md) lifecycle to promote collections
- Emitting [Metrics](../../../schemas/metrics.md)

---

# Inputs

```yaml
sources:

window:
  start:
  end:

bounds:
  max_events:

redaction:

scope_id:

roe_id:
```

`sources` reference authorized log sources. `window` bounds the time range. `bounds` limits volume.

---

# Outputs

Typical outputs MAY include

- Artifacts of type `log-collection` referencing Log Events
- Evidence references produced through the shared lifecycle
- Metrics describing collected log counts

Outputs SHALL contain no Findings or Risk.

---

# Authorization

The Log Collection Capability SHALL collect only from authorized sources within the assessment
[Scope](../../../schemas/scope.md). Collection SHALL be bounded in volume and window. Unauthorized
sources SHALL never be collected.

---

# Dependencies

The Log Collection Capability depends on

- [Configuration Model](../../core/configuration-model.md)
- [Execution Model](../../core/execution-model.md)
- [Error Handling](../../core/error-handling.md)
- [Logging](../../shared/logging/README.md)
- [Evidence](../../shared/evidence/README.md)
- [Artifact Schema](../../../schemas/artifact.md)
- [Log Event Schema](../../../schemas/log-event.md)
- [Metrics Schema](../../../schemas/metrics.md)

The Log Collection Capability SHALL NOT depend on domain skills.

---

# Consumers

Typical consumers include

- Domain Security skills requiring log evidence
- Reporting, through promoted Evidence
- Timeline, which correlates collected log events

---

# Security Principles

The Log Collection Capability SHALL

- Collect only from authorized, in-scope sources
- Bound collection volume and window
- Redact sensitive log content where configured
- Produce no Findings or Risk
- Preserve auditability

---

# Best Practices

Consumers SHOULD

- Provide authorized sources and bounded windows
- Rely on the shared Evidence lifecycle for durability
- Route interpretation to Domain Security capabilities

---

# Anti-Patterns

Consumers SHOULD NOT

- Read or store logs directly
- Collect from unauthorized sources
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
- adr/ADR-001-log-collection-capability.md

---

# Related Packages

- [Logging](../../shared/logging/README.md)
- [Evidence](../../shared/evidence/README.md)
- [Timeline](../timeline/README.md)

---

# Canonical Schemas

- [Artifact](../../../schemas/artifact.md)
- [Log Event](../../../schemas/log-event.md)
- [Evidence](../../../schemas/evidence.md)
- [Metrics](../../../schemas/metrics.md)

---

# Architecture Decisions

- [ADR-001 — Log Collection Capability](adr/ADR-001-log-collection-capability.md)

---

# Future Extensions

Future versions MAY support

- Source-correlated collection
- Structured-field extraction policies
- Streaming log collection

Backward compatibility SHOULD be maintained.

---

# Success Criteria

A compliant Log Collection Capability collects authorized, in-scope log events within bounds,
preserves their ordering, and invokes the shared Evidence lifecycle for durability, without
interpreting content or producing Findings or Risk.
