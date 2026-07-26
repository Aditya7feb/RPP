# Wordlists Capability

**File:** `skills/active-testing/wordlists/README.md`

**Version:** 1.0.0

---

# Purpose

The Wordlists Capability is an Active-Testing-tier capability that provides curated,
implementation-independent input lists for use by other capabilities and domain skills
within the Robust PenTest Platform (RPP).

It supplies reusable collections of candidate values — words, paths, parameter names,
subdomains, and payload seeds — as canonical data, so that discovery, active-testing, and
domain capabilities draw candidate inputs from a single governed source rather than
embedding their own.

The Wordlists Capability emits [Artifacts](../../../schemas/artifact.md) referencing list
content and [Payload](../../../schemas/payload.md) seeds. It produces no Findings and
performs no target-facing action.

---

# Goals

The Wordlists Capability SHALL

- Provide named, versioned input lists as canonical data
- Support selection, filtering, and bounded sampling of list entries
- Emit list content by reference as [Artifacts](../../../schemas/artifact.md)
- Emit candidate values as [Payload](../../../schemas/payload.md) seeds where requested
- Remain implementation independent
- Produce no Findings or Risk

---

# Non-Goals

The Wordlists Capability SHALL NOT

- Contact targets or perform any network action
- Generate mutated or encoded payloads (that is Payload Generation)
- Interpret results or produce Findings or Risk
- Persist secrets within list content
- Invoke command-line tools or parse their output

Target-facing delivery belongs to active-testing and domain capabilities; payload shaping
belongs to Payload Generation.

---

# Design Principles

The Wordlists Capability SHALL be

- Deterministic given the same list and selection
- Bounded in sample size
- Referenced rather than inlined for large lists
- Governed and versioned
- Implementation independent

---

# Architecture

```
Consuming Capability

↓

Wordlists Capability

├── List Registry
├── Selector And Filter
├── Bounded Sampler
├── Artifact Emitter        → Artifact
└── Seed Emitter            → Payload (seed)

↓

Artifacts · Payload Seeds · Metrics
```

The Wordlists Capability serves data and SHALL remain unaware of how consumers deliver it.

---

# Responsibilities

The Wordlists Capability is responsible for

- Registering and versioning named lists
- Selecting, filtering, and bounded-sampling entries
- Emitting list content as [Artifacts](../../../schemas/artifact.md)
- Emitting candidate values as [Payload](../../../schemas/payload.md) seeds
- Emitting [Metrics](../../../schemas/metrics.md) describing selection

---

# Inputs

```yaml
list_name:

selection:
  filter:
  max_entries:

emit:
  as_artifact:
  as_seeds:
```

`list_name` SHALL name a registered list. `selection` bounds the returned entries. `emit`
selects output form.

---

# Outputs

Typical outputs MAY include

- Artifacts referencing selected list content
- Payload seeds
- Metrics describing selection counts

Outputs SHALL remain implementation independent and SHALL contain no Findings or Risk.

---

# Dependencies

The Wordlists Capability depends on

- [Configuration Model](../../core/configuration-model.md)
- [Execution Model](../../core/execution-model.md)
- [Error Handling](../../core/error-handling.md)
- [Payload Schema](../../../schemas/payload.md)
- [Artifact Schema](../../../schemas/artifact.md)
- [Metrics Schema](../../../schemas/metrics.md)

The Wordlists Capability SHALL NOT depend on domain skills.

---

# Consumers

Typical consumers include

- Payload Generation, Fuzzing, and Parameter Mining capabilities
- Discovery skills requiring candidate values

---

# Security Principles

The Wordlists Capability SHALL

- Perform no target-facing action
- Bound sample sizes
- Persist no secrets in list content
- Produce no Findings or Risk
- Preserve auditability

---

# Best Practices

Consumers SHOULD

- Reference named lists rather than embedding their own
- Bound sample sizes
- Capture emitted Artifacts and Metrics

---

# Anti-Patterns

Consumers SHOULD NOT

- Embed private copies of lists
- Request unbounded samples
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
- adr/ADR-001-wordlists-capability.md

---

# Related Packages

- [Payload Generation](../payload-generation/README.md)
- [Fuzzing](../fuzzing/README.md)
- [Parameter Mining](../parameter-mining/README.md)

---

# Canonical Schemas

- [Payload](../../../schemas/payload.md)
- [Artifact](../../../schemas/artifact.md)
- [Metrics](../../../schemas/metrics.md)

---

# Architecture Decisions

- [ADR-001 — Wordlists Capability](adr/ADR-001-wordlists-capability.md)

---

# Future Extensions

Future versions MAY support

- List provenance and licensing metadata
- Weighted and context-ranked selection
- Domain-tuned list variants

Backward compatibility SHOULD be maintained.

---

# Success Criteria

A compliant Wordlists Capability provides governed, versioned, bounded input lists as
canonical data for the platform, without contacting targets, shaping payloads, or producing
Findings or Risk.
