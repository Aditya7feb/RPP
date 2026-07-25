# Evidence Configuration

**File:** `skills/shared/evidence/configuration.md`

**Version:** 1.0.0

---

# Purpose

This document defines the configuration model for the Evidence Shared Skill.

Configuration determines artifact backends, integrity settings, redaction rules,
scope policy, and retention.

Configuration is declarative and implementation independent, consistent with the
[Configuration Model](../../core/configuration-model.md).

---

# Configuration Sources

The Evidence Shared Skill SHALL resolve configuration from the following sources,
in increasing order of precedence.

```
Platform Defaults

↓

Assessment Configuration

↓

Consumer Configuration

↓

Invocation Override
```

A higher-precedence source MAY narrow scope or shorten retention but SHALL NOT
disable integrity sealing or redaction.

---

# Configuration Structure

```yaml
evidence:

  backends:

  integrity:

  redaction:

  scope_policy:

  retention:

  observability:
```

---

# Backends

```yaml
backends:
  - name:
    kind:
    max_artifact_bytes:
```

`backends` SHALL enumerate configured artifact stores.

`kind` SHALL identify an adapter kind without exposing implementation details.

`max_artifact_bytes` SHALL bound the size of a single artifact.

---

# Integrity

```yaml
integrity:
  seal:
  digest_algorithm:
```

`seal` SHALL be a boolean and SHALL default to `true`. Sealing SHALL NOT be
disabled through any configuration source.

`digest_algorithm` SHALL identify the algorithm used for content digests.

---

# Redaction

```yaml
redaction:
  enabled:
  patterns:
  fields:
```

`enabled` SHALL be a boolean and SHALL default to `true`. Redaction SHALL NOT be
disabled through any configuration source.

`patterns` SHALL describe value patterns treated as secrets.

`fields` SHALL list keys always redacted.

---

# Scope Policy

```yaml
scope_policy:
  default_scope:
  allow_cross_assessment:
```

`default_scope` SHALL be applied when a capture does not specify one.

`allow_cross_assessment` SHALL be a boolean. When `false`, evidence SHALL NOT be
resolvable outside its originating assessment.

Scope policy SHALL take precedence over capture scope requests.

---

# Retention

```yaml
retention:
  default_ttl:
  dispose_policy:
  record_disposal:
```

`default_ttl` SHALL bound evidence lifetime.

`dispose_policy` SHALL be one of `delete` or `archive`.

`record_disposal` SHALL be a boolean and SHALL default to `true`, preserving an
audit record of disposal.

---

# Observability

```yaml
observability:
  emit_events:
  metrics_enabled:
```

`emit_events` SHALL enable publication of lifecycle events.

`metrics_enabled` SHALL enable metric exposure.

---

# Validation Rules

A valid configuration SHALL satisfy

- At least one backend is configured
- `integrity.seal` is `true`
- `redaction.enabled` is `true`
- `dispose_policy` is one of `delete` or `archive`
- `record_disposal` is `true`
- No secret material appears in configuration

---

# Example Configuration

```yaml
evidence:

  backends:
    - name: primary
      kind: object-store
      max_artifact_bytes: 256MB

  integrity:
    seal: true
    digest_algorithm: sha-256

  redaction:
    enabled: true
    fields:
      - authorization
      - set-cookie
      - password
    patterns:
      - bearer-token
      - api-key

  scope_policy:
    default_scope: assessment
    allow_cross_assessment: false

  retention:
    default_ttl: 90d
    dispose_policy: archive
    record_disposal: true

  observability:
    emit_events: true
    metrics_enabled: true
```

---

# Related Documents

- [Interface](interface.md)
- [Execution](execution.md)
- [Evidence Schema](../../../schemas/evidence.md)
- [Configuration Model](../../core/configuration-model.md)
