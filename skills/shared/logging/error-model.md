# Logging Error Model

**File:** `skills/shared/logging/error-model.md`

**Version:** 1.0.0

---

# Purpose

This document defines the error model for the Logging Shared Skill.

The error model classifies the failure conditions the shared skill MAY produce
and aligns them with
[the platform error handling model](../../core/error-handling.md).

All errors SHALL be normalized and implementation independent.

---

# Error Philosophy

The Logging Shared Skill SHALL

- Produce canonical, structured errors
- Prefer availability of the caller operation over log delivery, unless
  configured to fail closed
- Always fail closed on redaction failure to protect secrets
- Never leak secret material through errors

---

# Error Categories

The Logging Shared Skill maps its failures onto the canonical categories.

```
Configuration

Validation

Redaction

Sink

Adapter

Internal
```

---

# Configuration Errors

Raised when configuration is invalid.

Conditions

- Invalid severity `level`
- `security_event` or `audit` placed in disabled categories
- Redaction disabled
- A sink lacks a `kind`

Configuration errors SHALL be non-retryable.

---

# Validation Errors

Raised when a log request is malformed.

Conditions

- Missing severity, message, category, or source
- Secret material present in structured attributes that cannot be redacted by
  key or pattern

Validation errors SHALL be non-retryable.

---

# Redaction Errors

Raised when redaction cannot be completed for an event.

Redaction errors SHALL cause the affected event to fail closed, meaning the
event SHALL NOT be routed to any sink.

Redaction errors SHALL be recorded through internal counters without exposing
the unredacted content.

---

# Sink Errors

Raised when a sink cannot accept an event.

Under `fail_open`, sink errors SHALL NOT propagate to the caller; the event
SHALL be counted as dropped.

Under `fail_closed`, a required sink error SHALL propagate a canonical logging
error.

Sink errors MAY be retryable subject to configuration.

---

# Adapter Errors

Raised when an underlying sink adapter fails unexpectedly.

Adapter errors SHALL be normalized and handled according to the configured
failure mode.

---

# Internal Errors

Raised for unexpected conditions within the Logging Shared Skill.

Internal errors SHALL be treated as non-retryable and SHOULD be reported for
diagnosis.

---

# Error Structure

Every error SHALL conform to the canonical error structure.

```yaml
category:

code:

message:

retryable:

sink:
```

`category` SHALL be one of the canonical categories.

`retryable` SHALL indicate whether emission MAY be attempted again.

Errors SHALL NOT contain secret material or unredacted event content.

---

# Outcome Mapping

| Outcome | Category | Retryable |
|---------|----------|-----------|
| invalid_level | Configuration | No |
| redaction_disabled | Configuration | No |
| malformed_request | Validation | No |
| redaction_failed | Redaction | No (fails closed) |
| sink_unavailable | Sink | Config dependent |
| adapter_failure | Adapter | Config dependent |
| unexpected | Internal | No |

---

# Failure Mode Summary

| Failure | fail_open | fail_closed |
|---------|-----------|-------------|
| Redaction failure | Event dropped | Event dropped |
| Required sink failure | Event dropped | Caller error |
| Optional sink failure | Event dropped | Event dropped |

Redaction failure SHALL always drop the event regardless of failure mode.

---

# Related Documents

- [Interface](interface.md)
- [Execution](execution.md)
- [Error Handling Model](../../core/error-handling.md)
- [Log Event Schema](../../../schemas/log-event.md)
