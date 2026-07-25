# Retry Execution Model

**File:** `skills/shared/retry/execution.md`

**Version:** 1.0.0

---

# Purpose

The Retry Execution Model defines how retry semantics are applied to a
recoverable operation from invocation through terminal outcome within the Robust
PenTest Platform (RPP).

It specifies the runtime behavior of the Retry Shared Skill while remaining
independent of any operation implementation.

Execution SHALL follow the platform-wide execution model defined in
[the execution model](../../core/execution-model.md).

---

# Design Principles

Retry execution SHALL be

- Deterministic given the same policy and outcomes
- Bounded
- Observable
- Recoverable
- Deadline aware
- Transport Independent
- Evidence Driven

---

# Relationship

```
Caller

↓

Retry Interface

↓

Retry Execution Engine

├── Policy Resolver
├── Retryable Classifier
├── Backoff Calculator
├── Budget Manager
├── Deadline Guard

↓

Caller-Provided Operation
```

---

# Execution Overview

```
Receive Invocation

↓

Resolve Policy

↓

Validate Inputs

↓

Initialize Budget

↓

Execute Attempt

↓

Evaluate Outcome

↓

Retryable and Within Bounds?

├── No → Finalize

└── Yes → Compute Backoff

          ↓

          Wait

          ↓

          Next Attempt

↓

Capture Evidence

↓

Publish Events

↓

Return Result
```

---

# Stage 1 — Receive Invocation

The Retry Shared Skill SHALL receive

- Request metadata
- Operation reference
- Idempotency declaration
- Policy reference or inline override
- Execution options
- Execution context

The invocation SHALL conform to the [Retry Interface](interface.md).

---

# Stage 2 — Resolve Policy

The applicable [Retry Policy](../../../schemas/retry-policy.md) SHALL be resolved
according to [the configuration model](../../core/configuration-model.md) and
the resolution precedence defined in [configuration.md](configuration.md).

The resolved policy SHALL be clamped to the configured global bounds and SHALL
remain immutable for the duration of the invocation.

---

# Stage 3 — Validate Inputs

The engine SHALL validate

- Operation reference presence
- Policy validity
- Idempotency compatibility
- Deadline sanity

Invalid invocations SHALL fail before the first attempt.

---

# Stage 4 — Initialize Budget

The engine SHALL initialize

- Attempt counter
- Elapsed-time tracker
- Deadline guard

The first attempt SHALL always be permitted when inputs are valid.

---

# Stage 5 — Execute Attempt

The engine SHALL invoke the caller-provided operation exactly once per attempt.

The operation SHALL return a normalized outcome. The engine SHALL NOT inspect
operation internals.

---

# Stage 6 — Evaluate Outcome

The engine SHALL classify the outcome using the resolved policy.

A successful outcome SHALL finalize execution as `succeeded`.

A failed outcome SHALL be classified as retryable or non-retryable, considering

- Canonical error category
- Idempotency
- Non-retryable categories
- Abort categories
- Retryable status codes

An abort category SHALL finalize execution as `aborted`.

A non-retryable outcome SHALL finalize execution with the propagated error.

---

# Stage 7 — Evaluate Budget and Deadline

Before scheduling a retry the engine SHALL confirm

- The attempt budget is not exhausted
- The elapsed-time budget is not exceeded
- The next attempt would complete before any active deadline

If any bound is violated, execution SHALL finalize as `exhausted` or
`deadline_exceeded`.

---

# Stage 8 — Compute Backoff

When a retry is permitted the engine SHALL compute the delay using the policy
backoff strategy and jitter.

When the policy honors retry signals and the outcome carried a `Retry-After`
value, that value SHALL take precedence, bounded by `global_max_delay`.

The computed delay SHALL never exceed `backoff.max_delay`.

---

# Stage 9 — Wait

The engine SHALL wait for the computed delay before the next attempt.

Waiting SHALL remain cancellable by the platform.

---

# Stage 10 — Capture Evidence

Each attempt SHOULD record

- Attempt number
- Outcome category
- Computed delay
- Elapsed time

Evidence SHALL conform to the canonical
[Evidence schema](../../../schemas/evidence.md).

---

# Stage 11 — Publish Events

The engine SHOULD publish

- RetryStarted
- AttemptStarted
- AttemptFailed
- RetryScheduled
- RetrySucceeded
- RetryExhausted
- RetryAborted

Events SHALL update the Execution State.

---

# Stage 12 — Return Result

The engine SHALL return a normalized result containing

- Terminal outcome
- Result or terminal error
- Attempt history
- Metrics
- Evidence references

---

# Concurrency

The Retry Shared Skill MAY drive multiple independent retry loops concurrently.

Concurrency SHALL preserve per-operation isolation. Jitter SHOULD be applied to
reduce synchronized retries across concurrent callers.

---

# Cancellation

Execution MAY be cancelled by

- Master Agent
- Workflow
- Policy Engine
- Operator

Cancellation SHALL

- Stop any pending wait
- Preserve collected evidence
- Release resources
- Return a structured terminal status

---

# Deadline Handling

When `deadline_aware` is enabled the engine SHALL NOT schedule an attempt whose
expected completion would exceed the caller deadline.

Deadline enforcement SHALL take precedence over the attempt budget.

---

# Error Handling

Errors SHALL conform to
[the platform error handling model](../../core/error-handling.md) and
[the Retry error model](error-model.md).

The terminal error SHALL be the last canonical error returned by the operation.

---

# Metrics

The engine SHOULD record

```yaml
attempt_count:

retry_count:

total_delay:

elapsed_time:

terminal_outcome:
```

---

# Resource Cleanup

Execution SHALL release

- Timers
- Wait handles
- Temporary attempt state

Cleanup SHALL occur even after failure or cancellation.

---

# Audit Requirements

Execution SHOULD record

- Request identifier
- Resolved policy identifier
- Attempt history
- Terminal outcome
- Policy decisions

Sensitive values in operation context SHALL be redacted.

---

# Validation Rules

A compliant execution SHALL

- Resolve and clamp the policy
- Validate inputs
- Enforce budgets and deadlines
- Classify outcomes deterministically
- Preserve evidence
- Produce structured errors

---

# Quality Requirements

The execution model SHALL

✓ Remain operation independent

✓ Enforce bounded attempts

✓ Support deadlines

✓ Support cancellation

✓ Support observability

✓ Produce normalized results

✓ Preserve evidence

✓ Support concurrent execution

---

# Future Extensions

Future versions MAY include

- Circuit-breaker integration
- Adaptive backoff informed by observed latency
- Shared budgets across a request batch
- Retry storm detection

Backward compatibility SHOULD be maintained.

---

# Success Criteria

A compliant Retry Execution Model provides a bounded, deterministic, and
observable mechanism for recovering from transient failures.

It enables every shared package and domain skill to apply consistent retry
behavior while abstracting operation complexity, preserving evidence, and
integrating with the platform execution lifecycle.
