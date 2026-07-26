# Screenshot Capture Configuration

**File:** `skills/evidence/screenshot-capture/configuration.md`

**Version:** 1.0.0

---

# Purpose

This document defines the declarative configuration of the Screenshot Capture Capability and the
precedence rules that govern it.

---

# Configuration Object

```yaml
screenshot_capture:
  capture:
    full_page: true
    viewport:
  bounds:
    max_captures:
  redaction:
    redact_sensitive: true
  evidence:
    promote: true
```

---

# Field Definitions

## capture

`full_page` and `viewport` select capture parameters.

## bounds

`max_captures` bounds capture volume. The capability SHALL NOT exceed this bound.

## redaction

`redact_sensitive` SHALL default to `true`.

## evidence

`promote` SHALL default to `true`, invoking the shared Evidence lifecycle to promote captures.

---

# Precedence

Configuration precedence, from highest to lowest, SHALL be

1. Rules of Engagement and Scope constraints
2. Policy Engine decisions
3. Per-request options
4. Capability configuration in this document
5. Documented defaults

---

# Validation Rules

- `max_captures` SHALL be a positive integer when present.
- Unknown fields SHALL be ignored for forward compatibility.

---

# Related Documents

- [interface.md](interface.md)
- [execution.md](execution.md)
- [error-model.md](error-model.md)
