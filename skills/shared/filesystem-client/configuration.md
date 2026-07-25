# Filesystem Client Configuration

**File:** `skills/shared/filesystem-client/configuration.md`

**Version:** 1.0.0

---

# Purpose

This document defines the configuration model for the Filesystem Client Shared
Skill.

Configuration determines roots, confinement policy, size and depth bounds, write
gating, governance policy defaults, and observability.

Configuration is declarative and implementation independent, consistent with the
[Configuration Model](../../core/configuration-model.md).

---

# Configuration Sources

The Filesystem Client Shared Skill SHALL resolve configuration from the following
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

A higher-precedence source MAY narrow roots or tighten bounds but SHALL NOT widen
a root or disable confinement.

---

# Configuration Structure

```yaml
filesystem_client:

  roots:

  confinement:

  execution:

  bounds:

  governance:

  observability:
```

---

# Roots

```yaml
roots:
  - root_id:
    backend:
    base:
    writable:
```

`roots` SHALL enumerate the configured roots.

`backend` SHALL identify the backend kind, such as `local`, `remote`, or
`container`, without exposing implementation detail.

`base` SHALL be the canonical base path of the root.

`writable` SHALL be a boolean gating writes to the root.

---

# Confinement

```yaml
confinement:
  enforce:
  follow_symlinks:
```

`enforce` SHALL be a boolean and SHALL default to `true`. Confinement SHALL NOT
be disabled through any configuration source.

`follow_symlinks` SHALL be a boolean. When `true`, links SHALL be followed only
where they resolve within the root.

---

# Execution

```yaml
execution:
  allow_write:
  allow_delete:
```

`allow_write` and `allow_delete` SHALL gate intrusive operations and SHALL
default to `false`.

A write SHALL require both `allow_write` and a `writable` root.

---

# Bounds

```yaml
bounds:
  max_read_bytes:
  max_write_bytes:
  max_list_entries:
  max_depth:
```

`max_read_bytes` and `max_write_bytes` SHALL bound content sizes.

`max_list_entries` and `max_depth` SHALL bound listings.

---

# Governance

```yaml
governance:
  default_rate_limit_policy_id:
  default_retry_policy_id:
```

`default_rate_limit_policy_id` and `default_retry_policy_id` SHALL reference
canonical policies applied when an invocation omits its own.

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

- Every root defines a `root_id`, `backend`, and `base`
- Root identifiers are unique
- `confinement.enforce` is `true`
- `allow_write` and `allow_delete` default to `false`
- `max_read_bytes`, `max_write_bytes`, `max_list_entries`, and `max_depth` are
  greater than or equal to `1`
- Referenced default policies exist and are valid
- No secret material appears in configuration

---

# Example Configuration

```yaml
filesystem_client:

  roots:
    - root_id: staging
      backend: local
      base: /var/rpp/staging
      writable: true
    - root_id: target-host
      backend: remote
      base: /etc
      writable: false

  confinement:
    enforce: true
    follow_symlinks: false

  execution:
    allow_write: false
    allow_delete: false

  bounds:
    max_read_bytes: 64MB
    max_write_bytes: 64MB
    max_list_entries: 10000
    max_depth: 8

  governance:
    default_rate_limit_policy_id: ratelimitpolicy-default-http
    default_retry_policy_id: retrypolicy-default-network

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
