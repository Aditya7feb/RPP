# Payload Generation Configuration

**File:** `skills/active-testing/payload-generation/configuration.md`

**Version:** 1.0.0

---

# Purpose

This document defines the declarative configuration of the Payload Generation Capability and
the precedence rules that govern it.

---

# Configuration Object

```yaml
payload_generation:
  templates:
    registry:
  bounds:
    default_max_payloads:
  encoding:
    default: none
  safety:
    default_non_destructive: true
    mark_destructive_requires_approval: true
```

---

# Field Definitions

## templates

`registry` enumerates the payload templates available by default.

## bounds

`default_max_payloads` bounds output when a request omits `max_payloads`.

## encoding

`default` selects the default applied encoding.

## safety

`default_non_destructive` SHALL default to `true`. `mark_destructive_requires_approval` SHALL
default to `true`.

---

# Precedence

Configuration precedence, from highest to lowest, SHALL be

1. Per-request parameters
2. Capability configuration in this document
3. Documented defaults

---

# Validation Rules

- `default_max_payloads` SHALL be a positive integer when present.
- Unknown fields SHALL be ignored for forward compatibility.

---

# Related Documents

- [interface.md](interface.md)
- [execution.md](execution.md)
- [error-model.md](error-model.md)
