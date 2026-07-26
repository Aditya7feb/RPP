# Artifact Collection Configuration

**File:** `skills/evidence/artifact-collection/configuration.md`

**Version:** 1.0.0

---

# Purpose

This document defines the declarative configuration of the Artifact Collection Capability and the
precedence rules that govern it.

---

# Configuration Object

```yaml
artifact_collection:
  types:
    enabled:
  bounds:
    max_artifacts:
    max_size_bytes:
  redaction:
    redact_sensitive: true
  evidence:
    promote: true
    integrity_hash: true
```

---

# Field Definitions

## types

`enabled` enumerates the artifact types collected, such as `file` and `certificate`.

## bounds

`max_artifacts` and `max_size_bytes` bound collection. The capability SHALL NOT exceed these
bounds.

## redaction

`redact_sensitive` SHALL default to `true`.

## evidence

`promote` SHALL default to `true`, invoking the shared Evidence lifecycle. `integrity_hash` SHALL
default to `true`.

---

# Precedence

Configuration precedence, from highest to lowest, SHALL be

1. Rules of Engagement and Scope constraints
2. Per-request parameters
3. Capability configuration in this document
4. Documented defaults

---

# Validation Rules

- `max_artifacts` and `max_size_bytes` SHALL be positive values when present.
- Unknown fields SHALL be ignored for forward compatibility.

---

# Related Documents

- [interface.md](interface.md)
- [execution.md](execution.md)
- [error-model.md](error-model.md)
