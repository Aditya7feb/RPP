# WebSocket Client Error Model

**File:** `skills/shared/websocket-client/error-model.md`

**Version:** 1.0.0

---

# Purpose

This document defines the error model for the WebSocket Client Shared Skill.

The error model classifies the failure conditions the shared skill MAY produce
and aligns them with
[the platform error handling model](../../core/error-handling.md).

All errors SHALL be normalized and implementation independent.

---

# Error Philosophy

The WebSocket Client Shared Skill SHALL

- Produce canonical, structured errors
- Distinguish handshake failures from frame-exchange failures
- Treat a peer-initiated close as a normal terminal condition
- Never leak secret payloads

---

# Error Categories

The WebSocket Client maps its failures onto the canonical categories.

```
Configuration

Validation

Handshake

Transport

Negotiation

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
- `max_message_bytes` less than `max_fragment_bytes`

Configuration errors SHALL be non-retryable.

---

# Validation Errors

Raised when an invocation is malformed.

Conditions

- Invalid `ws` or `wss` URL
- Inline secret supplied
- A frame exceeding message bounds

Validation errors SHALL be non-retryable.

---

# Handshake Errors

Raised when the upgrade handshake fails.

Handshake errors SHALL propagate the canonical
[HTTP Client](../http-client/README.md) error and MAY be retryable when
transient.

---

# Transport Errors

Raised when frames cannot be exchanged.

Conditions

- Connection reset during exchange
- Frame write failure

Transport errors MAY be retryable only when the caller declares the exchange
safe to repeat.

---

# Negotiation Errors

Raised when a required subprotocol is unavailable.

Conditions

- `require_subprotocol` is `true` and no acceptable subprotocol is offered

Negotiation errors SHALL be non-retryable without changing requirements.

---

# Timeout Errors

Raised when a bound is exceeded.

Conditions

- Handshake timeout
- Idle timeout
- Connection lifetime exceeded

Timeout errors SHALL carry the breached bound.

---

# Governance Errors

Raised when a connection would violate governance.

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

Raised for unexpected conditions within the WebSocket Client.

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

url:

close_code:
```

`category` SHALL be one of the canonical categories.

`retryable` SHALL indicate whether the operation MAY be attempted again.

Errors SHALL NOT contain secret payload material.

---

# Outcome Mapping

| Outcome | Category | Retryable |
|---------|----------|-----------|
| handshake_failed | Handshake | Transient only |
| closed_by_peer | (normal terminal) | N/A |
| reset | Transport | Caller declared |
| subprotocol_unavailable | Negotiation | No |
| timed_out | Timeout | No |
| rejected | Governance | No |
| invalid_url | Validation | No |
| missing_policy | Configuration | No |
| adapter_failure | Adapter | Policy dependent |
| unexpected | Internal | No |

---

# Peer Close Principle

A peer-initiated close SHALL be treated as a normal terminal condition, recorded
with its close code and reason, rather than an error.

Consumers SHALL decide whether a particular close code is significant.

---

# Evidence

Errors SHOULD be captured as evidence conforming to the
[Evidence schema](../../../schemas/evidence.md), including the category, URL, and
close code, and SHALL exclude secret payloads.

---

# Related Documents

- [Interface](interface.md)
- [Execution](execution.md)
- [Error Handling Model](../../core/error-handling.md)
- [HTTP Client](../http-client/README.md)
