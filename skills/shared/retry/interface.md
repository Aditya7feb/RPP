# Retry Interface

**File:** `skills/shared/retry/interface.md`

**Version:** 1.0.0

---

# Purpose

The Retry Interface defines the canonical contract through which platform
components apply retry semantics to recoverable operations.

The interface standardizes retry invocation, policy resolution, outcome
classification, and result propagation while remaining independent of any
operation implementation.

All consumers SHALL apply retries exclusively through this interface.

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

Retry Interface

↓

Retry Shared Skill

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

Retry Policy

↓

Execution Options

↓

Execution Context

↓

Retry Result

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

idempotent:
```

`operation` SHALL be a caller-provided execution callback that performs a single
attempt and returns a normalized outcome.

`idempotent` SHALL be a boolean declaring whether the operation is safe to
repeat. When a policy sets `idempotent_only`, retries SHALL occur only when
`idempotent` is `true`.

---

# Retry Policy

Every invocation SHALL reference a policy.

```yaml
policy_id:
```

`policy_id` SHALL reference a [Retry Policy](../../../schemas/retry-policy.md).

An invocation MAY supply an inline policy override that conforms to the Retry
Policy schema. Overrides SHALL be validated before use.

---

# Execution Options

The caller MAY specify

```yaml
deadline:

max_attempts_override:

capture_evidence:

emit_events:
```

`deadline` SHALL be an absolute time after which no further attempts are
scheduled.

`max_attempts_override` MAY lower, but SHALL NOT raise, the policy attempt
budget.

These options influence execution without changing the interface.

---

# Execution Context

The Retry Shared Skill SHALL receive read-only context.

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

retry_signal:
```

`success` SHALL be a boolean.

`error` SHALL conform to the canonical error structure when `success` is
`false`.

`retry_signal` MAY carry a transport-provided `Retry-After` duration or a
retryable status code.

---

# Retry Result

Every invocation SHALL return a normalized result.

```yaml
outcome:

result:

error:

attempts:

total_delay:

elapsed_time:

evidence:
```

`outcome` SHALL be one of

```
succeeded

exhausted

aborted

deadline_exceeded
```

`attempts` SHALL be an ordered array of attempt records.

Transport-specific objects SHALL NOT be exposed.

---

## Attempt Record

Each attempt record SHALL include

```yaml
attempt_number:

outcome_category:

delay_before:

started_at:

completed_at:
```

The complete attempt history SHOULD be preserved.

---

# Evidence

The interface SHALL expose structured evidence.

Evidence MAY include

- Policy reference
- Attempt history
- Delays
- Terminal decision

Evidence SHALL conform to the canonical
[Evidence schema](../../../schemas/evidence.md).

---

# Metrics

Execution metrics MAY include

```yaml
attempt_count:

retry_count:

total_delay:

elapsed_time:
```

Metrics SHOULD support observability.

---

# Error Contract

Errors SHALL conform to
[the platform error handling model](../../core/error-handling.md) and to
[the Retry error model](error-model.md).

When retries are exhausted or aborted, the interface SHALL propagate the last
canonical error from the operation.

---

# Compatibility

The interface SHALL remain stable across operation types.

Example

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
- Retry Policy
- Execution Context
- Retry Result
- Error Handling
- Evidence

---

# Quality Requirements

The Retry Interface SHALL

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

- Streaming attempt notifications
- Circuit-breaker state exposure
- Shared budget handles
- Adaptive policy negotiation

Backward compatibility SHOULD be maintained.

---

# Success Criteria

A compliant Retry Interface provides a stable, implementation-independent
contract through which all platform components apply retry semantics.

It enables interchangeable operations to benefit from consistent, bounded, and
observable recovery across the Robust PenTest Platform.
