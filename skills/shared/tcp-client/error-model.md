# TCP Client Error Model

**File:** `skills/shared/tcp-client/error-model.md`

**Version:** 1.0.0

---

# Purpose

This document defines the error model for the TCP Client Shared Skill.

The error model classifies the failure conditions the shared skill MAY produce
and aligns them with
[the platform error handling model](../../core/error-handling.md).

All errors SHALL be normalized and implementation independent.

---

# Error Philosophy

The TCP Client Shared Skill SHALL

- Produce canonical, structured errors
- Distinguish connection failures from governance rejections
- Preserve enough context for auditing
- Never leak secret payloads

---

# Error Categories

The TCP Client maps its failures onto the canonical categories.

```
Configuration

Validation

Resolution

Connection

Timeout

Governance

Adapter

Internal
```

---

# Configuration Errors

Raised when configuration is invalid or incomplete.

Conditions

- A referenced default policy does not resolve
- `deadline` is less than `connect`

Configuration errors SHALL be non-retryable.

---

# Validation Errors

Raised when an invocation is malformed.

Conditions

- Missing or out-of-range port
- Missing endpoint
- Unbounded read requested without `max_bytes`

Validation errors SHALL be non-retryable.

---

# Resolution Errors

Raised when a hostname cannot be resolved.

Resolution errors SHALL propagate the canonical
[DNS Client](../dns-client/README.md) error and MAY be retryable subject to the
caller policy.

---

# Connection Errors

Raised when a connection cannot be established or is reset.

Conditions

- Connection refused
- Connection reset
- Network unreachable

Connection errors MAY be retryable subject to the caller policy.

---

# Timeout Errors

Raised when a bound is exceeded.

Conditions

- Connect timeout
- Read timeout
- Write timeout
- Deadline exceeded

Timeout errors SHALL carry the breached bound.

---

# Governance Errors

Raised when a connection would violate governance.

Conditions

- Direct egress required but prohibited
- Rate ceiling would be exceeded

Governance errors SHALL be non-retryable without operator intervention.

---

# Adapter Errors

Raised when an underlying transport adapter fails unexpectedly.

Adapter errors SHALL be normalized so that consumers remain unaware of the
implementation.

---

# Internal Errors

Raised for unexpected conditions within the TCP Client.

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

endpoint:

breached_bound:
```

`category` SHALL be one of the canonical categories.

`retryable` SHALL indicate whether the operation MAY be attempted again.

Errors SHALL NOT contain secret payload material.

---

# Outcome Mapping

| Outcome | Category | Retryable |
|---------|----------|-----------|
| connect_failed | Connection | Policy dependent |
| reset | Connection | Policy dependent |
| timed_out | Timeout | No |
| resolution_failed | Resolution | Policy dependent |
| rejected | Governance | No |
| invalid_endpoint | Validation | No |
| missing_policy | Configuration | No |
| adapter_failure | Adapter | Policy dependent |
| unexpected | Internal | No |

---

# Interaction With Retry And Rate Limiter

`Connection`, `Timeout`, and `Resolution` errors MAY be retried through the
[Retry](../retry/README.md) shared skill, and each retry SHALL acquire a fresh
permit from the [Rate Limiter](../rate-limiter/README.md).

`Governance` errors SHALL NOT be retried automatically.

---

# Evidence

Errors SHOULD be captured as evidence conforming to the
[Evidence schema](../../../schemas/evidence.md), including the category and
endpoint, and SHALL exclude secret payloads.

---

# Related Documents

- [Interface](interface.md)
- [Execution](execution.md)
- [Error Handling Model](../../core/error-handling.md)
- [DNS Client](../dns-client/README.md)
