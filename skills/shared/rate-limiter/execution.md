# Rate Limiter Execution Model

**File:** `skills/shared/rate-limiter/execution.md`

**Version:** 1.0.0

---

# Purpose

This document defines the execution model for the Rate Limiter Shared Skill.

The execution model describes how the shared skill processes a pacing request
from policy resolution through permit allocation, execution, and result
propagation.

The model is deterministic given the same policy, scope state, and inputs.

---

# Execution Overview

```
Receive Invocation

↓

Resolve Policy

↓

Validate Against Governance Ceiling

↓

Compute Scope Key

↓

Request Permit

↓

Handle Overflow (if required)

↓

Acquire Concurrency Slot

↓

Execute Operation

↓

Observe Throttle Signals

↓

Release Slot

↓

Emit Evidence and Events

↓

Return Result
```

---

# Stage 1 — Policy Resolution

The Rate Limiter SHALL resolve the effective
[Rate Limit Policy](../../../schemas/rate-limit-policy.md) using the precedence
defined in [configuration.md](configuration.md).

An inline override SHALL be validated before use.

---

# Stage 2 — Governance Validation

The resolved policy SHALL be validated against the Rules of Engagement ceiling.

If the resolved policy exceeds the ceiling and the ceiling is enforced, the
Rate Limiter SHALL clamp the effective bounds to the ceiling.

The clamped bounds SHALL be recorded in evidence.

---

# Stage 3 — Scope Keying

The Rate Limiter SHALL compute the scope key from the policy `scope` and the
supplied scope inputs.

Missing inputs required by the scope SHALL result in a configuration error.

---

# Stage 4 — Permit Request

The Rate Limiter SHALL request a permit from the algorithm state associated with
the scope key.

- For `token_bucket` and `leaky_bucket`, a permit consumes one token, bounded by
  `burst`.
- For `fixed_window` and `sliding_window`, a permit increments the window count,
  bounded by `permits` per `interval`.

If a permit is immediately available, execution proceeds to Stage 6.

---

# Stage 5 — Overflow Handling

When no permit is available, the Rate Limiter SHALL apply `on_limit.action`.

```
action = wait

↓

Enqueue (bounded by max_queue_depth)

↓

Await Permit or max_wait or deadline

↓

Permit → Proceed | Timeout → deadline_exceeded error
```

```
action = reject

↓

Return rate-limit error immediately
```

```
action = shed

↓

Drop lowest-priority queued operation

↓

Enqueue current operation if capacity remains
```

Queue depth SHALL never exceed `max_queue_depth`.

---

# Stage 6 — Concurrency Slot

Where `concurrency.max_in_flight` is defined, the Rate Limiter SHALL acquire a
slot before execution.

If no slot is available, the operation SHALL be treated according to the same
overflow behavior as permit exhaustion.

---

# Stage 7 — Operation Execution

The Rate Limiter SHALL invoke the caller-provided operation callback exactly
once per granted permit.

The Rate Limiter SHALL NOT inspect or modify the operation implementation.

---

# Stage 8 — Throttle Observation

When `adaptive.enabled` is `true`, the Rate Limiter SHALL inspect the operation
outcome for a `throttle_signal`.

Upon a throttle signal, the Rate Limiter SHALL

- Reduce the effective rate for the scope
- Suppress operations for any `Retry-After` duration when
  `respect_retry_after` is `true`
- Schedule recovery according to the policy `recovery` mode

---

# Stage 9 — Slot Release

The concurrency slot SHALL be released on completion, including on error.

Slot release SHALL NOT be skipped under any terminal condition.

---

# Stage 10 — Evidence and Events

The Rate Limiter SHOULD emit per-decision evidence and lifecycle events
according to the resolved policy and configuration.

---

# Determinism

Given identical policy, scope state, and inputs, the Rate Limiter SHALL produce
identical decisions.

Randomization SHALL be confined to jittered recovery scheduling where a policy
requests it and SHALL be bounded by the configured recovery mode.

---

# Concurrency and Fairness

The Rate Limiter SHALL serve queued operations fairly within a priority band.

Higher-priority operations SHALL be served before lower-priority operations.

Within a priority band, operations SHALL be served in arrival order.

---

# Deadlines

Where a `deadline` is supplied, no permit acquisition or queue wait SHALL extend
beyond it.

An operation that cannot acquire a permit before its deadline SHALL fail with a
`deadline_exceeded` outcome.

---

# Interaction With Retry

When a consumer combines rate limiting with [Retry](../retry/README.md), each
retry attempt SHALL acquire its own permit.

This ensures retry traffic remains within the configured rate and does not
amplify outbound load.

---

# Failure Handling

Execution failures SHALL be classified according to
[error-model.md](error-model.md).

A permit consumed by a failed operation SHALL NOT be automatically refunded
unless the operation never began, in which case the permit MAY be returned to
the scope.

---

# Execution Outputs

The execution model SHALL produce

- A normalized rate-limit result
- A decision history
- Rate metrics
- Evidence references

Outputs SHALL remain implementation independent.

---

# Related Documents

- [Interface](interface.md)
- [Configuration](configuration.md)
- [Error Model](error-model.md)
- [Rate Limit Policy Schema](../../../schemas/rate-limit-policy.md)
- [Execution Model](../../core/execution-model.md)
