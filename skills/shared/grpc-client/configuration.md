# gRPC Client Configuration

**File:** `skills/shared/grpc-client/configuration.md`

**Version:** 1.0.0

---

# Purpose

This document defines the configuration model for the gRPC Client Shared Skill.

Configuration determines message and call bounds, governance policy defaults,
and observability.

Configuration is declarative and implementation independent, consistent with the
[Configuration Model](../../core/configuration-model.md).

---

# Configuration Sources

The gRPC Client Shared Skill SHALL resolve configuration from the following
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

A higher-precedence source MAY tighten bounds but SHALL NOT exceed Rules of
Engagement ceilings.

---

# Configuration Structure

```yaml
grpc_client:

  bounds:

  governance:

  observability:
```

---

# Bounds

```yaml
bounds:
  max_message_bytes:
  max_messages:
  default_deadline:
  connect_timeout:
```

`max_message_bytes` and `max_messages` SHALL bound message size and count.

`default_deadline` SHALL bound calls that do not specify one.

`connect_timeout` SHALL bound channel establishment.

---

# Governance

```yaml
governance:
  default_rate_limit_policy_id:
  default_retry_policy_id:
  default_proxy_id:
  retryable_status_codes:
```

`default_rate_limit_policy_id`, `default_retry_policy_id`, and
`default_proxy_id` SHALL reference canonical policies applied when an invocation
omits its own.

`retryable_status_codes` SHALL enumerate gRPC status codes eligible for retry,
such as `UNAVAILABLE` and `DEADLINE_EXCEEDED`, subject to idempotency.

---

# Observability

```yaml
observability:
  emit_events:
  capture_evidence:
  metrics_enabled:
```

`emit_events` SHALL enable publication of lifecycle events.

`capture_evidence` SHALL enable gRPC evidence capture conforming to the
[Evidence schema](../../../schemas/evidence.md).

`metrics_enabled` SHALL enable metric exposure.

---

# Validation Rules

A valid configuration SHALL satisfy

- `max_message_bytes`, `max_messages` are greater than or equal to `1`
- `default_deadline` and `connect_timeout` are positive durations
- Referenced default policies exist and are valid
- `retryable_status_codes` contains valid gRPC status codes
- No secret material appears in configuration

---

# Example Configuration

```yaml
grpc_client:

  bounds:
    max_message_bytes: 4MB
    max_messages: 1000
    default_deadline: 30s
    connect_timeout: 5s

  governance:
    default_rate_limit_policy_id: ratelimitpolicy-default-http
    default_retry_policy_id: retrypolicy-default-network
    default_proxy_id: proxy-corporate-egress
    retryable_status_codes:
      - UNAVAILABLE
      - DEADLINE_EXCEEDED

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
