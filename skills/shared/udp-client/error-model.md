# UDP Client Error Model

**File:** `skills/shared/udp-client/error-model.md`

**Version:** 1.0.0

---

# Purpose

This document defines the error model for the UDP Client Shared Skill.

The error model classifies the failure conditions the shared skill MAY produce
and aligns them with
[the platform error handling model](../../core/error-handling.md).

All errors SHALL be normalized and implementation independent.

---

# Error Philosophy

The UDP Client Shared Skill SHALL

- Produce canonical, structured errors
- Distinguish a normal `no_response` outcome from transport errors
- Enforce amplification protection as a hard boundary
- Never leak secret payloads

---

# Error Categories

The UDP Client maps its failures onto the canonical categories.

```
Configuration

Validation

Resolution

Transport

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
- Amplification protection disabled

Configuration errors SHALL be non-retryable.

---

# Validation Errors

Raised when an invocation is malformed.

Conditions

- Missing or out-of-range port
- Payload exceeding `max_payload_bytes`
- Retry requested for a non-idempotent exchange

Validation errors SHALL be non-retryable.

---

# Resolution Errors

Raised when a hostname cannot be resolved.

Resolution errors SHALL propagate the canonical
[DNS Client](../dns-client/README.md) error and MAY be retryable subject to the
caller policy.

---

# Transport Errors

Raised when a datagram cannot be sent or an ICMP error is observed.

Conditions

- Send failure
- Port unreachable indication

Transport errors MAY be retryable only for idempotent exchanges.

---

# Timeout Errors

Raised when a total deadline is exceeded.

A `no_response` within the response window is NOT a timeout error; a breached
total `deadline` is.

---

# Governance Errors

Raised when an exchange would violate governance.

Conditions

- Direct egress required but prohibited when UDP proxying is unavailable
- Amplification ratio exceeded
- Rate ceiling exceeded

Governance errors SHALL be non-retryable without operator intervention.

---

# Adapter Errors

Raised when an underlying transport adapter fails unexpectedly.

Adapter errors SHALL be normalized so that consumers remain unaware of the
implementation.

---

# Internal Errors

Raised for unexpected conditions within the UDP Client.

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
```

`category` SHALL be one of the canonical categories.

`retryable` SHALL indicate whether the exchange MAY be attempted again.

Errors SHALL NOT contain secret payload material.

---

# Outcome Mapping

| Outcome | Category | Retryable |
|---------|----------|-----------|
| no_response | (normal outcome) | N/A |
| send_failed | Transport | Idempotent only |
| port_unreachable | Transport | Idempotent only |
| timed_out | Timeout | No |
| resolution_failed | Resolution | Policy dependent |
| amplification_exceeded | Governance | No |
| direct_egress_blocked | Governance | No |
| invalid_payload | Validation | No |
| adapter_failure | Adapter | Policy dependent |
| unexpected | Internal | No |

---

# No-Response Principle

A `no_response` outcome SHALL be treated as a normal result of an unreliable
protocol, not an error.

Consumers SHALL decide whether the absence of a response is significant for their
domain purpose.

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
