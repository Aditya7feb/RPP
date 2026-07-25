# Rate Limiter Examples

**File:** `skills/shared/rate-limiter/examples.md`

**Version:** 1.0.0

---

# Purpose

This document provides realistic, implementation-independent examples of the
Rate Limiter Shared Skill in use.

Examples demonstrate consumers, policies, scope keying, overflow handling,
adaptive throttling, evidence, and expected outputs.

All examples are illustrative and contain no implementation code.

---

# Example 1 — Per-Host HTTP Pacing

A discovery skill enumerates endpoints on a single host and paces its requests
through the Rate Limiter.

## Policy

```yaml
policy_id: ratelimitpolicy-default-http
scope: per_host
rate:
  algorithm: token_bucket
  permits: 10
  interval: 1s
  burst: 20
on_limit:
  action: wait
  max_wait: 5s
```

## Invocation

```yaml
metadata:
  request_id: req-1001
  assessment_id: asmt-42
  task_id: task-endpoint-enum
  skill_id: endpoint-enumeration
operation: <send-http-request-callback>
priority: 5
policy_id: ratelimitpolicy-default-http
host: app.example.com
```

## Outcome

```yaml
outcome: executed
wait_time: 40ms
effective_rate: 10/s
queue_depth: 0
```

The operation waited briefly for a token, then executed within the configured
rate.

---

# Example 2 — Reject Under Load

An API skill uses a `reject` policy so that it can immediately fail fast rather
than queue when the target is saturated.

## Policy

```yaml
policy_id: ratelimitpolicy-fastfail
scope: per_target
rate:
  algorithm: sliding_window
  permits: 5
  interval: 1s
on_limit:
  action: reject
```

## Outcome When Exhausted

```yaml
outcome: rejected
error:
  category: RateLimited
  code: rate_permit_unavailable
  retryable: true
  earliest_retry: 2026-07-25T10:15:03Z
```

The caller receives a canonical `RateLimited` error and may retry after
`earliest_retry`.

---

# Example 3 — Adaptive Throttling On 429

An authenticated REST skill enables adaptive control. When the target responds
with `429`, the Rate Limiter reduces the effective rate and honors
`Retry-After`.

## Policy

```yaml
policy_id: ratelimitpolicy-adaptive-api
scope: per_credential
rate:
  algorithm: token_bucket
  permits: 20
  interval: 1s
  burst: 20
adaptive:
  enabled: true
  respect_retry_after: true
  throttle_status_codes:
    - 429
  recovery: exponential
```

## Operation Outcome Reporting A Throttle

```yaml
success: false
error:
  category: Transport
  code: remote_throttled
throttle_signal:
  retry_after: 2s
  status_code: 429
```

## Rate Limiter Response

```yaml
outcome: executed
effective_rate: 10/s        # reduced from 20/s
suppressed_until: 2026-07-25T10:20:05Z
```

The effective rate is halved and outbound operations for the credential scope
are suppressed for two seconds, then recover exponentially.

---

# Example 4 — Rules of Engagement Ceiling

A consumer supplies an aggressive inline override. The governance ceiling clamps
it.

## Governance Ceiling

```yaml
policy_id: ratelimitpolicy-roe-ceiling
scope: per_host
rate:
  algorithm: token_bucket
  permits: 15
  interval: 1s
  burst: 15
roe_binding:
  enforced: true
  source: rules-of-engagement
```

## Inline Override

```yaml
rate:
  algorithm: token_bucket
  permits: 200
  interval: 1s
  burst: 400
```

## Result

```yaml
outcome: executed
effective_rate: 15/s        # clamped to ceiling
evidence:
  clamped: true
  ceiling_policy_id: ratelimitpolicy-roe-ceiling
```

The override is clamped to the ceiling and the clamp is recorded as evidence.

---

# Example 5 — Concurrency Limiting

A TLS analysis skill bounds simultaneous handshakes to protect a fragile target.

## Policy

```yaml
policy_id: ratelimitpolicy-tls-concurrency
scope: per_host
rate:
  algorithm: token_bucket
  permits: 50
  interval: 1s
  burst: 50
concurrency:
  max_in_flight: 4
on_limit:
  action: wait
  max_wait: 10s
```

## Behavior

At most four handshakes proceed simultaneously per host. Additional operations
wait for a slot, bounded by `max_wait`.

---

# Example 6 — Combined With Retry

An HTTP operation is both paced and retried. Each retry acquires a fresh permit.

## Flow

```
Attempt 1 → acquire permit → execute → transient timeout

↓ Retry decides to retry

Attempt 2 → acquire permit → execute → success
```

## Result

```yaml
rate_limiter:
  permits_granted: 2
retry:
  attempts: 2
  outcome: succeeded
```

Retry traffic remains within the configured rate because every attempt consumes
its own permit.

---

# Example 7 — Evidence Record

A single decision produces the following evidence.

```yaml
evidence:
  type: rate-limit-decision
  policy_id: ratelimitpolicy-default-http
  scope_key: per_host:app.example.com
  decision: executed
  wait_time: 40ms
  effective_rate: 10/s
  queue_depth: 0
  decided_at: 2026-07-25T10:15:00Z
```

The evidence conforms to the canonical
[Evidence schema](../../../schemas/evidence.md) and supports auditing.

---

# Related Documents

- [Interface](interface.md)
- [Configuration](configuration.md)
- [Execution](execution.md)
- [Error Model](error-model.md)
- [Rate Limit Policy Schema](../../../schemas/rate-limit-policy.md)
- [Retry](../retry/README.md)
