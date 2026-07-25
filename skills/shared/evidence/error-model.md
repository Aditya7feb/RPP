# Evidence Error Model

**File:** `skills/shared/evidence/error-model.md`

**Version:** 1.0.0

---

# Purpose

This document defines the error model for the Evidence Shared Skill.

The error model classifies the failure conditions the shared skill MAY produce
and aligns them with
[the platform error handling model](../../core/error-handling.md).

All errors SHALL be normalized and implementation independent.

---

# Error Philosophy

The Evidence Shared Skill SHALL

- Produce canonical, structured errors
- Preserve integrity and never return tampered evidence as valid
- Fail closed on redaction failure to protect secrets
- Never leak secret material through errors

---

# Error Categories

The Evidence Shared Skill maps its failures onto the canonical categories.

```
Configuration

Validation

Redaction

Integrity

Storage

Scope

Adapter

Internal
```

---

# Configuration Errors

Raised when configuration is invalid.

Conditions

- No backend configured
- Integrity sealing disabled
- Redaction disabled
- Invalid dispose policy

Configuration errors SHALL be non-retryable.

---

# Validation Errors

Raised when a capture request is malformed.

Conditions

- Missing evidence `type`
- Inline payload exceeding inline limits
- Non-secret fields containing unredactable secrets

Validation errors SHALL be non-retryable.

---

# Redaction Errors

Raised when redaction cannot be completed.

Redaction errors SHALL fail the capture closed; no evidence SHALL be persisted.

Redaction errors SHALL NOT expose the unredacted content.

---

# Integrity Errors

Raised when sealing fails or verification detects tampering.

Conditions

- Sealing cannot be computed
- A resolved record fails digest verification

Integrity errors SHALL prevent returning the evidence as valid and SHALL be
reported for investigation.

---

# Storage Errors

Raised when an artifact or record cannot be stored or loaded.

Conditions

- Artifact exceeds `max_artifact_bytes`
- Backend rejects or loses a record

Storage errors on capture SHALL fail the capture without issuing a reference.

Storage errors MAY be retryable subject to the caller policy.

---

# Scope Errors

Raised when a reference is resolved outside its scope.

Scope errors SHALL return `out_of_scope` and SHALL be non-retryable without a
policy change.

---

# Adapter Errors

Raised when an underlying backend fails unexpectedly.

Adapter errors SHALL be normalized so that consumers remain unaware of the
implementation.

---

# Internal Errors

Raised for unexpected conditions within the Evidence Shared Skill.

Internal errors SHALL be treated as non-retryable and SHOULD be reported for
diagnosis.

---

# Error Structure

Every error SHALL conform to the canonical error structure.

```yaml
category:

code:

message:

retryable:

evidence_ref:

scope:
```

`category` SHALL be one of the canonical categories.

`retryable` SHALL indicate whether the operation MAY be attempted again.

Errors SHALL NOT contain secret material or unredacted evidence content.

---

# Outcome Mapping

| Outcome | Category | Retryable |
|---------|----------|-----------|
| no_backend | Configuration | No |
| sealing_disabled | Configuration | No |
| malformed_capture | Validation | No |
| redaction_failed | Redaction | No (fails closed) |
| seal_failed | Integrity | No |
| tamper_detected | Integrity | No |
| artifact_too_large | Storage | No |
| backend_error | Storage | Policy dependent |
| out_of_scope | Scope | No |
| adapter_failure | Adapter | Policy dependent |
| unexpected | Internal | No |

---

# Integrity Principle

The Evidence Shared Skill SHALL never return evidence that fails integrity
verification as valid.

Detected tampering SHALL be surfaced as an integrity error and preserved for
audit rather than silently ignored.

---

# Related Documents

- [Interface](interface.md)
- [Execution](execution.md)
- [Error Handling Model](../../core/error-handling.md)
- [Evidence Schema](../../../schemas/evidence.md)
