# Mutation Engine Capability

**File:** `skills/active-testing/mutation-engine/README.md`

**Version:** 1.0.0

---

# Purpose

The Mutation Engine Capability is an Active-Testing-tier capability that transforms base
inputs into bounded sets of variants within the Robust PenTest Platform (RPP).

It applies deterministic mutation strategies — encoding, case and boundary changes,
structural edits, and marker insertion — to a base [Payload](../../../schemas/payload.md) or
value, producing derived Payloads with full lineage. It performs no target-facing action and
produces no Findings.

The Mutation Engine emits derived [Payloads](../../../schemas/payload.md) and
[Metrics](../../../schemas/metrics.md).

---

# Goals

The Mutation Engine Capability SHALL

- Apply named, deterministic mutation strategies to a base input
- Produce bounded sets of derived [Payloads](../../../schemas/payload.md) with lineage
- Preserve non-destructive safety markers on derived Payloads
- Emit [Metrics](../../../schemas/metrics.md) describing mutation counts
- Remain implementation independent
- Produce no Findings or Risk

---

# Non-Goals

The Mutation Engine Capability SHALL NOT

- Contact targets or perform any network action
- Deliver payloads (that is Fuzzing or a domain capability)
- Interpret results or produce Findings or Risk
- Emit destructive mutations without preserving the approval requirement
- Invoke command-line tools or parse their output

Delivery belongs to active-testing and domain capabilities; interpretation belongs to domain
capabilities.

---

# Design Principles

The Mutation Engine Capability SHALL be

- Deterministic given the same base input, strategy, and seed
- Bounded in the number of variants produced
- Lineage-preserving
- Safety-preserving
- Implementation independent

---

# Architecture

```
Consuming Capability

↓

Mutation Engine Capability

├── Strategy Registry
├── Mutation Applicator
├── Lineage Recorder
├── Safety Preserver
├── Payload Emitter        → Payload (derived)
└── Metrics Emitter        → Metrics

↓

Derived Payloads · Metrics
```

The Mutation Engine transforms data and SHALL remain unaware of how consumers deliver it.

---

# Responsibilities

The Mutation Engine Capability is responsible for

- Registering named mutation strategies
- Applying strategies to a base input within bounds
- Recording `lineage` on each derived [Payload](../../../schemas/payload.md)
- Preserving `safety` markers, including `requires_approval` for destructive mutations
- Emitting [Metrics](../../../schemas/metrics.md)

---

# Inputs

```yaml
base_payload_ref:

strategies:

bounds:
  max_variants:

seed:
```

`base_payload_ref` references the base [Payload](../../../schemas/payload.md). `strategies`
names the mutation strategies. `bounds` limits output. `seed` enables deterministic
reproduction.

---

# Outputs

Typical outputs MAY include

- Derived Payloads with `lineage.source` `mutated`
- Metrics describing mutation counts

Outputs SHALL contain no Findings or Risk.

---

# Dependencies

The Mutation Engine Capability depends on

- [Configuration Model](../../core/configuration-model.md)
- [Execution Model](../../core/execution-model.md)
- [Error Handling](../../core/error-handling.md)
- [Payload Schema](../../../schemas/payload.md)
- [Metrics Schema](../../../schemas/metrics.md)

The Mutation Engine Capability SHALL NOT depend on domain skills.

---

# Consumers

Typical consumers include

- Payload Generation and Fuzzing capabilities
- Domain skills requiring input variants

---

# Security Principles

The Mutation Engine Capability SHALL

- Perform no target-facing action
- Bound variant counts
- Preserve non-destructive and approval markers on derived Payloads
- Produce no Findings or Risk
- Preserve auditability

---

# Best Practices

Consumers SHOULD

- Provide a seed for reproducibility
- Bound variant counts
- Capture emitted Metrics and lineage

---

# Anti-Patterns

Consumers SHOULD NOT

- Request unbounded variant sets
- Strip safety markers from derived Payloads
- Expect target interaction from this capability

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
- adr/ADR-001-mutation-engine-capability.md

---

# Related Packages

- [Payload Generation](../payload-generation/README.md)
- [Fuzzing](../fuzzing/README.md)
- [Wordlists](../wordlists/README.md)

---

# Canonical Schemas

- [Payload](../../../schemas/payload.md)
- [Metrics](../../../schemas/metrics.md)

---

# Architecture Decisions

- [ADR-001 — Mutation Engine Capability](adr/ADR-001-mutation-engine-capability.md)

---

# Future Extensions

Future versions MAY support

- Grammar-aware structural mutation
- Coverage-guided mutation feedback
- Strategy weighting

Backward compatibility SHOULD be maintained.

---

# Success Criteria

A compliant Mutation Engine Capability produces bounded, deterministic, lineage-preserving
input variants without contacting targets or producing Findings or Risk.
