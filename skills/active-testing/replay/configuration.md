# Replay Configuration

**File:** `skills/active-testing/replay/configuration.md`

**Version:** 1.0.0

---

# Purpose

This document defines the declarative configuration of the Replay Capability and the precedence
rules that govern it.

---

# Configuration Object

```yaml
replay:
  bounds:
    max_requests:
    rate_ceiling:
  adjustment:
    allow_field_adjustment: true
    destructive_adjustments_require_approval: true
  delivery:
    non_destructive_only: true
  evidence:
    capture_interactions: true
    redact_sensitive: true
```

---

# Field Definitions

## bounds

`max_requests` and `rate_ceiling` bound replay. The capability SHALL NOT exceed these bounds.

## adjustment

`allow_field_adjustment` enables bounded field changes.
`destructive_adjustments_require_approval` SHALL default to `true`.

## delivery

`non_destructive_only` SHALL default to `true`.

## evidence

`capture_interactions` and `redact_sensitive` SHALL default to `true`.

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

- `max_requests` and `rate_ceiling` SHALL be positive values when present.
- `non_destructive_only` SHOULD remain `true` unless approval is granted.
- Unknown fields SHALL be ignored for forward compatibility.

---

# Related Documents

- [interface.md](interface.md)
- [execution.md](execution.md)
- [error-model.md](error-model.md)
