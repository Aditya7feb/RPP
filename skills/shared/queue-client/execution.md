# Queue Client Execution Model

**File:** `skills/shared/queue-client/execution.md`

**Version:** 1.0.0

---

# Purpose

This document defines the execution model for the Queue Client Shared Skill.

The execution model describes how the shared skill publishes and consumes
messages, manages acknowledgment and visibility, and handles poison messages.

The model is deterministic in bounds given the same configuration and inputs,
acknowledging that broker delivery is influenced by external state.

---

# Execution Overview

```
Receive Operation Request

↓

Resolve Configuration

↓

Acquire Rate Permit

↓

Connect And Authenticate

↓

Publish Or Consume

↓

Manage Acknowledgment / Visibility

↓

Handle Poison Messages

↓

Emit Evidence and Events

↓

Return Result
```

---

# Stage 1 — Configuration Resolution

The Queue Client SHALL resolve brokers, bounds, poison behavior, and governance
using the precedence defined in [configuration.md](configuration.md).

Redelivery bounds SHALL always be enforced.

---

# Stage 2 — Rate Permit

The Queue Client SHALL acquire a permit from the
[Rate Limiter](../rate-limiter/README.md) per publish and per consume batch.

---

# Stage 3 — Connect And Authenticate

The Queue Client SHALL connect to the broker and authenticate through the
[Authentication](../authentication/README.md) package.

---

# Stage 4 — Publish

For `publish`, the Queue Client SHALL send messages bounded by
`max_message_bytes` and `max_publish_rate`, with the declared delivery semantic.

Publishing to target-owned queues SHALL proceed only when `allow_target_publish`
is enabled.

The effective delivery semantic SHALL be reported.

---

# Stage 5 — Consume

For `consume`, the Queue Client SHALL receive messages bounded by `max_messages`
and `max_duration`, each with a visibility timeout during which it is invisible
to other consumers.

Consumed payloads SHALL be stored by reference.

---

# Stage 6 — Acknowledgment And Visibility

A processed message SHALL be acknowledged.

An unprocessed message SHALL be negatively acknowledged or allowed to time out,
returning to the queue for redelivery.

Visibility SHALL be extended only within configured bounds.

---

# Stage 7 — Poison Handling

The Queue Client SHALL track redelivery counts.

A message exceeding `max_redeliveries` SHALL be dead-lettered where supported, or
reported as a poison message, rather than redelivered indefinitely.

---

# Stage 8 — Evidence And Events

The Queue Client SHOULD emit operation evidence and lifecycle events according to
configuration. Evidence SHALL exclude sensitive contents.

---

# Delivery Semantics

The Queue Client SHALL report the `effective_semantic` provided by the broker.

Where the broker cannot provide the requested semantic, the strongest available
semantic SHALL be reported rather than silently degrading.

Consumers relying on `at_least_once` SHALL process idempotently.

---

# Retry Behavior

Transient broker failures MAY be retried through the [Retry](../retry/README.md)
shared skill, each retry acquiring a fresh permit.

Publishing SHALL be retried only when idempotent or under `exactly_once`
semantics to avoid duplicates.

---

# Determinism

Given identical configuration and inputs, the Queue Client SHALL enforce identical
bounds and produce identical outcome classifications for the same observed broker
behavior.

---

# Failure Handling

Execution failures SHALL be classified according to
[error-model.md](error-model.md).

An unacknowledged message SHALL return to the queue rather than be lost, subject
to the delivery semantic.

---

# Execution Outputs

The execution model SHALL produce

- Publish confirmations
- Consumed messages by reference with acknowledgment state
- Dead-letter outcomes
- Operation metrics
- Evidence references

Outputs SHALL remain implementation independent.

---

# Related Documents

- [Interface](interface.md)
- [Configuration](configuration.md)
- [Error Model](error-model.md)
- [Authentication](../authentication/README.md)
- [Execution Model](../../core/execution-model.md)
