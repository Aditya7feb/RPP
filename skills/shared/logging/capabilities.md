# Logging Capabilities

**File:** `skills/shared/logging/capabilities.md`

**Version:** 1.0.0

---

# Purpose

This document enumerates the capabilities exposed by the Logging Shared Skill.
Capabilities describe *what* the shared skill provides, not *how* it is
implemented.

Each capability is implementation independent and consumed through the
[Logging Interface](interface.md).

---

# Capability Model

```
Event Composition

Correlation

Redaction

Gating

Routing

Evidence Linkage

Observability
```

---

# Event Composition Capabilities

## Structured Event Building

The Logging Shared Skill SHALL compose structured
[Log Event](../../../schemas/log-event.md) records from caller input.

---

## Field Normalization

The Logging Shared Skill SHALL normalize severity, category, and source fields to
canonical values.

---

# Correlation Capabilities

## Context Injection

The Logging Shared Skill SHALL inject correlation identifiers from the execution
context.

---

## Span Linkage

The Logging Shared Skill SHALL record span and parent-span identifiers where
present.

---

# Redaction Capabilities

## Secret Redaction

The Logging Shared Skill SHALL redact secret material from messages, attributes,
and extensions before emission.

---

## Redaction Recording

The Logging Shared Skill SHALL record redacted field keys in the event.

---

# Gating Capabilities

## Severity Gating

The Logging Shared Skill SHALL drop events below the configured severity
threshold.

---

## Category Filtering

The Logging Shared Skill SHALL support per-category enablement.

---

# Routing Capabilities

## Sink Routing

The Logging Shared Skill SHALL route qualifying events to configured sinks.

---

## Adapter Independence

The Logging Shared Skill SHALL route events without exposing sink
implementations to consumers.

---

# Evidence Linkage Capabilities

## Evidence Reference

The Logging Shared Skill SHOULD link events to evidence through `evidence_ref`.

---

# Observability Capabilities

## Counters

The Logging Shared Skill SHOULD expose emitted, dropped, and redacted event
counts.

---

# Capability Boundaries

The Logging Shared Skill SHALL NOT

- Produce security findings
- Store evidence in place of the Evidence package
- Perform target-facing operations
- Route secrets to any sink

---

# Capability Summary

| Capability | Category | Requirement |
|------------|----------|-------------|
| Structured Event Building | Composition | SHALL |
| Field Normalization | Composition | SHALL |
| Context Injection | Correlation | SHALL |
| Span Linkage | Correlation | SHALL |
| Secret Redaction | Redaction | SHALL |
| Redaction Recording | Redaction | SHALL |
| Severity Gating | Gating | SHALL |
| Category Filtering | Gating | SHALL |
| Sink Routing | Routing | SHALL |
| Adapter Independence | Routing | SHALL |
| Evidence Reference | Evidence Linkage | SHOULD |
| Counters | Observability | SHOULD |

---

# Related Documents

- [Interface](interface.md)
- [Configuration](configuration.md)
- [Execution](execution.md)
- [Error Model](error-model.md)
- [Log Event Schema](../../../schemas/log-event.md)
