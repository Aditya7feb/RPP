# HTTP Archive Configuration

**File:** `skills/evidence/http-archive/configuration.md`

**Version:** 1.0.0

---

# Purpose

This document defines the declarative configuration of the HTTP Archive Capability and the
precedence rules that govern it.

---

# Configuration Object

```yaml
http_archive:
  bounds:
    max_transactions:
  format:
    archive_format: har
  redaction:
    redact_credentials: true
    redact_tokens: true
    redact_bodies:
  evidence:
    promote: true
    integrity_hash: true
```

---

# Field Definitions

## bounds

`max_transactions` bounds archived volume. The capability SHALL NOT exceed this bound.

## format

`archive_format` names the archive serialization, such as `har`.

## redaction

`redact_credentials` and `redact_tokens` SHALL default to `true`. `redact_bodies` controls body
redaction.

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

- `max_transactions` SHALL be a positive integer when present.
- Credential and token redaction SHOULD remain enabled.
- Unknown fields SHALL be ignored for forward compatibility.

---

# Related Documents

- [interface.md](interface.md)
- [execution.md](execution.md)
- [error-model.md](error-model.md)
