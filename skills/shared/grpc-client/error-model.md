# gRPC Client Error Model

**File:** `skills/shared/grpc-client/error-model.md`

**Version:** 1.0.0

---

# Purpose

This document defines the error model for the gRPC Client Shared Skill.

The error model classifies the failure conditions the shared skill MAY produce
and aligns them with
[the platform error handling model](../../core/error-handling.md).

All errors SHALL be normalized and implementation independent.

---

# Error Philosophy

The gRPC Client Shared Skill SHALL

- Produce canonical, structured errors
- Preserve the gRPC status code in mapped errors
- Distinguish transport failures from status errors
- Never leak secret payloads or metadata

---

# Error Categories

The gRPC Client maps its failures onto the canonical categories.

```
Configuration

Validation

Channel

Transport

Status

Timeout

Governance

Adapter

Internal
```

---

# Configuration Errors

Raised when configuration is invalid.

Conditions

- A referenced default policy does not resolve
- Invalid retryable status code configured

Configuration errors SHALL be non-retryable.

---

# Validation Errors

Raised when an invocation is malformed.

Conditions

- Missing service or method
- Invalid method kind
- A message exceeding size bounds
- Inline secret in metadata

Validation errors SHALL be non-retryable.

---

# Channel Errors

Raised when the HTTP/2 channel cannot be established.

Channel errors SHALL propagate the canonical
[HTTP Client](../http-client/README.md) error and MAY be retryable when
transient.

---

# Transport Errors

Raised when messages cannot be exchanged.

Conditions

- Stream reset
- Message write failure

Transport errors MAY be retryable only for idempotent calls.

---

# Status Errors

Raised when the call completes with a non-`OK` gRPC status.

Status errors SHALL preserve the gRPC status code.

Configured retryable statuses MAY be retried; other statuses SHALL NOT.

---

# Timeout Errors

Raised when the call deadline is exceeded.

Timeout errors SHALL carry the deadline.

---

# Governance Errors

Raised when a call would violate governance.

Conditions

- Direct egress required but prohibited
- Rate ceiling exceeded

Governance errors SHALL be non-retryable without operator intervention.

---

# Adapter Errors

Raised when an underlying transport adapter fails unexpectedly.

Adapter errors SHALL be normalized so that consumers remain unaware of the
implementation.

---

# Internal Errors

Raised for unexpected conditions within the gRPC Client.

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

authority:

status_code:
```

`category` SHALL be one of the canonical categories.

`status_code` SHALL carry the gRPC status where applicable.

`retryable` SHALL indicate whether the call MAY be attempted again.

Errors SHALL NOT contain secret payload or metadata material.

---

# Outcome Mapping

| Outcome | Category | Retryable |
|---------|----------|-----------|
| channel_failed | Channel | Transient only |
| reset | Transport | Idempotent only |
| status_error | Status | Configured statuses only |
| timed_out | Timeout | No |
| rejected | Governance | No |
| invalid_method | Validation | No |
| missing_policy | Configuration | No |
| adapter_failure | Adapter | Policy dependent |
| unexpected | Internal | No |

---

# Status Mapping Principle

A non-`OK` gRPC status SHALL be preserved in the canonical error so that domain
skills MAY interpret it.

The gRPC Client SHALL NOT interpret a status as a security weakness.

---

# Evidence

Errors SHOULD be captured as evidence conforming to the
[Evidence schema](../../../schemas/evidence.md), including the category,
authority, and status code, and SHALL exclude secret payloads and metadata.

---

# Related Documents

- [Interface](interface.md)
- [Execution](execution.md)
- [Error Handling Model](../../core/error-handling.md)
- [HTTP Client](../http-client/README.md)
