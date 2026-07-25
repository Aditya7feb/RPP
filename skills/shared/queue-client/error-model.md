# Queue Client Error Model

**File:** `skills/shared/queue-client/error-model.md`

**Version:** 1.0.0

---

# Purpose

This document defines the error model for the Queue Client Shared Skill.

The error model classifies the failure conditions the shared skill MAY produce
and aligns them with
[the platform error handling model](../../core/error-handling.md).

All errors SHALL be normalized and implementation independent.

---

# Error Philosophy

The Queue Client Shared Skill SHALL

- Produce canonical, structured errors
- Report delivery semantics honestly
- Preserve messages rather than lose them on failure
- Never leak sensitive message contents

---

# Error Categories

The Queue Client maps its failures onto the canonical categories.

```
Configuration

Validation

Connection

Authentication

Publish

Consume

Semantic

Timeout

Governance

Adapter

Internal
```

---

# Configuration Errors

Raised when configuration is invalid.

Conditions

- A referenced broker does not exist
- Redelivery bound absent
- A referenced default policy does not resolve

Configuration errors SHALL be non-retryable.

---

# Validation Errors

Raised when an invocation is malformed.

Conditions

- Missing broker or queue
- Inline secret supplied
- A message exceeding size bounds

Validation errors SHALL be non-retryable.

---

# Connection Errors

Raised when the broker cannot be reached.

Connection errors MAY be retryable subject to the caller policy.

---

# Authentication Errors

Raised when broker authentication fails.

Authentication errors SHALL NOT expose credentials and SHALL be non-retryable
without new credentials.

---

# Publish Errors

Raised when a publish fails.

Conditions

- Broker rejects the message
- Publish to a target queue attempted without authorization

Publish errors SHALL be handled per delivery semantic to avoid duplicates.

---

# Consume Errors

Raised when consumption fails.

Conditions

- Consume rejected
- Visibility extension failure

Unacknowledged messages SHALL return to the queue rather than be lost.

---

# Semantic Errors

Raised when a requested delivery semantic cannot be honored.

Semantic mismatches SHALL be reported through `effective_semantic` rather than
raised as fatal errors, unless the caller requires the exact semantic.

---

# Timeout Errors

Raised when a bound is exceeded.

Conditions

- Consume duration exceeded
- Visibility timeout with no acknowledgment

Timeout errors SHALL carry the breached bound.

---

# Governance Errors

Raised when an operation would violate governance.

Conditions

- Publishing to a target queue when `allow_target_publish` is disabled
- Rate ceiling exceeded

Governance errors SHALL be non-retryable without operator intervention.

---

# Adapter Errors

Raised when an underlying broker adapter fails unexpectedly.

Adapter errors SHALL be normalized so that consumers remain unaware of the
implementation.

---

# Internal Errors

Raised for unexpected conditions within the Queue Client.

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

broker_id:

queue:
```

`category` SHALL be one of the canonical categories.

`retryable` SHALL indicate whether the operation MAY be attempted again.

Errors SHALL NOT contain sensitive message contents.

---

# Outcome Mapping

| Outcome | Category | Retryable |
|---------|----------|-----------|
| connect_failed | Connection | Policy dependent |
| auth_failed | Authentication | No |
| publish_rejected | Publish | Semantic dependent |
| target_publish_blocked | Governance | No |
| consume_failed | Consume | Policy dependent |
| semantic_downgraded | Semantic | Reported, not fatal |
| timed_out | Timeout | No |
| rejected | Governance | No |
| invalid_request | Validation | No |
| adapter_failure | Adapter | Policy dependent |
| unexpected | Internal | No |

---

# Message-Preservation Principle

An unacknowledged message SHALL NOT be lost due to a client failure.

Unacknowledged messages SHALL return to the queue for redelivery, bounded by the
redelivery limit, after which they SHALL be dead-lettered.

---

# Evidence

Errors SHOULD be captured as evidence conforming to the
[Evidence schema](../../../schemas/evidence.md), including the category, broker,
and queue, and SHALL exclude sensitive contents.

---

# Related Documents

- [Interface](interface.md)
- [Execution](execution.md)
- [Error Handling Model](../../core/error-handling.md)
- [Authentication](../authentication/README.md)
