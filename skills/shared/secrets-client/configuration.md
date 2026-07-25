# Secrets Client Configuration

**File:** `skills/shared/secrets-client/configuration.md`

**Version:** 1.0.0

---

# Purpose

This document defines the configuration model for the Secrets Client Shared
Skill.

Configuration determines secret stores, handle lifetime, lease behavior,
redaction enforcement, and observability.

Configuration is declarative and implementation independent, consistent with the
[Configuration Model](../../core/configuration-model.md).

---

# Configuration Sources

The Secrets Client Shared Skill SHALL resolve configuration from the following
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

A higher-precedence source MAY shorten handle lifetime but SHALL NOT disable
redaction or enable value return.

---

# Configuration Structure

```yaml
secrets_client:

  stores:

  handles:

  redaction:

  observability:
```

---

# Stores

```yaml
stores:
  - store_id:
    kind:
    namespace:
```

`stores` SHALL enumerate the configured secret stores.

`kind` SHALL identify the store kind without exposing implementation detail.

`namespace` SHALL bound the references resolvable from the store.

Store configuration SHALL NOT contain secret values.

---

# Handles

```yaml
handles:
  max_lifetime:
  renew_before_expiry:
  clear_on_expiry:
```

`max_lifetime` SHALL bound how long a handle remains valid.

`renew_before_expiry` SHALL define when leases are renewed.

`clear_on_expiry` SHALL be a boolean and SHALL default to `true`, ensuring any
in-memory retention is cleared on expiry.

---

# Redaction

```yaml
redaction:
  enforce:
  never_return_values:
```

`enforce` SHALL be a boolean and SHALL default to `true`. Redaction SHALL NOT be
disabled through any configuration source.

`never_return_values` SHALL be a boolean and SHALL default to `true`. Returning
secret values to general consumers SHALL NOT be enabled.

---

# Observability

```yaml
observability:
  emit_events:
  capture_evidence:
  metrics_enabled:
```

`emit_events` SHALL enable publication of lifecycle events without values.

`capture_evidence` SHALL enable non-sensitive access evidence conforming to the
[Evidence schema](../../../schemas/evidence.md).

`metrics_enabled` SHALL enable metric exposure.

---

# Validation Rules

A valid configuration SHALL satisfy

- Every store defines a `store_id`, `kind`, and `namespace`
- Store identifiers are unique
- `max_lifetime` is a positive duration
- `clear_on_expiry` is `true`
- `redaction.enforce` is `true`
- `never_return_values` is `true`
- No secret material appears in configuration

---

# Example Configuration

```yaml
secrets_client:

  stores:
    - store_id: engagement-vault
      kind: managed-store
      namespace: asmt-42

  handles:
    max_lifetime: 15m
    renew_before_expiry: 2m
    clear_on_expiry: true

  redaction:
    enforce: true
    never_return_values: true

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
