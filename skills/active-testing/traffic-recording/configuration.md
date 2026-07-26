# Traffic Recording Configuration

**File:** `skills/active-testing/traffic-recording/configuration.md`

**Version:** 1.0.0

---

# Purpose

This document defines the declarative configuration of the Traffic Recording Capability and the
precedence rules that govern it.

---

# Configuration Object

```yaml
traffic_recording:
  bounds:
    max_transactions:
    max_duration:
  redaction:
    redact_credentials: true
    redact_tokens: true
    redact_pii: true
  storage:
    format: har
  evidence:
    integrity_hash: true
```

---

# Field Definitions

## bounds

`max_transactions` and `max_duration` bound capture. The capability SHALL NOT exceed these
bounds.

## redaction

`redact_credentials`, `redact_tokens`, and `redact_pii` SHALL default to `true`.

## storage

`format` names the stored artifact format, such as `har`.

## evidence

`integrity_hash` SHALL default to `true`, recording an artifact content hash.

---

# Precedence

Configuration precedence, from highest to lowest, SHALL be

1. Rules of Engagement and Scope constraints
2. Policy Engine decisions
3. Per-request parameters
4. Capability configuration in this document
5. Documented defaults

---

# Validation Rules

- `max_transactions` and `max_duration` SHALL be positive values when present.
- Redaction of credentials and tokens SHOULD remain enabled.
- Unknown fields SHALL be ignored for forward compatibility.

---

# Related Documents

- [interface.md](interface.md)
- [execution.md](execution.md)
- [error-model.md](error-model.md)
