# Timeline Configuration

**File:** `skills/evidence/timeline/configuration.md`

**Version:** 1.0.0

---

# Purpose

This document defines the declarative configuration of the Timeline Capability and the precedence
rules that govern it.

---

# Configuration Object

```yaml
timeline:
  correlation:
    causal_links: true
  bounds:
    max_items:
  evidence:
    promote: true
```

---

# Field Definitions

## correlation

`causal_links` enables maintenance of causal relationships between correlated items.

## bounds

`max_items` bounds timeline size. The capability SHALL NOT exceed this bound.

## evidence

`promote` SHALL default to `true`, invoking the shared Evidence lifecycle to promote the timeline.

---

# Precedence

Configuration precedence, from highest to lowest, SHALL be

1. Per-request `correlation` and `bounds`
2. Capability configuration in this document
3. Documented defaults

---

# Validation Rules

- `max_items` SHALL be a positive integer when present.
- Unknown fields SHALL be ignored for forward compatibility.

---

# Related Documents

- [interface.md](interface.md)
- [execution.md](execution.md)
- [error-model.md](error-model.md)
