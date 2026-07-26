# Finding Correlation Configuration

**File:** `skills/reporting/finding-correlation/configuration.md`

**Version:** 1.0.0

---

# Purpose

This document defines the declarative configuration of the Finding Correlation Capability and the
precedence rules that govern it.

---

# Configuration Object

```yaml
finding_correlation:
  operations:
    deduplicate: true
    relate: true
    build_chains: true
  bounds:
    max_findings:
  determinism:
    stable_ordering: true
```

---

# Field Definitions

## operations

`deduplicate`, `relate`, and `build_chains` enable correlation operations. All default to `true`.

## bounds

`max_findings` bounds correlation scope. The capability SHALL NOT exceed this bound.

## determinism

`stable_ordering` SHALL default to `true` for reproducible output.

---

# Precedence

Configuration precedence, from highest to lowest, SHALL be

1. Per-request `correlation` and `bounds`
2. Capability configuration in this document
3. Documented defaults

---

# Validation Rules

- `max_findings` SHALL be a positive integer when present.
- Unknown fields SHALL be ignored for forward compatibility.

---

# Related Documents

- [interface.md](interface.md)
- [execution.md](execution.md)
- [error-model.md](error-model.md)
