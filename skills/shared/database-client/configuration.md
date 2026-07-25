# Database Client Configuration

**File:** `skills/shared/database-client/configuration.md`

**Version:** 1.0.0

---

# Purpose

This document defines the configuration model for the Database Client Shared
Skill.

Configuration determines security defaults, result and statement bounds, write
gating, governance policy defaults, and observability.

Configuration is declarative and implementation independent, consistent with the
[Configuration Model](../../core/configuration-model.md).

---

# Configuration Sources

The Database Client Shared Skill SHALL resolve configuration from the following
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
NOT weaken a required-encryption setting or disable parameterization.

---

# Configuration Structure

```yaml
database_client:

  security:

  execution:

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

`default_tls_mode` SHALL be one of `disabled`, `preferred`, or `required`.

`require_tls_for_auth` SHALL be a boolean and SHALL default to `true`.
Authentication over cleartext SHALL NOT be permitted when `true`.

---

# Execution

```yaml
execution:
  allow_write_statements:
  allow_schema_changes:
  parameterization_enforced:
```

`allow_write_statements` and `allow_schema_changes` SHALL gate intrusive
operations and SHALL default to `false`.

`parameterization_enforced` SHALL be a boolean and SHALL default to `true`.
Parameterization SHALL NOT be disabled through any configuration source.

---

# Bounds

```yaml
bounds:
  max_rows:
  max_result_bytes:
  statement_timeout:
  connection_timeout:
```

`max_rows` and `max_result_bytes` SHALL bound returned result sets.

`statement_timeout` and `connection_timeout` SHALL bound statement and connection
durations.

---

# Governance

```yaml
governance:
  default_rate_limit_policy_id:
  default_retry_policy_id:
  default_proxy_id:
```

`default_rate_limit_policy_id`, `default_retry_policy_id`, and
`default_proxy_id` SHALL reference canonical policies applied when an invocation
omits its own.

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

- `default_tls_mode` is one of the allowed modes
- `require_tls_for_auth` is `true`
- `parameterization_enforced` is `true`
- `allow_write_statements` and `allow_schema_changes` default to `false`
- `max_rows` and `max_result_bytes` are greater than or equal to `1`
- `statement_timeout` and `connection_timeout` are positive durations
- Referenced default policies exist and are valid
- No secret material appears in configuration

---

# Example Configuration

```yaml
database_client:

  security:
    default_tls_mode: required
    require_tls_for_auth: true

  execution:
    allow_write_statements: false
    allow_schema_changes: false
    parameterization_enforced: true

  bounds:
    max_rows: 10000
    max_result_bytes: 64MB
    statement_timeout: 30s
    connection_timeout: 5s

  governance:
    default_rate_limit_policy_id: ratelimitpolicy-default-http
    default_retry_policy_id: retrypolicy-default-network
    default_proxy_id: proxy-corporate-egress

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
