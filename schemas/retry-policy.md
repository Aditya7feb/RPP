# Retry Policy Schema

**File:** `schemas/retry-policy.md`

**Version:** 1.0.0

---

# Purpose

The Retry Policy Schema defines the canonical, implementation-independent
representation of a retry policy within the Robust PenTest Platform (RPP).

A retry policy describes how transient failures SHOULD be handled: which
outcomes are retryable, how many attempts are permitted, how long to wait
between attempts, and when to stop. It is consumed by the
[Retry](../skills/shared/retry/README.md) shared package and referenced by every
package that performs recoverable operations, including the
[HTTP Client](../skills/shared/http-client/README.md),
[TLS Client](../skills/shared/tls-client/README.md), and
[DNS Client](../skills/shared/dns-client/README.md).

A Retry Policy object represents configuration and intent only. It SHALL NOT
contain runtime state, security interpretation, or findings. Runtime state
belongs to the [Retry Attempt](#relationships) records produced during
execution.

---

# Design Principles

A Retry Policy SHALL be

- Declarative
- Deterministic given the same inputs
- Transport independent
- Reusable across packages
- Bounded
- Safe to reference
- Free of embedded secrets

---

# Identity

Every Retry Policy SHALL contain

```yaml
policy_id:

schema_version:
```

`policy_id` SHALL be unique within an assessment or configuration namespace.

`schema_version` SHALL be `1.0.0`.

---

# Classification

Every Retry Policy SHALL contain

```yaml
name:

description:
```

`name` SHALL be a stable, human-readable identifier such as
`default-network-retry`.

`description` SHALL summarize the intended use of the policy.

---

# Attempt Budget

Every Retry Policy SHALL contain

```yaml
max_attempts:
```

`max_attempts` SHALL be an integer greater than or equal to `1`.

`max_attempts` counts the initial attempt plus all retries. A value of `1`
means no retries.

A Retry Policy MAY contain

```yaml
max_elapsed_time:
```

`max_elapsed_time` SHALL be a duration bounding the total time across all
attempts. When present, retries SHALL stop once the elapsed time would exceed
this bound, even if `max_attempts` has not been reached.

---

# Backoff Strategy

Every Retry Policy SHALL contain

```yaml
backoff:
```

`backoff` SHALL contain

```yaml
strategy:

initial_delay:

max_delay:
```

`strategy` SHALL be one of

```
none

fixed

linear

exponential

exponential_jitter
```

`initial_delay` SHALL be a non-negative duration applied before the first retry.

`max_delay` SHALL be a duration bounding any single computed delay.

A `backoff` MAY contain

```yaml
multiplier:

jitter:
```

`multiplier` SHALL be a number greater than or equal to `1.0` and is REQUIRED
when `strategy` is `linear`, `exponential`, or `exponential_jitter`.

`jitter` SHALL describe randomization applied to each delay and is REQUIRED when
`strategy` is `exponential_jitter`.

`jitter` SHALL contain

```yaml
type:

factor:
```

`type` SHALL be one of

```
none

full

equal

decorrelated
```

`factor` SHALL be a number from `0.0` through `1.0` describing jitter
proportion when `type` is `equal`.

---

# Retryable Classification

Every Retry Policy SHALL contain

```yaml
retryable:
```

`retryable` SHALL contain

```yaml
error_categories:

idempotent_only:
```

`error_categories` SHALL be an array of canonical error categories, as defined
in [the platform error handling model](../skills/core/error-handling.md), that
are eligible for retry. Examples include `Timeout`, `Connection`, and
`Transport`.

`idempotent_only` SHALL be a boolean. When `true`, retries SHALL be permitted
only for operations declared idempotent by the caller.

A Retry Policy MAY contain

```yaml
non_retryable:
```

`non_retryable` SHALL be an array of canonical error categories that SHALL never
be retried, overriding `error_categories` on conflict.

---

# Response Signals

A Retry Policy MAY contain

```yaml
respect_retry_after:

retry_status_codes:
```

`respect_retry_after` SHALL be a boolean indicating whether a transport-provided
`Retry-After` signal overrides the computed backoff delay.

`retry_status_codes` SHALL be an array of protocol status codes, such as `429`,
`502`, `503`, and `504`, that mark an otherwise successful response as
retryable. Interpreting these codes as security weaknesses SHALL remain the
responsibility of domain skills, not this schema.

---

# Deadline Awareness

A Retry Policy MAY contain

```yaml
deadline_aware:
```

`deadline_aware` SHALL be a boolean. When `true`, the Retry package SHALL NOT
schedule an attempt whose expected completion would exceed the caller's
execution deadline.

---

# Abort Conditions

A Retry Policy MAY contain

```yaml
abort_on:
```

`abort_on` SHALL be an array of canonical error categories that SHALL
immediately terminate the retry loop and propagate the error without further
attempts.

---

# Observability

A Retry Policy MAY contain

```yaml
emit_events:

capture_evidence:
```

`emit_events` SHALL be a boolean indicating whether retry lifecycle events are
published to the Execution State.

`capture_evidence` SHALL be a boolean indicating whether each attempt records
evidence conforming to [evidence.md](evidence.md).

---

# Extensions

A Retry Policy MAY contain

```yaml
extensions:
```

`extensions` SHALL contain namespaced metadata.

`extensions` SHALL NOT contain secrets.

---

# Required Fields

A valid Retry Policy object SHALL contain

- `policy_id`
- `schema_version`
- `name`
- `description`
- `max_attempts`
- `backoff.strategy`
- `backoff.initial_delay`
- `backoff.max_delay`
- `retryable.error_categories`
- `retryable.idempotent_only`

---

# Validation Rules

A valid Retry Policy object SHALL satisfy

- `max_attempts` is an integer greater than or equal to `1`
- `backoff.strategy` is one of the allowed strategies
- `backoff.multiplier` is present and greater than or equal to `1.0` when
  `strategy` is `linear`, `exponential`, or `exponential_jitter`
- `backoff.jitter` is present when `strategy` is `exponential_jitter`
- `backoff.initial_delay` is less than or equal to `backoff.max_delay`
- `jitter.factor`, when present, is between `0.0` and `1.0`
- `error_categories` and `non_retryable` do not overlap
- No secret material appears in `extensions`

---

# Relationships

```
Retry Policy

├── referenced by HTTP Client configuration
├── referenced by TLS Client configuration
├── referenced by DNS Client configuration
├── consumed by Retry shared package
└── produces Retry Attempt records (runtime)
```

A Retry Policy is referenced by a package configuration through a policy
reference. During execution the Retry package produces per-attempt records that
reference the originating `policy_id` and are preserved as
[evidence](evidence.md). Retryable and non-retryable categories reference the
canonical categories defined in
[the platform error handling model](../skills/core/error-handling.md).

---

# Example Object

```yaml
policy_id: retrypolicy-default-network
schema_version: 1.0.0
name: default-network-retry
description: >
  Default policy for transient network failures using exponential backoff
  with full jitter and a bounded attempt budget.
max_attempts: 4
max_elapsed_time: 30s
backoff:
  strategy: exponential_jitter
  initial_delay: 200ms
  max_delay: 5s
  multiplier: 2.0
  jitter:
    type: full
    factor: 1.0
retryable:
  error_categories:
    - Timeout
    - Connection
    - Transport
  idempotent_only: true
non_retryable:
  - Validation
  - Authentication
respect_retry_after: true
retry_status_codes:
  - 429
  - 503
  - 504
deadline_aware: true
abort_on:
  - Authorization
emit_events: true
capture_evidence: true
```

---

# Versioning Notes

The schema SHALL follow semantic versioning.

Minor versions MAY introduce optional fields such as additional backoff
strategies or jitter types.

Major versions SHALL indicate breaking changes, such as renaming or removing a
required field.

Consumers SHOULD ignore unknown optional fields to preserve forward
compatibility.

---

# Extension Points

Future versions MAY introduce

- Circuit-breaker coupling
- Adaptive backoff informed by observed latency
- Per-category attempt budgets
- Budget sharing across a request batch
- Server-timing correlation

Backward compatibility SHOULD be maintained through `extensions`.

---

# Related Schemas

- [Evidence](evidence.md)
- [HTTP Transaction](http-transaction.md)
- [HTTP Timing](http-timing.md)
- [Execution State](execution-state.md)

---

# Success Criteria

A compliant Retry Policy object provides a complete, declarative description of
how transient failures are retried.

It enables every shared package to apply consistent, bounded, observable retry
behavior without embedding retry logic of its own.
