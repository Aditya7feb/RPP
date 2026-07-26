# Network Trace Capability

**File:** `skills/evidence/network-trace/README.md`

**Version:** 1.0.0

---

# Purpose

The Network Trace Capability is an Evidence-tier capability that collects transport-level network
evidence — packet and flow captures — for in-scope targets within the Robust PenTest Platform
(RPP).

It captures network traffic at the transport layer and records it as durable network evidence by
reference. It performs no interpretation and produces no Findings.

The Network Trace Capability drives the shared [TCP Client](../../shared/tcp-client/README.md) and
[UDP Client](../../shared/udp-client/README.md), gates every target-facing action through the
[Policy Engine](../../shared/policy-engine/README.md), emits
[Artifacts](../../../schemas/artifact.md), and invokes the shared
[Evidence](../../shared/evidence/README.md) lifecycle to promote traces into durable Evidence.

---

# Goals

The Network Trace Capability SHALL

- Capture packet and flow-level network evidence for in-scope targets
- Record captures as [Artifacts](../../../schemas/artifact.md) of type `network-trace`
- Consult the [Policy Engine](../../shared/policy-engine/README.md) before every capture
- Invoke the shared [Evidence](../../shared/evidence/README.md) lifecycle to promote traces
- Redact sensitive payload content where configured
- Bound capture volume and duration
- Emit [Metrics](../../../schemas/metrics.md) describing captured flow counts
- Remain implementation independent
- Produce no Findings or Risk

---

# Non-Goals

The Network Trace Capability SHALL NOT

- Open transport connections directly rather than through the shared transport clients
- Interpret captured traffic or produce Findings or Risk
- Own durable persistence, integrity, or retention (that is the shared Evidence lifecycle)
- Capture out-of-scope traffic
- Invoke command-line tools or parse their output

Transport belongs to the shared TCP and UDP clients; interpretation belongs to Domain Security
capabilities; the durable evidence lifecycle belongs to the shared Evidence infrastructure.

---

# Design Principles

The Network Trace Capability SHALL be

- Scope-confined and policy-gated
- Faithful to captured traffic
- Bounded in volume and duration
- Redaction-aware
- Implementation independent

---

# Architecture

```
Consuming Skill Or Workflow

↓

Network Trace Capability

├── Policy Gate            → Policy Engine
├── Flow Capturer          → TCP Client / UDP Client
├── Redactor
├── Trace Writer           → Artifact
├── Evidence Promoter      → Evidence (shared lifecycle)
└── Metrics Emitter        → Metrics

↓

Artifacts · Evidence · Metrics
```

The Network Trace Capability captures flows and SHALL remain unaware of the transport
implementation.

---

# Responsibilities

The Network Trace Capability is responsible for

- Consulting the [Policy Engine](../../shared/policy-engine/README.md) before each capture
- Capturing packet and flow evidence through the
  [TCP Client](../../shared/tcp-client/README.md) and
  [UDP Client](../../shared/udp-client/README.md)
- Recording captures as [Artifacts](../../../schemas/artifact.md)
- Invoking the shared [Evidence](../../shared/evidence/README.md) lifecycle to promote traces
- Emitting [Metrics](../../../schemas/metrics.md)

---

# Inputs

```yaml
target:

selection:
  protocols:
  ports:

bounds:
  max_flows:
  max_duration:

redaction:

scope_id:

roe_id:
```

`target` SHALL be an in-scope host or service. `selection` selects protocols and ports. `bounds`
limits capture. `redaction` configures payload removal.

---

# Outputs

Typical outputs MAY include

- Artifacts of type `network-trace`
- Evidence references produced through the shared lifecycle
- Metrics describing captured flow counts

Outputs SHALL contain no Findings or Risk.

---

# Policy Enforcement

The Network Trace Capability SHALL consult the
[Policy Engine](../../shared/policy-engine/README.md) before every capture. Capture is an `active`
action permitted only on an `allow` decision. A `requires_approval` decision SHALL defer the
capture. Capture SHALL be bounded in volume and duration. Out-of-scope traffic SHALL never be
captured.

---

# Dependencies

The Network Trace Capability depends on

- [Configuration Model](../../core/configuration-model.md)
- [Execution Model](../../core/execution-model.md)
- [Error Handling](../../core/error-handling.md)
- [TCP Client](../../shared/tcp-client/README.md)
- [UDP Client](../../shared/udp-client/README.md)
- [Policy Engine](../../shared/policy-engine/README.md)
- [Evidence](../../shared/evidence/README.md)
- [Artifact Schema](../../../schemas/artifact.md)
- [Metrics Schema](../../../schemas/metrics.md)

The Network Trace Capability SHALL NOT depend on domain skills.

---

# Consumers

Typical consumers include

- Domain Security skills requiring transport-level evidence
- Reporting, through promoted Evidence
- Timeline, which correlates captured flows

---

# Security Principles

The Network Trace Capability SHALL

- Act only within scope and Rules of Engagement, enforced by the Policy Engine
- Bound capture volume and duration and preserve non-destructive behavior
- Redact sensitive payload content where configured
- Produce no Findings or Risk
- Preserve auditability

---

# Best Practices

Consumers SHOULD

- Provide in-scope targets and bounded capture selection
- Rely on the shared Evidence lifecycle for durability
- Route interpretation to Domain Security capabilities

---

# Anti-Patterns

Consumers SHOULD NOT

- Open transport connections directly
- Bypass the Policy Engine
- Capture out-of-scope traffic
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
- adr/ADR-001-network-trace-capability.md

---

# Related Packages

- [TCP Client](../../shared/tcp-client/README.md)
- [UDP Client](../../shared/udp-client/README.md)
- [Evidence](../../shared/evidence/README.md)
- [Timeline](../timeline/README.md)

---

# Canonical Schemas

- [Artifact](../../../schemas/artifact.md)
- [Evidence](../../../schemas/evidence.md)
- [Metrics](../../../schemas/metrics.md)

---

# Architecture Decisions

- [ADR-001 — Network Trace Capability](adr/ADR-001-network-trace-capability.md)

---

# Future Extensions

Future versions MAY support

- Flow-level metadata summaries
- Encrypted-flow metadata capture
- Capture-filter policies

Backward compatibility SHOULD be maintained.

---

# Success Criteria

A compliant Network Trace Capability captures faithful, policy-gated, bounded transport-level
evidence and invokes the shared Evidence lifecycle for durability, without interpreting traffic or
producing Findings or Risk.
