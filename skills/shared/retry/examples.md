# Retry Examples

**File:** `skills/shared/retry/examples.md`

**Version:** 1.0.0

---

# Purpose

This document provides illustrative examples of how the Retry Shared Skill is
used by shared packages, domain skills, workflows, and agents within the Robust
PenTest Platform (RPP).

Examples demonstrate interface usage, policy selection, execution patterns,
evidence generation, and error handling.

All examples are conceptual and implementation independent.

---

# Example 1 — HTTP Client Retrying a Transient Timeout

## Scenario

The [HTTP Client](../http-client/README.md) delegates retry decisions to the
Retry Shared Skill after a connect timeout.

### Invocation

```yaml
metadata:
  request_id: req-001
  assessment_id: asm-001
  task_id: task-001
  skill_id: network.http

operation: send_http_request
idempotent: true
policy_id: default-network-retry
options:
  deadline: '2026-07-25T10:00:30Z'
```

### Result

```yaml
outcome: succeeded
attempts:
  - attempt_number: 1
    outcome_category: Timeout
    delay_before: 0ms
  - attempt_number: 2
    outcome_category: Success
    delay_before: 220ms
retry_count: 1
```

The HTTP Client never implements a retry loop of its own.

---

# Example 2 — Non-Retryable Validation Failure

## Scenario

A request fails validation before transmission.

### Result

```yaml
outcome: aborted
attempts:
  - attempt_number: 1
    outcome_category: Validation
error:
  category: Validation
  retryable: false
```

The Retry Shared Skill does not retry validation failures.

---

# Example 3 — Exhausted Attempt Budget

## Scenario

A DNS resolution repeatedly times out.

```text
Attempt 1 → Timeout
Attempt 2 → Timeout
Attempt 3 → Timeout
Attempt 4 → Timeout
```

### Result

```yaml
outcome: exhausted
retry_count: 3
error:
  category: Timeout
  retryable: true
  terminal_outcome: exhausted
```

The last operation error is propagated with retry metadata.

---

# Example 4 — Respecting Retry-After

## Scenario

A target responds with `429 Too Many Requests` and a `Retry-After` header.

### Attempt Outcome

```yaml
success: false
retry_signal:
  retry_after: 2s
  status_code: 429
```

### Behavior

```text
Computed backoff: 400ms
Retry-After signal: 2s
Applied delay: 2s
```

When the policy sets `respect_retry_after`, the transport signal overrides the
computed backoff, bounded by `global_max_delay`.

---

# Example 5 — Deadline Awareness

## Scenario

An execution deadline is near.

```text
Deadline: 10:00:30Z
Now: 10:00:29Z
Next attempt expected duration: 3s
```

### Result

```yaml
outcome: deadline_exceeded
```

The Retry Shared Skill does not schedule an attempt that would exceed the
deadline.

---

# Example 6 — Idempotency Guard

## Scenario

A non-idempotent `POST` operation fails with a connection reset.

### Invocation

```yaml
operation: submit_form
idempotent: false
policy_id: default-network-retry
```

### Behavior

Because the policy sets `idempotent_only` and the operation is not idempotent,
the operation SHALL NOT be retried.

```yaml
outcome: aborted
error:
  category: Idempotency
```

---

# Example 7 — Abort Category

## Scenario

An operation returns an `Authorization` failure listed in `abort_on`.

### Result

```yaml
outcome: aborted
attempts:
  - attempt_number: 1
    outcome_category: Authorization
error:
  category: Authorization
```

The retry loop terminates immediately.

---

# Example 8 — Batch Execution

## Scenario

A Content Discovery skill probes multiple endpoints with shared retry semantics.

```text
/login
/admin
/health
```

Each operation is retried independently while sharing a common elapsed-time
budget and honoring per-operation isolation.

---

# Example 9 — Evidence Generation

Evidence generated during a retried operation

```yaml
evidence:
  policy: default-network-retry
  attempts:
    - attempt_number: 1
      outcome_category: Timeout
      delay_before: 0ms
    - attempt_number: 2
      outcome_category: Success
      delay_before: 220ms
  terminal_outcome: succeeded
```

Evidence conforms to the canonical
[Evidence schema](../../../schemas/evidence.md).

---

# Example 10 — TLS Client Handshake Retry

## Scenario

The [TLS Client](../tls-client/README.md) retries a handshake after a transient
network reset.

```text
Attempt 1 → Connection reset
Attempt 2 → Handshake completed
```

The TLS Client supplies the handshake as the operation and delegates the retry
decision.

---

# Best Practices

Consumers SHOULD

- Reference shared retry policies
- Declare idempotency explicitly
- Propagate execution deadlines
- Combine retry with the Rate Limiter
- Preserve retry evidence

---

# Anti-Patterns

Consumers SHOULD NOT

- Implement manual retry loops
- Retry without a bounded budget
- Retry non-idempotent operations silently
- Hardcode backoff values
- Retry validation or authorization failures

---

# Validation Checklist

A compliant consumer

✓ Uses the Retry Interface

✓ References a canonical Retry Policy

✓ Declares idempotency

✓ Preserves evidence

✓ Propagates deadlines

✓ Remains operation independent

---

# Success Criteria

A compliant consumer applies retries exclusively through the Retry Shared Skill,
enabling bounded, deterministic, observable recovery from transient failures
throughout the Robust PenTest Platform.
