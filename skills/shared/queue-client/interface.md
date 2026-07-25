# Queue Client Interface

**File:** `skills/shared/queue-client/interface.md`

**Version:** 1.0.0

---

# Purpose

The Queue Client Interface defines the canonical contract through which platform
components publish and consume messages.

The interface standardizes publish and consume requests, delivery semantics,
acknowledgment, and result propagation while remaining independent of any broker
implementation.

All consumers SHALL perform message-queue access exclusively through this
interface.

---

# Design Principles

The interface SHALL be

- Stable
- Strongly Defined
- Broker Independent
- Versioned
- Observable
- Backward Compatible
- Semantics-Explicit

---

# Relationship

```
Master Agent

↓

Domain Skill

↓

Queue Client Interface

↓

Queue Client Shared Skill

↓

Broker Adapter
```

The interface SHALL NOT expose or depend on adapter internals.

---

# Interface Overview

```
Metadata

↓

Broker Target

↓

Operation

↓

Delivery Semantics

↓

Governance References

↓

Execution Context

↓

Operation Result

↓

Evidence

↓

Errors
```

---

# Metadata

Every invocation SHALL include

```yaml
request_id:

assessment_id:

task_id:

skill_id:

timestamp:
```

Metadata enables tracing and auditing.

---

# Broker Target

Every invocation SHALL define

```yaml
broker_id:

queue:

credential_ref:
```

`broker_id` SHALL identify the configured broker.

`queue` SHALL identify the queue, topic, or subject.

`credential_ref` SHALL reference a credential resolved by the
[Authentication](../authentication/README.md) package.

The interface SHALL NOT accept inline secrets.

---

# Operation

Every invocation SHALL define

```yaml
kind:

messages:

consume_options:
```

`kind` SHALL be one of `publish` or `consume`.

For `publish`, `messages` SHALL be a bounded sequence, each with a payload
reference and optional attributes.

For `consume`, `consume_options` SHALL declare a maximum count, visibility
timeout, and total duration.

Publishing to target-owned queues SHALL be authorized as intrusive.

The interface SHALL treat message payloads opaquely.

---

# Delivery Semantics

Every invocation SHALL define

```yaml
requested_semantic:
```

`requested_semantic` SHALL be one of `at_most_once`, `at_least_once`, or
`exactly_once`.

The result SHALL report the `effective_semantic` actually provided.

---

# Governance References

Every invocation MAY reference

```yaml
rate_limit_policy_id:

retry_policy_id:
```

Referenced policies SHALL conform to their canonical schemas. Absent references
SHALL inherit configured defaults.

---

# Execution Context

The Queue Client Shared Skill SHALL receive read-only context.

```yaml
execution_id:

parent_span:

variables:
```

The interface SHALL treat context as read-only.

---

# Operation Result

Every invocation SHALL return a normalized result.

```yaml
outcome:

effective_semantic:

published:

consumed:

dead_lettered:

error:

evidence:
```

`outcome` SHALL be one of

```
completed

partial

rejected

timed_out
```

For `consume`, `consumed` SHALL summarize messages, referencing payloads as
artifacts, with per-message acknowledgment state.

Adapter-specific broker objects SHALL NOT be exposed.

---

# Evidence

The interface SHALL expose structured evidence.

Evidence MAY include

- Broker and queue identifiers
- Operation kind and effective semantic
- Message counts and sizes
- Acknowledgment and dead-letter outcomes

Evidence SHALL conform to the canonical
[Evidence schema](../../../schemas/evidence.md) and SHALL NOT contain sensitive
message contents.

---

# Error Contract

Errors SHALL conform to
[the platform error handling model](../../core/error-handling.md) and to
[the Queue Client error model](error-model.md).

A requested semantic the broker cannot provide SHALL be reported through
`effective_semantic`, not silently degraded.

---

# Compatibility

The interface SHALL remain stable across brokers and consumers.

Consumers SHALL require no modification when brokers change.

---

# Versioning

The interface SHALL follow semantic versioning.

Minor versions MAY introduce optional fields.

Major versions SHALL indicate breaking changes.

---

# Validation Rules

A compliant invocation SHALL define

- Metadata
- Broker Target
- Operation
- Requested Delivery Semantic
- Execution Context
- Operation Result
- Error Handling
- Evidence

---

# Quality Requirements

The Queue Client Interface SHALL

✓ Remain broker independent

✓ Report delivery semantics honestly

✓ Bound message size and volume

✓ Support structured errors

✓ Preserve evidence

✓ Protect message contents

✓ Remain backward compatible

---

# Future Extensions

Future versions MAY include

- Streaming consumption descriptors
- Ordered partition consumption
- Transactional publish batches

Backward compatibility SHOULD be maintained.

---

# Success Criteria

A compliant Queue Client Interface provides a stable, implementation-independent
contract through which all platform components publish and consume messages with
explicit semantics across the Robust PenTest Platform.
