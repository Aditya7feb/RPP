# Mutation Engine Configuration

**File:** `skills/active-testing/mutation-engine/configuration.md`

**Version:** 1.0.0

---

# Purpose

This document defines the declarative configuration of the Mutation Engine Capability and
the precedence rules that govern it.

---

# Configuration Object

```yaml
mutation_engine:
  strategies:
    enabled:
  bounds:
    default_max_variants:
  determinism:
    require_seed: true
  safety:
    mark_destructive_requires_approval: true
```

---

# Field Definitions

## strategies

`enabled` enumerates the mutation strategies available by default.

## bounds

`default_max_variants` bounds output when a request omits `max_variants`.

## determinism

`require_seed` SHALL default to `true`, requiring a seed for reproducible output.

## safety

`mark_destructive_requires_approval` SHALL default to `true`, ensuring destructive mutations
carry `requires_approval`.

---

# Precedence

Configuration precedence, from highest to lowest, SHALL be

1. Per-request `strategies` and `bounds`
2. Capability configuration in this document
3. Documented defaults

---

# Validation Rules

- `default_max_variants` SHALL be a positive integer when present.
- Unknown fields SHALL be ignored for forward compatibility.

---

# Related Documents

- [interface.md](interface.md)
- [execution.md](execution.md)
- [error-model.md](error-model.md)
