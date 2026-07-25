# SMTP Client Error Model

**File:** `skills/shared/smtp-client/error-model.md`

**Version:** 1.0.0

---

# Purpose

This document defines the error model for the SMTP Client Shared Skill.

The error model classifies the failure conditions the shared skill MAY produce
and aligns them with
[the platform error handling model](../../core/error-handling.md).

All errors SHALL be normalized and implementation independent.

---

# Error Philosophy

The SMTP Client Shared Skill SHALL

- Produce canonical, structured errors
- Preserve SMTP reply codes in mapped errors
- Refuse cleartext where confidentiality is required
- Never leak credentials or unauthorized message bodies

---

# Error Categories

The SMTP Client maps its failures onto the canonical categories.

```
Configuration

Validation

Connection

Security

Authentication

Protocol

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
- `require_tls_for_auth` disabled

Configuration errors SHALL be non-retryable.

---

# Validation Errors

Raised when an invocation is malformed.

Conditions

- Missing or out-of-range port
- Inline secret supplied
- Message exceeding size bounds

Validation errors SHALL be non-retryable.

---

# Connection Errors

Raised when a session cannot be established.

Connection errors SHALL propagate the canonical
[TCP Client](../tcp-client/README.md) error and MAY be retryable when transient.

---

# Security Errors

Raised when confidentiality cannot be assured.

Conditions

- `starttls_required` and `STARTTLS` unavailable
- TLS upgrade failure

Security errors SHALL terminate the session and SHALL be non-retryable without a
policy change.

---

# Authentication Errors

Raised when authentication fails.

Conditions

- Credentials rejected
- Authentication attempted over cleartext when prohibited

Authentication errors SHALL NOT expose credentials and SHALL be non-retryable
without new credentials.

---

# Protocol Errors

Raised when the server returns an error reply.

- `4xx` maps to a transient protocol error, potentially retryable
- `5xx` maps to a permanent protocol error, non-retryable

Protocol errors SHALL preserve the SMTP reply code.

---

# Timeout Errors

Raised when a bound is exceeded.

Conditions

- Command timeout
- Session timeout

Timeout errors SHALL carry the breached bound.

---

# Governance Errors

Raised when a session or command would violate governance.

Conditions

- Direct egress required but prohibited
- Message send attempted when `allow_message_send` is disabled
- Rate ceiling exceeded

Governance errors SHALL be non-retryable without operator intervention.

---

# Adapter Errors

Raised when an underlying transport adapter fails unexpectedly.

Adapter errors SHALL be normalized so that consumers remain unaware of the
implementation.

---

# Internal Errors

Raised for unexpected conditions within the SMTP Client.

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

host:

reply_code:
```

`category` SHALL be one of the canonical categories.

`reply_code` SHALL carry the SMTP reply code where applicable.

`retryable` SHALL indicate whether the operation MAY be attempted again.

Errors SHALL NOT contain credentials or unauthorized message bodies.

---

# Outcome Mapping

| Outcome | Category | Retryable |
|---------|----------|-----------|
| connect_failed | Connection | Transient only |
| tls_required_unavailable | Security | No |
| tls_upgrade_failed | Security | No |
| auth_failed | Authentication | No |
| transient_reply | Protocol | Yes (4xx) |
| permanent_reply | Protocol | No (5xx) |
| timed_out | Timeout | No |
| send_blocked | Governance | No |
| rejected | Governance | No |
| invalid_request | Validation | No |
| adapter_failure | Adapter | Policy dependent |
| unexpected | Internal | No |

---

# Confidentiality Principle

The SMTP Client SHALL never authenticate or transmit sensitive material over
cleartext when confidentiality is required.

A `starttls_required` session without `STARTTLS` SHALL fail rather than downgrade.

---

# Evidence

Errors SHOULD be captured as evidence conforming to the
[Evidence schema](../../../schemas/evidence.md), including the category, host,
and reply code, and SHALL exclude credentials.

---

# Related Documents

- [Interface](interface.md)
- [Execution](execution.md)
- [Error Handling Model](../../core/error-handling.md)
- [TCP Client](../tcp-client/README.md)
