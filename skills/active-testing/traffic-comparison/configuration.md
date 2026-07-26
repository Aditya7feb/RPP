# Traffic Comparison Configuration

**File:** `skills/active-testing/traffic-comparison/configuration.md`

**Version:** 1.0.0

---

# Purpose

This document defines the declarative configuration of the Traffic Comparison Capability and the
precedence rules that govern it.

---

# Configuration Object

```yaml
traffic_comparison:
  dimensions:
    enabled:
  bounds:
    max_transactions:
  tolerance:
    ignore_headers:
    timing_threshold:
  redaction:
    redact_sensitive: true
  storage:
    diff_format: structured-record
```

---

# Field Definitions

## dimensions

`enabled` enumerates the compared dimensions, such as `status`, `headers`, `timing`, and `body`.

## bounds

`max_transactions` bounds comparison scope. The capability SHALL NOT exceed this bound.

## tolerance

`ignore_headers` excludes volatile headers from comparison. `timing_threshold` sets the timing
difference considered significant.

## redaction

`redact_sensitive` SHALL default to `true`.

## storage

`diff_format` names the difference artifact format.

---

# Precedence

Configuration precedence, from highest to lowest, SHALL be

1. Per-request `comparison` and `bounds`
2. Capability configuration in this document
3. Documented defaults

---

# Validation Rules

- `max_transactions` SHALL be a positive integer when present.
- Unknown fields SHALL be ignored for forward compatibility.

---

# Related Documents

- [interface.md](interface.md)
- [execution.md](execution.md)
- [error-model.md](error-model.md)
