# Rate Limit Policy Schema

**File:** `schemas/rate-limit-policy.md`

**Version:** 1.0.0

---

# Purpose

The Rate Limit Policy Schema defines the canonical, implementation-independent
representation of an outbound rate limit within the Robust PenTest Platform
(RPP).

A rate limit policy describes how frequently a platform component MAY perform
outbound operations against a target scope: the permitted request rate, the
burst allowance, the concurrency ceiling, and the behavior when the limit is
reached. It is consumed by the
[Rate Limiter](../skills/shared/rate-limiter/README.md) shared package and
referenced by every package that performs outbound operations, including the
[HTTP Client](../skills/shared/http-client/README.md),
[TLS Client](../skills/shared/tls-client/README.md), and
[DNS Client](../skills/shared/dns-client/README.md).

A Rate Limit Policy object represents configuration and intent only. It SHALL
NOT contain runtime state, security interpretation, or findings. Runtime state
belongs to the [Rate Limit Decision](#relationships) records produced during
execution.

---

# Design Principles

A Rate Limit Policy SHALL be

- Declarative
- Deterministic given the same inputs
- Transport independent
- Reusable across packages
- Bounded
- Safe to reference
- Free of embedded secrets

---

# Identity

Every Rate Limit Policy SHALL contain

```yaml
policy_id:

schema_version:
```

`policy_id` SHALL be unique within an assessment or configuration namespace.

`schema_version` SHALL be `1.0.0`.

---

# Classification

Every Rate Limit Policy SHALL contain

```yaml
name:

description:
```

`name` SHALL be a stable, human-readable identifier such as
`default-outbound-http`.

`description` SHALL summarize the intended use of the policy.

---

# Scope

Every Rate Limit Policy SHALL contain

```yaml
scope:
```

`scope` SHALL be one of

```
global

per_host

per_target

per_assessment

per_credential
```

`scope` determines the key against which the limit is enforced. `global`
applies a single limit across all outbound operations. `per_host` maintains an
independent limit for each resolved host. `per_target` keys on the assessment
target. `per_assessment` keys on the assessment identifier. `per_credential`
keys on the authenticating principal.

---

# Rate

Every Rate Limit Policy SHALL contain

```yaml
rate:
```

`rate` SHALL contain

```yaml
algorithm:

permits:

interval:
```

`algorithm` SHALL be one of

```
token_bucket

leaky_bucket

fixed_window

sliding_window
```

`permits` SHALL be an integer greater than or equal to `1` describing the
number of operations allowed per `interval`.

`interval` SHALL be a positive duration over which `permits` are replenished or
counted.

A `rate` MAY contain

```yaml
burst:
```

`burst` SHALL be an integer greater than or equal to `permits` describing the
maximum instantaneous allowance. `burst` is meaningful only for the
`token_bucket` and `leaky_bucket` algorithms.

---

# Concurrency

A Rate Limit Policy MAY contain

```yaml
concurrency:
```

`concurrency` SHALL contain

```yaml
max_in_flight:
```

`max_in_flight` SHALL be an integer greater than or equal to `1` bounding the
number of simultaneously outstanding operations within the resolved `scope`.

Concurrency limiting is independent of rate limiting. A policy MAY define
either, both, or neither beyond the required `rate`.

---

# Overflow Behavior

Every Rate Limit Policy SHALL contain

```yaml
on_limit:
```

`on_limit` SHALL contain

```yaml
action:
```

`action` SHALL be one of

```
wait

reject

shed
```

`wait` blocks the caller until a permit becomes available. `reject` returns a
canonical rate-limit error immediately. `shed` discards the lowest-priority
queued operations to preserve throughput for higher-priority work.

An `on_limit` MAY contain

```yaml
max_wait:

max_queue_depth:
```

`max_wait` SHALL be a duration bounding how long a caller MAY block when
`action` is `wait`. When exceeded, the operation SHALL fail with a canonical
rate-limit error.

`max_queue_depth` SHALL be an integer bounding the number of operations that MAY
be queued awaiting a permit.

---

# Adaptive Response

A Rate Limit Policy MAY contain

```yaml
adaptive:
```

`adaptive` SHALL contain

```yaml
enabled:

respect_retry_after:

throttle_status_codes:

recovery:
```

`enabled` SHALL be a boolean. When `true`, the Rate Limiter MAY reduce the
effective rate in response to throttling signals observed by the caller.

`respect_retry_after` SHALL be a boolean indicating whether a transport-provided
`Retry-After` signal temporarily suppresses further operations within the
resolved `scope`.

`throttle_status_codes` SHALL be an array of protocol status codes, such as
`429` and `503`, that indicate remote throttling. Interpreting these codes as
security weaknesses SHALL remain the responsibility of domain skills, not this
schema.

`recovery` SHALL describe how the effective rate returns toward the configured
rate after throttling subsides and SHALL be one of

```
immediate

linear

exponential
```

---

# Rules of Engagement Binding

A Rate Limit Policy MAY contain

```yaml
roe_binding:
```

`roe_binding` SHALL contain

```yaml
enforced:

source:
```

`enforced` SHALL be a boolean. When `true`, the policy values SHALL NOT be
exceeded by any override and SHALL be treated as a Rules of Engagement ceiling.

`source` SHALL identify the authority that established the ceiling, such as
`rules-of-engagement` or `operator`.

---

# Observability

A Rate Limit Policy MAY contain

```yaml
emit_events:

capture_evidence:
```

`emit_events` SHALL be a boolean indicating whether rate-limit lifecycle events
are published to the Execution State.

`capture_evidence` SHALL be a boolean indicating whether limiting decisions
record evidence conforming to [evidence.md](evidence.md).

---

# Extensions

A Rate Limit Policy MAY contain

```yaml
extensions:
```

`extensions` SHALL contain namespaced metadata.

`extensions` SHALL NOT contain secrets.

---

# Required Fields

A valid Rate Limit Policy object SHALL contain

- `policy_id`
- `schema_version`
- `name`
- `description`
- `scope`
- `rate.algorithm`
- `rate.permits`
- `rate.interval`
- `on_limit.action`

---

# Validation Rules

A valid Rate Limit Policy object SHALL satisfy

- `scope` is one of the allowed scopes
- `rate.algorithm` is one of the allowed algorithms
- `rate.permits` is an integer greater than or equal to `1`
- `rate.interval` is a positive duration
- `rate.burst`, when present, is greater than or equal to `rate.permits`
- `rate.burst` is present only when `algorithm` is `token_bucket` or
  `leaky_bucket`
- `concurrency.max_in_flight`, when present, is greater than or equal to `1`
- `on_limit.action` is one of the allowed actions
- `on_limit.max_wait` is present when `action` is `wait`
- `on_limit.max_queue_depth`, when present, is greater than or equal to `1`
- `adaptive.recovery`, when present, is one of the allowed recovery modes
- When `roe_binding.enforced` is `true`, no override raises any bound
- No secret material appears in `extensions`

---

# Relationships

```
Rate Limit Policy

├── referenced by HTTP Client configuration
├── referenced by TLS Client configuration
├── referenced by DNS Client configuration
├── consumed by Rate Limiter shared package
├── constrained by Rules of Engagement
└── produces Rate Limit Decision records (runtime)
```

A Rate Limit Policy is referenced by a package configuration through a policy
reference. During execution the Rate Limiter produces per-decision records that
reference the originating `policy_id` and are preserved as
[evidence](evidence.md). Throttle categories reference the canonical error
categories defined in
[the platform error handling model](../skills/core/error-handling.md).

---

# Example Object

```yaml
policy_id: ratelimitpolicy-default-http
schema_version: 1.0.0
name: default-outbound-http
description: >
  Default per-host outbound limit for HTTP operations using a token bucket
  with a bounded burst and adaptive throttling on remote 429 responses.
scope: per_host
rate:
  algorithm: token_bucket
  permits: 10
  interval: 1s
  burst: 20
concurrency:
  max_in_flight: 8
on_limit:
  action: wait
  max_wait: 5s
  max_queue_depth: 256
adaptive:
  enabled: true
  respect_retry_after: true
  throttle_status_codes:
    - 429
    - 503
  recovery: exponential
roe_binding:
  enforced: true
  source: rules-of-engagement
emit_events: true
capture_evidence: true
```

---

# Versioning Notes

The schema SHALL follow semantic versioning.

Minor versions MAY introduce optional fields such as additional algorithms or
recovery modes.

Major versions SHALL indicate breaking changes, such as renaming or removing a
required field.

Consumers SHOULD ignore unknown optional fields to preserve forward
compatibility.
