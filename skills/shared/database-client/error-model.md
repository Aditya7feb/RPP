# Database Client Error Model

**File:** `skills/shared/database-client/error-model.md`

**Version:** 1.0.0

---

# Purpose

This document defines the error model for the Database Client Shared Skill.

The error model classifies the failure conditions the shared skill MAY produce
and aligns them with
[the platform error handling model](../../core/error-handling.md).

All errors SHALL be normalized and implementation independent.

---

# Error Philosophy

The Database Client Shared Skill SHALL

- Produce canonical, structured errors
- Preserve engine error codes for domain interpretation
- Enforce parameterization and encryption as boundaries
- Never leak credentials or parameter values

---

# Error Categories

The Database Client maps its failures onto the canonical categories.

```
Configuration

Validation

Connection

Security

Authentication

Statement

Transaction

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
- Parameterization disabled
- `require_tls_for_auth` disabled

Configuration errors SHALL be non-retryable.

---

# Validation Errors

Raised when an invocation is malformed.

Conditions

- Missing or out-of-range port
- Inline secret supplied
- A value interpolated into statement text rather than bound
- A `write` statement without authorization

Validation errors SHALL be non-retryable.

---

# Connection Errors

Raised when the connection cannot be established.

Connection errors SHALL propagate the canonical
[TCP Client](../tcp-client/README.md) error and MAY be retryable when transient.

---

# Security Errors

Raised when encryption cannot be assured.

Conditions

- `required` encryption unavailable
- TLS negotiation failure

Security errors SHALL fail the operation and SHALL be non-retryable without a
policy change.

---

# Authentication Errors

Raised when authentication fails.

Conditions

- Credentials rejected
- Authentication over cleartext when prohibited

Authentication errors SHALL NOT expose credentials and SHALL be non-retryable
without new credentials.

---

# Statement Errors

Raised when a statement fails.

Conditions

- Syntax or constraint error reported by the engine
- Permission denied by the engine

Statement errors SHALL preserve the engine error code and SHALL NOT be classified
as security findings.

---

# Transaction Errors

Raised when a transaction cannot begin, commit, or roll back.

A commit failure SHALL trigger rollback where possible.

Transaction errors SHALL preserve consistency and SHALL be surfaced.

---

# Timeout Errors

Raised when a bound is exceeded.

Conditions

- Statement timeout
- Connection timeout

Timeout errors SHALL carry the breached bound.

---

# Governance Errors

Raised when an operation would violate governance.

Conditions

- Direct egress required but prohibited
- Write attempted when `allow_write_statements` is disabled
- Schema change attempted when `allow_schema_changes` is disabled
- Rate ceiling exceeded

Governance errors SHALL be non-retryable without operator intervention.

---

# Adapter Errors

Raised when an underlying engine adapter fails unexpectedly.

Adapter errors SHALL be normalized so that consumers remain unaware of the
implementation.

---

# Internal Errors

Raised for unexpected conditions within the Database Client.

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

engine:

engine_code:
```

`category` SHALL be one of the canonical categories.

`engine_code` SHALL carry the engine error code where applicable.

`retryable` SHALL indicate whether the operation MAY be attempted again.

Errors SHALL NOT contain credentials or parameter values.

---

# Outcome Mapping

| Outcome | Category | Retryable |
|---------|----------|-----------|
| connect_failed | Connection | Transient only |
| encryption_required_unavailable | Security | No |
| tls_failed | Security | No |
| auth_failed | Authentication | No |
| statement_error | Statement | No |
| transaction_error | Transaction | Idempotent only |
| timed_out | Timeout | No |
| write_blocked | Governance | No |
| rejected | Governance | No |
| interpolation_detected | Validation | No |
| adapter_failure | Adapter | Policy dependent |
| unexpected | Internal | No |

---

# Parameterization Principle

The Database Client SHALL reject operations that interpolate values into
statement text rather than binding them as parameters.

This boundary prevents injection regardless of how a domain skill constructs its
inputs.

---

# Evidence

Errors SHOULD be captured as evidence conforming to the
[Evidence schema](../../../schemas/evidence.md), including the category, engine,
and engine code, and SHALL exclude credentials and parameter values.

---

# Related Documents

- [Interface](interface.md)
- [Execution](execution.md)
- [Error Handling Model](../../core/error-handling.md)
- [TCP Client](../tcp-client/README.md)
