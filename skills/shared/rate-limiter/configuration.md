# Rate Limiter Configuration

**File:** `skills/shared/rate-limiter/configuration.md`

**Version:** 1.0.0

---

# Purpose

This document defines the configuration model for the Rate Limiter Shared Skill.

Configuration determines which [Rate Limit Policy](../../../schemas/rate-limit-policy.md)
applies to an operation, how policies are resolved, and how governance ceilings
are enforced.

Configuration is declarative and implementation independent, consistent with the
[Configuration Model](../../core/configuration-model.md).

---

# Configuration Sources

The Rate Limiter SHALL resolve configuration from the following sources, in
increasing order of precedence.

```
Platform Defaults

↓

Assessment Configuration

↓

Consumer Configuration

↓

Invocation Override
```

A higher-precedence source MAY narrow a limit but SHALL NOT exceed a Rules of
Engagement ceiling established by `roe_binding.enforced`.

---

# Configuration Structure

```yaml
rate_limiter:

  default_policy_id:

  policies:

  scope_defaults:

  governance:

  observability:
```

---

# Default Policy

```yaml
default_policy_id:
```

`default_policy_id` SHALL reference a
[Rate Limit Policy](../../../schemas/rate-limit-policy.md) applied when a
consumer does not specify one.

The default policy SHALL exist and SHALL be valid.

---

# Policy Registry

```yaml
policies:
  - policy_id:
    ref:
```

`policies` SHALL enumerate the rate-limit policies available within the
configuration namespace.

Each entry SHALL reference a valid Rate Limit Policy object.

Policy identifiers SHALL be unique.

---

# Scope Defaults

```yaml
scope_defaults:
  host_normalization:
  credential_keying:
```

`host_normalization` SHALL describe how hosts are normalized before keying,
such as lowercasing and default-port collapsing, so that equivalent hosts share
a scope.

`credential_keying` SHALL describe how a principal is keyed for
`per_credential` scope without exposing secret material.

Scope defaults SHALL NOT contain secrets.

---

# Governance

```yaml
governance:
  roe_ceiling_policy_id:
  enforce_ceiling:
```

`roe_ceiling_policy_id` SHALL reference the Rate Limit Policy that expresses the
Rules of Engagement ceiling.

`enforce_ceiling` SHALL be a boolean. When `true`, the Rate Limiter SHALL reject
any resolved policy or override whose bounds exceed the ceiling.

Governance settings SHALL take precedence over all other configuration.

---

# Observability

```yaml
observability:
  emit_events:
  capture_evidence:
  metrics_enabled:
```

`emit_events` SHALL enable publication of lifecycle events to the Execution
State.

`capture_evidence` SHALL enable per-decision evidence capture conforming to the
[Evidence schema](../../../schemas/evidence.md).

`metrics_enabled` SHALL enable metric exposure.

---

# Policy Resolution Order

The Rate Limiter SHALL resolve the effective policy as follows.

```
Invocation Override

↓ (if absent)

Consumer Policy Reference

↓ (if absent)

Default Policy
```

The resolved policy SHALL then be validated against the governance ceiling
before use.

---

# Validation Rules

A valid configuration SHALL satisfy

- `default_policy_id` references an existing policy
- Every entry in `policies` references a valid Rate Limit Policy
- Policy identifiers are unique
- `governance.roe_ceiling_policy_id` references an existing policy when
  `enforce_ceiling` is `true`
- No resolved policy exceeds the governance ceiling
- No secret material appears in configuration

---

# Example Configuration

```yaml
rate_limiter:

  default_policy_id: ratelimitpolicy-default-http

  policies:
    - policy_id: ratelimitpolicy-default-http
      ref: schemas/rate-limit-policy.md
    - policy_id: ratelimitpolicy-dns
      ref: schemas/rate-limit-policy.md
    - policy_id: ratelimitpolicy-roe-ceiling
      ref: schemas/rate-limit-policy.md

  scope_defaults:
    host_normalization: lowercase-collapse-default-port
    credential_keying: principal-id-hash

  governance:
    roe_ceiling_policy_id: ratelimitpolicy-roe-ceiling
    enforce_ceiling: true

  observability:
    emit_events: true
    capture_evidence: true
    metrics_enabled: true
```

---

# Configuration Precedence Summary

| Source | May Narrow | May Exceed Ceiling |
|--------|------------|--------------------|
| Platform Defaults | Yes | No |
| Assessment Configuration | Yes | No |
| Consumer Configuration | Yes | No |
| Invocation Override | Yes | No |

---

# Related Documents

- [Interface](interface.md)
- [Execution](execution.md)
- [Rate Limit Policy Schema](../../../schemas/rate-limit-policy.md)
- [Configuration Model](../../core/configuration-model.md)
