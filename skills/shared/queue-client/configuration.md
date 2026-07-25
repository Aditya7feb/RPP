# Queue Client Configuration

**File:** `skills/shared/queue-client/configuration.md`

**Version:** 1.0.0

---

# Purpose

This document defines the configuration model for the Queue Client Shared Skill.

Configuration determines brokers, message and consumption bounds, redelivery and
dead-lettering behavior, publish gating, governance policy defaults, and
observability.

Configuration is declarative and implementation independent, consistent with the
[Configuration Model](../../core/configuration-model.md).

---

# Configuration Sources

The Queue Client Shared Skill SHALL resolve configuration from the following
sources, in increasing order of precedence.

```
Platform Defaults

↓

Assessment Configuration

↓

Consumer Configuration

↓

Invocation Override
```

A higher-precedence source MAY tighten bounds but SHALL NOT remove redelivery
bounds or enable unauthorized publishing.

---

# Configuration Structure

```yaml
queue_client:

  brokers:

  publish:

  consume:

  poison:

  governance:

  observability:
```

---

# Brokers

```yaml
brokers:
  - broker_id:
    kind:
    endpoints:
```

`brokers` SHALL enumerate the configured brokers.

`kind` SHALL identify the broker kind without exposing implementation detail.

`endpoints` SHALL describe reachable endpoints, without secrets.

---

# Publish

```yaml
publish:
  max_message_bytes:
  max_publish_rate:
  allow_target_publish:
```

`max_message_bytes` SHALL bound message size.

`max_publish_rate` SHALL bound publish rate beyond rate-limit policy.

`allow_target_publish` SHALL be a boolean gating publishing to target-owned
queues and SHALL default to `false`.

---

# Consume

```yaml
consume:
  max_messages:
  visibility_timeout:
  max_duration:
```

`max_messages` SHALL bound messages per consume operation.

`visibility_timeout` SHALL define the invisibility window during processing.

`max_duration` SHALL bound total consumption time.

---

# Poison

```yaml
poison:
  max_redeliveries:
  dead_letter:
```

`max_redeliveries` SHALL bound redelivery attempts.

`dead_letter` SHALL declare whether poison messages are dead-lettered where
supported.

---

# Governance

```yaml
governance:
  default_rate_limit_policy_id:
  default_retry_policy_id:
```

`default_rate_limit_policy_id` and `default_retry_policy_id` SHALL reference
canonical policies applied when an invocation omits its own.

---

# Observability

```yaml
observability:
  emit_events:
  capture_evidence:
  metrics_enabled:
```

`emit_events` SHALL enable publication of lifecycle events.

`capture_evidence` SHALL enable operation evidence capture conforming to the
[Evidence schema](../../../schemas/evidence.md).

`metrics_enabled` SHALL enable metric exposure.

---

# Validation Rules

A valid configuration SHALL satisfy

- Every broker defines a `broker_id`, `kind`, and `endpoints`
- Broker identifiers are unique
- `max_message_bytes`, `max_messages` are greater than or equal to `1`
- `visibility_timeout` and `max_duration` are positive durations
- `max_redeliveries` is greater than or equal to `1`
- `allow_target_publish` defaults to `false`
- Referenced default policies exist and are valid
- No secret material appears in configuration

---

# Example Configuration

```yaml
queue_client:

  brokers:
    - broker_id: platform-bus
      kind: managed-broker
      endpoints:
        - bus.internal.example.com:5671

  publish:
    max_message_bytes: 256KB
    max_publish_rate: 100/s
    allow_target_publish: false

  consume:
    max_messages: 100
    visibility_timeout: 30s
    max_duration: 60s

  poison:
    max_redeliveries: 5
    dead_letter: true

  governance:
    default_rate_limit_policy_id: ratelimitpolicy-default-http
    default_retry_policy_id: retrypolicy-default-network

  observability:
    emit_events: true
    capture_evidence: true
    metrics_enabled: true
```

---

# Related Documents

- [Interface](interface.md)
- [Execution](execution.md)
- [Evidence Schema](../../../schemas/evidence.md)
- [Configuration Model](../../core/configuration-model.md)
