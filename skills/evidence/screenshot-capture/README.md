# Screenshot Capture Capability

**File:** `skills/evidence/screenshot-capture/README.md`

**Version:** 1.0.0

---

# Purpose

The Screenshot Capture Capability is an Evidence-tier capability that captures browser
screenshots and rendered page captures of in-scope targets within the Robust PenTest Platform
(RPP).

It renders in-scope pages through the shared [Browser](../../shared/browser/README.md) and
records the rendered result as durable visual evidence. It performs no interpretation and produces
no Findings.

The Screenshot Capture Capability gates every target-facing action through the
[Policy Engine](../../shared/policy-engine/README.md), emits
[Artifacts](../../../schemas/artifact.md), and invokes the shared
[Evidence](../../shared/evidence/README.md) lifecycle to promote captures into durable Evidence.

---

# Goals

The Screenshot Capture Capability SHALL

- Capture browser screenshots and rendered page captures of in-scope targets
- Consult the [Policy Engine](../../shared/policy-engine/README.md) before every capture
- Record captures as [Artifacts](../../../schemas/artifact.md) of type `screenshot`
- Invoke the shared [Evidence](../../shared/evidence/README.md) lifecycle to promote captures
- Redact sensitive on-screen content where configured
- Emit [Metrics](../../../schemas/metrics.md) describing capture counts
- Remain implementation independent
- Produce no Findings or Risk

---

# Non-Goals

The Screenshot Capture Capability SHALL NOT

- Render pages directly rather than through the shared Browser
- Interpret captured content or produce Findings or Risk
- Own durable persistence, integrity, or retention (that is the shared Evidence lifecycle)
- Capture out-of-scope pages
- Invoke command-line tools or parse their output

Rendering belongs to the shared Browser; interpretation belongs to Domain Security capabilities;
the durable evidence lifecycle belongs to the shared Evidence infrastructure.

---

# Design Principles

The Screenshot Capture Capability SHALL be

- Scope-confined and policy-gated
- Faithful to the rendered result
- Bounded in capture volume
- Redaction-aware
- Implementation independent

---

# Architecture

```
Consuming Skill Or Workflow

↓

Screenshot Capture Capability

├── Policy Gate            → Policy Engine
├── Page Renderer          → Browser
├── Redactor
├── Artifact Emitter       → Artifact
├── Evidence Promoter      → Evidence (shared lifecycle)
└── Metrics Emitter        → Metrics

↓

Artifacts · Evidence · Metrics
```

The Screenshot Capture Capability captures rendered results and SHALL remain unaware of the
browser implementation.

---

# Responsibilities

The Screenshot Capture Capability is responsible for

- Consulting the [Policy Engine](../../shared/policy-engine/README.md) before each capture
- Rendering in-scope pages through the [Browser](../../shared/browser/README.md)
- Recording captures as [Artifacts](../../../schemas/artifact.md)
- Invoking the shared [Evidence](../../shared/evidence/README.md) lifecycle to promote captures
- Emitting [Metrics](../../../schemas/metrics.md)

---

# Inputs

```yaml
target:

capture:
  full_page:
  viewport:

redaction:

scope_id:

roe_id:
```

`target` SHALL be an in-scope page. `capture` selects capture options. `redaction` configures
on-screen content removal.

---

# Outputs

Typical outputs MAY include

- Artifacts of type `screenshot`
- Evidence references produced through the shared lifecycle
- Metrics describing capture counts

Outputs SHALL contain no Findings or Risk.

---

# Policy Enforcement

The Screenshot Capture Capability SHALL consult the
[Policy Engine](../../shared/policy-engine/README.md) before every capture. Capture is an
`active` action permitted only on an `allow` decision. A `requires_approval` decision SHALL defer
the capture. Out-of-scope pages SHALL never be captured.

---

# Dependencies

The Screenshot Capture Capability depends on

- [Configuration Model](../../core/configuration-model.md)
- [Execution Model](../../core/execution-model.md)
- [Error Handling](../../core/error-handling.md)
- [Browser](../../shared/browser/README.md)
- [Policy Engine](../../shared/policy-engine/README.md)
- [Evidence](../../shared/evidence/README.md)
- [Artifact Schema](../../../schemas/artifact.md)
- [Metrics Schema](../../../schemas/metrics.md)

The Screenshot Capture Capability SHALL NOT depend on domain skills.

---

# Consumers

Typical consumers include

- Domain Security skills requiring visual evidence
- Reporting, through promoted Evidence

---

# Security Principles

The Screenshot Capture Capability SHALL

- Act only within scope and Rules of Engagement, enforced by the Policy Engine
- Bound capture volume and preserve non-destructive behavior
- Redact sensitive on-screen content where configured
- Produce no Findings or Risk
- Preserve auditability

---

# Best Practices

Consumers SHOULD

- Provide in-scope pages and bounded capture options
- Rely on the shared Evidence lifecycle for durability
- Route interpretation to Domain Security capabilities

---

# Anti-Patterns

Consumers SHOULD NOT

- Render pages directly
- Bypass the Policy Engine
- Expect interpretation or findings from this capability
- Capture out-of-scope pages

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
- adr/ADR-001-screenshot-capture-capability.md

---

# Related Packages

- [Browser](../../shared/browser/README.md)
- [Evidence](../../shared/evidence/README.md)
- [Policy Engine](../../shared/policy-engine/README.md)

---

# Canonical Schemas

- [Artifact](../../../schemas/artifact.md)
- [Evidence](../../../schemas/evidence.md)
- [Metrics](../../../schemas/metrics.md)

---

# Architecture Decisions

- [ADR-001 — Screenshot Capture Capability](adr/ADR-001-screenshot-capture-capability.md)

---

# Future Extensions

Future versions MAY support

- Element-scoped captures
- Visual-diff-friendly capture normalization
- Multi-viewport capture sets

Backward compatibility SHOULD be maintained.

---

# Success Criteria

A compliant Screenshot Capture Capability captures faithful, policy-gated, bounded visual evidence
of in-scope pages and invokes the shared Evidence lifecycle for durability, without interpreting
content or producing Findings or Risk.
