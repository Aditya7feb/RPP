# WebSocket Client Configuration

**File:** `skills/shared/websocket-client/configuration.md`

**Version:** 1.0.0

---

# Purpose

This document defines the configuration model for the WebSocket Client Shared
Skill.

Configuration determines message and lifetime bounds, negotiation defaults,
governance policy defaults, and observability.

Configuration is declarative and implementation independent, consistent with the
[Configuration Model](../../core/configuration-model.md).

---

# Configuration Sources

The WebSocket Client Shared Skill SHALL resolve configuration from the following
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
websocket_client:

  bounds:

  negotiation:

  governance:

  observability:
```

---

# Bounds

```yaml
bounds:
  max_message_bytes:
  max_fragment_bytes:
  max_connection_lifetime:
  handshake_timeout:
  idle_timeout:
```

`max_message_bytes` and `max_fragment_bytes` SHALL bound frame sizes.

`max_connection_lifetime` SHALL bound total connection duration.

`handshake_timeout` and `idle_timeout` SHALL bound handshake and idle periods.

---

# Negotiation

```yaml
negotiation:
  default_subprotocols:
  allow_extensions:
```

`default_subprotocols` SHALL provide a default preference list.

`allow_extensions` SHALL enumerate permitted extensions.

---

# Governance

```yaml
governance:
  default_rate_limit_policy_id:
  default_retry_policy_id:
  default_proxy_id:
  pace_outbound_frames:
```

`default_rate_limit_policy_id`, `default_retry_policy_id`, and
`default_proxy_id` SHALL reference canonical policies applied when an invocation
omits its own.

`pace_outbound_frames` SHALL be a boolean enabling per-frame pacing for
high-volume connections.

---

# Observability

```yaml
observability:
  emit_events:
  capture_evidence:
  metrics_enabled:
```

`emit_events` SHALL enable publication of lifecycle events.

`capture_evidence` SHALL enable WebSocket evidence capture conforming to the
[Evidence schema](../../../schemas/evidence.md).

`metrics_enabled` SHALL enable metric exposure.

---

# Validation Rules

A valid configuration SHALL satisfy

- `max_message_bytes` is greater than or equal to `max_fragment_bytes`
- `max_connection_lifetime`, `handshake_timeout`, and `idle_timeout` are
  positive durations
- Referenced default policies exist and are valid
- No secret material appears in configuration

---

# Example Configuration

```yaml
websocket_client:

  bounds:
    max_message_bytes: 1MB
    max_fragment_bytes: 64KB
    max_connection_lifetime: 10m
    handshake_timeout: 10s
    idle_timeout: 60s

  negotiation:
    default_subprotocols: []
    allow_extensions:
      - permessage-deflate

  governance:
    default_rate_limit_policy_id: ratelimitpolicy-default-http
    default_retry_policy_id: retrypolicy-default-network
    default_proxy_id: proxy-corporate-egress
    pace_outbound_frames: false

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
