# Retry Capabilities

**File:** `skills/shared/retry/capabilities.md`

**Version:** 1.0.0

---

# Purpose

This document defines the canonical capabilities provided by the Retry Shared
Skill.

These capabilities represent reusable retry behaviors that MAY be consumed by
any shared package or domain skill within the Robust PenTest Platform (RPP).

Capabilities describe *what* the Retry Shared Skill can do, not *how* it is
implemented.

---

# Relationship

```
Consumer

↓

Capability

↓

Retry Shared Skill

↓

Caller-Provided Operation
```

Consumers SHALL depend on capabilities rather than on retry implementations.

---

# Design Principles

Capabilities SHALL be

- Canonical
- Composable
- Deterministic
- Reusable
- Observable
- Versioned
- Implementation Independent

---

# Capability Categories

```
Execution

↓

Classification

↓

Backoff

↓

Budgeting

↓

Evidence

↓

Observability
```

---

# Execution

## resilience.retry.execute

### Purpose

Execute a caller-provided operation under a resolved retry policy, retrying
transient failures until success or a terminal condition.

### Inputs

- Operation reference
- Retry policy reference
- Idempotency declaration
- Execution deadline

### Outputs

- Final result or terminal error
- Attempt history
- Evidence

---

## resilience.retry.execute_batch

### Purpose

Apply retry semantics across a batch of operations while preserving per-operation
isolation and a shared time budget.

### Inputs

- Operation collection
- Retry policy reference
- Concurrency constraints

### Outputs

- Per-operation results
- Aggregate metrics

---

# Classification

## resilience.retry.classify

### Purpose

Determine whether a given outcome is retryable under a policy without executing
a retry.

### Inputs

- Outcome or canonical error
- Retry policy reference
- Idempotency declaration

### Outputs

- Retryable decision
- Reason

---

# Backoff

## resilience.retry.compute_backoff

### Purpose

Compute the delay before the next attempt for a given attempt number.

### Inputs

- Retry policy reference
- Attempt number
- Optional transport retry signal

### Outputs

- Delay duration
- Applied strategy
- Applied jitter

---

# Budgeting

## resilience.retry.evaluate_budget

### Purpose

Evaluate whether another attempt is permitted under the active attempt budget,
elapsed-time budget, and execution deadline.

### Inputs

- Retry policy reference
- Attempt context
- Execution deadline

### Outputs

- Permitted decision
- Limiting bound

---

# Evidence

## resilience.retry.evidence.capture

### Purpose

Capture evidence describing the retry lifecycle.

Evidence MAY include

- Policy reference
- Attempt history
- Delays
- Terminal decision

Evidence SHALL conform to the canonical
[Evidence schema](../../../schemas/evidence.md).

---

# Observability

## resilience.retry.metrics.collect

### Purpose

Collect retry execution metrics.

Metrics MAY include

- Attempt count
- Total delay
- Elapsed time
- Terminal outcome

---

## resilience.retry.events.publish

### Purpose

Publish retry lifecycle events.

Events MAY include

- RetryStarted
- AttemptFailed
- RetryScheduled
- RetrySucceeded
- RetryExhausted
- RetryAborted

---

# Capability Dependencies

| Capability | Dependency |
|------------|------------|
| resilience.retry.execute | Retry Policy, Execution Model |
| resilience.retry.classify | Error Handling |
| resilience.retry.compute_backoff | Retry Policy |
| resilience.retry.evidence.capture | Evidence Shared Skill |
| resilience.retry.metrics.collect | Logging / Metrics |

The Retry Shared Skill SHALL expose these capabilities regardless of
implementation.

---

# Capability Composition

Capabilities MAY be composed.

Example

```
resilience.retry.execute

↓

resilience.retry.classify

↓

resilience.retry.evaluate_budget

↓

resilience.retry.compute_backoff

↓

resilience.retry.evidence.capture
```

---

# Capability Constraints

Capabilities SHALL

- Enforce bounded attempts
- Preserve execution context
- Produce structured outputs
- Record evidence
- Generate structured errors

Capabilities SHALL NOT

- Execute input or output themselves
- Detect vulnerabilities
- Produce findings
- Modify assessment scope

---

# Versioning

Capabilities SHALL use semantic versioning.

Capability identifiers SHOULD remain stable across versions.

---

# Validation Rules

A compliant capability SHALL

- Have a unique identifier
- Define inputs
- Define outputs
- Specify dependencies
- Produce structured responses
- Support observability

---

# Quality Requirements

Retry capabilities SHALL

✓ Be reusable

✓ Be deterministic

✓ Be implementation independent

✓ Support composition

✓ Integrate with canonical schemas

✓ Preserve evidence

✓ Support structured errors

✓ Remain bounded

---

# Future Extensions

Future versions MAY include

- resilience.retry.circuit_breaker
- resilience.retry.adaptive_backoff
- resilience.retry.budget.share

Backward compatibility SHOULD be maintained.

---

# Success Criteria

A compliant Retry Shared Skill exposes a standardized set of reusable retry
capabilities that provide recovery services to consumers without exposing retry
implementation details.

These capabilities form the resilience foundation for network, discovery, and
active-testing workflows throughout the Robust PenTest Platform.
