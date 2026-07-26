# Payload Generation Capability

**File:** `skills/active-testing/payload-generation/README.md`

**Version:** 1.0.0

---

# Purpose

The Payload Generation Capability is an Active-Testing-tier capability that composes concrete
test inputs for use by active-testing and domain capabilities within the Robust PenTest
Platform (RPP).

It assembles [Payloads](../../../schemas/payload.md) from templates, wordlist seeds, and
mutation variants, applying encoding and safety marking, so that consumers obtain ready,
governed inputs rather than constructing their own. It performs no target-facing action and
produces no Findings.

The Payload Generation Capability consumes [Wordlists](../wordlists/README.md) and the
[Mutation Engine](../mutation-engine/README.md), and emits
[Payloads](../../../schemas/payload.md) and [Metrics](../../../schemas/metrics.md).

---

# Goals

The Payload Generation Capability SHALL

- Compose Payloads from templates, wordlist seeds, and mutation variants
- Apply encoding and non-destructive safety marking
- Reference markers and out-of-band values rather than inlining them
- Emit generated [Payloads](../../../schemas/payload.md) with lineage
- Emit [Metrics](../../../schemas/metrics.md) describing generation
- Remain implementation independent
- Produce no Findings or Risk

---

# Non-Goals

The Payload Generation Capability SHALL NOT

- Contact targets or deliver payloads (that is Fuzzing or a domain capability)
- Interpret results or produce Findings or Risk
- Inline markers, out-of-band values, or credentials
- Emit destructive payloads without an approval requirement
- Invoke command-line tools or parse their output

Delivery belongs to active-testing and domain capabilities; interpretation belongs to domain
capabilities.

---

# Design Principles

The Payload Generation Capability SHALL be

- Deterministic given the same template, seeds, and mutation seed
- Bounded in the number of Payloads produced
- Lineage- and safety-preserving
- Reference-based for sensitive content
- Implementation independent

---

# Architecture

```
Consuming Capability

↓

Payload Generation Capability

├── Template Registry
├── Seed Composer          → Wordlists
├── Variant Composer       → Mutation Engine
├── Encoder
├── Safety Marker
├── Payload Emitter        → Payload
└── Metrics Emitter        → Metrics

↓

Payloads · Metrics
```

The Payload Generation Capability composes data and SHALL remain unaware of delivery.

---

# Responsibilities

The Payload Generation Capability is responsible for

- Resolving templates and composing Payloads
- Drawing seeds from [Wordlists](../wordlists/README.md)
- Deriving variants through the [Mutation Engine](../mutation-engine/README.md)
- Applying encoding and safety marking
- Emitting [Payloads](../../../schemas/payload.md) and
  [Metrics](../../../schemas/metrics.md)

---

# Inputs

```yaml
template_ref:

seeds:
  wordlist_name:
  max_entries:

mutation:
  strategies:
  max_variants:
  seed:

encoding:

bounds:
  max_payloads:
```

`template_ref` references a payload template. `seeds` draws candidate values from a wordlist.
`mutation` derives variants. `encoding` selects an applied encoding. `bounds` limits output.

---

# Outputs

Typical outputs MAY include

- Generated Payloads with lineage and safety markers
- Metrics describing generation counts

Outputs SHALL contain no Findings or Risk.

---

# Dependencies

The Payload Generation Capability depends on

- [Configuration Model](../../core/configuration-model.md)
- [Execution Model](../../core/execution-model.md)
- [Error Handling](../../core/error-handling.md)
- [Wordlists](../wordlists/README.md)
- [Mutation Engine](../mutation-engine/README.md)
- [Payload Schema](../../../schemas/payload.md)
- [Metrics Schema](../../../schemas/metrics.md)

The Payload Generation Capability SHALL NOT depend on domain skills.

---

# Consumers

Typical consumers include

- Fuzzing and Replay capabilities
- Web Security and API Security skills requiring governed inputs

---

# Security Principles

The Payload Generation Capability SHALL

- Perform no target-facing action
- Bound the number of Payloads produced
- Reference markers, out-of-band values, and credentials rather than inlining them
- Mark destructive payloads with `requires_approval`
- Produce no Findings or Risk
- Preserve auditability

---

# Best Practices

Consumers SHOULD

- Provide seeds for reproducibility
- Bound generation counts
- Capture emitted Payloads, lineage, and Metrics

---

# Anti-Patterns

Consumers SHOULD NOT

- Request unbounded generation
- Inline sensitive values
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
- adr/ADR-001-payload-generation-capability.md

---

# Related Packages

- [Wordlists](../wordlists/README.md)
- [Mutation Engine](../mutation-engine/README.md)
- [Fuzzing](../fuzzing/README.md)

---

# Canonical Schemas

- [Payload](../../../schemas/payload.md)
- [Metrics](../../../schemas/metrics.md)

---

# Architecture Decisions

- [ADR-001 — Payload Generation Capability](adr/ADR-001-payload-generation-capability.md)

---

# Future Extensions

Future versions MAY support

- Context-aware template selection
- Grammar-driven composition
- Coverage-guided generation

Backward compatibility SHOULD be maintained.

---

# Success Criteria

A compliant Payload Generation Capability composes bounded, deterministic, governed Payloads
with lineage and safety markers, without contacting targets or producing Findings or Risk.
