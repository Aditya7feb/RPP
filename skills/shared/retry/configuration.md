# Retry Configuration

**File:** `skills/shared/retry/configuration.md`

**Version:** 1.0.0

---

# Purpose

This document defines the configuration parameters supported by the Retry Shared
Skill.

It extends the platform-wide configuration model defined in
[the configuration model](../../core/configuration-model.md).

Only retry-specific configuration is defined here. The declarative shape of a
policy is defined by the
[Retry Policy schema](../../../schemas/retry-policy.md); this document defines
how policies are registered, resolved, and defaulted at runtime.

---

# Relationship

```
Platform Configuration

↓

Retry Configuration

↓

Retry Policy Registry

↓

Resolved Policy

↓

Retry Execution
```

---

# Design Principles

Retry configuration SHALL be

- Explicit
- Predictable
- Immutable during a single execution
- Bounded
- Validated
- Transport Independent

---

# Configuration Categories

```
Policy Registry

↓

Default Policy

↓

Resolution

↓

Global Bounds

↓

Observability
```

---

# Policy Registry

## policies

A named collection of retry policies available to consumers.

Type

```
Map<String, RetryPolicy>
```

Each entry SHALL conform to the
[Retry Policy schema](../../../schemas/retry-policy.md).

---

## policy_source

Where policies are loaded from.

Supported values

```
inline

configuration_store

profile
```

Default

```
configuration_store
```

---

# Default Policy

## default_policy_id

The policy applied when a consumer does not reference a specific policy.

Type

```
Reference
```

Default

```
default-network-retry
```

A default policy SHALL always be resolvable.

---

## fail_closed

Behavior when a referenced policy cannot be resolved.

Type

```
Boolean
```

Default

```
true
```

When `true`, an unresolved policy SHALL raise a configuration error rather than
silently disabling retries.

---

# Resolution

## allow_inline_override

Whether callers MAY supply an inline policy override.

Type

```
Boolean
```

Default

```
true
```

---

## override_precedence

Order in which policy sources are resolved.

Default

```
inline_override

named_policy

default_policy
```

An override SHALL never raise the attempt budget above the global maximum.

---

# Global Bounds

Global bounds protect the platform from unbounded or aggressive retries and
SHALL take precedence over any policy value.

## global_max_attempts

Absolute upper bound on attempts for any operation.

Type

```
Integer
```

Default

```
10
```

Minimum

```
1
```

---

## global_max_elapsed_time

Absolute upper bound on total retry time for any operation.

Type

```
Duration
```

Default

```
120s
```

---

## global_max_delay

Absolute upper bound on any single computed delay.

Type

```
Duration
```

Default

```
30s
```

---

## enforce_deadline

Whether execution deadlines are always honored.

Type

```
Boolean
```

Default

```
true
```

---

# Idempotency

## default_idempotent

Default idempotency assumption when a caller does not declare one.

Type

```
Boolean
```

Default

```
false
```

Defaulting to `false` ensures non-idempotent operations are not retried
accidentally.

---

# Observability

## capture_evidence

Record per-attempt evidence.

Type

```
Boolean
```

Default

```
true
```

---

## emit_events

Publish retry lifecycle events.

Type

```
Boolean
```

Default

```
true
```

---

## capture_metrics

Collect retry metrics.

Type

```
Boolean
```

Default

```
true
```

---

# Validation Rules

A valid retry configuration SHALL satisfy

- `default_policy_id` resolves to a registered policy
- Every registered policy conforms to the Retry Policy schema
- No policy `max_attempts` exceeds `global_max_attempts`
- No policy `max_delay` exceeds `global_max_delay`
- No policy `max_elapsed_time` exceeds `global_max_elapsed_time`
- `global_max_attempts` is greater than or equal to `1`

Configuration that violates a global bound SHALL be rejected at load time.

---

# Example

```yaml
policy_source: configuration_store
default_policy_id: default-network-retry
fail_closed: true
allow_inline_override: true
global_max_attempts: 10
global_max_elapsed_time: 120s
global_max_delay: 30s
enforce_deadline: true
default_idempotent: false
capture_evidence: true
emit_events: true
capture_metrics: true
policies:
  default-network-retry:
    policy_id: retrypolicy-default-network
    schema_version: 1.0.0
    name: default-network-retry
    description: Default transient network retry policy.
    max_attempts: 4
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
```

---

# Extension Points

Future versions MAY introduce

- Per-consumer policy namespaces
- Environment-specific global bounds
- Circuit-breaker configuration
- Adaptive bound tuning

Backward compatibility SHOULD be maintained.

---

# Success Criteria

A compliant Retry configuration provides explicit, validated, and bounded
control over retry behavior.

It guarantees that every resolved policy remains within platform-wide safety
bounds while allowing consumers to select purpose-specific policies.
