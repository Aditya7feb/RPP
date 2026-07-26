# Fuzzing Configuration

**File:** `skills/active-testing/fuzzing/configuration.md`

**Version:** 1.0.0

---

# Purpose

This document defines the declarative configuration of the Fuzzing Capability and the
precedence rules that govern it.

---

# Configuration Object

```yaml
fuzzing:
  bounds:
    max_requests:
    rate_ceiling:
    max_duration:
  delivery:
    non_destructive_only: true
    stop_on_denied: true
  recording:
    capture_requests: true
    capture_responses: true
  evidence:
    redact_sensitive: true
```

---

# Field Definitions

## bounds

`max_requests`, `rate_ceiling`, and `max_duration` bound delivery. The capability SHALL NOT
exceed these bounds and SHALL never cause denial of service.

## delivery

`non_destructive_only` SHALL default to `true`; destructive payloads require approval.
`stop_on_denied` halts delivery on a `deny` decision.

## recording

`capture_requests` and `capture_responses` control artifact capture.

## evidence

`redact_sensitive` SHALL default to `true`.

---

# Precedence

Configuration precedence, from highest to lowest, SHALL be

1. Rules of Engagement and Scope constraints
2. Policy Engine decisions
3. Per-request parameters
4. Capability configuration in this document
5. Documented defaults

Policy Engine decisions SHALL always override requested parameters.

---

# Validation Rules

- `max_requests`, `rate_ceiling`, and `max_duration` SHALL be positive values when present.
- `non_destructive_only` SHOULD remain `true` unless approval is granted for destructive
  payloads.
- Unknown fields SHALL be ignored for forward compatibility.

---

# Related Documents

- [interface.md](interface.md)
- [execution.md](execution.md)
- [error-model.md](error-model.md)
