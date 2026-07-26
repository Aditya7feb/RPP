# Finding Mapping Configuration

**File:** `skills/reporting/finding-mapping/configuration.md`

**Version:** 1.0.0

---

# Purpose

This document defines the declarative configuration of the Finding Mapping Capability and the
precedence rules that govern it.

---

# Configuration Object

```yaml
finding_mapping:
  frameworks:
    owasp: true
    mitre_attack: true
  bounds:
    max_findings:
  presentation:
    enrichment_only: true
```

---

# Field Definitions

## frameworks

`owasp` and `mitre_attack` enable mapping frameworks. Both default to `true`.

## bounds

`max_findings` bounds mapping scope. The capability SHALL NOT exceed this bound.

## presentation

`enrichment_only` SHALL default to `true`, marking mappings as presentation enrichment that does not
alter canonical Finding classification.

---

# Precedence

Configuration precedence, from highest to lowest, SHALL be

1. Per-request `mapping` and `bounds`
2. Capability configuration in this document
3. Documented defaults

---

# Validation Rules

- `max_findings` SHALL be a positive integer when present.
- `enrichment_only` SHALL remain `true`.
- Unknown fields SHALL be ignored for forward compatibility.

---

# Related Documents

- [interface.md](interface.md)
- [execution.md](execution.md)
- [error-model.md](error-model.md)
