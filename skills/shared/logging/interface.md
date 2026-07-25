# Logging Interface

**File:** `skills/shared/logging/interface.md`

**Version:** 1.0.0

---

# Purpose

The Logging Interface defines the canonical contract through which platform
components emit structured log events.

The interface standardizes event submission, correlation, redaction, and
routing while remaining independent of any sink implementation.

All consumers SHALL emit operational logs exclusively through this interface.

---

# Design Principles

The interface SHALL be

- Stable
- Strongly Defined
- Sink Independent
- Versioned
- Observable
- Backward Compatible
- Deterministic in field composition

---

# Relationship

```
Master Agent

↓

Workflow

↓

Shared Package or Domain Skill

↓

Logging Interface

↓

Logging Shared Skill

↓

Configured Sinks
```

The interface SHALL NOT expose or depend on sink internals.

---

# Interface Overview

```
Log Request

↓

Execution Context

↓

Composition

↓

Emission Result

↓

Errors
```

---

# Log Request

Every invocation SHALL define

```yaml
severity:

message:

category:

source:

attributes:

evidence_ref:
```

`severity`, `category`, and `source` SHALL conform to the
[Log Event schema](../../../schemas/log-event.md).

`attributes` SHALL be structured and SHALL NOT contain secrets.

`evidence_ref` MAY link the event to evidence.

---

# Execution Context

The Logging Shared Skill SHALL receive read-only context.

```yaml
assessment_id:

task_id:

request_id:

execution_id:

span_id:

parent_span_id:
```

Correlation identifiers SHALL be injected from context into the composed event.

The interface SHALL treat context as read-only.

---

# Composition

The interface SHALL compose a canonical
[Log Event](../../../schemas/log-event.md) from the request and context.

Composition SHALL

- Normalize severity and category
- Inject correlation
- Apply redaction
- Record redacted fields

---

# Emission Result

Every invocation SHALL return a normalized result.

```yaml
outcome:

event_id:
```

`outcome` SHALL be one of

```
emitted

dropped

error
```

`dropped` SHALL indicate the event was below the severity threshold or a
disabled category.

`event_id` SHALL be present when `outcome` is `emitted`.

---

# Error Contract

Errors SHALL conform to
[the platform error handling model](../../core/error-handling.md) and to
[the Logging error model](error-model.md).

A sink failure SHALL NOT propagate as a caller error unless configured to fail
closed.

---

# Determinism

Given identical request and context, the composed event fields SHALL be
identical apart from `event_id` and `timestamp`.

---

# Compatibility

The interface SHALL remain stable across event categories and sinks.

Consumers SHALL require no modification when sinks change.

---

# Versioning

The interface SHALL follow semantic versioning.

Minor versions MAY introduce optional fields.

Major versions SHALL indicate breaking changes.

---

# Validation Rules

A compliant invocation SHALL define

- Severity
- Message
- Category
- Source
- Non-secret attributes
- Execution Context for correlation

---

# Quality Requirements

The Logging Interface SHALL

✓ Remain sink independent

✓ Produce canonical log events

✓ Inject correlation automatically

✓ Enforce redaction

✓ Support structured errors

✓ Remain backward compatible

---

# Future Extensions

Future versions MAY include

- Batch event submission
- Sampling directives
- Structured per-category payloads

Backward compatibility SHOULD be maintained.

---

# Success Criteria

A compliant Logging Interface provides a stable, implementation-independent
contract through which all platform components emit structured, correlated, and
redacted log events across the Robust PenTest Platform.
