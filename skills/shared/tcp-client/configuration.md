# TCP Client Configuration

**File:** `skills/shared/tcp-client/configuration.md`

**Version:** 1.0.0

---

# Purpose

This document defines the configuration model for the TCP Client Shared Skill.

Configuration determines default timeouts, byte bounds, governance policy
defaults, and observability.

Configuration is declarative and implementation independent, consistent with the
[Configuration Model](../../core/configuration-model.md).

---

# Configuration Sources

The TCP Client Shared Skill SHALL resolve configuration from the following
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

A higher-precedence source MAY tighten bounds but SHALL NOT exceed a Rules of
Engagement ceiling enforced by governance policies.

---

# Configuration Structure

```yaml
tcp_client:

  timeouts:

  bounds:

  governance:

  observability:
```

---

# Timeouts

```yaml
timeouts:
  connect:
  read:
  write:
  deadline:
```

`connect`, `read`, and `write` SHALL be positive durations.

`deadline` SHALL bound the total operation and SHALL be greater than or equal to
`connect`.

---

# Bounds

```yaml
bounds:
  max_bytes:
  max_concurrent:
```

`max_bytes` SHALL bound bytes read per operation.

`max_concurrent` SHALL bound concurrent connections managed by the client.

---

# Governance

```yaml
governance:
  default_rate_limit_policy_id:
  default_retry_policy_id:
  default_proxy_id:
  require_proxy:
```

`default_rate_limit_policy_id`, `default_retry_policy_id`, and
`default_proxy_id` SHALL reference canonical policies applied when an invocation
omits its own.

`require_proxy` SHALL be a boolean. When `true`, connections SHALL be routed
through a proxy and direct egress SHALL be refused where governance prohibits it.

---

# Observability

```yaml
observability:
  emit_events:
  capture_evidence:
  metrics_enabled:
```

`emit_events` SHALL enable publication of lifecycle events.

`capture_evidence` SHALL enable connection evidence capture conforming to the
[Evidence schema](../../../schemas/evidence.md).

`metrics_enabled` SHALL enable metric exposure.

---

# Validation Rules

A valid configuration SHALL satisfy

- All timeouts are positive durations
- `deadline` is greater than or equal to `connect`
- `max_bytes` and `max_concurrent` are greater than or equal to `1`
- Referenced default policies exist and are valid
- No secret material appears in configuration

---

# Example Configuration

```yaml
tcp_client:

  timeouts:
    connect: 5s
    read: 10s
    write: 10s
    deadline: 30s

  bounds:
    max_bytes: 4MB
    max_concurrent: 64

  governance:
    default_rate_limit_policy_id: ratelimitpolicy-default-http
    default_retry_policy_id: retrypolicy-default-network
    default_proxy_id: proxy-corporate-egress
    require_proxy: false

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
