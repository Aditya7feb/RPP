# Log Collection Configuration

**File:** `skills/evidence/log-collection/configuration.md`

**Version:** 1.0.0

---

# Purpose

This document defines the declarative configuration of the Log Collection Capability and the
precedence rules that govern it.

---

# Configuration Object

```yaml
log_collection:
  bounds:
    max_events:
    window:
  redaction:
    redact_sensitive: true
  ordering:
    preserve: true
  evidence:
    promote: true
    integrity_hash: true
```

---

# Field Definitions

## bounds

`max_events` and `window` bound collection. The capability SHALL NOT exceed these bounds.

## redaction

`redact_sensitive` SHALL default to `true`.

## ordering

`preserve` SHALL default to `true`, preserving log event ordering.

## evidence

`promote` SHALL default to `true`, invoking the shared Evidence lifecycle. `integrity_hash` SHALL
default to `true`.

---

# Precedence

Configuration precedence, from highest to lowest, SHALL be

1. Rules of Engagement and Scope constraints
2. Per-request parameters
3. Capability configuration in this document
4. Documented defaults

---

# Validation Rules

- `max_events` SHALL be a positive integer when present.
- Unknown fields SHALL be ignored for forward compatibility.

---

# Related Documents

- [interface.md](interface.md)
- [execution.md](execution.md)
- [error-model.md](error-model.md)
