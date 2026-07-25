# SMTP Client Configuration

**File:** `skills/shared/smtp-client/configuration.md`

**Version:** 1.0.0

---

# Purpose

This document defines the configuration model for the SMTP Client Shared Skill.

Configuration determines security defaults, session and message bounds,
governance policy defaults, and observability.

Configuration is declarative and implementation independent, consistent with the
[Configuration Model](../../core/configuration-model.md).

---

# Configuration Sources

The SMTP Client Shared Skill SHALL resolve configuration from the following
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

A higher-precedence source MAY strengthen security or tighten bounds but SHALL
NOT weaken a required-TLS setting.

---

# Configuration Structure

```yaml
smtp_client:

  security:

  bounds:

  governance:

  observability:
```

---

# Security

```yaml
security:
  default_tls_mode:
  require_tls_for_auth:
```

`default_tls_mode` SHALL be one of `none`, `starttls_optional`,
`starttls_required`, or `implicit`.

`require_tls_for_auth` SHALL be a boolean and SHALL default to `true`.
Authentication over cleartext SHALL NOT be permitted when `true`.

---

# Bounds

```yaml
bounds:
  max_message_bytes:
  max_recipients:
  session_timeout:
  command_timeout:
```

`max_message_bytes` SHALL bound message size.

`max_recipients` SHALL bound `RCPT TO` count per session.

`session_timeout` and `command_timeout` SHALL bound session and command
durations.

---

# Governance

```yaml
governance:
  default_rate_limit_policy_id:
  default_retry_policy_id:
  default_proxy_id:
  allow_message_send:
```

`default_rate_limit_policy_id`, `default_retry_policy_id`, and
`default_proxy_id` SHALL reference canonical policies applied when an invocation
omits its own.

`allow_message_send` SHALL be a boolean gating commands that transmit mail, which
are treated as intrusive and subject to authorization.

---

# Observability

```yaml
observability:
  emit_events:
  capture_evidence:
  metrics_enabled:
```

`emit_events` SHALL enable publication of lifecycle events.

`capture_evidence` SHALL enable session evidence capture conforming to the
[Evidence schema](../../../schemas/evidence.md).

`metrics_enabled` SHALL enable metric exposure.

---

# Validation Rules

A valid configuration SHALL satisfy

- `default_tls_mode` is one of the allowed modes
- `require_tls_for_auth` is `true`
- `max_message_bytes`, `max_recipients` are greater than or equal to `1`
- `session_timeout` and `command_timeout` are positive durations
- Referenced default policies exist and are valid
- No secret material appears in configuration

---

# Example Configuration

```yaml
smtp_client:

  security:
    default_tls_mode: starttls_required
    require_tls_for_auth: true

  bounds:
    max_message_bytes: 10MB
    max_recipients: 100
    session_timeout: 60s
    command_timeout: 15s

  governance:
    default_rate_limit_policy_id: ratelimitpolicy-default-http
    default_retry_policy_id: retrypolicy-default-network
    default_proxy_id: proxy-corporate-egress
    allow_message_send: false

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
