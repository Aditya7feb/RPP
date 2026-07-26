# Evidence Bundle Configuration

**File:** `skills/reporting/evidence-bundle/configuration.md`

**Version:** 1.0.0

---

# Purpose

This document defines the declarative configuration of the Evidence Bundle Capability and the
precedence rules that govern it.

---

# Configuration Object

```yaml
evidence_bundle:
  bounds:
    max_evidence:
    max_size_bytes:
  integrity:
    verify: true
  redaction:
    redact_sensitive: true
  format:
    bundle_format:
```

---

# Field Definitions

## bounds

`max_evidence` and `max_size_bytes` bound the bundle. The capability SHALL NOT exceed these bounds.

## integrity

`verify` SHALL default to `true`, verifying integrity references through the shared Evidence
infrastructure.

## redaction

`redact_sensitive` SHALL default to `true` for distribution.

## format

`bundle_format` names the bundle serialization produced through the shared Reporting package.

---

# Precedence

Configuration precedence, from highest to lowest, SHALL be

1. Per-request `redaction` and `bounds`
2. Capability configuration in this document
3. Documented defaults

---

# Validation Rules

- `max_evidence` and `max_size_bytes` SHALL be positive values when present.
- `verify` SHOULD remain `true`.
- Unknown fields SHALL be ignored for forward compatibility.

---

# Related Documents

- [interface.md](interface.md)
- [execution.md](execution.md)
- [error-model.md](error-model.md)
