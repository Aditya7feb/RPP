# Rate Limiter Interface

**File:** `skills/shared/rate-limiter/interface.md`

**Version:** 1.0.0

---

# Purpose

The Rate Limiter Interface defines the canonical contract through which platform
components pace outbound operations.

The interface standardizes permit acquisition, policy resolution, overflow
handling, and result propagation while remaining independent of any operation
implementation.

All consumers SHALL pace outbound operations exclusively through this interface.

---

# Design Principles

The interface SHALL be

- Stable
- Strongly Defined
- Operation Independent
- Versioned
- Observable
- Backward Compatible
- Deterministic

---

# Relationship

```
Master Agent

↓

Workflow

↓

Shared Package or Domain Skill

↓

Rate Limiter Interface

↓

Rate Limiter Shared Skill

↓

Caller-Provided Operation
```

The operation is supplied by the caller as an execution callback. The interface
SHALL NOT expose or depend on operation internals.

---

# Interface Overview

```
Metadata

↓

Operation Reference

↓

Rate Limit Policy

↓

Scope Inputs

↓

Execution Options

↓

Execution Context

↓

Rate Limit Result

↓

Evidence

↓

Metrics

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

# Operation Reference

Every invocation SHALL define

```yaml
operation:

priority:
```

`operation` SHALL be a caller-provided execution callback that performs a single
outbound operation and returns a normalized outcome.

`priority` SHALL be an integer describing scheduling priority when overflow
handling queues or sheds operations. Higher values indicate higher priority.

---

# Rate Limit Policy

Every invocation SHALL reference a policy.

```yaml
policy_id:
```

`policy_id` SHALL reference a
[Rate Limit Policy](../../../schemas/rate-limit-policy.md).

An invocation MAY supply an inline policy override that conforms to the Rate
Limit Policy schema. Overrides SHALL be validated before use and SHALL NOT
exceed a Rules of Engagement ceiling.

---

# Scope Inputs

Every invocation SHALL provide the inputs required to compute the scope key.

```yaml
host:

target_id:

credential_id:
```

Only the fields required by the policy `scope` SHALL be consulted. Unused fields
MAY be omitted.

---

# Execution Options

The caller MAY specify

```yaml
deadline:

capture_evidence:

emit_events:
```

`deadline` SHALL be an absolute time after which the invocation SHALL fail
rather than continue to wait for a permit.

These options influence execution without changing the interface.

---

# Execution Context

The Rate Limiter Shared Skill SHALL receive read-only context.

```yaml
execution_id:

parent_span:

variables:
```

The interface SHALL treat context as read-only.

---

# Attempt Outcome

The caller-provided operation SHALL return a normalized outcome.

```yaml
success:

result:

error:

throttle_signal:
```

`success` SHALL be a boolean.

`error` SHALL conform to the canonical error structure when `success` is
`false`.

`throttle_signal` MAY carry a transport-provided `Retry-After` duration or a
throttling status code used by adaptive control.

---

# Rate Limit Result

Every invocation SHALL return a normalized result.

```yaml
outcome:

result:

error:

wait_time:

effective_rate:

queue_depth:

evidence:
```

`outcome` SHALL be one of

```
executed

rejected

shed

deadline_exceeded
```

Transport-specific objects SHALL NOT be exposed.

---

## Decision Record

Each decision record SHALL include

```yaml
scope_key:

decision:

wait_time:

effective_rate:

decided_at:
```

The complete decision history SHOULD be preserved.

---

# Evidence

The interface SHALL expose structured evidence.

Evidence MAY include

- Policy reference
- Scope key
- Decision outcome
- Wait duration
- Effective rate

Evidence SHALL conform to the canonical
[Evidence schema](../../../schemas/evidence.md).

---

# Metrics

Execution metrics MAY include

```yaml
granted:

deferred:

rejected:

shed:

average_wait:
```

Metrics SHOULD support observability.

---

# Error Contract

Errors SHALL conform to
[the platform error handling model](../../core/error-handling.md) and to
[the Rate Limiter error model](error-model.md).

When an operation is rejected, shed, or exceeds its deadline, the interface
SHALL propagate a canonical rate-limit error.

---

# Compatibility

The interface SHALL remain stable across operation types.

```
HTTP Request Operation

↓

Same Interface

↓

DNS Query Operation

↓

Same Interface

↓

TLS Handshake Operation

↓

Same Interface
```

Consumers SHALL require no modification when operation types change.

---

# Versioning

The interface SHALL follow semantic versioning.

Minor versions MAY introduce optional fields.

Major versions SHALL indicate breaking changes.

---

# Validation Rules

A compliant invocation SHALL define

- Metadata
- Operation Reference
- Rate Limit Policy
- Scope Inputs required by the policy
- Execution Context
- Rate Limit Result
- Error Handling
- Evidence

---

# Quality Requirements

The Rate Limiter Interface SHALL

✓ Remain operation independent

✓ Produce normalized results

✓ Support structured errors

✓ Preserve execution context

✓ Preserve evidence

✓ Support observability

✓ Remain backward compatible

---

# Future Extensions

Future versions MAY include

- Reservation handles for multi-step operations
- Cost-weighted permit requests
- Distributed permit negotiation
- Streaming queue-position notifications

Backward compatibility SHOULD be maintained.

---

# Success Criteria

A compliant Rate Limiter Interface provides a stable, implementation-independent
contract through which all platform components pace outbound operations.

It enables interchangeable operations to benefit from consistent, bounded, and
observable pacing across the Robust PenTest Platform.
