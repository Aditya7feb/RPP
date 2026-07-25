# FTP Client Configuration

**File:** `skills/shared/ftp-client/configuration.md`

**Version:** 1.0.0

---

# Purpose

This document defines the configuration model for the FTP Client Shared Skill.

Configuration determines security defaults, transfer and session bounds,
data-channel mode defaults, governance policy defaults, and observability.

Configuration is declarative and implementation independent, consistent with the
[Configuration Model](../../core/configuration-model.md).

---

# Configuration Sources

The FTP Client Shared Skill SHALL resolve configuration from the following
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
ftp_client:

  security:

  data_channel:

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

`default_tls_mode` SHALL be one of `none`, `explicit_optional`, or
`explicit_required`.

`require_tls_for_auth` SHALL be a boolean and SHALL default to `true`.
Authentication over cleartext SHALL NOT be permitted when `true`, except for
anonymous access where explicitly requested.

---

# Data Channel

```yaml
data_channel:
  default_mode:
  allow_active:
```

`default_mode` SHALL be one of `passive` or `active` and SHOULD default to
`passive`.

`allow_active` SHALL be a boolean gating active mode.

---

# Bounds

```yaml
bounds:
  max_transfer_bytes:
  session_timeout:
  command_timeout:
```

`max_transfer_bytes` SHALL bound a single transfer.

`session_timeout` and `command_timeout` SHALL bound session and command
durations.

---

# Governance

```yaml
governance:
  default_rate_limit_policy_id:
  default_retry_policy_id:
  default_proxy_id:
  allow_write_operations:
```

`default_rate_limit_policy_id`, `default_retry_policy_id`, and
`default_proxy_id` SHALL reference canonical policies applied when an invocation
omits its own.

`allow_write_operations` SHALL be a boolean gating write and delete commands,
which are treated as intrusive.

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
- `default_mode` is `passive` or `active`
- `max_transfer_bytes` is greater than or equal to `1`
- `session_timeout` and `command_timeout` are positive durations
- Referenced default policies exist and are valid
- No secret material appears in configuration

---

# Example Configuration

```yaml
ftp_client:

  security:
    default_tls_mode: explicit_required
    require_tls_for_auth: true

  data_channel:
    default_mode: passive
    allow_active: false

  bounds:
    max_transfer_bytes: 100MB
    session_timeout: 120s
    command_timeout: 30s

  governance:
    default_rate_limit_policy_id: ratelimitpolicy-default-http
    default_retry_policy_id: retrypolicy-default-network
    default_proxy_id: proxy-corporate-egress
    allow_write_operations: false

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
