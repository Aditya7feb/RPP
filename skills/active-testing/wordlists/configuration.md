# Wordlists Configuration

**File:** `skills/active-testing/wordlists/configuration.md`

**Version:** 1.0.0

---

# Purpose

This document defines the declarative configuration of the Wordlists Capability and the
precedence rules that govern it.

---

# Configuration Object

```yaml
wordlists:
  registry:
    default_lists:
  selection:
    default_max_entries:
    deterministic_sampling: true
  emit:
    default_form: artifact
```

---

# Field Definitions

## registry

`default_lists` enumerates the named lists available by default.

## selection

`default_max_entries` bounds default sample size. `deterministic_sampling` SHALL default to
`true` for reproducibility.

## emit

`default_form` selects the default output form, `artifact` or `seeds`.

---

# Precedence

Configuration precedence, from highest to lowest, SHALL be

1. Per-request `selection` and `emit`
2. Capability configuration in this document
3. Documented defaults

---

# Validation Rules

- `default_max_entries` SHALL be a positive integer when present.
- Unknown fields SHALL be ignored for forward compatibility.

---

# Related Documents

- [interface.md](interface.md)
- [execution.md](execution.md)
- [error-model.md](error-model.md)
