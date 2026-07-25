# Cloud Storage Client Configuration

**File:** `skills/shared/cloud-storage-client/configuration.md`

**Version:** 1.0.0

---

# Purpose

This document defines the configuration model for the Cloud Storage Client Shared
Skill.

Configuration determines authorized scopes, encryption requirements, object and
listing bounds, presigned-reference lifetime, write gating, governance policy
defaults, and observability.

Configuration is declarative and implementation independent, consistent with the
[Configuration Model](../../core/configuration-model.md).

---

# Configuration Sources

The Cloud Storage Client Shared Skill SHALL resolve configuration from the
following sources, in increasing order of precedence.

```
Platform Defaults

↓

Assessment Configuration

↓

Consumer Configuration

↓

Invocation Override
```

A higher-precedence source MAY narrow scopes or tighten bounds but SHALL NOT
widen a scope or weaken required encryption.

---

# Configuration Structure

```yaml
cloud_storage_client:

  scopes:

  encryption:

  execution:

  bounds:

  presign:

  governance:

  observability:
```

---

# Scopes

```yaml
scopes:
  - scope_id:
    provider:
    bucket:
    prefix:
    writable:
```

`scopes` SHALL enumerate the authorized bucket-and-prefix scopes.

`provider` SHALL identify the provider kind without exposing implementation
detail.

`writable` SHALL be a boolean gating writes to the scope.

---

# Encryption

```yaml
encryption:
  require_server_side:
  default_mode:
```

`require_server_side` SHALL be a boolean and SHALL default to `true`. Writes
without server-side encryption SHALL be refused when `true`.

`default_mode` SHALL declare the default encryption mode.

---

# Execution

```yaml
execution:
  allow_write:
  allow_delete:
  allow_policy_changes:
```

`allow_write`, `allow_delete`, and `allow_policy_changes` SHALL gate intrusive
operations and SHALL default to `false`.

---

# Bounds

```yaml
bounds:
  max_object_bytes:
  max_list_keys:
```

`max_object_bytes` SHALL bound object read and write sizes.

`max_list_keys` SHALL bound listing volume.

---

# Presign

```yaml
presign:
  max_ttl:
  allow_presign:
```

`max_ttl` SHALL bound presigned-reference lifetime.

`allow_presign` SHALL gate presigned-reference generation.

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

- Every scope defines a `scope_id`, `provider`, and `bucket`
- Scope identifiers are unique
- `require_server_side` is `true`
- `allow_write`, `allow_delete`, and `allow_policy_changes` default to `false`
- `max_object_bytes` and `max_list_keys` are greater than or equal to `1`
- `max_ttl` is a positive, bounded duration
- Referenced default policies exist and are valid
- No secret material appears in configuration

---

# Example Configuration

```yaml
cloud_storage_client:

  scopes:
    - scope_id: target-public-audit
      provider: object-store
      bucket: target-assets
      prefix: public/
      writable: false
    - scope_id: staging
      provider: object-store
      bucket: rpp-staging
      prefix: asmt-42/
      writable: true

  encryption:
    require_server_side: true
    default_mode: provider-managed

  execution:
    allow_write: false
    allow_delete: false
    allow_policy_changes: false

  bounds:
    max_object_bytes: 128MB
    max_list_keys: 5000

  presign:
    max_ttl: 5m
    allow_presign: false

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
