# Cloud Storage Client Error Model

**File:** `skills/shared/cloud-storage-client/error-model.md`

**Version:** 1.0.0

---

# Purpose

This document defines the error model for the Cloud Storage Client Shared Skill.

The error model classifies the failure conditions the shared skill MAY produce
and aligns them with
[the platform error handling model](../../core/error-handling.md).

All errors SHALL be normalized and implementation independent.

---

# Error Philosophy

The Cloud Storage Client Shared Skill SHALL

- Produce canonical, structured errors
- Enforce scope confinement and encryption as boundaries
- Distinguish scope rejection from ordinary not-found conditions
- Never leak object contents or presigned references

---

# Error Categories

The Cloud Storage Client maps its failures onto the canonical categories.

```
Configuration

Validation

Scope

Authentication

Encryption

NotFound

Authorization

Timeout

Governance

Adapter

Internal
```

---

# Configuration Errors

Raised when configuration is invalid.

Conditions

- A referenced scope does not exist
- Required server-side encryption disabled
- A referenced default policy does not resolve

Configuration errors SHALL be non-retryable.

---

# Validation Errors

Raised when an invocation is malformed.

Conditions

- Missing scope or key
- Inline secret supplied
- A write without an encryption declaration

Validation errors SHALL be non-retryable.

---

# Scope Errors

Raised when an object key escapes its authorized scope.

Scope errors SHALL be non-retryable and SHALL preserve the attempted key for
audit without performing the operation.

---

# Authentication Errors

Raised when provider authentication fails.

Authentication errors SHALL NOT expose credentials and SHALL be non-retryable
without new credentials.

---

# Encryption Errors

Raised when required encryption cannot be assured.

Conditions

- Server-side encryption required but unavailable
- Client-side key resolution failure

Encryption errors SHALL fail the write rather than store unencrypted data.

---

# Not-Found Errors

Raised when a confined object does not exist.

Not-found errors SHALL be distinguished from scope rejections and MAY be expected
during discovery.

---

# Authorization Errors

Raised when an intrusive operation is not authorized.

Conditions

- Write, delete, or policy change attempted when disabled
- Write attempted on a non-writable scope

Authorization errors SHALL be non-retryable without a policy change.

---

# Timeout Errors

Raised when an operation exceeds its bound.

Timeout errors SHALL carry the breached bound.

---

# Governance Errors

Raised when an operation would violate governance.

Conditions

- Presign attempted when disabled
- Rate ceiling exceeded

Governance errors SHALL be non-retryable without operator intervention.

---

# Adapter Errors

Raised when an underlying provider adapter fails unexpectedly.

Adapter errors SHALL be normalized so that consumers remain unaware of the
implementation.

---

# Internal Errors

Raised for unexpected conditions within the Cloud Storage Client.

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

scope_id:

key:
```

`category` SHALL be one of the canonical categories.

`retryable` SHALL indicate whether the operation MAY be attempted again.

Errors SHALL NOT contain object contents or presigned references.

---

# Outcome Mapping

| Outcome | Category | Retryable |
|---------|----------|-----------|
| scope_rejected | Scope | No |
| auth_failed | Authentication | No |
| encryption_required_unavailable | Encryption | No |
| not_found | NotFound | Context dependent |
| write_blocked | Authorization | No |
| presign_blocked | Governance | No |
| timed_out | Timeout | No |
| rejected | Governance | No |
| invalid_request | Validation | No |
| missing_scope | Configuration | No |
| adapter_failure | Adapter | Policy dependent |
| unexpected | Internal | No |

---

# Confinement Principle

The Cloud Storage Client SHALL never perform an operation on an object outside an
authorized scope.

A scope violation SHALL be rejected and preserved for audit rather than silently
normalized.

---

# Evidence

Errors SHOULD be captured as evidence conforming to the
[Evidence schema](../../../schemas/evidence.md), including the category, scope,
and attempted key, and SHALL exclude object contents and presigned references.

---

# Related Documents

- [Interface](interface.md)
- [Execution](execution.md)
- [Error Handling Model](../../core/error-handling.md)
- [Secrets Client](../secrets-client/README.md)
