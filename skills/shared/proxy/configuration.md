# Proxy Configuration

**File:** `skills/shared/proxy/configuration.md`

**Version:** 1.0.0

---

# Purpose

This document defines the configuration model for the Proxy Shared Skill.

Configuration determines which
[Proxy Configuration](../../../schemas/proxy-configuration.md) objects are
available, how proxies are selected, and how failure and governance behavior is
applied.

Configuration is declarative and implementation independent, consistent with the
[Configuration Model](../../core/configuration-model.md).

---

# Configuration Sources

The Proxy Shared Skill SHALL resolve configuration from the following sources, in
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

A higher-precedence source MAY change proxy selection but SHALL NOT permit
direct egress where Rules of Engagement prohibit it.

---

# Configuration Structure

```yaml
proxy:

  proxy_set:

  default_behavior:

  governance:

  observability:
```

---

# Proxy Set

```yaml
proxy_set:
  - proxy_id:
    ref:
```

`proxy_set` SHALL enumerate the available proxy configurations within the
namespace.

Each entry SHALL reference a valid
[Proxy Configuration](../../../schemas/proxy-configuration.md).

Proxy identifiers SHALL be unique.

---

# Default Behavior

```yaml
default_behavior:
  when_no_match:
  on_failure:
```

`when_no_match` SHALL be one of `direct` or `fail`, describing routing when no
proxy matches a destination.

`on_failure` SHALL provide the default `on_failure` behavior for proxies that do
not specify one.

---

# Governance

```yaml
governance:
  allow_direct_egress:
  require_proxy_schemes:
```

`allow_direct_egress` SHALL be a boolean. When `false`, no bypass, no-match, or
fallback path SHALL result in direct egress, and unmatched destinations SHALL
fail.

`require_proxy_schemes` SHALL be an array of schemes that MUST be proxied.

Governance settings SHALL take precedence over all other configuration.

---

# Observability

```yaml
observability:
  emit_events:
  capture_evidence:
  metrics_enabled:
```

`emit_events` SHALL enable publication of lifecycle events.

`capture_evidence` SHALL enable routing evidence capture conforming to the
[Evidence schema](../../../schemas/evidence.md).

`metrics_enabled` SHALL enable metric exposure.

---

# Selection Resolution Order

The Proxy Shared Skill SHALL resolve routing as follows.

```
Evaluate Bypass Rules

↓ (no bypass)

Evaluate Governance require_proxy_schemes

↓

Select Most-Specific Matching Proxy

↓ (no match)

Apply when_no_match (subject to allow_direct_egress)
```

---

# Validation Rules

A valid configuration SHALL satisfy

- Every entry in `proxy_set` references a valid Proxy Configuration
- Proxy identifiers are unique
- `when_no_match` is one of `direct` or `fail`
- When `governance.allow_direct_egress` is `false`, `when_no_match` is `fail`
- No secret material appears in configuration

---

# Example Configuration

```yaml
proxy:

  proxy_set:
    - proxy_id: proxy-corporate-egress
      ref: schemas/proxy-configuration.md
    - proxy_id: proxy-testing-intercept
      ref: schemas/proxy-configuration.md

  default_behavior:
    when_no_match: fail
    on_failure: fail

  governance:
    allow_direct_egress: false
    require_proxy_schemes:
      - http
      - https

  observability:
    emit_events: true
    capture_evidence: true
    metrics_enabled: true
```

---

# Configuration Precedence Summary

| Source | May Change Selection | May Force Direct Egress |
|--------|----------------------|--------------------------|
| Platform Defaults | Yes | No |
| Assessment Configuration | Yes | No |
| Consumer Configuration | Yes | No |
| Invocation Override | Yes | No |

---

# Related Documents

- [Interface](interface.md)
- [Execution](execution.md)
- [Proxy Configuration Schema](../../../schemas/proxy-configuration.md)
- [Configuration Model](../../core/configuration-model.md)
