# Logging Execution Model

**File:** `skills/shared/logging/execution.md`

**Version:** 1.0.0

---

# Purpose

This document defines the execution model for the Logging Shared Skill.

The execution model describes how the shared skill processes a log request from
composition through redaction, gating, routing, and emission.

The model is deterministic in field composition given the same request and
context.

---

# Execution Overview

```
Receive Log Request

↓

Resolve Configuration

↓

Compose Event

↓

Inject Correlation

↓

Apply Redaction

↓

Evaluate Gates

↓

Route To Sinks

↓

Return Emission Result
```

---

# Stage 1 — Configuration Resolution

The Logging Shared Skill SHALL resolve level, categories, redaction, sinks, and
failure mode using the precedence defined in [configuration.md](configuration.md).

Mandatory redaction SHALL always be enforced.

---

# Stage 2 — Event Composition

The Logging Shared Skill SHALL compose a canonical
[Log Event](../../../schemas/log-event.md) from the request, normalizing
severity, category, and source.

---

# Stage 3 — Correlation Injection

The Logging Shared Skill SHALL inject assessment, task, request, execution, and
span identifiers from the execution context.

Where an identifier is absent, the corresponding field SHALL be omitted rather
than fabricated.

---

# Stage 4 — Redaction

The Logging Shared Skill SHALL redact secret material from the message,
attributes, and extensions before any further processing.

Redacted field keys SHALL be recorded in `redaction.fields`, and
`redaction.applied` SHALL be set accordingly.

Redaction SHALL precede gating and routing.

---

# Stage 5 — Gating

The Logging Shared Skill SHALL drop events

- Below the configured `level`
- In a disabled category

`security_event` and `audit` categories SHALL NOT be droppable by category
configuration.

Dropped events SHALL return an `outcome` of `dropped`.

---

# Stage 6 — Routing

The Logging Shared Skill SHALL route qualifying events to each sink whose
`min_level` and `categories` match.

Sink implementations SHALL remain hidden behind adapters.

---

# Stage 7 — Emission Result

The Logging Shared Skill SHALL return a normalized emission result including the
`outcome` and, when emitted, the `event_id`.

---

# Determinism

Given identical request and context, composed event fields SHALL be identical
apart from `event_id` and `timestamp`.

---

# Concurrency

The Logging Shared Skill SHALL support concurrent emission from multiple callers.

Event ordering within a single span SHOULD be preserved where the sink supports
ordering.

---

# Failure Handling

Execution failures SHALL be classified according to
[error-model.md](error-model.md).

Under `fail_open`, a sink failure SHALL NOT propagate to the caller; the event
SHALL be counted as dropped and an internal counter SHALL record the failure.

Under `fail_closed`, a required sink failure SHALL propagate a canonical logging
error.

Redaction failure SHALL always fail closed for the affected event to prevent
secret leakage.

---

# Interaction With Evidence

Where an event corresponds to captured evidence, the execution model SHALL set
`evidence_ref` so that logs and evidence remain correlated through the
[Evidence](../evidence/README.md) shared package.

---

# Execution Outputs

The execution model SHALL produce

- A canonical log event routed to sinks
- An emission result
- Internal counters

Outputs SHALL remain implementation independent.

---

# Related Documents

- [Interface](interface.md)
- [Configuration](configuration.md)
- [Error Model](error-model.md)
- [Log Event Schema](../../../schemas/log-event.md)
- [Execution Model](../../core/execution-model.md)
