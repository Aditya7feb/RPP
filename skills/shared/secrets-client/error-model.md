# Secrets Client Error Model

**File:** `skills/shared/secrets-client/error-model.md`

**Version:** 1.0.0

---

# Purpose

This document defines the error model for the Secrets Client Shared Skill.

The error model classifies the failure conditions the shared skill MAY produce
and aligns them with
[the platform error handling model](../../core/error-handling.md).

All errors SHALL be normalized, implementation independent, and free of secret
values.

---

# Error Philosophy

The Secrets Client Shared Skill SHALL

- Produce canonical, structured errors
- Never expose secret values, including in error context
- Distinguish denial from absence
- Fail closed on any redaction uncertainty

---

# Error Categories

The Secrets Client maps its failures onto the canonical categories.

```
Configuration

Validation

NotFound

Authorization

Lease

Store

Adapter

Internal
```

---

# Configuration Errors

Raised when configuration is invalid.

Conditions

- A referenced store does not exist
- Redaction disabled
- Value return enabled

Configuration errors SHALL be non-retryable.

---

# Validation Errors

Raised when an invocation is malformed.

Conditions

- Missing secret reference
- Missing broker target for `broker_apply`
- A value supplied where only references are permitted

Validation errors SHALL be non-retryable.

---

# Not-Found Errors

Raised when a reference cannot be resolved.

Not-found errors SHALL be distinguished from authorization denials and MAY be
expected during discovery of references.

---

# Authorization Errors

Raised when access to a secret is denied.

Authorization errors SHALL NOT reveal whether the secret exists beyond what the
store permits and SHALL be non-retryable without a policy change.

---

# Lease Errors

Raised when a lease cannot be established or renewed, or a handle has expired.

Conditions

- Handle expired
- Lease renewal failure

Lease errors MAY be resolved by re-resolving the reference.

---

# Store Errors

Raised when the store cannot service a request.

Store errors SHALL be normalized and MAY be retryable subject to the caller
policy.

---

# Adapter Errors

Raised when an underlying store adapter fails unexpectedly.

Adapter errors SHALL be normalized so that consumers remain unaware of the
implementation.

---

# Internal Errors

Raised for unexpected conditions within the Secrets Client.

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

secret_ref:
```

`category` SHALL be one of the canonical categories.

`secret_ref` SHALL identify the reference, never the value.

`retryable` SHALL indicate whether the operation MAY be attempted again.

Errors SHALL NEVER contain secret values or any material from which a value could
be derived.

---

# Outcome Mapping

| Outcome | Category | Retryable |
|---------|----------|-----------|
| not_found | NotFound | Context dependent |
| denied | Authorization | No |
| expired | Lease | Re-resolve |
| lease_failed | Lease | Re-resolve |
| store_unavailable | Store | Policy dependent |
| redaction_disabled | Configuration | No |
| value_supplied | Validation | No |
| adapter_failure | Adapter | Policy dependent |
| unexpected | Internal | No |

---

# Non-Exposure Principle

No error path SHALL expose a secret value.

Where an operation cannot complete without risking exposure, the Secrets Client
SHALL fail closed and return a non-sensitive error.

---

# Evidence

Errors SHOULD be captured as non-sensitive evidence conforming to the
[Evidence schema](../../../schemas/evidence.md), including the category and secret
reference, and SHALL NEVER contain secret values.

---

# Related Documents

- [Interface](interface.md)
- [Execution](execution.md)
- [Error Handling Model](../../core/error-handling.md)
- [Authentication](../authentication/README.md)
