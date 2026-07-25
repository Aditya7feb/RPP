# SSH Client Error Model

**File:** `skills/shared/ssh-client/error-model.md`

**Version:** 1.0.0

---

# Purpose

This document defines the error model for the SSH Client Shared Skill.

The error model classifies the failure conditions the shared skill MAY produce
and aligns them with
[the platform error handling model](../../core/error-handling.md).

All errors SHALL be normalized and implementation independent.

---

# Error Philosophy

The SSH Client Shared Skill SHALL

- Produce canonical, structured errors
- Treat host-key rejection as a safety-preserving outcome
- Bound authentication attempts
- Never leak credentials, private keys, or unauthorized output

---

# Error Categories

The SSH Client maps its failures onto the canonical categories.

```
Configuration

Validation

Connection

HostKey

Authentication

Channel

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
- `record_only` used outside a permitted discovery context

Configuration errors SHALL be non-retryable.

---

# Validation Errors

Raised when an invocation is malformed.

Conditions

- Missing or out-of-range port
- Inline secret or private key supplied
- An `exec` operation without authorization

Validation errors SHALL be non-retryable.

---

# Connection Errors

Raised when the transport cannot be established.

Connection errors SHALL propagate the canonical
[TCP Client](../tcp-client/README.md) error and MAY be retryable when transient.

---

# Host-Key Errors

Raised when host-key verification fails.

Conditions

- Unknown key under `strict`
- Changed key under `strict` or `trust_on_first_use`

Host-key errors SHALL be non-retryable without a trust decision and SHALL
preserve the fingerprint for audit.

---

# Authentication Errors

Raised when authentication fails.

Conditions

- Credentials or key rejected
- Attempts exceed `max_attempts`

Authentication errors SHALL NOT expose credentials or keys and SHALL be
non-retryable beyond the attempt bound.

---

# Channel Errors

Raised when a channel or operation fails.

Conditions

- Channel open rejected
- Execution not authorized
- Forwarding not permitted
- Output exceeds `max_output_bytes`

Channel errors SHALL be handled per operation authorization.

---

# Timeout Errors

Raised when a bound is exceeded.

Conditions

- Command timeout
- Session timeout

Timeout errors SHALL carry the breached bound.

---

# Governance Errors

Raised when a session or operation would violate governance.

Conditions

- Direct egress required but prohibited
- Execution attempted when disabled
- Forwarding attempted when disabled
- Rate ceiling exceeded

Governance errors SHALL be non-retryable without operator intervention.

---

# Adapter Errors

Raised when an underlying transport adapter fails unexpectedly.

Adapter errors SHALL be normalized so that consumers remain unaware of the
implementation.

---

# Internal Errors

Raised for unexpected conditions within the SSH Client.

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

fingerprint:
```

`category` SHALL be one of the canonical categories.

`fingerprint` SHALL carry the host-key fingerprint for host-key errors.

`retryable` SHALL indicate whether the operation MAY be attempted again.

Errors SHALL NOT contain credentials, private keys, or unauthorized output.

---

# Outcome Mapping

| Outcome | Category | Retryable |
|---------|----------|-----------|
| connect_failed | Connection | Transient only |
| host_key_rejected | HostKey | No |
| auth_failed | Authentication | No (beyond bound) |
| channel_failed | Channel | Per authorization |
| exec_unauthorized | Validation | No |
| timed_out | Timeout | No |
| forwarding_blocked | Governance | No |
| rejected | Governance | No |
| adapter_failure | Adapter | Policy dependent |
| unexpected | Internal | No |

---

# Host-Key Principle

The SSH Client SHALL NOT silently accept an unknown or changed host key under a
`strict` policy.

A rejected host key SHALL be surfaced with its fingerprint so that domain skills
MAY interpret and operators MAY decide.

---

# Evidence

Errors SHOULD be captured as evidence conforming to the
[Evidence schema](../../../schemas/evidence.md), including the category, host,
and fingerprint, and SHALL exclude credentials and keys.

---

# Related Documents

- [Interface](interface.md)
- [Execution](execution.md)
- [Error Handling Model](../../core/error-handling.md)
- [TCP Client](../tcp-client/README.md)
