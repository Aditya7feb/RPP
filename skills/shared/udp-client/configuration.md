# UDP Client Configuration

**File:** `skills/shared/udp-client/configuration.md`

**Version:** 1.0.0

---

# Purpose

This document defines the configuration model for the UDP Client Shared Skill.

Configuration determines default response windows, size bounds, governance
policy defaults, amplification protection, and observability.

Configuration is declarative and implementation independent, consistent with the
[Configuration Model](../../core/configuration-model.md).

---

# Configuration Sources

The UDP Client Shared Skill SHALL resolve configuration from the following
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

A higher-precedence source MAY tighten bounds but SHALL NOT exceed amplification
or Rules of Engagement ceilings.

---

# Configuration Structure

```yaml
udp_client:

  windows:

  bounds:

  amplification:

  governance:

  observability:
```

---

# Windows

```yaml
windows:
  response_window:
  deadline:
```

`response_window` SHALL be a positive duration bounding how long a response is
awaited.

`deadline` SHALL bound the total exchange.

---

# Bounds

```yaml
bounds:
  max_payload_bytes:
  max_response_bytes:
  max_concurrent:
```

`max_payload_bytes` SHALL bound datagram payload size.

`max_response_bytes` SHALL bound response intake.

`max_concurrent` SHALL bound concurrent exchanges.

---

# Amplification Protection

```yaml
amplification:
  max_response_ratio:
  enforce:
```

`max_response_ratio` SHALL bound the acceptable ratio of response size to sent
size, mitigating amplification abuse.

`enforce` SHALL be a boolean and SHALL default to `true`. Amplification
protection SHALL NOT be disabled through any configuration source.

---

# Governance

```yaml
governance:
  default_rate_limit_policy_id:
  default_retry_policy_id:
  allow_direct_egress:
```

`default_rate_limit_policy_id` and `default_retry_policy_id` SHALL reference
canonical policies applied when an invocation omits its own.

`allow_direct_egress` SHALL gate direct egress where UDP proxying is
unavailable.

---

# Observability

```yaml
observability:
  emit_events:
  capture_evidence:
  metrics_enabled:
```

`emit_events` SHALL enable publication of lifecycle events.

`capture_evidence` SHALL enable datagram evidence capture conforming to the
[Evidence schema](../../../schemas/evidence.md).

`metrics_enabled` SHALL enable metric exposure.

---

# Validation Rules

A valid configuration SHALL satisfy

- `response_window` and `deadline` are positive durations
- `max_payload_bytes`, `max_response_bytes`, and `max_concurrent` are greater
  than or equal to `1`
- `amplification.enforce` is `true`
- Referenced default policies exist and are valid
- No secret material appears in configuration

---

# Example Configuration

```yaml
udp_client:

  windows:
    response_window: 2s
    deadline: 5s

  bounds:
    max_payload_bytes: 1400
    max_response_bytes: 64KB
    max_concurrent: 128

  amplification:
    max_response_ratio: 4
    enforce: true

  governance:
    default_rate_limit_policy_id: ratelimitpolicy-dns
    default_retry_policy_id: retrypolicy-default-network
    allow_direct_egress: true

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
