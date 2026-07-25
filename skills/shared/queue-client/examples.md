# Queue Client Examples

**File:** `skills/shared/queue-client/examples.md`

**Version:** 1.0.0

---

# Purpose

This document provides realistic, implementation-independent examples of the
Queue Client Shared Skill in use.

Examples demonstrate publishing, consumption, acknowledgment, poison handling,
semantic reporting, evidence, and expected outputs.

All examples are illustrative and contain no implementation code.

---

# Example 1 — Publish With At-Least-Once

A workflow publishes a coordination message.

## Invocation

```yaml
metadata:
  request_id: req-10001
  assessment_id: asmt-42
  task_id: task-coordination
  skill_id: workflow-runtime
broker_id: platform-bus
queue: task-events
credential_ref: cred-bus
kind: publish
requested_semantic: at_least_once
messages:
  - payload_ref: staging://queue/task-complete
```

## Result

```yaml
outcome: completed
effective_semantic: at_least_once
published: 1
```

The message is published with the reported effective semantic.

---

# Example 2 — Consume With Visibility Timeout

A consumer processes messages with a visibility window.

## Invocation

```yaml
kind: consume
consume_options:
  max_messages: 10
  visibility_timeout: 30s
  max_duration: 60s
```

## Result

```yaml
outcome: completed
consumed:
  - message_ref: artifact://queue/req-10002-m1
    acknowledged: true
  - message_ref: artifact://queue/req-10002-m2
    acknowledged: true
```

Processed messages are acknowledged within the visibility window.

---

# Example 3 — Semantic Downgrade Reported

Exactly-once is requested but the broker provides at-least-once.

## Invocation

```yaml
requested_semantic: exactly_once
```

## Result

```yaml
outcome: completed
effective_semantic: at_least_once
```

The effective semantic is reported honestly rather than silently degraded;
consumers process idempotently.

---

# Example 4 — Poison Message Dead-Lettered

A message repeatedly fails processing.

## Configuration

```yaml
poison:
  max_redeliveries: 5
  dead_letter: true
```

## Result

```yaml
outcome: completed
dead_lettered: 1
```

The poison message is dead-lettered after the redelivery bound rather than
looping.

---

# Example 5 — Target Publish Blocked

Publishing to a target-owned queue is attempted while disabled.

## Configuration

```yaml
publish:
  allow_target_publish: false
```

## Result

```yaml
outcome: rejected
error:
  category: Governance
  code: target_publish_blocked
  retryable: false
```

Publishing to target queues is intrusive and requires authorization.

---

# Example 6 — Unacknowledged Message Preserved

A client failure occurs before acknowledgment.

## Behavior

```
consume message → processing fails → no ack → visibility timeout → redelivered
```

The message returns to the queue rather than being lost, bounded by the
redelivery limit.

---

# Example 7 — Evidence Record

A single operation produces the following evidence.

```yaml
evidence:
  type: queue-operation
  broker_id: platform-bus
  queue: task-events
  kind: publish
  effective_semantic: at_least_once
  message_count: 1
  duration_ms: 22
  decided_at: 2026-07-25T17:45:00Z
```

The evidence conforms to the canonical
[Evidence schema](../../../schemas/evidence.md), excludes sensitive contents, and
supports auditing.

---

# Related Documents

- [Interface](interface.md)
- [Configuration](configuration.md)
- [Execution](execution.md)
- [Error Model](error-model.md)
- [Workflow Runtime](../workflow-runtime/README.md)
