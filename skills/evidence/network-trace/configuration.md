# Network Trace Configuration

**File:** `skills/evidence/network-trace/configuration.md`

**Version:** 1.0.0

---

# Purpose

This document defines the declarative configuration of the Network Trace Capability and the
precedence rules that govern it.

---

# Configuration Object

```yaml
network_trace:
  selection:
    protocols:
    ports:
  bounds:
    max_flows:
    max_duration:
  redaction:
    redact_payloads: true
  evidence:
    promote: true
    integrity_hash: true
```

---

# Field Definitions

## selection

`protocols` and `ports` scope capture.

## bounds

`max_flows` and `max_duration` bound capture. The capability SHALL NOT exceed these bounds.

## redaction

`redact_payloads` SHALL default to `true`.

## evidence

`promote` SHALL default to `true`, invoking the shared Evidence lifecycle. `integrity_hash` SHALL
default to `true`.

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

- `max_flows` and `max_duration` SHALL be positive values when present.
- Unknown fields SHALL be ignored for forward compatibility.

---

# Related Documents

- [interface.md](interface.md)
- [execution.md](execution.md)
- [error-model.md](error-model.md)
