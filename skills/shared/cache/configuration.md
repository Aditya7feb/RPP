# Cache Configuration

**File:** `skills/shared/cache/configuration.md`

**Version:** 1.0.0

---

# Purpose

This document defines the configuration model for the Cache Shared Skill.

Configuration determines cache namespaces, freshness defaults, scope policy,
eviction budgets, and observability.

Configuration is declarative and implementation independent, consistent with the
[Configuration Model](../../core/configuration-model.md).

---

# Configuration Sources

The Cache Shared Skill SHALL resolve configuration from the following sources, in
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

A higher-precedence source MAY shorten freshness or narrow scope but SHALL NOT
extend `global` reuse where policy prohibits it.

---

# Configuration Structure

```yaml
cache:

  namespaces:

  defaults:

  scope_policy:

  eviction:

  observability:
```

---

# Namespaces

```yaml
namespaces:
  - name:
    default_ttl:
    max_entries:
    max_bytes:
```

`namespaces` SHALL enumerate the logical caches, such as `dns`, `tls`, and
`http`.

Each namespace SHALL define freshness and budget defaults.

---

# Defaults

```yaml
defaults:
  ttl:
  stale_while_revalidate:
  scope:
```

`defaults` SHALL provide freshness and scope defaults applied when a namespace
or invocation does not specify them.

---

# Scope Policy

```yaml
scope_policy:
  allow_global:
  session_isolation:
```

`allow_global` SHALL be a boolean. When `false`, `global` scope SHALL be
downgraded to `assessment` scope.

`session_isolation` SHALL be a boolean requiring strict isolation of `session`
entries.

Scope policy SHALL take precedence over invocation scope requests.

---

# Eviction

```yaml
eviction:
  policy:
  high_watermark:
  low_watermark:
```

`policy` SHALL be one of `lru`, `lfu`, or `ttl`.

`high_watermark` and `low_watermark` SHALL bound cache occupancy, triggering
eviction when the high watermark is reached and stopping at the low watermark.

---

# Observability

```yaml
observability:
  emit_events:
  capture_evidence:
  metrics_enabled:
```

`emit_events` SHALL enable publication of lifecycle events.

`capture_evidence` SHALL enable lookup evidence capture conforming to the
[Evidence schema](../../../schemas/evidence.md).

`metrics_enabled` SHALL enable metric exposure.

---

# Resolution Order

The Cache Shared Skill SHALL resolve freshness and scope as follows.

```
Invocation Override

↓ (if absent)

Namespace Setting

↓ (if absent)

Defaults

↓

Apply Scope Policy
```

---

# Validation Rules

A valid configuration SHALL satisfy

- Namespace names are unique
- `default_ttl` and `defaults.ttl` are non-negative durations
- `eviction.policy` is one of `lru`, `lfu`, or `ttl`
- `low_watermark` is less than `high_watermark`
- When `allow_global` is `false`, no resolved scope is `global`
- No secret material appears in configuration

---

# Example Configuration

```yaml
cache:

  namespaces:
    - name: dns
      default_ttl: 300s
      max_entries: 10000
      max_bytes: 16MB
    - name: tls
      default_ttl: 600s
      max_entries: 5000
      max_bytes: 32MB
    - name: http
      default_ttl: 60s
      max_entries: 20000
      max_bytes: 128MB

  defaults:
    ttl: 120s
    stale_while_revalidate: 30s
    scope: assessment

  scope_policy:
    allow_global: false
    session_isolation: true

  eviction:
    policy: lru
    high_watermark: 0.9
    low_watermark: 0.7

  observability:
    emit_events: true
    capture_evidence: true
    metrics_enabled: true
```

---

# Configuration Precedence Summary

| Source | May Shorten Freshness | May Extend Global Reuse |
|--------|-----------------------|--------------------------|
| Platform Defaults | Yes | No |
| Assessment Configuration | Yes | No |
| Consumer Configuration | Yes | No |
| Invocation Override | Yes | No |

---

# Related Documents

- [Interface](interface.md)
- [Execution](execution.md)
- [Cache Entry Schema](../../../schemas/cache-entry.md)
- [Configuration Model](../../core/configuration-model.md)
