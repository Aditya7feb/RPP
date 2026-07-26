# HTTP Archive Capability

**File:** `skills/evidence/http-archive/README.md`

**Version:** 1.0.0

---

# Purpose

The HTTP Archive Capability is an Evidence-tier capability that collects and archives HTTP
request and response evidence for in-scope targets within the Robust PenTest Platform (RPP).

It captures HTTP transactions — including full request and response detail — and records them as
durable HTTP evidence in archive form (such as HAR). It performs no interpretation and produces no
Findings.

The HTTP Archive Capability drives the [HTTP Client](../../shared/http-client/README.md) and may
route through the [Proxy](../../shared/proxy/README.md), gates every target-facing action through
the [Policy Engine](../../shared/policy-engine/README.md), emits
[Artifacts](../../../schemas/artifact.md) referencing
[HTTP Transactions](../../../schemas/http-transaction.md), and invokes the shared
[Evidence](../../shared/evidence/README.md) lifecycle to promote archives into durable Evidence.

---

# Goals

The HTTP Archive Capability SHALL

- Collect HTTP request and response transactions for in-scope targets
- Record transactions as [Artifacts](../../../schemas/artifact.md) in archive form such as HAR
- Reference the canonical [HTTP Transaction](../../../schemas/http-transaction.md) schema
- Consult the [Policy Engine](../../shared/policy-engine/README.md) before every request
- Invoke the shared [Evidence](../../shared/evidence/README.md) lifecycle to promote archives
- Redact sensitive request and response content
- Emit [Metrics](../../../schemas/metrics.md) describing archived transaction counts
- Remain implementation independent
- Produce no Findings or Risk

---

# Non-Goals

The HTTP Archive Capability SHALL NOT

- Issue requests directly rather than through the shared HTTP Client
- Interpret transactions or produce Findings or Risk
- Own durable persistence, integrity, or retention (that is the shared Evidence lifecycle)
- Archive out-of-scope traffic
- Invoke command-line tools or parse their output

Transport belongs to the shared HTTP Client and Proxy; interpretation belongs to Domain Security
capabilities; the durable evidence lifecycle belongs to the shared Evidence infrastructure.

---

# Design Principles

The HTTP Archive Capability SHALL be

- Scope-confined and policy-gated
- Faithful to captured transactions
- Bounded in volume
- Redaction-aware
- Implementation independent

---

# Architecture

```
Consuming Skill Or Workflow

↓

HTTP Archive Capability

├── Policy Gate            → Policy Engine
├── Transaction Collector  → HTTP Client / Proxy
├── Redactor
├── Archive Writer         → Artifact (HTTP Transaction)
├── Evidence Promoter      → Evidence (shared lifecycle)
└── Metrics Emitter        → Metrics

↓

Artifacts · Evidence · Metrics
```

The HTTP Archive Capability collects transactions and SHALL remain unaware of the transport
implementation.

---

# Responsibilities

The HTTP Archive Capability is responsible for

- Consulting the [Policy Engine](../../shared/policy-engine/README.md) before each request
- Collecting transactions through the [HTTP Client](../../shared/http-client/README.md) and, where
  configured, the [Proxy](../../shared/proxy/README.md)
- Recording transactions as [Artifacts](../../../schemas/artifact.md) referencing the
  [HTTP Transaction](../../../schemas/http-transaction.md) schema
- Invoking the shared [Evidence](../../shared/evidence/README.md) lifecycle to promote archives
- Emitting [Metrics](../../../schemas/metrics.md)

---

# Inputs

```yaml
target:

selection:

bounds:
  max_transactions:

redaction:

scope_id:

roe_id:
```

`target` SHALL be an in-scope endpoint. `selection` selects which transactions to archive.
`bounds` limits volume. `redaction` configures content removal.

---

# Outputs

Typical outputs MAY include

- Artifacts of type `http-archive` referencing HTTP Transactions
- Evidence references produced through the shared lifecycle
- Metrics describing archived transaction counts

Outputs SHALL contain no Findings or Risk.

---

# Policy Enforcement

The HTTP Archive Capability SHALL consult the
[Policy Engine](../../shared/policy-engine/README.md) before every request. Collection is an
`active` action permitted only on an `allow` decision and within the attached rate ceiling. A
`requires_approval` decision SHALL defer the action. Out-of-scope traffic SHALL never be archived.

---

# Dependencies

The HTTP Archive Capability depends on

- [Configuration Model](../../core/configuration-model.md)
- [Execution Model](../../core/execution-model.md)
- [Error Handling](../../core/error-handling.md)
- [HTTP Client](../../shared/http-client/README.md)
- [Proxy](../../shared/proxy/README.md)
- [Policy Engine](../../shared/policy-engine/README.md)
- [Evidence](../../shared/evidence/README.md)
- [Artifact Schema](../../../schemas/artifact.md)
- [HTTP Transaction Schema](../../../schemas/http-transaction.md)
- [Metrics Schema](../../../schemas/metrics.md)

The HTTP Archive Capability SHALL NOT depend on domain skills.

---

# Consumers

Typical consumers include

- Domain Security skills requiring HTTP evidence
- Reporting, through promoted Evidence
- Timeline, which correlates archived transactions

---

# Security Principles

The HTTP Archive Capability SHALL

- Act only within scope and Rules of Engagement, enforced by the Policy Engine
- Bound volume and preserve non-destructive behavior
- Redact sensitive request and response content
- Produce no Findings or Risk
- Preserve auditability

---

# Best Practices

Consumers SHOULD

- Provide in-scope targets and bounded selection
- Rely on the shared Evidence lifecycle for durability
- Route interpretation to Domain Security capabilities

---

# Anti-Patterns

Consumers SHOULD NOT

- Issue requests directly
- Bypass the Policy Engine
- Archive out-of-scope traffic
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
- adr/ADR-001-http-archive-capability.md

---

# Related Packages

- [HTTP Client](../../shared/http-client/README.md)
- [Proxy](../../shared/proxy/README.md)
- [Evidence](../../shared/evidence/README.md)
- [Timeline](../timeline/README.md)

---

# Canonical Schemas

- [Artifact](../../../schemas/artifact.md)
- [HTTP Transaction](../../../schemas/http-transaction.md)
- [Evidence](../../../schemas/evidence.md)
- [Metrics](../../../schemas/metrics.md)

---

# Architecture Decisions

- [ADR-001 — HTTP Archive Capability](adr/ADR-001-http-archive-capability.md)

---

# Future Extensions

Future versions MAY support

- Session-grouped archives
- Streaming-response archival
- Selective body-capture policies

Backward compatibility SHOULD be maintained.

---

# Success Criteria

A compliant HTTP Archive Capability collects faithful, policy-gated, redacted HTTP evidence,
records it in archive form referencing the canonical HTTP Transaction schema, and invokes the
shared Evidence lifecycle for durability, without interpreting transactions or producing Findings
or Risk.
